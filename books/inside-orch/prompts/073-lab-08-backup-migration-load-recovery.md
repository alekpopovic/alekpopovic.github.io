# Prompt 073 — Lab 08 — Backup, migration, load, and recovery boundaries

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

Read `scripts/backup-db.sh`, `scripts/restore-db.sh`, `internal/migrations/manager.go`, migration tests, all migration pairs, `internal/version/version.go`, server schema-check composition, `cmd/orch-loadtest/main.go`, scale tests, `docs/BACKUP_RESTORE.md`, `docs/MIGRATIONS.md`, `docs/UPGRADES.md`, `docs/LOAD_TESTING.md`, and `docs/SCALE_TESTING.md`. Trace exact script arguments, required database URLs, migration locking, and down-migration authorization.

## Build the capstone lab

Create `books/inside-orch/labs/08-recovery-boundaries/README.md`, `lab.json`, experiment inputs, and recovery verification instructions. Separate three tracks: offline schema/source analysis, fake-agent load measurement, and optional reader-run PostgreSQL backup/restore into a disposable replacement database. No Docker or PostgreSQL operation runs during authoring. Every database URL must be supplied by the reader's lab environment; never embed credentials or default to a production connection.

Use a precise inventory of desired state, actual observations, events/audit, encrypted secret rows, envelope-key material, Docker images/volumes, runtime configuration, and monitoring data. State which belong in a database dump and which require separate protection. Most importantly, demonstrate that a dump of the existing database cannot recover live intent owned by the shipped MemoryService. A successful restore proves restoration of database artifacts within its scope.

For migrations, inspect up/down directions, run status/up/up idempotency in the optional database track, verify locking/compatibility tests, and show explicit rejection of down without `--allow-down`. Do not execute destructive down or clean restore against an existing environment. Prefer restore into a fresh named replacement and check schema, row counts, references, and secret decryptability with the same envelope key.

For fake load, use the actual `orch-loadtest` flags with a fixed seed and bounded duration. Capture machine/Go versions, workload size, raw counters, errors, convergence timing, and execution status. Repeat only if the experiment asks a meaningful variance question. No fake-agent number may be described as Docker performance, PostgreSQL throughput, production capacity, or a service-level objective.

Define recovery objectives as a proposed measurement contract: exact start/stop events, intended-state completeness, missing secrets, orphan containers, agent re-enrollment, application validation, and residual data loss. A future durable extension can supply its own evidence separately, but cannot retroactively change claims about the locked release.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/08-check.json` with track status, prerequisite checks, dump hash, source/target database identities redacted safely, schema versions, row-count comparisons, decryption outcome, load inputs/output, and recovery claim scope. Machine-check migration pairs and declared compatibility ranges, repeat-up idempotency when executed, and restoration only into the lab's replacement target.

A recovery pass requires all defined restored-artifact checks; full live orchestration recovery remains `unsupported_default_runtime` unless a separately labeled extension is executed and tested. Guard scripts must reject empty target identity and accidental source/target equality. Confirm cleanup deletes only lab-owned files/databases and preserves raw measurement evidence. Finish with complete answers explaining why backups, restart safety, controller leadership, and measured workload capacity are distinct guarantees. The capstone must leave the reader able to audit a future production proposal without confusing repository scaffolding with proven behavior.

## Immutable starting references

- [scripts/backup-db.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/backup-db.sh)
- [internal/migrations/manager.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go)
- [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)
