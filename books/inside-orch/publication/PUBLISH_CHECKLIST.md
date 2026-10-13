# Inside orch — reviewable publication checklist

## Current result and action boundary

The complete English book, native Jekyll integration and final release package are prepared locally in `alekpopovic/alekpopovic.github.io`, branch `book/inside-orch-000`. The website baseline and unchanged local default branch are `80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`. No commit, push, PR, merge, Pages deployment or external message was made. These commands describe the next author-controlled action; they have not been executed merely because they are printed here.

Open **http://localhost:4000/books/inside-orch/** while the retained preview runs. The first section is `/books/inside-orch/00-preface.html`; Chapter 6 is `/books/inside-orch/06-follow-one-request-through-the-control-plane.html`. Native chapter URLs have the existing site's `.html` suffix. The intended production location is `https://www.alekpopovic.com/books/inside-orch/`; this handoff does not assert that it is already deployed.

## Inspect the accepted edition

- Read `HANDOFF.md`, `RELEASE_NOTES.md`, `RIGHTS.md` and `NOTICE.md`. Original manuscript: All rights reserved. Source/asset provenance and original rights remain explicit.
- Inspect `edition-manifest.json`, `validation/RELEASE_GATE.md`, `validation/reviews/final-independent-review.md` and the three detailed reviewer reports. All material findings are resolved. Accepted minor erratum: use disposable database names `inside_orch_lab_<unique_run>_test`.
- Open the shipped PDF/EPUB and native reader. There are 47 sections, 40 numbered chapters, 6 appendices, 8 executed bounded labs, 101,211 measured meaningful words and 546 PDF pages. Meaningful words include worked answers and exclude fenced code/output, duplicated exports and separate lab guides.
- Verify the final files from the website root without rebuilding them:

```bash
cd books/inside-orch/dist
sha256sum -c SHA256SUMS.txt
```

Return to the website root before running subsequent commands. The final ZIP SHA256 is `2790a4d4d0cf0d71431ee2ca4f4532f4edfc6f69f9d15216389a473e15032e4b`. `validation/publication/final-release-independent-verification.json` records the independent CRC/member/hash/snapshot checks. The final release preserves the 095 editable-source snapshot, adds later gate/review/handoff records separately, and retains the actual 098-in-progress/099-pending tracker snapshot at assembly. The canonical tracker outside the archive contains subsequent completion evidence.

## Review the exact local changes

The existing `publication/site-adapter/changes.patch` covers the reviewed catalog/build adapter, new posts, browser tests and core book publisher/verifiers as frozen at 095. It is not a substitute for all canonical book files or the later release/handoff files. Do not apply it again to this already integrated checkout. `final-source-inventory.json` inventories the relevant current source files; its snapshot exclusions are explicit. The complete canonical folder remains available for review in the working tree.

From the repository root, inspect:

```bash
git branch --show-current
git status --short
git diff --check
git diff -- _config.yml _data/glossary.yml _data/updates.yml scripts/book_catalog.py scripts/build-books.py scripts/check-performance.mjs tests/workspace-editor.spec.js
git check-ignore book-pages/inside-orch/index.html assets/books/inside-orch/downloads/inside-orch.pdf _data/books.json
```

The scoped change set is the canonical `books/inside-orch/` folder, those seven tracked files, `tests/inside-orch.spec.js` and three new posts for Chapters 5, 6 and 19. The book-level ignore rules omit private database dumps and intermediate PDF/offline build trees. Generated `book-pages/`, `assets/books/` and `_data/books.json` stay ignored; never force-add them. Root `AGENTS.md`, root `README.md`, unrelated books and the immutable application snapshot were not rewritten.

## Validation already performed

The final gate records actual npm and Jekyll builds, book/post/download/local-link validation, site metadata/search/feed/sitemap/analytics checks, content validation, publisher tests, 8 real bounded lab results, EPUBCheck, PDF visual coverage, offline browser checks, UI and 20-route synthetic performance measurements. Fresh final pack/strict checks passed with no errors or warnings, all 361 application files retained their locked hashes, and local HTTP checks verified the exact final downloads and a true 404.

Keep the actual limits visible: the full UI invocation had 151 passes and one stale five-book assertion; the corrected six-book assertion passed separately. Original PostgreSQL fixture failures and six external baseline skips are preserved. No new Firefox/WebKit hardware compatibility, proprietary e-reader, external human endorsement or production certification was invented. The historical PDF range-report hash discrepancy has a dedicated archived history supplement; the unavailable prior lab report was not reconstructed, and actual final raster equivalence remains inspectable.

If source or format inputs change before publication, rerun the affected acceptance checks. The ordinary website sequence from a fully provisioned checkout is:

```bash
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
npm run check:site
npm run check:content
npm run test:ui
npm run check:performance
```

Ordinary builds are local and fetch no assets. CI uses its own installed Python environment (`python` instead of `.venv/bin/python`). A rebuild can change PDF bytes despite identical rendered pages; newly generated bytes require their format/visual checks and updated release identity. Do not rerun `run_release_gate.py` against the frozen 096 files and silently invalidate final review hashes; preserve this edition and create separately named evidence for a later candidate.

## Optional next action after the author chooses a draft PR

Review any additional work before staging. The following scoped commands are provided for the author to run after deciding to create the draft; nothing in this checklist pushes the default branch:

```bash
git add -- _config.yml _data/glossary.yml _data/updates.yml scripts/book_catalog.py scripts/build-books.py scripts/check-performance.mjs tests/workspace-editor.spec.js tests/inside-orch.spec.js _posts/2026-10-13-a-ready-server-may-have-forgotten-your-cluster.md _posts/2026-10-13-follow-a-resource-limit-all-the-way-to-docker.md _posts/2026-10-13-an-offline-node-is-not-proof-that-its-workload-stopped.md books/inside-orch
git diff --cached --check
git diff --cached --stat
git status --short
git commit -m "Add source-verified Inside orch book and native reading edition"
git push --set-upstream origin book/inside-orch-000
gh pr create --draft --base main --head book/inside-orch-000 --title "Add Inside orch engineering book and native reader" --body-file books/inside-orch/publication/site-adapter/pr-description.md
```

The existing Pages workflow validates PRs and skips their deploy job. A merge/push to `main` or manual workflow dispatch can deploy; leave that for the author's publication decision. Check the actual remote configuration and current branch before executing these future commands. The local task does not authorize opening a PR or contacting reviewers.

## After a separately authorized publication

Use the established Pages workflow. Inspect its real build/deploy results, then run the existing public checker with the actual deployed revision, not a guessed feature-branch SHA:

```bash
git fetch origin main
REVIEWED_SITE_SHA=$(git rev-parse origin/main)
python3 scripts/check-publication.py --expected-sha "$REVIEWED_SITE_SHA" --attempts 12 --retry-delay 10
```

Independently open the public book landing, preface, Chapters 5/6/19 and the new posts. Verify PDF `%PDF-`/EPUB ZIP signatures, reading/search/reciprocal links, canonical URLs, feeds, sitemap and genuine 404 responses. Compare deployed download hashes to the accepted edition or explicitly review the CI-generated candidate. Record actual results before claiming the book is live. No such public verification is claimed by this local handoff.
