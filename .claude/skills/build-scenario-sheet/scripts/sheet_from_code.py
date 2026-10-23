#!/usr/bin/env python3
"""Turn a live build's window.SCENARIO into rows for the Chat Simulation template.

Used by the skill's migrate mode when the code wins: it writes the values for each
template tab, and a local .xlsx with the template headers so the result can be
checked against the code with compare_sheet_code.py (round trip).

    python3 sheet_from_code.py <index.html> --out <folder>
        [--old <old sheet.xlsx>]   keep Partial/points on articles the code marks not right
        [--title "Practice Chat - ..."]   Chat title (default: "Practice Chat - " + code title)

Writes <folder>/sheet-values.json ({tab: {"range": A1, "values": rows}}) and
<folder>/roundtrip.xlsx. Prints anything the template can't hold.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare_sheet_code import QUOTES, clean_articles, scenario_from_js  # noqa: E402

HEADERS = {
    "Meta": ["Scenario Info", "Your value"],
    "Stages": ["Stage ID", "Name on scorecard", "Max points", "Strength (shown at end if done well)",
               "Improvement (shown at end if missed/partial)", "Additive (Y/N)"],
    "Screens": ["Screen ID", "Stage scored", "Expert message (optional)", "User message (optional)",
                "Question or Prompt"],
    "Choices": ["Screen ID", "Choice letter", "Choice text", "Rating (correct/partial/\nincorrect)", "Points",
                "Next screen (Screen ID or __end__)", "Retry (Y/N)", "Max points on second try",
                "Reaction 1: user reply or inline text (optional)",
                "Reaction 2: Expert reply or inline text (optional)",
                "Reaction 3: user reply or inline text (optional)", "Score to a different stage (optional)",
                "Extra credit: stage (optional)", "Extra credit: points", "Extra credit: rating",
                "Screenshot to display", "Only after a retry (Y/N, optional)"],
    "Articles": ["Article title (same words as the choice)", "Article link", "Right article? (Y/Partial/N)",
                 "Points"],
}
META_ORDER = ["Chat title", "Intro bio", "First screen", "User name", "Meet image", "Close image",
              "Tracking form"]
COLS = "ABCDEFGHIJKLMNOPQ"
notes = []
cell_notes = []  # [tab, data row index, column index, text]: engine fields with no template column

FIELD_HELP = {
    "showIf": "the screen only shows when this flag is set (\"!flag\" = not set)",
    "skipTo": "where the chat goes instead when showIf isn't met",
    "sets": "picking this sets a flag that a later screen's showIf checks",
    "speakerIf": "the user message only plays if the learner did this first (resourceOpened = opened a resource)",
    "say": "what the transcript shows the Expert saying for this [Action] pick",
    "improvement": "results-screen coaching line used when this is the pick that scored the stage",
    "note": "not read by the engine",
    "silent": "not read by the engine",
}


def note(msg):
    notes.append(msg)


def code_only(tab, row, col, fields):
    lines = [f"{k}: {json.dumps(v, ensure_ascii=False)} ({FIELD_HELP.get(k, 'engine field')})"
             for k, v in fields.items()]
    cell_notes.append([tab, row, col, "In the live code only (the template has no column for this yet):\n"
                       + "\n".join(lines)])


# ------------------------------- reactions ----------------------------------
def split_blocks(text, names):
    """Engine consequence/speaker text -> [(kind, text)], kind = user/expert/inline."""
    label = re.compile(rf"^\s*({'|'.join(map(re.escape, names))}|expert)\s*:\s*", re.I)
    blocks = []
    for part in text.split("\n\n"):
        if not part.strip():
            continue
        m = label.match(part)
        if m:
            kind = "expert" if m.group(1).lower() == "expert" else "user"
            blocks.append([kind, part])
        elif part.lstrip().startswith("("):
            blocks.append(["inline", part])
        elif part.strip() == "[image]" and blocks:
            blocks[-1][1] += "\n[image]"
        elif blocks:
            blocks[-1][1] += "\n\n" + part  # a second paragraph of the same reply
        else:
            blocks.append(["user", part])
    out = []
    for kind, part in blocks:
        lines = []
        for line in part.split("\n"):
            if line.strip() == "[image]":
                lines.append("[Screenshot]")
            else:
                lines.append(label.sub("", line, count=1) if kind != "inline" else line)
        out.append((kind, "\n".join(lines).strip()))
    return out


SLOTS = (("user", "inline"), ("expert", "inline"), ("user", "inline"))  # Reaction 1 / 2 / 3


def reaction_cells(text, names, where):
    cells, pos = ["", "", ""], 0
    for kind, body in split_blocks(text, names):
        i = next((i for i in range(pos, 3) if kind in SLOTS[i]), None)
        if i is None:
            note(f"{where}: the reply has more turns than Reaction 1-3 can hold; the extra turn was added to "
                 f"Reaction 3. Check it.")
            cells[2] = (cells[2] + "\n\n" + body).strip()
            continue
        cells[i], pos = body, i + 1
    return cells


# ------------------------------- building rows ------------------------------
KEY_FOR_SRC = {}  # image path -> the old sheet's asset key, so keys survive a migration


def asset_key(src):
    if src in KEY_FOR_SRC:
        return KEY_FOR_SRC[src]
    stem = os.path.splitext(os.path.basename(src))[0]
    return "asset." + re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_")


def chat_title(code_title):
    rest = re.sub(r"^\s*practice\s+(chat|call)\s*[-—–:]\s*", "", code_title or "", flags=re.I)
    return f"Practice Chat - {rest.strip()}"


def old_article_marks(path):
    """{link: (right, points)} from the old sheet, to keep Partial marks the engine doesn't score."""
    if not path:
        return {}
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    tab = next((t for t in ("Articles", "Helpers - Articles") if t in wb.sheetnames), None)
    if not tab:
        return {}
    rows = clean_articles(list(wb[tab].iter_rows(values_only=True)))
    head = [str(h or "").strip().lower() for h in rows[0]]
    find = lambda *names: next((i for i, h in enumerate(head) if any(h.startswith(n) for n in names)), None)
    li, ri, pi = find("url", "article link"), find("right article", "correct"), find("points", "credit")
    out = {}
    for r in rows[1:]:
        if li is not None and r[li]:
            out[str(r[li]).strip()] = (str(r[ri] or "").strip() if ri is not None else "",
                                       r[pi] if pi is not None else None)
    return out


