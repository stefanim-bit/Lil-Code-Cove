# Identity-linking options — parked, not in progress

Context: Rise's Code Block sandbox blocks any access to the SCORM API (`cmi.core.student_id`), confirmed in both Rise's editor preview and a real Smart-published course (`Blocked a frame with origin "https://packages.articulateusercontent.com" from accessing a cross-origin frame`). A Storyline block embedded in Rise appears not to have this restriction — community reports confirm people writing real `cmi.interactions` data from inside one — so it can read the SCORM email where a Code Block can't.

That still leaves a gap: Code Blocks can't read anything from each other or from an embedded Storyline block (same isolation). Two ways to bridge that gap were discussed and **parked as of 2026-08-12** — not pursued further right now, kept here in case they're worth revisiting:

**1. Short session code, typed once.** The Storyline block reads the real SCORM email, generates a short code, POSTs an identity row (code + email) to the Sheet, and displays the code for the learner to type into Rise. Exact join, no ambiguity, but costs the learner one bit of manual entry — and if the 10 scenes stay as separate Code Blocks rather than being consolidated, that entry would need repeating per scene.

**2. Timestamp stitching, no learner action.** The Storyline block's identity row and the Code Blocks' choice rows all land with precise timestamps; group rows by proximity to infer which session they belong to. Zero friction, but probabilistic — breaks down if two Experts test within the same tight window. (Smart's own attempt records only expose enroll date, not a per-attempt timestamp, so this can't be backed by an authoritative source either — it would rely entirely on our own client-side timestamps.)

Neither was judged ideal. Not in progress — revisit if a better idea surfaces or if these tradeoffs become acceptable later.
