# Practice Session — Scenario Authoring Handoff

*Last updated: 2026-08-30 — reflects conventions confirmed across all scenario builds so far (Sessions 1, 3, 4), not just the original spec. Anything specific to one scenario (its correct/distractor articles, exact caller lines, market rules) belongs with that scenario's own matrix and fact-check doc, not here.*

**Purpose of this file:** context for building the *content* of Onboarding Practice Session scenarios in a separate Cowork project. Write the scenario content to the schema in §6, following the rules in §4–§5, and return it in the format in §9. It drops straight into the interactive template in the Code project (`practice_scenario_template.html`).

---

## 1. What this project is

Wix Customer Care L&D is replacing the old manual practice model (fake cases + live Session Supporters + manual benchmarking) with **branching call-simulation scenarios** an Expert plays solo for self-evaluation. Each scenario mirrors a real Expert↔user interaction and is scored against the **live Session Supporter scorecard**.

- **Audience:** CC Onboarding — internal Experts + BPO.
- **Build target:** self-contained **HTML/JavaScript inside an Articulate Rise "Code Block."** No Storyline, no external libraries.
- **Launch target:** Sep 13, 2026.
- **Session 1 (Wix Editor: sub-pages)** is the reference scenario. Full session list lives on the Monday board (not needed to author content).

## 2. How the build works (so your content fits it)

The HTML file has **two parts**:

1. **THE SCENARIO** — a single `window.SCENARIO = { … }` JavaScript object. **This is the only part authors touch.** It reads like structured data: stages, screens, choices.
2. **THE ENGINE** — reusable machinery that plays any scenario. Never edit it.

**Your deliverable is the filled-in `SCENARIO` object (§9).** You do not write HTML, CSS, or engine logic.

## 3. The rubric — the 8 graded behaviors (100 pts)

Every scenario is scored on these eight behaviors. They mirror the Session Supporter scorecard and define the natural order of a good interaction. **Total must sum to 100.**

| Stage `id` | Name | Max pts | What a correct choice demonstrates |
|---|---|---|---|
| `open` | Opening & closing etiquette | 5 | Greets, reassures, and closes with a recap + offer of more help |
| `dynamics` | Use Dynamics (features & steps) | 10 | Uses Dynamics/User Manager to see the account, knows where to click |
| `familiarize` | Familiarize | 10 | Gets oriented to the user's site/setup before troubleshooting |
| `clarify` | Clarify the issue | 15 | Confirms the real problem before proposing anything |
| `roadmap` | Roadmapping | 10 | Tells the user the plan for what happens next (**floats — see §5**) |
| `article` | Locate article / use Copilot | 20 | Goes to the official CSI source of truth, not memory or forums |
| `recreate` | Recreate the issue | 10 | Reproduces the issue to confirm the cause before promising a fix |
| `solve` | Solve the issue | 20 | Gives a correct fix, matched to the confirmed cause, in clear steps |

## 4. The interaction model — non-negotiable rules

1. **Feedback is saved for the END.** During play the learner sees NO grade, NO correctness colors, NO running score. Choosing an answer just advances the interaction. All feedback lives on the final review screen (§7).
2. **In-character reactions are NOT feedback.** A weak choice may make the caller react in dialogue ("I don't have a menu panel like that…"), sometimes as a short back-and-forth rather than one line. That's part of the sim, not a grade. Use these to make the moment feel real.
3. **Don't lead the learner.** Prompts must be neutral ("How do you respond?", "What's your next step?") — never name the behavior being tested ("Before troubleshooting, how do you get oriented?" ❌). Stage names are hidden during play.
4. **Mostly gated, some freedom.** Most screens are `gate:true` (must finish to advance). A few natural moments are `gate:false` — an OPEN moment where more than one valid path exists.
5. **Retry only when the caller naturally prompts it.** There is no "try again" button. A wrong choice can re-open a screen ONLY when a real caller would push back ("Wait, that's not what I see…"). Everything else has a consequence and moves on.
6. **Skips are recoverable.** Each stage keeps its own best score. If a learner performs a behavior late/out of order, they still earn it.

## 5. Authoring rules & tone

