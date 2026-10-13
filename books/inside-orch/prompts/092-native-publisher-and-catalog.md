# 092. Wire the orch publisher and source catalog into the existing build

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

The target repository is already identified: alekpopovic/alekpopovic.github.io, inspected SHA 80801c8d3d97a4d8ff78e0fe69f3f902beda00c0. Reinspect current root AGENTS.md and actual sources; reconcile changes since that SHA without resetting the user branch. Use SITE_WORKSPACE.md and editorial/SITE_CONTRACT.md. This task integrates a native book, not a replacement site.

Add the new source record to scripts/book_catalog.py with id inside-orch; source ROOT/books/inside-orch; output ROOT/book-pages/inside-orch; files ROOT/assets/books/inside-orch; files_url /assets/books/inside-orch; metadata loaded from books/inside-orch/book.json; paths from safe books/inside-orch/manuscript/Book.txt selection; editions books/inside-orch/dist; filename inside-orch; chapter_group Chapters and chapter_label Chapter. Include truthful cover and licensing metadata and the explicit epub_chapters map. Configure cover bytes consistently between the catalog asset and EPUB/media/cover.png. The licensing page needs publication_notes or a real LICENSE.md; do not copy another book's public license claims.

Wire the actual orch publication build into scripts/build-books.py before its catalog copy loop. Registration alone cannot regenerate exports: current main explicitly calls only selected existing publishers. Import the new module safely without depending on current working directory or accidental mutable globals. Generate inside-orch.md, .pdf and .epub from the same complete 47-section canonical manuscript. Do not overwrite Modern CI, AgentPlane, LogBranik, Secret Contract Operator or Universal Tracking exports. Preserve and extend root renderer/companion-copy handling for orch based on prompt 091's adapter and concrete tests.

Confirm books/inside-orch is excluded in _config.yml so raw source/prompts are not copied by Jekyll. Preserve production origin, analytics and existing excludes. Keep book-pages/, assets/books/ and _data/books.json ignored. Canonical manuscript, scripts, metadata, final exports and meaningful validation records belong in books/inside-orch and Git. Generated public copies must not be force-added.

Prepare three chapter post drafts and the inside-orch glossary/update changes for the next task. Do not treat a half-completed registration as a release-ready site: all these source changes must be coherent before the full publication gate in 093. Run book-specific publisher/adapter checks and source exports with available toolchains. Verify 47 sections, 40 numbered chapters and 6 appendices, manifest paths, PDF/EPUB signatures, canonical/export consistency, license page inputs and existing-book preservation. Record actual commands, versions, outcomes and blockers under books/inside-orch/validation/publication/. Add focused tests for the new path; never weaken global completeness checks. Update the tracker and leave a concrete reviewable branch result. No main-branch push or deployment is authorized by this prompt.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.
