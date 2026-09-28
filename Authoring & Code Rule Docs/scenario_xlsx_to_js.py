#!/usr/bin/env python3
"""
scenario_xlsx_to_js.py — turn a filled-in scenario workbook into a
`window.SCENARIO = { ... }` block you can paste into a Care Dojo scenario's
<script id="scenario"> tag.

Emits the CURRENT schema (see "Care Dojo HTML & Data - Source of Truth.md"):
  • user:{ name, image, completeImage, bio }      (NOT the old flat userBio)
  • resources:{ title, stage, capIfUnchecked, note, items:[{label,url,correct:true}] }
      (the gate+cap model — NOT the old points-per-resource items)
  • stages:[{ id, name, max, additive?, strength, improvement }]
  • choices with `consequence` (a single string) — NOT the old reactions[]/learnerLine
  • choice `id` letters, `note`, `say`, `silent`, `showsImage`, `showsImageAfter`,
    per-choice/per-screen `image:{src}`, `speakerIf`, `credits`, retry/capIfRetried.

Usage:
    python3 scenario_xlsx_to_js.py <input.xlsx> [output.js]

If output.js is omitted, the JS block is printed to stdout.

EXPECTED WORKBOOK TABS & COLUMNS (header row 1, data from row 2)
---------------------------------------------------------------
Meta      (key / value / notes)  — recognised keys:
            title, user_name, user_image, user_completeImage, user_bio, start,
            resources_title, resources_stage, resources_capIfUnchecked, resources_note
Stages    id | name | max | additive (Y/N) | strength | improvement
Screens   screen_id | stage | gate (Y/N) | speaker | speakerIf | image_src | prompt
Choices   screen_id | choice_id | text | verdict | points | goTo | consequence |
          note | say | silent (Y/N) | showsImage (Y/N) | showsImageAfter (Y/N) |
          image_src | retry (Y/N) | capIfRetried | stageOverride |
          credit_stage | credit_points | credit_verdict
Resources label | url | correct (Y/N) | note (author reference; not exported)

Notes for authors:
  • Screen ORDER in the output follows the row order of the Screens tab.
  • For multi-line speaker/consequence text, use a real line break in the cell
    (Alt+Enter). Label the parts, e.g. "Samantha: ..." and "Expert: ...".
  • An [Action] choice (text begins with "[Action]") renders as a centered
    "You ..." note; give it `note` for exact wording and do NOT give it `say`.
  • The script warns (does not fail) on: stage max not summing to 100, a goTo that
    points nowhere, and any em-dash (—) in exported text.
"""
import sys
import json
import openpyxl


# ------------------------------- helpers -----------------------------------
def rows(ws):
    """Yield each non-blank data row (after the header) as a list of cell values."""
    for r in ws.iter_rows(min_row=2, values_only=True):
        if any(v not in (None, "") for v in r):
            yield r


def s(v):
    """Trimmed string, '' for None. Also normalises a literal backslash-n typed by
    hand into a real newline so both authoring styles produce clean JS."""
    if v is None:
        return ""
    return str(v).strip().replace("\\n", "\n")


def yesish(v):
    return s(v).upper().startswith("Y")


def num(v, default=0):
    return int(v) if v not in (None, "") else default


def js(v):
    """JSON-encode a string value (double-quoted, unicode kept, newlines -> \\n)."""
    return json.dumps(s(v), ensure_ascii=False)


def load(path):
    return openpyxl.load_workbook(path, data_only=True)


# ------------------------------- readers -----------------------------------
def build_meta(wb):
    meta = {}
    for row in rows(wb["Meta"]):
        field = s(row[0])
        value = s(row[1]) if len(row) > 1 else ""
        if field:
            meta[field] = value
    return meta


