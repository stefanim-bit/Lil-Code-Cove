# Sheet format (template: PS4 Domains: Connect a Domain)

The template is the source of truth for layout. Every tab has a header in row 1 (white
bold on `#242424`, frozen) and data from row 2. Copy the template; never rebuild tabs.

## Info (leave as is)

Static description of the tabs. Don't write to it.

## Meta: `Scenario Info | Your value`

Each Scenario Info cell is the setting name (bold, first line) with its help text on the
line below (`check_draft.py` writes both from the third column here). The build reads only
the first line, so never change the name.

| Scenario Info (name) | Your value | Help text (line 2) |
|---|---|---|
| `Chat title` | `<Topic>: <Scenario>`, e.g. `Domains: Connecting a Domain` | Shown in the chat header. |
| `Intro bio` | Bio in the fixed format (see SKILL.md step 2) | One line: who they are + why they're calling. |
| `First screen` | `s_open` | Screen ID of the very first screen (must exist in the Screens tab). |
| `User name` | e.g. `Jordan` | The user's first name (labels their replies). |
| `Meet image` | e.g. `Jordan/Jordan_Meet.png` | Portrait on the Meet screen (folder/file name). |
| `Close image` | e.g. `Jordan/Jordan_Close.png` | Portrait on the results screen (folder/file name). |
| `Tracking form` | the teammate's Form link, or blank | Blank = the build sends no tracking. |
| `asset.<key>` | the screenshot's folder/file name, e.g. `Scenario Screenshots/Whois.png` (or `placeholder_<key>` until the image exists) | What the screenshot shows. One row per screenshot. |
| `resources.title` | `Check Resources` | Title for the resources button/drawer. |
| `resources.sheet` | `Articles` | Source tab for reference articles. |
| `resources.enabled` | `TRUE` | Whether the resources helper drawer is enabled. |

Asset rows sit between `First screen` and `resources.title`. Choices reference them by the
full key (`asset.whois`) in their `Screenshot to display` column.

Earlier sheets use `Setting | Your value | What it does` (plain names in column A), and
the oldest (before 2026-10-21) use `Field | Value | Notes` and the keys `title`,
`userBio`, `start`. Read both; write only the new names.

## Stages: `Stage ID | Name on scorecard | Max points | Strength (shown at end if done well) | Improvement (shown at end if missed/partial) | Additive (Y/N)`

Default (template) rows, in this order. Weights must total 100:

| Stage ID | Name on scorecard | Max points |
|---|---|---|
| open | Opening & closing | 5 |
| dynamics | Use Dynamics | 10 |
| familiarize | Familiarize | 10 |
| clarify | Clarify the issue | 15 |
| roadmap | Roadmapping | 10 |
| recreate | Recreate the issue | 10 |
| article | Use resources | 20 |
| solve | Solve the issue | 20 |

Strength = full sentence, past tense, "You ..." with this scenario's specifics.
Improvement = imperative coaching line with specifics (e.g. names the right articles).

## Screens: `Screen ID | Stage scored | Expert message (optional) | User message (optional) | Question or Prompt`

- `Screen ID`: `s_<stage>`, then `s_<stage>2`, `s_<stage>3` for repeats; `s_close` for
  the closing screen (stage `open`).
- `Expert message`: optional Expert line that plays before the user's line on this screen
  (e.g. "Got it, thank you for clarifying!" before "Okay, so what now?"). Usually blank.
- `User message`: the user's line. Use a line break inside the cell for two bubbles.
- `Question or Prompt`: neutral, never names the behavior ("What do you say next?",
  "How do you respond?", "While <Name> is upgrading their site, what can you do or say?").
- Row order = play order.

## Choices: 17 columns

