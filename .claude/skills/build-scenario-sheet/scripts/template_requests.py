#!/usr/bin/env python3
"""Build one Sheets batchUpdate that puts an old scenario sheet on the new template layout.

The template's data tabs carry example screenshots that the API can't remove, so they
aren't copied. Instead this rebuilds each tab from the template's formatting (header
cells and notes, column widths, data-row format, Choices rating colors), fills it with
the rows from sheet_from_code.py, deletes the replaced old tabs and puts the copied
Info tab first. Tabs it doesn't replace (Call Choices, Copy of Choices...) stay as they are.

    python3 template_requests.py --template template-format.json --migration migration.json
        --existing existing-props.json --info-sheet-id 123 --replace "Meta,Stages,..." --out requests.json

template-format.json: get_spreadsheet on the template with grid data for row 1-3 of each
data tab (see the skill's migrate steps). existing-props.json: get_spreadsheet
fields ["sheets.properties"] on the sheet being migrated.
"""
import argparse
import copy
import json

TABS = ["Meta", "Stages", "Screens", "Choices", "Articles"]
DATA_FG = {"red": 0.2, "green": 0.2, "blue": 0.2}  # #333333, template example rows are grey italic


def value(v):
    if isinstance(v, bool):
        return {"stringValue": "Y" if v else ""}
    if isinstance(v, (int, float)):
        return {"numberValue": v}
    return {"stringValue": "" if v is None else str(v)}


def slim(x):
    """Drop the *Style twins Sheets returns next to each color (colorStyle beside color...)."""
    if isinstance(x, dict):
        return {k: slim(v) for k, v in x.items() if not (k.endswith("Style") and k[:-5] in x)}
    if isinstance(x, list):
        return [slim(v) for v in x]
    return x


def data_format(fmt):
    f = slim(copy.deepcopy(fmt or {}))
    tf = f.setdefault("textFormat", {})
    tf["italic"] = False
    tf["foregroundColor"] = DATA_FG
    tf.pop("foregroundColorStyle", None)
    tf.pop("link", None)  # the example row's hyperlink would otherwise land on every cell
    return f


def trim(cells):
    """Empty cells as {} and no trailing empties: the tab is new, so nothing needs clearing."""
    cells = [c if c.get("userEnteredValue") != {"stringValue": ""} or "note" in c else {} for c in cells]
    while cells and cells[-1] == {}:
        cells.pop()
    return cells


