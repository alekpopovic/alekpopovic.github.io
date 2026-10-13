# 009. Extract the decisions and tradeoffs behind the code

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 008 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/*DESIGN.md; books/inside-orch/evidence/orch/docs/ARCHITECTURE.md; books/inside-orch/evidence/orch/internal/; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/DECISION_REGISTER.md; books/inside-orch/validation/intake/decisions.json

## Work to perform

Create an architectural decision register from source and design evidence. Include Docker-first runtime boundaries, polling agents, Go packages, PostgreSQL stores, memory-backed executable composition, desired/actual state, deterministic planning, optimistic concurrency, namespaces, local storage, host ports, optional ingress, and extension interfaces. For every decision record context, observed implementation, alternatives, benefits, costs and unresolved questions.

Do not attribute an author's motivation when only the code is visible. Label your reconstruction as an inference and state the evidence. Explain the costs of simpler orchestration in small clusters without claiming that orch replaces every Kubernetes guarantee. Use concrete scenarios: a lost status response, saturated node, partitioned worker, concurrent operators, failed second GitOps manifest, and process restart. Identify which guarantees require atomic persistence, durable ownership, leases or fencing and which can be demonstrated with current packages. Keep prospective fixes in a separate teaching-design section with a validation plan. These decisions should guide chapter explanations rather than become generic cloud architecture essays.

## Acceptance and evidence

Decisions have code/design anchors; inferred rationale is labeled; tradeoffs use concrete failures; future guarantees are separate from baseline capabilities.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
