# Failure and recovery model

Baseline `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`; source reviewed 2026-10-13T00:35:06.866797+00:00. This matrix defines tests and acceptable claims; none of its scenarios is described as an executed experiment without a separate command record.

## Ownership determines recovery

The default server's live authority is `MemoryService` at [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L148). The Docker daemon owns container effects independently. PostgreSQL store operations own durable rows only when a caller injects that store. An agent owns its polling/probe memory and local runtime interaction; a node monitor owns timeout decisions in the active server. These owners fail independently, so the same word “restart” cannot identify a guarantee.

| Failure boundary | Last known state and recovery owner | Deterministic test | Separate integration experiment | Residual risk |
| --- | --- | --- | --- | --- |
| request-validation | No mutation before rejected input; request and caller own retry; API decoder, normalizer and admission | Repeat invalid payload; compare counts and error.code | Loopback HTTP request to owned server | No atomicity promised for arbitrary external effects |
| mutation-event | Maps volatile; best-effort audit/event can fail after mutation; MemoryService maps versus transactional store | Fail event append fake; compare task and event state | Disposable PostgreSQL WithTx rollback test | A memory mutex is not a durable transaction |
| task-claim | Task version is volatile or DB row depending injected store; scheduler and expected UpdatedAt | Race two claimers on one pending task | Two DB sessions on disposable schema | Claim CAS does not reserve whole planning snapshot capacity |
| image-pull | Registry request may have side effect/cache; task identity retained; agent and Docker daemon | Fake PullImage failure and repeated attempts | Owned test image/daemon; inspect labels and failed report | Pull stream is discarded; do not promise complete error taxonomy |
| container-create | Container may exist before status report; agent owns adoption; Docker external effect and task identity | Lose report then retry same task ID in fake runtime | Create exact task-labeled container and restart owned agent | Changing task identity can create duplicate work |
| lost-report | Runtime effect may exist with old server status; agent HTTP retry and control-plane guards | Repeat same report; reject mismatched node | Interrupt only owned loopback proxy then restore | No exactly-once network delivery |
| probe-failure | Container can remain running while unhealthy is reported; agent health counters and task state | Clock-controlled threshold fixture | Owned app returns failure status; capture report | Running status and rollout availability are distinct from probe health |
| agent-restart | Docker objects survive agent memory; server identity still required; local agent maps versus Docker labels | Adoption and unassigned cleanup fixtures | Restart owned agent, inspect same container identity | Expired credential/re-registration is not server durability |
| controller-restart | Preserved object maps, not a new process; new controller on same MemoryService | Chaos rollout subtest with reused cp | Restart only controller fixture, not host process | Cannot establish process durability |
| server-restart | All desired records and credential hashes volatile; composition root NewMemoryService | Instantiate second independent MemoryService | Kill/relaunch own server and list namespaces/services | Containers may outlive ownership; backup of unused DB cannot restore them |
| daemon-outage | Server intent can survive only within live memory process; agent Docker client and host daemon | Fake inspect/start errors and retries | Use separate disposable daemon, never stop shared host daemon | No remote runtime recovery proof from fake errors |
| heartbeat-timeout | Replacement task may coexist with isolated old container; node monitor and control plane | Inject clock and offline transition | Isolate only owned agent/server connection; observe old endpoint | No worker fencing; single-writer workloads unsafe to assume exclusivity |
| network-partition | Old runtime side effect may continue; central monitor only changes records; agent retry and worker workload | Fake heartbeat failures and late reports | Local proxy partition with explicit bounded recovery | Late cleanup after reconnection is not instantaneous fencing |
| duplicate-controller | Default binary has no leadership wrapper; memory servers independent; scheduler optimistic claim and leadership package | Run competing fixture schedulers; inspect task/events | Actual advisory lock session test, cancellation and handover | Leadership cannot merge independent MemoryService maps |
| gitops-failure | Earlier files can be applied before later failure; LastError volatile; sequential manifest apply and ownership list | Valid first YAML plus invalid second | Owned local Git fixture and explicit sync | No atomic batch; failed ownership bookkeeping affects later prune |
| scheduled-job-misfire | LastScheduleAt/ActiveJobIDs volatile; immediate retry tasks; cron controller and job attempts | Injected clock, timezone and concurrency fixtures | Owned loopback server and finite local job | No exactly-once, durable scheduling or system-cron equivalence |
| migration-interruption | DB state durability follows migration mechanism, not server maps; manager, SQL transaction and migration records | Inspect guarded down and failed migration fixtures | Disposable DB only; status before/after controlled interruption | All sixteen migrations require their own recorded run |

