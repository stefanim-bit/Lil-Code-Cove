> ⚠️ **SUPERSEDED — do not author to this doc.** The current authoring model is **`SCENARIO_AUTHORING_HANDOFF.md`** (`window.SCENARIO` schema: 8 stages, `verdict`/`goTo`/`credits`, no pass/fail shown). This file uses an older `SCENES`/`flags`/`correct` schema and a 9-criteria rubric and is kept for reference only.

# Handoff — authoring branching-scenario content for the Practice Session engine

**Purpose.** You're about to write the *content* of one or more practice-call scenarios in a separate Cowork project. This doc tells you the exact shape that content must take so it drops into the already-built, already-tested engine here with no re-interpretation. Write to this format and bringing it back is copy-paste; write freely and it's a translation job.

**Audience.** A content builder who has NOT seen the engine. Everything you need is below.

Last updated: 2026-08-13.

---

## 1. What already exists (the target you're authoring for)

There is a working "practice call" simulation that runs as a single **Articulate Rise Code Block** (one self-contained HTML/JS file). It is proven end-to-end: branching, scoring, resource-use tracking, and per-click data capture to a Google Sheet all work in Rise and are being validated in the Wix Smart LMS.

You do **not** touch any of the plumbing. The engine already handles:
- Rendering scenes, choices, consequence feedback, and Continue/Back flow.
- Branching, including loop-backs (send the learner back to retry a scene).
- Scoring per criterion, a final score slide, and conditional feedback lines.
- Three optional helper buttons (Open CSI, Ask a Colleague, Check the Articles).
- Per-click telemetry to a Google Sheet, plus a final summary row.

