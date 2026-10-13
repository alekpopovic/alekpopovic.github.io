# 010. Establish immutable citations and a compact bibliography

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 009 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/commits.json; books/inside-orch/evidence/prompt-commit-map.json; books/inside-orch/editorial/SOURCE_POLICY.md

## Output artifacts

books/inside-orch/editorial/REFERENCES.md; books/inside-orch/validation/intake/reference-register.json

## Work to perform

Define source references for exact code excerpts, historical implementation commits, original prompts, design documents, tests and external documentation. Use full-SHA GitHub blob/commit URLs; include line anchors for excerpts and preserve the SHA that actually contains historical code. Avoid moving main/latest references for facts that must be reproducible. Record retrieval dates for external versioned primary sources.

Build a bibliography only for material the book actually uses. Primary sources may include Go language/runtime documentation, Docker Engine API, PostgreSQL transaction/locking documentation, HTTP specifications, Prometheus guidance and relevant security standards. Retrieve them before making precise external claims. Do not fabricate DOI, ISBN, endpoint, issue or release links. Deduplicate references and give readable labels. A commit title is not a citation for an implementation detail unless the diff/source supports it. Specify how to cite an excerpt, a teaching adaptation and an inference differently. Add an offline navigation route through the bundled snapshot, prompt map and patch corpus when web links are unavailable.

## Acceptance and evidence

All repository SHAs resolve to known corpus objects; excerpt anchors match actual lines; external references are retrieved/primary; no fabricated attribution or moving source links.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
