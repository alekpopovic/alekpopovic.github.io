# 19. Recover from cancellation, uncertainty, and rollback


## Cancellation has a timeline

A queued job can often be cancelled without contacting a runner. An active job requires a request, delivery, runtime action, and a stopped observation. A deployment may have already changed the target before any of those steps finish. Keep the cancellation request timestamp and the observed terminal timestamp distinct.

If cancellation races a successful exit, preserve the actual observation. A request to stop does not prove that the operation was stopped. The laboratory permits a success result arriving after a cancellation request while the same claim is still active. The user can see that cancellation was requested too late rather than being shown a fictional cancelled deployment.

A timeout follows the same principle. It is a policy deadline for permitted execution, not a guarantee that every external side effect has stopped at that instant.

## Quarantine uncertain targets

When a runner disappears during a target mutation, mark the deployment uncertain and retain its target reservation. The recovery procedure should first establish runner state, then target state, then the relation between the two. An operator needs a stable deployment identity and a checklist, not a generic Retry button.

A useful reconciliation record includes the observer, time, target identity, observed revision, active operation identifier if available, and the resulting decision. A recovered connection can provide evidence, but it does not automatically make the old runner authoritative again. Its original attempt and fence still matter.

Permit read-only inspection with narrower credentials when possible. If the target can report a deployment operation by idempotency key, use that to distinguish “not applied,” “still applying,” “applied,” and “unknown.” An adapter unable to inspect state should declare that limitation.

## Retry policies depend on side effects

A pure compilation step can often be retried after infrastructure failure. A package publication, payment-like external operation, or database migration may not be safe to repeat without additional identity checks. Classify retry safety explicitly rather than assigning the same `max_retries` setting to every job type.

Backoff is useful for transient faults but does not fix a semantic error. Retrying a bad credential, invalid pipeline, or unauthorized target just creates noise. Record the reason for each retry and show attempts separately.

The platform should never advertise exactly-once execution for arbitrary shell commands. It can offer durable attempt identity, conditional state updates, idempotency contracts for specific adapters, and conservative reconciliation when the external boundary cannot provide certainty.

## Rollback is another controlled change

Rollback normally selects a previously retained artifact and applies an adapter-specific reverse transition. It needs its own authorization, target reservation, and health verification. It is not a database time machine and cannot generally reverse arbitrary external effects.

A database schema change may prevent an old application binary from running. A data migration may have discarded information. A new external message may already have been consumed. Record rollback compatibility before release and distinguish an application rollback from a database restore.

When rollback itself becomes uncertain, do not erase the original deployment record. Link the operations and reconcile the actual target state. Operators need to see the complete sequence of intended and observed changes.

## Exercise

A deploy command uploads a new image, runs a destructive data migration, and restarts the service. The health check fails. An automated rollback simply starts the previous image. What prerequisite was missing?

## Worked answer

The release lacked a verified compatibility and recovery plan for the data change. The previous binary may no longer understand the schema or data. Use expansion-and-contraction changes where possible, test rollback within its stated window, and keep a separately tested restore procedure for changes that cannot be reversed safely. A previous image digest alone is not a complete rollback plan.

## Completion evidence

Run failure experiments before and after each externally visible mutation. Demonstrate that target locks remain held through uncertainty and that recovery decisions preserve the original event history.