## Acceptable outcomes and abort criteria

For every row keep before/fault/after snapshots, exact task/container identity, API error status and events. A rejection is acceptable only when its source guard explains the outcome and no unintended mutation occurred. A retry is acceptable only when the same task is adopted or a documented new attempt is created; count residual containers. A failed controller pass must leave an observable error and a clear recovery owner; a log line does not prove the loop is still active. Stop the experiment if it reaches an unowned daemon, non-lab namespace, external host or non-disposable database. Cleanup only recorded IDs created by the run.

## Restart is three different experiments

The chaos subtest `server restarts during rollout` in [internal/e2e/chaos_test.go:41](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L41-L62) constructs another controller over the same `cp`. It proves the fixture's controller reconstruction can progress against preserved maps. It neither starts another server process nor restores from a database. A real fresh default server has new maps; API desired state and node credential hashes are not reconstructed. An agent restart can adopt a Docker object using unchanged task labels when the server still knows that task. These are useful but different outcomes.

## Residual side effects and fencing

The node monitor cannot remotely switch off a partitioned Docker container. After a timeout, central state can replace work while the old worker still serves. Reconnection permits label-aware cleanup; it does not retroactively prevent concurrent writers. A single-writer database or local volume needs fencing or an application-level ownership protocol before failover can be called exclusive. A local volume claim is bookkeeping and topology affinity, not replicated data.

Task state guards are in [internal/controlplane/controlplane.go:877](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L877-L978) and [pkg/types/lifecycle.go:140](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L140-L190); inspect the exact report path for each stale-state test. A repeated running report can be idempotent, and the supplied chaos returning-node scenario deliberately accepts a running report after shutdown/return. Do not describe universal rejection of old work.

## Atomicity and coordination limits

[internal/gitops/gitops.go:220](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L220-L280) reads and applies sorted files sequentially. An error in file two does not roll back file one. LastRevision can remain the old successful revision while LastError and LastSyncedAt describe the latest failed attempt. Task CAS at [internal/store/postgres.go:919](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L919) protects one task's stale assignment; it is not global capacity reservation. Event atomicity depends on actual transaction participation. A leader advisory lock can serialize a controller callback, but default main does not use that wrapper and coordination does not reconstruct state.

## Teaching improvements outside this edition

Durable domain-service wiring, multi-object reservation transactions, fencing generations, supervised controller restart and transactional GitOps plans are possible extensions. They must be separately labeled, implemented outside immutable evidence and tested. The baseline does not promise exactly-once jobs, zero-downtime updates, replicated storage, complete kernel isolation or restart-safe desired state. `labs/failure-matrix.json` is the machine-readable source of these review scenarios.

## Subsequent observed execution

Root-run `validation/intake/full-schema-recovery-corrected.json` records a two-pool PostgreSQL experiment: cancellation closes Lease.Done and Release returns nil, but an independent pool cannot acquire until the original pool closes. This confirms the advisory-lock cancellation concern for that package/session composition; it does not establish default server HA because leadership remains unwired. The same scoped record covers sixteen migrations, idempotent second Up, guarded Down refusal, one-winner concurrent assignment and a backup/restore canary. Original upstream fixture failures remain preserved separately.
