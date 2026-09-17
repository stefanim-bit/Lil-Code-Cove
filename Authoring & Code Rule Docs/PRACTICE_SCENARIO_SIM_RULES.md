# Practice Session — Simulation Rules & Rollout Guide

Shared UI/behavior rules for the interactive practice-call HTML scenarios
(`Current Sub-Pages Scenario.html`, `ps3_billing_double_charge_monthly_plan.html`,
`wix_editor_layers_scenario.html`, and any future scenario built on the same engine).

Each scenario is a single self-contained HTML file that shares the same JS engine
(look for `function revealSegments`). Apply every rule below to each file.

---

## Reference colors (from `assets/reference/colors.png`)

| Token            | Hex       | Used for                                             |
|------------------|-----------|------------------------------------------------------|
| **Inline green** | `#5BBE7E` | Centered inline notes only (see Rule 3)              |
| Orange (brand)   | `#DA3B01` | End button                                            |
| Blue (agent)     | `#0F62E6` | Expert bubbles / accents                             |
| Deep blue        | `#1464A0` | —                                                    |

---

## Rule 1 — Simulation container: fixed chat window, options always visible

The chat (`.chat`) is a **fixed-height window with its own inner scrollbar** — it
stays ONE consistent size on every screen. The point is NOT to show the whole
conversation at once; it's that the **response options below the chat are always
fully visible without scrolling the page**. Older messages scroll inside the chat;
the options never get pushed off-screen on the common (≤4 option) screens.

Find the `.chat{…}` rule and set a fixed height (`40vh`) that leaves room for the
options, keeping the inner scroll:

```css
/* BEFORE (e.g. 52vh was too tall — options fell below the fold) */
.chat{ … ; height:52vh; overflow-y:auto }

/* AFTER */
.chat{ … ; height:40vh; overflow-y:auto }
```

`40vh` fits the options on every screen with up to 4 options (including the reported
clarify screen). A rare screen with many options (e.g. a 6-option article stage) can
still push the last option(s) just below the fold on short viewports — accepted
tradeoff in exchange for a consistent chat size. If a scenario routinely uses 5–6
option screens and you want them to fit too, lower the value (≈`35vh`).

**Variant — flex-based `.chat`.** Some files (e.g. `ps3_billing_double_charge_monthly_plan.html`)
size the chat with flex: `.chat{ … ; flex:1 1 auto; min-height:0; overflow-y:auto }`
inside a flex `.panel`. To match the fixed-window behavior, drop the flex and give it a
fixed `height:40vh; overflow-y:auto` like above (and remove any `flex:1` / `min-height:0`
on the parent that was letting the panel size to the viewport).

Do NOT use `height:auto` / `min-height` (the sim then grows with the conversation and
pushes the options off-screen — the exact bug this rule fixes).

---

## Rule 2 — "Click to view fullscreen" on every sim

Add a fullscreen toggle to the sim header, using the native Fullscreen API on the
`.panel` element.

**a. Give the panel an id** (in the `startCall()` template):

```html
<section class="panel" id="sim">
```

**b. Add the button** in `.panel-head`, to the **left of the Check Resources
button** — i.e. immediately *before* the `helperbar-head` div (not after it):

```html
<button class="btn-fs" id="fsBtn" type="button" title="Click to view fullscreen">⤢ Click to view fullscreen</button>
<div class="helperbar-head" id="helperbar"></div>
<button class="btn-end" id="endBtn">End</button>
```

**c. CSS:**

```css
.btn-fs{background:none;border:0;color:var(--muted);font-family:var(--font-text);font-weight:600;font-size:0.78125rem;cursor:pointer;padding:0.4375rem 0.625rem;border-radius:62.4375rem;display:inline-flex;align-items:center;gap:0.375rem}
.btn-fs:hover{color:var(--agent);background:var(--agent-bubble)}
.panel:fullscreen{border-radius:0;display:flex;flex-direction:column;overflow:auto}
.panel:fullscreen .chat{min-height:0;flex:1}
```

**d. JS** — wire it up inside `startCall()`, right after the `endBtn` handler:

```js
const fsBtn = document.getElementById('fsBtn'), sim = document.getElementById('sim');
if(fsBtn && sim && document.fullscreenEnabled){
  fsBtn.onclick = ()=>{
    if(document.fullscreenElement) document.exitFullscreen();
    else sim.requestFullscreen().catch(()=>{});
  };
  document.addEventListener('fullscreenchange', ()=>{
    fsBtn.innerHTML = document.fullscreenElement===sim ? '⤡ Exit fullscreen' : '⤢ Click to view fullscreen';
  });
} else if(fsBtn){ fsBtn.style.display='none'; }
```

