# 16. Move durable processing to PostgreSQL

## Preserve the contract when changing storage

SQLite is useful for an inspectable single-node laboratory. PostgreSQL becomes appropriate when ingestion, detector workers, delivery workers, and operators need controlled concurrent access. A database migration should preserve behavior before it improves throughput.

Keep event uniqueness on authenticated node and request ID. Preserve immutable event digests and original decision expiries. Add durable jobs and delivery intent as transactional records. Test the same retry and replay scenarios against the new storage implementation. If an optimization removes one of those invariants, it is a behavior change rather than a transparent migration.

The delivered `companion/sql/production-schema.sql` is a teaching schema for events, detector jobs, decisions, and delivery work. It is not a tested migration for an existing database. Production migrations need versioning, rollback or forward-repair strategy, representative data, and execution against the actual PostgreSQL version.

## Claim a job, then commit its effect

Several workers can claim available rows using row-level locking with `SKIP LOCKED`. This is useful for a queue-like workload, but it does not automatically serialize every shared counter those jobs will update. Two different events for the same site and address may be claimed by different workers.

A transaction outline is:

```sql
BEGIN;
SELECT id, node_id, request_id
FROM detector_jobs
WHERE completed_at IS NULL
ORDER BY id
LIMIT 1
FOR UPDATE SKIP LOCKED;

-- Lock or atomically update the shared detector state.
-- Write a detection and decision when appropriate.
-- Write delivery intent in the same transaction.
-- Mark the claimed job completed.
COMMIT;
```

The comments identify required application work; this listing is not a complete worker. Hold the claim lock until the effects and completion commit together. A worker crash before commit leaves the job eligible. A crash after commit leaves its effects recorded once.

## Serialize the detector's shared key

The relevant shared state is usually site, address, rule version, and time window. You can use a dedicated row lock, a carefully defined advisory lock, or an atomic SQL design. The choice must handle concurrent events for the same key and independent events for different keys.

An in-process mutex does not coordinate separate worker processes. A queue row lock coordinates that row, not every event from the same visitor. Process-local counters make behavior dependent on which worker happens to receive an event. Start with one detector worker, demonstrate correctness, then add concurrency with a race test designed to expose lost or repeated increments.

Window processing also needs a policy for out-of-order events. A simple fixed bucket boundary can miss a burst split across two buckets. A rolling window can require more retained state. The lab uses a direct query because the scale is small. Production should choose a window model deliberately and preserve freshness exclusion before counting.

## Outbox as a transaction boundary

Create desired decisions and delivery intent together. Otherwise a crash can leave a committed ban with no durable instruction to publish it. A delivery worker can later derive a full per-agent snapshot, allocate a revision, sign it, store its bytes, and retry those bytes while fresh.

Signing can involve external secret infrastructure. Do not hold a high-contention detector lock while waiting indefinitely for it. Define how unsigned intent becomes signed, persisted delivery work and how a crash at that boundary is repaired. Revision allocation and exact stored bytes still need a coherent transaction design.

Notifications are a latency optimization. A worker must also scan durable pending work after restart or a missed notification. Relying on a transient message as the only work record recreates the ingestion gap that the database was meant to close.

## Exercise

Two workers claim different event rows from the same site and address. Each reads a shared counter value of four and each writes five. What is lost, and which lock did not solve the problem?

## Answer

One increment is lost, and both workers may make an inconsistent threshold decision. Locking each queue row did not serialize the shared detector key. Use a shared-state lock or a correct atomic update, and commit the decision and job completion with the counter effect. A real PostgreSQL concurrency test is required for this migration.
