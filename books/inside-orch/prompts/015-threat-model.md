# 015. Map trust boundaries before writing security chapters

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 014 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/internal/auth/; books/inside-orch/evidence/orch/internal/health/; books/inside-orch/evidence/orch/internal/secrets/; books/inside-orch/evidence/orch/internal/gitops/; books/inside-orch/evidence/orch/internal/notifications/; books/inside-orch/evidence/orch/docs/SECURITY_REVIEW.md

## Output artifacts

books/inside-orch/editorial/THREAT_MODEL.md; books/inside-orch/validation/intake/security-boundaries.json

## Work to perform

Identify operator, agent, server, Docker daemon, image registry, Git source, notification receiver, DNS client and database trust boundaries. Trace optional user JWT auth, registration tokens, node credentials, namespace context, secret envelopes, registry auth and debug routes. Describe default development configurations and the conditions under which authenticated behavior is active.

Inspect SSRF validation and actual dialing, DNS resolution, proxy behavior, redirects, notification URLs and GitOps filesystem boundaries. Distinguish source-derived concerns from demonstrated vulnerabilities; propose safe tests using local fakes or loopback fixtures rather than external targets. Treat Docker socket access as host privilege. Explain that namespaces and RBAC are API boundaries, not full kernel/network isolation. Check secret values through logs/errors/events and encryption-key management; encrypted storage does not eliminate plaintext at the execution boundary. Define testable security assertions for admission, redaction, path traversal and unauthorized status reports. Avoid blanket production-hardening claims, hypothetical warnings and unexplained checklists.

## Acceptance and evidence

Trust paths source-traced; default/optional auth visible; SSRF/file-boundary hypotheses labeled and testable; tenant isolation claims scoped; no credential data captured.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
