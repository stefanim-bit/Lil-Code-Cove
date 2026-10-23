#!/usr/bin/env python3
"""Compare a scenario Sheet (downloaded as .xlsx) with a live build's index.html.

Used by the skill's migrate mode: before moving an older sheet to the new template,
list every place where the sheet and the live code disagree so the user can pick
which one wins.

    python3 compare_sheet_code.py <sheet.xlsx> <index.html> [--choices-tab "Chat Choices"]
                                  [--json out.json]

The sheet is read with scenario_xlsx_to_js.py (any header generation), so the
comparison is engine-shaped: what the sheet would build vs. what the code has.
Text is compared after straightening quotes and collapsing spaces; speaker
labels ("Sarah:", "Caller:", "Expert:") are ignored in reactions.
"""
import argparse
import importlib.util
import json
import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CONVERTER = os.path.join(REPO, "Authoring & Code Rule Docs", "scenario_xlsx_to_js.py")


# ------------------------------- JS literal parser --------------------------
class JSParser:
    """Just enough JavaScript to read a window.SCENARIO object literal."""

    def __init__(self, src, pos=0):
        self.s, self.i = src, pos

    def ws(self):
        while self.i < len(self.s):
            c = self.s[self.i]
            if c.isspace():
                self.i += 1
            elif self.s.startswith("//", self.i):
                end = self.s.find("\n", self.i)
                self.i = len(self.s) if end < 0 else end
            elif self.s.startswith("/*", self.i):
                self.i = self.s.index("*/", self.i) + 2
            else:
                break

    def value(self):
        v = self.single()
        self.ws()
        while self.i < len(self.s) and self.s[self.i] == "+":  # "a" + "b"
            self.i += 1
            self.ws()
            v = f"{v}{self.single()}"
            self.ws()
        return v

    def single(self):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'`":
            return self.string()
        m = re.compile(r"-?\d+(\.\d+)?").match(self.s, self.i)
        if m:
            self.i = m.end()
            return float(m.group()) if m.group(1) else int(m.group())
        m = re.compile(r"[A-Za-z_$][\w$]*").match(self.s, self.i)
        if m:
            self.i = m.end()
            return {"true": True, "false": False, "null": None, "undefined": None}.get(m.group(), m.group())
        raise ValueError(f"Unexpected {c!r} at {self.i}")

    def string(self):
        q = self.s[self.i]
        self.i += 1
        out = []
        esc = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}
        while self.s[self.i] != q:
            c = self.s[self.i]
            if c == "\\":
                n = self.s[self.i + 1]
                if n == "u":
                    out.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                    continue
                if n == "\n":
                    self.i += 2
                    continue
                out.append(esc.get(n, n))
                self.i += 2
            else:
                out.append(c)
                self.i += 1
        self.i += 1
        return "".join(out)

    def obj(self):
        self.i += 1
        out = {}
        while True:
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return out
            key = self.string() if self.s[self.i] in "\"'" else self.single()
            self.ws()
            assert self.s[self.i] == ":", f"expected : at {self.i}"
            self.i += 1
            out[str(key)] = self.value()
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1

    def arr(self):
        self.i += 1
        out = []
        while True:
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
                return out
            out.append(self.value())
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1


def scenario_from_js(text):
    m = re.search(r"window\.SCENARIO\s*=\s*\{", text)
    if not m:
        sys.exit("Couldn't find window.SCENARIO in the code file.")
    return JSParser(text, m.end() - 1).value()


# ------------------------------- reading the sheet --------------------------
class Workbook:
    """Presents the sheet's tabs under the names the converter expects."""

    def __init__(self, wb, choices_tab):
        self.tabs = {ws.title: ws for ws in wb}
        self.map = {}
        for want, options in (("Choices", [choices_tab, "Choices", "Chat Choices"]),
                              ("Articles", ["Articles", "Helpers - Articles"])):
            for o in options:
                if o and o in self.tabs:
                    self.map[want] = o
                    break
        for t in ("Meta", "Stages", "Screens"):
            if t in self.tabs:
                self.map[t] = t
        self.sheetnames = list(self.map)

    def __getitem__(self, name):
        return Rows(self.tabs[self.map[name]], name)


class Rows:
    def __init__(self, ws, name):
        self.ws, self.name = ws, name

    def iter_rows(self, values_only=True):
        rows = list(self.ws.iter_rows(values_only=True))
        if not rows:
            return iter(rows)
        if self.name == "Stages":
            # Old sheets end with a "Total max must equal 100" helper row.
            rows = rows[:1] + [r for r in rows[1:] if not (r and r[0] and " " in str(r[0]).strip())]
        if self.name == "Articles":
            rows = clean_articles(rows)
        return iter(rows)


OPEN_ACTION = re.compile(r"^\s*(?:\[action\]\s*)?(?:open|(?:provide a )?reply using)\s*", re.I)