def main():
    ap = argparse.ArgumentParser()
    for k in ("template", "migration", "existing", "out"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--info-sheet-id", type=int, required=True)
    ap.add_argument("--replace", required=True, help="comma-separated old tab titles to delete")
    ap.add_argument("--copied", help='JSON {"Meta": sheetId, ...}: the five data tabs were copied from an '
                                     "already-migrated sheet, so only clear their values and notes, add this "
                                     "sheet's asset labels and notes, and swap tabs (implies --no-values)")
    ap.add_argument("--no-values", action="store_true",
                    help="layout, headers, Meta labels and cell notes only; write the values with "
                         "update_values from sheet-values.json (smaller calls)")
    a = ap.parse_args()

    tpl = {s["properties"]["title"]: s for s in json.load(open(a.template))["sheets"]}
    mig = json.load(open(a.migration))
    existing = json.load(open(a.existing))["sheets"]
    titles = {s["properties"]["title"]: s["properties"]["sheetId"] for s in existing}
    used = set(titles.values()) | {a.info_sheet_id}
    replace = [t.strip() for t in a.replace.split(",") if t.strip()]
    missing = [t for t in replace if t not in titles]
    if missing:
        raise SystemExit(f"Not in the sheet: {missing}. Tabs there: {list(titles)}")

    notes = {}
    for tab, row, col, text in mig["cell_notes"]:
        notes[(tab, row, col)] = text

    reqs, new_ids = [], {}
    if a.copied:
        return copied_requests(a, json.loads(a.copied), tpl, mig, titles, replace, notes)
    base = 910000000
    for i, tab in enumerate(TABS):
        sid = base + i
        while sid in used:
            sid += 17
        used.add(sid)
        new_ids[tab] = sid
        t = tpl[tab]
        grid = t["data"][0]
        rows = grid.get("rowData", [])
        head = rows[0]["values"]
        ncols = sum(1 for c in head if "userEnteredValue" in c)
        sample = rows[1]["values"] if len(rows) > 1 else []
        data = mig["tabs"][tab]
        nrows = max(1000, len(data) + 200)
        reqs.append({"addSheet": {"properties": {
            "sheetId": sid, "title": f"_new_{tab}", "index": i + 1,
            "gridProperties": {"rowCount": nrows, "columnCount": t["properties"]["gridProperties"]["columnCount"],
                               "frozenRowCount": 1, "hideGridlines": True}}}})
        for c, meta in enumerate(grid.get("columnMetadata", [])[:ncols + 1]):
            if meta.get("pixelSize"):
                reqs.append({"updateDimensionProperties": {
                    "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": c, "endIndex": c + 1},
                    "properties": {"pixelSize": meta["pixelSize"]}, "fields": "pixelSize"}})
        h = grid.get("rowMetadata", [{}])[0].get("pixelSize")
        if h:
            reqs.append({"updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": h}, "fields": "pixelSize"}})

        fmts = [data_format(sample[c].get("userEnteredFormat") if c < len(sample) else {}) for c in range(ncols)]
        # Data-row format once per run of same-format columns (row 2 down); cells then carry values only.
        c = 0
        while c < ncols:
            end = c + 1
            while end < ncols and fmts[end] == fmts[c]:
                end += 1
            reqs.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": nrows,
                                                  "startColumnIndex": c, "endColumnIndex": end},
                                        "cell": {"userEnteredFormat": fmts[c]}, "fields": "userEnteredFormat"}})
            c = end
        out_rows = [{"values": [slim({k: v for k, v in cell.items()
                                      if k in ("userEnteredValue", "userEnteredFormat", "note", "textFormatRuns")})
                                for cell in head[:ncols]]}]
        for r, row in enumerate(data):
            cells = []
            for c in range(ncols):
                v = row[c] if c < len(row) else ""
                if tab == "Meta" and c == 0:
                    if r < mig["meta_fixed_rows"]:  # the template's own label + help text, as is
                        src = rows[r + 1]["values"][0]
                        cells.append(slim({k: src[k] for k in ("userEnteredValue", "userEnteredFormat",
                                                               "textFormatRuns") if k in src}))
                        continue
                    src = slim(rows[1]["values"][0])  # asset row: bold name line, grey help line
                    first = str(v).split("\n")[0]
                    runs = src.get("textFormatRuns", [])
                    cell = {"userEnteredValue": value(v), "userEnteredFormat": src.get("userEnteredFormat", {})}
                    if len(runs) >= 2 and "\n" in str(v):
                        cell["textFormatRuns"] = [{"startIndex": 0, "format": runs[0].get("format", {})},
                                                  {"startIndex": len(first), "format": runs[1].get("format", {})}]
                    cells.append(cell)
                    continue
                cell = {"userEnteredValue": value(v)}
                if (tab, r, c) in notes:
                    cell["note"] = notes[(tab, r, c)]
                cells.append(cell)
            out_rows.append({"values": cells if tab == "Meta" else trim(cells)})
        # Header + Meta labels set their own format; data cells keep the column format above.
        reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 0, "columnIndex": 0}, "rows": out_rows[:1],
                                     "fields": "userEnteredValue,userEnteredFormat,note,textFormatRuns"}})
        if tab == "Meta":
            reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 1, "columnIndex": 0},
                                         "rows": [{"values": r["values"][:1]} for r in out_rows[1:]],
                                         "fields": "userEnteredValue,userEnteredFormat,textFormatRuns"}})
            if not a.no_values:
                reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 1, "columnIndex": 1},
                                             "rows": [{"values": r["values"][1:]} for r in out_rows[1:]],
                                             "fields": "userEnteredValue"}})
        elif not a.no_values:
            reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 1, "columnIndex": 0},
                                         "rows": out_rows[1:], "fields": "userEnteredValue,note"}})
        else:
            for (nt, r, c), text in notes.items():
                if nt == tab:
                    reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": r + 1, "columnIndex": c},
                                                 "rows": [{"values": [{"note": text}]}], "fields": "note"}})
        for rule in t.get("conditionalFormats", []):
            r2 = slim(copy.deepcopy(rule))
            r2["ranges"] = [{"sheetId": sid, "startRowIndex": 1, "endRowIndex": nrows,
                             "startColumnIndex": 0, "endColumnIndex": ncols}]
            reqs.append({"addConditionalFormatRule": {"rule": r2, "index": 0}})

    for t in replace:
        reqs.append({"deleteSheet": {"sheetId": titles[t]}})
    for tab, sid in new_ids.items():
        reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "title": tab}, "fields": "title"}})
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": a.info_sheet_id, "title": "Info", "index": 0},
                                           "fields": "title,index"}})
    for i, tab in enumerate(TABS):
        reqs.append({"updateSheetProperties": {"properties": {"sheetId": new_ids[tab], "index": i + 1},
                                               "fields": "index"}})
    json.dump(reqs, open(a.out, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"{len(reqs)} requests, {len(json.dumps(reqs, ensure_ascii=False)) // 1000} KB -> {a.out}")
    print("New tab ids:", new_ids)


def copied_requests(a, ids, tpl, mig, titles, replace, notes):
    """Tabs copied from a migrated sheet keep its formatting; wipe its content, then swap tabs."""
    reqs = []
    for tab in TABS:
        sid = ids[tab]
        if tab == "Meta":  # keep the label rows' column A; clear values and any asset rows
            fixed = mig["meta_fixed_rows"]
            reqs.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 1000,
                                                  "startColumnIndex": 1, "endColumnIndex": 2},
                                        "cell": {}, "fields": "userEnteredValue,note"}})
            reqs.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": fixed + 1, "endRowIndex": 1000,
                                                  "startColumnIndex": 0, "endColumnIndex": 1},
                                        "cell": {}, "fields": "userEnteredValue,note,textFormatRuns"}})
            src = slim(tpl["Meta"]["data"][0]["rowData"][1]["values"][0])
            runs = src.get("textFormatRuns", [])
            rows = []
            for r in mig["tabs"]["Meta"][fixed:]:
                first = str(r[0]).split("\n")[0]
                cell = {"userEnteredValue": value(r[0])}
                if len(runs) >= 2 and "\n" in str(r[0]):
                    cell["textFormatRuns"] = [{"startIndex": 0, "format": runs[0].get("format", {})},
                                              {"startIndex": len(first), "format": runs[1].get("format", {})}]
                rows.append({"values": [cell]})
            if rows:
                reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": fixed + 1, "columnIndex": 0},
                                             "rows": rows, "fields": "userEnteredValue,textFormatRuns"}})
        else:
            reqs.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 1000,
                                                  "startColumnIndex": 0, "endColumnIndex": 26},
                                        "cell": {}, "fields": "userEnteredValue,note"}})
            for (nt, r, c), text in notes.items():
                if nt == tab:
                    reqs.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": r + 1, "columnIndex": c},
                                                 "rows": [{"values": [{"note": text}]}], "fields": "note"}})
    for t in replace:
        reqs.append({"deleteSheet": {"sheetId": titles[t]}})
    for tab in TABS:
        reqs.append({"updateSheetProperties": {"properties": {"sheetId": ids[tab], "title": tab}, "fields": "title"}})
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": a.info_sheet_id, "title": "Info", "index": 0},
                                           "fields": "title,index"}})
    for i, tab in enumerate(TABS):
        reqs.append({"updateSheetProperties": {"properties": {"sheetId": ids[tab], "index": i + 1},
                                               "fields": "index"}})
    json.dump(reqs, open(a.out, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"{len(reqs)} requests, {len(json.dumps(reqs, ensure_ascii=False)) // 1000} KB -> {a.out}")


if __name__ == "__main__":
    main()