---

## Rule 3 — Inline notes: green + timed reveal (2s notes / 5s typing)

**Definition — "inline note" = the centered `system` bubble ONLY.** These are:
- an **action the Expert takes** — e.g. "You clone Sarah's site in User Manager…"
- a **thing the Expert finds** — e.g. "(You find there's a button that says 'Set to Advanced'.)"

Caller (Sarah) replies and the Expert's own spoken bubbles are **NOT** inline notes —
they keep their normal color and normal timing. Do not turn responses green.

### 3a. Color — green `#5BBE7E`

Add after the `.msg.system .bubble.action{…}` rule:

```css
/* Inline notes — centered "system" bubbles only: an action you take or a
   thing you find. These are the ONLY lines painted green. */
.msg.reaction .bubble,
.msg.reaction .bubble.action{color:#5BBE7E !important}
```

### 3b. Timing — inline notes 2s apart, spoken consequence lines 5s typing

Inside a consequence (a `reaction` reveal):

- **Inline notes (centered `system` bubbles)** reveal on a **2-second** beat — 2s after
  the choice for the first, and 2s between each subsequent inline note.
- **Spoken consequence lines — Samantha (caller) OR the Expert (learner/`you`)** — show a
  **5-second typing indicator**, then land. The Expert typing indicator applies **only to
  consequence replies**, never to a normal choice selection (the learner's own pick still
  appears immediately).

Add the constants near the other timing constants (`TAI_MS`, `YOU_MS`…):

```js
// Consequence beats: inline notes 2s apart; spoken lines get a 5s typing indicator.
const REACT_INLINE_MS = 2000, REACT_TYPING_MS = 5000;
```

Make `typingBubble` able to render on the Expert (`you`) side too:

```js
function typingBubble(kind){
  const you = kind==='you';
  const side = you ? 'you' : 'caller';
  const who  = you ? (learner_name||'You') : U.name;
  return appendNode(
    `<div class="msg typing ${side}"><div class="meta">${escapeHtml(who)} · typing…</div>`+
    `<div class="bubble"><span class="tai-dot"></span><span class="tai-dot"></span><span class="tai-dot"></span></div></div>`);
}
```

### 3c. Plumbing — tag inline notes with a `reaction` class

The green class + 1s beat are driven by a `reaction` flag threaded through the
bubble renderers. Make these four edits:

**`bubbleMarkup`** — accept `reaction`, add the class:

```js
function bubbleMarkup(kind, text, metaText, reaction){
  const meta = metaText ? `<div class="meta">${escapeHtml(metaText)}</div>` : '';
  const cls  = 'bubble' + (kind==='system' ? ' action' : '');
  const msgCls = 'msg ' + kind + (reaction ? ' reaction' : '');
  const body = escapeHtml(px(text)).replace(/\n/g,'<br>');
  return `<div class="${msgCls}">${meta}<div class="${cls}">${body}</div></div>`;
}
```

**`appendBubble`** — accept and forward `reaction`:

```js
function appendBubble(kind, text, reaction){
  const meta = kind==='system' ? '' :
    `${kind==='you' ? (learner_name||'You') : U.name} · ${mmss(callSeconds)}`;
  return appendNode(bubbleMarkup(kind, text, meta, reaction));
}
```

**`appendActionNote`** — the learner's own action note is an inline note, so mark it:

```js
function appendActionNote(text){ return appendBubble('system', text, true); }
```

**`revealSegments`** — add an `opts.reaction` mode where **only `system` segments**
turn green (2s beat), and spoken consequence lines (caller/you) get the 5s typing
indicator. Outside a reaction reveal, behavior is unchanged:

```js
function revealSegments(segs, animate, done, opts){
  opts = opts || {};
  const reaction = !!opts.reaction;
  let i=0, sawCaller=false;
  (function next(){
    if(i>=segs.length){ if(done) done(); return; }
    const s=segs[i++];
    // In a consequence (reaction) reveal:
    //  • centered inline notes (system) turn green and reveal 2s apart;
    //  • spoken lines — Samantha (caller) OR the Expert (you) — show a 5s typing
    //    indicator, then land.
    const inlineNote = reaction && s.kind==='system';
    if(!animate){ appendBubble(s.kind, s.text, inlineNote); return next(); }
    if(inlineNote){
      setTimeout(()=>{ appendBubble('system', s.text, true); next(); }, REACT_INLINE_MS);
    } else if(reaction && (s.kind==='caller' || s.kind==='you')){
      const dots=typingBubble(s.kind);
      setTimeout(()=>{ dots.remove(); appendBubble(s.kind, s.text); next(); }, REACT_TYPING_MS);
    } else if(s.kind==='caller'){
      const t = sawCaller ? TAI_FOLLOW_MS : TAI_MS; sawCaller=true;
      const dots=typingBubble();
      setTimeout(()=>{ dots.remove(); appendBubble('caller', s.text); next(); }, t);
    } else {
      setTimeout(()=>{ appendBubble(s.kind, s.text); next(); }, s.kind==='you'?YOU_MS:SYS_MS);
    }
  })();
}
```

