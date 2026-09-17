# Paste into Rise → test in Smart

The file to paste: **[index.html](index.html)** (in this folder). It's the entire 10-scene branching scenario as one self-contained Code Block — verified working end-to-end locally (all branching, the 1.5 loop-back + score cap, PathTaken, and per-choice telemetry all confirmed).

## Steps

1. In your Rise lesson: **Add Block → All Blocks → Code** → **Add code**.
2. Open [index.html](index.html), select all, copy, and paste the **entire** contents into the code editor. (Per Articulate's docs, the Code Block runs your paste as a real `index.html` inside an iframe — so it's fine that the file starts with `<meta charset="utf-8">`.)
3. Save the block.
4. **Preview inside Rise first** — click "Take the Call", walk a few choices, confirm the dialogue and buttons render and clicking advances scenes. (Open the "show/hide debug log" link at the bottom to watch rows send.)
5. **Publish → upload to Smart** (fresh course, per your usual test hygiene) and walk it there.

## What to check in Smart

- **Branching:** every choice advances to the right next scene; at Scene 1.5, picking "Okay, so you want a drop-down" or "Have you tried refreshing" loops back to 1.5 with a "still on the line" banner, and picking correctly *after* that advances to 1.6.
- **The Sheet:** each choice lands a row tagged `course = Practice Session 1 - Wix Editor Sub-pages - Rise POC`, with `scene`, `interaction` (the criterion), `response` (choice text), `correct` (yes/no), and `points`. A retry-capped correct answer at 1.5 shows `points = 8` and `notes` containing `retry-capped`.
- **learner_email will still be `NO-API`** — expected. The Code Block sandbox blocks SCORM; identity is the separate short-code step we've deliberately deferred (see [../IDENTITY-LINKING-OPTIONS.md](../IDENTITY-LINKING-OPTIONS.md)). This test is branching + choice telemetry only.

## What's deliberately not in this build yet (all additive, no rebuild)

- **Scoring display + score slide (1.12/1.13)** — but every choice's `correct`/`points` and all the boolean flags (`EtiquetteOpen`, `AskedForHelp`, etc.) are *already being recorded* in state and sent to the Sheet, so adding the on-screen score is a read, not a rework.
- **Helper buttons** (Open CSI · Ask a Colleague · Check the Articles) — the header has a mount point reserved; `AskedForHelp` (which caps ScoreSolving at 1.8) already exists in state.
- **Short-code identity** — one line (`SESSION_CODE`) is the only hook; everything sends with or without it.

## Before this ever goes near real Experts

- Remove the debug log block (marked in the file) — it exposes internal state.
- Keep the `- Rise POC` course suffix on test runs so they filter out of real data.