def build_stages(wb):
    out, total = [], 0
    for row in rows(wb["Stages"]):
        (id_, name, max_, additive, strength, improvement) = (list(row) + [None] * 6)[:6]
        if s(id_) == "" or max_ in (None, ""):
            continue
        m = int(max_)
        total += m
        parts = [f"    {{ id:{js(id_)}, name:{js(name)}, max:{m}"]
        if yesish(additive):
            parts.append(", additive:true")
        parts.append(f",\n      strength:{js(strength)},\n      improvement:{js(improvement)} }}")
        out.append("".join(parts))
    if total != 100:
        print(f"WARNING: Stages max values sum to {total}, not 100.", file=sys.stderr)
    return ",\n".join(out)


def build_screens(wb):
    screens = {}
    order = []
    for row in rows(wb["Screens"]):
        (screen_id, stage, gate, speaker, speakerIf, image_src, prompt) = (list(row) + [None] * 7)[:7]
        sid = s(screen_id)
        if not sid:
            continue
        screens[sid] = {
            "stage": s(stage),
            "gate": yesish(gate),
            "speaker": s(speaker),
            "speakerIf": s(speakerIf),
            "image_src": s(image_src),
            "prompt": s(prompt),
            "choices": [],
        }
        order.append(sid)
    return screens, order


def build_choices(wb, screens):
    for row in rows(wb["Choices"]):
        (screen_id, choice_id, text, verdict, points, goTo, consequence,
         note, say, silent, showsImage, showsImageAfter, image_src,
         retry, capIfRetried, stageOverride,
         credit_stage, credit_points, credit_verdict) = (list(row) + [None] * 19)[:19]
        sid = s(screen_id)
        if not sid:
            continue
        if sid not in screens:
            raise ValueError(
                f"Choices row references unknown screen_id '{sid}' — add it to the Screens tab."
            )
        screens[sid]["choices"].append({
            "id": s(choice_id),
            "text": s(text),
            "verdict": s(verdict),
            "points": num(points),
            "goTo": s(goTo),
            "consequence": s(consequence),
            "note": s(note),
            "say": s(say),
            "silent": yesish(silent),
            "showsImage": yesish(showsImage),
            "showsImageAfter": yesish(showsImageAfter),
            "image_src": s(image_src),
            "retry": yesish(retry),
            "capIfRetried": capIfRetried,
            "stageOverride": s(stageOverride),
            "credit_stage": s(credit_stage),
            "credit_points": credit_points,
            "credit_verdict": s(credit_verdict),
        })


def build_resources(wb, meta):
    if "Resources" not in wb.sheetnames:
        return ""
    items = []
    for row in rows(wb["Resources"]):
        (label, url, correct, _note) = (list(row) + [None] * 4)[:4]
        if not s(label):
            continue
        line = f"      {{ label:{js(label)}, url:{js(url)}"
        if yesish(correct):
            line += ", correct:true"
        line += " }"
        items.append(line)
    if not items:
        return ""

    head = [f"    title:{js(meta.get('resources_title') or 'Check Resources')}"]
    if meta.get("resources_stage"):
        head.append(f"    stage:{js(meta['resources_stage'])}")
    if meta.get("resources_capIfUnchecked"):
        head.append(f"    capIfUnchecked:{int(meta['resources_capIfUnchecked'])}")
    if meta.get("resources_note"):
        head.append(f"    note:{js(meta['resources_note'])}")
    head_joined = ",\n".join(head)
    items_joined = ",\n".join(items)
    return f"  resources: {{\n{head_joined},\n    items: [\n{items_joined}\n    ]\n  }},\n"