def build(code, title, old):
    user = code.get("user", {})
    name = user.get("name") or "Caller"
    names = [name, "caller", "customer", "user"]
    assets = {}

    stages = [[s["id"], s.get("name", ""), s.get("max", 0), s.get("strength", ""), s.get("improvement", ""),
               "Y" if s.get("additive") else ""] for s in code.get("stages", [])]

    screens, choices = [], []
    for sid, x in code.get("screens", {}).items():
        extra = {k: v for k, v in x.items() if k not in ("stage", "speaker", "prompt", "choices", "gate")}
        if extra:
            note(f"Screen {sid}: {', '.join(extra)} kept as a cell note (no template column).")
            code_only("Screens", len(screens), 0, extra)
        expert, said = "", x.get("speaker", "") or ""
        if re.match(r"^\s*expert\s*:", said, re.I):
            blocks = split_blocks(said, names)
            expert = blocks[0][1]
            said = "\n\n".join(b for _, b in blocks[1:])
        screens.append([sid, x.get("stage", ""), expert, said, x.get("prompt", "")])

        for c in x.get("choices", []):
            where = f"Choice {sid} {c.get('id')}"
            extra = {k: v for k, v in c.items()
                     if k not in ("id", "text", "verdict", "points", "goTo", "retry", "capIfRetried", "retryOnly",
                                  "stageOverride", "consequence", "credits", "image", "showsImage",
                                  "showsImageAfter")}
            if extra:
                note(f"{where}: {', '.join(extra)} kept as a cell note (no template column).")
                code_only("Choices", len(choices), 2, extra)
            r = reaction_cells(c.get("consequence", "") or "", names, where)
            credit = (c.get("credits") or [{}])[0]
            shot = ""
            if c.get("image"):
                src = urllib.parse.unquote(str(c["image"].get("src", "")))
                key = asset_key(src)
                assets[key] = src
                in_reply = "[image]" in (c.get("consequence") or "")
                shot = key + (" (show first)" if c.get("showsImage") and not in_reply else "")
            choices.append([sid, c.get("id", ""), c.get("text", ""), c.get("verdict", ""), c.get("points", 0),
                            c.get("goTo", ""), "Y" if c.get("retry") else "N",
                            c.get("capIfRetried", "") if c.get("retry") else "",
                            r[0], r[1], r[2], c.get("stageOverride", ""),
                            credit.get("stage", ""), credit.get("points", "") if credit else "",
                            credit.get("verdict", ""), shot, "Y" if c.get("retryOnly") else ""])

    articles = []
    for a in (code.get("resources") or {}).get("items", []):
        if a.get("correct"):
            right, pts = "Y", 20
        else:
            right, pts = old.get(str(a.get("url", "")).strip(), ("N", 0))
            right = right if right in ("Partial",) else "N"
            pts = pts if right == "Partial" and pts not in (None, "") else 0
        articles.append([a.get("label", ""), a.get("url", ""), right, pts])

    meta_vals = {"Chat title": title, "Intro bio": user.get("bio", ""), "First screen": code.get("start", ""),
                 "User name": user.get("name", ""),
                 "Meet image": urllib.parse.unquote(user.get("image", "") or ""),
                 "Close image": urllib.parse.unquote(user.get("completeImage", "") or ""), "Tracking form": ""}
    meta = [[k, meta_vals[k]] for k in META_ORDER]
    meta += [[f"{k}\nScreenshot: {os.path.splitext(os.path.basename(v))[0]}.", v] for k, v in assets.items()]
    return {"Meta": meta, "Stages": stages, "Screens": screens, "Choices": choices, "Articles": articles}


