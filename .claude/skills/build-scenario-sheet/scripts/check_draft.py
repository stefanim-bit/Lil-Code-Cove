#!/usr/bin/env python3
"""Check a scenario draft JSON and (optionally) turn it into Google Sheets values.

Usage:
    python3 check_draft.py <scenario-draft.json>
    python3 check_draft.py <scenario-draft.json> --values <sheet-values.json> [--clear-rows 60]

Prints ERRORS (must fix) and WARNINGS (fix or explain to the user). Exit code 1 if
there are errors. With --values, writes {"<Tab>": {"range": "...", "values": [[...]]}}
for update_values, one entry per tab (Meta, Stages, Screens, Choices, Articles),
padded with "" so leftover template rows are cleared. Stdlib only.
"""
import argparse
import json
import re
import sys
from collections import defaultdict

STAGE_IDS = ["open", "dynamics", "familiarize", "clarify", "roadmap", "recreate", "article", "solve"]
VERDICTS = {"correct", "partial", "incorrect"}
BEHAVIOR_WORDS = ["familiariz", "clarif", "roadmap", "dynamics", "recreate", "empath", "rapport", "opening", "closing"]

HEADERS = {
    "Meta": ["field", "value", "notes"],
    "Stages": ["id", "name", "max", "strength (shown at end if done well)",
               "improvement (shown at end if missed/partial)"],
    "Screens": ["screen_id", "stage", "gate (Y/N)", "learner (expert line, optional)",
                "speaker (caller line, optional)", "prompt (neutral — never names the behavior)"],
    "Choices": ["screen_id", "choice_id", "text", "verdict (correct/partial/incorrect)", "points",
                "goTo (screen_id or __end__)", "retry (Y/N)", "capIfRetried",
                "consequence (optional caller reaction or inline outcome) 1",
                "consequence (optional expert reply or inline outcome)",
                "consequence (optional caller reaction or inline outcome) 2",
                "stage Override (optional)", "credit_stage (optional floating credit)",
                "credit_points", "credit_verdict", "asset"],
    "Articles": ["title", "stage (this credits)", "article_title", "URL", "correct (Y/N)", "Credit"],
}
COLS = {"Meta": "C", "Stages": "E", "Screens": "F", "Choices": "P", "Articles": "F"}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def s(v):
    return "" if v is None else str(v)


def num(v):
    if v in (None, ""):
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() else f
    except (TypeError, ValueError):
        return None


def norm_title(t):
    return re.sub(r"[\s.,;:]+$", "", t.strip()).replace("’", "'").lower()


def reply_titles(text):
    m = re.search(r"Reply using (.+)$", text)
    return re.findall(r"[\"“](.+?)[\"”]", m.group(1)) if m else []


def walk_strings(obj, path="draft"):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


