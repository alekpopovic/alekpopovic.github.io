# 091. Implement the native Jekyll reader adapter

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Read scripts/book_catalog.py, scripts/build-books.py, scripts/check-books.py, _layouts/book.html, _layouts/book-overview.html and _plugins/site_features.rb. Read books/inside-orch/editorial/SITE_CONTRACT.md and books/inside-orch/manuscript/Book.txt. SITE is the repository root and BOOK is books/inside-orch. The complete reading order is 47 sections, beginning with a real preface. Do not create an unrelated static website or replace the existing reader.

Implement an orch-specific source adapter for metadata, safe nested selection, title/section classification, stable heading IDs, rendering, source-relative local reference rewriting, companion traversal and asset copying. Source paths may be nested under manuscript/chapters and manuscript/appendices; reject path escapes and duplicate stems. The Modern CI selection function requires direct child files, and its renderer has book-specific assumptions. Reuse only demonstrated compatible primitives. First H1s must match the inspected Chapter N - Title / Appendix A - Title grammar; index zero is Preface.

Preserve the native book, book-overview and book-license layouts. Code listings containing Liquid syntax must remain protected through build-books.write_page rather than being evaluated as templates. Reader URLs are /books/inside-orch/<source-stem>.html, public files /assets/books/inside-orch/, and downloads /assets/books/inside-orch/downloads/inside-orch.pdf and .epub. Exact source/commit links stay external immutable URLs. Resolve manuscript and companion links against their source parent and safely translate them to actual reader/companion/public-file addresses. Copy only referenced companion files; never publish the prompt corpus, entire research snapshot or private execution logs implicitly.

Add focused adapter tests for nested paths, renamed historical links, fragments, duplicate headings, companion documents, escaped paths and unsupported files. Keep an explicit epub_chapters map matching the generated EPUB rather than accepting the generic new-book chNNN guess. Record an interface/export manifest in books/inside-orch/publication/site-adapter/adapter-contract.json and actual test logs under books/inside-orch/validation/publication/. Tests can exercise the adapter directly before adding the catalog entry in prompt 092. Do not hand-author generated book-pages or _data/books.json.

Acceptance: all 47 source paths recognized in exact order, chapter/appendix counts correct, titles and slugs stable, local links round-trip to native addresses, referenced assets bounded to BOOK, and no raw workflow content exposed. Report actual executed tests and missing prerequisites. Update books/inside-orch/state/execution-tracker.csv for 091 with concrete evidence. Keep the implementation in books/inside-orch/scripts and a reviewable minimal native adapter patch; preserve existing books and do not publish live.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.
