# orch technical evidence audit

Snapshot: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`, read-only source review. Source root: `evidence/orch`. Instructions read: root `AGENTS.md`. No repository edits or runtime verification performed for this audit. The observations below are source-derived; proposed labs must label their output as expected until executed.

## Editorial stance

Describe orch as a Docker-first, MVP-era Go orchestration project with substantial package-level implementation. Do not imply that every package, migration, design document, or prompt completion is a capability of the default binary. Distinguish (1) default executable behavior, (2) implemented library behavior, (3) design proposals, and (4) teaching additions. The strongest book will repeatedly trace constructor → dependency → controller loop → side effect → state transition → observable evidence.

## Top findings and exact evidence

| Topic | Source evidence | What the book must state |
| --- | --- | --- |
| Persistence | `cmd/orch-server/main.go:142–148` constructs `controlplane.NewMemoryService`; `DatabaseURL` is used for optional schema checking and migration subcommands, not normal server state | The default server does not persist its control-plane state in PostgreSQL. Restarting the process creates fresh maps. A configured database URL and successful migrations do not change that composition. |
| Service placement | `internal/controlplane/controlplane.go`, `reconcileServiceTasksLocked`, lines 2249–2330, especially 2292–2299, chooses `eligibleNodes[len(active)%len(eligibleNodes)]` and creates `TaskAssigned` | Normal service create/update/heartbeat reconciliation bypasses the independent `scheduler.Plan` resource and placement checks. The scheduler loop exists, but most service tasks already have assigned state before that loop sees them. |
| Resource enforcement | `internal/controlplane/controlplane.go`, `AgentTask` has no resource requirements field; `ListAssignedTasks` returns env/ports/security/health; `internal/agent/agent.go`, `ensureTask` omits `ContainerSpec.Resources`; `internal/docker/docker.go:434–436` maps provided limits to Docker Memory/NanoCPUs | CPU/memory fields can be normalized and planned in packages, and the adapter supports limits, but the active agent path does not propagate service limits. Do not promise cgroup enforcement for ordinary deployments from the default binary. |
| Reconciliation | Standalone `internal/reconciler/reconciler.go` is implemented and tested; server startup does not instantiate it; `MemoryService` performs its own immediate reconciliation | Teach both mechanisms as separate implementations. Do not imply the standalone reconciler is the default server's convergence loop. |
| HA | `internal/leadership/{leadership,postgres}.go` implement local/PostgreSQL electors and cancellation wrapper; no `RunWithLeadership` use outside leadership tests | Leader-election primitives are implemented; production composition is not. Two default server processes have independent memory and do not form an HA control plane. |
| Advisory-lock cleanup risk | `postgresLease.monitor` calls `l.close()` on parent cancellation/error; `close()` calls `conn.Release()`; `Release()` returns immediately when `done` closed | A pooled connection being returned is not an explicit PostgreSQL session close. Verify session-lock release on cancellation and failed unlock with real PostgreSQL before teaching the lease as complete. Treat this as an integration-test risk, not a proven observed outage. |
| Autoscaling | `internal/autoscaler/autoscaler.go` provides controller/provider interfaces, cooldown/recommendation behavior; no constructor or controller loop in server startup | Autoscaling is a implemented package/design surface, not an enabled default executable loop. |
| Tests vs restart claims | `internal/e2e/chaos_test.go`, subtest `server restarts during rollout`, reuses the same `MemoryService` and creates a new rollout controller | This is a controller-restart simulation preserving memory, not a process-restart durability test. Other chaos subtests inject reported states rather than kill real processes or Docker. |
| PostgreSQL feature parity | `internal/store/store.go` declares jobs/cron/storage/sinks interfaces, but `internal/store/postgres.go` lacks their corresponding methods; task SQL also excludes `JobID`, command and resolved mounts used by memory workloads | Schema/interface presence does not establish full PostgreSQL control-plane support. A new durable service layer needs explicit feature parity and restart tests. |

### Representative unchanged snippets

Default composition, `cmd/orch-server/main.go`:

```go
controlPlane := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope), controlplane.WithClusterPolicy(cfg.ClusterPolicy), controlplane.WithRetentionConfig(cfg.Retention))
controlPlane.SetNotificationDispatcher(notifications.NewDispatcher(controlPlane, nil))
serverMetrics := metrics.NewServer()
```

Active service placement, `internal/controlplane/controlplane.go`:

```go
node := eligibleNodes[len(active)%len(eligibleNodes)]
```

Task-specific Docker adoption, `internal/docker/docker.go`:

```go
existing, err := r.findContainerForTask(ctx, spec.TaskID)
if err == nil {
    return existing.ID, nil
}
```

Database optimistic assignment, `internal/store/postgres.go`:

```sql
WHERE id = $1 AND updated_at = $5 AND actual_status = 'pending'
```

This protects a task claim against stale state. It does not make independent planning snapshots into a global atomic capacity or port reservation. The exact return-error behavior and transaction-scoped event append are worth explaining together.

## Implemented package strengths worth teaching

### Scheduler

`internal/scheduler/scheduler.go` separates pure `Plan(PlanInput)` from I/O in `RunOnce`. Nodes/tasks are sorted by ID; candidate score orders free memory descending, then service task count ascending, total task count ascending, then node ID. Fits checks ready status, placement labels, allocatable CPU/memory, volume node affinity and single writer ownership, and port allocation. Dynamic TCP/UDP ports occupy 30000–32767, keyed by protocol. Failed tasks whose reason contains `port allocation failed` reserve ports. This string-based classification is concrete and limited, not a generic runtime-error taxonomy.

`persistAssignment` uses `store.WithTx`, stale `UpdatedAt` expectation, and strict event emission when the store is a `Transactor`. Conflicts count metrics and skip claims instead of stopping the entire pass. Use `internal/scheduler/property_test.go` to explain deterministic randomized tests (five fixed seeds, 100 pending tasks) and the difference between that coverage and a formal proof. The planning function accounts requests, not limits, and does not measure actual cgroup usage.

### Reconciler

`internal/reconciler/reconciler.go` counts current versions, stops outdated tasks, respects restart policy, scales down in a deterministic state-priority order, handles service deletion, and skips services with active deployments. Side effects and related events can share transactions. Leader lock defaults to `NoopLeaderLock`. It has a different interface from `leadership.LeaderElector`; a bridge and server wiring are required. `reconcileDeletedServices` assumes service ownership and should be reviewed before feeding it job tasks with blank ServiceID.

### Agent and Docker adapter

`internal/agent/agent.go` registers, heartbeats with jitter, polls assigned tasks, adopts managed containers, reports lifecycle states, handles HTTP/TCP health threshold counters, and cleans unassigned managed containers. Runtime dependencies can be replaced with `docker.FakeRuntime`. There is no containerd implementation: the Docker interface is a future boundary.

`internal/docker/docker.go` uses Docker Engine typed APIs, labels (`orch.managed`, service/task/node/version), idempotent create/adoption, repeated start handling, missing-stop/remove tolerance, Docker logs decoding, named volumes, security context conversion. `PullImage` discards the pull response stream and ignores the copy error; the book should not describe pull response parsing or a robust error taxonomy beyond the code. Adoption by task ID does not independently verify every supplied spec field.

Agent retry retries errors without permanent/transient classification. Heartbeat retries can prevent polling while connectivity is unavailable. Lost/expired node credentials and process restarts need carefully scoped recovery instructions. Capacity reports use runtime CPU count and `/proc/meminfo` with allocatable equal to detected capacity, not reserved host capacity or cgroup-aware discovery.

### Security and observability

User auth is HS256 JWT with roles admin/operator/viewer and namespace roles; empty JWT secret bypasses user auth. Static users can override token roles globally. Expiration is checked when `exp > 0`, so expiration is not mandatory. Bootstrap registration auth is optional when token empty. Per-node random credentials are hashed with SHA-256, expire in 15 minutes by default, and rotate on registration/heartbeat. Server-to-agent logs use the bootstrap token, not those node credentials. Native listeners use HTTP; documented production TLS termination is external.

Secrets use AES-GCM with random nonce and key ID as authenticated data. Local key material is either a suitable base64 AES key or SHA-256 of a string; this is not an implemented KMS envelope/key-rotation service. API metadata excludes plaintext, while assigned agents receive the referenced values and Docker environment necessarily exposes them to Docker/node administrators.

Policy gates forbid privileged/host network/PID/capability/host paths by default and can allow them explicitly. Assigned-port validation plus same-origin redirects harden health probes; neither justifies claiming every possible SSRF surface is solved. Notifications use URL targets and signed optional HMAC but deserve a separate outbound-network threat model. The 2026-07-14 `docs/SECURITY_REVIEW.md` includes now-stale claims that advanced security fields do not exist; current source is authoritative.

Prometheus counters, durations, events, audit records, Docker metrics wrappers, and profiling routes exist. `/metrics` is exempt from user JWT. Pprof is disabled by default and bound to loopback by default, but the debug handler itself has no authentication and configuration can change its address. Audits are best-effort. Never turn package presence into a claim all instrumentation is wired.

### GitOps, jobs, cron, storage

GitOps (`internal/gitops/gitops.go`) clones via `exec.CommandContext` (no interpolated shell), shallow single branch, rejects embedded URL credentials and lexical escaping paths, sorts YAML manifests, applies sequentially, stores revision and owned service names, optionally prunes previous managed services. A later bad manifest can leave earlier changes applied; no all-manifest transaction. There is no signature verification or private-repository credential provider here. Lexical path checks need symlink/adversarial filesystem tests before claiming a complete sandbox. Drift auto-revert lives in `MemoryService.GitOpsStatus`, so status reads have mutating behavior; periodic sync reapplies Git but is not the same mechanism.

Jobs become pending tasks and scheduler synthesizes a service view. Successful zero exit yields succeeded status; failures create new task IDs until BackoffLimit exhausted. Despite the name, retries are immediate, without timed exponential delay in `retryOrFailJobLocked`. Cron supports five fields with lists/ranges/steps and timezone; matching ANDs day-of-month and day-of-week and search is bounded to 366 days. Explain those semantics rather than assuming system-cron equivalence. Cron controller exits on a pass error, and server logs stopped instead of supervising restart. Controller initial context is default namespace; review all-namespace behavior before asserting cross-namespace scheduling. Storage is local Docker named volumes, node binding and single-writer bookkeeping, not replicated distributed storage or automatic recovery after node loss.

## Ten meaningful labs and evidence gates

| Lab | Failure / lesson | Validation | Scope |
| --- | --- | --- | --- |
| 1. Default-server restart | Create namespace then terminate/relaunch own server | Namespace present before, absent after; database unreachable with schema check disabled | Local loopback, no agent or Docker |
| 2. Pure placement matrix | Insufficient CPU/memory, mismatching labels, offline node, static port collision | `go test ./internal/scheduler -run 'TestSchedulerRandomizedInvariants|TestPlan' -v`; add teaching fixture in separate lab workspace | Package behavior, not binary promise |
| 3. Claim collision | Two claimers race for one pending task | Disposable PostgreSQL and `TestPostgresStoreConcurrentAssignTaskOnce`; exactly one success, conflict handling and single assignment event | Integration gate, destructive fixture DB |
| 4. Event/write atomicity | Event append fails after state mutation | `TestPostgresStoreWithTxRollsBackOnError`, inspect both task and event tables | Requires disposable DB |
| 5. Agent container adoption | Status report lost after Docker create; restart agent | Fake/runtime tests plus real isolated Docker test; same task ID finds same container, no duplicate | Different from server durability |
| 6. Runtime limits trace | Set service resources, inspect Docker HostConfig | Expected current active-path zero limits; adapter direct fixture sets Memory/NanoCPUs | Demonstrates a composition gap |
| 7. Offline node and late reports | Stop heartbeat, replacement, old container keeps serving | Observe service/task states/events and direct old endpoint; inspect stale report acceptance | No fencing guarantee; isolated workloads |
| 8. HA lease cancellation | Acquire/release/cancel/drop connection | Two real DB sessions; after cancellation another session must acquire, no lock remains in pool; callback stops | Existing local elector tests are insufficient |
| 9. GitOps partial apply | First manifest valid, second invalid; remove old manifest with prune | Earlier service changed, LastError populated, revision/ownership bookkeeping; test symlink escape separately | Dedicated temp repository/namespaces |
| 10. Cron/retry semantics | Compare Forbid/Replace/Allow, DST and missed schedules; job exits nonzero | Inject clock; verify Attempts, task IDs, LastScheduleAt, immediate retry and AND day semantics | Package fixtures first, durable behavior unimplemented |

## Commands and verification caveats

Core: `go build ./...`, `go test ./...`, `make lint`. Runtime dependencies are Go 1.25+, Docker, pgx, Cobra, YAML, Prometheus. Tests gated by `ORCH_DOCKER_INTEGRATION=1`, `ORCH_E2E_DOCKER=1`, `ORCH_INTEGRATION_DATABASE_URL`, and `ORCH_E2E_DATABASE_URL` skip by default. Several database tests reset schema: never point them at a real database. `TestPostgresMigrationsE2E` applies only migration 000001, so it is not evidence all 16 migrations have passed. An ordinary green `go test ./...` must report skipped external suites explicitly.

## Suggested chapter framing

The runtime-composition chapter should be early, before the sophisticated scheduler chapters. Make an executable capability matrix the book's recurring anchor. Then readers can learn algorithms, persistence, leadership, security and operational failure modes without inheriting incorrect deployment guarantees. Historical commit subjects and completed prompts are development evidence, never substitutes for source/control-flow or executed test evidence.
