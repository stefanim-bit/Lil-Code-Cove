# Handoff — Storyline → Google Sheet telemetry (Onboarding Redesign practice sim)

Last updated: 2026-08-10

## Goal

An Articulate Storyline simulation writes per-step learner responses **directly to a Google Sheet** as the Expert works through it, keyed on the learner email that **Smart** (the LMS) passes down via SCORM. Smart continues to handle completion and score through SCORM as normal — the Sheet is a **second, parallel channel**, not a replacement.

Two independent channels by design:
- **SCORM** → completion + score → Smart (untouched, working)
- **fetch() from Storyline JS triggers** → Google Sheet (what we're building)

## Current status

**BLOCKED on one thing:** the Storyline `Execute JavaScript` trigger on the button throws a runtime error instead of executing. Everything on the Google side is proven working, and the click/trigger-order mechanics are proven working — this is now narrowed to a broken/stale publish output, not a CSP block and not a script-content bug.

| Component | Status |
|---|---|
| Google Sheet + headers | ✅ Done |
| Apps Script `doPost` web app | ✅ Code works locally, ❌ **cannot be deployed publicly** (admin policy) |
| Google Form sink | ✅ Working — accepts anonymous POSTs, writes to Sheet |
| Form endpoint + all 12 field IDs | ✅ Verified via browser console, `STATUS: 200` + row landed |
| SCORM learner email handoff | ✅ Working — `cmi.core.student_id` returns the real email |
| Storyline click registering on button | ✅ Confirmed — Adjust Variable trigger fires reliably |
| Storyline `Execute JavaScript` trigger (button) | ❌ **Throws `Script2 is not defined` — this is the blocker** |

**Access update:** Tony has granted access to **SCORM Cloud** as an alternate test host. Not yet used — earmarked specifically to isolate whether the `Script2` error is baked into the published package (reproduces on SCORM Cloud too) or specific to how Smart serves/caches this course (doesn't reproduce there).

## Assets and IDs

**Sheet:** `Onboarding Sim — Raw Results`
- Tab `Responses` — normalized schema, headers created by `setupSheet()`
- Second tab auto-created by the form (`Onboarding Sim — Telemetry Sink` / `Form Responses 1`) — raw submissions land here

**Schema (`COLS` in `Code.gs`):**
```
timestamp | learner_email | learner_name | attempt_id | course | scene | interaction |
question | response | correct | points | time_on_step_sec | notes
```

**Apps Script project:** container-bound to the Sheet (Extensions → Apps Script → `Code.gs`).
Functions present: `setupSheet`, `doPost`, `out`, `buildForm`, and (to be added) `installFormTrigger` / `onFormSubmitToResponses`.
`SHARED_KEY` is on the `SHARED_KEY` const line in `Code.gs` — only used by the `doPost` path, which is currently unused.

**Google Form (the working sink):**
- POST endpoint: `https://docs.google.com/forms/d/e/1FAIpQLSegiZwFV7DN-wwWsqnBbrqzJ5yEK-3lk8Zl182M0fMNFYH5hg/formResponse`
- Public link: `https://docs.google.com/forms/d/e/1FAIpQLSegiZwFV7DN-wwWsqnBbrqzJ5yEK-3lk8Zl182M0fMNFYH5hg/viewform`
- Edit link: `https://docs.google.com/forms/d/1ca-gYlUY1FQlV-di8awpcuxFcInA3Mvv1VUr1VUkyVE/edit`
- Settings: Collect email = Do not collect; response editing off; limit-1 off; **login not required** (confirmed by incognito submit)

**Field map:**
```json
{
  "learner_email":    "entry.1276253364",
  "learner_name":     "entry.2005409239",
  "attempt_id":       "entry.1673953677",
  "course":           "entry.2010105379",
  "scene":            "entry.1283761747",
  "interaction":      "entry.1781563601",
  "question":         "entry.786197073",
  "response":         "entry.2057562952",
  "correct":          "entry.1897805741",
  "points":           "entry.1780599104",
  "time_on_step_sec": "entry.1327709145",
  "notes":            "entry.1963386753"
}
```

## Key decisions and why

**Apps Script web app was abandoned as the transport.** Wix Workspace policy caps web-app access at "Anyone within Wix" — the "Anyone" option is not offered in the deploy dialog. curl against the deployed `/exec` URL returned a Drive "Page Not Found" HTML page. The URL came back in the domain-scoped form (`script.google.com/a/macros/wix.com/s/.../exec`), which is the tell.

**Cookie-based auth inside the LMS iframe does not work.** Tested `credentials: 'include'` against the domain-restricted `/exec` URL from a published SCORM package in Smart. No execution ever appeared in the Apps Script Executions panel. Dead end.

**Google Form `formResponse` is the current transport.** Forms have a separate access policy from Apps Script web apps and this one accepts anonymous posts. Tradeoff: `formResponse` is undocumented — stable for years and widely used, but not a contract Google owes us. `doPost` in `Code.gs` is written and tested as a drop-in replacement if an IT exception ever comes through.

**`mode: 'no-cors'` is mandatory in Storyline** (cross-origin), which means the course **cannot** read the response. The Sheet is the only confirmation a post landed. This is why every debug step below uses on-screen variable readouts rather than console output.

**Content-Type must be `application/x-www-form-urlencoded`** — a CORS-safe simple type. `application/json` triggers a preflight that fails under `no-cors`.

## Open action item

**IT ticket for Apps Script "publish to anyone" is NOT yet filed.** Recommended regardless of whether the form path ships — it's the path to a transport we'd actually want to depend on long-term.

## Test ladder — what passed

1. ✅ `testWrite()` run from the Apps Script editor → `{"ok":true,"written":1}` + row. Proves Sheet ID, tab, permissions.
2. ❌ curl the deployed `/exec` → HTML sign-in page. Killed the web-app path.
3. ✅ Incognito manual submit of the Google Form → row landed. Proves anonymous submission + form→Sheet link.
4. ✅ Browser console `fetch` to `formResponse` from `docs.google.com` (same-origin, `no-cors` dropped so status was readable) → `STATUS: 200` + row. **Proves endpoint and all 12 entry IDs are correct.**
5. ✅ Storyline in Smart: debug text box showed `EMAIL: stefanim@wix.com`. **Proves the SCORM handshake and that Smart puts the real email in `cmi.core.student_id`** (not a GUID, not `student_name`).
6. ❌ Clicking the Storyline button produces no row — in Preview *and* in Smart.
7. ❌ `debugSent` variable set from JS stays blank in Preview *and* in Smart → **the JavaScript is not executing at all.**
8. ✅ Added a non-JS `Adjust variable` trigger (`debugSent = 'CLICK-OK'`) ordered before the JS trigger, same button. Fires reliably in Smart every time. **Proves the click and trigger queue both work** — the failure is isolated to the `Execute JavaScript` action specifically.
9. ✅ Opened the JS trigger's Script editor and read back its exact saved contents twice — confirmed the full send-script (and later a stripped one-line `GetPlayer().SetVar('debugSent','JS-OK');`) is present, syntactically valid, and actually saved. **Rules out the "script never saved" hypothesis.**
10. ❌ Even with the full script *and* the one-line version, `debugSent` never advances past `CLICK-OK` — no `FIRED`, no `JS-OK`, no row, in Smart, on a fresh (non-cached) attempt with the correct file type re-uploaded.
11. ❌ DevTools Console during the click shows the real cause: `bootstrapper.min.js:2 actionator::exeJavaScript - Script2 is not defined`. **This is a Storyline runtime error** — the trigger correctly tries to invoke its compiled script function, but that function's body isn't present in the published output Smart is serving. Not a CSP block (no "Refused to connect" message), not a code bug (content confirmed correct in test 9).
12. ❌ Tried: DevTools "Disable cache" + hard reload. Did not fix it.
13. Fuller console capture in Smart showed `Script1 is not defined` **and** `Script2 is not defined` together, plus `user.js:45 Uncaught SyntaxError: missing ) after argument list`. Since Storyline bundles all trigger scripts into one `user.js`, a syntax error anywhere breaks the whole file — explains both scripts failing together. (Also incidentally confirmed Smart is Moodle-based, per `first.js`/`modal_factory` console lines.)
14. ❌ Deleted the button's `Execute JavaScript` trigger entirely and recreated it from scratch with corrected minimal code (`var player = GetPlayer(); player.SetVar('debugSent', 'FIRED ' + new Date().toLocaleTimeString());`), clean republish, reuploaded to Smart → **still `CLICK-OK`, no `FIRED`.** Rules out corrupted/orphaned script content — a brand-new trigger with verified-clean code still doesn't run.
15. ❌ Uploaded that same freshly-rebuilt package to **SCORM Cloud** (separate host, no shared state with Smart) → **identical result, `CLICK-OK`, no `FIRED`.** Rules out anything Smart-specific (caching, CSP, serving pipeline) — the failure travels with the file.
16. ❌ Removed the `CLICK-OK` Adjust Variable trigger, leaving the `Execute JavaScript` trigger as the *only* trigger on the click event (ruling out trigger-stacking as the cause) → **`debugSent` stayed completely blank.** The JS trigger does not execute on a click event in this file at all, under any configuration tried.

**Conclusion for this session: `Execute JavaScript` on a Timeline-Starts trigger works reliably in this file; `Execute JavaScript` on a User-Clicks trigger does not, on any host, under any trigger configuration, with verified-clean minimal code. This is narrowed as far as it can be without either rebuilding the test slide in a fresh Storyline file or involving Articulate support/known-issues for this Storyline version.**

## Storyline test file (throwaway, not the real sim)

One blank slide. Not the production simulation — built purely to validate the pipeline.

**Variables (all Text):** `learnerEmail`, `learnerName`, `attemptId`, `simResponse`, `debugSent`

**On-slide objects:**
- Text box: `EMAIL: %learnerEmail%` (working — shows real email in Smart)
- Text box: `SENT: %debugSent%` (blank — the symptom)
- Button: `Send test row`

**Trigger 1 — init.** Execute JavaScript · When: Timeline starts · On: this slide. **This one works.**

```javascript
var player = GetPlayer();

function lmsGet(el) {
  try {
    var api = (window.parent && window.parent.API) ||
              (window.parent && window.parent.API_1484_11) ||
              (window.parent && window.parent.parent && window.parent.parent.API) ||
              (window.parent && window.parent.parent && window.parent.parent.API_1484_11) ||
              window.API || window.API_1484_11;
    if (!api) return '';
    return api.LMSGetValue ? api.LMSGetValue(el) : api.GetValue(el);
  } catch (e) { return ''; }
}

var email = lmsGet('cmi.core.student_id') || lmsGet('cmi.learner_id') || '';
var name  = lmsGet('cmi.core.student_name') || lmsGet('cmi.learner_name') || '';

player.SetVar('learnerEmail', email || 'NO-API');
player.SetVar('learnerName', name);
player.SetVar('attemptId', (email || 'anon') + '-' + Date.now());
```

`'NO-API'` fallback is deliberate: distinguishes a failed SCORM handshake from an empty email field.

**Trigger 2 — send.** Execute JavaScript · When: User clicks · On: `Send test row` button. **This is what isn't running.**

```javascript
var player = GetPlayer();
player.SetVar('debugSent', 'FIRED ' + new Date().toLocaleTimeString());

var ENDPOINT = 'https://docs.google.com/forms/d/e/1FAIpQLSegiZwFV7DN-wwWsqnBbrqzJ5yEK-3lk8Zl182M0fMNFYH5hg/formResponse';

var FIELDS = {
  'entry.1276253364': player.GetVar('learnerEmail'),
  'entry.2005409239': player.GetVar('learnerName'),
  'entry.1673953677': player.GetVar('attemptId'),
  'entry.2010105379': 'Onboarding Sim v1 — TEST',
  'entry.1283761747': 'stage-3',
  'entry.1781563601': 'button-click',
  'entry.786197073':  'n/a',
  'entry.2057562952': 'clicked',
  'entry.1897805741': '',
  'entry.1780599104': '',
  'entry.1327709145': '',
  'entry.1963386753': 'form-sink test'
};

var body = [];
for (var k in FIELDS) {
  if (Object.prototype.hasOwnProperty.call(FIELDS, k)) {
    var v = FIELDS[k];
    body.push(k + '=' + encodeURIComponent(v === undefined || v === null ? '' : v));
  }
}

fetch(ENDPOINT, {
  method: 'POST',
  mode: 'no-cors',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
  body: body.join('&')
}).catch(function () { /* never block the learner */ });
```

Note: no `credentials: 'include'` — deliberate. Sending Google cookies from the LMS iframe is exactly what failed in the Apps Script attempt.

## NEXT STEP — pick up here

Every host-side and content-side theory has now been ruled out (see tests 13–16): confirmed identical failure on Smart *and* SCORM Cloud, with a freshly-recreated trigger, verified-clean minimal code, and with trigger-stacking eliminated as a variable. `Execute JavaScript` on a **User Clicks** event does not run in this file, full stop — while the exact same action type on a **Timeline Starts** event works fine. This is now a Storyline authoring/file-level question, not something further console-log chasing will resolve.

Two paths forward, either is reasonable to start with:

1. **Rebuild the test slide from scratch in a brand-new Storyline file.** Don't copy the existing slide — recreate the button, variables, and both triggers manually. If the new file's click-triggered JS works, the original file has some form of corruption specific to it (possibly tied to how many edit cycles this slide's objects have been through) and the real course should be built fresh rather than extending this one.
2. **Check with Articulate support or their known-issues list** for this Storyline version, searching specifically for `Execute JavaScript` not firing on click-type triggers (as distinct from Timeline Starts). If this is a recognized bug, there may be a patch, a workaround (e.g. routing the click through a different trigger type first), or a required publish setting we haven't found.

Once JS-on-click works again (via either path), retest with the one-line `JS-OK` script first, then restore the full send-script — watch for the em dash `—` in `'Onboarding Sim v1 — TEST'` as a plausible copy-paste corruption source, worth swapping for a plain hyphen preemptively. Then retest for `FIRED` + a landed Sheet row. **If** it reaches `FIRED` but still no row: that's a separate, later-stage environment block, not code — open DevTools during the click and look for `Refused to connect to 'https://docs.google.com/...'`, which would be CSP needing `docs.google.com` allowlisted (check on whichever host is being used at that point).

## Remaining work after unblocking

1. Add `installFormTrigger` / `onFormSubmitToResponses` to `Code.gs` and run `installFormTrigger` once — normalizes form-tab rows into the `Responses` tab so the original schema stays the source of truth. Rows will exist in both places; the form tab is a free append-only backup.
2. Duplicate the send trigger onto each real interaction, replacing the hardcoded `'stage-3'` / `'clicked'` strings with `player.GetVar('simScene')`, `player.GetVar('simResponse')`, etc.
3. Drop the `— TEST` suffix from `course`.
4. **Delete both debug text boxes** (`EMAIL:` and `SENT:`) before the real course ships — a learner's email displayed on-slide is not acceptable in production.
5. Re-verify SCORM completion + score still register in Smart after the telemetry code is in.
6. Concurrency check: two Experts clicking simultaneously, confirm no lost rows.

## Gotchas worth carrying forward

- **Test in a hidden test module in Smart**, never the live onboarding course. Keep `course` suffixed `— TEST` so test rows filter out trivially.
- **LMS caches the SCO aggressively.** If a change appears to have no effect, hard-refresh (Cmd+Shift+R) or delete-and-re-upload the package. Prior attempt state can also cause Smart to resume an old attempt instead of starting fresh.
- **Storyline Preview is not a reliable JS test** — some builds restrict `Execute JavaScript` there, so a blank result in Preview is ambiguous. Smart is the authoritative environment.
- **Chrome requires typing `allow pasting`** in DevTools console before it accepts pasted code.
- An **RPA browser extension** (`InPageRpaContentService`) is injecting into Google Docs pages and produces unrelated console noise. Not a factor, but ignore it when reading logs.
- **`actionator::exeJavaScript - ScriptN is not defined` in the console is a Storyline publish bug, not a CSP block or code bug.** It means the trigger fired and tried to call its compiled script function, but that function's body wasn't in the published output. Seen after multiple edit-republish-upload cycles on the same trigger; "Disable cache" + hard reload alone did not fix it. Next things to try: delete-and-recreate the trigger (new script ID), a genuinely clean republish (delete output folder first), or test on SCORM Cloud to see if it's baked into the package vs. Smart-specific.
- Storyline Trigger Wizard has two different "OK/Save" actions that are easy to conflate: the **Script editor window's own Save** (saves the JS code) vs. the outer **Trigger Wizard's OK** (saves the trigger's settings). Also easy to conflate: the **Adjust Variable** action's plain-text **Value** field vs. the **Execute JavaScript** action's actual **Script** code editor — pasting code into the former just stores it as a literal string.

## PII note

Learner work emails are being written to a Sheet outside the LMS — new PII in a new place. Before running on real Experts:
- Restrict the Sheet to the L&D group, not "anyone at Wix"
- Check with whoever owns Smart/HR data whether this needs a heads-up
- Build an aggregate view (pivot on `scene` + `correct`) so routine analysis doesn't require opening the raw email-bearing tab

Testing with a dummy account writing `stefanim@wix.com` needs no sign-off; real-Expert rollout does.

`SHARED_KEY` is a **shared secret, not a private key** — the same value sits on both ends, and the Storyline copy is compiled into the published SCORM package where anyone who opens the course can read it. It stops random internet traffic; it does not protect against someone inside Smart. Don't reuse it anywhere that needs real secrecy. (Currently moot — the `doPost` path is unused.)
