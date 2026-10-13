# 000. Establish a separate, reproducible book workspace

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** None; this is the intake task.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

AGENTS.md; BOOK_SPEC.md; books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/orch/AGENTS.md

## Output artifacts

books/inside-orch/state/workspace.json; books/inside-orch/validation/intake/baseline.md; books/inside-orch/manuscript/README.md

## Work to perform

Inspect the working directory and any existing Git state before creating files. Identify the book workspace, the immutable evidence snapshot, and a separate location for runnable labs. Record the full application SHA, tree SHA, corpus counts, tags, author, title, language, and local tool versions. Run books/inside-orch/scripts/verify_pack.py and retain its actual output. If a Git checkout of the source is needed for historical navigation, clone into a separate read-only source location and checkout the locked SHA; do not substitute the moving main branch. Never initialize or push a repository inside books/inside-orch/evidence/orch.

Create the manuscript directory layout and a scope note explaining that this workflow generates a new engineering book. Preserve any existing draft rather than overwriting it. Record which tools are present for Go, Docker, PostgreSQL, PDF rendering, EPUB checks and the site build; absence blocks the dependent lab or publication task, not the research tasks. Leave unavailable commands unrun and record why. Set up a durable validation directory with UTC execution records. Explain that the supplied snapshot contains tracked files and exported diffs, not a .git database.

## Acceptance and evidence

Every locked source hash matches; all 91 development prompts and 105 commit records are available; workspace paths are isolated; no user files overwritten; exact baseline and actual tool capabilities are recorded.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Site-root bootstrap

Verify the current Git remote identifies alekpopovic/alekpopovic.github.io, inspect branch/status and read any deeper instructions before changes. Do not reset the site to the inspection SHA or overwrite unrelated work. Compare the current site contract with the locked evidence and reconcile material changes. Add `books/inside-orch` to `_config.yml` exclude before running Jekyll, preventing raw research/prompts/source snapshots from becoming public static files. Preserve all existing excludes and the production origin. Keep the new book unregistered until its complete manuscript and native exports are ready; ordinary site builds must remain valid meanwhile. Create canonical `books/inside-orch/book.json` with English metadata and planned edition status; this file does not make the book publicly available.
