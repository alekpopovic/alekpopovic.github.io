# alekpopovic.github.io

Personal website for Aleksandar Popovic, built with Ruby, Jekyll, and Tailwind CSS.

## Local development

Install dependencies:

```sh
bundle install
npm install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-books.txt
```

Build the book editions, reading pages, and Tailwind:

```sh
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
```

Run the Jekyll server:

```sh
npm run dev
```

The development server writes `_site-dev/`; production builds and automated
checks use `_site/`, so live regeneration cannot overwrite test artifacts.

For active styling work, run Tailwind in a second terminal:

```sh
npm run watch
```

## Publishing to GitHub Pages

In the repository's **Settings → Pages → Build and deployment**, select
**GitHub Actions** as the source. `.github/workflows/pages.yml` builds the book
editions, generated reading pages, and assets, runs the publication and browser
checks, and deploys `_site/` after they pass.

The branch-based Pages builder cannot run the Python book publisher or the
custom Jekyll plugin. It can replace the complete site with a build that has
an empty book library and missing downloads. Use the Actions workflow as the
only publishing source.

For browser checks matching CI, install the Playwright-managed browsers:

```sh
npx playwright install --with-deps chromium firefox webkit
npm run test:ui
SITE_BROWSER=firefox npm run test:ui -- tests/compatibility.spec.js
SITE_BROWSER=webkit npm run test:ui -- tests/compatibility.spec.js
```

`CHROME_PATH` is an optional local browser override. CI uses Playwright's pinned
browser, so a pass with a different local Chrome version is not a CI reproduction.

## Books

`books/modern-ci-book/manuscript/` contains the canonical Modern CI text;
`Book.txt` defines the complete reading order. Edit those Markdown files and
`book.json`, then run `npm run build` again. The builder uses `.venv` automatically
when it exists. PDF export needs the Pango, HarfBuzz, and DejaVu font packages
listed in [the book build guide](books/modern-ci-book/publishing/BUILDING.md).

Generated reading pages live in `book-pages/modern-ci/`; downloads and licenses
are copied to `assets/books/modern-ci/`. Shared metadata lives in `_data/books.json`.
These generated files are ignored by Git and rebuilt by the Pages workflow.
The site provides a library at `/books/`, full contents at `/books/modern-ci/`,
and all 30 reading sections with previous/next navigation. Complete PDF and EPUB
files are available under `/assets/books/modern-ci/downloads/`.

Use `npm run build:css` for styling changes that do not change the manuscript.
The publication checks compare every online chapter and EPUB section with its
source, verify internal links, images and reference anchors, and check every PDF.

`books/logbranik/lessons/` contains **LogBranik / Nginx Log Security**. Its
`manuscript/Book.txt` defines the order of all 24 sections. The site publishes
the complete, supplied PDF and EPUB editions from `books/logbranik/output/`.
After editing lessons, regenerate those editions with the book's own
`tools/build_book.py` (see its publishing guide for ReportLab/Pandoc requirements)
before running `npm run build`; stale exports fail the completeness checks.
The reading pages are generated into `book-pages/logbranik/` with URLs under
`/books/logbranik/`. Its original cover, diagram, licenses, and full downloads
are copied to `assets/books/logbranik/`. These generated directories are ignored
by Git and recreated by the Pages workflow. All books appear in the library
and on the homepage; the reader preserves each book's chapter navigation.

`books/agentplane-book/book/book.json` defines **AgentPlane**: a preface,
28 chapters, four appendices and references (34 reading sections). The site
preserves the supplied editions in `dist/` and their contributor attribution.
After manuscript changes, follow `books/agentplane-book/BUILDING.md` to rebuild
the original exports. Its text/diagrams are CC BY-SA 4.0; code is MIT.
Reading URLs use `/books/agentplane/`.

Keep its `reports/VALIDATION.md` and `reports/BUILD_RESULTS.json` in Git:
the publication links to these supplied edition records. Only the root
`/reports/` directory contains ignored browser and performance output.

`books/Secret_Contract_Operator/chapters/` contains the **Secret Contract
Operator** English manuscript, ordered by numeric filename: a preface,
22 chapters and four appendices (27 reading sections). Its publisher at
`books/Secret_Contract_Operator/tools/build.py` regenerates English PDF, EPUB,
Markdown, cover and diagram assets during `npm run build`, using metadata from
`book.json`. Generated editions live in the package's `dist/` directory.
Original `_SR` files remain private reference material, excluded from Jekyll;
previous download addresses serve the new English edition. Reading URLs stay
under `/books/secret-contract-operator/`, including the original chapter slugs.
This package supplies no text/code license, so its publication notes do not
claim a Creative Commons or MIT grant.

