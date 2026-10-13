# Appendix E - Operator Runbooks and Measurement Contracts

An operational procedure needs a supported mode, an observation and a stop condition. Otherwise a useful diagnostic command can become an uncontrolled repair attempt. These runbooks target disposable Atlas laboratories and the pinned implementation. The default server keeps live state in memory; the database restore procedure applies to an explicitly constructed extension, not to that default process.

The companion index contains ten complete playbooks with trigger, real command paths, triage order, decision points, bounded action, verification and rollback or stop condition. The condensed table is a navigation aid. Supply the dedicated namespace and captured resource IDs from the laboratory rather than pasting placeholders into a shared cluster.

| Incident | First observations | Decision that prevents a misleading repair |
| --- | --- | --- |
| pending-tasks | `orch service inspect`, `orch service ps` | If no eligible capacity exists, distinguish a valid pending result from a failed scheduler loop; ordinary immediate placement can bypass Plan constraints. |
| unhealthy-workload | `orch service ps`, `orch service inspect` | Decide whether unhealthy stays retryable or MemoryService converts it to failed under replacement policy; new rollout success requires healthy. |
| agent-enrollment | `orch node ls`, `orch node inspect` | Distinguish incorrect authority, rotated-token response loss, wrong-node access and a memory-server restart that erased credential records. |
| node-loss | `orch node inspect`, `orch service ps` | Stateless replacement is eligible; stateful work remains local for manual recovery. Neither implies the old process stopped. |
| drain-capacity | `orch node drain-status`, `orch node inspect` | If replacement capacity is unavailable, waiting is correct; drain complete concerns desired work and can precede physical removal. |
| rollout-failure | `orch rollout status`, `orch service inspect` | Choose between waiting for an owned probe repair and an explicit rollback; a raw running target is not newHealthy. |
| gitops-drift | `orch gitops ls`, `orch gitops status` | A fetch/parser failure should not authorize pruning untrusted broad paths; distinguish drift observation from a successful apply. |
| quota-denial | `orch quota get`, `orch service ls` | Zero quota fields mean unlimited; a racing mutation can legitimately win before this request. Requested reservations are not measured Docker consumption. |
| memory-restart | `orch service ls`, `orch node ls` | This is expected process-local loss, not proof PostgreSQL restore failed; surviving containers need careful label reconciliation. |
| postgres-restore | `orch cluster check-upgrade` | A successful pg_restore exit is insufficient; the current memory binary does not read this database as live intent. |

## Process readiness and control-loop evidence

`GET /healthz` and `GET /readyz` are process responses. They do not test durable storage, validate every worker’s reachability or prove that desired replicas are serving users. The optional schema check can fail startup on an incompatible database; it does not turn readiness into continuous database health or replace the live MemoryService constructor.

The executable starts GitOps, cron, scheduler, rollout and node monitoring, plus usage capture and retention work. DNS is conditional on its configured listener; profiling uses a separate explicitly enabled listener. It does not start the standalone reconciler, autoscaler or leadership package. Their registered collectors describe available instrumentation contracts, not proof those loops are active. A zero or absent sample must be interpreted according to that wiring.

Use counters for accumulated occurrences and gauges for current values. API request counters and histograms have method, route and status labels. Agent Docker operation counters use operation labels; task-state change counters use status. The healthcheck success/failure counters have no label keys. Do not invent a namespace label because a dashboard would find it convenient. The companion collector inventory records exact names, types and label keys from source.

An alert rule or suggested threshold remains a proposal until its collector, scrape path, scope and action were configured and tested. A service-level objective additionally needs a user-facing success definition and an observation window. A scheduler counter cannot substitute for gateway request availability, and requested CPU cannot substitute for Docker consumption.

## Measurement contracts

| Question | Unit | Start/denominator and finish/numerator |
| --- | --- | --- |
| placement-success | ratio | Cohort snapshot to first assigned observation |
| task-convergence | seconds | Accepted service version to first complete matching healthy population |
| replacement-latency | seconds | Server node_lost/failed decision to replacement actual healthy |
| rollout-health-budget | tasks | Every controller snapshot until terminal deployment |
| heartbeat-age | seconds | Heartbeat update to each monitor observation |
| drift-recovery | seconds | Observed drift state to successful matching apply/version |
| quota-usage | millicores and bytes | Same namespace mutation/snapshot boundary |
| cron-occurrence-uniqueness | count per scheduled instant | Occurrence selection to persisted LastScheduleAt/created job identity |
| backup-recovery-completeness | ratio and seconds | Confirmed canary backup boundary to successful restore+verification |

