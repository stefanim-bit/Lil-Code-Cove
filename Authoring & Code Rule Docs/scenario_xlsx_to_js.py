#!/usr/bin/env python3
"""
scenario_xlsx_to_js.py: turn a filled-in Chat Simulation Sheet (downloaded as .xlsx)
into a ready-to-test Care Dojo folder.

HOW TO USE
  1. In the Google Sheet: File > Download > Microsoft Excel (.xlsx).
     Download it right before you build, so it has your latest edits.
  2. Run (from the Lil Code Cove folder, or with full paths):
       python3 "Authoring & Code Rule Docs/scenario_xlsx_to_js.py" "<your sheet>.xlsx"
     Optional:
       --out "<folder>"   where to build (default: "<Chat title> Test Build" next to the .xlsx)
       --overwrite        replace an existing build folder's index.html
       --js-only          just print the window.SCENARIO block, build nothing
  3. Add the image files it lists, then test-play the folder's index.html.

  First run only: if you see "No module named openpyxl", run
       python3 -m pip install openpyxl

WHAT IT READS (header row 1, data from row 2; columns are found by header name)
  Meta      Scenario Info | Your value
            (only the first line of a Scenario Info cell counts; the rest is help text)
            Chat title, Intro bio, First screen, User name, Meet image, Close image,
            Tracking form, and asset.<name> rows (value = image folder/file name)
  Stages    Stage ID | Name on scorecard | Max points | Strength | Improvement | Additive (Y/N)
  Screens   Screen ID | Stage scored | Expert message | User message | Question or Prompt
  Choices   Screen ID | Choice letter | Choice text | Rating | Points | Next screen | Retry |
            Max points on second try | Reaction 1-3 | Score to a different stage |
            Extra credit: stage / points / rating | Screenshot to display |
            Only after a retry
  Articles  Article title | Article link | Right article? | Points
  Sheets made before 2026-10-21 (Screen_ID, GoTo, Consequence..., Credit_Stage, Asset,
  Field/Value, title/userBio/start) are read too.

WHAT IT BUILDS
  A copy of the canonical engine (PS1 Layers) with this scenario's data, plus two
  fixes applied to the copy only (the PS1 file itself is never changed):
    - inline text works in any reaction, not just the first
    - tracking goes to the Sheet's Tracking form, or nowhere if it's blank

  Reactions: Reaction 1 and 3 are the user's bubbles, Reaction 2 is the Expert's.
  A reaction that starts with [Inline text] or [Inline], or is wrapped in
  (parentheses), shows as a centered inline note instead.
  Screenshots show after the reactions; "asset.<name> (show first)" shows them when
  the choice is picked; a line of just [Screenshot] in a reaction cell shows it there.
  A screen's Expert message plays before its User message.
  Only after a retry = Y hides a choice until the screen re-opens after a Retry pick.

  Engine fields it writes (see "Care Dojo HTML & Data - Source of Truth.md"):
  title, user{name,image,completeImage,bio}, resources{title,stage,capIfUnchecked,note,
  items[{label,url,correct}]}, stages[{id,name,max,additive,strength,improvement}],
  start, screens{stage,speaker,prompt,choices[{id,text,verdict,points,goTo,retry,
  capIfRetried,retryOnly,stageOverride,consequence,credits,image,showsImage,
  showsImageAfter}]}.
  Per-article Points and Partial aren't read by the engine yet (end-of-October update).
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ENGINE = os.path.join(REPO, "Practice Session 1", "PS1 Layers", "Current",
                      "PS1 Layers Code Block 2026-09-16 2", "index.html")
RESOURCES_NOTE = ("Open the resources below. Checking the right one before you answer "
                  "is the skill, not remembering it.")
VERDICTS = ("correct", "partial", "incorrect")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ------------------------------- cell helpers ------------------------------
QUOTE_FIX = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def s(v):
    """Trimmed text ('' for blank). Turns a typed \\n into a real line break and
    straightens curly quotes, which Google Sheets adds on its own."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip().replace("\\n", "\n").translate(QUOTE_FIX)


def yes(v):
    return s(v).upper().startswith("Y")


def js(v):
    return json.dumps(s(v), ensure_ascii=False)


