# 016. Prepare author metadata and an explicit rights record

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 015 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

BOOK_SPEC.md; books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/orch/go.mod; books/inside-orch/publication/book-metadata.json

## Output artifacts

books/inside-orch/publication/RIGHTS.md; books/inside-orch/publication/NOTICE.md; books/inside-orch/publication/book-metadata.json

## Work to perform

Set author Aleksandar Popovic, website https://www.alekpopovic.com and the canonical title/subtitle from BOOK_SPEC. Record copyright and edition metadata consistently in Markdown, PDF, EPUB and site catalog outputs. This pack has not selected a public manuscript license or assigned a new license to the source repository.

Inspect actual repository license files and dependency notices. GitHub metadata reported no source license at baseline, so public availability alone does not justify an open-source designation. Separate original manuscript prose, exact source excerpts, adaptations, vector brand assets and third-party material. Retain provenance and required notices. If the intended public release license is still unspecified, keep the release licensing decision explicit and unresolved rather than guessing or copying another book's license. Do not fabricate ISBN, publisher approval or professional certifications. Record any external image/font rights used by generated publication assets. Keep the narrative free from workflow instructions while preserving a transparent technical provenance appendix.

## Acceptance and evidence

Author/title metadata consistent; no invented public license/ISBN; all reused materials have provenance; unresolved rights decisions remain clearly recorded for release.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Canonical metadata and license page

Write and synchronize `books/inside-orch/book.json` as the site's canonical metadata source, not only the companion publication JSON. The new catalog entry requires truthful metadata.publication_notes or a source LICENSE.md for its license page. Do not copy Modern CI's CC BY/MIT claims, hardcoded title, edition date or cover into orch. Preserve the explicitly selected rights and author attribution.
