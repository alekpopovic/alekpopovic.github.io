# 018. Freeze chapter scope, dependencies and evidence coverage

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 017 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; books/inside-orch/editorial/READER_PATHS.md; books/inside-orch/editorial/PROMPT_HISTORY.md; books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/editorial/QUALITY_GATES.md

## Output artifacts

books/inside-orch/editorial/TOC.md; books/inside-orch/editorial/CHAPTER_CONTRACTS.md; books/inside-orch/validation/intake/toc-coverage.json

## Work to perform

Review all 40 chapters and six appendices against the original prompt corpus, implementation map and reader paths. Each chapter needs a distinct motivating problem, exact source targets, a concrete lab or analysis task and an explicit boundary. Ensure all 91 original prompts are covered without demanding one chapter per prompt. Design-only topics should explain decisions and gaps, not pretend to operate absent features.

Reorder only if necessary for prerequisites and retain stable chapter IDs or a documented migration map. The in-memory/runtime-composition boundary must appear early. Check that developers get source walkthroughs, operators get observable recovery procedures and architects get tradeoffs/invariants. Avoid duplicate explanations of authentication, events or lifecycle constants; point to their defining chapter and revisit only when behavior changes. Set word budgets to meet BOOK_SPEC without filler. Establish narrative continuity for the running case study and cross-reference placeholders that resolve to actual future chapter IDs. Record any deferred topics and why. Freeze the contract before writing the chapter prompts.

## Acceptance and evidence

Exactly 40 distinct chapters plus A–F; original prompt coverage complete; prerequisite order coherent; every chapter has specific books/inside-orch/evidence/lab/limits; no ornamental filler.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Canonical reading order

Write `books/inside-orch/manuscript/Book.txt` with exactly 47 relative entries: `00-preface.md`, the 40 `chapters/<slug>.md` entries from the outline in order, then six `appendices/<slug>.md` entries. Paths are relative to the manuscript directory and must resolve inside it with unique stems. The existing Modern CI selection helper rejects nested paths, so orch needs its own safe selection adapter rather than blindly reusing that function. Do not register unfinished paths in the live catalog.