# ------------------------------- renderers ---------------------------------
def render_choice(ch, indent="        "):
    head = f'{{ id:{js(ch["id"])}, text:{js(ch["text"])},\n{indent}  '
    head += f'verdict:{js(ch["verdict"])}, points:{ch["points"]}, goTo:{js(ch["goTo"])}'
    tail = []
    if ch["note"]:
        tail.append(f'note:{js(ch["note"])}')
    if ch["say"]:
        tail.append(f'say:{js(ch["say"])}')
    if ch["silent"]:
        tail.append("silent:true")
    if ch["showsImage"]:
        tail.append("showsImage:true")
    if ch["showsImageAfter"]:
        tail.append("showsImageAfter:true")
    if ch["image_src"]:
        tail.append(f'image:{{ src:{js(ch["image_src"])} }}')
    if ch["retry"]:
        tail.append(f'retry:true, capIfRetried:{num(ch["capIfRetried"])}')
    if ch["stageOverride"]:
        tail.append(f'stageOverride:{js(ch["stageOverride"])}')
    if ch["consequence"]:
        tail.append(f'consequence:{js(ch["consequence"])}')
    if ch["credit_stage"]:
        cp = num(ch["credit_points"])
        cv = ch["credit_verdict"] or "correct"
        tail.append(f'credits:[{{ stage:{js(ch["credit_stage"])}, points:{cp}, verdict:{js(cv)} }}]')
    body = head
    if tail:
        body += ",\n" + indent + "  " + (",\n" + indent + "  ").join(tail)
    body += " }"
    return body


def render_screens(screens, order):
    blocks = []
    for sid in order:
        scr = screens[sid]
        lines = [f'    {sid}: {{',
                 f'      stage:{js(scr["stage"])}, gate:{"true" if scr["gate"] else "false"},']
        if scr["speaker"]:
            lines.append(f'      speaker:{js(scr["speaker"])},')
        if scr["speakerIf"]:
            lines.append(f'      speakerIf:{js(scr["speakerIf"])},')
        if scr["image_src"]:
            lines.append(f'      image:{{ src:{js(scr["image_src"])} }},')
        lines.append(f'      prompt:{js(scr["prompt"])},')
        lines.append("      choices:[")
        lines.append(",\n".join(f"        {render_choice(ch)}" for ch in scr["choices"]))
        lines.append("      ]")
        lines.append("    }")
        blocks.append("\n".join(lines))
    return ",\n\n".join(blocks)


def render_user(meta):
    fields = []
    if meta.get("user_name"):
        fields.append(f"    name: {js(meta['user_name'])}")
    if meta.get("user_image"):
        fields.append(f"    image: {js(meta['user_image'])}")
    if meta.get("user_completeImage"):
        fields.append(f"    completeImage: {js(meta['user_completeImage'])}")
    if meta.get("user_bio"):
        fields.append(f"    bio: {js(meta['user_bio'])}")
    if not fields:
        return ""
    return "  user: {\n" + ",\n".join(fields) + "\n  },\n"


# ------------------------------- checks ------------------------------------
def sanity_checks(screens, order):
    known = set(order) | {"__end__"}
    for sid in order:
        for ch in screens[sid]["choices"]:
            if ch["goTo"] and ch["goTo"] not in known:
                print(f"WARNING: {sid} choice {ch['id']} goTo '{ch['goTo']}' is not a known screen id or __end__.",
                      file=sys.stderr)
            if ch["retry"] and ch["capIfRetried"] in (None, ""):
                print(f"WARNING: {sid} choice {ch['id']} has retry but no capIfRetried.", file=sys.stderr)


def emdash_check(text):
    if "—" in text:
        n = text.count("—")
        print(f"WARNING: output contains {n} em-dash(es) (—). House style forbids them — use a hyphen, comma, or parentheses.",
              file=sys.stderr)


# ------------------------------- main --------------------------------------
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    wb = load(in_path)
    meta = build_meta(wb)
    stages_js = build_stages(wb)
    screens, order = build_screens(wb)
    build_choices(wb, screens)
    sanity_checks(screens, order)
    screens_js = render_screens(screens, order)
    user_block = render_user(meta)
    resources_block = build_resources(wb, meta)

    out = (
        "window.SCENARIO = {\n"
        f"  title: {js(meta.get('title'))},\n"
        f"{user_block}"
        f"{resources_block}"
        "  stages: [\n"
        f"{stages_js}\n"
        "  ],\n\n"
        f"  start: {js(meta.get('start'))},\n"
        "  screens: {\n\n"
        f"{screens_js}\n\n"
        "  }\n"
        "};\n"
    )

    emdash_check(out)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote {out_path}")
    else:
        print(out)


if __name__ == "__main__":
    main()
