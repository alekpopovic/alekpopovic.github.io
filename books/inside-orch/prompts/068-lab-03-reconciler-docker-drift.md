# Prompt 068 — Lab 03 — Reconciliation and Docker drift ownership

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

Read `internal/reconciler/reconciler.go`, reconciler tests, `internal/controlplane/controlplane.go`, `internal/agent/agent.go`, agent drift tests, `internal/docker/docker.go`, `internal/docker/fake.go`, fake-runtime tests, Docker integration tests, and `docs/RECONCILER.md`. Trace how the shipped memory control plane creates/stops tasks and how the store-backed reconciler package differs. Inspect exact ownership labels and cleanup predicates before designing drift cases.

## Build the lab

Create `books/inside-orch/labs/03-reconciler-drift/README.md`, `lab.json`, fixture descriptions, and an optional isolated teaching harness. Begin with replicas below target, failed tasks with `always` versus `never` policies, scale-down ordering, and soft deletion. Ask the reader to predict task counts and stop directives over two identical passes. Explain that the reconciler changes intent while the agent changes Docker state; neither owns the other's responsibility.

Use fake runtime cases for a missing managed container, a stopped managed container, a mismatched label/image/version, an unexpected owned container, and an unrelated unmanaged container. Derive expected behavior from `currentTaskContainer`, cleanup helpers, and lifecycle validation. In particular, test whether a missing container for a previously running task can be re-created through legal status reports; do not assume resetting to `pulling` is legal. A discovered error is valuable evidence and must be preserved as a boundary finding.

Follow ownership precisely. A matching container may be adopted using its labels; cleanup must never remove another node's workload or an unmanaged container solely because of a name similarity. Show the role of `orch` labels, task identity, node identity, and version. Use short genuine code excerpts with immutable source attribution rather than an invented ideal reconcile loop.

Provide an optional Docker integration track only for the reader's disposable host. Require explicit opt-in, daemon/socket permission checks, captured container IDs, and cleanup by lab-owned IDs or labels. Existing runtime integration tests use `ORCH_DOCKER_INTEGRATION=1`; retain that exact gate. No live Docker execution occurs while generating the pack. Do not imply fake-runtime success validates daemon behavior or restart-safe distributed convergence.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/03-check.json` with each case's initial service/task/container state, expected directive, observed directive, event count, and ownership conclusion. Require repeated unchanged reconciliation to avoid extra pending tasks and duplicate transition events within the tested package contract. Verify scale-down order from actual implementation and demonstrate the preservation of failed non-restartable tasks.

Machine-check that the unrelated container survives every cleanup case and that deleted service terminal state waits for removed-task reports. Record any missing-container transition rejection with exact error and state rather than changing an assertion to disguise a bug. Include raw test output, source SHA, fixture hashes, and explicit runtime mode. If a harness needs internal package access, place a teaching copy under `books/inside-orch/examples/teaching-extensions` and document its diff. Finish with a comparison table: desired-state replica reconciliation, local Docker drift reconciliation, process restart, and database restoration, each with owner, evidence, and remaining limitation.

## Immutable starting references

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [internal/docker/docker_integration_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker_integration_test.go)
- [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go)
