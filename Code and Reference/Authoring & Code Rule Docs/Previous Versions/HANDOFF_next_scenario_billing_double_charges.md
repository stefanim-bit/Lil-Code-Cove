# Handoff — Build the Next Practice Session Scenario

**Next topic: Billing — Double Charges.** This document is written for a fresh chat in this project. It carries over every convention, decision, inclusion, and exclusion from the Session 3 (Billing: Wire Transfer) build so the next scenario matches it. Read it top to bottom before authoring.

**Reference example (open these first):**
- `session3_billing_wire_transfer.html` — the finished, worked example. Copy this file as your starting engine + styles and swap in new content.
- `Session3_Billing_WireTransfer_Branching_Matrix.docx` — the reviewer-facing routing/scoring matrix to reproduce for the new scenario.
- `SCENARIO_AUTHORING_HANDOFF.md` — the original project spec (schema, rules). Still valid; this doc extends it with everything learned during the Session 3 build.

---

## 1. The scenario to build

| Field | Value |
|---|---|
| Product area | Billing: Double charges |
| Example user issue | "I was charged twice for my monthly plan." |
| Issue cause | One charge was the previous month's renewal (i.e. not a true duplicate — it's a renewal + the new period). |
| Starting resources | "Payments for Wix Services (Double Charge on Monthly Plan)" (looks like the correct source) · "Billing Common Scenarios" (good/relevant but not the exact answer — likely a partial/distractor) |

**What makes this scenario different from wire transfer:** the "double charge" is *explainable*, not an error. The correct outcome is to **verify the two charges in the billing history, then educate/reassure the user** about why both appear (renewal timing) — most likely **no refund and no escalation**. This leans heavily on the Tone doc's "handle user confusion without blame" and "ownership" guidance (§9 below).

**Confirm with the user early (judgment calls for this topic):**
1. Is this purely the *explainable renewal* case (educate, no refund), or should a branch cover a *true duplicate* (refund/escalation path)? The stated cause points to explain-only.
2. Which starting resource is the **correct 20-point** source vs the partial/distractor? (User hinted "Payments for Wix Services (Double Charge on Monthly Plan)" is it; "Billing Common Scenarios" is "good but not it.")
3. Exact opening line the user says, and the caller's name.
4. Any Dynamics specifics for double charges (where the two charges show, what fields confirm renewal vs duplicate).

---

## 2. Start-of-chat gate (do this before writing any content)

The project's clarifying-questions gate still applies. Audience, KPI, and length are already configured in this project, but confirm them plus the scenario specifics:
- **Audience / KPI / length** — default is CC Onboarding (Experts + BPO), QCI / Session Supporter scorecard, 15–25 min. Confirm.
- **Rubric / scorecard** — *not yet decided for this topic.* Default is the same 8 behaviours summing to 100 (below). **Check the scorecard together with the user** and flag any **N/A stage** early (in Session 3, wire transfer had "nothing to recreate," which we handled). For double charges, Recreate almost certainly *does* apply (open the billing history to confirm the two dated charges), and Solve is likely *explain + reassure* rather than *fix*. Confirm weights and any N/A before authoring.
- Run the **Bloom's verb audit** on any learning objectives and the **required-elements audit** at the end, per project instructions.

---

## 3. Deliverables (same as Session 3)

1. **Playable HTML** — copy `session3_billing_wire_transfer.html`, keep the `<style>` and `<script id="engine">` blocks untouched, and replace only the `window.SCENARIO = { … }` object (including the embedded `resources`). Save as e.g. `session4_billing_double_charge.html`.
2. **Word routing/scoring matrix** — reproduce the reviewer doc (see §10) from the new SCENARIO.

Deliver both with `present_files`. Note: preview images and scratch `.txt` files created during QA land in the user's folder and can't be deleted programmatically (permission is declined) — tell the user they're safe to remove.

---

## 4. Engine & interaction model (reuse exactly)

