# 10. Fence attempts and preserve uncertainty


## A timeout is not a stopped process

A runner starts a deployment and then loses its network connection. The server's lease expires. The deployment may still be running perfectly well on the target. Starting another attempt immediately can run two releases concurrently, even if the database believes there is only one owner.

Distinguish **control ownership** from **physical execution**. A lease gives a runner time-limited permission to report and redeem capabilities. A monotonically increasing fence identifies the generation of that permission. Neither can reach backward through a network partition to terminate an arbitrary external command.

Every current-attempt message should identify the job, attempt, runner, and fence. Result acceptance is a conditional transaction that checks all four, the current state, and the lease policy. A zero-row update means the claim is no longer current; it is not a reason to retry the same update without predicates.

## Walk through a stale completion

At time `t0`, runner R1 receives attempt A1 with fence 7. At `t1`, ownership expires and the job becomes uncertain. An authorized reconciliation establishes that the old execution stopped. A retry creates A2 with fence 8. At `t2`, R1 reconnects and reports success for A1.

The platform retains the report as a late observation if useful, but it must not replace A2's current state. The laboratory's `TestStaleCompletion` exercises this distinction. Its old attempt remains in the ledger with its own result, and the new attempt has a larger generation.

```text
job J
  attempt A1 / fence 7 / observed stopped / failed
  attempt A2 / fence 8 / current / running
late report for A1 -> rejected as current completion
```

A fence must be scoped so it cannot be confused across jobs or projects. A numeric generation alone is insufficient. Bind it to a specific attempt and runner identity, and authorize the owning project separately.

## Heartbeats must not resurrect old authority

A heartbeat arriving after lease expiry should not blindly extend the row. Require the same current claim, an active state, and an unexpired lease under the chosen policy. Rejoining after a longer interruption is a reconciliation flow, not a heartbeat with a generous timeout.

Also distinguish the result path from duplicate acknowledgement. If a valid terminal result was already committed, an identical retry may be acknowledged after the lease time has passed. It does not renew execution rights. A conflicting terminal result must be rejected or recorded as a conflict without replacing the committed outcome.

Runner clock time is diagnostic data, not authority for lease validity. Record the server's receipt time and the worker's observation time separately. This helps operators see whether a report is delayed without allowing a worker to extend its own lease by reporting a favorable clock value.

## Fence external targets where possible

The control database can reject stale results, but an external target may need its own defense. Prefer idempotent operations keyed by deployment identity, compare-and-set target revisions, or an adapter that checks a target-side generation before mutation. These controls must actually be implemented at the target boundary; adding a fence field to an HTTP payload does not help if the receiver ignores it.

For a target that cannot enforce such a contract, use a conservative uncertainty policy: retain the lock, inspect the target, and require a controlled recovery decision. Document the residual risk. A generic shell deployment cannot honestly promise exactly-once effects.

## Exercise

A scheduler stores fence 11, while the target still accepts commands from a disconnected worker carrying fence 10. The worker cannot update the CI database. Is the deployment safe?

## Worked answer

The database is protected from stale state updates, but the target is not protected from stale side effects. The target must enforce an idempotency or generation rule, or the system must prevent another deployment until the old activity is reconciled. Fencing is only as strong as the boundary that checks it.

## Completion evidence

Inject delayed heartbeats, duplicate results, conflicting results, old-runner reconnects, clock skew, and disconnects around target mutation. The expected state must name uncertainty explicitly rather than silently returning work to the queue.
