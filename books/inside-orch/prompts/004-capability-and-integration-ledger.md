# 004. Build the capability ledger that governs every chapter

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 003 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/TECHNICAL_AUDIT.md; books/inside-orch/evidence/orch/cmd/orch-server/main.go; books/inside-orch/evidence/orch/internal/controlplane/; books/inside-orch/evidence/orch/internal/agent/; books/inside-orch/evidence/orch/internal/docker/

## Output artifacts

books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/validation/intake/capabilities.json

## Work to perform

Reinspect the supplied technical audit against the pinned source. For each capability classify runtime-integrated, implemented package, partial integration, design only, teaching extension or future work. Include persistence, scheduler/reconciler paths, Docker resource enforcement, lifecycle guards, heartbeat/offline recovery, HA, autoscaling, auth, secrets, tenants, quotas, image identity, GitOps, jobs, cron, volumes, DNS, notifications, upgrades and billing.

For every row trace a constructor or call path and cite the defining lines. The default server uses MemoryService. Its immediate round-robin assigned tasks differ from scheduler.Plan. AgentTask and ensureTask do not carry resource limits to the adapter's supported enforcement fields. Autoscaling and leadership packages are absent from server composition. Tests using the same MemoryService after a controller restart are not process durability tests. Distinguish a potential pooled-session advisory-lock cleanup defect from a demonstrated test result. Identify direct code evidence, uncertainty and the experiment that could resolve it. Give this ledger a stable row ID so later manuscript claims can reference it. Treat the ledger as an editorial control, not a badge of production fitness.

## Acceptance and evidence

All major executable/library/design differences documented with source lines; critical gaps cannot disappear in later chapters; unconfirmed security/reliability risks are labeled as hypotheses.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
