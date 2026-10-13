# Operational playbooks

Commands below name real CLI paths. Supply the dedicated Atlas namespace and captured IDs from your own disposable lab. These are scoped procedures, not claims that a live incident was executed.

## pending-tasks

Trigger: Desired replicas exist but one or more tasks remain pending.

Mode: Default memory mode; store-backed scheduler package tests have separate scope.

Observation command paths: `orch service inspect`, `orch service ps`, `orch node ls`, `orch events`.

Triage: Compare service intent/version with task desired/actual state, then node readiness, requests, placement labels and public-port reservations.

Decision: If no eligible capacity exists, distinguish a valid pending result from a failed scheduler loop; ordinary immediate placement can bypass Plan constraints.

Bounded action: In the disposable Atlas lab, change only the captured service replica request or restore one known eligible node after recording the original setting.

Verification: Re-read assigned NodeID, actual state and conditions for the same task/service version.

Stop/rollback: Stop before broad node changes or an unreviewed force override; restore the recorded replica setting when the experiment ends.

Boundary: placement.

## unhealthy-workload

Trigger: A task becomes unhealthy or client requests fail despite running.

Mode: Default memory+agent mode; source-derived policy must match the selected service.

Observation command paths: `orch service ps`, `orch service inspect`, `orch logs`, `orch endpoints`, `orch events`.

Triage: Check local probe configuration, runtime/container status, restart policy and the gateway path independently.

Decision: Decide whether unhealthy stays retryable or MemoryService converts it to failed under replacement policy; new rollout success requires healthy.

Bounded action: Inspect only the captured disposable task’s logs and adjust only its synthetic health fixture; avoid private destination probing.

Verification: Observe a permitted healthy transition or a distinct replacement task, then verify the client path separately.

Stop/rollback: Stop when a probe target is not owned or log output may reveal real secret material; restore the original lab manifest.

Boundary: runtime execution.

## agent-enrollment

Trigger: Registration, heartbeat or task polling is rejected.

Mode: Default issued-agent credential flow; optional user JWT is a separate surface.

Observation command paths: `orch node ls`, `orch node inspect`, `orch events`.

Triage: Separate registration bootstrap authority from issued node bearer credentials; compare node identity, expiry and request IDs without printing tokens.

Decision: Distinguish incorrect authority, rotated-token response loss, wrong-node access and a memory-server restart that erased credential records.

Bounded action: Pause the captured disposable worker and deliberately re-enroll it through the configured lab authority only after confirming its old runtime ownership.

Verification: The same intended worker appears with valid current identity and heartbeat; assignment requests are authorized for that node only.

Stop/rollback: Stop before using another node’s token, automatic unrestricted retries or exposing credentials in support bundles.

Boundary: identity.

## node-loss

Trigger: Heartbeat age exceeds the configured cutoff and a node becomes offline.

Mode: Default monitor/bookkeeping; no physical fencing or replicated storage.

Observation command paths: `orch node inspect`, `orch service ps`, `orch events`.

Triage: Compare server observation time with nonzero LastHeartbeat, node status and task node_lost conditions; inspect workload Stateful flags.

Decision: Stateless replacement is eligible; stateful work remains local for manual recovery. Neither implies the old process stopped.

Bounded action: In the lab, isolate only the owned worker process or restore its connection; avoid forcing local-volume work onto another node.

Verification: Record old/new task IDs, current NodeID and runtime ownership; verify any returned worker cleans only its labeled old work.

Stop/rollback: Stop on uncertain old-writer activity or missing storage/fencing design; restore connectivity rather than deleting unknown containers.

Boundary: identity and runtime execution.

## drain-capacity

Trigger: A drain request remains incomplete or shows insufficient replacement capacity.

Mode: Default node drain path; maintenance constraints still apply.

Observation command paths: `orch node drain-status`, `orch node inspect`, `orch service ps`, `orch events`.

Triage: Inspect draining status, off-node replacement count and the running-or-healthy availability predicate.

Decision: If replacement capacity is unavailable, waiting is correct; drain complete concerns desired work and can precede physical removal.

Bounded action: Add only the explicitly owned disposable capacity or uncordon the captured node with a recorded reason.

Verification: Verify off-node availability, desired stops and separate actual removals.

Stop/rollback: Stop before unconditional force, stateful movement or a claim that drain complete proves zero containers.

