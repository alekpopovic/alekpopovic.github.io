# Prompt 064 — Appendix E — Operational playbooks and measurement contracts

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

Read `docs/OPERATIONS.md`, `docs/OBSERVABILITY.md`, `docs/RELIABILITY.md`, `docs/LOAD_TESTING.md`, `docs/SCALE_TESTING.md`, `docs/PERFORMANCE.md`, `docs/BACKUP_RESTORE.md`, `docs/UPGRADES.md`, `internal/metrics/prometheus.go`, node monitoring, control-plane operations, migration entrypoints, `cmd/orch-loadtest/main.go`, backup/restore scripts, and the Grafana dashboard. Verify exact metrics, labels, command syntax, and applicability to the memory server.

## Produce operational references

Create `books/inside-orch/manuscript/appendices/e-ops-measurement.md`, `books/inside-orch/runbooks/index.json`, `books/inside-orch/runbooks/playbooks.md`, and `books/inside-orch/reference/measurement-contracts.json`. Write ten playbooks: pending tasks, unhealthy workload, agent enrollment failure, node loss, drain without capacity, rollout failure, GitOps sync/drift failure, quota denial, memory-server restart, and future PostgreSQL restore rehearsal. Each must specify trigger, observation commands, triage order, decision points, bounded action, verification, rollback or stop condition, and the exact supported mode.

Distinguish `/readyz` process readiness from backing-store health; document why a green readiness endpoint does not prove durable orchestration. Explain which background controllers the server actually starts and which leadership/autoscaling metrics may reflect isolated package contracts. Classify alert ideas as proposals until configured and tested. Use source-defined event names, metric types, labels, and error codes; never invent monitoring outputs.

Define measurement contracts for placement success, task convergence, replacement latency, rollout health budget, agent heartbeat age, drift recovery, quota usage, cron occurrence uniqueness, and backup recovery completeness. For every metric, state numerator/denominator or start/stop event, unit, timestamp source, sampling, missing-data behavior, workload size, warm-up, and limitations. Requested resources are reservations, not observed Docker usage; task runtime accounting is not billing. Avoid combining counters with gauges in a way that invents rates.

Provide an experiment sheet for the fake-agent load tool: exact flags, seed, service/node/replica counts, machine and Go versions, duration, raw output, and run status. State prominently that it exercises in-memory control-plane behavior, not Docker startup throughput or PostgreSQL throughput. Provide a separate future durable-cluster measurement plan without fabricated performance numbers or promised service-level objectives.

## Acceptance and evidence

Create `books/inside-orch/validation/064-ops-contract-check.json`. Programmatically resolve all command references against Appendix A, verify every cited metric and label against registered collectors, and ensure all ten playbooks include verification and stop conditions. Parse the measurement JSON and reject missing units, undefined denominators, ambiguous clock origins, and claims without an evidence class.

All irreversible or environment-wide actions must be outside the default exercise path and explicitly scoped to a disposable lab. Backup instructions must state the envelope-key requirement and that the default server does not persist live state in the database. Record actual measurement results separately from empty experiment templates; a template must be labeled unexecuted and contain fully defined inputs rather than invented values. Finish by mapping each playbook to the architecture boundary it tests, so an operator can tell whether the incident concerns intent, placement, runtime execution, identity, or the database extension.

## Immutable starting references

- [internal/metrics/prometheus.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go)
- [docs/OPERATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OPERATIONS.md)
- [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go)
- [docs/BACKUP_RESTORE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md)

## Native appendix contract

Use the first H1 exactly `# Appendix E - Operator Runbooks and Measurement Contracts` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/e-ops-measurement.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.