def norm(h):
    return re.sub(r"\s+", " ", s(h).lower()).strip()


def number(v, where, what, required=True):
    """Numbers only (10, not "10 pts"). Returns None for a blank optional cell."""
    if v is None or s(v) == "":
        if required:
            err(f"{where}: {what} is empty. Numbers only, e.g. 10.")
        return None
    if isinstance(v, (int, float)):
        return int(v) if float(v).is_integer() else v
    t = s(v)
    if re.fullmatch(r"-?\d+(\.\d+)?", t):
        f = float(t)
        return int(f) if f.is_integer() else f
    err(f"{where}: {what} must be a number only (got \"{t}\"). Write 10, not \"10 pts\".")
    return None


# ------------------------------- reading tabs ------------------------------
# Each column: (key, header names that count as it). New names first, then the
# names used before 2026-10-21. A header matches if it equals one of these, or
# starts with one followed by " (" (so hints like "(optional)" don't matter).
COLUMNS = {
    "Stages": [("id", ["stage id", "id"]), ("name", ["name on scorecard", "name"]),
               ("max", ["max points", "max"]),
               ("strength", ["strength"]), ("improvement", ["improvement"]),
               ("additive", ["additive"])],
    "Screens": [("screen", ["screen id", "screen_id"]), ("stage", ["stage scored", "stage"]),
                ("expert", ["expert message", "learner"]), ("user", ["user message", "speaker"]),
                ("question", ["question or prompt", "question above choices", "prompt"])],
    "Choices": [("screen", ["screen id", "screen_id"]), ("letter", ["choice letter", "choice_id"]),
                ("text", ["choice text", "text"]), ("rating", ["rating", "verdict"]),
                ("points", ["points"]), ("next", ["next screen", "goto"]),
                ("retry", ["retry"]), ("cap", ["max points on second try", "capifretried"]),
                ("r1", ["reaction 1: user reply or inline text", "reaction 1"]),
                ("r2", ["reaction 2: expert reply or inline text", "reaction 2"]),
                ("r3", ["reaction 3: user reply or inline text", "reaction 3"]),
                ("override", ["score to a different stage", "stage override"]),
                ("cstage", ["extra credit: stage", "credit_stage"]),
                ("cpoints", ["extra credit: points", "credit_points"]),
                ("crating", ["extra credit: rating", "credit_verdict"]),
                ("shot", ["screenshot to display", "asset"]),
                ("retry_only", ["only after a retry", "retry only", "retryonly"])],
    "Articles": [("title", ["article title", "article_title"]), ("link", ["article link", "url"]),
                 ("right", ["right article?", "correct"]), ("points", ["points", "credit"])],
}
REQUIRED = {
    "Stages": ["id", "name", "max", "strength", "improvement"],
    "Screens": ["screen", "stage", "user", "question"],
    "Choices": ["screen", "letter", "text", "rating", "points", "next"],
    "Articles": ["title", "link", "right"],
}
NEW_NAME = {  # what to tell people a missing column is called
    "Stages": {"id": "Stage ID", "name": "Name on scorecard", "max": "Max points",
               "strength": "Strength (shown at end if done well)",
               "improvement": "Improvement (shown at end if missed/partial)"},
    "Screens": {"screen": "Screen ID", "stage": "Stage scored", "user": "User message (optional)",
                "question": "Question or Prompt"},
    "Choices": {"screen": "Screen ID", "letter": "Choice letter", "text": "Choice text",
                "rating": "Rating (correct/partial/incorrect)", "points": "Points",
                "next": "Next screen (Screen ID or __end__)"},
    "Articles": {"title": "Article title (same words as the choice)", "link": "Article link",
                 "right": "Right article? (Y/Partial/N)"},
}


def header_map(tab, header):
    found, old_consequences = {}, []
    for i, h in enumerate(header):
        n = norm(h)
        if not n:
            continue
        if tab == "Choices" and n.startswith("consequence"):
            old_consequences.append(i)  # old sheets: three "Consequence ..." columns, in order
            continue
        for key, names in COLUMNS[tab]:
            if key in found:
                continue
            if any(n == a or n.startswith(a + " (") for a in names):
                found[key] = i
                break
    for key, i in zip(("r1", "r2", "r3"), old_consequences):
        found.setdefault(key, i)
    return found


