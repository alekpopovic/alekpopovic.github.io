# Prompt 070 — Lab 05 — Secrets, authorization, and healthcheck trust boundaries

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/secrets/envelope.go`, envelope tests, `internal/auth/auth.go`, agent credential tests, `internal/api/api.go`, API authorization tests, redaction helpers, `internal/health/health.go`, health tests, `pkg/types` healthcheck validators, assigned-agent payload construction, and `docs/SECURITY.md`, `docs/SECRETS.md`, and `docs/REGISTRIES.md`. Inspect both input validation and the network client's redirect behavior; neither alone proves SSRF resistance.

## Build the lab

Create `books/inside-orch/labs/05-security-boundaries/README.md`, `lab.json`, complete local fixtures, and any teaching harness under `books/inside-orch/examples/teaching-extensions/security`. Use synthetic one-use secret canaries generated at run time, never real credentials. Keep token/envelope keys in private temporary files or process environment and record only hashes or redacted markers. Define cleanup before the reader runs the exercise.

Demonstrate secret encryption/decryption through the local envelope, metadata-only API reads, namespace-scoped reference resolution, assigned-agent plaintext delivery, redacted errors/audits, and the consequence of losing envelope-key material. Explain that encrypted data in MemoryService remains volatile despite cryptographic protection. List which processes necessarily receive plaintext and what trust assumptions follow.

Test user roles and agent identity separately. Build positive and negative cases for viewer reads, denied mutation, namespace operator scope, cluster administration, bootstrap registration, issued agent credentials, wrong-node reports, and expired/rotated credential handling. Use actual signing/issuer interfaces and source-defined response codes; no hand-written JWT should imply unsupported production identity integration.

For healthcheck security, use local `httptest` servers or loopback-only disposable endpoints. Demonstrate legal relative paths, invalid absolute/protocol-relative inputs where the parser rejects them, same-origin redirects, blocked cross-origin redirects, timeout handling, and bounded response consumption. Do not contact cloud metadata, public attacker infrastructure, private production services, or external DNS targets. Discuss gaps such as address selection and DNS behavior only to the extent the source exposes them; do not claim a complete SSRF defense from a single redirect guard.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/05-check.json` with a case matrix, actor/namespace, expected HTTP result, actual result, secret visibility boundary, and network destinations. Add a canary scanner over captured logs/errors/audits and metadata responses; separate explicitly permitted assigned-agent plaintext from forbidden output so legitimate delivery does not mask leaks. Record scanned file hashes and forbid raw canaries in published evidence.

Machine-check at least twelve authorization/secret/probe cases, including wrong-node denial and blocked cross-origin redirects. Every network connection must remain local and every cleanup target must be lab-owned. Missing crypto/toolchain prerequisites produce explicit skipped status. Verify expected error codes against actual handler mapping rather than assuming all denials are 403. The final explanation must identify the disabled-auth local default, trusted Docker socket privilege, static bootstrap limitations, missing mTLS, and durable-state boundary without declaring the release production-safe. Finish with a complete trust-boundary table that names producer, consumer, permitted sensitive data, enforcement point, and residual assumption.

## Immutable starting references

- [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go)
- [internal/auth/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go)
- [internal/health/health.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)