**Your job is only to produce the scenario content, mapped to the data schema in §4.** The reference implementation is `rise-branching-scenario/index.html` in the Code project (that's "Practice Session 1 — Wix Editor: Sub-pages"). The source it was built from is `Practice_Session_1_-_Wix_Editor_Sub-pages_Storyboard__Final_.pdf` — read that first; it's the model for tone, structure, and scoring.

---

## 2. The interaction model (locked — do not invent new formats)

Every scenario is a linear-ish chain of **decision scenes**. Each decision scene is:

- One **situation** — a line the caller says (or a short prompt).
- **2–4 choices**, each a single-select button.
- Each choice has **consequence feedback**, a **score**, a **destination** (next scene, loop back, or end), and optional **flags**.

That's the whole vocabulary. The engine supports exactly this. It does **not** support (without new engineering — flag it if a scenario needs one):
- multi-select / "pick many"
- drag-and-drop, sorting, matching
- free-text entry
- timed decisions
- media beyond text (no audio/video/images yet)

If your scenario truly needs one of those, call it out separately as an engine change request — don't smuggle it into the content.

An **intro scene** (welcome + "start" button) and the **score slides** at the end are also part of the model (see §6, §7).

---

## 3. The scoring model (locked)

- Each decision scene maps to **one scoring criterion** with a **maximum**.
- The **sum of all criteria maxima = 100** for a full scenario. (Practice Session 1's split, for reference: Etiquette 5 · Tools 10 · Familiarization 10 · Clarifying 15 · Roadmapping 10 · Article 15 · Recreate 10 · Solving 20 · Suggestions 5 = 100.) A new scenario can use different criteria and a different split, **but it must total 100.**
- The **correct** choice normally earns the criterion's full max. Distractors earn **partial** (a "close but…" answer) or **0** (a wrong/harmful answer). Decide the partial values deliberately — they're a teaching signal, not decoration.
- Exactly **one** choice per scene is marked correct.
- **No pass/fail is shown to the learner** — only the per-criterion table and a total out of 100. (This is a deliberate design decision carried over from PS1.)

### Special scoring mechanics you can use (all already supported):

- **Etiquette split across two scenes.** PS1 scores "opening etiquette" at the first decision and "closing etiquette" at the last, then combines them: both good = 5, one good = 3, neither = 0. If your scenario does this, mark the opening scene's correct choice with a flag and the closing scene's correct choice with another flag (see `EtiquetteOpen`/`EtiquetteClose` in §5).
- **Loop-back with a cap.** A distractor can send the learner *back* to the same scene to try again ("choices still live"). When it does, the scene can **cap** the score they can still earn on the retry (PS1 caps Clarifying at its partial value of 8 after a guess). See `next: 'return'` and `retryCap` in §4.
- **Score that depends on behaviour.** A choice's points can depend on a flag — e.g. PS1's "Solving" is worth 20, but only 10 if the learner used a colleague hint anywhere in the call. See the "conditional points" note in §4.

---

## 4. The data schema (THE part that matters for bring-back)

The engine reads one JavaScript object called `SCENES`. Each key is a scene id (a string like `'1.2'`). **Author each scene as one object literal following the annotated template below.** If you produce exactly this, I paste it straight in.

```js
'1.2': {                              // scene id — unique, ordered (1.2, 1.3, …)
  title: 'Opening the Call',          // short scene title (shown as a badge)
  criterion: 'Opening etiquette',     // the scoring criterion label; also the telemetry "interaction" value.
                                      //   Keep it consistent — same wording everywhere it appears.
  pathLabel: 'Open',                  // ONE short word; used to build the readable "path taken" summary
  speaker: 'Sam Trent',               // who is talking in the situation line
  situation: 'Hi — I’m trying to add sub-pages to my menu and it’s just not working.',
                                      // the caller's line / the prompt. Verbatim, learner-facing.

  // OPTIONAL scene-level fields:
  retryCap: 8,                        // include ONLY if a choice loops back; caps retry score at this value
  showCheckArticles: true,            // include ONLY if the "Check the Articles" helper appears on this scene

  choices: [
    {
      text: 'That sounds frustrating. Let me take a look.',   // exact button wording, learner-facing
      feedback: 'Kind, and that counts — but you haven’t told Sam what you’re doing.',
                                      // consequence feedback shown after the click
      correct: false,                 // true on exactly one choice per scene
      points: 0,                      // number 0..max
      next: '1.3'                     // destination: another scene id | 'return' (loop back) | 'end'
      // flags: { EtiquetteOpen: true } // OPTIONAL — see §5
    },
    {
      text: 'Hi, you’re through to Wix Support, this is [name]. Sorry you’ve been stuck — can I start with the email on your account?',
      feedback: 'Good open. Sam knows who you are, that you heard them, and what’s next.',
      correct: true,
      points: 0,                      // etiquette is scored via flags, so points here are 0 — see §3/§5
      next: '1.3',
      flags: { EtiquetteOpen: true }
    }
    // …2–4 choices total
  ]
}
```

**Conditional points** (a choice worth different amounts depending on prior behaviour) are written as a tiny function instead of a number — you don't have to write the code, just tell me the rule in plain English (e.g. *"Solving = 20, or 10 if the learner used any colleague hint"*) and I'll express it. If you're comfortable writing it, the PS1 form is:
```js
points: function (s) { return s.flags.AskedForHelp ? 10 : 20; }
```

**Field checklist per decision scene:** `title`, `criterion`, `pathLabel`, `speaker`, `situation`, `choices[]`. Each choice: `text`, `feedback`, `correct`, `points`, `next`, and optional `flags`.

---

## 5. Flags (behaviour switches the scoring/feedback can read)

Flags are booleans set by a choice (or a helper). They let scoring and end-of-scenario feedback react to *behaviour*, not just answers. PS1's set:

| Flag | Set by | Used for |
|---|---|---|
| `EtiquetteOpen` | correct choice on the opening scene | combined etiquette score |
| `EtiquetteClose` | correct choice on the closing scene | combined etiquette score |
| `SawRealCause` | correct choice on the "recreate the issue" scene | (available for feedback) |
| `UsedResource` | opening the **Check the Articles** helper | "did they check their resources" |
| `FoundCorrectArticle` | viewing the correct article inside that helper | "checked *and* found the right one" |
| `AskedForHelp` | using any **Ask a Colleague** hint | caps a later score; triggers a feedback line |

For a **new** scenario you can reuse these names or define new ones — just tell me: the flag name, what choice/action sets it, and what it should affect. Keep the *meaning* stable (a flag is a fact about the learner's process).

**Important design rule carried from PS1 (Addendum B):** "did they check their resources" is set by *opening the resource*, **not** by picking a choice that claims they did. This is deliberate — it separates a learner who genuinely checked from one who guessed the right answer. Preserve this distinction if your scenario has a "check your resources" beat.

---

## 6. The helper buttons (reusable; content is per-scenario)

Three optional on-screen helpers exist. The mechanics are built; you supply the *content* if a scenario uses them.

- **Open CSI** (persistent lookup): a searchable list of article **titles only** (no full text — deliberately, so it doesn't hand over the answer). You provide: the list of plausible CSI article titles for this scenario (include the real relevant ones + a few realistic distractors).
- **Ask a Colleague** (persistent hint panel): a "what do you need a hand with?" list. You provide: 3–5 options, each with the learner-facing *pick* label, the *hint* they get, and a short `topic` tag (logged as `HelpTopic`). Using any hint sets `AskedForHelp`. (In PS1 that caps the "Solving" score — decide if your scenario has an equivalent penalty.)
- **Check the Articles** (appears on one scene via `showCheckArticles: true`): shows the full text of 2+ candidate articles as tabs. You provide: each article's title + full body text, and which one is "correct." Opening it sets `UsedResource`; viewing the correct one sets `FoundCorrectArticle`.

If a scenario doesn't need a helper, just omit it — nothing else changes.

---

## 7. The intro and score slides (author these too)

- **Intro scene** (`intro: true`): a title, a few intro paragraphs (`body: [ ... ]`), and a start-button label (`cta`). See PS1 scene `1.1`.
- **"What good looked like"** slide: the readable path is auto-generated, but you author the **"what works every time"** checklist — the ordered list of what a strong call does (PS1 has 10 items). Provide it as a plain ordered list.
- **Score slide**: the per-criterion table and total are generated from your criteria. You author the **conditional feedback lines** — short notes that show only when a condition is true. PS1 has three:
  - shown when the article score is the partial value (found *an* article, not the right one),
  - shown when the "recreate" score is below full (didn't check the site),
  - shown when `AskedForHelp` is true (solved with assistance).
  For each conditional line, give me: the condition in plain English + the exact line text.

---

## 8. What to hand back, and in what format

**Best (most mechanical bring-back):** the filled `SCENES` object — one annotated object literal per scene per §4, in scene order, plus the helper content (§6) and intro/score content (§7) as clearly-labelled blocks. A single `.md` or `.js` file is perfect.

**Also fine:** a structured storyboard (like the PS1 PDF) where every scene lists — title, criterion, criterion max, pathLabel, speaker, situation, and for each choice: text / feedback / correct? / points / destination / any flag. If every one of those fields is present per choice, I can convert it cleanly. The PS1 storyboard PDF is the format to imitate.

**Avoid:** prose that describes scenes without breaking out the per-choice fields — that forces me to guess scoring and destinations, which is exactly the re-interpretation this doc exists to prevent.

Whatever the form, include for the scenario as a whole: the **criteria list with maxima** (must total 100), the **scene order and branch map** (which choice goes where, and any loop-backs with their caps), and the **flag list** (name → set by → affects).

---

## 9. Non-negotiable rules (the engine assumes these)

1. Criteria maxima **sum to 100**.
2. **Exactly one** `correct: true` choice per decision scene.
3. Every `next` points to a real scene id, or `'return'`, or `'end'`.
4. Any scene with a `next: 'return'` choice **must** have a `retryCap`.
5. `criterion` labels are **consistent** wherever repeated (they key the score table and the telemetry).
6. `pathLabel` is one short word.
7. Choice `text`, `feedback`, `situation` are **learner-facing and verbatim** — write them as they should appear.
8. Punctuation: curly quotes, em dashes, accents are all fine (the file is UTF-8) — write naturally.
9. Keep 2–4 choices per scene.

---

## 10. What you do NOT need to worry about (fixed on the Code side)

- The Google Sheet, the field IDs, the transport, the `no-cors` mechanics — all done and locked.
- The per-click telemetry, the final summary row, the completion signal — automatic.
- Learner identity — the rows are currently anonymous by design; a separate "short-code" step (see `IDENTITY-LINKING-OPTIONS.md`) will link them to a real learner later. **Do not build identity capture into the content.**
- Styling, buttons, modals, layout — the engine renders all of it from your data.

---

## 11. Style + review

Content should follow Wix L&D writing style. In Cowork:
- Use the **Wix eLearning Course Builder** skill to draft scenario content in L&D style.
- Run the draft through the **L&D content reviewer** skill for a copy/clarity pass before hand-back.
- Match the *voice* of the PS1 storyboard: realistic caller lines, consequence feedback that teaches (says *why*, not just right/wrong), and distractors that are plausible, not obviously wrong.

---

## 12. Reference files in the Code project

- `rise-branching-scenario/index.html` — the working engine + PS1 content (your target format, in situ).
- `Practice_Session_1_-_Wix_Editor_Sub-pages_Storyboard__Final_.pdf` (in Downloads) — the source storyboard PS1 was built from; the model to imitate.
- `HANDOFF-storyline-sheets-telemetry.md` — transport background (context only; you don't touch it).
- `IDENTITY-LINKING-OPTIONS.md` — why rows are anonymous for now (context only).

When you bring content back, drop it in this project and say which scenario it is — I'll map it into the engine and we'll test it in Rise → Smart the same way PS1 was validated.