`books/universal-tracking-technical-book/metadata.yaml` defines **Engineering a
Universal Real-Time Tracking Platform**: front matter, 35 chapters, and six
appendices (42 reading sections). Its supplied 184-page PDF and complete EPUB
remain unchanged. The site adapter in `scripts/site.py` handles Pandoc heading
and image attributes, checklists, and EPUB sections split across multiple files.
After manuscript changes, run the package's `scripts/build-book.sh` with Pandoc
and WeasyPrint to rebuild its supplied editions. Ordinary website builds reuse
these local exports and check source consistency. Reading URLs use
`/books/universal-tracking/`; copyright remains all rights reserved.

Books keep their cover and diagram designs; Secret Contract Operator
uses English text throughout these assets. Referenced companion
documents are rendered with the site layout; their public support files live
under `assets/books/<id>/`. Canonical package folders are excluded from Jekyll.
Book-specific attribution, licenses, languages and cover proportions come from
the catalog. Search, saved reading positions, downloads and post filters include
every registered book. Keep all canonical packages and their supplied editions
in Git; only the generated site copies are ignored.

## Posts and new books

Posts are original editorial Markdown in `_posts/`, with `book_id` and
`chapter_slug` linking each note to a chapter. The shared post layout adds the
chapter link and related notes; book chapters link back to matching posts.
Categories are read from post metadata automatically. `/posts/` supports combined
book/category filters and keyword search, with shareable URL parameters.

When adding a book, write at least three substantive posts about different
numbered chapters in the same change. Keep their metadata complete and their
topics varied; do not duplicate chapter text or use placeholders. See
[AGENTS.md](AGENTS.md) for the required fields and publication rules. The existing
`scripts/check-books.py` check enforces coverage for every book, validates chapter
references, and checks all local post links. CI runs it before deployment.
Posts are versioned source files; ordinary builds never overwrite them.

## Videos

`/videos/` embeds the two YouTube playlists and lists their videos with a picker.
The playlist IDs, descriptions, and video index live in `_data/video_playlists.json`.
Run `npm run sync:videos` to refresh that index from the public playlists, then
`npm run build:css` and `bundle exec jekyll build`. Sync needs network access;
ordinary site builds use the saved index. The embedded playlist menu also shows
the current playlist directly from YouTube. Players load only after a selection;
video links work without JavaScript.

## Search, projects, reading and discovery

`/ai/` is the featured AI Lab, with independent guides, categories, a tool
filter, full-text command search, and shareable filter URLs. Its modern dark
theme uses local fonts and a separate stylesheet, loaded only where needed.
The homepage and main navigation lead directly to it. AI guides also appear
in `/posts/`, global search, the sitemap, social previews, and the Atom feed.

Add AI guides as `_posts/*.md` with `layout: post`, `section: ai`, `title`,
`description`, `category`, `tool`, `surface`, `format`, `verified_at`, `sources`,
`illustration`, and `tags`. `tool` identifies an entry in `_data/ai_tools.yml`,
or `workflow` for guidance across tools. Each source has a `title` and HTTPS `url`.
Use original examples, verify command names against official documentation,
and distinguish web, desktop, CLI, IDE, custom, and retired commands. See
[AI source notes](docs/ai-sources.md). The shared post layout and card include
render AI guides without requiring artificial book/chapter links.

Edit `src/ai.css` and run `npm run build:css` to rebuild the AI theme. The usual
Tailwind watch command watches `src/input.css`; AI stylesheet edits need a rebuild.

The homepage offers visual learning paths into books, notes, and videos, with
counts taken from the existing catalogs. `assets/js/effects.js` adds one-time
scroll entrances, pointer highlights on cards, and depth on the hero illustration.
The shared header gains a translucent background while scrolling. Book covers
react to hover; the AI theme adds a subtle grid, glow, and gradient headings.
All timed decorations finish within four seconds. Reduced-motion preferences
disable animation and pointer effects, including when changed during a visit.
Content is never hidden pending an animation: navigation and filters work if
the effects script or observer API is unavailable. The document reader does not
load the effects script, and decorative layers are excluded from print.

`/search/` searches full post/chapter text, books, projects and video titles. The
index is generated locally by Jekyll and fetched only on the search page. A
browseable directory works without JavaScript or if the index cannot load.

The reader saves its position and text/theme preferences on the current device.
Book actions show Continue reading when a saved chapter exists. Unavailable or
invalid browser storage does not block reading. The document toolbar provides
chapter selection, collapsible/filterable contents, a section outline, reading
progress, focus mode (Escape to exit), and printing of the current section.
With JavaScript, chapters use a full-window workspace with independently
scrolling text and contents. Scrolling the text hides the site navigation and
moves the book toolbar to the top. Return to the beginning or use the toolbar's
site navigation button to show it again. Text fills the available width, and
the contents become an overlay on small screens. Saved places and progress use
the text panel's scroll position. The hidden site menu stays hidden between
chapters of the same book during the browser session. Printing includes the
complete section and preserves the reading position afterward.
Chapters, navigation, and downloads remain available without JavaScript.