def read_tab(wb, tab, optional=False):
    if tab not in wb.sheetnames:
        if not optional:
            err(f"The workbook has no \"{tab}\" tab. Don't rename or delete tabs.")
        return []
    rows = list(wb[tab].iter_rows(values_only=True))
    if not rows:
        return []
    cols = header_map(tab, rows[0])
    missing = [k for k in REQUIRED[tab] if k not in cols]
    if missing:
        names = ", ".join(f"\"{NEW_NAME[tab][k]}\"" for k in missing)
        err(f"The {tab} tab is missing the column(s) {names}. Don't rename or delete header "
            f"columns; copy the header row from the blank template if needed.")
        return []
    out = []
    for r, row in enumerate(rows[1:], start=2):
        if not any(s(v) for v in row):
            continue
        rec = {k: (row[i] if i < len(row) else None) for k, i in cols.items()}
        rec["_row"] = r
        out.append(rec)
    return out


META_KEYS = {"chat title": "title", "title": "title", "intro bio": "bio", "userbio": "bio",
             "first screen": "start", "start": "start", "user name": "user_name",
             "meet image": "meet_image", "close image": "close_image",
             "tracking form": "tracking_form"}


def read_meta(wb):
    meta, assets = {}, {}
    if "Meta" not in wb.sheetnames:
        err("The workbook has no \"Meta\" tab. Don't rename or delete tabs.")
        return meta, assets
    for row in list(wb["Meta"].iter_rows(values_only=True))[1:]:
        # First line is the setting name; anything below it is help text for authors.
        key = s(row[0] if row else "").split("\n")[0].strip()
        value = s(row[1] if len(row) > 1 else "")
        if not key:
            continue
        if key.lower().startswith("asset."):
            assets[key] = value
        elif norm(key) in META_KEYS:
            meta[META_KEYS[norm(key)]] = value
    for k, label in (("title", "Chat title"), ("bio", "Intro bio"), ("start", "First screen"),
                     ("user_name", "User name"), ("meet_image", "Meet image"),
                     ("close_image", "Close image")):
        if not meta.get(k):
            (err if k in ("title", "start") else warn)(
                f"Meta tab: \"{label}\" is empty" + ("." if k in ("title", "start") else
                                                     ". The build uses a placeholder."))
    return meta, assets


# ------------------------------- building ----------------------------------
INLINE_TAG = re.compile(r"^\s*\[inline(?: text)?\]\s*", re.I)


def inline_body(text):
    """The note text if this cell is marked inline, else None."""
    m = INLINE_TAG.match(text)
    if m:
        return text[m.end():].strip()
    if text.startswith("(") and text.endswith(")"):
        return text[1:-1].strip()
    return None


SHOT_MARK = re.compile(r"^\s*\[(?:screenshot|image)\]\s*$", re.I)


def has_shot_mark(text):
    return any(SHOT_MARK.match(l) for l in text.split("\n"))


def line_for(text, label, user_name):
    """One reaction cell -> one engine line: '(note)' or 'Label: words'.
    A line of just [Screenshot] inside the cell becomes the engine's [image] line,
    so the choice's screenshot shows at that point in the reply."""
    if has_shot_mark(text):
        chunks, cur = [], []
        for l in text.split("\n") + ["[image]"]:
            if SHOT_MARK.match(l):
                part = "\n".join(cur).strip()
                if part:
                    chunks.append(line_for(part, label, user_name))
                chunks.append("[image]")
                cur = []
            else:
                cur.append(l)
        return "\n".join(chunks[:-1])
    body = inline_body(text)
    if body is not None:
        return f"({body})"
    first = text.split("\n", 1)[0]
    if re.match(rf"^\s*(expert|{re.escape(user_name)}|caller|customer)\s*:", first, re.I):
        return text  # already labeled
    return f"{label}: {text}"


def image_src(path):
    return urllib.parse.quote(path, safe="/()&'-_.,!~*")