The engine renders **any** SCENARIO; never edit it. Its behaviour:
- **Running chat thread.** The call renders as a scrollable conversation; earlier caller lines and the learner's own replies stay on screen. Feedback is withheld until the end (no scores, no correctness colours during play).
- **Spoken vs Action choices.** A choice whose text starts with a quote (`"…"`) renders as the Expert's spoken message in the chat. A choice written as a narration/action (e.g. `Open User Manager…`) is **collected and scored silently** — not shown as a chat bubble. Auto-detected by the leading quote; override with `action:true`/`action:false` on the choice if needed.
- **Caller responses.** Put the caller's reply in `consequence`. Two kinds:
  - **Neutral "Caller responds"** — the caller answering a question the Expert asked (gives email, states country). Default.
  - **Negative "Consequence"** — an in-character reaction to a misstep. Mark these with `negative:true`. (The Word matrix colours negatives differently; the engine shows both as caller lines.)
- **Every question gets an answer.** If a spoken choice asks the user something, give it a `consequence` so the path stays logical (ask → the caller answers).
- **Retry only on believable pushback.** Set `retry:true` + `capIfRetried:<n>` only when a real caller would push back ("that option isn't there…"). No generic "try again."
- **Floating credit.** A good-but-early move can earn partial credit toward another stage via `credits:[{stage, points, verdict}]` (e.g. asking region inside the greeting earns early Clarify credit). Best score per stage wins; skips are recoverable.
- **End screen** auto-builds: total out of 100, per-stage scorecard (green/amber/red dot), "Top strengths" (each done stage's `strength` + the exact response chosen), "Areas for improvement" (each missed/partial stage's `improvement` + response). No pass/fail mark.

---

## 5. The 8-behaviour rubric (default; confirm per stage)

All 8 stages, in order, `max` summing to **100**. `strength`/`improvement` are the end-of-call coaching lines.

| Stage `id` | Name | Max | What "correct" looked like in Session 3 (adapt per topic) |
|---|---|---|---|
| `open` | Opening & closing | 5 | Greet + reassure at the start; recap + offer more help at the close. |
| `dynamics` | Use Dynamics | 10 | Look the account up in User Manager yourself instead of asking the user to describe it. For double charges: open the **billing history** to see the two charges. |
| `familiarize` | Familiarize | 10 | **An impactful contextual-discovery question** that links the issue to the user's goal/use case — *not* an account lookup and *not* a generic "what's your business." |
| `clarify` | Clarify the issue | 15 | Confirm the real problem before proposing anything. **Three-tier rubric:** *Not well* (0, confusion remains) / *Adequately* (partial, some effort, misses a key detail) / *Very well* (full, confirms understanding + all key details). Use one shared partial value. |
| `roadmap` | Roadmapping | 10 | Tell the user the plan for what happens next. Floats — can be credited anywhere, even the greeting. |
| `article` | Article / Copilot | 20 | Go to the official source of truth, not memory. Scored via the **Resources** helper (see §8). |
| `recreate` | Recreate the issue | 10 | Reproduce/verify on your own side before promising. *Adequately* = attempted but not confirmed. For double charges: confirm the two charges and their dates in the billing history. (In Session 3 this became "verify it's unavailable" because wire transfer can't be recreated — confirm this stage's meaning for the new topic.) |
| `solve` | Solve the issue | 20 | Correct fix matched to the confirmed cause, in clear steps. May include a **transfer/escalation** if CSI says so (Session 3 escalated to the Risk Premium team). For double charges the fix is likely **explain the renewal timing + reassure** (no refund). |

**Scoring definitions are per-scenario** — the tiers above are what we settled on for wire transfer. Re-derive them with the user for double charges, then apply the Bloom's verb audit to the `strength`/`improvement` wording.

---

## 6. Authoring rules & conventions (the hard-won ones)

