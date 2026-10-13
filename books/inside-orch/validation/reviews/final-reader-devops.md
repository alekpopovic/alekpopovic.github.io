# Final skeptical reader review — DevOps lens

Recommendation: proceed to a local, reviewable handoff with one accepted minor naming erratum. There is no blocking operational teaching defect in the reviewed final edition. This is an AI review with a distinct DevOps lens, not an external human endorsement, live deployment test or production certification.

The accepted 096 gate is bound by SHA256 `d4651b1e5f5d8daac5ebaa7352b950b3cb04faf14402886576e221fea2fa4278`. The final PDF is `a734dd82a27fde589fd81cf9755693401f8b1abbe9a055d1ebe2e482916caee3`, EPUB `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`, reader ZIP `040359760ed4ae64623c3907c7ff3433a3da8bcb0278f22a152b39241ce3ab0a` and source ZIP `052901306f6e0b0073f45752193879df6f8c7bf88b46251f43d03c87a8699e06`. Detailed inputs and evidence hashes are in [final-reader-devops.json](final-reader-devops.json).

## What was challenged

I reread all eight final lab guides, the common environment contract and ten playbooks, then checked critical final passages on rollout, node loss, leadership, migrations, failure recovery and release. The prior 078/079 all-chapter operational reviews remain supporting history; the final heading/lab inventory and exact 096 gate bind the complete edition. Chapters 09–16/25–32 and Labs 06/07 include my authorship, so my scrutiny of them is explicitly self-review within this lens. Other agents provide separate lenses. A path/hash inventory is evidence of the inspected edition, not proof that every word was reread anew.

| Adversarial assertion | Evidence and reader consequence |
| --- | --- |
| Two memory servers are HA | Lab 06 actually observes 404 across independently constructed handlers; a fresh default binary loses objects. The final text requires explicit shared-state composition. |
| A task CAS reserves all capacity | Full-schema PostgreSQL reports one winner/one conflict for one row. Chapters 09/10/28 separate that from global CPU/port reservations and ordinary immediate assignment. |
| Offline/drained means physically fenced | Chapter 19 uses strict heartbeat cutoff, conservative stateful handling and explicit live-overlap warnings. Fake bookkeeping/returned-node tests do not become an actual packet partition. |
| Declared limits protect ordinary containers | The owned Docker flow observes ordinary memory/CPU zero while direct supplied adapter limits are populated. All three captured containers have independent absence checks. |
| A test named restart proves durability | The pinned chaos test retains its control-plane object. Chapters 17/37 distinguish controller reconstruction from the actual fresh-process loss record. |
| Failed GitOps sync is atomic | The actual second-manifest failure retains the first applied replicas while LastRevision remains old. Chapter 30/Lab 07 preserve partial apply, status mutation and name-based prune caveats. |
| Lease.Done and Release nil prove unlock | The actual two-pool PostgreSQL record retains the lock after cancellation/release and allows the competitor only after original pool close. Chapter 34 identifies the defect without prescribing termination of unknown sessions. |
| Green default tests cover databases | Six named external test skips remain explicit. The original owned store run still has two 42703 failures and one pass; the all-sixteen-schema extension is labelled separately. |
| A restored database recovers default live intent | Lab 08 checks fresh targets, all sixteen migrations, row counts, matching canary/key and wrong-key rejection. The default binary still constructs MemoryService. |
| Compose and broad cleanup are safe defaults | ENVIRONMENT warns of Docker socket authority, upstream unrestricted ports, moving tags and broad prune. Actual Docker fixtures publish no workload ports and delete only captured IDs. |

## Accepted minor erratum: FINAL-OPS-001

The common environment contract names `inside_orch_lab_<run>` without explicitly requiring `_test`. The book's guard accepts that prefix-only name, but upstream `internal/store/postgres_test.go:556–565` refuses it before resetting the schema. A reader can therefore pass the guard's `--check-only` and then receive a safe refusal. This is a procedural gap rather than a production safety bypass; the actual executed lab names already ended `_test`.

The new in-process [actual demonstration](097-devops-database-name-contract-command.json) passes synthetic container dictionaries directly to `validate_target` for a prefix-only and a suffixed name. Both pass the book guard; the first lacks the inspected upstream-required suffix. It opens no socket, inspects no Docker daemon and executes no SQL/reset. The probe source is retained in the JSON report.

Use `inside_orch_lab_<unique_run>_test` in the handoff. The parent accepted this minor frozen-edition erratum and will state the workaround in release notes/handoff. A later revision should explicitly document the suffix and reject its absence in the book guard with a unit case. No source snapshot, manuscript, format, public asset or accepted archive was changed by this review.

## Operational acceptance and remaining limits

The guides identify privileges, exact source/tool prerequisites, expected versus captured results, stop conditions, ownership, and cleanup. Docker daemon access remains broad host authority. Destructive store tests require a fresh labelled loopback-only database; keys and credentials stay out of logs. Cleanup records use captured IDs/names, with no daemon-wide prune. Source-only verifiers are not advertised as fresh experiments.

No external laboratories or formats were rerun here: the exact 096 gate and fresh 076 records already establish those bounded executions. The sole new command demonstrates the naming issue safely in process. There is no newly executed physical partition, production restore, live HA failover or outside human signoff. None is implied by a passing recommendation. Proceed to 098 only after the parent reconciles all three 097 lenses and retains this erratum and the existing runtime limitations.
