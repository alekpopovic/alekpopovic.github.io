# 013. Define the evidence that proves each operational lesson

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 012 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/internal/metrics/; books/inside-orch/evidence/orch/internal/events/; books/inside-orch/evidence/orch/internal/audit/; books/inside-orch/evidence/orch/deploy/monitoring/; books/inside-orch/evidence/orch/docs/OBSERVABILITY.md

## Output artifacts

books/inside-orch/editorial/OBSERVATION_CONTRACT.md; books/inside-orch/labs/observations.json

## Work to perform

List real metrics, events, audit records, API responses and runtime inspections usable in the case study. Trace where each metric/event is emitted and what its absence means. Differentiate control-plane intent, agent report and independently observed container behavior. A healthy process is not proof of convergence; a succeeded controller pass is not proof of durable state.

For each lab set evidence criteria using specific fields and timing boundaries: assignment outcome, stale status rejection, replica health, rollout availability, heartbeat age, failed GitOps sync, quota response, job attempts and actual Docker HostConfig. Inspect dashboards and alerts rather than assuming every panel has a live metric. Identify source-package signals absent from default runtime paths. Define low-cardinality metric labels and token-safe logs with exact redaction limitations. Explain collection interval and stale data when discussing alerts. Create a trace worksheet that correlates service/task/node/deployment IDs across API, event and agent evidence. Keep illustrative output separate from captured output and declare measurement duration/sample size for performance claims.

## Acceptance and evidence

Every observation maps to a real emitted field; intent vs runtime distinguished; no invented metric names; redaction and measurement limits visible.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
