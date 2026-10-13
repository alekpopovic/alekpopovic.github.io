# Inside orch — edition 1.0

**Inside orch: Building and Operating a Docker Orchestrator in Go**, Aleksandar Popovic, 13 October 2026. Complete local reviewed edition; website publication has not been performed.

## Readers and scope

This English engineering book is for Go developers, platform engineers and operators who want to trace a small orchestrator from intent through placement, reconciliation and Docker execution. Forty numbered chapters, a preface and six appendices form 47 ordered reading sections. Worked exercises and answers, eight actually executed bounded labs, exact source excerpts, original teaching additions, history maps and operational playbooks accompany the narrative.

Measured meaningful manuscript length is **101,211 words**: 86,644 in reading sections plus 14,567 in worked-answer companions. Fenced code/output, URL destinations, duplicated exports and the separate 9,705-word lab guides are excluded. The accepted PDF has **546 pages**. Measurement inputs are recorded in `validation/publication/manuscript-measurement.json`; final format counts and hashes are bound by the edition manifest.

The immutable application source is `alekpopovic/orch` at **cbfc94ade5b57e449d6b73bf1485b1c5b1647022**. Its 361 locked files remain unchanged. Original application prompts 00–90 are historical evidence, distinct from this book-production workflow. Historical associations do not invent one commit or successful execution per prompt.

## Delivered files

- `inside-orch.pdf`: reviewed print/read edition with embedded local fonts and bookmarks.
- `inside-orch.epub`: validated reflowable edition, cover and navigation.
- `inside-orch.md`: unified manuscript export.
- `inside-orch-offline.zip`: self-contained reader, all 47 sections, worked answers, selected companions, local assets and PDF/EPUB downloads. Open `inside-orch/reader/index.html` after extraction.
- `inside-orch-sources.zip`: editable book inputs, examples, lab guides, publishing tools and selected evidence metadata. The full application/site checkout and private execution artifacts are deliberately excluded; see `REPRODUCE.md`.
- `inside-orch-release.zip`: final assembly of the exact reviewed exports, the source/reader archives, provenance, rights, gate/reviewer records and this handoff.

`dist/SHA256SUMS.txt` covers the PDF, EPUB and three ZIPs. `publication/edition-manifest.json` lists exact member hashes, measured metadata, tools and provenance. Both archives created at 095 are frozen input snapshots. Later 096–099 gate, review and author handoff are separate final-edition records; the source ZIP is not represented as containing future tracker completion. Generation prompts are outside the public reader/source packages.

The native Jekyll integration uses `/books/inside-orch/`, registers the sixth book and generates ignored reading/download assets. Three original standalone posts cover Chapters 5, 6 and 19, with reciprocal chapter links. Shared search, glossary, feed, sitemap, reader controls and analytics layouts remain in use. The canonical book folder is excluded from raw Jekyll copying.

## What the evidence supports

The default application owns active state in process-local `MemoryService`. PostgreSQL packages/migrations, HA leadership and autoscaling are discussed according to their actual integration status, not presented as default server guarantees. Task compare-and-swap is not an aggregate reservation or fencing protocol. Ordinary assignment does not propagate resource requirements to runtime limits; a direct adapter experiment is a separate path. Logical stop/drain accounting can precede physical stop. Logical namespaces are not hostile kernel isolation, local volumes are not distributed storage, and GitOps can partially apply a revision. Supply-chain/plugin/overlay proposals remain labelled designs.

The actual acceptance record includes source/code/security/reader reviews; all 8 bounded lab executions; EPUBCheck 5.4.0 with zero errors/warnings; actual visual review of all 546 PDF pages; final-PDF raster equivalence; native section/post/search/feed/sitemap/download checks; no-JavaScript offline reading; and real browser/performance checks. The offline reader passed 216 cases and 8 navigation assertions, with external requests blocked. Local performance checks covered 20 routes, including the new landing and Chapter 6; these are synthetic measurements, not field data.

The full UI invocation produced 151 passes and one stale five-book catalog-count assertion. That assertion was corrected for six books and its focused rerun passed. This is combined coverage from separate invocations, not a claim that the original full invocation exited successfully. Original PostgreSQL fixture failures caused by its incomplete 14-migration setup remain recorded; a separately labelled full 16-migration teaching extension passed. Six external baseline skips remain visible. Optional procedures without execution evidence are not called executed. No external human endorsement, physical e-reader compatibility, distributed proof or production certification is implied.

## Accepted minor erratum

**FINAL-OPS-001 — disposable database naming.** Always use **`inside_orch_lab_<unique_run>_test`**. `labs/ENVIRONMENT.md` states the prefix but omits the immutable upstream reset suite's `_test` suffix. The book precheck accepts a prefix-only name; the upstream suite then refuses it before schema reset. Actual authored runs used the correct suffix. This safe refusal does not invalidate them. A later edition should require the suffix in the book precheck, its tests and the common guide; never edit the immutable application tests to evade their guard.

The earlier major Chapter 17 stop-accounting finding is resolved in canonical text, worked reasoning and the accepted formats. No release-blocking editorial issue remains in the local 096/097 gates. Residual application limitations are instructional content, not silent fixes to the application.

## Rights, errata and later editions

Original manuscript rights: **All rights reserved**, as selected by the author. `RIGHTS.md` and `NOTICE.md` preserve source/third-party provenance and font notices. The pinned application does not include a top-level license grant; this book does not create one. Packaging is not legal clearance or a new license for application code/dependencies.

Report errata to the author through the website's existing contact path, or propose a scoped issue/PR in the website repository. Include edition 1.0, chapter/claim ID, exact source SHA, reproduction prerequisites, expected/observed behavior and evidence with secrets removed. Do not include database dumps, tokens, private environment files or unrelated host logs. No issue, PR or message was sent as part of this task.

For a later edition, choose and record a deliberate new immutable source lock, compare capabilities/history/interfaces/migrations, revise affected chapters and teaching additions, and rerun the affected labs plus editorial/format/site/release gates. Do not merely advance dates or relabel historical evidence as fresh. Rebuilding a PDF may change its bytes even with identical page rasters; preserve and verify this edition's exact reviewed exports. See `REPRODUCE.md` for tools, commands, archive boundaries and reproducibility limits.
