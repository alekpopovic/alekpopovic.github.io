# Execute from the website repository root

**Target repository:** https://github.com/alekpopovic/alekpopovic.github.io  
**Inspected site SHA:** `80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`  
**SITE:** repository root  
**BOOK:** `books/inside-orch`  
**Book ID:** `inside-orch`  
**Reader URL:** `/books/inside-orch/`

Install this package beneath BOOK. Never copy its AGENTS.md, README.md or scripts over the site's root files. Open SITE in Codex and execute `books/inside-orch/prompts/000-workspace-and-baseline.md`, followed by the numbered tasks. Read both SITE/AGENTS.md and BOOK/AGENTS.md. Reinspect the actual working repository if it has changed since the inspected SHA; do not reset or overwrite user work to match the lock.

## Path ownership

| Path | Owner and behavior |
| --- | --- |
| `books/inside-orch/book.json` | Canonical author/title/edition/language metadata |
| `books/inside-orch/manuscript/Book.txt` | Exact 47-section reading order; paths relative to manuscript/ |
| `books/inside-orch/manuscript/00-preface.md` | First section, authored in prompt 019 |
| `books/inside-orch/manuscript/chapters/` | Forty canonical numbered chapters |
| `books/inside-orch/manuscript/appendices/` | Six canonical appendices |
| `books/inside-orch/scripts/` | Book-specific helpers and new publisher |
| `books/inside-orch/{editorial,evidence,examples,labs,validation,state,publication,dist}/` | Book source, research, teaching code and canonical exports |
| `scripts/book_catalog.py` | Root registry/adapters; add an orch entry without replacing existing books |
| `scripts/build-books.py` | Root orchestrator; explicitly invoke the new orch publisher before copying exports |
| `_posts/` | Three or more original substantive editorial source posts, committed with final integration |
| `_data/glossary.yml` | Add inside-orch terms with real chapter slugs; preserve existing glossary entries |
| `_data/updates.yml` | Stable entry for the visible book change |
| `_config.yml` | Exclude books/inside-orch from raw Jekyll static copying; retain origin/configuration |
| `book-pages/inside-orch/` | Generated reader pages; ignored; never author or force-add |
| `assets/books/inside-orch/` | Generated public files/downloads; ignored; never author or force-add |
| `_data/books.json` | Generated catalog; ignored; never hand-maintain |

The Python tools resolve package-relative JSON fields from BOOK internally. Prompt instructions show site-root artifact paths explicitly. Upstream orch source paths are relative to BOOK/evidence/orch. For Go/Docker/PostgreSQL experiments, make a disposable source checkout/copy outside canonical website content and record its working directory. Do not run `go build ./...` in the Jekyll root.

## Native publishing constraints

The current catalog is `scripts/book_catalog.py`, not a YAML catalog. A catalog source record needs id, source, output, files/files_url, metadata, paths, editions, filename, chapter_group/chapter_label and truthful licenses/attribution. Canonical exports are BOOK/dist/inside-orch.pdf and .epub; public download copies are `/assets/books/inside-orch/downloads/inside-orch.pdf` and .epub.

There are 47 reader sections: preface, 40 chapters, six appendices. The native classifier always treats index zero as the preface. Numbered H1 must match `# Chapter 1 - Title` or `# 1. Title`. Appendix H1 must match `# Appendix A - Title`. A colon or em dash after the number does not meet the inspected classifier. Keep canonical Markdown plain; do not display YAML metadata in book content.

The Modern CI selection helper rejects nested paths. Orch's own selection must safely allow `chapters/` and `appendices/` beneath manuscript/, reject path escapes and duplicate stems, and preserve Book.txt order. Do not reuse its hardcoded cover/title/licenses. The root build currently calls only certain publishers explicitly: catalog registration alone does not regenerate orch editions. Add the orch publisher call in the source orchestrator.

Implement exact local-reference rewriting, companion traversal/copying and stable heading IDs for orch. Existing adapter branches are book-specific. All links must resolve inside BOOK or be explicitly external; do not expose the research/prompt corpus merely because it is installed. An explicit `epub_chapters` map is necessary when EPUB uses source-stem filenames, since the generic check guesses EPUB/text/chNNN.xhtml. The cover check expects exact configured cover bytes in `EPUB/media/cover.png`. The licensing page needs truthful publication_notes or LICENSE.md. No public license is inferred from the application being on GitHub.

## Required editorial integration

The new book must ship with at least three original substantive posts covering different numbered chapters. Front matter requires layout: post, title, description, category, book_id: inside-orch, chapter_slug, illustration and tags. Illustrations: clock, queue, shield, network, package, logs. Reuse fitting existing categories. Prepared companion drafts are included under BOOK/publication/site-adapter/prepared-posts/; prompt 093 verifies them against completed chapters before copying them to _posts/. They are not generated or overwritten by normal book builds.

Add at least three substantive terms under inside-orch in `_data/glossary.yml`, each with term, definition and a real chapter slug. check-site requires glossary keys to exactly match catalog IDs. Add a stable `_data/updates.yml` entry. Keep new catalog registration, posts and glossary coherent in one integration change; do not run a release check against half of that change.

## Required verification

From SITE:

```bash
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
npm run check:site
npm run check:content
```

CI uses its configured Python when .venv is absent. For shared layout/browser changes, also run `npm run test:ui` and `npm run check:performance`, including existing compatibility suites as applicable. Preserve source-completeness, EPUB spine/content/cover, local-link, PDF/download and post-coverage checks. Never weaken them to pass an incomplete book.

Preserve shared layouts, analytics configuration, local-note privacy, storage-failure handling, keyboard/no-JavaScript reading, responsive covers, search/feed/sitemap and opt-in per-section offline saving. Do not precache whole books or PDF/EPUB downloads. The production origin stays https://www.alekpopovic.com. No replacement website or hosting migration is part of this task.

## Publication boundary

The current Pages workflow deploys after a push to main; pull-request builds do not deploy. Work on a separate branch and make a reviewable complete result. A request to generate this pack does not authorize a push to the website's default branch. Publish only when the current task separately authorizes it, then verify the expected revision and actual public chapters/download signatures through the existing post-deploy checks.