def build(wb):
    meta, assets = read_meta(wb)
    stages = read_tab(wb, "Stages")
    screens = read_tab(wb, "Screens")
    choices = read_tab(wb, "Choices")
    articles = [a for a in read_tab(wb, "Articles", optional=True) if s(a.get("title"))]
    user_name = meta.get("user_name") or "Caller"

    # Stages
    stage_ids, total, stage_js = set(), 0, []
    for st in stages:
        sid = s(st["id"])
        if not sid:
            continue
        where = f"Stages row {st['_row']} ({sid})"
        if sid != sid.lower() or " " in sid:
            err(f"{where}: Stage ID must be lowercase with no spaces.")
        mx = number(st.get("max"), where, "Max points")
        stage_ids.add(sid)
        total += mx or 0
        add = ", additive:true" if yes(st.get("additive")) else ""
        stage_js.append(f"    {{ id:{js(sid)}, name:{js(st.get('name'))}, max:{mx or 0}{add},\n"
                        f"      strength:{js(st.get('strength'))},\n"
                        f"      improvement:{js(st.get('improvement'))} }}")
    if stages and total != 100:
        warn(f"Stage Max points add up to {total}, not 100 (Care Dojo default; fine for other projects).")

    # Screens
    order, scr = [], {}
    for x in screens:
        sid = s(x["screen"])
        if not sid:
            continue
        where = f"Screens row {x['_row']} ({sid})"
        if sid in scr:
            err(f"{where}: Screen ID \"{sid}\" is used twice.")
            continue
        if s(x.get("stage")) not in stage_ids:
            err(f"{where}: Stage scored \"{s(x.get('stage'))}\" isn't a Stage ID on the Stages tab.")
        if not s(x.get("question")):
            err(f"{where}: Question or Prompt is empty.")
        speaker = s(x.get("user"))
        if speaker and inline_body(speaker) is not None:
            speaker = f"({inline_body(speaker)})"
        expert = s(x.get("expert"))
        if expert:
            # The Expert's line plays first, then the user's.
            speaker = "\n\n".join([line_for(expert, "Expert", user_name)]
                                  + ([line_for(speaker, user_name, user_name)] if speaker else []))
        order.append(sid)
        scr[sid] = {"stage": s(x.get("stage")), "speaker": speaker,
                    "prompt": s(x.get("question")), "choices": []}

    start = meta.get("start", "")
    if start and start not in scr:
        err(f"Meta tab: First screen \"{start}\" isn't a Screen ID on the Screens tab.")

    # Articles
    titles = {}
    items = []
    for a in articles:
        t = s(a["title"])
        where = f"Articles row {a['_row']} ({t})"
        if "reply using" in t.lower():
            quoted = re.findall(r"\"(.+?)\"", t)
            if quoted:
                t = re.sub(r"[\s.]+$", "", quoted[0])
                warn(f"{where}: Article title should be just the article's name; used \"{t}\".")
            else:
                err(f"{where}: Article title should be just the article's name, without \"Reply using\".")
        if not s(a.get("link")).startswith("http"):
            err(f"{where}: Article link is missing or isn't a link.")
        right = s(a.get("right")).lower()
        if right not in ("y", "n", "partial", "yes", "no"):
            err(f"{where}: Right article? must be Y, Partial or N.")
        titles[title_key(t)] = t
        line = f"      {{ label:{js(t)}, url:{js(a.get('link'))}"
        items.append(line + (", correct:true }" if right.startswith("y") else " }"))
    if articles and not any(i.endswith("correct:true }") for i in items):
        err("Articles tab: no article is marked Y (the right article).")

    # Choices
    images = []
    for c in choices:
        sid = s(c["screen"])
        if not sid:
            continue
        cid = s(c.get("letter"))
        where = f"Choices row {c['_row']} ({sid} {cid})"
        if sid not in scr:
            err(f"{where}: Screen ID \"{sid}\" isn't on the Screens tab.")
            continue
        rating = s(c.get("rating")).lower()
        if rating not in VERDICTS:
            err(f"{where}: Rating must be correct, partial or incorrect (got \"{s(c.get('rating'))}\").")
        pts = number(c.get("points"), where, "Points")
        nxt = s(c.get("next"))
        if nxt != "__end__" and nxt not in scr:
            err(f"{where}: Next screen \"{nxt}\" isn't a Screen ID on the Screens tab (or __end__).")
        text = s(c.get("text"))
        m = REPLY_USING.search(text)
        for q in re.findall(r"[\"](.+?)[\"]", text[m.end():]) if m else []:
            if not title_matches(q, titles):
                err(f"{where}: \"Reply using\" quotes \"{q}\", which isn't an Article title on the Articles tab.")
        parts = [f'{{ id:{js(cid)}, text:{js(text)},\n          verdict:{js(rating)}, points:{pts or 0}, goTo:{js(nxt)}']
        retry = yes(c.get("retry"))
        if retry:
            cap = number(c.get("cap"), where, "Max points on second try", required=False)
            parts.append("retry:true" + (f", capIfRetried:{cap}" if cap is not None else ""))
        retry_only = yes(c.get("retry_only"))
        if retry_only:
            parts.append("retryOnly:true")
        override = s(c.get("override"))
        if override:
            if override not in stage_ids:
                err(f"{where}: Score to a different stage \"{override}\" isn't a Stage ID.")
            parts.append(f"stageOverride:{js(override)}")
        lines = [line_for(s(c.get(k)), lab, user_name)
                 for k, lab in (("r1", user_name), ("r2", "Expert"), ("r3", user_name)) if s(c.get(k))]
        if lines:
            parts.append(f"consequence:{js(chr(10).join([lines[0]] + [chr(10) + l for l in lines[1:]]))}")
        cstage = s(c.get("cstage"))
        if cstage:
            if cstage not in stage_ids:
                err(f"{where}: Extra credit: stage \"{cstage}\" isn't a Stage ID.")
            cp = number(c.get("cpoints"), where, "Extra credit: points")
            cr = s(c.get("crating")).lower()
            if cr not in VERDICTS:
                err(f"{where}: Extra credit: rating is required when Extra credit: stage is filled "
                    f"(correct, partial or incorrect).")
            parts.append(f"credits:[{{ stage:{js(cstage)}, points:{cp or 0}, verdict:{js(cr)} }}]")
        shot = s(c.get("shot"))
        in_reply = any(has_shot_mark(s(c.get(k))) for k in ("r1", "r2", "r3"))
        if in_reply and not shot:
            err(f"{where}: a reaction has a [Screenshot] line, but Screenshot to display is empty. "
                f"Add the asset key there.")
        if shot:
            key = shot.split()[0]
            first = "(show first)" in shot.lower()
            path = assets.get(key)
            if path is None:
                err(f"{where}: Screenshot \"{key}\" has no matching asset row on the Meta tab.")
            else:
                if not path or path.lower().startswith("placeholder"):
                    warn(f"{where}: {key} has no image file yet (Meta value is \"{path}\").")
                else:
                    images.append(path)
                img = f"image:{{ src:{js(image_src(path))} }}"
                if in_reply:  # placed by the [Screenshot] line, so no before/after flag
                    if first:
                        warn(f"{where}: (show first) is ignored because a reaction has a [Screenshot] line.")
                    parts.append(img)
                else:
                    parts.append(img + ", " + ("showsImage:true" if first else "showsImageAfter:true"))
        scr[sid]["choices"].append((cid, retry, retry_only, ",\n          ".join(parts) + " }"))

    for sid in order:
        cs = scr[sid]["choices"]
        first_view = [r for _, r, ro, _ in cs if not ro]
        if not cs:
            err(f"Screen {sid} has no choices on the Choices tab.")
        elif all(r for _, r, _, _ in cs):
            err(f"Screen {sid}: every choice has Retry = Y, so the learner gets stuck. Set at least one to N.")
        elif first_view and all(first_view):
            err(f"Screen {sid}: every choice shown on the first try has Retry = Y, so the learner gets stuck. "
                f"Set at least one to N.")
        if any(ro for _, _, ro, _ in cs) and not any(r for _, r, _, _ in cs):
            warn(f"Screen {sid}: a choice is set to Only after a retry, but no choice on this screen has "
                 f"Retry = Y, so it never shows.")
        letters = [l for l, _, _, _ in cs]
        if len(set(letters)) != len(letters):
            err(f"Screen {sid}: a Choice letter is used twice ({', '.join(letters)}).")

    # Assemble
    screen_js = []
    for sid in order:
        x = scr[sid]
        body = [f"    {sid}: {{", f"      stage:{js(x['stage'])},"]
        if x["speaker"]:
            body.append(f"      speaker:{js(x['speaker'])},")
        body.append(f"      prompt:{js(x['prompt'])},")
        body.append("      choices:[\n        " + ",\n        ".join(c for _, _, _, c in x["choices"]) + "\n      ]")
        body.append("    }")
        screen_js.append("\n".join(body))
    user = (f"  user: {{\n    name: {js(user_name)},\n"
            f"    image: {js(image_src(meta.get('meet_image', '')))},\n"
            f"    completeImage: {js(image_src(meta.get('close_image', '')))},\n"
            f"    bio: {js(meta.get('bio'))}\n  }},\n\n")
    resources = ""
    if items:
        resources = ("  resources: {\n    title: \"Check Resources\",\n"
                     "    stage: \"article\", capIfUnchecked: 10,\n"
                     f"    note: {js(RESOURCES_NOTE)},\n    items: [\n" + ",\n".join(items) + "\n    ]\n  },\n\n")
        if "article" not in stage_ids:
            warn("The Articles tab has articles but there's no \"article\" stage, so Check Resources isn't scored.")
    block = ("window.SCENARIO = {\n"
             f"  title: {js(meta.get('title'))},\n\n" + user + resources +
             "  stages: [\n" + ",\n".join(stage_js) + "\n  ],\n\n"
             f"  start: {js(start)},\n  screens: {{\n\n" + ",\n\n".join(screen_js) + "\n\n  }\n};")
    if "—" in block:
        warn(f"The content has {block.count(chr(0x2014))} em dash(es) (—). House style: use a comma, period or parentheses.")
    images = [meta[k] for k in ("meet_image", "close_image") if meta.get(k)] + images
    return meta, block, list(dict.fromkeys(images))


