# Lab 07 — Git intent, job attempts and scheduled occurrences

By Aleksandar Popovic. Source edition: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`.

## Problem and scope

Atlas wants Git to describe services, a report to finish once, and a daily report to follow Belgrade wall time. These are three different controllers with different failure windows. This teaching extension runs real local Git, the locked CLI parsers and actual control-plane methods. It injects task reports, a log transport, a clock and a CronJob store. It launches no container, database or network listener. A successful exit-zero report proves the state transition after a report, not execution of the shell command in Docker.

Prerequisites: a disposable verified copy of the pinned module, Go 1.25.0, Git and IANA timezone data. Read `internal/gitops/gitops.go`, `internal/controlplane/workloads.go`, `internal/cronjobs/cronjobs.go`, `internal/cli/workloads.go`, `pkg/types/workloads.go` and their tests. Compare `docs/GITOPS.md`, `docs/JOBS.md` and `docs/JOBS_DESIGN.md` with implementation. The lab initializes `book-workloads`; no previous lab process is assumed to survive. Its connection to Lab 06 is the namespace/admission contract, not retained objects.

## Canonical fixtures and parser fidelity

`10-api.yaml` and `20-worker.yaml` are service manifests read through the actual deploy parser in lexical order. Their zero replicas avoid claiming a connected runtime. Both specify 100 millicores and 64 MiB. The Job fixtures include `kind`, name, image, command, backoffLimit and resource strings; the successful job has zero retries and the failing job has one. `cron.yaml` uses the actual CLI envelope: `schedule`, `timezone`, `concurrencyPolicy`, and `jobTemplate` image/command/resources. It deliberately omits unsupported CLI fields such as missedScheduleLimit or jobTemplate.backoffLimit. Direct controller fixtures set missedScheduleLimit separately and are labelled in-process tests.

The harness invokes the actual CLI root with an injected capture client. The parser still requires `--server`; the supplied `http://127.0.0.1:1` is never contacted because the capture client implements the called methods. The first run exposed this missing setup and failed. Its record remains `validation/labs/lab07-gitops-jobs-cron.json`; the corrected implementation adds the required CLI option. The final canonical run passed all 26 cases.

Copy `examples/teaching-extensions/lab07/main.go` into `.book-labs/gitops-jobs-cron/main.go` in the disposable pinned module, then run:

```sh
go run ./.book-labs/gitops-jobs-cron /absolute/site/books/inside-orch/labs/07-gitops-jobs-cron/fixtures
```

Use Go 1.25.0, `GOTOOLCHAIN=local`, its verified `GOROOT`, and `GOFLAGS=-buildvcs=false` for the source export. The exact executed argv, cwd and UTC interval are retained in `validation/labs/lab07-canonical-fixtures.json`, with stdout containing generated source/job IDs and full local commit SHAs. The illustrative absolute path is reader configuration. A new run must retain new records rather than overwrite the previous run.

## GitOps experiment

The program creates a uniquely owned temporary local repository, disables hooks for its Git commands, and commits only synthetic manifests. The actual CommandFetcher clones that local repository; no Git operation touches the immutable evidence repository. Fetch unavailability is separately injected and never uses a fake external host.

| Action | Prediction | Actual observed result |
| --- | --- | --- |
| Initial sync | Managed names in lexical order; recorded full revision | `atlas-api`, `atlas-worker`; source ID and revision captured |
| Unchanged sync | No false version increment | Passed, version stays 1 |
| Manual scale in warn mode | Desired/live drift visible, manual replicas retained | Drifted with replicas 2 |
| auto_revert status request | Desired replicas restored | Replicas 0; status call mutates state |
| Failed fetch | Existing objects retained and no prune | Both services remain active |
| First valid file, second invalid | Earlier application can survive later failure | API replicas 1, worker retained, LastRevision unchanged |
| Remove managed worker, sync | Worker deleted, unrelated manual service retained | Passed |
| Credential-bearing repository URL | Rejected without synthetic private value | Userinfo and token-query cases passed |

The recorded fixture revisions are real commits created by that execution, not the application source SHA. Sequential apply is not a transaction: a failed sync can leave an earlier manifest applied even though LastRevision still names the previous success. Prune uses previous managed names within the namespace; preserving a never-managed object does not establish safe ownership transfer for a reused managed name. The auto_revert status path restores recorded desired state directly; it must not be described as a new admission decision or a passive read.

## Jobs and latest-attempt logs

The successful parser fixture produces requests/limits of 100 millicores and 1048576 bytes and an explicit shell command. A real MemoryService creates an owned task, receives injected running/stopped reports with exit code zero, and marks the job succeeded. No process executes the command here.

For the failing fixture, BackoffLimit 1 means an initial attempt plus one retry. The first injected nonzero stop creates a new attempt task and pending state with Attempts 2; the second ends failed with Attempts 2. The CLI log command selects the latest attempt task ID. Its transport is an explicit fake that writes a marker to an in-memory/discarded destination; this is argument-selection evidence, not captured report output. No timed backoff, jitter, deadline, parallelism, completion count, TTL or HA uniqueness is inferred.

## Cron decisions and daylight saving

An injected clock advances from `2026-08-21T12:00:00Z` to `12:03:00Z`. With one-minute schedule and missed limit 2, Allow creates two occurrences and advances the checkpoint to `12:02:00Z`. Forbid with an already-active job creates none and leaves its checkpoint unadvanced. Replace deletes the active job metadata and creates one replacement. Suspension creates none; resuming catches up two retained occurrences. These are actual controller/store calls with an injected clock and store, not a daemon waiting until those dates.

| Belgrade scenario | UTC base | Actual computed next/due instants |
| --- | --- | --- |
| Daily local 02:30 across missing spring hour | 2026-03-28 23:00Z | Next 2026-03-30 00:30Z; March 29 02:30 does not exist |
| Daily local 02:30 across repeated fall hour | 2026-10-25 00:00Z | 00:30Z at +02:00 and 01:30Z at +01:00 |

The parser accepts exactly five cron fields. The implementation matches all specified fields, including day-of-month and day-of-week. Job creation and CronJob checkpoint update are separate operations; a crash between them can repeat an occurrence. A future durable uniqueness key such as `(cronjob_id, scheduled_instant)` would require an atomic storage design and executable recovery test. It is not supplied by this lab or the default memory server. Forbid's behavior is measured with a job already active at tick start; it does not certify one job across every catch-up loop.

## Assertions, cleanup and rerun

```sh
python3 books/inside-orch/scripts/verify_namespace_workload_labs.py --lab 07
```

The offline verifier checks retained logs and canonical hashes, all required cases, real revision forms, latest job outcomes, preservation of unrelated services and exact timezone results. A new Go run is the fresh experiment; the verifier alone is not. On failure inspect the recorded parser envelope or UTC instant before changing expected values.

The temporary fixture repository is removed by the program, GitOps checkouts self-clean, jobs are removed through supported methods, and memory state is discarded. The harness never deletes shared containers, databases or source evidence. Rerun starts a fresh temporary repository with new commits and IDs.

| Mechanism | Implemented observation | Durability or safety boundary |
| --- | --- | --- |
| Source-of-truth reconciliation | Local Git fetch, warn/status revert, name-based prune | Partial apply; same-name ownership and re-admission gaps |
| Finite execution | Owned attempts and report-driven terminal state | Injected reports; no Docker execution or persistent job recovery |
| Scheduled intent | Five-field parser, overlap choices, bounded catch-up, real timezone computation | Separate occurrence creation/checkpoint; no exactly-once promise |
| Durable occurrence deduplication | Not supplied | Requires a separately implemented transaction/uniqueness extension |