Each contract explicitly records clock origin, sampling, workload size, warm-up, missing-data handling and limitations. Local elapsed durations should use one monotonic observer clock where possible; preserve server UTC timestamps for ordering and interpretation. Never subtract monotonic readings from separate processes. When wall-clock comparisons are unavoidable, record synchronization assumptions and clock uncertainty.

Missing completion is censored or timed out, not a zero latency sample. A denominator must identify the same cohort as its numerator. For quota usage, zero means unlimited rather than a division operation. For cron, occurrence identity includes the cron resource and scheduled instant; it does not prove an external side effect ran exactly once. For backup recovery, matching count alone is insufficient: compare stable IDs, content digests, schema and synthetic secret decryptability.

## A bounded, actual fake-agent experiment

The following command was executed from the separate disposable Orch module using the source-built Go 1.25.0 binary. It performs **in-memory fake-node/status simulation**. It does not pull an image, start Docker containers, use PostgreSQL or measure network serving throughput.

```sh
orch-loadtest --nodes 3 --services 12 --replicas 2 \
  --failure-rate 0.1 --duration 1s --seed 17
```

There was no separate warm-up: initial service creation contributes to the reported convergence timing, then a one-second simulation follows. The recorded host was Linux x86_64 with 12 logical CPUs; the evidence file retains the exact kernel/glibc platform and Go version. That machine description is context, not a portable capacity estimate.

Actual output was 24 tasks created, 8 running and 16 failed at the final snapshot, 10 simulation iterations, 12 initial reconciliation iterations and zero reported scheduler/reconciler errors. The timing fields are retained in raw evidence; their microsecond scale must not be presented as Docker startup latency. A deterministic random seed controls failures, but scheduler timing and wall-clock measurement remain machine dependent. A zero exit means this bounded simulation ran, not that all tasks converged healthy.

A future durable-cluster plan must first name an explicitly wired service/store, transaction and leadership paths, exact schema and credential recovery. Then measure accepted intent through real worker execution separately from database throughput and backup reconstruction. Use captured canaries and failure windows; do not attach performance numbers from this fake run to that future architecture.

## Recovery and laboratory navigation

The restore playbook uses a new disposable target and all sixteen migrations. Preserve the envelope key independently: restored encrypted rows cannot be decrypted from KeyID alone. Stop on schema or canary mismatch and retain the original target. Database success cannot recover MemoryService maps that were never written there, and database backups do not contain Docker volumes or container filesystems.

Each laboratory records its own actual or expected evidence class. Follow the eight laboratory guides for initialization, placement, drift, rollout, security, namespaces, GitOps/cron and recovery. They should be read alongside the corresponding playbook; a source-derived procedure is not a transcript that the action was already performed on your machine.

- [Initialization and restart](../../labs/01-initialization-restart/README.md)
- [Scheduler placement](../../labs/02-scheduler-placement/README.md)
- [Reconciler drift](../../labs/03-reconciler-drift/README.md)
- [Rollout and rollback](../../labs/04-rollout-rollback/README.md)
- [Security boundaries](../../labs/05-security-boundaries/README.md)
- [Namespaces and quotas](../../labs/06-namespaces-quotas/README.md)
- [GitOps, jobs and cron](../../labs/07-gitops-jobs-cron/README.md)
- [Recovery boundaries](../../labs/08-recovery-boundaries/README.md)

The boundary map is deliberate: pending/drain incidents test placement; unhealthy work and rollout test runtime execution; enrollment and node loss test identity; GitOps and quota test intent mutation; memory restart tests process-local ownership; restore tests the database extension. Crossing one boundary successfully does not close every other incident path.

Sources: [operations](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OPERATIONS.md), [registered collectors](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go), [server composition](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go), [fake-load implementation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go), and [backup/restore scope](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md).

Source-backed boundary statements for this appendix are indexed in the [appendix claim record](../../validation/evidence/appendices.json). Detailed command, state, exercise and reference tables retain their own source provenance.
