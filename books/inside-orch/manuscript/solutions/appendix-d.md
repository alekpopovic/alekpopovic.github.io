# Appendix D — worked solutions

These are reasoned answers to the 24 additional practice exercises, not fictional execution output. Named test logs are recorded separately.

## DEV-01

Both attempts plan from the pending snapshot. The first compare-and-write changes NodeID and ActualStatus to assigned; the second stale claim conflicts. The scheduler treats that conflict as a benign non-assignment. The fixture requires exactly one successful assignment and one assignment event, not two. This proves a store/scheduler claim contract for one record. It does not fence a worker after a partition or prove default-server durability. Physical process uniqueness requires a separate execution/fencing design.

Full credit requires: one successful claim; one assignment event; physical fencing remains unproven.

## DEV-02

The report enters as unhealthy; MemoryService checks service restart policy and converts it to failed when replacement is permitted. Failed is terminal for that task identity. Reconciliation creates distinct replacement work instead of making the same failed task healthy again. With replacement disallowed, unhealthy can remain retryable and later report running or healthy through valid transitions. Do not rewrite the agent’s original report as failed or assume every unhealthy service automatically rolls back.

Full credit requires: incoming unhealthy retained in trace; stored failed for restartable branch; new identity instead of resurrection.

## DEV-03

The generic transition helper permits failed to removed, but the agent guard rejects that change while desired remains running because terminal tasks accept only duplicates in that branch. Cleanup intent stopped or removed activates the cleanup report allowance, so removal is accepted. Service finalization still waits for all associated actual tasks to be removed; failed or stopped is insufficient. Label ownership must be checked by the agent before physical deletion.

Full credit requires: running-intent removal rejected; cleanup-intent removal accepted; all actual tasks removed required.

## DEV-04

The active budget is three and the minimum available budget is one. Old availability can count running or healthy, while newHealthy counts only healthy target-version tasks. A running target task does not increment newHealthy. Repeated controller ticks therefore need explicit health transitions before the new population can satisfy the completion predicate. Desired stops and actual removals are separate: even a succeeded model state can precede physical cleanup.

Full credit requires: active budget 3; minimum available 1; new running is not newHealthy.

## DEV-05

Same-name services may exist in separate namespaces with distinct IDs. ListServices under A returns A’s resources. GetService under A with B’s UUID must behave as not found, avoiding existence/metadata disclosure through the identifier. This specific tested service contract does not prove all newer job, volume or operation handlers perform the same lookup checks. Each path must validate namespace before returning a record. Authentication alone cannot replace object-level scope.

Full credit requires: A list excludes B; B UUID yields not found for A; new workload paths require separate review.

## DEV-06

Starting total is two. Each accepted scale adds one, but the namespace maximum permits only one additional replica. Serialized mutation/accounting admits one request and denies the other with the quota error; final total is three. The winner is nondeterministic and must not be asserted by name. This memory-lock test is a local concurrency guarantee, not a transaction protocol for an unwired durable multi-writer deployment.

Full credit requires: one success; one quota denial; final total 3 independent of winner.

## DEV-07

Initial sync records a revision and the managed api name. A repeated unchanged revision must not increment DeploymentVersion. Removing the manifest and committing a new local revision prunes the previously source-managed service; it does not authorize deleting every unrelated service in the namespace. The fixture creates a temporary local repository, uses no remote credentials and checks the deleted model state. Physical removal of running tasks remains asynchronous in a real agent deployment.

Full credit requires: unchanged revision no new version; prune limited to managed identity; model deletion differs from runtime cleanup.

## DEV-08

Forbid leaves the existing active job and creates no overlapping job. Replace removes/replaces the active job identity in the fixture and creates one new active entry; Allow is a different policy. With creation at 12:00, now 12:03 and a per-minute schedule, the catch-up fixture admits only two jobs because the missed-schedule bound is two. It also records LastScheduleAt and NextScheduleAt. These are scheduling/model results, not proof arbitrary business effects execute exactly once across crashes.

