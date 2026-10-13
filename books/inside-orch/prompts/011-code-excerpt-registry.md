# 011. Select and lock the book’s source listings

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 010 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/examples/source-excerpts/registry.json; books/inside-orch/scripts/extract_snippets.py; books/inside-orch/evidence/orch/; books/inside-orch/editorial/book-outline.json

## Output artifacts

books/inside-orch/examples/source-excerpts/registry.json; books/inside-orch/validation/intake/excerpt-review.md

## Work to perform

Review the supplied excerpt seeds and extend them chapter by chapter. Choose coherent units: a constructor path, a lifecycle guard, atomic assignment, Docker adoption, rollout calculation, namespace context, policy decision or error boundary. Record exact file, line interval, source SHA, checksum, symbol and teaching purpose. Use books/inside-orch/scripts/extract_snippets.py to regenerate listings from immutable bytes rather than copying code manually.

Keep listings short enough to read, with necessary surrounding context explained in prose. If unrelated lines are omitted, mark the omission as editorial and do not present the result as an exact contiguous excerpt. Do not change identifiers or silently fix a source listing. A simplified or adapted example belongs in teaching-extensions with its own tests and attribution. Avoid embedding actual secrets, tokens or personal metadata. Add companion source links with line ranges and an explanation of how the excerpt participates in the executable. Check that source examples featuring a standalone library do not imply server integration. Give every listing a stable ID for later PDF/HTML/EPUB cross-references.

## Acceptance and evidence

Listings are byte-derived and pinned; checksums match; purpose and runtime scope are documented; adapted code is separately labeled and testable.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