def check(d):
    meta = d.get("meta", {})
    stages = d.get("stages", [])
    screens = d.get("screens", [])
    choices = d.get("choices", [])
    articles = d.get("articles", [])

    # Copy rules
    for path, text in walk_strings(d):
        if "—" in text:
            err(f"Em-dash in {path}: {text[:80]!r}")

    # Meta
    for k in ("title", "userBio", "start"):
        if not s(meta.get(k)).strip():
            err(f"meta.{k} is empty")
    bio = s(meta.get("userBio")).replace("’", "'")
    if bio.lower().startswith("meet "):
        err("userBio starts with 'Meet ...': the name belongs in the title only")
    if not re.search(r"In this activity, you'll simulate a (chat|call) with (him|her|them)\.", bio):
        warn("userBio is missing the boilerplate \"In this activity, you'll simulate a chat/call with him/her/them.\"")
    if "Check Resources" not in bio:
        warn("userBio is missing the *\"Check Resources\"* sentence")
    asset_keys = set()
    for a in meta.get("assets", []):
        key = s(a.get("key"))
        if not key.startswith("asset."):
            err(f"Meta asset key {key!r} must start with 'asset.'")
        asset_keys.add(key)

    # Stages
    ids = [x.get("id") for x in stages]
    if ids and sorted(ids) != sorted(STAGE_IDS):
        warn(f"Stage ids differ from the default eight: {ids}. Confirmed with the user?")
    total = sum(num(x.get("max")) or 0 for x in stages)
    if total != 100:
        err(f"Stage max values sum to {total}, not 100")
    stage_max = {x.get("id"): num(x.get("max")) or 0 for x in stages}
    additive = {x.get("id") for x in stages if x.get("additive")}
    for x in stages:
        if not s(x.get("strength")).strip() or not s(x.get("improvement")).strip():
            err(f"Stage {x.get('id')}: strength and improvement are both required")

    # Screens
    screen_ids = [x.get("screen_id") for x in screens]
    dupes = {i for i in screen_ids if screen_ids.count(i) > 1}
    if dupes:
        err(f"Duplicate screen_id(s): {sorted(dupes)}")
    screen_stage = {x.get("screen_id"): x.get("stage") for x in screens}
    if meta.get("start") and meta.get("start") not in screen_stage:
        err(f"start {meta.get('start')!r} is not a screen")
    for x in screens:
        if x.get("stage") not in stage_max:
            err(f"Screen {x.get('screen_id')}: unknown stage {x.get('stage')!r}")
        if s(x.get("gate")) not in ("Y", "N"):
            err(f"Screen {x.get('screen_id')}: gate must be Y or N")
        prompt = s(x.get("prompt"))
        if not prompt.strip():
            err(f"Screen {x.get('screen_id')}: prompt is empty")
        hits = [w for w in BEHAVIOR_WORDS if w in prompt.lower()]
        if hits:
            warn(f"Screen {x.get('screen_id')}: prompt may name the behavior ({hits}): {prompt!r}")

    # Choices
    by_screen = defaultdict(list)
    for c in choices:
        by_screen[c.get("screen_id")].append(c)
    article_titles = {}
    for a in articles:
        for t in re.findall(r"[\"“](.+?)[\"”]", s(a.get("article_title"))):
            article_titles[norm_title(t)] = a
    for c in choices:
        cid = f"{c.get('screen_id')}/{c.get('choice_id')}"
        if c.get("screen_id") not in screen_stage:
            err(f"Choice {cid}: screen_id is not a screen")
        if c.get("verdict") not in VERDICTS:
            err(f"Choice {cid}: verdict must be correct/partial/incorrect")
        pts = num(c.get("points"))
        if pts is None:
            err(f"Choice {cid}: points missing")
        stage = c.get("stageOverride") or screen_stage.get(c.get("screen_id"))
        if pts is not None and stage in stage_max and pts > stage_max[stage]:
            err(f"Choice {cid}: {pts} points is over the {stage} max ({stage_max[stage]})")
        if c.get("verdict") == "incorrect" and pts:
            warn(f"Choice {cid}: incorrect but worth {pts} points")
        if c.get("verdict") == "correct" and pts == 0:
            warn(f"Choice {cid}: correct but worth 0 points")
        go = c.get("goTo")
        if go != "__end__" and go not in screen_stage:
            err(f"Choice {cid}: goTo {go!r} is not a screen or __end__")
        if s(c.get("retry")) == "Y" and num(c.get("capIfRetried")) is None:
            err(f"Choice {cid}: retry Y needs capIfRetried")
        if c.get("credit_stage") and c.get("credit_stage") not in stage_max:
            err(f"Choice {cid}: credit_stage {c.get('credit_stage')!r} is not a stage")
        if c.get("credit_stage") and num(c.get("credit_points")) is None:
            err(f"Choice {cid}: credit_stage needs credit_points")
        if c.get("asset") and c.get("asset") not in asset_keys:
            err(f"Choice {cid}: asset {c.get('asset')!r} is not a Meta asset key")
        for t in reply_titles(s(c.get("text"))):
            if norm_title(t) not in article_titles:
                err(f"Choice {cid}: 'Reply using \"{t}\"' has no matching row in Articles")

    for sid, cs in by_screen.items():
        letters = [c.get("choice_id") for c in cs]
        if len(set(letters)) != len(letters):
            err(f"Screen {sid}: duplicate choice ids {letters}")
        if not 2 <= len(cs) <= 5:
            warn(f"Screen {sid}: {len(cs)} choices (usual is 2 to 4, template goes up to 5)")
        if not any(c.get("verdict") == "correct" for c in cs):
            warn(f"Screen {sid}: no correct choice")
    for sid in screen_stage:
        if sid not in by_screen:
            err(f"Screen {sid}: has no choices")

    # Reachability
    seen, todo = set(), [meta.get("start")]
    while todo:
        cur = todo.pop()
        if cur in seen or cur not in screen_stage:
            continue
        seen.add(cur)
        todo.extend(c.get("goTo") for c in by_screen.get(cur, []))
    for sid in screen_stage:
        if sid not in seen:
            err(f"Screen {sid}: unreachable from start")
    if not any(c.get("goTo") == "__end__" for c in choices):
        err("No choice goes to __end__")

    # Each stage reachable to its max
    best = defaultdict(float)
    per_screen = defaultdict(lambda: defaultdict(float))
    for c in choices:
        stage = c.get("stageOverride") or screen_stage.get(c.get("screen_id"))
        p = num(c.get("points")) or 0
        per_screen[stage][c.get("screen_id")] = max(per_screen[stage][c.get("screen_id")], p)
        if c.get("credit_stage"):
            cs_ = c["credit_stage"]
            per_screen[cs_]["credit:" + cid_of(c)] = max(per_screen[cs_]["credit:" + cid_of(c)],
                                                         num(c.get("credit_points")) or 0)
    for st, mx in stage_max.items():
        vals = per_screen.get(st, {})
        got = sum(vals.values()) if st in additive else max(vals.values(), default=0)
        best[st] = got
        if got < mx:
            warn(f"Stage {st}: best path reaches {got:g} of {mx}"
                 + ("" if st in additive else " (mark it additive if it spans screens?)"))

    # Answer position and length
    letters, longest, single = defaultdict(int), 0, 0
    for sid, cs in by_screen.items():
        correct = [c for c in cs if c.get("verdict") == "correct"]
        for c in correct:
            letters[c.get("choice_id")] += 1
        if len(correct) == 1 and len(cs) > 1:
            single += 1
            lens = sorted((len(s(c.get("text"))) for c in cs), reverse=True)
            if len(s(correct[0].get("text"))) == lens[0] and lens[0] > lens[1]:
                longest += 1
    n = len(by_screen)
    for L, k in letters.items():
        if n >= 4 and k > n / 2:
            warn(f"Choice {L} is correct on {k} of {n} screens. Shuffle positions")
    if single >= 4 and longest / single > 0.6:
        warn(f"The correct choice is the longest on {longest} of {single} screens. Trim it or lengthen distractors")

    # Articles
    for a in articles:
        if s(a.get("correct")) not in ("Y", "N", "Partial"):
            err(f"Article {a.get('article_title')!r}: correct must be Y, N or Partial")
        if not s(a.get("url")).startswith("http"):
            err(f"Article {a.get('article_title')!r}: URL missing")
    if articles and not any(s(a.get("correct")) == "Y" for a in articles):
        err("No article is marked correct (Y)")
    if not articles:
        warn("Articles tab is empty")


