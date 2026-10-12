# Interactive learning

The existing Jekyll site serves all exercises and reading material locally.
No AI credentials, additional service, or package CDN is needed by the browser
workshops. An external AI assistant still has its own installation and account.

## Workshops

`_data/workshops.yml` names six original exercises. `scripts/build-labs.py`
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
the editor and downloads usable. Drafts and the last source-matched test result are optional fields in version-1
reading backups. `codepop:workshop-check:<id>` records source, passed/total and
check time; editing makes the displayed result stale. Downloads remain available. Reference solutions are
explicitly available for comparison and never overwrite a draft automatically.

## Knowledge checks and AI discovery

Keep questions in `_data/knowledge_checks.yml`, keyed by learning path ID.
Five paths provide ten scenarios each (50 total). Each scenario has stable question IDs, answer choices, an explanation, and a real
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
workshop's deferred Worker and the optional vendored field-metrics core. Separate feature bundles load only where used.
CSS keeps its existing 130 KB per-page ceiling.

Reference for the browser boundary:
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers

Validation: build assets, build Jekyll, check books/site/content/labs, run UI
tests in Chromium and critical interactions in Firefox and WebKit, then run
the mobile Lighthouse performance checks.


## My Learning and editor controls

`/learn/workspace/` reads the existing local book, checklist, quiz and workshop
keys without rewriting them. Only catalogued chapter URLs can become resume
links. Counts of quiz choices do not imply correctness or practical completion.
Unknown records are ignored, corrupt records are reported without deletion, and
blocked storage leaves ordinary content links usable. The server renders all
book/path/workshop links for no-JavaScript navigation.

The editor's small lexical overlay and line gutter are hidden from assistive
technology; the labelled native textarea remains the editing control. Tab keeps
normal navigation; Ctrl/Cmd+Enter activates the existing sandboxed runner.
Forced colors restore ordinary textarea text. `.js`/`.mjs` imports are bounded
to 40 KB, require explicit replacement and never execute on import. Exercise
changes discard pending imports. Reference comparison uses a bounded 240-line
LCS preview, displays text only, and never marks an alternative solution wrong
solely because it differs from the reference.

Backups optionally include `workshops: { <id>: { draft, check } }`; drafts are
raw strings in storage, check records are JSON. Imports validate known IDs,
40,000-character limits, finite timestamps and passed/total bounds before writing.
Merge keeps local drafts, replace affects included entries only, and partial
writes roll back to their exact prior raw values. Backups can contain private
notes and source code; the interface tells visitors before export/import.

## Guided study and connected videos (2026-10-13)

`/learn/start/` uses `_data/learning_starts.yml` to recommend one existing path.
Topic, experience, and time are allowlisted URL values. The short option suggests
one practical step; the longer option suggests three. Times are planning
estimates, not measured completion times or prerequisites waived by a selector.

My Learning stores an explicit `codepop:study-plan` with a known path, a bounded
300-character goal, 20/40/60-minute sessions, and 2/3/5 planned sessions. The plan
uses only unfinished manual steps. Later sessions revisit the knowledge check;
it does not mark steps complete. Incorrect valid saved answers form a review
queue with stable question anchors. Unanswered questions remain in the path.

The optional `plan` field extends version-1 backups. Old files work unchanged;
imports validate values, preview the learning plan, preserve the existing plan
on merge, replace it only explicitly, and use the existing rollback behavior.
No goal, quiz text, or planner data is sent to analytics.

Six canonical workshops have three stages each. Each test belongs to exactly
one stage, validated during packaging. Stage results expire on edits, reset, or
exercise changes. Hints are native details elements, with static copies below
the editor for reading without JavaScript. The two new exercises use synthetic
objects and never connect to Kubernetes or sockets.

`_data/video_lessons.yml` is editorial source independent of playlist sync.
The video generator creates 15 companion pages before metadata generation.
Each links a real chapter and path and provides an original exercise with
observable evidence. These are learning companions, not copied transcripts.
Public timed captions were unavailable during authoring, so no topic timestamps
were invented. Visitors can create validated links to moments within the known
duration; creating a link never loads the player. Chapter/path/project links
are reciprocal. All companion pages enter search, sitemap, and deployment checks.
