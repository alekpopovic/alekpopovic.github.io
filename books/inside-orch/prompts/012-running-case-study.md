# 012. Design one progressive case study across the whole book

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 011 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; books/inside-orch/evidence/orch/deployments/examples/; books/inside-orch/evidence/orch/docs/SERVICE_SPEC.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/labs/CASE_STUDY.md; books/inside-orch/labs/case-study-manifest.json

## Work to perform

Choose a small stateless HTTP service and a finite worker/job as the running case study, using existing example specifications where possible. Introduce only the fields supported by the pinned parsers and validation. Carry the same service identity through deploy, scale, rollout, rollback, health failure, drift, node loss, namespace isolation, quota changes, GitOps and observation. Storage experiments use separate explicitly local fixtures.

For every stage record desired changes, expected state transitions, operator command source, telemetry, failure injection and cleanup. Identify which experiments run against the default server, standalone packages or teaching extensions. Add a deliberately resource-constrained scenario that exposes the difference between package planner behavior and MemoryService placement; do not hide it by selecting oversized lab machines. Include a restart scenario that demonstrates state loss before discussing durable store design. Specify how later chapters refer back to earlier observed IDs and logs without relying on an unreproducible environment. Keep results marked expected until executed. Build a small state graph that corresponds to actual lifecycle constants.

## Acceptance and evidence

One coherent case study covers eight lab stages; specs parse at baseline; failures target real paths; runtime/package/extension contexts and cleanup are explicit.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
