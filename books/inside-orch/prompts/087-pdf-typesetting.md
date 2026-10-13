# 087. Build a navigable print-quality PDF

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 086 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/manuscript/; books/inside-orch/examples/source-excerpts/; books/inside-orch/publication/cover.svg

## Output artifacts

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/publication/pdf-build/; books/inside-orch/validation/publication/pdf-build.json

## Work to perform

Assemble chapters and appendices from the canonical manifest order, excluding prompt workflow material and internal review notes. Choose available standard publishing tools and record versions and fonts. Build cover, title/rights pages, reader guidance, linked contents, bookmarks, numbered headings, code listings, figures and bibliography. Give chapter openers deliberate spacing and consistent headers/footers.

Ensure code, table and source-link layouts remain readable. Prefer short source-link labels with working PDF hyperlinks over printing 40-character URLs in every paragraph. Keep long listings in downloadable examples and avoid tiny fonts. Prevent headings orphaned at page bottoms, tables clipping the margin, overlapping text and broken glyphs. Export deterministic metadata and record the books/inside-orch/manuscript/source hashes used. Do not declare the PDF publication-ready before the next visual inspection task. Keep the build configuration with the manuscript so the edition can be regenerated rather than manually edited page by page.

## Acceptance and evidence

PDF contains complete canonical content, navigation and author metadata; build reproducible; no unresolved references; visual QA remains a separate required gate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Native publisher integration requirement

Implement `books/inside-orch/scripts/build.py` with metadata, safe nested selection, assemble, PDF, EPUB and explicit build entrypoints. Use available local dependencies and keep formats derived from one canonical 47-section manuscript. Reuse shared parsing primitives only after inspecting assumptions; never inherit Modern CI's hardcoded title, licenses or cover text. The native site build will call this publisher explicitly in prompt 092.
