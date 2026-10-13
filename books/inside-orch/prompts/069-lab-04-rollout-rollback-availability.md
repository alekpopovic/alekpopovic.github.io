# Prompt 069 — Lab 04 — Rollout, rollback, and availability accounting

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

Read `internal/rollout/rollout.go`, rollout tests, `internal/controlplane/operation_lock_test.go`, `internal/controlplane/rollback_test.go`, service version logic, `pkg/types/lifecycle.go`, `docs/ROLLOUTS.md`, maintenance enforcement, and CLI/API rollout flags and DTOs. Confirm the exact health gate and terminal conditions in code. Inspect the distinction between running and healthy, reserved pause behavior, and the absence of a progress deadline or automatic rollback.

## Build the lab

Create `books/inside-orch/labs/04-rollout-rollback/README.md`, `lab.json`, complete scenario inputs, and an optional deterministic teaching extension. Use three replicas with `maxUnavailable=0` and `maxSurge=1` for a clear baseline. Trace every controller pass with old-version active tasks, target-version active tasks, target healthy tasks, pending stop directives, and deployment status. Ask the reader to predict whether the next action creates, waits, stops, fails, or completes.

Inject slow target health, a target failure, exhausted placement capacity, and stale status reports through existing test seams. Show the safe waiting case when one extra replica cannot be placed and distinguish rollout availability accounting from measured external request success. The controller's model is not proof that an application endpoint experiences no downtime. A service without the required healthy transitions may expose a different boundary; keep that observation explicit.

Demonstrate operation concurrency: a repeated identical active rollout is idempotent, a different rollout conflicts, scale is blocked during active rollout, and delete cancels active work. Cite actual tests or execute an isolated harness with fixed IDs and clocks. Do not invent pause/resume, forced active rollback, progress deadline, or automatic failed-rollout recovery commands.

For rollback, retain the failed deployment history and create a separate rollback deployment targeting the previous successful version. Show the initial baseline special case from source and the rejection when no eligible previous version exists. Inspect maintenance-window enforcement and audited emergency bypass independently; never add `--force` to every example as a default convenience.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/04-check.json` and a timeline CSV with per-step replica budget calculations, health counts, deployment IDs/versions, terminal immutability, and operation outcomes. Machine-check surge never exceeds the configured modeled bound in the deterministic scenario, old-version stops respect the implementation's availability gate, repeated passes do not duplicate target work, and rollback preserves previous terminal records.

Require at least six timeline checkpoints plus three negative operation cases. Compare invariants against actual tests and explain any difference between documented semantics and shipped composition. Test outputs must include real exit codes; source-derived timelines must carry an `expected` label and remain separate from observed values. The Docker track is optional reader activity with explicit prerequisites and workload cleanup; it must not claim measured availability without a real probe trace, timestamp resolution, and sampling contract. Finish with complete answers explaining why a failed rollout can require an operator decision and why a durable controller restart differs from restarting the memory-based server.

## Immutable starting references

- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go)
- [internal/controlplane/rollback_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/rollback_test.go)
- [docs/ROLLOUTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ROLLOUTS.md)
