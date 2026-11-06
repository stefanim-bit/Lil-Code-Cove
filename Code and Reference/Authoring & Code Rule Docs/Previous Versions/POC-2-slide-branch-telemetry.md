# POC — real branch point → Google Sheet (path-frequency only)

Confirms the goal before building: **can we send interaction-level data (which choice a learner picked, at which decision point) to a Google Sheet, so path frequency across a cohort can be analyzed later — without touching Storyline's broken `Execute JavaScript`-on-click trigger.**

Explicitly out of scope for this pass (per decision, see [`HANDOFF-storyline-sheets-telemetry.md`](HANDOFF-storyline-sheets-telemetry.md) for the full debugging history):
- Correctness/scoring (`correct` field stays blank — this POC only proves *which button*, not *was it right*)
- Time-on-task (no start-timestamp variable, `time_on_step_sec` stays blank)
- Retry/back-navigation dedup, concurrency — later work

**Mechanism:** no Web Object, no click-triggered JS at all. Every choice button uses a plain **Adjust Variable** trigger (proven reliable — handoff test 8) to stage the choice, then **Jump to Slide**. The next slide's **Timeline Starts** `Execute JavaScript` trigger (proven reliable — this is the one trigger type that has worked in every test so far) reads the staged variables and does the `fetch()`. Native Storyline authoring the whole way; nothing routes through the click-JS path that's been throwing `ScriptN is not defined`.

Content is lifted directly from `Practice_Session_1_-_Wix_Editor_Sub-pages_Storyboard__Final_.pdf`, Scene 1.2 and the opening line of Scene 1.3.

## Variables to add (all Text, in addition to the existing `learnerEmail`/`learnerName`/`attemptId`/`debugSent` from the original test file)

- `simScene`
- `simInteraction`
- `simResponse`

These are just staging variables — overwritten at every decision point, read once by the very next slide's send trigger, then irrelevant until the next choice. Not tied to any one scene.

## Slide 1 — "Scene 1.2: Opening the Call"

**On-screen text (Sam's line, verbatim from the storyboard):**
> "Hi — I'm trying to add sub-pages to my menu and it's just not working. I've been at this for an hour."

**Trigger — Timeline starts (init, reused from the original test file's Trigger 1):**
Same `lmsGet`-based email/name/attemptId lookup as before. If you still have the original test file, this trigger doesn't change — copy it over as-is.

**Four buttons, exact text from the storyboard:**

| Button text | 
|---|
| "That sounds frustrating. Let me take a look." |
| "Hi, what's your account email?" |
| "Hi, you're through to Wix Support, this is [name]. Sorry you've been stuck — let's get it sorted. Can I start with the email on your account?" |
| "Sure — go into menu settings and switch it to Advanced." |

**Each button gets two triggers, in this order, all on "User clicks":**
1. **Adjust Variable** — three separate Adjust Variable actions (or one trigger with three actions, however your version groups them):
   - `simScene` = `"scene-1.2-opening-call"`
   - `simInteraction` = `"opening-etiquette"`
   - `simResponse` = `"<that button's exact text>"`
2. **Jump to slide** → Slide 2 ("Scene 1.3: Finding Their Account")

No `Execute JavaScript` anywhere on this slide. Every trigger type used here is one that's already proven to fire reliably in your file.

## Slide 2 — "Scene 1.3: Finding Their Account"

**On-screen text (Sam's line, verbatim — this is real next-scene content, not throwaway):**
> "It's sam.trent@gmail.com."

**Trigger — Timeline starts, Execute JavaScript:**

```javascript
var player = GetPlayer();

var ENDPOINT = 'https://docs.google.com/forms/d/e/1FAIpQLSegiZwFV7DN-wwWsqnBbrqzJ5yEK-3lk8Zl182M0fMNFYH5hg/formResponse';

var FIELDS = {
  'entry.1276253364': player.GetVar('learnerEmail'),
  'entry.2005409239': player.GetVar('learnerName'),
  'entry.1673953677': player.GetVar('attemptId'),
  'entry.2010105379': 'Practice Session 1 - Wix Editor Sub-pages - POC',
  'entry.1283761747': player.GetVar('simScene'),
  'entry.1781563601': player.GetVar('simInteraction'),
  'entry.786197073':  'n/a',
  'entry.2057562952': player.GetVar('simResponse'),
  'entry.1897805741': '',
  'entry.1780599104': '',
  'entry.1327709145': '',
  'entry.1963386753': '2-slide branch POC'
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

player.SetVar('debugSent', 'SENT ' + new Date().toLocaleTimeString());
```

`course` uses a plain hyphen, not an em dash — the handoff already flagged the em dash as a plausible copy-paste corruption source, worth avoiding preemptively here too.

Optional debug text box on this slide: `SENT: %debugSent%` — same on-screen-readout pattern as before, since `no-cors` still means the response is unreadable. Strip before anything resembling production, per the handoff's PII note.

## Test steps

1. Build the two slides above (reuse the existing test file's init trigger and variables rather than starting over).
2. Publish, upload to **Smart or SCORM Cloud** — per your call, skip Preview as the validation step.
3. Run the module **four separate times** (or four separate attempts), picking a different one of the four buttons each time.
4. Check the Sheet: expect **four rows**, same `scene = scene-1.2-opening-call` and `interaction = opening-etiquette`, but each with a different `response` matching the exact button text clicked.

If that lands: you've proven the whole pattern — real branch content, real choice text, landing in the Sheet — using only trigger types that don't depend on ever fixing (or working around via Web Object) the click-JS bug. At that point the remaining work is mechanical repetition: apply the same two-trigger-per-button / one-Timeline-Starts-per-landing-slide pattern to the other 9 scenes in the storyboard, updating only the `simScene`/`simInteraction` values and button text each time — the JS itself doesn't change between scenes.

If a row is missing or `response` doesn't match: check DevTools on that host for `Refused to connect` (CSP) before anything else — that's the only remaining unruled-out failure mode per the handoff.
