# Chapter 34 - Leader Election and the Durable HA Boundary

Atlas wants to restart a control-plane host without interrupting its API. Two server processes behind a load balancer look like an obvious solution. At the locked source revision, however, each default server creates its own MemoryService. Requests routed to different processes would see different services, nodes, credentials, and tasks. An extra endpoint would add inconsistency before it added useful availability.

This chapter separates API replication, durable state, and controller leadership. You will trace the lease interfaces, follow PostgreSQL session ownership, and identify what cancellation does and does not stop. The Atlas deliverable is a durable-composition decision record backed by deterministic leadership tests and a separate observed database lock boundary. It is not a demonstration of a highly available default server.

## API Availability and Controller Leadership

API availability means that a surviving instance can serve the same authoritative state after another instance fails. That requires a shared durable control plane with equivalent transactional semantics, authentication state, and operational readiness checks. Controller leadership answers a narrower question: which process may run a particular mutating loop at this moment? A leader lock does not automatically make API handlers durable or mutually consistent.

The [HA design proposes active API replicas and one active leader per controller](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/HA_CONTROL_PLANE_DESIGN.md#L19-L39). Independent lock names let one instance lead scheduling while another leads rollout progression. This avoids forcing every kind of background work through one process. It also introduces several independently observable ownership transitions. A dashboard showing “leader” without the controller name would conceal which work is actually protected.

The implementation exposes a compact lease abstraction:

```go
type LeaderElector interface {
	Acquire(ctx context.Context, name string) (Lease, error)
}

type Lease interface {
	Name() string
	Done() <-chan struct{}
	Release(ctx context.Context) error
}
```

Exact source: [internal/leadership/leadership.go:15–23](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go#L15-L23).

Acquire may fail because another owner holds the name. Done signals that the current lease is no longer usable. Release is an explicit cleanup operation. A lease does not supply a monotonically increasing fencing token, and its interface does not prove that every downstream side effect checks ownership. Those missing properties are important when an old worker has already sent a request before losing leadership.

The local elector stores leases in one mutex-protected map. Its exclusion is meaningful only to callers sharing that elector instance. Two separate LocalElector objects do not coordinate across processes or even within the same process. It is a deterministic implementation for tests, not a substitute for a distributed authority. Atlas should use it to exercise wrapper behavior, then separately verify the database implementation and final server composition.

Source history preserves the distinction. Commit [b29a6fe91e90f74721e5175e43bf12aed6410f19](https://github.com/alekpopovic/orch/commit/b29a6fe91e90f74721e5175e43bf12aed6410f19) added the HA design; [eb3a07c20c550a533afaf36f414ede1ba6c00f78](https://github.com/alekpopovic/orch/commit/eb3a07c20c550a533afaf36f414ede1ba6c00f78) added the leadership package. Neither changes the current fact that [main constructs MemoryService and directly starts controller loops](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L142-L148). Library implementation and executable integration remain different milestones.

## PostgreSQL Advisory Locks and Connections

The PostgreSQL elector acquires a pooled connection, computes a key from the controller name, and calls `pg_try_advisory_lock`. If another session holds the lock, it releases the connection and returns ErrLockHeld. If successful, the lease retains the connection while monitoring it. This dedicated session is essential because the advisory lock belongs to the database session rather than to a Go object or a row.

The [key derivation hashes `orch:` plus the controller name](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go#L76-L80). It does not include an explicit cluster identifier. Two independently operated clusters sharing one database and the same names can therefore contend. Conversely, two supposed replicas connected to different databases can each acquire a lock and both act as leader. A matching integer key is useful only when every participant consults the same authoritative database session space.

Normal release asks PostgreSQL to unlock, then closes the lease and returns the connection to its pool. Cancellation follows a different path. The monitor sees the canceled context, invokes close, closes Done, and calls the pool connection's Release method. Returning a connection to a pool does not necessarily terminate its underlying PostgreSQL session. This difference is the chapter's central failure window.

The actual [full-schema recovery experiment](../../validation/intake/full-schema-recovery-corrected.json) observed that cancellation closed the lease notification while a competing pool still could not acquire the same advisory lock. Closing the original pool finally allowed acquisition. The observation is scoped to that captured disposable database and teaching harness. It demonstrates why a local Done signal cannot be treated as proof that the database session lock has been released.

The [release fast path returns immediately when Done is already closed](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L67-L78). A deferred Release after monitor cancellation therefore does not issue a compensating unlock. The source explains the observed retained lock without inventing a PostgreSQL failure. Atlas must fix connection cleanup in a separate implementation before relying on prompt handover; this book does not modify the locked application to make that guarantee true.

Monitoring also checks connectivity with `SELECT 1` every five seconds. A successful query means the connection answered that query. It is not a fresh acquisition, a fencing check against every workload mutation, or protection against unsafe database dual-primary operation. Timeouts, database topology, session termination, and write authorization must be evaluated together. A reachable database can still be the wrong authority for the intended cluster.

| Observation | Supported conclusion | Unsupported conclusion |
| --- | --- | --- |
| Acquire succeeds | This session obtained the named advisory lock | All API state is durable |
| Done closes | The local lease ended | Every old side effect has stopped |
| Callback returns | That wrapper invocation finished | Its earlier external requests were undone |
| Successor acquires | The consulted database permits a new owner | Two database primaries cannot both accept writes |

## Lease Loss Must Cancel Controller Work

RunWithLeadership validates its inputs, acquires once, marks the controller leader metric true, and defers cleanup. It creates a child context and cancels it when either the parent context or lease Done ends. Finally, it invokes the supplied callback with that child context. The [wrapper implementation contains no acquisition retry loop](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go#L48-L73). Retry with backoff belongs to a higher-level supervisor that must be designed and tested separately.

Cancellation is cooperative. A callback waiting on ctx.Done exits promptly in the upstream unit test. A callback ignoring its context can continue issuing work after the wrapper has signaled loss. Likewise, a database or runtime request already accepted before cancellation can complete afterward. Atlas should pass the context through every layer, bound in-flight operations, and retain idempotent reconciliation so a successor can safely recompute uncertain work.

The deterministic loss scenario starts a wrapper, waits for its callback's started signal, calls LocalElector.Lose, and waits for context.Canceled. It then checks that the leader metric is false. This ordering is stronger than sleeping and assuming the loop has started. The channels establish causality: ownership was acquired, work began, loss was injected, and cooperative work stopped. The test does not simulate packet loss or observe a real database session.

A network partition introduces two timelines. The old process may lose database connectivity while still reaching agents. The database may eventually drop its session while an external request is still in flight. A new process can then acquire leadership. The safety question is whether repeated or overlapping work is harmless, not just whether two lease objects report different states. Atomic task claims, transactionally recorded events, and stable task identities remain necessary.

The proposed Atlas [durable-composition ADR](../../examples/teaching-extensions/ch34/ADR-durable-composition.md) therefore requires cluster-qualified names, one verified database primary, explicit session cleanup, callback termination checks, and bounded reacquisition. It also requires database-backed API transactions before API replicas become ready. These requirements are future composition work; the ADR does not imply that upstream already supplies fencing tokens or a complete HA server.

## The Durable State and Server Composition Prerequisites

Begin the lab in a disposable source copy with the locked Go toolchain. No live service is replicated. Run the upstream leadership package tests:

```bash
go test ./internal/leadership -count=1 -v
```

The [recorded run](../../validation/labs/ch34/leadership-tests.json) passed the one-owner test, cooperative lease-loss test, acquisition-failure metric test, and stable-key test. Its artifacts preserve exact command, working directory, UTC interval, and output. Cleanup releases test-local leases; there is no Docker workload or database to sweep in this deterministic run.

Use the separate full-schema record for the database session experiment. Read its sequence rather than relabeling it as this unit-test run. It used owned disposable resources and tested competing PostgreSQL elector pools, cancellation, and eventual acquisition after the first pool closed. Its application store and backup checks are separate observations. The default server was not wired to that store merely because both packages appeared in the same harness.

The first acceptance gate for durable composition is equivalence of API semantics. Service creation must preserve its service record, initial version, and event together. Task assignment must retain its conditional pending guard and event atomicity. Credentials and namespaces must survive fresh-process restart under the same policy. A database pool injected beside MemoryService satisfies none of these requirements by itself.

The second gate concerns readiness. A durable replica unable to reach its authoritative database should not advertise that it can safely serve writes. A controller unable to establish leadership should not start mutating work. These can be different readiness dimensions: an API replica may serve reads while another instance leads a controller, provided the durable state and failure policy support that behavior. Atlas must define the policy rather than infer it from `/readyz` returning success today.

Finally, rehearse handover against realistic failure windows: orderly release, canceled controller, abruptly killed process, dropped database connection, wrong database identity, and uncertain external completion. Each case needs an observable owner transition and an invariant about task/event effects. A green local lease test establishes a useful mechanism. It is only one piece of the evidence required for replicated operation.

A useful review artifact separates mechanisms from deployment assumptions. Record which database endpoint each candidate process uses, which controller name it requests, the UTC interval during which it believes itself leader, and the last accepted write associated with that interval. Redact credentials while retaining stable resource identity. This makes an overlap investigation possible without equating local metrics with database truth. If the old process stops logging, absence of a log line is not proof that its last runtime call failed. Inspect the task and the engine before allowing a successor to repeat the effect. That inspection is also how Atlas avoids turning a safe leadership handover into duplicated workloads.

Atlas leaves this chapter with a justified “not yet” for default-server HA and a concrete implementation plan. That decision protects the team from deploying two inconsistent memory control planes under an availability label. The implemented leadership package is valuable precisely because its contract and limitations can be inspected, tested, and improved without confusing it with the whole system.

## Exercises

1. Explain why two LocalElector instances can both acquire `scheduler`, and identify the state they fail to share.
2. Run the leadership tests and trace the channel sequence that makes lease-loss cancellation deterministic.
3. Explain the observed retained advisory lock after cancellation. Distinguish pool connection release from database session termination and identify the fast path that prevents a later unlock.
4. Review a proposal to add two default servers behind a load balancer. Specify the durable-state, topology, readiness, and side-effect gates required before approval.

Worked answers are in [Chapter 34 solutions](../solutions/ch34.md). Source and observation classifications are preserved in the [claim ledger](../../validation/evidence/ch34.json).
