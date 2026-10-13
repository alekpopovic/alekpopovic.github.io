# Lab 08 — Recover artifacts and state exactly what was recovered

Recovery starts with an inventory. Desired service specifications, observed task status, event and audit history, encrypted secret rows, envelope keys, Docker images and volumes, process configuration and monitoring data have different owners. A database dump can only contain what was actually written to that database. The default Orch server keeps active orchestration intent in MemoryService. Its recovery boundary cannot be enlarged by a successful backup command.

This capstone has three tracks: source/schema inspection, a bounded fake-agent load measurement, and an actual PostgreSQL restore into a fresh replacement database. It depends on the earlier lifecycle, namespace, security and placement lessons. The author-run records are specific observations, not a promise that any available database or Docker host is safe to reuse.

## Source and schema inventory

Inspect all16 up/down pairs under the pinned `migrations` directory. `internal/version/version.go` declares schema16 and accepted range15–16. Discovering a pair means a reversal file exists; it does not prove every downgrade preserves application semantics. The migration manager sorts versions, holds a PostgreSQL advisory lock, executes each up migration and its ledger insert in a transaction, and skips already-applied versions. `Status` creates its ledger table if absent, so it is not a strictly read-only database operation.

The source store fixture applies only1–14. Its actual guarded run failed two tests because current node queries refer to `agent_version`, introduced by migration16. Keep that result alongside the complete-schema teaching experiment; do not repair the immutable fixture or call the original suite green.

`backup-db.sh` requires an explicit database URL and invokes `pg_dump` in custom format. `restore-db.sh` requires a target, an existing input and `--yes`; `--clean` is explicitly destructive. These scripts cannot establish that the target is a disposable book database. This lab's additional target guards reject missing names, source/target equality, names outside the book prefix, existing replacement databases, remote endpoints, wrong container ownership labels and mismatched published ports. Restoring into a fresh target avoids overwriting a live source even when restore itself fails partway through.

## The actual disposable PostgreSQL experiment

The book creates a uniquely labelled PostgreSQL16 container with a random loopback host binding and temporary storage. Its ownership guard verifies `inside-orch.lab=true`, a unique run label, the exact configured database name and the `127.0.0.1` port mapping before any destructive suite. Do not change the guard to accept an existing production database.

The [recovery orchestrator](../../scripts/observe_database_recovery.py) creates two new, distinct lab database names only after confirming neither exists. It verifies all361 source-copy hashes, invokes the [full-schema teaching program](../../examples/teaching-extensions/full-schema/main.go), and records every executed argument vector and exit code. The program observes16 pending migrations, runs `Up`, verifies current000016 with none pending, runs `Up` again, and confirms that down without explicit permission is rejected. It does not execute an allowed downgrade in this lab.

The fixture creates one node, one service and one task. Two goroutines compete to assign the same pending task using the same expected timestamp; one succeeds and one receives conflict. This validates a per-task claim on the complete schema. It does not establish global capacity reservations, server leadership, or a durable control-plane composition.

A random one-use secret canary is encrypted and stored. Only its SHA256 digest enters the published record. `pg_dump` runs inside the owned container and the binary dump is hashed. `pg_restore` writes into the fresh replacement database. The verifier checks schema16, service/node row counts and secret decryption with the same envelope key; the decrypted digest must match. A different key must fail. The key used here is explicitly lab-only teaching material, not owner configuration. Encrypted values are not useful recovery artifacts if their corresponding key material has been lost.

The [actual recovery record](../../validation/intake/full-schema-recovery-corrected.json) captures the dump hash, full tool command vectors, source/target names, created object IDs, schema observations, restored row counts and digest comparison. Its cleanup removes precisely the two databases it created. The temporary container remains available for later isolated book checks until the root run's final cleanup; it is not a required public service.

The same program tests two independent PostgreSQL connection pools for an important leadership boundary. After cancellation, `Lease.Done` closes and `Release` returns nil, yet the other pool still cannot acquire the advisory lock. Closing the original pool releases the physical session and the second pool then acquires. This is an observed package defect in the locked release. It is separate from the default server, which does not start this leadership package.

## Bounded fake-agent measurement

Use the actual `orch-loadtest` flags: three fake nodes,30 services, two replicas, failure-rate0.02, duration2s and seed20261013. The [command record](../../validation/labs/lab08-fixed-seed-fake-load.json) and [raw counters](../../validation/labs/lab08-fixed-seed-fake-load.stdout.txt) preserve the measured run. Record the machine architecture, available CPU count, Go version and source hash alongside these inputs. A fixed pseudo-random seed stabilizes the choice stream; wall-clock loop scheduling and measured durations can still vary.

Read the load generator before interpreting its report. It uses MemoryService directly, fabricates task transitions and sleeps between ticks. Its scheduler/reconciler-labelled counters name operations in this simulator; they are not proof that standalone controller binaries or real Docker containers handled the workload. No PostgreSQL query throughput, container startup latency or HTTP service-level objective was measured. One small run is sufficient to inspect counters and their definitions; repeat only to answer a stated variance question.

The baseline source's successful fixture sizes and counters describe this bounded simulation. They cannot justify selecting production hardware, publishing a capacity number, or promising a recovery-time objective. For a real service proposal, define start and stop events, complete intended-state recovery, application checks, missing-secret handling, orphan-container review, agent re-enrollment and residual data-loss accounting before measuring a duration.

## Verify scope and clean up

`python3 books/inside-orch/scripts/verify_lab_records.py --lab 08 --mode inspection` inventories migration pairs and composition without connecting to a database. Recorded mode validates the author-run migration, restore, target-guard and load evidence and writes `validation/labs/08-check.json`. The report must keep full live orchestration recovery as `unsupported_default_runtime`; a restored-artifact pass is narrower.

Preserve the dump hash, raw measurement output and command records. Remove only owned child databases, exact captured containers and the run's temporary files. Never use source/target equality as a convenient restore shortcut. Test guard rejection before relying on a successful restore: [target guard tests](../../tests/test_recovery_targets.py) reject empty, equal and unrelated names. These tests are teaching safety controls; they do not silently modify the source project's scripts.

## Worked recovery decisions

**What does an equal canary digest prove?** The encrypted row survived dump/restore and the same envelope key can decrypt its original bytes. It does not prove every application secret was included, that keys are backed up securely, or that the default server loaded the restored secret store.

**Why are leadership and backups separate?** Backups describe past persisted artifacts. A leader lock coordinates current sessions. A complete dump cannot revoke a partitioned worker, unlock a healthy pooled session, or create fencing tokens for remote side effects. Each requires its own mechanism and test.

**What must a future durable extension demonstrate?** It needs API/interface parity, transactional mutations with events, correct restart hydration, tenant scoping, key continuity, controller reconstruction, remote ownership reconciliation, fencing and an application-level recovery oracle. Reusing the current pgx package is a starting point, not evidence that these requirements are satisfied.