REPLY_USING = re.compile(r"\b(?:reply using|provide a response using)\b", re.I)


def title_key(t):
    """Same matching as the engine's Check Resources lock: ignores case,
    punctuation and &/and, so authors don't have to copy titles exactly."""
    return frozenset(re.sub(r"[^a-z0-9]+", " ", s(t).lower().replace("&", " and ")).split())


def title_matches(q, titles):
    """A quoted title matches when its words are all in an article's title, or
    the other way round (the engine also accepts a shortened title)."""
    k = title_key(q)
    return bool(k) and any(k <= t or t <= k for t in titles if t)


# ------------------------------- tracking ----------------------------------
FORM_E = re.compile(r"https://docs\.google\.com/forms/d/e/([A-Za-z0-9_-]+)")


def tracking_endpoint(link, field_numbers):
    """formResponse URL for the Sheet's Tracking form, or '' for no tracking."""
    link = s(link)
    if not link:
        return ""
    if "forms.gle/" in link:
        try:
            with urllib.request.urlopen(link, timeout=15) as r:
                link = r.geturl()
        except Exception:
            err("Meta tab: couldn't open the Tracking form short link. Paste the full Form link instead "
                "(Send > link icon, then uncheck \"Shorten URL\").")
            return ""
    m = FORM_E.search(link)
    if not m:
        err("Meta tab: Tracking form should be the Form's share link, which looks like "
            "https://docs.google.com/forms/d/e/.../viewform (Send > link icon). The edit link won't work.")
        return ""
    view = f"https://docs.google.com/forms/d/e/{m.group(1)}/viewform"
    try:
        with urllib.request.urlopen(view, timeout=15) as r:
            page = r.read().decode("utf-8", "replace")
        missing = [n for n in field_numbers if n not in page]
        if missing:
            err("Meta tab: the Tracking form's questions don't match the Care Dojo tracking Form, so rows "
                "wouldn't land in the right columns. Make your Form by copying the Care Dojo tracking Form "
                "(ask Stefani), then use the copy's link.")
    except Exception:
        warn("Couldn't open the Tracking form to check its questions (offline, or the Form isn't public). "
             "When you test-play, check that new rows appear in your tracking Sheet.")
    return f"https://docs.google.com/forms/d/e/{m.group(1)}/formResponse"


