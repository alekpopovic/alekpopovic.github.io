# Prompt 071 — Lab 06 — Namespace scoping and atomic quota admission

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

Read `internal/namespace/context.go`, `internal/api/namespace_test.go`, API quota tests, `internal/controlplane/namespace_test.go`, control-plane quota tests, `internal/quota/quota.go`, store namespace/quota locking logic, migrations 000011 and 000012, `docs/MULTI_TENANCY.md`, and CLI quota/namespace commands. Follow namespace selection from CLI/config/header through lookup, reference resolution, and mutation, including routes with query parameters.

## Build the lab

Create `books/inside-orch/labs/06-namespaces-quotas/README.md`, `lab.json`, explicit fixtures, and optional isolated checks. Use two namespaces, `book-payments` and `book-observability`, each containing a service named `api`. Use distinct labels and non-sensitive environment values so accidental cross-scope reads are identifiable. Capture real IDs for executable API steps and use fixed identifiers only in deterministic fake inputs.

Demonstrate default namespace compatibility, selected namespace precedence, namespace-scoped roles, cluster administration, same-name service/secret independence, and cross-namespace object-ID hiding. A request for an inaccessible object must be compared with source-defined not-found behavior. Include the undeletable `default` namespace and deletion blocked by remaining workload/history; explain why deleting visible services may not empty namespace history.

Set concrete quota limits for services, replicas, CPU millicores, memory bytes, public ports, secrets, and registry credentials. Work through the exact accounting arithmetic from per-replica requests and current service state. Show zero limits as unlimited, deletion release semantics, and an update whose denied admission must leave the previous spec unchanged. Public-port quota counts declarations according to implementation, not an invented network allocation metric.

Introduce two concurrent scale requests competing for the last available replicas. Use existing in-memory tests or an isolated teaching harness, then separately define PostgreSQL advisory-lock integration prerequisites. Assert atomic admission only within the tested storage mode. Do not infer hostile tenant isolation, separate networks, separate Docker daemons, or independent control-plane failure domains from logical namespaces.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/06-check.json` with tenant/actor, source route, initial quota, requested delta, expected response, observed response, and final usage. Machine-check at least ten scope/admission cases, including duplicate service names in separate namespaces, cross-ID hiding, secret reference isolation, zero-limit behavior, concurrent capacity competition, and rejected mutation atomicity.

Require the arithmetic fixture to reproduce CPU/memory/replica totals and verify quota denials include actual structured details without secret values. Check the namespace header/query interaction against implementation and record discrepancies. Capture proof that only the admitted concurrent mutation affects final usage; skipped PostgreSQL tests must not inherit in-memory success status. Cleanup removes only lab objects when permitted; retained history gets an explicit explanation rather than direct unsafe database deletion. Finish with a worked architecture review distinguishing logical scoping, RBAC, resource admission, runtime isolation, and durable tenant recovery, identifying what this version implements and which boundaries still require extension.

## Immutable starting references

- [internal/api/namespace_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/namespace_test.go)
- [internal/controlplane/quota_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/quota_test.go)
- [internal/namespace/context.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go)
- [docs/MULTI_TENANCY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MULTI_TENANCY.md)
