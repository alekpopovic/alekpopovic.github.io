# 005. Resolve stale documentation through code-first comparison

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 004 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/ARCHITECTURE.md; books/inside-orch/evidence/orch/docs/RELIABILITY.md; books/inside-orch/evidence/orch/README.md; books/inside-orch/evidence/orch/RELEASE_NOTES.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/DOCUMENTATION_CONFLICTS.md; books/inside-orch/validation/intake/documentation-conflicts.json

## Work to perform

Compare architecture, operational guides and release notes to startup wiring, handlers, controllers, runtime calls and tests. Log each disagreement with quoted short source fragments or precise references, the more authoritative path, the engineering consequence and a proposed book explanation. Examples to verify include a node-monitor roadmap entry when the monitor is already constructed, durable-storage wording with an in-memory server, and integration claims inferred from design documents.

Use implementation as the authority for current executable behavior, while retaining design documents as evidence of intent. Tests clarify expected contracts but do not override actual startup composition. Avoid silently reconciling contradictory documents into an invented ideal system. Write editorial wording that introduces the discrepancy without attacking the project. A reader should learn to inspect a real evolving repository. Keep historical documentation differences separate from present defects. When a conflict cannot be resolved by source inspection, mark it unresolved and propose a narrowly scoped test or author question. Do not modify application documentation in the evidence snapshot.

## Acceptance and evidence

Every conflict has exact source paths and a resolution/uncertainty; chapters receive the relevant conflict IDs; stale roadmaps are not copied as current behavior.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
