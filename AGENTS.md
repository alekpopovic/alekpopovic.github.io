# Project rules

This is a Jekyll and Tailwind site. Keep the existing visual language and use
shared includes for post cards. Writing and interface copy are in English.

## Adding a book

- Keep canonical manuscripts, publishing scripts, metadata, and licenses under
  `books/`. Register each book in `scripts/book_catalog.py`.
- Generate reading pages under `book-pages/<book-id>/` and public files under
  `assets/books/<book-id>/`. Reading URLs stay under `/books/<book-id>/`.
- Every new book must ship with at least three original, substantive posts in
  `_posts/`, covering three different numbered chapters. Select varied practical
  topics and write standalone explanations or worked scenarios; do not copy
  chapters or publish placeholder summaries.
- Each book post needs `layout: post`, `title`, `description`, `category`, `book_id`,
  `chapter_slug`, `illustration`, and `tags` in its front matter. `book_id` must
  match the catalog, and `chapter_slug` must identify a real chapter.
- Reuse an existing category when it fits. Available illustrations are `clock`,
  `queue`, `shield`, `network`, `package`, and `logs`.
- Posts are editorial source files and belong in Git. Do not regenerate or
  overwrite them during ordinary book builds. Shared layouts provide links to
  the chapter, related notes, and reciprocal links from the chapter.
- Keep `book-pages/`, `assets/books/`, and `_data/books.json` ignored by Git.

## Verification

Run `npm run build`, then `bundle exec jekyll build`, then
`.venv/bin/python scripts/check-books.py` (or `python scripts/check-books.py`
in CI). The publication check must reject a book without its required posts,
invalid chapter references, and broken local links.

For post interface changes, verify combined book/category/search filters,
shareable filter URLs, empty results, mobile layouts, and reading without
JavaScript. Keep filter labels and reading controls accessible by keyboard.

## Site features

- `/ai/` is the dedicated AI library. AI guides are editorial source files in
  `_posts/` with `layout: post`, `section: ai`, `title`, `description`, `category`,
  `tool`, `surface`, `format`, `verified_at`, `sources`, `illustration`, and `tags`.
  Standalone AI guides do not need invented book or chapter references. Keep
  book-post validation and the three-chapter coverage requirement intact.
- Verify AI commands against official documentation, name the application and
  surface (web, desktop, CLI, or IDE), and record the check date and source links.
  Distinguish built-in commands, aliases, optional skills, and custom commands.
  Never present commands from one application as universal shortcuts for another.
- Reuse `post-card.html` for AI cards. Maintain `_data/ai_tools.yml`, the shared
  AI article include and `src/ai.css`; new `section: ai` posts must appear in the
  AI hub, post directory, full-text search, feed, and sitemap automatically.
- Maintain `_data/projects.json` and `projects/<id>.html` for featured projects.
  Describe verified behavior, link sources, and do not invent adoption or benchmarks.
  Label documentation previews as such.
- `npm run build` generates social cards, icons and responsive covers. Keep local
  fonts and licenses; ordinary builds must not fetch external assets.
- `_plugins/site_features.rb` generates metadata, the sitemap, RSS/Atom feed,
  full-text search index and legacy download copies. Keep all chapters searchable
  and preserve 404 responses for removed articles without a replacement.
- Run `npm run check:site`, `npm run test:ui` and `npm run check:performance` after
  shared layout or browser changes. Preserve no-JavaScript navigation, storage
  failure handling, accessible controls and analytics disabled without owner
  configuration.
- Every new HTML page must include the shared Google tag through the `default`
  layout, directly or through a nested layout. Standalone layouts must include
  `google-analytics.html` in `<head>` exactly once. Keep the owner's measurement
  ID in `google_analytics` in `_config.yml`; do not duplicate the tag snippet or
  hardcode IDs in page templates. An empty ID must disable the tag everywhere.
  `npm run check:site` must verify that every generated HTML page includes exactly
  one configured tag, or no tag when the ID is empty.
- Analytics and Search Console need the owner's account configuration. Never
  invent verification tokens or claim collection while settings are empty.
  See `docs/measurement.md`.
