# Ordered laboratory execution review

Pinned source: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. All eight mandatory laboratories were freshly repeated in order on 2026-10-13, with eleven command records and separate retained stdout/stderr. The first run began at 01:39:06 UTC; the last ended at 01:58:56 UTC. `validation/labs/summary.json` links each `lab-01.json` through `lab-08.json` result and corresponding combined `.log`. Every result records actual commands, working directory, UTC boundaries, exit codes, configuration hashes, observations, cleanup and rerun conditions. No mandatory prerequisite remains blocked for these recorded scopes.

## What actually ran

| Lab | Observed work | Scope boundary |
| --- | --- | --- |
| 01 | Two fresh authenticated server processes; real agent/Docker deployment, HTTP, logs/event, scale two/one, delete; exact three container IDs independently absent afterward | Restart loses active maps; separate daemon experiment has cached images and no published workload port |
| 02 | Twenty-four fixture permutations, candidate/assignment decisions, three uncached concurrent scheduler tests | Planner and competing task claims are separate from global database resource reservations |
| 03 | Fifteen agent/store-reconciler drift cases with captured identities, first/second-pass events and stop order | FakeRuntime and injected stores; missing-running-container recovery can hit a real lifecycle rejection |
| 04 | Seven rollout checkpoints, bounded cohort counts, rollback, failed history and operation/status conflicts | Injected health and control-plane reports, without live traffic measurement |
| 05 | Thirty API/issuer/envelope/probe cases; actual owned loopback HTTP/TCP, wrong-key and wrong-node rejection, forbidden-channel scans | No public network or daemon; authorized assignment plaintext remains an explicit permitted channel |
| 06 | Twenty-eight namespace/quota cases, concurrent admission, redaction and separately constructed server-state isolation | Actual in-process handlers and MemoryService; no PostgreSQL quota or hostile runtime isolation claim |
| 07 | Twenty-six local Git, CLI parser, Job and Cron cases, including failed fetch, partial apply, name-based prune and Belgrade DST | Real local Git; task reports, log transport, store and clock are injected |
| 08 | All sixteen migrations, repeat Up, refused unapproved Down, assignment CAS, session advisory locks, canary dump/restore and wrong-key rejection; fresh child databases removed | Separate teaching extension; default server persistence remains absent. Fixed-seed fake load is a distinct observation |

The source export and disposable working copy still match all 361 locked file hashes. All eight lab definitions' input hashes matched before the result records were written. The environment capture names Linux/x86_64, Go 1.25.0, Docker CLI 29.8.2, Compose v5.6.0 and the verified default Docker context using `unix:///var/run/docker.sock`. Source-export builds use the exact GOROOT and `-buildvcs=false`; no baseline source was repaired.

Atlas connects the learning problems, not an undocumented shared process. Each result explains its explicit state reconstruction. Root alone executed PostgreSQL mutations and daemon cleanup; the reviewer executed labs 02–07. Lab01's exact container cleanup records confirm absence. Lab08's owned source and restored child databases were created empty and both dropped. Other lanes discard process-local state, close owned listeners, or remove temporary local Git fixtures. No broad prune, shared database reset or production resource is part of this review.

## Findings and their acceptance conditions

**LAB-001** preserves the untouched store fixture's actual missing `agent_version` failure: migrations 1–14 omit the column added by migration 16. The accepted repair is editorial separation of that failure from the independently executed all-sixteen-schema teaching extension. Both histories remain retained; a green extension does not convert the original fixture into a pass.

**LAB-002** retains the original Lab07 harness failure caused by incomplete CLI setup. The corrected harness supplies an explicit client/server parser context without contacting that server. The final canonical author run and fresh review run both pass all 26 cases. Failed logs were not erased.

**LAB-003** records the actual agent/control-plane failure boundary discovered in Lab03: a missing running container can trigger a pulling report that legal lifecycle checks reject. A mismatch cleanup can precede a later rejection. The book and lab identify this as a tested limitation; passing the test means the expected failure was observed, not that recreation succeeded. No application feature was silently implemented.

Each finding is resolved within the book's acceptance scope, with exact evidence paths and consequences in the JSON. The original application limitations remain visible. No claim's validation was promoted merely because another lab passed: original source inspection and scoped executed claims retain their schema and evidence boundaries.

Lab08's fixed-seed fake tool created 60 tasks, reported 39 running and 21 failed, 20 scheduler and 30 reconciliation iterations, and zero scheduler/reconciler errors. Its 34.097 microsecond average and 1.11756 millisecond convergence duration describe that in-process run on this environment. They do not measure real image pulls, container density, database throughput or a universal performance guarantee. Public artifact/link verification and visual typesetting remain separate release gates.
