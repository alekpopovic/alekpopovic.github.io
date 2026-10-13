# 088. Render and inspect the actual final PDF

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 087 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/publication/pdf-build/; books/inside-orch/publication/DESIGN_SYSTEM.md

## Output artifacts

books/inside-orch/validation/publication/pdf-visual-review.md; books/inside-orch/validation/publication/pdf-pages.json

## Work to perform

Render the PDF to page images using available standard tools. Inspect cover, contents, every chapter/appendix opener, pages with tables/figures/code, and page endings; review every page at a legible resolution or systematically inspect all-page contact sheets followed by full-size suspect pages. Record page numbers checked and exact defects. Automated text extraction alone cannot establish visual correctness.

Check clipping, overlap, font substitutions, missing symbols, poor contrast, tiny listings, blank pages, inconsistent running headers, widows/orphans and broken table continuation. Test PDF links and bookmarks against the source/reference register. Compare selected extracted text with canonical Markdown to detect missing sections. Fix the typesetting source, rebuild and rerender affected pages and their neighbors; do not patch the PDF as the canonical manuscript. Record measured page count only after the final build. Keep internal screenshots as QA artifacts unless the user explicitly requests them as deliverables. Finish with a clear pass/fail list and actual evidence, not a generic assurance.

## Acceptance and evidence

All-page inspection coverage recorded; final rendered pages free of defects; links/bookmarks/contents correct; extracted content matches; measured page count and artifact hash captured.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
