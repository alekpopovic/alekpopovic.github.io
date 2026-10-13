# 093. Ship three original posts, glossary and updates with the native book

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Complete the source integration for inside-orch using the existing Jekyll/Tailwind reader. Read root AGENTS.md, _data/glossary.yml, _data/updates.yml, existing _posts front matter, scripts/check-books.py and scripts/check-site.py. Preserve shared includes and existing categories. All47 canonical sections and final PDF/EPUB exports must exist; a partial manuscript is not an edition.

Review the three prepared original posts under books/inside-orch/publication/site-adapter/prepared-posts/ against the now-completed chapters and actual source. Their topics are service resource propagation (Chapter05), default-server state/readiness (Chapter06), and partition/fencing limits (Chapter19). Revise to stand alone as substantive worked explanations; never copy chapter paragraphs or replace them with marketing summaries. Copy verified editorial sources into _posts/ with publication dates chosen at the actual release, stable filenames and required fields layout:post, title, description, category, book_id:inside-orch, real chapter_slug, allowed illustration and tags. Ordinary book builds must never regenerate these posts.

Add inside-orch to _data/glossary.yml with at least three useful definitions linked to real chapter slugs. The native check requires glossary keys to exactly match the catalog. Preserve all existing entries. Add a stable _data/updates.yml entry for the visible book change and accurate editorial dates. Extend a relevant learning path only when it has a real exercise and observable evidence; do not invent completed progress. Keep source IDs stable for bookmarks and backups.

From SITE run npm run build, then bundle exec jekyll build, then .venv/bin/python scripts/check-books.py (or configured CI Python). Run npm run check:site and npm run check:content. For shared/browser changes run npm run test:ui and npm run check:performance with the existing relevant compatibility checks. Missing dependencies are concrete blockers, not invented passes. Validate all 47 online sections, 40 chapter/6 appendix counts, native previous/next navigation, contents, code, companion links, three distinct numbered-chapter post links, reciprocal notes, glossary, search/feed/sitemap and full downloads. Compare PDF/EPUB/site text with canonical source and exact final hashes.

Confirm generated paths remain ignored and no raw workflow/evidence files leaked into _site. Produce books/inside-orch/publication/site-adapter/changes.patch, a source/generated file manifest and books/inside-orch/validation/publication/site-build.md with actual command logs. Inspect git status and stage only relevant canonical changes in the selected branch if committing. Do not push main or deploy. Acceptance is a complete, locally verified integration preserving existing books, not merely a new catalog card. Update the tracker with actual evidence and unresolved issues.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.
