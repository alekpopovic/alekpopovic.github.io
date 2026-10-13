# 097. Challenge the book as three skeptical readers

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 096 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/manuscript/; books/inside-orch/validation/RELEASE_GATE.md; books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/evidence/orch/

## Output artifacts

books/inside-orch/validation/reviews/final-independent-review.md; books/inside-orch/validation/reviews/final-findings.json

## Work to perform

Perform independent developer, DevOps and architect reviews of the complete edition. If parallel reviewers are available, give each a distinct lens and exact source lock. Developer: can listings/examples be followed and compiled, are interfaces/state transitions correct? DevOps: do procedures state privileges, prerequisites, observations, recovery limits and cleanup? Architect: are persistence, concurrency, fencing, isolation, resource accounting and tradeoffs accurately scoped?

Give reviewers adversarial scenarios, not a request to praise the manuscript: two servers with memory state, conflicting claims, a node partition, a worker with unapplied limits, restart during rollout, a failed second GitOps manifest, advisory lock cancellation and a database suite silently skipped. Require findings with chapter/claim IDs and direct code or actual log evidence. Reconcile duplicate findings and fix material ones in canonical sources. Retest affected books/inside-orch/examples/labs/formats and update hashes. Record residual limitations without framing the book as a certification. The final recommendation must be based on readable teaching quality and inspectable evidence, not word count.

## Acceptance and evidence

Three lenses review actual final content; concrete findings source-backed; major issues resolved with revalidation; remaining limitations explicit; no invented external endorsement.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
