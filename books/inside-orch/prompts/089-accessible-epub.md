# 089. Build an accessible reflowable EPUB edition

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 088 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/manuscript/; books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/cover.png; books/inside-orch/editorial/REFERENCES.md

## Output artifacts

books/inside-orch/dist/inside-orch.epub; books/inside-orch/publication/epub-build/; books/inside-orch/validation/publication/epub-build.json

## Work to perform

Create a reflowable EPUB from the same ordered manuscript as the PDF. Include correct title/author/language/identifier/version metadata, cover designation, a linked navigation document, landmarks, chapter files and bibliography. Use semantic headings, meaningful link labels, figure text alternatives and table captions/headers. Keep reading order independent of decorative styling.

Code blocks must remain usable on narrow screens: consider horizontal scrolling, safe wrapping or downloadable complete listings, while preserving code meaning and indentation. Avoid fixed page numbers as the sole cross-reference; use chapter/section links. Convert exact diagrams to supported images plus accessible descriptions where a reader cannot render Mermaid. Package only required fonts/images with known rights; avoid large redundant assets. Test light/dark theme contrast and scalable type. Record tool versions, input hashes and output manifest. Do not declare validation complete because the ZIP container is readable; the next task verifies EPUB structure and reader behavior.

## Acceptance and evidence

EPUB content matches canonical manuscript; metadata/nav/reading order correct; code/tables/figures accessible; build inputs and rights recorded; validation pending explicit next gate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Native EPUB contract

Record an explicit `epub_chapters` map for all 47 source stems when EPUB files use stem names. check-books otherwise guesses EPUB/text/chNNN.xhtml for new IDs. Package the exact catalog cover bytes at `EPUB/media/cover.png`, as required by the native cover check. Cross-section links and identifiers must be stable and source-derived.
