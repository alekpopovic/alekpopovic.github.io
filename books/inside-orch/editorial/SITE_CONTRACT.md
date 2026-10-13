# Site-native book authoring contract

Read-only source review at [`80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`](https://github.com/alekpopovic/alekpopovic.github.io/commit/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0), UTC 2026-10-12T23:54:17.809499+00:00. No site or pack changes; no build/test commands executed by this reviewer.

## Execution scope for all 100 prompts

The target is the existing Jekyll/Tailwind website repository, not a standalone book repository. Keep the site root as execution directory. Define `SITE` as that checkout root and `BOOK` as `SITE/books/inside-orch` (recommended stable book id: `inside-orch`). Book-relative prompt paths, state, editorial records, source corpus, manuscript, labs, examples, validation and editions must resolve under BOOK. Shared-site edits must explicitly resolve under SITE.

Read `SITE/AGENTS.md` first, then `BOOK/AGENTS.md` once created. Never overwrite the site's AGENTS.md, README.md, scripts, package.json or existing books with the former pack root. Nested helpers can retain their relative root calculations but must be invoked from SITE as `python3 books/inside-orch/scripts/verify_pack.py`, etc. A book task must not accidentally create root manuscript/, evidence/ or state/.

The repository's root AGENTS does not prescribe commit/push after each task. Its publication constraints and workflow must be honored; the original orch application's add/commit/push rule remains source evidence, not a mandate for site edits. The new user instruction establishes the target repository; it does not turn every authoring step into an automatic production deployment.

## Canonical and generated paths

| Purpose | Actual convention |
| --- | --- |
| Canonical book source, publisher, metadata, rights, examples and reports | `books/<package>/` |
| Registration and source adapter | `scripts/book_catalog.py` |
| Shared website builder | `scripts/build-books.py` (hyphens, not build_books.py) |
| Generated reading pages | `book-pages/<book-id>/` |
| Public URLs | `/books/<book-id>/`, section URLs `/books/<book-id>/<source-stem>.html` |
| Generated downloads/covers/license copies | `assets/books/<book-id>/` |
| Generated shared catalog | `_data/books.json` |
| Editorial book notes | `_posts/YYYY-MM-DD-<slug>.md` |
| Canonical linked glossary | `_data/glossary.yml` |
| User-visible update entry | `_data/updates.yml` |
| Shared reader/overview/post layouts | `_layouts/book.html`, `_layouts/book-overview.html`, `_layouts/post.html`, all nested in `default` |
| Production output | `_site/` |
| Development output | `_site-dev/` |

There is **no `_data/books.yml`**. `_data/books.json`, all book-pages/, all assets/books/ and build outputs are ignored by .gitignore and rebuilt. Keep canonical manuscripts and locally generated full editions under BOOK in Git, following README conventions. `_config.yml` enumerates canonical book folders in its exclude list: add `books/inside-orch` so corpus/prompts/validation never leak as static public files. Generated reading pages remain outside that excluded directory and publish through their permalinks.

## Catalog record schema

`scripts/book_catalog.py::catalog()` returns source records, not simple front matter. Required fields consumed by the builder/checker:

- `id`: stable URL/catalog id, recommended `inside-orch`.
- `source`: resolved canonical BOOK Path.
- `output`: SITE/book-pages/inside-orch.
- `files`: SITE/assets/books/inside-orch.
- `files_url`: `/assets/books/inside-orch`.
- `metadata`: title, subtitle, author, edition, language (`en`), description. Brand and language_label/edition_label should be explicit for coherent reader presentation.
- `paths`: ordered list of actual manuscript Paths with unique stems, contained by source.
- `editions`: directory containing the complete canonical PDF/EPUB.
- `filename`: export basename, recommended `inside-orch`.
- `chapter_group`: `Chapters`; `chapter_label`: `Chapter`.
- `licenses`: truthful source license filenames; an empty list is allowed only with accurate publication notes.

Useful optional fields: `cover` as source-relative asset path; metadata.cover_image as its public absolute path; metadata.license_note/license_url/text_license only where actual rights exist; metadata.publication_notes for the required license/attribution page; `epub_chapters` for exact source-stem → EPUB document-name lists; `epub_offset` only if using the site's default numbering convention.

Metadata must preserve author Aleksandar Popovic, title Inside orch, subtitle Building and Operating a Docker Orchestrator in Go, source pins and actual rights. The builder requires either metadata.publication_notes or BOOK/LICENSE.md even when the license-file list is empty. Do not copy another book's CC/MIT labels or license allocation automatically.

## Reading order and heading grammar

The first source item is always classified Preface by `section()`. To publish 40 chapters and six appendices correctly, put a substantive `00-preface.md` first: **47 reading sections** in order, with 40 numbered chapters and six appendices. Keep all stems unique even if source files live in nested folders.

The parser currently recognizes chapter titles only with `^(?:Chapter )?(\d+)(?:\.| -)` and appendices only with `^(?:Appendix|Dodatak) ([A-Z])(?:\.| -)`. Use H1 forms such as `# Chapter 1 - Why Build a Container Orchestrator?` and `# Appendix A - CLI, API, and Configuration Reference`. Colon or em-dash heading forms are not recognized by this parser and would corrupt chapter grouping/post coverage. Either follow current grammar or make an additive, tested parser change; do not assume broad Markdown title support.

Modern CI's selection() reads a Book.txt but disallows nested entry parents. The old book pack uses manuscript/chapters and manuscript/appendices, so write a proper orch selection adapter with bounded paths rather than blindly calling Modern CI's selection(). Source filenames become public slugs, so establish them before posts/bookmarks/cross-references. Canonical Markdown need not include Jekyll front matter; the shared builder supplies generated YAML and wraps rendered content in Liquid raw tags to protect code examples.

## Actual build integration points and traps

1. Register orch in scripts/book_catalog.py and implement its metadata, selection, title, render and local-reference handling deliberately.
2. `scripts/build-books.py::main()` explicitly rebuilds Modern CI PDF/EPUB and Secret Contract Operator, then loops the catalog. Merely adding a catalog item does not create orch editions. Add an orch publisher invocation or a documented source-consistency gate for supplied complete exports.
3. Current render()/local_references() and companion-copy logic contain hardcoded book-id branches. Nested source links to solutions, labs, diagrams and evidence need an orch adapter/branch using the bounded public_reference behavior. Default Modern CI rendering just changes .md suffixes and may leave nested paths incompatible with flattened reading URLs.
4. The shared builder copies PDF/EPUB to generated public downloads; it does not manufacture complete editions from every source record. Preserve old books and avoid making full-site builds depend on incomplete new drafts. Register a public complete edition only when its inputs exist and pass book gates.
5. `scripts/check-books.py` expects EPUB/{stem}.xhtml only for modern-ci; other ids default to EPUB/text/ch001.xhtml onward, plus optional offset. Set an explicit epub_chapters map for orch if its publisher uses another layout. The checker compares body text with full rendered source, not just the existence of spine items.
6. A configured `cover` must be copied correctly and EPUB must currently contain identical `EPUB/media/cover.png` bytes. Check the actual EPUB adapter rather than bypassing this assertion. PDF author metadata and all chapter titles are checked; public PDF/EPUB bytes must equal canonical editions.
7. Do not weaken check-books.py, leak source packages, publish excerpts as full chapters or relabel pending labs as complete to make an integration green.

## Required posts and glossary

Root AGENTS requires **at least three original substantive posts covering three different numbered chapters** in the same new-book change. Write independent practical explanations/scenarios, not copied chapter text or placeholder summaries. Front matter must include layout: post, title, description, category, book_id: inside-orch, chapter_slug: an exact real source stem, illustration, tags. Reuse an existing category where it fits. Allowed illustrations: clock, queue, shield, network, package, logs. Posts are canonical editorial sources; ordinary book builds must never overwrite them.

The post layout automatically links to the chapter and creates related-note links. The chapter layout links reciprocally. check-books.py rejects unknown books/slugs, missing chapter links and fewer than three distinct numbered chapter references.

`npm run check:site` requires glossary keys to equal catalog book ids exactly. Add inside-orch to `_data/glossary.yml` with at least three substantive terms, each containing term, definition and chapter matching a real published slug. This is a hard gate, not optional polish. Add a stable entry to `_data/updates.yml` for the visible book; use explicit editorial dates, with Europe/Belgrade as the site's timezone. Builds must not advance reviewed/modification dates automatically.

## Local dependencies and command sequence

README installation commands:

```sh
bundle install
npm install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-books.txt
```

Root verification sequence:

```sh
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
npm run check:site
npm run check:content
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`npm run build` executes build:books, build:labs, build:assets and build:css. `build:books` is python3 scripts/build-books.py and reexecutes into .venv when present. Styling-only builds can use npm run build:css. npm run dev serves _site-dev; production checks intentionally read _site.

For shared layout/browser changes, also run npm run test:ui and npm run check:performance; retain no-JavaScript/mobile/keyboard/search/book/category filters, storage-failure behavior, notes/export/offline semantics. Browser install is `npx playwright install --with-deps chromium firefox webkit`; CI uses pinned Playwright browsers, not arbitrary local Chrome.

The GitHub Pages workflow uses Ruby 3.3, Node 22 and Python 3.12, installs Cairo/Pango/HarfBuzz/DejaVu system libraries and Python requirements, validates books and source publications, builds Jekyll, runs book/site/content/workshop/Python/browser/performance checks, then deploys only non-PR builds. A push to main therefore triggers production deployment. Branch-based Pages cannot run the Python publisher/custom plugin; Actions is the required publication mode.

## Interaction and publication constraints

Preserve the existing visual language, shared includes and `_layouts/default.html`. New pages inherit exactly one configured Google tag through the shared default layout; do not hardcode analytics IDs or add duplicate snippets. `_config.yml` production origin is https://www.alekpopovic.com with empty baseurl. Canonical/social/schema/feed/search/offline generation is handled by `_plugins/site_features.rb`; use shared metadata rather than duplicating it. Analytics must not receive reader note text, selected text, searches or contact values.

Keep all current books, posts, projects, AI library, learning paths and reader behavior intact. Ordinary builds must use local fonts/assets without network fetches. Shared conditional JavaScript has a 65 KB/page limit and CSS 130 KB/page limit. Source-only authoring should not alter shared layouts unnecessarily. Final publishing should be a concrete reviewed diff/build artifact and a deliberate authorized action, since main pushes auto-deploy.

## Immutable source references

- [Site project rules](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/AGENTS.md)
- [Local/build/publication workflow](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/README.md)
- [Canonical catalog adapters](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/scripts/book_catalog.py)
- [Shared edition/reader builder](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/scripts/build-books.py)
- [Complete book/post/download validation](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/scripts/check-books.py)
- [Glossary and source metadata gates](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/scripts/check-site.py)
- [Git ignore boundaries](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/.gitignore)
- [Pages CI and production deploy](https://github.com/alekpopovic/alekpopovic.github.io/blob/80801c8d3d97a4d8ff78e0fe69f3f902beda00c0/.github/workflows/pages.yml)

This review establishes the inspected site's actual authoring/build contract; it does not claim these commands ran or that the new book already exists.
