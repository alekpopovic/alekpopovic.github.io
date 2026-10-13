# 008. Turn the outline into three coherent learning paths

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 007 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; BOOK_SPEC.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/READER_PATHS.md; books/inside-orch/editorial/LEARNING_OBJECTIVES.md

## Work to perform

Construct developer, DevOps and architect reading sequences using the fixed 40-chapter outline. Identify a shared foundation, dependencies between chapters, optional advanced branches and checkpoints with observable outcomes. A reader must understand the runtime boundary before encountering sophisticated scheduler, autoscaler or leadership packages.

For each chapter name the prior knowledge, the new mental model, a code-navigation skill and a practical result. Translate vague outcomes such as understand reliability into tasks such as trace a stale report through lifecycle guards or show what is lost after restarting a process. Use a dependency table rather than a decorative linear diagram. Plan cross-references so readers moving through a path can find definitions without duplicate multi-page explanations. Require all paths to encounter resource propagation, persistence and fencing limits. Introduce a single running service that later labs mutate in controlled ways. Include time estimates as editorial estimates rather than measured completion guarantees. Keep navigation and accessibility goals distinct from the project's maturity.

## Acceptance and evidence

All 40 chapters assigned; prerequisites form an acyclic graph; each path includes critical boundaries; outcomes are demonstrable; no path depends on unwritten implementation.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
