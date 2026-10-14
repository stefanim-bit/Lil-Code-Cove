# Agent notes

- This repo is a collection of standalone, self-contained HTML practice scenarios (Wix CS training, embedded in Rise/Wix HTML blocks). No build step, no package manager, no backend.
- Base44 preview: `docker compose -f docker-compose.base44.yml up -d` runs nginx (config in `.base44/nginx.conf`) serving the repo root read-only on port 3000 with a directory listing. Caching is disabled, so edits show on refresh; there is no live reload (refresh the preview after edits).
- Preview-only extras (scenario files on disk are never modified): `.base44/start-here.html` is shown above the file list on `/`; `.base44/feedback.js` (a click-an-element "Give feedback" button that builds a copyable note for the designer) is injected into every `.html` page by nginx `sub_filter` at `</body>`. After editing `.base44/nginx.conf`, run `docker compose -f docker-compose.base44.yml restart web` (a reload can miss the change). Feedback notes pasted in chat start with `DESIGN FEEDBACK` and name the scenario file, screen, element, and a CSS-style location; use them to find the exact spot in the scenario file.
- Paths contain spaces, `&`, and em-dashes — quote them in shell commands and URL-encode them in links.
- The only runtime network calls are Google Fonts / Wix static fonts and a public Google Forms `formResponse` telemetry POST (hardcoded, no credentials). No secrets required.
- `scenario_xlsx_to_js.py` is an offline authoring helper (xlsx -> JS), not part of the runtime.
- Verify: `curl -s localhost:3000/` lists the folders; open a scenario e.g. `/Practice Session 3/PS3 Wire Transfer/session3_billing_wire_transfer.html`.
