# Observation contract

Source edition `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. Reviewed 2026-10-13T00:35:06.866797+00:00. Status: source-inspected contract; experiments have not been executed by this document.

## Three independent statements

The API stores **intent and reported state**. An agent reports what it believes happened. Docker inspection and a direct application request independently observe a local runtime effect. Collect all three before describing convergence. `/readyz` has a fixed response in [internal/api/api.go:430](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L430-L443); HTTP readiness proves handler reachability, not database durability, leadership, or replica health. A successful controller pass may have produced no task; a task assignment event is a placement decision, not a running container.

## Exact instruments and live paths

The declarations below were extracted from immutable source bytes, not copied from dashboard labels. Server startup passes a shared metrics object to the API, scheduler and rollout controller; agent startup passes its own object to the runner and Docker wrapper. See [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L238), [cmd/orch-agent/main.go:45](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-agent/main.go#L45-L99), [internal/docker/metrics.go:19](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/metrics.go#L19-L101).

| Instrument | Default execution scope | Source |
| --- | --- | --- |
| `api_requests_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L45) |
| `api_request_duration_seconds` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L49) |
| `scheduler_runs_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L54) |
| `scheduler_errors_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L58) |
| `scheduler_scheduling_attempts_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L62) |
| `scheduler_scheduling_failures_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L66) |
| `scheduler_tasks_claimed_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L70) |
| `scheduler_assignment_conflicts_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L74) |
| `scheduler_duration_seconds` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L78) |
| `reconciler_runs_total` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L83) |
| `reconciler_errors_total` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L87) |
| `reconciler_duration_seconds` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L91) |
| `tasks_created_total` | partial integration; rollout increments, direct memory placement does not use this counter | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L96) |
| `tasks_failed_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L100) |
| `rollouts_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L104) |
| `rollout_failures_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L108) |
| `autoscaler_decisions_total` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L112) |
| `autoscaler_errors_total` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L116) |
| `autoscaler_recommendation_replicas` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L120) |
| `controller_leader_status` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L124) |
| `controller_leader_acquisition_failures_total` | implemented package; no default controller wiring | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L128) |
| `dns_queries_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L131) |
| `dns_errors_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L132) |
| `heartbeat_success_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L280) |
| `heartbeat_failure_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L284) |
| `docker_operations_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L288) |
| `docker_operation_errors_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L292) |
| `task_state_changes_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L296) |
| `healthcheck_success_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L300) |
| `healthcheck_failure_total` | runtime-integrated | [declaration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L304) |

`reconciler_runs_total`, errors and durations can remain zero because the standalone reconciler is not constructed by default main. Autoscaler and leader label series may be absent until package methods instantiate labels. Absence is not successful behavior. `AddStoppedTasks` is a no-op in the metrics implementation, so do not invent a stopped-task counter. `tasks_created_total` counts callers, not every domain task creation. Counters reset with the process; an increasing workload can coexist with a zero value after restart.

## Case-study evidence worksheet

`labs/observations.json` defines assignment, stale status, replica health, rollout, heartbeat, failed GitOps sync, quota, jobs and Docker inspection contracts. Record UTC observation time, namespace, service ID/version, deployment ID, job ID, task ID, node ID, container ID, desired/actual status, request ID, event ID and independent endpoint outcome. Empty identifiers are explicitly not applicable; never substitute a new task ID for the old identity in an adoption claim. Keep the pre-fault snapshot and the post-fault snapshot as distinct files.

1. Read desired replicas and version from service state.
2. Read matching tasks and each node's heartbeat age.
3. Correlate the agent's report and event with the same task and container labels.
4. Inspect Docker state, exact HostConfig and local volume identity.
5. Request the application endpoint separately, then record what was cleaned up.

An old-version replica in `running` may count toward rollout availability by [pkg/types/lifecycle.go:297](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L297-L300) without passing an application probe. However, `rolloutStateFor` counts new-version targets only when `actual_status == healthy` (internal/rollout/rollout.go:358–385). Record the exact source predicate instead of silently replacing it with your preferred healthy definition. Stale-status tests must state the guard under examination: wrong node, desired removal, or terminal task. Some repeated same-state reports are deliberately idempotent; age alone is not a universal rejection predicate.

## Events and audit records

[internal/events/events.go:11](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/events/events.go#L11-L99) names lifecycle events and normalizes UTC timestamps/severity. `Emit` returns nil for a nil store; non-strict append failures are logged and do not undo the domain mutation. Scheduler transaction-aware claims request strict emission when appropriate. Therefore missing events can mean a collection failure, best-effort append failure or a path that does not emit that event; absence alone is not evidence the mutation never occurred.

Audits contain `namespace`, `actor_type`, `actor_id`, `action`, `target_type`, `target_id`, `request_id`, `source_ip`, `outcome`, metadata and timestamp in [internal/audit/audit.go:25](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/audit/audit.go#L25-L95). Audit metadata redaction matches substrings in keys (authorization, cookie, credential, database_url, dsn, key, password, secret, token); URL-key values have user-info redacted. This does not scrub arbitrary values, query-string credentials in a harmlessly named field, free text, stdout or every error. Notification redaction is a different implementation and cannot be treated as a universal sanitizer. Capture synthetic tokens only; never export bearer headers or actual secret environments.

## Dashboard and alert interpretation

Prometheus scrapes and evaluates every **15 seconds** in [deploy/monitoring/prometheus.yml:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/prometheus.yml#L1-L26). Alert `for` periods begin only when an expression is observed continuously true; range windows, missed scrapes and evaluation phase add delay. `OrchAgentHeartbeatMissing` uses `increase(heartbeat_success_total[2m]) == 0` plus `for: 5m`; missing series are not equivalent to zero and an absent target needs the separate `up` alert. `DatabaseUnavailable` observes exporter reachability, not a server persistence dependency. `NodeOffline` observes the agent's metrics endpoint, not the control plane's node timeout decision.

All dashboard `expr` fields and alert expressions are checked by the accompanying source audit. Declared reconciler queries refer to a package not wired by default. Leader/autoscaler instruments also lack active controller calls in the default binary. Low-cardinality API route labels are normalized route patterns, operation/status/controller/decision labels must remain finite sets. The autoscaler recommendation's `service_id` label is inherently per-service and requires bounded retention; do not put task IDs, URLs, users or request IDs in added metric labels.

## Measurements and review limits

No benchmark duration, sample count or throughput is reported here. A later performance record must include source SHA, build flags, CPU/memory, fake versus real runtime, warm-up, measured duration, repeats, sample count, failures and cleanup. Never compare a single fake-agent throughput sample with real Docker capacity. Source inspection validates names and call paths; it does not validate Prometheus reachability, alert firing, Docker cgroups or recovery timing.
