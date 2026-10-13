Adds **Inside orch: Building and Operating a Docker Orchestrator in Go** as the sixth book in the existing Jekyll catalog. Readers get 47 native sections (preface, 40 chapters and 6 appendices), worked answers, PDF/EPUB downloads, source-traceable explanations and 8 executed bounded labs. The book is pinned to Orch commit `cbfc94ade5b57e449d6b73bf1485b1c5b1647022` and distinguishes actual default behavior from unwired packages and design proposals.

The adapter preserves shared reader layouts and ignored generated files. Three original posts cover Chapters 5, 6 and 19, with reciprocal chapter links; glossary, updates, search, feed and sitemap include the new edition. Canonical book/workflow sources stay excluded from raw Jekyll copying. The existing workspace test now expects six catalog books, and five new browser tests cover the Inside orch reader and filtering behavior.

Measured edition: 101,211 meaningful manuscript words (including worked answers, excluding fenced code/output and separate lab guides), 546 PDF pages. Reviewed PDF/EPUB, offline reader, editable source archive, final release ZIP, rights and provenance are under `books/inside-orch/`. Original manuscript rights are All rights reserved; pinned source and bundled third-party assets retain their existing rights/notices.

Validation performed locally:

- npm/Jekyll builds; book/post/download/local-link checks; site metadata, analytics, search, feed and sitemap validation; editorial content checks.
- Source/listing/compiler/security/reader reviews; all 8 bounded lab executions with actual evidence; original incomplete PostgreSQL fixture failures and six external baseline skips retained explicitly.
- EPUBCheck 5.4.0 with zero errors/warnings; actual visual review covering all 546 PDF pages plus exact final-raster equivalence; Chromium EPUB reading preview.
- Offline reader: 216 cases and 8 real navigation assertions. Final archives: independently checked exact member manifests, hashes, CRCs and snapshot boundaries; all five system checksums passed.
- UI: 151 passed/one stale five-book assertion in the full invocation, followed by a passing focused rerun after correcting that assertion. These are separate executions. New book tests passed. Synthetic performance: 20 routes passed; new landing 93 and Chapter 6 scored 95, each with accessibility/best-practices/SEO 100 and CLS/TBT 0.

The 096 gate and 097 skeptical developer/DevOps/architect review have no remaining blocker. One accepted minor erratum is documented: disposable lab database names must end in `_test`; prefix-only names pass the book precheck but are safely refused by the upstream reset test. The immutable source was not patched. No external human endorsement, proprietary e-reader/hardware compatibility or application production certification is claimed.

This change is prepared locally. No push, PR, merge or live deployment was performed as part of generation. See `books/inside-orch/publication/HANDOFF.md` and `PUBLISH_CHECKLIST.md` for the exact publication action and post-deploy verification.
