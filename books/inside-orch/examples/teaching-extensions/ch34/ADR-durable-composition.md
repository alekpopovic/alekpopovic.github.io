# Atlas proposal: durable control plane before replicated APIs

Status: design proposal, not upstream wiring or a completed HA deployment.

## Decision

Do not place a load balancer in front of independent MemoryService processes. First implement one durable control-plane composition with equivalent transactional API/controller semantics. Bind all replicas to one verified database primary and a persistent Atlas cluster identity; reject mismatches before readiness.

Give scheduler, reconciler, rollout, node monitor and autoscaler separate cluster-qualified leadership names. The baseline hashes only `orch:` plus controller name; cluster namespacing is new design. Use dedicated sessions with explicit unlock or verified session termination on cancellation and error. Do not return a live session with an advisory lock to a general pool. A connectivity probe is not a fencing token.

Wrap all mutating loops, pass the lease context into every operation, bound request duration and in-flight work, and wait for the old callback to exit before reporting successful handover. Add acquisition retries with bounded jitter outside baseline RunWithLeadership, which acquires once. Persist idempotency keys/optimistic task guards and event writes transactionally. Decide how database failover fences old writers and prohibit dual primaries.

## Acceptance evidence still required

- Concurrent replicated API mutations against durable state retain task/event invariants.
- Lease cancellation, callback exit, actual database unlock and successor acquisition have separate observations.
- Database partition fails durable readiness and stops new mutating work; reconnect recomputes state.
- In-flight external effects remain discoverable and idempotent after uncertain completion.
- Cluster identity mismatch and dual-primary topology are rejected operationally; no claim of independent distributed consensus.
- Fresh server processes read the same persisted services, credentials, tasks and events after restart.
- Backup/restore preserves required state and keys, with measured recovery and cleanup of owned resources.

## Rejected shortcut

Two running HTTP endpoints plus a green health response do not establish shared active state, exclusive work or durable recovery.
