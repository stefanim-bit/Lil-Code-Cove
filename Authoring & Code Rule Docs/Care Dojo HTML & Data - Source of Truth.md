# Care Dojo HTML & Data — Source of Truth

*The single reference for building, scoring, and publishing Wix Customer Care L&D
practice-call scenarios. If any other doc in this repo disagrees with this file,
**this file wins.** Older docs are kept only as history (see Part 10).*

**Last updated:** 2026-09-23
**Canonical engine (copy this when starting a new scenario):**
`Practice Session 1/PS1 Sub-Pages/Current/PS1 Sub-Pages Code Block 2026-09-21/index.html`
(Amber's redesigned chat engine). As of 2026-09-23 every current build shares this same
engine, so any of them is a valid copy source: PS1 Layers, PS1 Sub-Pages, PS3 Double
Charge (Chat and Call), and PS3 Wire Transfer were all synced to it. The redesign
touches the chat screen only, not the scoring model: borderless bubbles with the updated
blue/gray fills, a "confirm your details" step between Meet and the call, first-name-only
display of the learner, restyled pill helper buttons, and end-screen "you didn't reach
this step" notes for stages that were never played. This engine also **auto-generates the
`[Action]` "You ..." note from the choice text and no longer supports the per-choice
`note` or `silent` fields** (see Part 10) — write the choice text so its auto note reads
correctly.

**Where the old docs went:** the superseded authoring docs were moved to
`Authoring & Code Rule Docs/_Archive/`, and the alternate-build / research material
(Storyline + telemetry history, the POC folders, identity-linking research) to
`Authoring & Code Rule Docs/_Reference/`. Nothing was deleted — see Part 10.

---

## How to read this doc

It's written so a **non-technical stakeholder** can read Parts 1–2 and understand
what these are and how they ship, while an **author** works from Parts 3–4, and
whoever maintains the **engine/telemetry** works from Parts 5–7. Each part says up
top who it's for. You never have to read the whole thing to do one job.

| Part | For | What it covers |
|---|---|---|
| 1 | Everyone | What these sims are, in plain language |
| 2 | Everyone / publishers | How a finished scenario gets into a course |
| 3 | Authors | The scenario data schema — every field |
| 4 | Authors | Writing rules, tone, and the source-of-truth process |
| 5 | Engine maintainers | How the sim looks and behaves during play |
| 6 | Engine maintainers | Telemetry to Google Sheets + the "it stopped working" runbook |
| 7 | Reviewers | The routing & scoring matrix artifact |
| 8 | Authors | Final QA checklist |
| 9 | Everyone | Where files live + naming |
| 10 | Reference | Deprecated fields and retired approaches |

---

## Every scenario is different — confirm, don't assume

This doc describes the **shared engine and the standard model**, not a fixed template
every scenario must match. Scenarios legitimately vary:

- Some have **screenshots**, some have **none** at all.
- The **stage order** can differ, and a stage can be **scored across several screens**
  (or skipped where it doesn't apply to the topic).
- A topic may add an **extra stage**, drop one, or **re-weight** the rubric (the
  weights must still total 100).
- Callers, resources, retry moments, and floating credits are all per-scenario.

**Because of that, treat this doc as the default — not a rule that overrides the
actual source material or an existing scenario.** When the content you're building
contradicts this doc, contradicts another scenario, or the source material is unclear,
**stop and ask** rather than guessing. Confirm: the rubric and any N/A or extra stage,
which resource is the correct source, the exact caller lines, and any
escalation/transfer rules. It's always better to ask a clarifying question than to
assume how to proceed.

---

# PART 1 — What these are (plain language)

Wix Customer Care L&D is replacing the old manual practice model (fake cases + live
Session Supporters + manual benchmarking) with **branching call-simulation
scenarios** an Expert plays solo, then scores themselves against. Each scenario
mirrors a real Expert ↔ user interaction and is graded on the same behaviors the
live Session Supporter scorecard uses.

- **Audience:** CC Onboarding — internal Experts and BPO.
- **Each scenario is ONE self-contained HTML file** that runs three phases in a row:
  **Meet the user → Live chat → Complete (scorecard).**
- The live chat looks like the real Wix Communication Panel: gray customer bubbles
  on the left, blue agent bubbles on the right, a call timer, and a red **End**
  button.
- **No score or right/wrong is shown during play.** All feedback waits for the end.

### The file has two parts, on purpose

1. **THE SCENARIO** — a single `window.SCENARIO = { … }` block. It reads like a
   table of stages, screens, and choices. **This is the only part an author touches.**
2. **THE ENGINE** — the machinery that plays *any* scenario. **Never edited per
   scenario.** Improvements to the engine are shared across all scenarios.

Because the engine is generic, authoring a new scenario = copying a current file and
replacing only the `SCENARIO` block.

---

# PART 2 — How a finished scenario ships

*For everyone, especially whoever publishes into a course.*

### Default method — Rise 360 Code Block (this is what we use)

1. Keep the scenario as a folder: `index.html` + its image folders (the user
   portrait folder, e.g. `Samantha M/`, and the `Scenario Screenshots/` folder).
2. **Zip the folder** (HTML + image files together).
3. In a Rise lesson: **Add Block → All Blocks → Code → Add code**, and provide the
   package. Rise runs it as a real `index.html` inside an iframe on the page.
4. The engine tells Rise it's done: when the learner finishes the end screen it
   posts `activity_complete` to the parent page. Rise can read that to mark the
   block/lesson complete.

> The current builds ship as `…Code Block ….zip` next to each scenario folder —
> that zip is the deliverable.

### Optional method — SCORM 1.2 wrapper (experimental)

Some projects need the LMS itself (Wix **Smart**) to record completion/score via
SCORM. For that, the same unmodified scenario is wrapped in a tiny SCORM package
(`scorm12.js` + a launch `index.html` that loads the scenario in an iframe). The
wrapper listens for the scenario's `activity_complete` message and maps it to
`cmi.core.lesson_status = completed`.

- **Status: proven as a test, NOT the default.** Use it only when a specific
  project requires SCORM completion. The example package lives in each PS1 folder as
  `… SCORM (TEST)/`.

### Superseded method — Articulate Storyline (reference only)

An earlier approach built the sim natively in Storyline and sent per-click data to a
Google Sheet. It got **blocked** by a Storyline bug (`Execute JavaScript` on a
*User-Clicks* trigger throws `ScriptN is not defined`; the same action on a
*Timeline-Starts* trigger works). We moved to HTML-in-Rise instead. The Storyline
notes are **kept as a reference build option** but are not the path forward. See
Part 10.

---

# PART 3 — The scenario data schema

*For authors. This is the shape your content must take. Copy a current file and fill
this in.*

```js
window.SCENARIO = {
  title: "Practice Call — <Topic>",           // no em-dashes anywhere; use a hyphen

  user: {
    name: "Samantha",                          // caller's name (per-scenario; PS1 Sub-Pages uses "Sarah")
    image: "Samantha M/Samantha_Meet.png",     // shown on the Meet screen + call header
    completeImage: "Samantha M/Samantha_Close.png", // portrait on the end screen (optional)
    bio: "One line: who they are + why they're calling. You may use *italics* and [name]."
  },

  // The persistent Check Resources panel — scores the `article` stage. See §3.3.
  resources: {
    title: "Check Resources",
    stage: "article",           // which stage this panel scores
    capIfUnchecked: 10,         // article score is capped here if the correct resource is never opened
    note: "Open the resources below. Checking the right ones before you answer is the skill.",
    items: [
      { label:"…", url:"https://…", correct:true },  // a correct source (may be more than one)
      { label:"…", url:"https://…" }                 // a distractor (wrong market / off-topic)
    ]
  },

  // The 8 graded behaviors. Keep all 8, in this order. max values MUST sum to 100.
  stages: [
    { id:"open",        name:"Opening & closing", max:5,  strength:"…", improvement:"…" },
    { id:"dynamics",    name:"Use Dynamics",      max:10, strength:"…", improvement:"…" },
    { id:"familiarize", name:"Familiarize",       max:10, strength:"…", improvement:"…" },
    { id:"clarify",     name:"Clarify the issue", max:15, strength:"…", improvement:"…" },
    { id:"roadmap",     name:"Roadmapping",       max:10, strength:"…", improvement:"…" },
    { id:"article",     name:"Article / Copilot", max:20, strength:"…", improvement:"…" },
    { id:"recreate",    name:"Recreate the issue",max:10, strength:"…", improvement:"…" },
    { id:"solve",       name:"Solve the issue",   max:20, additive:true, strength:"…", improvement:"…" }
  ],

  start: "s_open",              // id of the first screen

  screens: {
    s_open: {
      stage:"open",            // which stage this screen scores
      gate:true,               // true = must finish to advance; false = an open moment
      speaker:"Caller's line, or omit. May contain Expert:/<Name>: labeled parts + \n\n.",
      speakerIf:"resourceOpened",  // OPTIONAL — only play `speaker` if a resource was opened (see §3.5)
      image:{ src:"Scenario Screenshots/Panel.png", caption:"authoring note only — NOT displayed" },
      prompt:"How do you respond?",  // NEUTRAL — never name the behavior being tested
      choices:[
        { id:"A", text:"…the option the learner clicks…",
          verdict:"incorrect", points:0, goTo:"s_dynamics",
          consequence:"Samantha: an in-character reaction, if any." },

        { id:"B", text:"[Action] Look the user up in User Manager.",
          verdict:"correct", points:10, goTo:"s_dynamics",
          note:"You locate the account and site details.",   // overrides the auto "You …" note
          credits:[{ stage:"roadmap", points:4, verdict:"partial" }] }  // OPTIONAL floating credit
      ]
    }
    // …more screens…
  }
};
```

### 3.1 The stages (the rubric — 100 points)

Every scenario is scored on these eight behaviors, mirroring the Session Supporter
scorecard. **The `max` values must total 100.** Keep all eight in order.

| `id` | Name | Max | What a correct choice shows |
|---|---|---|---|
| `open` | Opening & closing | 5 | Greets + reassures at the start; recaps + offers more help at the close |
| `dynamics` | Use Dynamics | 10 | Looks the account up in User Manager instead of asking the user to describe it |
| `familiarize` | Familiarize | 10 | Asks a question that ties the issue to the user's actual goal/use case |
| `clarify` | Clarify the issue | 15 | Confirms the real problem before proposing anything |
| `roadmap` | Roadmapping | 10 | Tells the user the plan for what happens next (**floats — can be credited anywhere**) |
| `article` | Article / Copilot | 20 | Goes to the official source of truth, not memory (scored via Check Resources — §3.3) |
| `recreate` | Recreate the issue | 10 | Reproduces/verifies the issue before promising a fix |
| `solve` | Solve the issue | 20 | Gives the correct fix, matched to the confirmed cause, in clear steps |

- **`strength`** = the coaching line shown at the end when the stage is done well.
- **`improvement`** = shown when the stage is missed/partial. Write both so they read
  naturally after the stage name (e.g. *"**Clarify the issue** — you confirmed the
  real problem before proposing a fix."*).
- Weights above are the default. A topic may re-derive them **with the user**, but
  they must still total 100.

### 3.2 How scoring adds up (best-of vs additive)

- **Default = best score per stage.** If a stage is scored on more than one screen,
  the learner keeps their **highest** result. This is why **skips are recoverable**:
  doing a behavior late/out of order still earns it.
- **`additive:true`** on a stage instead **sums** its screens' points (capped at the
  stage `max`). Used when one behavior legitimately spans two screens — e.g. `solve`
  = `s_solve` (15) + `s_solve2` (5) = 20.
- **`credits:[{stage, points, verdict}]`** on a choice awards *extra* credit toward a
  **different** stage (this is how floating roadmap works — credit it inside the
  greeting, etc.). **`stageOverride:"<id>"`** makes the whole choice score a different
  stage than its screen's default.

### 3.3 The `article` stage — Check Resources (gate + cap model)

This is the current, correct model. **It is NOT points-per-resource** (that was an
older idea — see Part 10).

- The **Check Resources** panel is persistent: the Expert can open it from any screen.
- `resources.items` each carry `correct:true` (a correct source) **or nothing** (a
  distractor). There can be more than one correct source.
- The `article` **screen's own choices** carry the real points (0/10/20).
- Two behaviors enforce "check, don't guess":
  1. **Gate:** a choice phrased `"Reply using '<Article>'"` (or `"Provide a response
     using …"`) is **blocked** unless the learner actually opened *those exact*
     article(s) in Check Resources first. Otherwise a polite notice appears and the
     pick doesn't register.
  2. **Cap:** at the end, if the learner **never opened a `correct:true` resource**
     (and opened it **at least 30 seconds** into the call — opening it too early
     doesn't count), the whole `article` stage is capped at `capIfUnchecked` (10).
- **Author it:** list the real correct article(s) as `correct:true`, plus believable
  distractors (wrong market / off-topic). Set `capIfUnchecked` (10 is standard). Give
  the article screen choices real points that match the resources (memory = 0,
  partial source = 10, complete source(s) = 20).

### 3.4 Choices — the fields

| Field | Meaning |
|---|---|
| `id` | A letter (`"A"`, `"B"`…). Used to disable the option on a retry. |
| `text` | Exact button wording, learner-facing. `[Action] …` marks a tool action (see below). |
| `verdict` | `"correct"` \| `"partial"` \| `"incorrect"`. Drives the end-screen colors. |
| `points` | 0..stage max. |
| `goTo` | Next screen id, or `"__end__"` to finish. |
| `consequence` | OPTIONAL. The in-character follow-up after this pick — see §3.6. |
| `note` | OPTIONAL. For an `[Action]` choice, the exact inline note text (overrides the auto "You …" phrasing). |
| `say` | OPTIONAL. Spoken words to show as the Expert's blue bubble (use instead of `text` when the button label isn't the spoken line). A choice with `say` is NOT treated as an action even if it reads "[Action]". |
| `credits` | OPTIONAL. Extra credit to another stage — see §3.2. |
| `stageOverride` | OPTIONAL. Score a different stage than the screen's. |
| `retry` + `capIfRetried` | OPTIONAL. Re-open the screen once because the caller pushed back; cap the second-try score. Use only where pushback is believable. |
| `image` | OPTIONAL. A screenshot tied to this choice (see §3.7). |
| `showsImage` | OPTIONAL. Reveal the image **immediately on selection**, before the reply. |
| `showsImageAfter` | OPTIONAL. Reveal the image **after** the reply finishes. Action-revealed images auto-open the zoom view. |
| `silent` | OPTIONAL. Render nothing in the chat for this pick (used with `retry` for a quiet re-open). |

**Spoken vs Action, auto-detected:**
- A choice whose text is a spoken line renders as the Expert's **blue bubble**.
- A choice written as a tool action — text starting with `[Action]` — is shown as a
  centered **"You …" note** and scored silently (not a spoken bubble). Give it a
  `note` for exact wording. **Do not** give an `[Action]` choice a `say:` value.

### 3.5 Screens — the fields

| Field | Meaning |
|---|---|
| `stage` | Which stage this screen scores. |
| `gate` | `true` = must finish to advance (most screens). `false` = an open moment where more than one valid path exists. |
| `speaker` | The caller's line. May bundle `Expert:` / `<Name>:` labeled parts separated by blank lines (`\n\n`); the engine splits them into separate bubbles. Omit if the screen opens on the learner's action. |
| `speakerIf` | OPTIONAL gate. `"resourceOpened"` means the `speaker` line only plays if the learner clicked a resource link at some point (e.g. a line like "(You open CSI.)" that only makes sense if they actually looked something up). If not met, the line is skipped entirely — no fallback — in both live play and the end transcript. |
| `prompt` | The question shown on the choices sheet. **Neutral** — never name the behavior. |
| `image` | OPTIONAL screenshot for the screen (see §3.7). |
| `choices` | 2–4 choices. |

### 3.6 `consequence` — what it is

`consequence` is the **optional in-character follow-up to a choice.** It can be any
mix of:
- a **caller reaction** (`"Samantha: I don't have a menu panel like that…"`),
- an **Expert reply** (`"Expert: Ok, I understand."`),
- an **inline action or outcome** the Expert takes/finds, written in parentheses,
  which renders as a green centered note.

Label speakers with `Samantha:` / `Expert:` and separate turns with a blank line
(`\n\n`). A weak choice can carry a short back-and-forth here; a strong choice may
need none. **These reactions are part of the sim, not feedback** — they never reveal
the grade.

> Deprecated: the older `reactions:[ … ]` array is **not supported** — use
> `consequence`. See Part 10.

### 3.7 Screenshots

- Put the file in `Scenario Screenshots/` and reference it as
  `image:{ src:"Scenario Screenshots/File.png" }` on a **screen** or a **choice**.
- **No captions are shown.** Learners read the screenshot and find the info
  themselves. (The engine ignores any `caption:` field — those are dead authoring
  notes and should be cleaned out of scenario data.)
- Every screenshot is **click-to-zoom** (opens a full-screen lightbox).
- **Choice-gated reveal:** a screenshot appears only when the learner picks the
  choice it's tied to — `showsImage` (before the reply) or `showsImageAfter` (after).
  Action-revealed screenshots auto-open the zoom view so the detail is seen
  immediately.

---

# PART 4 — Writing rules, tone, and source-of-truth

*For authors. These are locked conventions, confirmed across every build so far.*

### 4.1 The interaction model (non-negotiable)

1. **Feedback is saved for the END.** No grade, colors, or running score during play.
2. **In-character reactions are NOT feedback.** A weak choice can make the caller
   react in dialogue; that's realism, not a grade.
3. **Don't lead the learner.** Prompts are neutral ("How do you respond?", "What's
   your next step?") — never name the behavior. Stage names are hidden during play.
4. **Mostly gated, some freedom.** Most screens `gate:true`. A few natural moments are
   `gate:false`.
5. **Retry only when the caller naturally prompts it.** No generic "try again." A
   wrong choice re-opens a screen only when a real caller would push back; cap the
   retry with `capIfRetried`.
6. **Skips are recoverable.** Each stage keeps its best score (see §3.2).

### 4.2 Choices & distractors

- **2–4 choices per screen.** Exactly one is best, unless the topic genuinely has
  multiple right answers (that's fine and intentional).
- **Don't let length give away the answer.** The correct choice must not be the
  longest option every time — trim correct answers, beef up distractors.
- **Distractors must be realistic** — plausible things a real Expert might pick, not
  cartoonishly wrong. A wrong option must not misstate the product (don't imply a
  feature works when it doesn't).
- **Verdicts:** reserve `partial` for genuinely partially-correct behavior, not any
  plausible wrong answer. Not every screen needs a partial.
- **Shuffle the correct-answer position** across screens.

### 4.3 Tone (apply to correct answers; use the "wrong" patterns for distractors)

- **Voice:** positive, polite, calm, confident, kind, friendly, with **ownership** —
  focus on what *can* be done.
- **Transfers/escalations:** positive framing ("Let me connect you with the best
  person to help," not "I can't help with this"); reassure the next person has the
  details; **never expose internal mechanics** to the caller (don't name internal
  queues or say "I'll attach the article to your ticket").
- **"Isn't available," not "won't ever."** Avoid definitive negatives.
- **Match, then guide:** mirror the user's words, then introduce the Wix term.
- **Handle mistakes without blame:** "It looks like the setting was changed," not
  "You changed it."
- **Empathy traps to avoid:** "no worries" to a frustrated caller; "I understand your
  frustration" with no personalization; "at least…" / "look on the bright side";
  presuming an emotion the caller hasn't expressed. **Tie every empathy line to
  something specific the caller actually said.**
- **Every technique gets a BEFORE/AFTER** when you're *teaching* phrasing (pair the
  weak default with the improved version).

### 4.4 Copy rules

- **No em-dashes anywhere (—).** Use commas, periods, or parentheses. Applies to the
  title, code comments, and every learner-facing string.
- Active voice, present tense, contractions ("you're", "isn't", "let's").
- Spell out numbers one through nine; numerals for 10+.
- Spell out acronyms on first use with the acronym in parentheses.
- No punctuation on headers or short bullets. Inclusive language. Don't over-comma —
  break long sentences up.

### 4.5 Editor-topic specifics (Wix Editor scenarios only)

Apply during `recreate`/`solve` when the issue involves working on a site:
- **Impersonate the user** to recreate the issue; don't take the report at face value.
- **Don't delete an element** to recreate/fix; clone the site and work on the clone.
- **For advanced issues, rebuild from scratch** on a new site to isolate the cause.
- **Check the Layers panel** — an element can look fine on desktop but be broken on
  mobile (or vice versa).

### 4.6 Source-of-truth process (before authoring the correct path)

1. **Gather both sides:** the user runs the case through **Copilot in Dynamics**
   (internal CSI) and pastes the result; you index the public **Wix Help Center** for
   the same issue.
2. **Reconcile discrepancies out loud** and let the user confirm the correct path.
3. **Flag transfer/escalation rules** explicitly (and any "don't do X before
   escalating" traps).
4. **Remove dead ends** (cut dead links).
5. **Verify every fact with the user before finalizing.** Do not invent CSI content.
   (The Wix MCP covers developer/site-building docs, NOT CC billing CSI; internal CSI
   comes from the user/Copilot.)

---

# PART 5 — How the sim looks and behaves (engine)

*For whoever maintains the engine. This documents what the canonical Care Dojo build
actually does. It supersedes the older `PRACTICE_SCENARIO_SIM_RULES.md`.*

- **Fixed sim window.** `.panel` is a fixed-height flex column (`height:600px`); the
  chat (`.chat`) is `flex:1` and scrolls internally. Choices live in a **slide-up
  bottom "sheet"** with a handle; a `ResizeObserver` keeps the newest messages just
  above it. (This replaces the earlier `40vh` static-chat rule.)
- **Fullscreen** is a **floating icon button** (`fs-fab`, maximize/minimize SVG) over
  the top corner of the sim; it toggles the whole wrapper via the Fullscreen API and
  swaps its icon. (This replaces the earlier text button placed next to Check
  Resources.)
- **Inline notes = dark, timed.** Centered `system` bubbles (an action the Expert
  takes, or a thing they find) render in dark ink (`#242424`), not green. (Green
  `#5BBE7E` is now used only for the "Live" status dot in the call header.) In a
  consequence reveal they appear **2 seconds** apart (`REACT_INLINE_MS`); spoken
  consequence lines (caller **or** Expert) show a **5-second** typing indicator
  (`REACT_TYPING_MS`) before landing. Normal caller typing uses `TAI_MS` (5s) then
  `TAI_FOLLOW_MS` (1.5s) for follow-ons.
- **Screenshots:** captionless, click-to-zoom lightbox; choice-gated via
  `showsImage`/`showsImageAfter`; action-revealed ones auto-open (see §3.7).
- **Speaker gating:** `speakerIf:"resourceOpened"` skips a speaker line unless a
  resource link was clicked — enforced in both live play and the end transcript.
- **End screen:** heading "Complete!" (no "Chat complete" eyebrow), a big score `/
  100`, and an **accordion** with three sections — **Scorecard**, **Top strengths**,
  **Areas for improvement**. The **Finish** button stays locked until **all three
  sections have been opened**; clicking Finish is what fires the completion signal
  (`activity_complete`). A **View conversation transcript** button replays the whole
  call.
- **Completion signal:** the engine posts `{type:'setVar', name:'activity_complete',
  value:'true'}` to the parent on Finish, and a boot-time `{type:'complete'}` so Rise
  knows the block loaded. The Rise Code Block (default) or the SCORM wrapper
  (optional) listens for these.

### Reference colors

| Token | Hex | Used for |
|---|---|---|
| Live green | `#5BBE7E` | The "Live" status dot in the call header only |
| Inline note ink | `#242424` | Centered inline/action notes |
| Orange (brand) | `#DA3B01` | End button |
| Blue (agent) | `#0F62E6` | Expert bubbles / accents |

### Testing note

Scenarios with full-resolution embedded screenshots can exceed a preview tool's
file-size limit. To test logic locally, temporarily swap the long
`data:image/png;base64,…` strings (or heavy image files) for small placeholders — the
engine/logic is identical.

---

# PART 6 — Telemetry to Google Sheets + runbook

*For engine maintainers. This is a second, parallel data channel — it does not
replace SCORM completion.*

Per learner action, the engine POSTs one row to a **Google Form** whose responses
feed a Sheet. A Form's `formResponse` endpoint accepts anonymous, cross-origin POSTs
with no auth or deployment permissions — which is why it works where an Apps Script
Web App was blocked by Wix Workspace policy.

- **Endpoint:** `https://docs.google.com/forms/d/e/1FAIpQLSegiZwFV7DN-wwWsqnBbrqzJ5yEK-3lk8Zl182M0fMNFYH5hg/formResponse`
- **Request:** `POST`, `mode:'no-cors'`,
  `Content-Type: application/x-www-form-urlencoded;charset=UTF-8`. `no-cors` means the
  response is unreadable — **the only confirmation a write landed is a row appearing
  in the Sheet.**
- **Schema (Form fields):** `timestamp | learner_email | learner_name | attempt_id |
  course | scene | interaction | question | response | correct | points |
  time_on_step_sec | notes`. Each maps to a specific `entry.NNN` id in the engine's
  `FIELD_IDS` map — if the Form's questions change, refresh those ids.
- `learner_email` is captured on the Meet screen (HTML/Rise path). In a SCORM/Storyline
  context, `cmi.core.student_id` supplies the real email.

### Runbook — "telemetry stopped populating the Sheet"

**Symptom:** new responses stop appearing. Both hosts can look broken at once because
they share ONE dependency: the same Form → Sheet.

**30-second diagnosis:** submit a test, check the **Form's Responses tab count**:
- **Count climbing but Sheet not updating → it's the Form→Sheet link, never the sim
  code or endpoint.** Stop looking at the HTML.
- **Count NOT climbing → the Form itself isn't recording** (check Form settings/quota).

**Root cause seen (2026-09-23):** a **sort/filter left active on the linked "Form
Responses" tab** silently stops the native append. Repeated unlink/relink then piles
up orphaned "Form Responses N" tabs and compounds it.

**Fix that worked:** unlink, then **link to a BRAND-NEW spreadsheet** (Responses → ⋮
→ link → *Create new spreadsheet*). A fresh sheet gets a fresh sync connection.
Re-selecting the old cluttered sheet tends to re-break. Repoint analysis to the new
sheet.

**Prevention:** **never sort, filter, rename, or restructure the live "Form
Responses" tab** — treat it as append-only. Do all sorting/pivoting on a SEPARATE tab
that pulls from it, e.g.:
```
=SORT(QUERY('Form Responses 1'!A:L, "select * where A is not null", 1), 1, FALSE)
```

**Durable fix (removes this failure mode):** stop depending on the native link. Add a
form-bound Apps Script with an installable **"On form submit"** trigger that
`appendRow`s straight into the normalized Sheet by field id (real-time,
owner-controlled). The `onFormSubmitToResponses` handler is already earmarked in
`Code.gs`.

### PII

Learner work emails written to a Sheet outside the LMS are new PII in a new place.
Before running on real Experts: restrict the Sheet to the L&D group; confirm with
whoever owns Smart/HR data; build an aggregate view so routine analysis doesn't open
the raw email-bearing tab. Testing with a dummy account writing your own email needs
no sign-off; real-Expert rollout does.

---

# PART 7 — The routing & scoring matrix (reviewer artifact)

Before/after writing the JS, lay each scenario out as a table for stakeholder review
(colors applied by hand in Docs/Sheets). Columns:

**Stage it scores · What the learner picks · Caller responds · Points · Routing /
Goes to · Max if retried**

- **Rows group by stage** (merge the Stage cell per screen).
- **Colored columns:** Points by correctness — ✓ Correct `#D9EAD3` · ◐ Partial
  `#FFF2CC` · ✗ Incorrect `#F4CCCC`. Routing by type — → Advance `#1155CC` · ↩ Retry
  `#674EA7` · ⤳ Consequence `#B45F06` · ■ End `#666666`.
- Always keep the ✓ ◐ ✗ / → ↩ ⤳ ■ glyphs so meaning survives B/W and color-blind
  review. Note at the foot that colors are for reviewers only (hidden during play).
- Article/resource names can be **hyperlinked** to their CSI / Help Center URLs — do
  this in a final pass once the article set is locked.

---

# PART 8 — QA checklist (before handing a scenario off)

**Logic:**
- [ ] All 8 stages present; `max` values sum to **100**.
- [ ] Every stage is achievable to its max by some path.
- [ ] Every `choice.goTo` points to a real screen id or `"__end__"`; `start` exists;
      no orphan/unreachable screens.
- [ ] Every choice has a `verdict` and `points`; `retry` choices have `capIfRetried`.
- [ ] Exactly one clearly-best choice per screen (unless the topic genuinely has
      multiple correct answers — note those).
- [ ] Correct answer is **not** consistently the longest option; position is shuffled.

**Article stage:**
- [ ] `resources.items` mark the correct source(s) `correct:true`, plus believable
      distractors; `capIfUnchecked` set (10 standard).
- [ ] Article screen choice points match the resources; "Reply using '…'" choices name
      articles that exist in the panel.

**Content:**
- [ ] No em-dashes. Present tense, active voice, contractions. Numbers one–nine
      spelled out. No comma splices.
- [ ] Prompts are neutral (never name the behavior).
- [ ] Correct path reflects the reconciled CSI + Help Center truth; transfer/escalation
      rules honored; dead links removed.
- [ ] Empathy lines personalized; no internal jargon exposed to the caller.
- [ ] Any technique being taught includes a BEFORE/AFTER.
- [ ] No leftover `caption:` fields, no `reactions:[]`, no `learnerLine` (deprecated —
      Part 10).

---

# PART 9 — Where files live + naming

- **Scenarios** live under `Practice Session <n>/<Feature>/Current/…`, with a
  `Previous Versions/` sibling for old drafts.
- A **scenario folder** = `index.html` + image folders (user portrait folder +
  `Scenario Screenshots/`). The zipped folder is the Rise deliverable.
- **`Authoring & Code Rule Docs/`** holds this doc (the source of truth), the local
  authoring workbook, and the retired references (Part 10).
- **Canonical engine to copy:** `Practice Session 1/PS1 Layers/Current/PS1 Layers
  Code Block 2026-09-16 2/index.html`. PS1 Sub-Pages is an equally current copy source.
- **Caller names are per-scenario** (Samantha in Layers, Sarah in Sub-Pages) — set
  `user.name` and the portrait paths per scenario.

**Authoring workflow (from the "Kirk" overview):** edit in **VS Code**, review the
diff in **Fork**, commit with a short note, push to **GitHub** for backup + history,
roll back anytime.

### Two ways to write the `SCENARIO` block

You never touch the engine — you only produce the `window.SCENARIO = { … }` block.

**A) Write the JS by hand.** Copy the canonical engine file, then edit the block in
the `<script id="scenario">` tag directly, following Part 3. Best when you want full
control or the scenario uses newer fields.

**B) Author in a spreadsheet, then generate the JS.** Good for non-coders and for
building a scenario alongside its reviewer matrix.

1. Copy **`Practice_Session_Scenario_Template.xlsx`** (in `Authoring & Code Rule
   Docs/`) and fill in its tabs — **Meta, Stages, Screens, Choices, Resources** (the
   **Read Me** tab explains each). The tab columns map 1:1 to the Part 3 schema.
2. Download it as `.xlsx`.
3. Run the converter:
   ```bash
   python3 "Authoring & Code Rule Docs/scenario_xlsx_to_js.py" your_scenario.xlsx out.js
   ```
   (Needs Python 3 + `openpyxl`: `pip3 install openpyxl`. Omit `out.js` to print to
   the screen instead.)
4. Paste the generated block into your copied engine file's `<script id="scenario">`
   tag, replacing the old block. Add the image files it references.

The converter emits the **current** schema (`user{}`, `consequence`, the
`correct:true` + `capIfUnchecked` resources model, choice `id`, `additive`, images) and
**warns** if stage `max` values don't sum to 100, a `goTo` points nowhere, or any
em-dash slips in. Screen order in the output follows the row order of the **Screens**
tab. For multi-line `speaker`/`consequence` cells, use a real line break (Alt+Enter)
and label the parts (`Samantha:` / `Expert:`).

> The converter and template are kept in sync with this schema. If you add a brand-new
> engine field, update `scenario_xlsx_to_js.py` (and the template columns) too, or
> author that field by hand.

---

# PART 10 — Deprecated fields & retired approaches (do not use)

Kept so nobody re-introduces them.

### Deprecated schema fields
- **`reactions:[{speaker,text}]`** — replaced by `consequence` (§3.6). The engine does
  not read it.
- **`learnerLine`** — a scripted Expert line on screen load; not implemented in the
  engine. Use a choice `say`/`consequence` instead.
- **`caption`** on an `image` — the engine renders no caption; remove these from data.
- **`resources.items[].points` (points-per-resource)** — replaced by the `correct:true`
  + `capIfUnchecked` gate/cap model (§3.3).
- **`note` on a choice (custom action-note text)** — the current engine auto-generates
  the `[Action]` "You ..." note from the choice text and ignores a custom `note`. Write
  the choice text so its auto note reads correctly. (§3.4 still lists `note` as a field;
  it is inert in the current engine.)
- **`silent:true` on a choice** — the current engine renders every `[Action]` pick as a
  "You ..." note, so there is no silent pick. Older engines skipped rendering for a quiet
  retry re-open.

### Retired docs (superseded by THIS file)
- `Must Review & Consolidate/HANDOFF-content-authoring.md` — old `SCENES`/`flags`
  schema and a 9-criteria rubric. Historical.
- `Must Review & Consolidate/SCENARIO_AUTHORING_HANDOFF.md` — the `reactions:[]` +
  points-per-resource era. Superseded here.
- `Previous Versions/HANDOFF_next_scenario_billing_double_charges.md` — the
  `consequence`-based HTML build handoff; most of its content is folded in above.
- `PRACTICE_SCENARIO_SIM_RULES.md` — the SIM UI rules, now in Part 5 (updated to the
  live engine).
- `Must Review & Consolidate/rise-branching-scenario/` + `PASTE-INTO-RISE.md` — the
  old `SCENES` Rise engine.

### Retired build approach
- **Articulate Storyline + native telemetry** — blocked by the `Execute JavaScript`
  on-click bug (`ScriptN is not defined`). Kept as a reference option only. Details:
  `Data/HANDOFF-storyline-sheets-telemetry.md`, `Previous Versions/
  POC-2-slide-branch-telemetry.md`, and the `First POCs For Reference/poc-*` folders.
- **Identity linking** (short-code / timestamp stitching) — parked; see
  `Research/IDENTITY-LINKING-OPTIONS …md`.
