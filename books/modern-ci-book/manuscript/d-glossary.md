# Appendix D. Glossary

## Approval subject

The exact project, environment, artifact, configuration, and policy identity authorized by an approver.

## Artifact

A finalized output with ownership, producer identity, digest, and retention policy.

## Attempt

One concrete execution of a logical job; retries create new attempts.

## Backpressure

A bounded response to a producer generating data faster than the consumer can accept it.

## Build context

The explicitly supplied source material visible to an image build.

## Cache

An optional optimization whose absence must not change correctness.

## Capability

A narrowly scoped permission or token for one operation, resource, or attempt.

## Claim

An atomic assignment of eligible work to a particular runner attempt.

## Compiler

The component that validates pipeline input and produces a frozen execution plan.

## Control plane

The services that decide, authorize, persist, and expose system behavior rather than execute repository code.

## Cursor

A stable position used to resume reading ordered events or log segments.

## DAG

A directed acyclic graph; its dependency edges do not contain a cycle.

## Deployment

A tracked change of a target environment to an identified release.

## Digest

A content-derived identifier; useful for integrity, but not proof of producer trust.

## Execution envelope

The complete bounded runtime description handed to an executor.

## Fence

A generation identifier checked to reject stale ownership at a boundary.

## Gitlink

The superproject tree entry selecting a commit in a submodule.

## Heartbeat

A current owner's request to renew its time-limited control lease.

## Idempotency key

An identity under which identical request retries map to one accepted intent.

## Inbox

Durable receipt and processing state for an incoming external event.

## Job

A logical schedulable node whose attempts determine its outcome.

## Lease

Time-limited control ownership; not proof that physical execution stops on expiry.

## Outbox

A durable record of external delivery work committed with the state change that caused it.

## Pool

An authorized grouping of runners with defined capabilities and access rules.

## Provenance

Recorded information about how an output was produced and which inputs and builder participated.

## Reconciliation

Establishing current reality after observations, ownership, or transport become uncertain.

## Release manifest

A record connecting source commits, built outputs, versions, and verification evidence.

## Run

An immutable execution request with source, inputs, compiled graph, and history.

## Snapshot

A fixed representation of state or intent at a defined revision.

## Step

An operation within a job, with defined workspace and exit semantics.

## Superproject

A repository that composes independent child repositories using submodule references.

## Target reservation

A concurrency control preventing incompatible operations on the same external target.

## Trust domain

A scope within which code, credentials, caches, and execution authority are deliberately related.

## Uncertain

A state in which the platform lacks enough evidence to assert the physical outcome safely.

## Workspace overlay

A local development convenience that does not replace independent dependency declarations.
