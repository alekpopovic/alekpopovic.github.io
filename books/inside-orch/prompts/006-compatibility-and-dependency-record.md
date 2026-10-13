# 006. Freeze the dependency and compatibility assumptions

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 005 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/go.mod; books/inside-orch/evidence/orch/go.sum; books/inside-orch/evidence/orch/internal/version/; books/inside-orch/evidence/orch/docs/UPGRADES.md; books/inside-orch/evidence/orch/docs/MIGRATIONS.md; books/inside-orch/evidence/orch/.github/workflows/ci.yml

## Output artifacts

books/inside-orch/editorial/COMPATIBILITY.md; books/inside-orch/validation/intake/toolchain.json

## Work to perform

Record Go version, direct dependency versions, API/server/agent/schema compatibility constants and CI tools from the inspected source. This is a versioned baseline, not a claim about the newest upstream releases. If the book discusses external semantics, retrieve and cite primary documentation at a version that applies. Do not recommend upgrading dependencies as part of manuscript generation.

Explain the distinction between compile/toolchain compatibility, wire compatibility, schema compatibility and rolling-upgrade compatibility. Trace how version metadata is checked in registration, heartbeat and migration commands. Document external suites' environment variables, build tags and skip conditions, including the danger that a normal passing suite skipped Docker or PostgreSQL. Explain why CI coverage artifacts prove only the checks actually executed. Record supported platforms from the source installation guide without inventing release assets. Include precise database test isolation requirements; schema-reset tests need a disposable database. Establish a policy for version annotations in command listings and lock regeneration for a future edition.

## Acceptance and evidence

Versions match locked files; compatibility dimensions are distinct; skips/prerequisites are explicit; external technical references are primary and version-appropriate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