# ------------------------------- engine copy --------------------------------
def patch_engine(html, block, title, endpoint):
    def sub(pattern, repl, label, flags=0):
        nonlocal html
        new, n = re.subn(pattern, repl, html, count=1, flags=flags)
        if n != 1:
            sys.exit(f"STOPPED: the engine file changed and the converter couldn't find {label}. "
                     f"Ask Stefani to update scenario_xlsx_to_js.py.")
        html = new

    sub(r'(<script id="scenario">\s*)window\.SCENARIO = \{.*?\n\};(\s*</script>)',
        lambda m: m.group(1) + block + m.group(2), "the scenario block", re.S)
    sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", "the page title", re.S)
    # Inline text anywhere: a line that starts with "(" always begins a centered note.
    sub(r"else if\(!cur && /\^\\s\*\\\(/\.test\(line\)\)", lambda m: r"else if(/^\s*\(/.test(line))",
        "the inline-note rule")
    sub(r"const TELEMETRY_ENDPOINT = '[^']*';",
        lambda m: f"const TELEMETRY_ENDPOINT = '{endpoint}';   // blank = no tracking for this build",
        "the tracking endpoint")
    sub(r"(\n(\s*)try\{\s*\n\s*fetch\(TELEMETRY_ENDPOINT)",
        lambda m: f"\n{m.group(2)}if(!TELEMETRY_ENDPOINT) return;   // no Tracking form set{m.group(1)}",
        "the tracking call")
    return html


