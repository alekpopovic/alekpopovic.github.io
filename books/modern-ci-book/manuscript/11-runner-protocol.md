# 11. Design an outbound runner protocol


## Let runners ask for work

The runner initiates HTTPS connections to the server. This avoids requiring a publicly reachable listener on each worker host. It is an operational choice, not an authorization shortcut. The runner still validates the server identity, and the server still restricts what that runner may receive or submit.

A minimal protocol needs enrollment, capability advertisement, claim acquisition, start acknowledgement, heartbeat, log upload, result submission, cancellation observation, and reconciliation. Version these messages before adding optimizations. Start with bounded long polling if it meets the latency target; a streaming transport does not remove the need for durable request identities.

A claim reply should contain an immutable plan fragment, current attempt identity, fence, lease duration, and the exact resource references the runner may use. It should not contain broad administrative credentials or arbitrary instructions to read host files. Prefer scoped handles that can be redeemed only for the active attempt.

## Negotiate capabilities without trusting labels

A runner advertises architecture, operating system, executor features, and configured capacity. The server matches required capabilities only within an authorized pool. A runner saying it supports privileged execution does not give a project permission to use that mode.

Store the runner version and protocol range. Reject incompatible workers before they claim work. During a rolling upgrade, keep a tested overlap range or drain old workers. A mixed fleet is normal; an undocumented mixed fleet is an incident waiting for a rarely used message type.

The runner's capacity is a promise about its own local admission. The server's capacity reservations are a promise about the global policy. Both need reconciliation after a restart. If the runtime shows two managed containers but the runner's local state file is empty, starting two additional jobs because the configured concurrency is two is wrong.

## Make every mutation replayable

If a claim reply is lost, the runner cannot know whether the server reserved work. Give claim requests an idempotency identity or expose a “current assignments for this runner” recovery endpoint. Otherwise, a retry can strand one assignment and obtain another.

For logs and results, repeat the same attempt and segment identifiers. For credential redemption, bind the request to an authorized capability rather than accepting a free-form secret name. For cancellation, report whether the runtime observed termination; do not merely acknowledge that a cancel message was received.

Use bounded exponential backoff with jitter on connection failures. Keep heartbeats distinct from high-volume log transfer so a slow object upload does not accidentally expire execution ownership. All buffers and retry queues need limits and visible error behavior.

## Drain and restart deliberately

Draining a runner stops new claims while allowing current attempts to finish or enter controlled cancellation. A runner upgrade should drain, persist its assignment journal, inspect the runtime, restart, and reconcile before admitting new work. Record the last confirmed log sequence and result state for each assignment.

The journal is not the authoritative job database, but it is evidence about local processes. Persist it atomically with safe file permissions. Never store plaintext long-lived secrets in a convenient diagnostic bundle. Keep credentials in a separate protected location and redact the bundle by construction.

A forced shutdown may leave physical work running. On return, the runner identifies its containers using explicit ownership labels and known attempt identifiers. It must not delete every container on a shared host to restore a clean-looking state.

## Exercise

The server claims a job and commits, but the HTTP reply is lost. The runner retries without a stable request identifier. What could go wrong, and what does the protocol need?

## Worked answer

The first assignment can remain leased without the runner knowing its identity, while the retry claims a second job. Use a stable claim request key with a stored response or a reconciliation endpoint that returns the runner's current assignments. The runner should recover the first assignment or explicitly abandon it through the contract before treating a new response as unrelated work.

## Completion evidence

Run protocol tests with a proxy that drops replies after the server commits, interrupts uploads, duplicates messages, and disconnects during shutdown. Test the supported version matrix using actual built runner and server binaries.