Full credit requires: Forbid no extra job; Replace changes identity; catch-up jobs 2.

## OPS-01

A ciphertext backup is unusable without the matching envelope key material. KeyID authenticates the envelope context but is not the decrypting key. Recover the exact key through an authorized independent recovery channel, prove decryption with a synthetic canary and never log real plaintext. If the key is irretrievable, record loss and re-provision secrets through application-specific recovery rather than claiming a database restore repaired them. Default MemoryService live secret records were never durable database state.

Full credit requires: matching key required; synthetic canary only; no automatic plaintext recovery claim.

## OPS-02

The executable constructs MemoryService, so process restart loses its live maps. A successful listener restart and ready response do not restore desired services or issued credentials. Preserve sanitized pre-restart intent if available, reconcile any surviving owned containers carefully, then re-enroll disposable nodes and reapply reviewed intent in the laboratory. Do not query PostgreSQL as though it owned that lost state. Stop before adopting or deleting containers whose label ownership is uncertain.

Full credit requires: MemoryService named; readiness independent of data; owned runtime reconciliation before replay.

## OPS-03

Record exact flags, seed, source SHA, Go/machine information, workload size, warm-up and duration with raw output. Explain that the tool drives in-memory control-plane behavior with fake agents. It does not pull images, start Docker containers or exercise the PostgreSQL store. Report its denominators and error counts as actually emitted, without deriving unsupported startup latency or durable-cluster capacity. If no run exists, mark the sheet unexecuted and leave measured results absent.

Full credit requires: full reproducibility inputs; fake-agent scope explicit; no Docker/database inference.

## OPS-04

Trace requested resources separately from runtime limits. The adapter can translate ResourceLimits into Docker Memory and NanoCPUs, but ordinary agent ContainerSpec construction omits that field. Therefore parser/DTO acceptance and adapter unit support do not establish the default end-to-end limit. Retain container IDs and inspect only captured disposable containers. Classify the missing propagation as an integration gap; do not silently patch source or promise enforcement based on quota reservations.

Full credit requires: missing Resources field identified; request/reservation distinct; actual inspect boundary retained.

## OPS-05

After successful server rotation, the stored hash may correspond to the new token while the worker retains the old token. A retry can then fail authentication even though transport delivered the previous heartbeat. Record request IDs and expiry metadata without tokens. Confirm the exact node and laboratory enrollment authority, stop uncontrolled retry/re-enrollment loops, and use a deliberate recovery process. Neither token hashing nor a fifteen-minute TTL makes the response-loss window disappear.

Full credit requires: rotation/receipt separate; no token logging; bounded authorized recovery.

## OPS-06

Stateless tasks receive node_lost metadata and are failed with desired removal so replacement can occur. Stateful tasks retain assignment for manual recovery because node-local data is not replicated or moved by a status update. A partitioned worker can still execute either old process. Offline detection is suspicion based on heartbeat age, not physical shutdown. Do not force stateful failover without a storage and fencing plan; stop if ownership or old-writer quiescence cannot be established.

Full credit requires: stateless replacement trace; stateful locality retained; no physical fencing inference.

## OPS-07

Process liveness/readiness confirms the HTTP process’s reported state; the handlers do not prove a database-backed live control plane or workload health. Inspect task assignments, actual/container health and specific operation errors separately. If schema check is enabled, database access can gate startup, but a past startup check is not a continuous durability guarantee. Proposed alerts need configured collectors and tested thresholds. Keep missing workload samples unknown rather than healthy.

Full credit requires: process/workload/store separated; startup check not continuous; missing data remains unknown.

## OPS-08

Use an owned disposable database, all sixteen migrations, known canary records and an exact dump/restore procedure. Retain the envelope key independently and compare restored record identities and content digests, not just process exit codes. Record restore duration and tolerated data-loss window from defined event origins. Do not claim the default memory server’s live intent is in this database. Stop on schema mismatch, missing keys or canary divergence; never overwrite a production database as an exercise.