def as_text(v):
    """Keep sheet input as typed: a leading apostrophe stops Sheets turning text into numbers or formulas."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    v = "" if v is None else str(v)
    return "'" + v if re.match(r"^[=+\-@]|^\d[\d/.\-]*$", v) else v


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("html", help="the live build's index.html, or the old sheet's .xlsx when there's no code")
    ap.add_argument("--choices-tab", help="with an .xlsx: which tab holds the chat choices")
    ap.add_argument("--out", required=True)
    ap.add_argument("--old")
    ap.add_argument("--title")
    a = ap.parse_args()

    if a.html.lower().endswith(".xlsx"):
        # No live code: read the old sheet the way the build would, then lay it out again.
        import openpyxl
        from compare_sheet_code import Workbook, load_converter
        conv = load_converter()
        wb = Workbook(openpyxl.load_workbook(a.html, data_only=True), a.choices_tab)
        meta, block, _ = conv.build(wb)
        for e in conv.errors:
            note(f"Old sheet: {e}")
        KEY_FOR_SRC.update({path: key for key, path in conv.read_meta(wb)[1].items()})
        code = scenario_from_js(block)
        if not meta.get("user_name"):  # the converter's "Caller" stand-in isn't a real name
            code["user"]["name"] = ""
        a.old = a.old or a.html
    else:
        with open(a.html, encoding="utf-8") as f:
            code = scenario_from_js(f.read())
    tabs = build(code, a.title or chat_title(code.get("title")), old_article_marks(a.old))
    os.makedirs(a.out, exist_ok=True)

    values = {}
    for tab, rows in tabs.items():
        if tab == "Meta":  # column A of the first rows holds the template's own labels; write B only
            fixed = [[as_text(r[1])] for r in rows[:len(META_ORDER)]]
            values["Meta"] = {"range": f"Meta!B2:B{len(META_ORDER) + 1}", "values": fixed}
            extra = rows[len(META_ORDER):]
            if extra:  # column A (asset.<key> + help line) is written with its formatting by template_requests.py
                start = len(META_ORDER) + 2
                values["Meta assets"] = {"range": f"Meta!B{start}:B{start + len(extra) - 1}",
                                         "values": [[as_text(r[1])] for r in extra]}
            continue
        width = len(HEADERS[tab])
        values[tab] = {"range": f"{tab}!A2:{COLS[width - 1]}{len(rows) + 1}",
                       "values": [[as_text(v) for v in r] for r in rows]}
    with open(os.path.join(a.out, "sheet-values.json"), "w", encoding="utf-8") as f:
        json.dump(values, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "migration.json"), "w", encoding="utf-8") as f:
        json.dump({"tabs": tabs, "meta_fixed_rows": len(META_ORDER), "cell_notes": cell_notes},
                  f, ensure_ascii=False, indent=1)

    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for tab, rows in tabs.items():
        ws = wb.create_sheet(tab)
        ws.append(HEADERS[tab])
        for r in rows:
            ws.append([v if not isinstance(v, str) else v for v in r])
    wb.save(os.path.join(a.out, "roundtrip.xlsx"))

    counts = ", ".join(f"{t} {len(r)}" for t, r in tabs.items())
    print(f"Rows: {counts}")
    for n in dict.fromkeys(notes):
        print("NOTE:", n)


if __name__ == "__main__":
    main()
