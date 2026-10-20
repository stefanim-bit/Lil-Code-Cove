# Sheet format (template: PS4 Domains: Connect a Domain)

The template is the source of truth for layout. Every tab has a header in row 1 (white
bold on `#242424`, frozen) and data from row 2. Copy the template; never rebuild tabs.

## Info (leave as is)

Static description of the tabs. Don't write to it.

## Meta: `field | value | notes`

| field | value | notes |
|---|---|---|
| `title` | `<Topic>: <Scenario>`, e.g. `Domains: Connecting a Domain` | Shown in the chat header. |
| `userBio` | Bio in the fixed format (see SKILL.md step 2) | One line: who they are + why they're calling. |
| `start` | `s_open` | screen_id of the very first screen (must exist in the Screens tab). |
| `asset.<key>` | `placeholder_<key>` | Placeholder asset key for <what the screenshot shows>. One row per screenshot. |
| `resources.title` | `Check Resources` | Title for the resources button/drawer. |
| `resources.sheet` | `Articles` | Source tab for reference articles. |
| `resources.enabled` | `TRUE` | Whether the resources helper drawer is enabled. |

Asset rows sit between `start` and `resources.title`. Choices reference them by the
full key (`asset.whois`) in their `asset` column.

## Stages: `id | name | max | strength | improvement`

Default (template) rows, in this order. Weights must total 100:

| id | name | max |
|---|---|---|
| open | Opening & closing | 5 |
| dynamics | Use Dynamics | 10 |
| familiarize | Familiarize | 10 |
| clarify | Clarify the issue | 15 |
| roadmap | Roadmapping | 10 |
| recreate | Recreate the issue | 10 |
| article | Use resources | 20 |
| solve | Solve the issue | 20 |

`strength` = full sentence, past tense, "You ..." with this scenario's specifics.
`improvement` = imperative coaching line with specifics (e.g. names the right articles).

## Screens: `screen_id | stage | gate (Y/N) | learner (expert line, optional) | speaker (caller line, optional) | prompt`

- `screen_id`: `s_<stage>`, then `s_<stage>2`, `s_<stage>3` for repeats; `s_close` for
  the closing screen (stage `open`).
- `learner`: an Expert line shown before the caller's line on that screen (rare).
- `speaker`: the caller's line. Use a line break inside the cell for two bubbles.
- `prompt`: neutral, never names the behavior ("What do you say next?", "How do you
  respond?", "While <Name> is upgrading their site, what can you do or say?").
- Row order = play order.

## Choices: 16 columns

| Col | Header | Notes |
|---|---|---|
| A | `screen_id` | |
| B | `choice_id` | A, B, C... per screen |
| C | `text` | Spoken line, or `[Action] ...` for a tool action. Article picks: `[Action] Reply using "<exact title>"` |
| D | `verdict (correct/partial/incorrect)` | drives row color |
| E | `points` | 0 to the stage max (additive stages: this screen's share) |
| F | `goTo (screen_id or __end__)` | |
| G | `retry (Y/N)` | Y only when a real caller would push back |
| H | `capIfRetried` | required when G = Y |
| I | `consequence (optional caller reaction or inline outcome) 1` | caller's reply, or the result of an action in plain words |
| J | `consequence (optional expert reply or inline outcome)` | Expert's follow-up (often the recovery after a wrong pick) |
| K | `consequence (optional caller reaction or inline outcome) 2` | caller again |
| L | `stage Override (optional)` | |
| M | `credit_stage (optional floating credit)` | e.g. `clarify` |
| N | `credit_points` | |
| O | `credit_verdict` | |
| P | `asset` | `asset.<key>` from Meta |

Patterns from the template worth repeating: a wrong opener gets a confused caller in
I plus an Expert recovery in J; `[Action]` picks put the found result in I ("Domain
Status: Active / Expire Date: ..."); Familiarize choices that also clarify carry a
`clarify` floating credit.

## Articles: `title | stage (this credits) | article_title | URL | correct (Y/N) | Credit`

| Col | Value |
|---|---|
| title | `Check Resources` |
| stage | `article` |
| article_title | `[Action] Reply using "<exact article title>"` |
| URL | the exact link the Expert Assistant cited |
| correct | `Y`, `Partial`, or `N` |
| Credit | 20 for Y, 10 for Partial, 0 or 10 for N (as the user decides) |

Every `[Action] Reply using "..."` choice on the article screen must match a row here.

The template prefills `title` and `stage` on rows 2–11 (greyed out, soft validation). Write
each article into the next prefilled row; don't overwrite A/B. When reading a sheet, skip
any row with no `article_title` and no `URL` — it's an unused prefilled row, not an article.

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
    "assets": [
      {"key": "asset.user_manager", "value": "placeholder_user_manager", "notes": "Placeholder asset key for Riley User Manager view."}
    ],
    "resources": {"title": "Check Resources", "sheet": "Articles", "enabled": true}
  },
  "stages": [
    {"id": "open", "name": "Opening & closing", "max": 5, "strength": "...", "improvement": "..."}
  ],
  "screens": [
    {"screen_id": "s_open", "stage": "open", "gate": "N", "learner": "", "speaker": "Hi! ...", "prompt": "How do you open the conversation?"}
  ],
  "choices": [
    {"screen_id": "s_open", "choice_id": "A", "text": "...", "verdict": "correct", "points": 5,
     "goTo": "s_familiarize", "retry": "N", "capIfRetried": null,
     "caller1": "...", "expert": "", "caller2": "",
     "stageOverride": "", "credit_stage": "", "credit_points": null, "credit_verdict": "",
     "asset": ""}
  ],
  "articles": [
    {"article_title": "[Action] Reply using \"Exact Article Title\"", "url": "https://...", "correct": "Y", "credit": 20}
  ]
}
```

`stages` lists all eight with `max`. Set `"additive": true` on any stage that sums
across screens (usually `solve`). The template's Stages tab has no additive column,
so this flag is used only by the checker (to test that the stage can reach its max)
and isn't written to the sheet.
