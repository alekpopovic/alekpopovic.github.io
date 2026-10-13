# 002. Reconstruct the engineering history with verifiable milestones

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 001 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/commits.json; books/inside-orch/evidence/commits.csv; books/inside-orch/evidence/commit-diffs/; books/inside-orch/evidence/COMMIT_INDEX.md

## Output artifacts

books/inside-orch/editorial/HISTORY.md; books/inside-orch/validation/intake/milestones.json

## Work to perform

Read the complete 105-commit corpus and selected diffs, retaining both author and committer dates. Group meaningful engineering changes into scaffold/API/runtime, scheduling/reconciliation, lifecycle/reliability, v0.2-era hardening, v0.3 contracts/workloads/operations, documentation and maintenance. Inspect changed files before describing a milestone's result. Differentiate merge commits, dependency updates, tracker-only commits and implementation commits.

Verify tag identities from source-lock and the prompt mapping: 0.1.0 and 0.3.0 are present; a release-preparation commit does not establish a 0.2.0 tag or a published artifact. Explain that 0.3.0 tags a formatting fix preceding the final documentation HEAD. Preserve this difference when selecting editions and linking sources. A chapter discussing historical code links to the historical SHA; a walkthrough of present code links to the locked HEAD. Build a reader-friendly timeline that explains why each change matters and what remained incomplete. Do not turn release notes or titles into executed-test evidence. Retain compact exact commit subjects for navigation with full-SHA URLs.

## Acceptance and evidence

Timeline dates and tag SHAs match corpus; historical/current links are separated; every milestone has diff evidence; no claim of release publication is made without direct evidence.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
