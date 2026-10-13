# Prompt 067 — Lab 02 — Deterministic placement and concurrent task claims

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

Read `internal/scheduler/scheduler.go`, scheduler unit/property/benchmark tests, `internal/store/postgres.go`, task assignment interfaces, `internal/controlplane/controlplane.go`, `internal/controlplane/agent_test.go`, `docs/SCHEDULER.md`, `docs/RESOURCES.md`, and agent capacity reporting. Reconcile stale scheduler documentation against current source for ports, heartbeat handling, and volume constraints. Trace registration, heartbeat, and Docker container spec fields before claiming end-to-end resource enforcement.

## Build the lab

Create `books/inside-orch/labs/02-scheduler-placement/README.md`, `lab.json`, complete fixture inputs, and a separate teaching extension only if existing tests cannot expose required observations. Build a deterministic scenario with three nodes, explicit capacities and allocatable resources, label constraints, public-port conflicts, and six task candidates. Choose fixed IDs and timestamps for fake-state inputs; actual runtime identifiers must be captured from responses.

Ask readers to calculate fit and score before revealing the selected node. Use requests, not limits, for scheduling arithmetic, and state CPU/memory units. Account for non-terminal assigned work, including stopping tasks. Demonstrate lexicographic tie-breaking and stable pending-task order by permuting input order repeatedly. Add one no-fit case whose pending state is a correct outcome rather than a scheduler failure.

Introduce two scheduler passes reading the same pending task and explain the expected timestamp guard. In the in-memory track, run existing concurrency/regression tests and cite their precise oracle. In the PostgreSQL track, specify a disposable database, migration prerequisites, and actual existing test gates; use row-lock/`SKIP LOCKED` behavior only if evidenced by the implementation. Do not call concurrent isolated MemoryService processes an HA cluster.

Expose the agent resource-plumbing boundary: inspect the DTO produced by registration/heartbeat and the container specification used by `CreateContainer`. Compare model resource values, advertised allocatable values, and actual Docker limits. A missing consumer becomes an explicit lab finding; do not patch the source to make the happy path pass. An optional separate extension may add instrumentation or fill the gap, but must compare its behavior against the original.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/02-check.json` with input hashes, expected placements, observed placements, capacity/port calculations, duplicate claims, and execution modes. Machine-check deterministic outputs for at least twenty distinct input permutations; exactly one successful task claim under the chosen concurrency test; no capacity overcommit within the scheduler's accounted model; no assignment to non-ready nodes; and truthful pending behavior for no-fit candidates.

Use `go test` package commands only after discovering exact test names and prerequisites, preserving logs as executed evidence. PostgreSQL absence yields `not_run`, never a synthetic claim result. Require a call-path evidence table from workload request to scheduling accounting and to runtime limit construction, with separate confidence levels. Record documentation mismatches and explain their reader consequence. Cleanup drops only the explicitly created disposable database/schema and removes extension output owned by this lab. Finish with a worked explanation of why atomic claims reduce duplicate placement races but do not solve durable control-plane wiring, leadership, or split-brain recovery.

## Immutable starting references

- [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go)
- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