def cid_of(c):
    return f"{c.get('screen_id')}/{c.get('choice_id')}"


NUMLIKE = re.compile(r"^\s*[-+]?(\d[\d,]*\.?\d*|\.\d+)\s*%?\s*$|^\s*\d{1,4}[/-]\d{1,2}([/-]\d{1,4})?\s*$")


def cell_text(v):
    """Keep text as text: update_values parses like the Sheets UI."""
    t = s(v)
    if t and (t[0] in "=+-@" or NUMLIKE.match(t) or t.upper() in ("TRUE", "FALSE")):
        return "'" + t
    return t


def cell_num(v):
    n = num(v)
    return "" if n is None else n


def build_values(d, clear_rows):
    meta = d["meta"]
    res = meta.get("resources", {})
    rows = {
        "Meta": [["title", cell_text(meta["title"]), "Shown in the chat header."],
                 ["userBio", cell_text(meta["userBio"]), "One line: who they are + why they're calling."],
                 ["start", cell_text(meta["start"]),
                  "screen_id of the very first screen (must exist in the Screens tab)."]]
        + [[a["key"], cell_text(a.get("value", "")), cell_text(a.get("notes", ""))]
           for a in meta.get("assets", [])]
        + [["resources.title", cell_text(res.get("title", "Check Resources")),
            "Title for the resources button/drawer."],
           ["resources.sheet", cell_text(res.get("sheet", "Articles")), "Source tab for reference articles."],
           ["resources.enabled", "TRUE" if res.get("enabled", True) else "FALSE",
            "Whether the resources helper drawer is enabled."]],
        "Stages": [[x["id"], cell_text(x["name"]), cell_num(x["max"]), cell_text(x.get("strength")),
                    cell_text(x.get("improvement"))] for x in d["stages"]],
        "Screens": [[x["screen_id"], x["stage"], x.get("gate", "Y"), cell_text(x.get("learner")),
                     cell_text(x.get("speaker")), cell_text(x.get("prompt"))] for x in d["screens"]],
        "Choices": [[c["screen_id"], c["choice_id"], cell_text(c.get("text")), c.get("verdict", ""),
                     cell_num(c.get("points")), c.get("goTo", ""), c.get("retry") or "N",
                     cell_num(c.get("capIfRetried")), cell_text(c.get("caller1")),
                     cell_text(c.get("expert")), cell_text(c.get("caller2")),
                     s(c.get("stageOverride")), s(c.get("credit_stage")), cell_num(c.get("credit_points")),
                     s(c.get("credit_verdict")), s(c.get("asset"))] for c in d["choices"]],
        "Articles": [["Check Resources", "article", cell_text(a["article_title"]), s(a.get("url")),
                      s(a.get("correct")), cell_num(a.get("credit"))] for a in d.get("articles", [])],
    }
    out = {}
    for tab, data in rows.items():
        width = len(HEADERS[tab])
        grid = [HEADERS[tab]] + data
        total = max(len(grid), clear_rows)
        grid += [[""] * width for _ in range(total - len(grid))]
        out[tab] = {"range": f"'{tab}'!A1:{COLS[tab]}{total}", "values": grid}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--values", help="write sheet values JSON here")
    ap.add_argument("--clear-rows", type=int, default=60,
                    help="pad every tab to at least this many rows so old template rows are cleared")
    a = ap.parse_args()
    with open(a.draft, encoding="utf-8") as f:
        d = json.load(f)
    check(d)
    for e in errors:
        print("ERROR:  ", e)
    for w in warnings:
        print("WARNING:", w)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s); "
          f"{len(d.get('screens', []))} screens, {len(d.get('choices', []))} choices, "
          f"{len(d.get('articles', []))} articles")
    if errors:
        sys.exit(1)
    if a.values:
        with open(a.values, "w", encoding="utf-8") as f:
            json.dump(build_values(d, a.clear_rows), f, ensure_ascii=False, indent=1)
        print(f"Sheet values written to {a.values}")


if __name__ == "__main__":
    main()
