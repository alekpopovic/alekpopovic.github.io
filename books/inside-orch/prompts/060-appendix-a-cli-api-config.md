# Prompt 060 — Appendix A — CLI, API, and configuration reference

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

Read `docs/CLI.md`, `docs/API.md`, `docs/CONFIGURATION.md`, `docs/SERVICE_SPEC.md`, `api/openapi.yaml`, `schemas/service.schema.json`, `internal/cli/root.go`, `internal/cli/operations.go`, `internal/cli/workloads.go`, `internal/cli/deploy.go`, `internal/config/config.go`, `internal/api/api.go`, `internal/api/operations.go`, `internal/api/workloads.go`, and all three binary entrypoints. Discover deeper instruction files before inspecting their subtree.

## Produce the reference

Create `books/inside-orch/manuscript/appendices/a-cli-api-config.md` and `books/inside-orch/reference/cli-api-config.json`. Enumerate the actual Cobra command tree, supported flags, output formats, argument arity, environment variables, config keys, defaults, and validation rules. Cover migration commands separately because `orch-server migrate` is dispatched outside the CLI. Explain precedence with a fully specified local example using `ORCH_SERVER_URL=http://127.0.0.1:18080`, a dedicated temporary config, and an overriding `--server` value. Do not assume the server URL defaults to localhost.

For each implemented API operation, record method, normalized path, authentication boundary, namespace behavior, DTO symbols, status/error envelopes, and OpenAPI coverage. Public OpenAPI deliberately excludes agent-only routes: mark this boundary rather than reporting exclusion as missing implementation. Compare the static specification against registered handlers and report real discrepancies. Include the namespace header, request ID behavior, soft deletion, operational conflicts, health endpoints, and agent credential exchange without sample secret values.

Build a configuration table distinguishing loaded, validated, consumed, redacted, and ignored fields. Trace `DATABASE_URL` through migration/schema-check paths and prove it does not wire the default live control plane. Trace the Docker socket setting to runtime construction rather than trusting its advertised description. Explain integer CPU millicores and memory bytes in API DTOs versus human-readable quantities in deployment YAML, including duration encoding differences.

Generate local command help through source-built binaries only if the toolchain exists; offline help and validation must not contact a server. Retain generated help as evidence, never as prose dumped into the appendix. Use complete manifests accepted by the locked parser; keep examples in `books/inside-orch/examples/reference` and validate without deployment. Show safe redacted config printing based on actual executable options.

## Acceptance and evidence

Create `books/inside-orch/validation/060-reference-check.json` containing every command path and flag, every route/method pair, and every config field with its consumer. Add a checker that rejects duplicates, unresolved symbols, invented commands, missing provenance, and any unsupported claim of persistence. Require exact agreement between the extracted command inventory and your reference inventory; document excluded automatic help/completion nodes. Compare handler routes and OpenAPI methods programmatically, separating public and agent surfaces. Each example must have parser evidence or an explicit unexecuted status. Finish with a concise discrepancy ledger: source behavior, documentation statement, reader consequence, and immutable source links. No result may silently collapse unknown behavior into support.

## Immutable starting references

- [internal/cli/root.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go)
- [internal/config/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)
- [api/openapi.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/api/openapi.yaml)

## Native appendix contract

Use the first H1 exactly `# Appendix A - CLI, API, and Configuration Reference` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/a-cli-api-config.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.
