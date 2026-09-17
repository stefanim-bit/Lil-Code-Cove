# Rise version of the branch-telemetry POC

Same goal as the Storyline version — prove Scene 1.2's four choices can be logged to the Sheet for path-frequency analysis — but built for Rise since Storyline was freezing. See [`../POC-2-slide-branch-telemetry.md`](../POC-2-slide-branch-telemetry.md) for the Storyline version and full background.

**Why this is actually simpler in Rise:** Storyline needed the whole Adjust-Variable-then-Timeline-Starts workaround because its `Execute JavaScript`-on-click trigger goes through a proprietary compiler that was throwing `Script2 is not defined`. Rise has no such compiler — a block's JavaScript is just a normal script running in the browser, so a plain `button.addEventListener('click', ...)` works directly. No variables, no second slide, no staging step — [`index.html`](index.html) is the entire Scene 1.2 interaction (Sam's line + all 4 real choices + the send logic) in one self-contained block.

**What's genuinely untested here (the tradeoff):** whether Rise's block sandbox permits reaching the SCORM API in the parent frame the way Storyline's did. `findAPI()` in the code is defensive about this — wrapped in try/catch so a stricter sandbox degrades to `learner_email = NO-API` instead of crashing the whole block — but which outcome actually happens in Smart is still unverified until you test it there.

## Step 1 — check which block type you have

Open a Rise lesson → **Add Block** → **All Blocks**. Look for a category called **Code**.

- **If you see "Code":** use that one — Articulate's docs describe it as running your HTML/JS more directly (still in an iframe, but not the older embed-sandbox path). Click **Add code**, paste the entire contents of `index.html`, save.
- **If you only see "Embed", no "Code":** your account doesn't have the newer feature (it needs a specific Articulate 360 license tier). Use **Embed** → look for an option like "Embed code" or "Custom HTML" (as opposed to a URL/oEmbed field) → paste the same `index.html` contents there. This path is less certain — the Embed block's iframe may need script permissions explicitly enabled, which isn't something you control from the paste-in dialog. If the block renders blank or the buttons don't respond, that's the likely cause — worth knowing going in rather than treating it as a mystery.

## Step 2 — test in stages, same discipline as the Storyline debugging

1. **Preview inside Rise first.** Confirm the dialogue text and four buttons render, and clicking one updates the on-screen log to `Clicked: "..."` → `fetch() resolved`. This alone doesn't confirm the SCORM email lookup (Preview may not have a real LMS API to find), but it proves the block runs JS at all and that clicks/fetch work.
2. **Check the Sheet** for a row with `course: "...Rise POC"` and the matching `response` text.
3. **Only then publish and upload to Smart or SCORM Cloud** to test the SCORM email piece — expect the log to show `Found SCORM ... API` → `learner_email = <real email>` instead of `NO-API`, or `Frame access blocked...` if the sandbox is stricter than Storyline's. Either outcome tells you something concrete about the platform, which is the point of testing it in stages rather than building the full 10-scene course into this block first.

## What this does and doesn't prove

Proves: real Scene 1.2 content, real choice text, landing in the Sheet, from inside a Rise block, with no dependency on Storyline working at all.

Doesn't prove: whether the SCORM email handoff survives Rise's specific sandboxing (step 2.3 above is the open question), and doesn't replicate Rise's own native branching "Scenario" block — this deliberately bypasses that in favor of one plain custom block, since Rise's built-in Scenario block has no known way to hook custom telemetry into individual choices.
