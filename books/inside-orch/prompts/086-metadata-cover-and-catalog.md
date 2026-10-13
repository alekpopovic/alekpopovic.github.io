# 086. Create final metadata, cover and catalog material

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 085 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/RIGHTS.md; books/inside-orch/publication/book-metadata.json; books/inside-orch/manuscript/

## Output artifacts

books/inside-orch/publication/cover.svg; books/inside-orch/publication/cover.png; books/inside-orch/publication/catalog.json; books/inside-orch/publication/catalog-copy.md

## Work to perform

Create a publication cover from the existing orch vector identity and final title/subtitle. Use author Aleksandar Popovic consistently. Produce scalable SVG and a high-resolution export with verified aspect ratio and text legibility; inspect the result at cover and catalog-card sizes. Keep precise architecture diagrams outside decorative cover art. Derive all blurbs from completed chapters and validated capabilities.

Write a short catalog description, extended overview, learning outcomes, audience, prerequisites, reader paths and transparent edition/source metadata. Describe the book as a code-based engineering study of orch, including its current executable boundaries, not as a turnkey production HA platform. Populate real chapter/appendix counts, measured manuscript word count, actual lab status, source SHA and generated format paths. Never invent endorsements, bestseller status, ISBN, page count or review scores. Verify rights/attribution records and avoid relabeling source licensing. Include accessible alt text and short social metadata. The website can later use these assets through an adapter based on its real code.

## Acceptance and evidence

Cover visually checked; copy matches finished manuscript and real lab status; metadata measured; author/rights/source edition consistent; no unsupported marketing claims.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Final native metadata synchronization

Synchronize the final measured and reviewed edition metadata to canonical `books/inside-orch/book.json`, which scripts/book_catalog.py loads. Keep publication/book-metadata.json and catalog copy consistent with it. Replace planned/generation_pack status only when manuscript and required validations justify the final edition; do not leave a planned edition label in the release catalog or falsely mark incomplete work published. Preserve author, English language, source SHA, actual date, description and truthful rights.