Finally, pass `{ reaction:true }` as the 4th arg on **both** consequence reveals in
`choose()` (the retry/pushback reveal and the normal auto-advance reveal):

```js
revealSegments(segs, true, ()=> …renderScreen(scr.id, {…}), { reaction:true });
…
revealSegments(segs, true, ()=>{ …renderScreen(ch.goTo, {animateSpeaker:true}); }, { reaction:true });
```

---

## Authoring rule — inline notes vs. spoken lines

In scenario data (`consequence` strings):

- **Inline note (goes green, 1s beat):** wrap in parentheses → `"(You find there's a button that says 'Set to Advanced'.)"`. These render as centered `system` bubbles.
- **A thing the Expert DOES:** author the choice as `text:"[Action] …"` with **no** `say`. It renders as a green centered action note ("You …").
- **A spoken reply (NOT green):** use a `say:` value, or a plain choice `text`, or a `Sarah:`/`Expert:` labeled line in a `consequence`. These stay normal-colored.

Do **not** give an `[Action]` choice a `say:` value — that turns it into a spoken
(blue) line instead of a green centered action note.

---

## Rule 4 — Screenshots: choice-gated, no caption, click-to-zoom

Screenshots (the Layers panel, Accessibility Wizard, etc.) live on a screen as
`scr.image = { src, alt }`. Three behaviors:

**4a. No caption.** Learners read the screenshot and find the info themselves — never
label what it shows. Drop any `caption` field, and make `appendImage` render no
`<figcaption>`.

**4b. Click-to-zoom (lightbox).** Every screenshot opens enlarged on click / Enter / Space.

```css
.msg.system .screenshot img{ …existing… ; cursor:zoom-in }

/* Lightbox: click-to-enlarge overlay for inline screenshots */
.lightbox{border:0;padding:0;background:transparent;max-width:95vw;max-height:95vh}
.lightbox::backdrop{background:rgba(15,17,25,0.82)}
.lightbox img{display:block;max-width:95vw;max-height:95vh;object-fit:contain;border-radius:0.5rem;box-shadow:0 1.5rem 3rem rgba(0,0,0,0.35)}
.lightbox-close{position:fixed;top:1rem;right:1.5rem;background:rgba(255,255,255,0.92);border:0;border-radius:50%;width:2.5rem;height:2.5rem;font-size:1.5rem;line-height:1;cursor:pointer;color:var(--ink)}
.lightbox-close:hover{background:#fff}
```