Boundary: placement and runtime execution.

## rollout-failure

Trigger: A deployment stalls, fails or conflicts with another mutation.

Mode: Default rollout controller; model success is not cleanup completion.

Observation command paths: `orch rollout status`, `orch service inspect`, `orch service ps`, `orch events`.

Triage: Read FromVersion/ToVersion, target health, old availability, surge/unavailable budgets and operation-lock conflicts.

Decision: Choose between waiting for an owned probe repair and an explicit rollback; a raw running target is not newHealthy.

Bounded action: In the disposable lab, invoke rollback only for the captured service after retaining the failed deployment ID and intended previous version.

Verification: Observe a new rolling_back deployment and target healthy population; verify physical old-container cleanup independently.

Stop/rollback: Stop on an unrelated active operation or insufficient capacity; preserve terminal history rather than rewriting it.

Boundary: intent and runtime execution.

## gitops-drift

Trigger: Sync fails or actual service content differs from a source-managed revision.

Mode: Default GitOps controller with local fixture scope; remote access needs explicit authority.

Observation command paths: `orch gitops ls`, `orch gitops status`, `orch gitops diff`, `orch events`.

Triage: Record source ID/revision/path, parser errors and managed-service set; compare warn versus auto_revert policy.

Decision: A fetch/parser failure should not authorize pruning untrusted broad paths; distinguish drift observation from a successful apply.

Bounded action: Use a temporary local repository and synchronize only its captured source ID after fixing one owned manifest.

Verification: Check LastRevision, managed names, exact service diff and that unrelated services remain unchanged.

Stop/rollback: Stop before embedding credentials in a repository URL, enabling broad prune, or overwriting an unrelated manual service.

Boundary: intent.

## quota-denial

Trigger: A mutation returns quota_exceeded or the namespace’s remaining reservation is insufficient.

Mode: MemoryService namespace accounting, protected by local mutation lock.

Observation command paths: `orch quota get`, `orch service ls`, `orch service inspect`, `orch events`.

Triage: Read quota and current usage in the same selected namespace; compute CPU/memory requests times replicas, and count positive published-port declarations once per service. Compare projected totals after excluding the service being replaced.

Decision: Zero quota fields mean unlimited; a racing mutation can legitimately win before this request. Requested reservations are not measured Docker consumption.

Bounded action: Reduce only the captured lab service’s request/replicas or adjust an explicitly owned lab quota after retaining its prior values.

Verification: Re-query usage and confirm the denied request did not partially change intent.

Stop/rollback: Stop before raising a shared limit or equating quota acceptance with runtime enforcement; restore the recorded lab quota.

Boundary: intent and placement.

## memory-restart

Trigger: After process restart, the listener is ready but previous services or credentials are missing.

Mode: Shipped memory server only; process restart loses active maps.

Observation command paths: `orch service ls`, `orch node ls`, `orch events`.

Triage: Confirm the binary source pin and NewMemoryService composition; preserve any pre-restart sanitized intent and captured runtime identities.

Decision: This is expected process-local loss, not proof PostgreSQL restore failed; surviving containers need careful label reconciliation.

Bounded action: Reapply reviewed disposable intent and re-enroll only captured owned workers after examining old containers.

Verification: Compare recreated identities and desired versions, then separately verify runtime convergence and new authentication.

Stop/rollback: Stop if there is no authoritative intent snapshot or container ownership is ambiguous; do not bulk-delete runtime objects.

Boundary: intent and identity.

## postgres-restore

Trigger: An explicitly wired future durable extension rehearses database loss or backup recovery.

Mode: Teaching extension/future durable composition; actual package restore evidence is narrower.

Observation command paths: `orch cluster check-upgrade`.

Triage: Use a new owned disposable database, retained envelope key, exact schema version and synthetic identity/content canaries.

Decision: A successful pg_restore exit is insufficient; the current memory binary does not read this database as live intent.

Bounded action: Apply all 16 locked migrations and restore a synthetic backup into a fresh disposable target; no production overwrite or clean restore in the default path.

Verification: Compare canary count, stable IDs and content digests; prove synthetic secret decryption with the retained matching key.

Stop/rollback: Stop on schema/key/canary mismatch; keep the original database untouched and destroy only the captured lab target after evidence review.

Boundary: database extension.
