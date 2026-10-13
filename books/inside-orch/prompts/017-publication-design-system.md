# 017. Define a readable multi-format book design

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 016 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/BRAND.md; books/inside-orch/evidence/orch/docs/assets/; books/inside-orch/editorial/book-outline.json; books/inside-orch/publication/book-metadata.json

## Output artifacts

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/style-tokens.json

## Work to perform

Derive the visual identity from orch's existing orbit-and-node vector assets and documented cyan/blue/violet/slate palette. Create a restrained technical-book system for cover, chapter openers, source listings, evidence callouts, tables and diagrams. Preserve long-form readability: generous margins, legible body type, contrasting code panels, accessible links and printable grayscale distinctions.

Define separate print PDF, reflowable EPUB and responsive online-reader rules. Code must not be shrunk to unreadability or clipped; long lines require editorial selection, wrapping that preserves meaning, or a downloadable listing. Tables need repeated headers and may require a different layout on small screens. Give diagrams semantic labels and text alternatives. Keep vectors exact and avoid generated raster diagrams for precise topology. Plan front matter, contents, numbering, bookmarks and cross-reference labels. Review current site catalog/reader conventions before proposing a site-specific adapter; the visible site is not evidence that WordPress is used. Produce a small style specimen and describe how visual QA will be executed.

## Acceptance and evidence

Design tokens trace existing brand; body/code contrast readable; print/reflow/online rules distinct; diagrams accessible; no unverified site technology assumed.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
