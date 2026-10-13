# 094. Verify native discovery, accessibility and publication behavior

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Review the complete built inside-orch edition in the existing site. Use actual _site output, native reader layouts, scripts/check-site.py, scripts/check-publication.py, package.json and root AGENTS.md. Canonical origin remains https://www.alekpopovic.com and book URLs /books/inside-orch/. Preserve current analytics configuration and exactly-one-tag behavior; never expose notes, selected text, search queries or contact values to tracking.

Verify landing/47section metadata, canonical URLs, author/title/source edition, accurate structured book data, social covers, search full text, feed, sitemap and post/chapter reciprocal links. Do not invent ISBN, reviews, page counts or ratings. Test PDF/EPUB download signatures and compare public copies to reviewed canonical books/inside-orch/dist files. Verify removed or nonexistent paths stay true404s; do not add catchall rewrites. The current post-deploy checker can be prepared locally without claiming a live check before deployment.

Review keyboard navigation, focus visibility, chapter selection, contents, copy-code controls, tables, heading hierarchy, image alternatives, source links, mobile layouts and no-JavaScript reading. Check reading progress, bookmarks, note export and versioned backups including storage failure. Existing IDs/URLs of other books must be unchanged. Retain local fonts/assets; ordinary builds should not fetch network assets. Use the native shared Google tag/layout conventions on any new rendered HTML.

Offline saving stays opt-in per section; do not precache whole orch chapters or PDF/EPUB files. Confirm local manifests contain correct asset versions and the worker preserves genuine network404s. If an offline downloadable ZIP is provided, it is an explicit download rather than a silent service-worker preload. Preserve CSS/conditional-JavaScript budgets from rootAGENTS and relevant browser/performance suites. Do not add analytics widgets or redesign shared navigation for this book.

Run npm run check:site and npm run check:content; run applicable Playwright tests and npm run check:performance after shared/browser changes. Record exact tested browsers, viewports, tool versions, timestamps and exit codes in books/inside-orch/validation/publication/site-quality.md and JSON. Automated audit scores complement manual reading checks. Fix defects in canonical source/build adapters, rebuild and retest affected outputs. Keep untested conditions explicit. Update books/inside-orch/state/execution-tracker.csv only when concrete acceptance is met. Leave a reviewable local integration; no publication action is implied.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.
