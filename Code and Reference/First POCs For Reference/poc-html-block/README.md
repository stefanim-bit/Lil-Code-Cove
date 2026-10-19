# Web Object POC — bypassing Storyline's `Execute JavaScript` compiler

See [`../HANDOFF-storyline-sheets-telemetry.md`](../HANDOFF-storyline-sheets-telemetry.md) for full background. Short version: `Execute JavaScript` on a **User Clicks** trigger throws `ScriptN is not defined` in the published output, on every host tried, with verified-clean code. That error comes from Storyline's own trigger-compiler ("actionator") — it fires the trigger but the compiled function body isn't in the published `user.js`.

This POC sidesteps that compiler entirely. Instead of a Storyline trigger, [`index.html`](index.html) is a **plain static HTML page** loaded into a **Web Object** (a real `<iframe>` Storyline drops onto the slide, pointing at your own file). Browser-native script tag, no proprietary bundling step — so if this button reliably fires where the native trigger didn't, that isolates the bug to Storyline's compiler, not to fetch/CSP/SCORM-in-iframe mechanics (all of which were already independently proven fine in tests 1–10 of the handoff).

Same transport as the handoff: SCORM email lookup by walking up parent frames, then `fetch()` with `mode: 'no-cors'` to the Google Form `formResponse` endpoint (urlencoded body, the 12 `entry.*` field IDs). Nothing new to re-verify on the Google side.

## Test 1 — standalone in a browser (no LMS, no Storyline)

Just open `index.html` directly. Expect:
- Log shows `No SCORM API found` → `learner_email = NO-API` (correct outside an LMS)
- Clicking "Send test row" logs a resolved `fetch()` and a new row lands in the Sheet (`course = Onboarding Sim v1 - POC-webobject`)

This only proves the fetch/Form path works from a vanilla page — expected, since that path was already proven in handoff test 4. The real test is #2.

## Test 2 — as a Storyline Web Object (the actual point of this POC)

1. In Storyline, on a slide: **Insert → Web Object**.
2. Choose **"Other files or Web Sites"** → browse to this `index.html` on disk. Storyline copies the file (and folder) into the published output and embeds it as an iframe.
3. Recommended Web Object properties: **Show Web Object border** off, **Resize Browser to fit Web Object** on, size it to fill enough of the slide to see the log panel.
4. Publish, upload to Smart (or SCORM Cloud — either works, per handoff test 15), open the module.
5. Expect: log shows `Searching for SCORM API...` → `Found SCORM 1.2 API` (Smart is Moodle-based, LMSGetValue-style, per handoff §13) → `learner_email = <your real email>`.
6. Click the button. Expect a new row in the Sheet with `scene = poc-webobject`.

If step 6 lands a row: the bug is isolated to Storyline's native `Execute JavaScript`-on-click trigger specifically, and the Web Object is a viable permanent workaround (build the real sim's telemetry calls as Web Object buttons instead of triggers) — not just a POC.

If step 6 does **not** land a row but step 5 found the SCORM API fine: open DevTools during the click and check for `Refused to connect to 'https://docs.google.com/...'` — that would be a CSP block specific to iframe-within-iframe-within-Smart, a genuinely new failure mode distinct from anything ruled out so far.

## Test 3 — as a Rise "Embed" block

Rise's Embed block also runs raw HTML/JS in an iframe on the page, so the same file works with no changes. Paste the full contents of `index.html` into the Embed block's HTML source (Rise wants the raw markup, not a file upload). Same SCORM-API-search logic applies — Rise-in-an-LMS nests exactly like Storyline-in-an-LMS, cmi variables live in the same ancestor-frame chain.

## What this does NOT change

- `SHARED_KEY` / `doPost` — still unused, still the long-term path pending the IT ticket for "publish to anyone."
- PII posture — same as the handoff: fine for `stefanim@wix.com` test rows, needs sign-off before real Experts. This POC's on-screen log prints the email for debugging the same way the original test slide's debug text box did — strip it (or route console-only) before anything resembling production.
- The 12-field schema, endpoint, and content-type constraints — unchanged, copy-pasted from the proven-working values in the handoff.
