# 095. Create the offline edition and reproducible release inputs

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 094 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/dist/inside-orch.epub; _site/books/inside-orch/; books/inside-orch/manuscript/; books/inside-orch/examples/; books/inside-orch/validation/; books/inside-orch/publication/

## Output artifacts

books/inside-orch/dist/inside-orch-offline.zip; books/inside-orch/dist/inside-orch-sources.zip; books/inside-orch/dist/SHA256SUMS.txt; books/inside-orch/publication/REPRODUCE.md

## Work to perform

Package the complete reader edition separately from editable publication sources. Include PDF, EPUB, offline HTML, code examples, lab instructions, answers, source/commit index, rights notices and source edition metadata. Editable sources include canonical Markdown, style/build configuration, asset sources and validation records, with credentials, ephemeral logs containing secrets and unrelated site files excluded.

Ensure offline HTML navigates without a server where supported; if an embedded local server is required for search or module loading, document the exact dependency and provide a simple working launch command. Include exact source SHAs and explain how to retrieve the application repo without confusing it with teaching extensions. Generate checksums only after final files exist and verify them independently. Use deterministic archive order/timestamps where feasible and record remaining nondeterminism such as PDF metadata. A reproducibility note must describe actual tool versions and commands, not an aspirational one-line build. Keep these archives reviewable before publishing.

## Acceptance and evidence

Reader/source packages complete and distinct; no credentials; hashes independently verify; offline behavior tested or clearly scoped; exact reproduction instructions available.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Explicit offline reader producer

Prompt091 now produces the native adapter, not a standalone online/ directory. First build and validate the complete native site through prompts 092-094. Then explicitly create `books/inside-orch/dist/online/` for this offline edition from the finished native _site/books/inside-orch/ output or the book publisher's offline-export entrypoint. Copy only necessary reader styles, local fonts, images and code companions with an asset manifest; rewrite local navigation/assets safely for the packaged base and retain external source/commit links as online references. Preserve all 47 sections and title/source edition metadata. Validate the exported reader with a disposable loopback server, e.g. `python3 -m http.server 8765 --bind 127.0.0.1` from its own export directory, and scope/terminate only that owned process. Label any file-URL limitations. The explicit downloadable offline ZIP must not change the live service worker's opt-in per-section caching or precache complete books/downloads. Do not package a nonexistent online/ path or imply native adapter code itself is an offline edition.
