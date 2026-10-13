# 007. Design an isolated laboratory with honest prerequisites

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 006 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/compose.yaml; books/inside-orch/evidence/orch/docs/DEVELOPMENT.md; books/inside-orch/evidence/orch/docs/TESTING.md; books/inside-orch/evidence/orch/deployments/examples/; books/inside-orch/editorial/TECHNICAL_AUDIT.md

## Output artifacts

books/inside-orch/labs/ENVIRONMENT.md; books/inside-orch/validation/intake/lab-environment.json

## Work to perform

Define two tracks: source-only deterministic tests and disposable process/Docker/PostgreSQL experiments. Name all host privileges, exposed ports, databases, temporary repositories, images and cleanup scopes. Docker socket access is privileged; local development tokens and insecure dashboards must remain disposable lab defaults. Bind operator-facing services to loopback where the chosen commands support it and inspect actual configuration handling before changing values.

Create a prerequisite checker that reports capabilities without installing software or altering user infrastructure. Document exactly which experiments can run without Docker or a database. Database integration tests that reset schema must verify an explicitly designated throwaway URL; do not execute them against an existing real database. Define unique labels or namespaces for lab-created containers and only remove those resources. Explain that PostgreSQL running beside orch-server does not persist MemoryService state. Prefer pinned source builds rather than piping an uninspected latest installer into a shell. Store real execution evidence separately from expected-output examples. Include rollback/cleanup instructions for interrupted labs.

## Acceptance and evidence

Lab privilege and destruction scopes are visible; prerequisite checks are read-only; database isolation enforced; cleanup targets only lab-owned resources; expected output never represented as observed.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
