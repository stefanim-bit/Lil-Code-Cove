# Care Dojo Telemetry Sheet — Column Definitions

**One row = one learner action.** Every row from the same run shares an `attempt_id`, so filter or sort by it to rebuild one learner's full attempt in order.

| Column | What it is | How to read it |
|---|---|---|
| `timestamp` | When the row landed (added by Google Forms) | Sort by this within an attempt to see the order of actions. |
| `learner_email` | Email the learner entered on the Meet screen | Main key for finding a person. |
| `learner_name` | Name the learner entered | Typed by the learner, so spelling may vary. Match on email instead. |
| `attempt_id` | Unique ID for one run of a scenario | A new ID means a new run. If one email has several IDs, the learner retried the scenario. |
| `course` | Scenario title | Ends in `(BPO)` for BPO copies. |
| `scene` | ID of the screen the action happened on | Blank on non-choice rows (helpers, final, complete). |
| `interaction` | What kind of row it is (see **Row types** below) | Filter here first. |
| `question` | The prompt the learner saw | Only on choice rows. |
| `response` | What the learner picked or did | The reply they chose, the resource they opened, or the helper action. |
| `correct` | Verdict: `yes` / `partial` / `no` | Blank means the action isn't graded. |
| `points` | Points earned on this row | On `final` and `complete` rows, this is the **total score**. |
| `time_on_step_sec` | Seconds spent | Choice rows: time on that screen. Resource rows: time since Resources opened. Final/complete: total call time. |
| `notes` | Extra context from the engine | See **Notes examples** below. |

## Row types (`interaction` column)

| Value | Meaning |
|---|---|
| *stage name* (e.g. `Discovery`) | A graded choice on a scenario screen. |
| `resources` | Opened, closed, or clicked something in Check Resources. `correct = yes` means they opened the right article (only counts after the minimum time). `no` means they opened a distractor. |
| `mic_check` | Call builds only: the result of the mic setup (voice on, text only, new tab, blocked, error). |
| `voice` | Call builds only: a summary of how the learner's voice came across (spoken responses, too quiet/too loud counts). |
| `guided_retries` | Guided builds only. One per attempt, right before `final`. `response` lists the screens that were retried and the screens still wrong after the retry (partial or incorrect), e.g. `retried: s_open, s_ownership \| still wrong: s_open`. `notes` gives the counts. `points` is blank. |
| `final` | One per attempt, when results show. `points` = total score. |
| `complete` | The learner went through the end screen and finished. |

## Notes examples

| Row type | Example note | Meaning |
|---|---|---|
| Choice | `reply` / `action` | The learner picked something to say (reply) or something to do (action). |
| Choice | `reply; retry attempt, capped at 5` | Second try after a pushback. Points can't go above the cap. |
| Choice | `first attempt — caller pushed back, screen re-opened for a retry (capped at 5)` | A wrong first pick. It scores 0 and the screen opens again. |
| Choice | `reply; retry attempt, capped at 3; coaching shown; still wrong after retry` | Guided builds: the second try was still partial or incorrect. |
| Resources | `opened a resource (not scored)` | The scenario's Check Resources isn't scored, so there's no verdict. |
| Resources | `opened the correct resource` | They opened the right article and got credit for it. |
| Resources | `opened the correct resource too early to earn credit (before 20s)` | They opened the right article but too early in the call, so no credit. |
| Resources | `opened a distractor resource` | They opened the wrong article. |
| Voice | `6 spoken responses, 2 volume events (1 too quiet, 1 too loud)` | How much the learner spoke and how often their volume was off. |
| Final | `final score 18 / 25` | Total score out of the maximum. |
| Complete | `learner reviewed all end-screen sections and finished — 18 / 25` | They finished the whole end screen. |

Numbers in the examples are illustrative. Blank notes are normal for helper rows like opening or closing Resources and mic check.

## Quick interpretation tips

- **Score per learner:** filter `interaction = final` and read `points` or `notes`.
- **Did they finish?** The attempt has a `complete` row. A `final` row with no `complete` row means they saw their score but didn't finish the end screen. Neither row means they dropped off mid-scenario.
- **Retries inside a scenario:** a choice row with `points = 0` and a note starting "first attempt — caller pushed back" is followed by a second row for the same `scene`. The second row's points are capped (see the note).
- **Where people struggle:** filter choice rows, then group by `scene` and count `correct = no` / `partial`.
- **Hesitation:** a high `time_on_step_sec` on a choice row usually means the learner was unsure or looking something up.
- **Call recordings** live on the separate **Recordings** tab, linked by the same `attempt_id`.
- **BPO data** is in its own Sheet. The `(BPO)` label is a backup in case a row ever lands in the wrong Sheet.

## Suggested views & visualizations

**Before you start:** the Sheet has no *wave* or *topic* column. Add a small lookup tab and join it in with `VLOOKUP`/`XLOOKUP`:
- **Waves tab:** `learner_email → wave` (or group waves by date range on `timestamp`).
- **Scenarios tab:** `course → topic` (e.g. Domains, Billing), `practice_session` (PS1–PS4), `max_score`.

Build most views from a **pivot table** or a **filtered copy** of the `final` rows (one row = one attempt's score). Use the choice rows only for drill-downs.

### Expert level
| View | How | Tells you |
|---|---|---|
| Expert scorecard | Pivot: `learner_email` × `course`, value = best or latest `final` points | Each expert's standing across all scenarios. Add conditional formatting (red / amber / green). |
| First vs. best attempt | Per email + course: first `final` score next to max score | Whether retrying the scenario helped. |
| Personal weak spots | Filter by email, choice rows where `correct = no` | The exact screens to coach them on. |
| Completion status | Per email: has `final`? has `complete`? | Who hasn't started, who dropped off, who finished. |

### Wave level
| View | How | Tells you |
|---|---|---|
| Wave comparison | Bar chart: average score % per wave | Whether later waves perform better, e.g. after content changes. |
| Completion funnel | Per wave: started (any row) → `final` → `complete` | Where each wave drops off. |
| Score distribution | Histogram of score % per wave | Whether most people are strong or the scores are split. |
| Progress over time | Line chart: average score by week | Trends as each wave moves through the program. |

### Topic level
| View | How | Tells you |
|---|---|---|
| Topic heatmap | Pivot: topic × wave (or team), value = average score % | Which topics are weak, and for whom. |
| Resource use by topic | Share of attempts with a `resources` row where `correct = yes` | Whether experts look things up or guess. |
| Mistake rate by topic | Share of choice rows where `correct = no` | Topics that may need more training before the practice session. |

### Scenario level
| View | How | Tells you |
|---|---|---|
| Screen difficulty | Pivot: `scene` × `correct`, count | The hardest screens. Use it to fix content or coach. |
| Answer spread | For one `scene`: count of each `response` | Which wrong answer is most tempting. A popular wrong answer is a sign of a common misconception. |
| Time per screen | Average `time_on_step_sec` by `scene` | Screens that confuse people or need a lookup. |
| Retry rate | Share of attempts with the "caller pushed back" note, by `scene` | Where the first instinct is wrong. |
| Score distribution | Histogram of `final` score % | Whether the scenario is too easy or too hard. Ideally scores spread across the range. |
| Voice delivery (calls) | Count of `voice` rows by `response` rating | Whether volume or delivery coaching is needed. |

**Tip:** show scores as **% of max** (`points / max_score`) so scenarios with different point totals can be compared.