`/cv/` presents the profile, concurrent and past employment roles, project work,
books, and videos. Edit `_data/cv.yml` for profile and career details; employment
durations are calculated during the build using each role's end month when
provided, or the current month for ongoing roles. The page reuses the project and book
catalogs and supports printing or saving as PDF through the browser. See
[CV sources](docs/cv-sources.md) for provenance, including the owner's LinkedIn
screenshots.

`/codepop/` introduces the owner's company with services, solution categories,
the delivery process, founder context, and contact links. It shares the CV's
visual language, has a distinct main-menu link, and appears in full-text search,
the sitemap, and company structured data. Edit `codepop.html` for content; see
[CodePop sources](docs/codepop-sources.md) for provenance.

`_data/projects.json` supplies four detail pages and shared project cards.
`scripts/build-assets.py` generates social images, icons and responsive WebP
covers. Local fonts retain licenses; photos and documentation previews are
versioned assets. Builds do not fetch them from the network.

Generated images are published atomically so live Jekyll rebuilds cannot copy
partially encoded covers or social cards. `npm run check:site` also decodes
linked raster images in the publication build to reject empty or corrupt files.

`_includes/share-links.html` provides LinkedIn, X, Facebook, WhatsApp, Reddit, and email
sharing for posts, AI guides, books, chapters, projects, the CV, CodePop, and
playlists. Reuse this include on new content pages. Links always use the public
canonical URL from `_config.yml`, without visit-specific queries or fragments.
The links work without JavaScript; `assets/js/share.js` adds clipboard copying
with a selectable-link fallback and native sharing on supported devices. Share
controls are hidden when printing and load no third-party widgets.
Compact icons use each network's colors, keep one row on small screens, and
provide accessible names and hover labels. Profile photos keep their local
originals, with a matching color treatment and geometric frames in CSS.

The site includes a sitemap, canonical URLs, JSON-LD, social previews, favicon,
RSS/Atom at `/feed.xml`, custom 404 and compatibility downloads. See
[measurement setup](docs/measurement.md) for Search Console, Google Analytics,
optional Plausible analytics, quality checks and Lighthouse reports. The owner's
GA4 tag `G-QCGFECRJDS` is configured for all HTML pages. Search Console ownership still needs confirmation in the owner's account;
the owner's HTML token and raw verification file are configured and checked.


## Learning and a personal reading workspace

`/learn/` offers three data-driven learning paths. Edit `_data/learning_paths.yml`
for their sequence, exercises and expected evidence; keep real internal links.
Paths appear in search and the sitemap, and all reading and exercise text works
without JavaScript. The local checklist does not require an account.

The book toolbar's notes button opens the reading workspace: chapter bookmarks,
completed sections, a note per section, and Markdown export. All values stay in
browser storage and are never sent to analytics. Storage failure keeps controls
usable for the current visit and offers export. Notes are saved explicitly and
when leaving the page. `/reading/` exports a versioned JSON backup and previews
imports before writing. Merge keeps local entries; replacement affects included
entries only. It carries learning checklists and reading preferences too. There
is no automatic cross-device synchronization or upload.

Offline reading is opt-in per section. The service worker is registered only
when Save offline is activated, caches at most 24 chosen sections and their
reading assets, and preserves actual network 404s. `/offline/` lists and removes
saved sections. Complete PDF/EPUB files are never precached. Browser storage may
be cleared or evicted; downloaded editions and exported notes are the lasting
copies. Builds produce the local manifest without network access.

Project walkthroughs explain documented architecture without executing commands.
`_data/projects.json` records pinned source revisions, prerequisites and related
chapters. Native captures retain links to their original verification record;
documentation previews and historical/disconnected states are labeled.

Featured project pages also include explicitly scoped local recordings, with
transcripts and matching source pins. `/codepop/engineering-notes/` describes
public engineering decisions without inventing client case studies. See
[recording evidence](docs/project-demos.md) before updating those assets.

`/ai/workshops/` offers four original exercises with local Node.js starters,
acceptance tests, and separate reference solutions in `labs/ai-workshops/`.
`npm run build:labs` packages the source reproducibly for download, and
`npm run check:labs` confirms that starters fail assertions and solutions pass.
Ordinary builds need no network access for these exercises.

`/subscribe/` makes article RSS and site-change updates discoverable. Optional
email signup needs the owner's real `newsletter_url`. The first web issue lives
at `/newsletter/`; [newsletter setup](docs/newsletter.md) explains the owner steps
needed for email signup and delivery. Add stable changelog IDs
in `_data/updates.yml`; `last_modified_at` is an explicit editorial timestamp.
See [measurement and maintenance](docs/measurement.md) for GA4 events, owner
account setup, scheduled source reviews and post-deployment public checks.
See [browser review](docs/browser-review.md) for tested coverage and the remaining
manual checks, and [dependency maintenance](docs/dependencies.md) for the
reviewed parser override and outstanding upstream finding.