Full credit requires: all 16 schema and canary; envelope key retained; default memory limit explicit.

## ARC-01

The model allows up to 7 active tasks and requires at least 4 available by its accounting. New target-version running tasks still do not count toward newHealthy. An old task can fail physically after the snapshot but before a stop is applied, making the prior budget stale. Client reachability can fail despite local health. These counters guide controller decisions; they do not establish a continuously enforced service-level objective.

Full credit requires: max active 7; min available 4; stale observation counterexample.

## ARC-02

CPU reservation is 1250 millicores. Memory is 5×134217728=671088640 bytes, equivalent to 640 Mi. Both fit the stated 1500-millicore and 734003200-byte quotas before considering any other services. These are requested reservations, not observed process usage or proof Docker limits are applied. Include existing namespace consumption in a real quota decision and inspect field propagation before promising enforcement.

Full credit requires: CPU 1250; memory 671088640; reservation not observed usage.

## ARC-03

Replace the live state-owner construction with a complete durable service implementation rather than merely opening a pool. Wire controllers to durable transactions, restore identity/operation state and add active leader-loss cancellation tied to side-effect authority. Specify schema, credential and envelope-key recovery. A falsifying test kills the process after durable intent but before runtime/report completion and checks reconstruction plus duplicate suppression. This is future architecture; the current binary does not supply these guarantees.

Full credit requires: live owner replaced; leader loss reaches side effects; crash-window oracle.

## ARC-04

A session-level advisory lock belongs to its original database connection. Cancellation can release a pooled connection before unlock, allowing a later unlock call to run on another session and falsely appear sufficient. Done closure signals local ownership loss but does not prove remote lock release. Test two independent pools: acquire A, cancel/release A, attempt B before and after closing A’s pool. Repair requires unlocking on the original pinned connection or closing that session; default server HA remains unwired.

Full credit requires: original session ownership; Done not unlock proof; two independent pools.

## ARC-05

Use only owned loopback fixture servers with synthetic responses and controlled resolution; do not contact live metadata services. Validate destination policy for every connection/redirect path, accounting for DNS rebinding and address changes rather than checking only the initial string. The forbidden listener should observe zero hits. Configuration validation and generic HTTP client behavior are separate boundaries. Retain exact resolver and redirect behavior from the pinned health implementation before claiming SSRF prevention.

Full credit requires: owned fixture only; redirect/dial policy evaluated; forbidden hits 0.

## ARC-06

Create two namespaces and distinct resources, then request each foreign ID under the other namespace context. The result must avoid returning foreign metadata and should match the intended not-found policy rather than disclose existence. Test list, get, delete and mutation paths separately. Admin fallback authentication does not by itself establish namespace-scoped lookup or delete semantics. If the current method lacks a scope check, report the gap instead of extending older service tests to it.

Full credit requires: foreign lookup matrix; mutation coverage separate; test gap not hidden.

## ARC-07

The parser can validate digest form and admission policy can require a digest. That does not prove a remote registry returned the intended manifest, that all referenced layers were verified, or that a tag’s current mapping equals the recorded digest. Propose an explicitly authenticated registry resolution and content-verification workflow with immutable returned digest and provenance records. Keep this future workflow separate from baseline syntax support and do not invent adoption or integrity results.

Full credit requires: syntax support only; remote/content evidence distinct; future workflow labeled.

## ARC-08

Start at accepted intent version timestamp and stop at the first authoritative matching task health/required replica observation. Preserve one monotonic process clock for local elapsed durations or document wall-clock skew across processes. Mark missing completion as censored/timeout rather than zero latency, and separate restart-lost records from successful convergence. Specify workload size, warm-up and sample denominator. A dashboard expression and suggested threshold do not become an operational alert until configured and tested.

Full credit requires: version-matched event boundaries; censored missing data; alert proposal explicit.
