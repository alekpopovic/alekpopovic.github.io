# Native site integration acceptance

Final local candidate checked 2026-10-13T03:33:08.685561+00:00. The frozen edition has 47 sections (40 chapters and six appendices), 546 PDF pages, eight actually rerun laboratories and three substantive posts linked to Chapters 05, 06 and 19. No default-branch push or deployment was performed.

Final PDF SHA-256: `42b18782ecb996e526f98e000c7dbf59533ee6200737f71f536bbf536c2de51c`. EPUB SHA-256: `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`. Both canonical exports equal the generated asset and `_site` download bytes. The 47-entry EPUB/source map is explicit; raw workflow folders remain excluded. Generated reader/public paths and `_data/books.json` remain ignored.

## Actual commands and retained logs

- `npm run build` — exit 0, 2026-10-13T02:58:36.417714+00:00. Record: `validation/publication/invariant-table-site-build.json`; stdout: `validation/publication/invariant-table-site-build.stdout.txt`; stderr: `validation/publication/invariant-table-site-build.stderr.txt`.
- `bundle exec jekyll build` — exit 0, 2026-10-13T03:04:34.833109+00:00. Record: `validation/publication/invariant-table-jekyll-build.json`; stdout: `validation/publication/invariant-table-jekyll-build.stdout.txt`; stderr: `validation/publication/invariant-table-jekyll-build.stderr.txt`.
- `.venv/bin/python scripts/check-books.py` — exit 0, 2026-10-13T03:16:19.048231+00:00. Record: `validation/publication/invariant-table-books-check.json`; stdout: `validation/publication/invariant-table-books-check.stdout.txt`; stderr: `validation/publication/invariant-table-books-check.stderr.txt`.
- `npm run check:site` — exit 0, 2026-10-13T03:15:53.633233+00:00. Record: `validation/publication/invariant-table-site-check.json`; stdout: `validation/publication/invariant-table-site-check.stdout.txt`; stderr: `validation/publication/invariant-table-site-check.stderr.txt`.
- `npm run check:content` — exit 0, 2026-10-13T02:48:30.864812+00:00. Record: `validation/publication/final-content-check.json`; stdout: `validation/publication/final-content-check.stdout.txt`; stderr: `validation/publication/final-content-check.stderr.txt`.
- `npm run check:performance` — exit 0, 2026-10-13T02:49:37.043879+00:00. Record: `validation/publication/final-performance.json`; stdout: `validation/publication/final-performance.stdout.txt`; stderr: `validation/publication/final-performance.stderr.txt`.
- `npx playwright test tests/inside-orch.spec.js --grep connects|mobile|without JavaScript|storage` — exit 0, 2026-10-13T02:09:19.302220+00:00. Record: `validation/publication/inside-orch-reader-ui-system-browser.json`; stdout: `validation/publication/inside-orch-reader-ui-system-browser.stdout.txt`; stderr: `validation/publication/inside-orch-reader-ui-system-browser.stderr.txt`.
- `npx playwright test tests/workspace-editor.spec.js -g workspace and newsletter archive --workers=1` — exit 0, 2026-10-13T02:58:05.235411+00:00. Record: `validation/publication/workspace-six-books-ui.json`; stdout: `validation/publication/workspace-six-books-ui.stdout.txt`; stderr: `validation/publication/workspace-six-books-ui.stderr.txt`.

The initial full browser run retained 151 passes and one failure because a workspace assertion still expected five books. Updating that assertion to six produced an actual passing rerun of the affected test. The failed full-run record remains available; this report does not relabel it as passing. The focused Inside orch reader test passed using the recorded system Chromium.

The minimal review patch is `publication/site-adapter/changes.patch`. The source/generated hash manifest is `publication/site-adapter/source-generated-manifest.json`. Standalone post/source review is `validation/publication/post-editorial-review.json`. Detailed acceptance is `validation/publication/site-integration-acceptance.json`. Existing-book preservation means all six actual completeness/navigation/download checks passed; an unavailable historical generated-byte baseline was not invented.

Public deployment checks remain outside this local task. Final release readiness and independent skeptical reviews are separate 096/097 gates.