def clean_articles(rows):
    """Oldest sheets: Title | Stage | article_title | (blank header = link) | correct, with
    titles like '[Action] Open "X"' and correct/incorrect instead of Y/N."""
    head = list(rows[0])
    low = [str(h or "").strip().lower() for h in head]
    if "url" not in low and "article link" not in low and None in head:
        n = head.index(None)
        if any(len(r) > n and str(r[n] or "").startswith("http") for r in rows[1:]):
            head[n] = "url"
    tcol = next((i for i, h in enumerate(low) if h.startswith("article title") or h == "article_title"), None)
    rcol = next((i for i, h in enumerate(low) if h.startswith("right article") or h.startswith("correct")), None)
    out = [tuple(head)]
    for r in rows[1:]:
        r = list(r) + [None] * (len(head) - len(r))
        if tcol is None or not str(r[tcol] or "").strip():
            continue  # notes or blank rows under the table
        t = OPEN_ACTION.sub("", str(r[tcol]).translate(QUOTES)).strip()
        r[tcol] = re.sub(r"^[\"']+|[\"'.]+$", "", t).strip()
        if rcol is not None:
            v = str(r[rcol] or "").strip().lower()
            r[rcol] = {"correct": "Y", "incorrect": "N", "partial": "Partial"}.get(v, r[rcol])
        out.append(tuple(r))
    return out


def load_converter():
    spec = importlib.util.spec_from_file_location("conv", CONVERTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------- comparing ----------------------------------
QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "—": "-", "–": "-"})


