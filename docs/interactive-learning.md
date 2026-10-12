# Interactive learning

The existing Jekyll site serves all exercises and reading material locally.
No AI credentials, additional service, or package CDN is needed by the browser
workshops. An external AI assistant still has its own installation and account.

## Workshops

`_data/workshops.yml` names four original exercises. `scripts/build-labs.py`
packages their Node workspace and creates `assets/labs/browser-workshops.json`
from the canonical starters, separate solutions, and acceptance tests. The
browser adapter replaces only the Node imports; assertions are not rewritten.
Run `npm run check:labs` to confirm the starters fail and solutions pass in Node.
Browser tests confirm the same outcomes for every exercise.

`assets/js/labs/editor.js` loads only on `/ai/workshops/`. Code executes in a
fresh Worker with separate module imports inside an iframe with `sandbox="allow-scripts"`, without
same-origin permission. Its CSP denies network connections and external scripts.
The frame has no site storage access and the worker has no DOM. Stop, navigation,
exercise changes, and a four-second timeout discard the runner. Code and output
are rendered as text and never sent to analytics. These are transparent teaching
tests, not a tamper-proof grading or certification service.

Drafts use `codepop:workshop:<id>` on the visitor's device. Storage failure leaves
the editor and downloads usable. Drafts are intentionally separate from reading
backups; download `app.mjs` to keep a portable copy. Reference solutions are
explicitly available for comparison and never overwrite a draft automatically.

## Knowledge checks and AI discovery

Keep questions in `_data/knowledge_checks.yml`, keyed by learning path ID.
Each scenario has stable question IDs, answer choices, an explanation, and a real
reading link. Answers use `codepop:knowledge:<path-id>` and are optional in
version-1 reading backups. Imports validate question IDs and option bounds before
any write; old backups remain supported. Merge preserves local answer choices.
Quizzes do not automatically mark practical exercises complete. Explanations and
reading links remain available without JavaScript.

AI posts declare editorial `level` and `environments` in addition to their exact
`surface` and `format`. `web` includes browser workshop practice, `desktop` is a
desktop app, `cli` is a terminal, and `ide` is an editor integration. A workshop
can cover browser practice and a documented CLI workflow; this does not make
that tool's CLI commands available in a web chat. Combined filters preserve
`q`, `tool`, `category`, `environment`, `format`, and `level` in shareable URLs.
The AI filter selects progressively enhance into themed select-only comboboxes
with pointer selection, arrows, Home/End, typeahead, Enter/Space, Tab, and Escape.
URL restoration and clearing synchronize their displayed values. If the
enhancement cannot load, labelled native selects remain available. The keyboard
pattern follows https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-select-only/ .

## Reading assistance

`_data/glossary.yml` supplies original, short definitions for each book with
real chapter slugs. The sidebar works without JavaScript. Global search can
filter by book and highlights a contextual excerpt. Chapter results carry a
`find` query that the reader highlights locally, without changing canonicals.
Book-wide search fetches the index only on request; section search works without
a connection. Queries and selected text never enter analytics or storage.

The native figure dialog supports keyboard focus containment, Escape, original
image resolution, and 100–300% zoom. Closing it preserves reader focus mode and
returns focus to its trigger. Print output excludes assistive controls.

The JavaScript performance ceiling remains 65 KB per page, including the
workshop's deferred Worker. Separate feature bundles load only where used.
CSS keeps its existing 130 KB per-page ceiling.

Reference for the browser boundary:
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers

Validation: build assets, build Jekyll, check books/site/content/labs, run UI
tests in Chromium and critical interactions in Firefox and WebKit, then run
the mobile Lighthouse performance checks.