def field_numbers(html):
    m = re.search(r"const FIELD_IDS = \{(.*?)\};", html, re.S)
    return re.findall(r"entry\.(\d+)", m.group(1)) if m else []


# ------------------------------- main --------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Build a ready-to-test Care Dojo folder from a Sheet .xlsx")
    ap.add_argument("xlsx", help="the Sheet, downloaded as .xlsx")
    ap.add_argument("--out", help="build folder (default: '<Chat title> Test Build' next to the .xlsx)")
    ap.add_argument("--overwrite", action="store_true", help="replace an existing build's index.html")
    ap.add_argument("--js-only", action="store_true", help="print the window.SCENARIO block only")
    ap.add_argument("--engine", default=ENGINE, help=argparse.SUPPRESS)
    a = ap.parse_args()

    try:
        import openpyxl
    except ImportError:
        sys.exit("One-time setup needed. Run this, then try again:\n    python3 -m pip install openpyxl")
    if not os.path.exists(a.xlsx):
        sys.exit(f"Can't find the file: {a.xlsx}")
    if not a.xlsx.lower().endswith(".xlsx"):
        sys.exit("Use the .xlsx download (Google Sheets: File > Download > Microsoft Excel).")
    wb = openpyxl.load_workbook(a.xlsx, data_only=True)

    meta, block, images = build(wb)
    with open(a.engine, encoding="utf-8") as f:
        engine = f.read()
    endpoint = tracking_endpoint(meta.get("tracking_form"), field_numbers(engine)) if not a.js_only else ""

    for w in warnings:
        print("CHECK:", w)
    if errors:
        print()
        for e in errors:
            print("FIX:  ", e)
        print(f"\n{len(errors)} thing(s) to fix in the Sheet before it can build. "
              f"Fix them, download the .xlsx again, and re-run.")
        sys.exit(1)

    if a.js_only:
        print(block)
        return

    title = meta.get("title", "Chat Simulation")
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.xlsx)),
                                re.sub(r'[:/\\?*"<>|]+', " -", title).strip() + " Test Build")
    target = os.path.join(out, "index.html")
    if os.path.exists(target) and not a.overwrite:
        sys.exit(f"{target} already exists. Re-run with --overwrite to replace it, or pick another --out folder.")
    html = patch_engine(engine, block, title.replace("<", "&lt;"), endpoint)
    os.makedirs(out, exist_ok=True)
    for img in images:
        d = os.path.dirname(img)
        if d:
            os.makedirs(os.path.join(out, d), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nBuilt: {target}")
    print("Tracking: " + ("sends to your Tracking form" if endpoint else "off (no Tracking form on the Meta tab)"))
    todo = [i for i in images if not os.path.exists(os.path.join(out, i))]
    if todo:
        print("\nAdd these image files to the build folder (same folder/file names):")
        for i in todo:
            print("   ", i)
    print("\nNext: open this folder in Claude Code and ask for a local preview of index.html.")


if __name__ == "__main__":
    main()