def norm(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else ""
    return re.sub(r"\s+", " ", str(v).translate(QUOTES)).strip()


def norm_reply(v, names):
    """Reaction text without speaker labels, so 'Caller: hi' == 'Sarah: hi'."""
    t = str(v or "").translate(QUOTES)
    label = re.compile(rf"(?m)^\s*(?:{'|'.join(map(re.escape, names))})\s*:\s*", re.I)
    while label.search(t):  # old sheets wrote the name, and the converter adds it again
        t = label.sub("", t)
    return re.sub(r"\s+", " ", t).strip()


def loose(v):
    """Words only: ignores quotes, punctuation, (inline) parentheses and a missing
    [Action] tag, which old sheets wrote differently from the build."""
    t = re.sub(r"^\s*\[action\]\s*", "", norm(v).lower())
    return " ".join(re.sub(r"[^a-z0-9]+", " ", t).split())


def compare(sheet, code):
    """Each difference gets a kind:
    conflict = both have a value and they differ (the user picks),
    fill     = the sheet is blank and the code has it (migration copies it in),
    format   = same words, different punctuation or quoting (migration uses the code's)."""
    diffs = []

    def add(where, field, s, c, kind="conflict"):
        diffs.append({"kind": kind, "where": where, "field": field, "sheet": s, "code": c})

    def cmp(where, field, s, c, f=norm):
        if f(s) == f(c):
            return
        if not norm(s) and norm(c):
            add(where, field, s, c, "fill")
        elif loose(f(s)) == loose(f(c)):
            add(where, field, s, c, "format")
        else:
            add(where, field, s, c)

    su, cu = dict(sheet.get("user", {})), code.get("user", {})
    if su.get("name") == "Caller":  # the converter's stand-in for a blank User name
        su["name"] = ""
    names = ["expert", "caller", "customer", "user", su.get("name") or "x", cu.get("name") or "x"]
    cmp("Meta", "Chat title", sheet.get("title"), code.get("title"))
    cmp("Meta", "First screen", sheet.get("start"), code.get("start"))
    for k, label in (("name", "User name"), ("bio", "Intro bio"),
                     ("image", "Meet image"), ("completeImage", "Close image")):
        cmp("Meta", label, su.get(k), cu.get(k))

    # Stages
    ss = {x["id"]: x for x in sheet.get("stages", [])}
    cs = {x["id"]: x for x in code.get("stages", [])}
    if list(ss) != list(cs) and set(ss) == set(cs):
        add("Stages", "order", ", ".join(ss), ", ".join(cs))
    for sid in dict.fromkeys(list(ss) + list(cs)):
        a, b = ss.get(sid), cs.get(sid)
        if not a or not b:
            add(f"Stages {sid}", "row", "present" if a else "missing", "present" if b else "missing")
            continue
        for k, label in (("name", "Name on scorecard"), ("max", "Max points"), ("strength", "Strength"),
                         ("improvement", "Improvement"), ("additive", "Additive")):
            cmp(f"Stages {sid}", label, a.get(k), b.get(k))

    # Articles
    sr = (sheet.get("resources") or {}).get("items", [])
    cr = (code.get("resources") or {}).get("items", [])
    # Pair articles by link first, then by title words (sheets shorten or reword titles).
    words = lambda x: set(re.sub(r"[^a-z0-9]+", " ", norm(x.get("label")).lower().replace("&", "and")).split())
    left = list(cr)
    for a in sr:
        b = next((b for b in left if norm(b.get("url")) == norm(a.get("url"))), None)
        if b is None:
            b = next((b for b in left if words(a) and (words(a) <= words(b) or words(b) <= words(a))), None)
        where = f"Articles \"{a.get('label')}\""
        if b is None:
            add(where, "row", "present", "missing")
            continue
        left.remove(b)
        cmp(where, "Article title", a.get("label"), b.get("label"))
        cmp(where, "Article link", a.get("url"), b.get("url"))
        cmp(where, "Right article?", "Y" if a.get("correct") else "N", "Y" if b.get("correct") else "N")
    for b in left:
        add(f"Articles \"{b.get('label')}\"", "row", "missing", "present")

    # Screens and choices
    sx, cx = sheet.get("screens", {}), code.get("screens", {})
    if list(sx) != list(cx) and set(sx) == set(cx):
        add("Screens", "order", ", ".join(sx), ", ".join(cx))
    for sid in dict.fromkeys(list(sx) + list(cx)):
        a, b = sx.get(sid), cx.get(sid)
        if not a or not b:
            add(f"Screen {sid}", "row", "present" if a else "missing", "present" if b else "missing")
            continue
        cmp(f"Screen {sid}", "Stage scored", a.get("stage"), b.get("stage"))
        cmp(f"Screen {sid}", "User/Expert message", a.get("speaker"), b.get("speaker"),
            lambda v: norm_reply(v, names))
        cmp(f"Screen {sid}", "Question or Prompt", a.get("prompt"), b.get("prompt"))
        ac = {c["id"]: c for c in a.get("choices", [])}
        bc = {c["id"]: c for c in b.get("choices", [])}
        for cid in dict.fromkeys(list(ac) + list(bc)):
            p, q = ac.get(cid), bc.get(cid)
            where = f"Choice {sid} {cid}"
            if not p or not q:
                add(where, "row", "present" if p else "missing", "present" if q else "missing")
                continue
            for k, label in (("text", "Choice text"), ("verdict", "Rating"), ("points", "Points"),
                             ("goTo", "Next screen"), ("retry", "Retry"), ("capIfRetried", "Max on retry"),
                             ("retryOnly", "Only after a retry"), ("stageOverride", "Score to a different stage")):
                cmp(where, label, p.get(k), q.get(k))
            cmp(where, "Reactions", p.get("consequence"), q.get("consequence"),
                lambda v: norm_reply(v, names))
            pc, qc = (p.get("credits") or [{}])[0], (q.get("credits") or [{}])[0]
            cmp(where, "Extra credit", json.dumps(pc, sort_keys=True) if pc else "",
                json.dumps(qc, sort_keys=True) if qc else "")
            pi = os.path.basename(unquote(str((p.get("image") or {}).get("src", ""))))
            qi = os.path.basename(unquote(str((q.get("image") or {}).get("src", ""))))
            cmp(where, "Screenshot", pi, qi)
    return diffs


def code_only_fields(code):
    """Engine fields in the code the new template has no column for."""
    known = {"id", "text", "verdict", "points", "goTo", "retry", "capIfRetried", "retryOnly",
             "stageOverride", "consequence", "credits", "image", "showsImage", "showsImageAfter"}
    found = {}
    for sid, x in code.get("screens", {}).items():
        for k in x:
            if k not in ("stage", "speaker", "prompt", "choices"):
                found.setdefault(f"screen.{k}", []).append(sid)
        for c in x.get("choices", []):
            for k in c:
                if k not in known:
                    found.setdefault(f"choice.{k}", []).append(f"{sid} {c.get('id')}")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("xlsx")
    ap.add_argument("html")
    ap.add_argument("--choices-tab", help="which tab holds the chat choices (default: Choices, else Chat Choices)")
    ap.add_argument("--json", help="also write the differences to this JSON file")
    a = ap.parse_args()

    import openpyxl
    conv = load_converter()
    wb = Workbook(openpyxl.load_workbook(a.xlsx, data_only=True), a.choices_tab)
    _, block, _ = conv.build(wb)
    sheet = scenario_from_js(block)
    with open(a.html, encoding="utf-8") as f:
        code = scenario_from_js(f.read())

    diffs = compare(sheet, code)
    extra = code_only_fields(code)
    print(f"Sheet tabs used: {wb.map}")
    for e in conv.errors:
        print("SHEET ISSUE:", e)
    for kind, title in (("conflict", "CONFLICTS (pick sheet or code)"),
                        ("fill", "BLANK IN SHEET, IN CODE (copied in)"),
                        ("format", "FORMAT ONLY (code's version used)")):
        group = [d for d in diffs if d["kind"] == kind]
        print(f"\n{title}: {len(group)}")
        for d in group if kind != "format" else []:
            print(f"- {d['where']} | {d['field']}\n    sheet: {d['sheet']!r}\n    code:  {d['code']!r}")
    if extra:
        print("\nCode fields with no sheet column (ignored):")
        for k, v in extra.items():
            print(f"- {k}: {len(v)} ({', '.join(v[:6])}{'...' if len(v) > 6 else ''})")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"tabs": wb.map, "sheet_issues": conv.errors, "diffs": diffs, "code_only": extra},
                      f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
