# 17. Preserve the fast path in a Go agent

## Why separate the production implementation

The Python agent demonstrates semantics and is easy to inspect. A production edge service has additional responsibilities: bounded concurrency, lifecycle supervision, metrics, platform-specific socket ownership, key rotation, independent reconciliation, and predictable request latency. The source architecture chooses Go for that service, while retaining the same policy invariants.

This lesson is a porting design. The package does not contain a completed Go agent or a measured claim about its performance. The original sixty-task pack breaks implementation into verified milestones. Treat the Python tests as behavioral fixtures to reproduce in Go, not as evidence that an unwritten port works.

## Publish an immutable view

Represent the request-time state as one object containing modes, normalized allowlist keys, normalized active decision keys, revision identity, and expiry deadlines. Construct a new object during an update, then publish one pointer. Do not mutate a map that active request goroutines are reading.

A conceptual shape is:

```go
type View struct {
    Revision uint64
    // Maps are private and immutable after publication.
    Modes map[string]string
    Bans  map[Key]Decision
}

var current atomic.Pointer[View]
```

This excerpt is explanatory, not a compilable service: `Key`, `Decision`, imports, validation, and lifecycle are deliberately omitted. A pointer publication primitive does not make the maps immutable. That guarantee comes from ownership and code discipline. Keep update construction separate from the check path and use race tests on the finished implementation.

## Normalize address keys

Use an address type rather than arbitrary text. Apply the same IPv4-mapped IPv6 rule as the collector and central detector. Reject zone identifiers and unknown sites. Build composite keys from site and address; a missing site must not become global scope.

For each request, read the published view once, apply local bypass and allowlist precedence, test active deadlines, and return the documented status and outcome. No database access, disk read, central call, or signature verification belongs in that path.

## Serialize updates

One update coordinator validates the envelope, checks ordering, persists state, and publishes the view. If several control requests arrive simultaneously, the coordinator serializes them so that revision comparisons and publication remain coherent. Expensive work can occur before the final lock when safe, but recheck ordering at the commit boundary.

Bound the envelope body before allocating it. Bound policy entries before building indexes. Reject duplicate decisions and revision conflicts. Keep errors machine-readable enough for a dispatcher to distinguish stale data, invalid content, unauthorized identity, and transient storage failure.

## Supervise the process

Run the agent as an unprivileged service account. Provision a runtime directory with deliberate Nginx access to the authorization socket. Place durable state in a separate writable state directory. Apply systemd hardening only after verifying that it permits the required filesystem and network operations.

Do not have a remote policy execute `nginx -s reload` or edit arbitrary configuration. Initial deployment changes are operator-controlled. Runtime decisions update the local view. Service restart and policy update are different events and should have distinct operational procedures.

## Reconciliation and health

Add an outbound authenticated pull loop independent of push. The loop reports or uses the applied revision and receives only the agent's authorized snapshot. Apply the same validator and persistence sequence. Heartbeats include revision, version, time health, capacity, and emergency bypass state.

Keep request readiness distinct from process liveness. A process can be listening while it has no verified policy. A healthy local agent can have old but still valid state during a central outage. A new empty policy can establish readiness without any bans. These distinctions should survive the language migration.

## Exercise

A developer stores a pointer to a new view, then updates its ban map in place to remove expired entries. Why is this unsafe, and what alternatives preserve the model?

## Answer

Readers may race with map mutation or observe a partial change. Build and publish a new immutable view, or keep expiry evaluation in each check and prune by publishing another complete view later. The finished Go port needs a race-detector run and concurrent-check/update tests, plus the signature, replay, restart, and TTL fixtures from the lab.