```js
function appendImage(img){
  if(!img || !img.src) return null;
  const alt = escapeHtml(img.alt || '');
  // No caption; click / Enter / Space opens the zoom lightbox.
  return appendNode(
    `<div class="msg system"><figure class="screenshot">`+
    `<img src="${escapeHtml(img.src)}" alt="${alt}" loading="lazy" tabindex="0" role="button" `+
    `aria-label="View larger image" onclick="window.__openLightbox(this.src,this.alt)" `+
    `onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();window.__openLightbox(this.src,this.alt);}" `+
    `onerror="this.closest('figure').innerHTML='<div class=\\'noimg\\'>[ screenshot not found ]</div>'">`+
    `</figure></div>`);
}
function openLightbox(src, alt){
  const dlg = document.createElement('dialog'); dlg.className='lightbox';
  dlg.innerHTML = `<button class="lightbox-close" aria-label="Close">&times;</button>`+
    `<img src="${escapeHtml(src)}" alt="${escapeHtml(alt||'')}">`;
  document.body.appendChild(dlg); dlg.showModal();
  const close = ()=>{ try{dlg.close();}catch(e){} dlg.remove(); };
  dlg.addEventListener('click', e=>{ if(e.target===dlg) close(); });
  dlg.querySelector('.lightbox-close').onclick = close;
}
window.__openLightbox = openLightbox;
```

**4c. Choice-gated reveal (immediately on selection).** A screenshot must NOT auto-show
before the choices. It appears only when the learner picks the specific choice tied to
it, the instant that choice is selected (before the consequence reply).

- In `renderScreen`'s `showChoices`, **remove** the automatic `if(scr.image) appendImage(scr.image)`.
- Flag the triggering choice in scenario data: `{ id:"C", …, showsImage:true }`.
- In `choose()`, right after the pick bubble is appended (before the consequence reveal):

```js
// Choice-gated screenshot: shows immediately on selection, before the reply.
if(ch.showsImage && scr.image) appendImage(scr.image);
```

---

## Rule 5 — Complete screen: no "Chat complete" eyebrow

On the results/complete screen, remove the small eyebrow label above the heading. Keep
the `Complete!` heading.

```html
<!-- remove this line -->
<div class="eyebrow">Chat complete</div>
<h1 class="display">Complete!</h1>
```

---

## Rule 6 — Speaker lines that depend on looking something up (e.g. "You open CSI")

Some screens have a speaker line that only makes sense if the learner actually did the
thing it describes first. The clearest example: a screen opens with `"(You open CSI.)"`
— but that should only play if the learner actually opened a resource link in **Check
Resources** at some point in the call. If they never opened one, the line must be
skipped entirely (no fallback text) — not shown, and not left dangling implying the
learner looked something up when they didn't.

**"Opens a resource" = clicks an actual resource link inside the Check Resources
modal** (correct or distractor). Opening the modal and closing it without clicking
anything does **not** count.

This must hold in **two places**: the live reveal, and the end-of-call transcript
replay (which re-renders every screen's speaker line from a stored value — a naive
fix that only gates the live view will still leak the line into the results transcript).

**a. Track it.** Add a flag to the `help` state object, set on any resource-link click
(not just the correct one):

```js
const help = { used:false, checkedCorrectArticle:false, openedAnyResourceLink:false };
```

In `openResources()`, at the top of each item's `onclick`:

```js
a.onclick=()=>{
  // Any resource link click (correct or distractor) counts as "opened a
  // resource" — this gates speaker lines like "(You open CSI.)" that should
  // only appear if the learner actually looked something up.
  help.openedAnyResourceLink = true;
  if(it.correct){ … }
};
```

**b. Gate the live reveal.** Add a generic `speakerIf` field a screen can set, and a
small resolver (extensible for future gate keys):

```js
function speakerGateMet(scr){
  if(!scr.speakerIf) return true;
  if(scr.speakerIf === 'resourceOpened') return !!help.openedAnyResourceLink;
  return true;
}
```

Track whether the CURRENT screen's speaker line actually played, so downstream code
(the transcript push) can match what was really shown:

```js
let currentSpeakerShown = false;   // declare near earned/status/transcript
```

In `renderScreen`:

```js
currentSpeakerShown = !!(scr.speaker && !opts.skipSpeaker && speakerGateMet(scr));
if(currentSpeakerShown){
  revealSegments(splitDialogue(scr.speaker), !!opts.animateSpeaker, showChoices);
} else {
  showChoices();
}
```

**c. Gate the transcript record.** In `choose()`, both `transcript.push({...})` calls
currently store `scr.speaker` unconditionally — fix both to use `currentSpeakerShown`
so the end-screen replay matches what the learner actually saw:

```js
// retry/pushback push:
transcript.push({ speaker: currentSpeakerShown ? scr.speaker : null, picked:ch.text, say:ch.say, consequence:ch.consequence });

// normal auto-advance push:
transcript.push({ speaker: (typeof cap==='number' || !currentSpeakerShown) ? null : scr.speaker, picked:ch.text, say:ch.say, consequence:ch.consequence });
```

**d. Author it.** On any screen whose speaker line depends on a resource lookup, add
`speakerIf:"resourceOpened"` next to `speaker`:

```js
s_article: {
  stage:"article", gate:true,
  speaker:"(You open CSI.)", speakerIf:"resourceOpened",
  …
}
```

---

## Verified reference implementation

`wix_editor_layers_scenario.html` has **all** rules applied (fixed chat window,
fullscreen button left of Check Resources, green 2s inline notes + 5s typing,
choice-gated zoomable captionless screenshots, no "Chat complete" eyebrow) — use it as
the copy source when updating the other scenarios. `Current Sub-Pages Scenario.html`
has Rules 1–3 and 5–6 (it has no screenshots, so Rule 4 does not apply there).

> **Testing note:** scenarios with full-res embedded screenshots can exceed the preview
> pane's file-size limit and won't open directly. To test live, make a temporary copy and
> replace the long `data:image/png;base64,…` strings with a small placeholder image, then
> open the copy. The engine/logic is identical, so behavior is faithfully reproduced.