| Col | Header | Notes |
|---|---|---|
| A | `Screen ID` | |
| B | `Choice letter` | A, B, C... per screen |
| C | `Choice text` | Spoken line, or `[Action] ...` for a tool action. Article picks: `[Action] Reply using "<article title>"` |
| D | `Rating (correct/partial/incorrect)` | drives row color (a line break sits before "incorrect" in the header cell) |
| E | `Points` | 0 to the stage max (additive stages: this screen's share) |
| F | `Next screen (Screen ID or __end__)` | |
| G | `Retry (Y/N)` | Y only when a real user would push back |
| H | `Max points on second try` | recommended when G = Y |
| I | `Reaction 1: user reply or inline text (optional)` | user's reply, or the result of an action in plain words |
| J | `Reaction 2: Expert reply or inline text (optional)` | Expert's follow-up (often the recovery after a wrong pick), or inline text |
| K | `Reaction 3: user reply or inline text (optional)` | user again, or inline text |
| L | `Score to a different stage (optional)` | |
| M | `Extra credit: stage (optional)` | e.g. `clarify` |
| N | `Extra credit: points` | |
| O | `Extra credit: rating` | required when M is filled |
| P | `Screenshot to display` | `asset.<key>` from Meta. Shows after the reactions; `asset.<key> (show first)` shows it when picked; a line of just `[Screenshot]` inside a reaction cell shows it at that point instead |
| Q | `Only after a retry (Y/N, optional)` | Y = hidden until the screen re-opens after a Retry = Y pick (a "move on" option). The screen still needs a Retry = N choice that shows on the first try |

Inline text: any reaction (I, J or K) that starts with `[Inline text]` or `[Inline]`, or is
wrapped in `(parentheses)`, shows as a centered note instead of a bubble. Anything else
is a chat bubble (I and K = user, J = Expert). Action results always use a marker,
e.g. `[Inline] Domain Status: Active`.

Patterns from the template worth repeating: a wrong opener gets a confused user in
I plus an Expert recovery in J; `[Action]` picks put the found result in I ("[Inline] Domain
Status: Active / Expire Date: ..."); Familiarize choices that also clarify carry a
`clarify` extra credit.

## Articles: `Article title (same words as the choice) | Article link | Right article? (Y/Partial/N) | Points`

| Col | Value |
|---|---|
| A Article title | the article's name only (no `Reply using`, no quotes) |
| B Article link | the exact link the Expert Assistant cited |
| C Right article? | `Y`, `Partial`, or `N` |
| D Points | 20 for Y, 10 for Partial, 0 or 10 for N (as the user decides) |

Every `[Action] Reply using "..."` choice must quote a title listed here (capitalization,
punctuation and quote style don't matter). The drawer name (`Check Resources`) and stage
(`article`) are set once per scenario by the build, not per row. Older sheets have extra
`Title` and `Stage (this credits)` columns first; skip them when reading.

The engine doesn't score Partial or per-article Points yet (planned for the end-of-October
engine update), but fill them in.

---

## Draft JSON

The local draft (`Research/scenario-draft.json`) that the checker validates and turns
into sheet values. Keys map 1:1 to the columns above; omit empty optional keys.

```json
{
  "sheet_title": "PS5 Domains: Example Scenario",
  "meta": {
    "title": "Domains: Example Scenario",
    "userBio": "Riley wants to ... In this activity, you'll simulate a chat with them. Click *\"Check Resources\"* to view internal and external help documents at any point during the interaction. Let's begin!",
    "start": "s_open",
    "user_name": "Riley", "meet_image": "Riley/Riley_Meet.png", "close_image": "Riley/Riley_Close.png",
    "tracking_form": "",
    "assets": [
      {"key": "asset.user_manager", "value": "Scenario Screenshots/User Manager.png", "notes": "Placeholder asset key for Riley User Manager view."}
    ],
    "resources": {"title": "Check Resources", "sheet": "Articles", "enabled": true}
  },
  "stages": [
    {"id": "open", "name": "Opening & closing", "max": 5, "strength": "...", "improvement": "..."}
  ],
  "screens": [
    {"screen_id": "s_open", "stage": "open", "learner": "", "speaker": "Hi! ...", "prompt": "How do you open the conversation?"}
  ],
  "choices": [
    {"screen_id": "s_open", "choice_id": "A", "text": "...", "verdict": "correct", "points": 5,
     "goTo": "s_familiarize", "retry": "N", "capIfRetried": null,
     "caller1": "...", "expert": "", "caller2": "",
     "stageOverride": "", "credit_stage": "", "credit_points": null, "credit_verdict": "",
     "asset": "", "retryOnly": false}
  ],
  "articles": [
    {"article_title": "Exact Article Title", "url": "https://...", "correct": "Y", "credit": 20}
  ]
}
```

`stages` lists all eight with `max`. Set `"additive": true` on any stage that sums
across screens (usually `solve`). It's written to the Stages tab's
Additive (Y/N) column (Y, or blank when false), and the checker uses it to test that
the stage can reach its max.