- **Choices per screen:** 2–4. Exactly one is the best (correct) unless the topic genuinely has multiple right answers — that's fine and intentional; others are incorrect or partial.
- **Don't let length give away the answer.** The correct choice must not be the longest option on every screen. Trim correct answers and beef up distractors so they're comparable.
- **Distractors must be realistic** — plausible things a real Expert might pick, not cartoonishly wrong. Avoid distractors that misstate the product (a wrong option shouldn't imply a feature works when it doesn't).
- **Verdicts:** `correct` (full points), `partial` (right instinct, wrong execution — partial points), `incorrect` (0). Reserve `partial` for genuinely partially-correct behavior, not just any plausible wrong answer. Not every screen needs a partial.
- **Reactions:** give a choice a short in-character reaction where it's realistic, using `reactions` (see §6). Most choices need zero or one line (usually the caller). A few need a short back-and-forth (caller reacts, Expert replies, caller reacts again) — don't force this, use it only when the exchange genuinely needs more than one line to land.
- **Roadmap floats:** roadmapping can be credited **anywhere** it naturally happens — even in the greeting. Attach it as extra credit on any choice (see `credits` in §6). Don't force a dedicated roadmap screen if it reads better woven in.
- **Retry realism:** only set `retry` on a wrong choice when the caller pushing back is believable. Cap the retry score (`capIfRetried`) below full marks.
- **Letter shuffle:** don't let the correct answer sit in the same position every screen.
- **Caller voice:** callers sound like real, mildly frustrated users. Expert options are plain, realistic phone/chat lines — not textbook. Keep wording tight.
- **Source of truth:** the correct path should reflect the real Wix support process and the relevant CSI/Help Center article for the scenario's issue.
- **Credit checking, not claiming (carried from PS1):** for the `article` and `recreate` stages, credit the *act of genuinely checking the source/recreating the issue* — not a choice that merely *claims* the learner did. Distinguish a learner who really checked from one who guessed the right answer. Keep this distinction wherever a scenario has a "check your resources" beat.
- **No em-dashes anywhere (—).** Use commas, periods, or parentheses instead. This applies to the scenario title, code comments, and every learner-facing string.
- **Proofreading checklist (learner-facing text):** active voice, present tense, contractions ("you're", "isn't", "let's"), spell out numbers one through nine (numerals for 10+), spell out acronyms on first use with the acronym in parentheses, no punctuation on headers or short bullets, inclusive language, and don't over-comma — break a long sentence up instead.
- **Expert tone (for correct-answer language):** positive, polite, calm, confident, kind, friendly, with ownership — focus on what *can* be done. For transfers/escalations, use positive framing ("Let me connect you with the best person to help," not "I can't help with this") and never expose internal mechanics to the caller (don't name internal queues or describe internal actions like attaching a ticket note). Prefer "isn't available" over "won't ever." Match the caller's words, then introduce the Wix term. Handle mistakes without blame ("It looks like the setting was changed," not "You changed it.").
- **Empathy traps to avoid** in any caller-facing empathy line: "no worries" to a frustrated caller, "I understand your frustration" without personalization, "at least…" / "look on the bright side," and presuming an emotion the caller hasn't expressed. Tie every empathy line to something specific the caller actually said.
- **Every technique gets a BEFORE/AFTER.** If a screen is teaching a phrasing technique (not just testing it), pair a weak/common default with the improved version applying the technique.

## 5b. Category-specific notes: Editor issues

The rules below are specific to **Wix Editor scenarios** (not universal to every topic). Apply them whenever the `recreate` or `solve` stage of an Editor scenario involves working on a site:

- **Impersonate the user to recreate the issue.** Don't take the reported behavior at face value; log in as the user and reproduce it yourself before proposing a fix.
- **Don't delete an element to recreate or solve the problem.** If recreating or fixing the issue would require deleting an element, stop. Clone the site instead and work on the clone. Only the user can save and publish changes to their own site.
- **For advanced or complex issues, rebuild from scratch.** If the issue can't be pinned down on the user's site, recreate it from scratch on a new site to isolate the cause.
- **Check the Layers panel.** An element can look fine on desktop but be broken on mobile (or vice versa). The Layers panel helps catch this when a straightforward visual check doesn't.

## 6. The data schema (fill this)

```js
window.SCENARIO = {
  title: "Practice Call — <Topic>",
  userBio: "Meet <Name> — <one-line who they are + why they're calling>.",
  // NO pass/fail is shown to the learner. The review screen shows the per-stage
  // table + total out of 100 only — no pass mark, no pass/fail verdict. (Do not add passMark.)

  // --- The 8 stages. Keep all 8, in this order. strength/improvement are the END feedback. ---
  stages: [
    { id:"open",        name:"Opening & closing", max:5,
      strength:"<shown at end if done well>",
      improvement:"<shown at end if missed/partial>" },
    { id:"dynamics",    name:"Use Dynamics",      max:10, strength:"…", improvement:"…" },
    { id:"familiarize", name:"Familiarize",       max:10, strength:"…", improvement:"…" },
    { id:"clarify",     name:"Clarify the issue", max:15, strength:"…", improvement:"…" },
    { id:"roadmap",     name:"Roadmapping",       max:10, strength:"…", improvement:"…" },
    { id:"article",     name:"Article / Copilot", max:20, strength:"…", improvement:"…" },
    { id:"recreate",    name:"Recreate the issue",max:10, strength:"…", improvement:"…" },
    { id:"solve",       name:"Solve the issue",   max:20, strength:"…", improvement:"…" }
  ],

  start: "s_open",                    // id of the first screen

  screens: {
    s_open: {
      stage: "open",                  // which stage this screen scores
      gate: true,                     // true = must finish; false = open moment
      learnerLine: "<optional — a scripted Expert line the engine plays automatically, before speaker>",
      speaker: "<caller's line, or omit>",
      prompt: "How do you respond?",  // NEUTRAL — never name the behavior
      choices: [
        { text:"<option the learner clicks>",
          verdict:"incorrect",        // "correct" | "partial" | "incorrect"
          points:0,
          goTo:"s_dynamics",          // next screen id, or "__end__"
          reactions:[{ speaker:"caller", text:"<optional in-character reaction>" }] },

        { text:"<best option>",
          verdict:"correct", points:5, goTo:"s_dynamics",
          credits:[{ stage:"roadmap", points:4, verdict:"partial" }] }  // optional floating credit
      ]
    }
    // …more screens…
  }
};
```

**Field reference**

- **Stage** = `id`, `name`, `max`, `strength`, `improvement`.
- **Screen** = `stage`, `gate`, `learnerLine` (optional), `speaker` (optional), `prompt` (neutral), `choices[]`.
  - `learnerLine` — a line the *Expert* (the learner's own character) says automatically when the screen loads, before the caller's `speaker` line. It's scripted, not a choice — use it to bridge from the previous answer (e.g. acknowledging what the caller just said) so the next caller line doesn't land out of nowhere. Omit it when the caller's line stands fine on its own.
- **Choice** = `text`, `verdict`, `points`, `goTo`.
  - `credits:[{stage,points,verdict}]` — optional extra credit toward another stage (floating roadmap).
  - `retry:true` + `capIfRetried:<n>` — optional; re-opens the screen because the caller pushed back, cap the second-try score.
  - `reactions:[{speaker,text}]` — optional, zero or more chained lines that play after this choice, in order (e.g. caller reacts, Expert replies, caller reacts again). `speaker` is `"caller"` or `"expert"`. Most choices have zero or one; only add more turns when a single line genuinely can't carry the exchange. Replaces the old single `consequence:"…"` string — if you're bringing content forward from an older draft, wrap it as `reactions:[{ speaker:"caller", text:"…" }]`.
  - `stageOverride:"<id>"` — optional; credit a different stage than the screen's default.
  - `goTo:"__end__"` — sends the learner to the final review screen.

## 7. What the learner sees at the END (author the copy for this)

The engine builds the review screen automatically, but **you write the words**:

- **Scorecard** — per-stage points (auto).
- **Top Strengths** — for each stage done well, its `strength` line + the exact response the learner chose (auto-cited).
- **Areas for Improvement** — for each stage missed/partial, its `improvement` line + the exact response chosen.
- **View conversation transcript** button — full replay (auto).

So `strength` and `improvement` per stage are the coaching voice. Examples:
- `strength`: "you confirmed the real problem before proposing a fix."
- `improvement`: "clarify and confirm the issue before jumping to solutions or an article search."

Write them so they read naturally after the stage name: *"**Clarify the issue** — you confirmed the real problem before proposing a fix."*

**Conditional feedback lines (optional, carried from PS1).** Beyond the per-stage `strength`/`improvement`, you may supply short review-screen notes that appear only when a specific condition is true — e.g. *shown when the article score is partial* ("you found an article, but not the right one"), or *shown when the recreate stage is below full* ("you didn't reproduce the issue before promising a fix"). For each such line, give: the condition in plain English + the exact line text. If the engine doesn't yet support these, they still document the intended coaching and can be folded into the relevant `improvement` line.

## 7b. The Resources helper (single panel — author the per-scenario content)

Earlier drafts described three separate on-screen helpers (Open CSI, Ask a Colleague, Check the Articles). Those have been merged into **one Resources panel**; Ask a Colleague has been removed entirely. The panel is **persistent for the whole call** — the Expert can open it from any screen, not just a dedicated Article screen — and it's the panel, not a screen choice, that scores the `article` stage. The engine renders the panel and handles the telemetry/flag wiring; you supply only the per-scenario content:

- A list of **links** (title + URL) the Expert can open. The engine tracks which are opened, and that drives the `article` stage's score.
- **Layered 0 / 10 / 20 scoring:** didn't open anything → 0; opened only a partial/market-specific/answer-only resource → 10; opened a resource that gives the complete answer → 20. (More than one resource can be worth 20 if there's more than one valid source.)
- Include real relevant articles plus believable distractors (wrong market or off-topic).
- **Embed it in the SCENARIO** as a `resources` object so it travels with the file:

```js
resources: {
  items: [
    { title:"…", url:"https://…", points:20, note:"why it's the best source" },
    { title:"…", url:"https://…", points:10, note:"answer-only / partial" },
    { title:"…", url:"https://…", points:0 }   // distractor
  ]
}
```

- The "credit checking, not claiming" rule (§5) applies here: score the *act of opening the resource*, not a choice that merely claims the learner checked.
- **A scripted "which article do you open" screen can still exist for story flow** (it's a natural beat in the call), but its choices carry `points:0` on every option — flavor/narration only. The `article` stage's real points come only from `resources.items[].points`, via the panel. Don't double-score the same behavior in both places.

## 8. Planning aid — the routing & scoring matrix

Before writing the JS, it helps to lay each scenario out as a table (this is the reviewer-facing artifact; colors are applied by hand in Docs/Sheets). Columns:

**Stage it scores · What happens · What the learner picks · Points · Goes to · Max if retried**

- **Rows group by stage** (no screen or option-letter column needed).
- **Two colored columns:**
  - **Points** — fill by correctness: ✓ Correct `#D9EAD3` · ◐ Partial `#FFF2CC` · ✗ Incorrect `#F4CCCC`.
  - **What happens** — fill by routing: → Advance `#1155CC` · ↩ Retry `#674EA7` · ⤳ Consequence `#B45F06` · ■ End `#666666`.
- Always keep the ✓ ◐ ✗ / → ↩ ⤳ ■ glyphs so meaning survives B/W and color-blind review.

## 9. Deliverable format (what to send back to Code)

**Primary path — the Google Sheet.** Scenarios are authored in a live Google Sheet, one copy per scenario, duplicated from the same Meta / Stages / Screens / Choices / Resources tab structure as the schema in §6 (Screens also has the optional `learnerLine` column; Choices has the `reactions` columns from §6, in place of a single consequence). Two are in progress now: **Sub Pages Scenario** and **PS1 Wix Editor: Layers Scenario** (both in the Practice Session Sims Drive folder). To start a new scenario, duplicate one of these, clear the example rows, and fill it in per §4–§5b. Download the finished Sheet as `.xlsx` and run it through `scenario_xlsx_to_js.py <workbook.xlsx> [output.js]` (see below) to get the pasteable `window.SCENARIO` block.

**Equivalent path — writing the JS directly.** If it's easier, skip the Sheet and write the completed `window.SCENARIO = { … }` object by hand (the §6 schema, fully filled). One scenario per file/code block, named by session + topic (e.g., `Session 3 — Billing: Wire Transfers`).

Optionally also include the §8 matrix table for stakeholder review.

**Fallback path — the local authoring workbook.** `Practice_Session_Scenario_Template.xlsx` (kept in sync with the Sheet's schema) works the same way if you don't have Drive access: fill it in, then run `scenario_xlsx_to_js.py <workbook.xlsx> [output.js]` to generate the same `window.SCENARIO` block. The Sheet is the source of truth going forward; treat this file as a backup and keep it in sync when the Sheet's schema changes.

## 10. QA checklist (before handing back)

- [ ] All 8 stages present; `max` values sum to **100**.
- [ ] Every `choice.goTo` points to a real screen id or `"__end__"`.
- [ ] `start` and the closing screen (`goTo:"__end__"`) both exist; no orphan/dead-end screens.
- [ ] Exactly one clearly-best choice per decision screen, unless the topic genuinely has multiple right answers.
- [ ] Prompts are neutral (never name the behavior).
- [ ] `retry` used only where the caller's pushback is believable; `capIfRetried` set.
- [ ] Correct-answer position is shuffled across screens.
- [ ] Every stage has a `strength` and `improvement` line.
- [ ] Correct path reflects the real Wix process + the relevant CSI/Help Center article.
- [ ] No em-dashes; present tense, active voice, contractions used; numbers one through nine spelled out (numerals for 10+); acronyms spelled out on first use.
- [ ] Any caller-facing empathy line is personalized (ties to something the caller actually said) and avoids the empathy traps in §5.
- [ ] Any screen teaching a phrasing technique includes a BEFORE/AFTER pair.
- [ ] Every `reactions` entry has both `speaker` (`caller` or `expert`) and `text`; most choices have zero or one, not a forced back-and-forth.
- [ ] If there's a scripted Article screen, every one of its choices is `points:0` — the real `article` score comes only from `resources.items[].points`.

---

*Reference implementation: `practice_scenario_template.html` (Session 1 — Wix Editor: sub-pages) is a complete worked example of everything above. Open it, play it, and read the `SCENARIO` block to see the schema in use.*