- **2–4 choices per screen.** Exactly one clearly-best, unless the topic genuinely has **multiple right answers** (the Session 3 Article screen had two correct 20-point picks — that's fine and intentional).
- **Don't let length give away the answer.** The correct choice must NOT be the longest option every time. Trim correct answers and beef up distractors so they're comparable. (We ran a check that flagged "correct = longest on all 10 screens" and rebalanced it.)
- **Distractors must be realistic** — plausible things a real Expert might pick (e.g. "clear your cache," "check the status page"), not cartoonishly wrong. Avoid distractors that misstate the product (a wrong option shouldn't imply a feature works when it doesn't).
- **Partial credit does real work.** Reserve `partial` for *partially-correct behaviour*, not just "a plausible wrong answer." Use floating credits to reward good-but-incomplete moves.
- **Neutral prompts.** Never name the behaviour being tested ("How do you respond?", "What's your next step?"). Stage names are hidden during play.
- **Shuffle the correct-answer position** across screens.
- **No em-dashes anywhere** (—). Use commas, periods, or parentheses. This includes the `<title>`, comments, and all displayed strings.
- **Proofreading checklist:** active voice, present tense, contractions ("you're", "isn't", "let's"), spell out numbers one–nine (use numerals for 10+), spell out acronyms on first use with the acronym in parentheses, no punctuation on headers/short bullets, inclusive language, don't over-comma (break sentences up).
- **Empathy traps to avoid** (from project rules): no "No worries" to a frustrated user, no "I understand your frustration" without personalization, no "at least…" / "look on the bright side," no presuming an emotion. Every empathy line should reference something specific the user said.
- **Every technique gets a BEFORE/AFTER** if you're teaching phrasing.

---

## 7. Source-of-truth process (do this before authoring the correct path)

1. **Gather both sides.** The user runs the case through **Copilot in Dynamics** (internal CSI) and pastes what it returns; you index the **public Wix Help Center** for the same issue. Compare.
2. **Reconcile discrepancies out loud.** In Session 3, Copilot said "not supported," the public article added the SEPA-if-saved nuance, and a later CSI article added the mandatory Risk Premium escalation — each changed the correct path. Expect the same here; surface differences and let the user confirm.
3. **Flag transfer / escalation rules.** Ask explicitly whether CSI says to **transfer/escalate** this case type and under what conditions, and whether there are "don't do X before escalating" rules (Session 3: don't link an article to the ticket before escalating — which became a scored trap).
4. **Remove dead ends.** If a link (e.g. a feature-request form) is dead, cut it from the scenario (we removed the FR link when it turned out empty).
5. **Verify every fact with the user before finalizing.** Do not invent CSI content. The tool has the **Wix MCP** (developer/site-building docs — does NOT cover CC billing CSI) and **WebSearch/web_fetch** limited to the official Help Center. Internal CSI comes from the user/Copilot.

---

## 8. The Resources helper (single panel; scores the Article stage)

We merged the old "Open CSI" and "Check the Articles" into one **Resources** panel and **removed "Ask a Colleague"** entirely. Model:
- A list of **links** (title + URL) the Expert can open. The engine collects which are opened and that drives the **Article stage** score.
- **Layered 0 / 10 / 20 scoring:** didn't open anything → **0**; opened only a partial/market-specific/answer-only resource → **10**; opened a resource that gives the complete answer → **20**. (Multiple resources can be worth 20 — Session 3 had two.)
- Include **real relevant articles + believable distractors** (wrong-market or off-topic).
- **Embed it in the SCENARIO** as a `resources` object so it travels with the file. Shape used in Session 3:

```js
resources: {
  items: [
    { title:"…", url:"https://…", points:20, note:"why it's the best source" },
    { title:"…", url:"https://…", points:10, note:"answer-only / partial" },
    { title:"…", url:"https://…", points:0 }   // distractor
  ]
}
```

- Mirror the same 0/10/20 in the playable **Article screen's choices** (memory = 0, partial source = 10, complete source(s) = 20) since that's the in-file proxy until the live panel is wired.
- For double charges, start from the two resources the user gave and expand/reconcile with Copilot.

---

## 9. Tone & phrasing rules (from `Tone Practice for Experts`)

The user's Tone Practice course map governs the voice. Apply it to correct answers; use its "wrong" patterns for distractors.
- **Tone = positive, polite, calm, confident, kind, friendly. Ownership** = willingness to assist, take control, positive positioning (focus on what *can* be done).
- **Transfers/escalations:** use positive language ("Let me connect you with the best person to help", not "I can't help with this"); be transparent about *why*; reassure that the next person has the details. Model line: *"To make sure you get accurate information, I'm going to loop in [team]. I've included everything you shared so they're up to date."*
- **Never expose internal mechanics to the user.** Don't say "I'll attach the article to your ticket" or name internal queues to the caller. Say *"I'll add a note to your case and connect you with a specialized team."* (Internal actions like attaching an article become silent Action choices — and "attaching before escalating" is a scored trap where CSI forbids it.)
- **"Isn't available" not "won't ever."** Avoid definitive negatives.
- **Match, then guide** on terminology: mirror the user's words, then introduce the Wix term, then build context.
- **Handle mistakes without blame:** "It looks like the setting was changed," not "You changed it." Celebrate collaboration; offer proactive prevention. (Very relevant to double charges — the user is confused, not wrong; explain the renewal timing warmly.)
- **No solution / educate:** show empathy tied to specifics, positively position next steps, communicate partnership ("I'll make sure this is noted on your behalf").

---

## 10. Building the Word routing/scoring matrix

Reproduce `Session3_Billing_WireTransfer_Branching_Matrix.docx`. Build method that worked (the docx npm package was blocked by the registry, so use **python-docx**, which is installed):
1. Extract the SCENARIO to JSON: a small node script reads the HTML, `eval`s `window.SCENARIO`, writes `/tmp/scenario.json`.
2. A **python-docx** script builds the doc from that JSON.
3. Verify visually: `soffice --headless --convert-to pdf` → `pdftoppm -jpeg` → copy the JPGs into the user's folder → Read them. (The workspace shell throws an intermittent "e.reduce is not a function" wrapper error — just retry the command.)

**Doc layout (landscape US Letter):**
- Header: title, audience / KPI / length / total, caller bio.
- **Source of truth & key rules** (bullets).
- **Rubric table:** Stage (max) · Max · **Behavior Demonstrated Feedback** (the `strength`) · **Area for Improvement** (the `improvement`).
- **Legend:** ✓ Correct (green) · ◐ Partial (amber) · ✗ Incorrect (red); Routing → Advance / ↩ Retry / ■ End; Caller responds (neutral) vs Consequence (negative); [Spoken] vs [Action]; floating credit note.
- **Routing & scoring matrix**, columns in this order: **Stage it scores · What the learner picks · Caller responds · Points · Routing / Goes to · Max if retried**. Merge the Stage cell vertically per screen. Caller-responds cell labels neutral replies "Caller responds" (green tint) and negatives "Consequence" (orange tint). Routing cell is colour-filled by type. Correct-answer position shuffled; note at the foot that colours are for reviewers only (hidden during play).

---

## 11. Final QA checklist (run before handing back)

**Logic (scriptable):**
- [ ] `max` values sum to **100**.
- [ ] Every stage is **achievable to its max** by some path.
- [ ] Every `choice.goTo` points to a real screen id or `"__end__"`; `start` exists; no orphan/unreachable screens.
- [ ] Every choice has a `verdict` and `points`; `retry` choices have `capIfRetried`.
- [ ] Correct answer is **not** consistently the longest option.
- [ ] Correct-answer position is shuffled. (Intentional ties — multiple-correct screens — are fine; note them.)
- [ ] Read the full flow top to bottom: each caller reply connects logically into the next screen; wrong paths still converge to the close.

**Content:**
- [ ] No em-dashes. Present tense, active voice, contractions. Numbers one–nine spelled out. No comma splices.
- [ ] Prompts are neutral (never name the behaviour).
- [ ] Correct path reflects the reconciled CSI + Help Center truth; transfer/escalation rules honoured; dead links removed.
- [ ] Tone rules applied to correct answers; empathy lines personalized; no internal jargon to the user.
- [ ] Required-elements audit + Checklist Audit section included per project instructions.

**High-stakes verification:** for the final pass, consider a subagent to independently re-read the flow and proofread.

---

## 12. Quick reference — file names

- Engine/example: `session3_billing_wire_transfer.html`
- Matrix example: `Session3_Billing_WireTransfer_Branching_Matrix.docx`
- Original spec: `SCENARIO_AUTHORING_HANDOFF.md`
- Tone source: `Tone Practice for Experts Course Map` (user-provided)
- New scenario output (suggested): `session4_billing_double_charge.html` + `Session4_Billing_DoubleCharge_Branching_Matrix.docx`
