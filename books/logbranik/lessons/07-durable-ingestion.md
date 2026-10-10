# 7. Commit events before acknowledging them

## Validate at the boundary

An ingestion API must bound work before parsing the entire request. Limit body bytes, line bytes, event count, and field lengths. Check version, request-ID shape, authorized site, valid address, method, path, status, duration, byte count, and outcome. Reject nonfinite numbers and booleans where the schema requires an integer.

Why distinguish a boolean from an integer? Python considers `True` an instance of `int`. A loose revision or status validator can therefore accept a JSON boolean as an apparently valid numeric value. The laboratory's integer helper checks the exact type. Protocol schemas must describe wire types, not just the language's inheritance hierarchy.

The parser also rejects duplicate JSON keys. Two fields with the same name can be interpreted differently by separate components. A signature may authenticate the bytes while one component sees the first value and another sees the last. Removing that ambiguity is a protocol decision, not merely a stylistic preference.

## Define deduplication identity

The uniqueness key is authenticated node identity plus generated request ID. A request ID alone may collide across independently configured producers. A node field in the body is not authenticated identity. The TLS registry supplies the node separately.

For a first event, persist its validated representation and an immutable digest. For an identical retry, count a duplicate and preserve the original. For a retry with changed content, quarantine the conflict and retain the original. Changing content under an existing identity is not a normal retry; it is evidence of a broken or hostile producer.

The laboratory hashes a stable encoding of the validated incoming JSON before normalizing the client IP. This means reordered object keys do not cause a conflict, while changed values do. IPv4-mapped address normalization still gives the detector and agent a common address identity.

## Transaction scope

The teaching implementation serializes an ingestion transaction using a process lock and SQLite's immediate write transaction. It inserts new observations, updates detector effects, and commits before returning counters. If an entire batch is too large, no transaction begins. Invalid individual lines become bounded reason records; valid neighbors can commit.

This model intentionally favors clarity over throughput. A production system usually separates ingestion from detector work, while preserving an atomic connection through durable job rows. The transaction inserts the event and the pending job together. A notification can wake a worker, but the durable row is what survives a restart.

The important invariant is that success means the contract's required data is durable. A successful process-local queue insertion is not enough. A lost response is handled by deduplication; a lost in-memory event after a successful response cannot be repaired by a collector that believes its work is complete.

## Distinguish storage and processing

The event's ingest status should not be confused with detection status. An accepted event may be too old for a fresh ban. It may have an outcome excluded by the detector. It may be valid history without triggering any rule. Saving every valid event does not mean every event is allowed to affect enforcement.

Persist the reason for processing ineligibility when it helps investigation. In the compact schema, the `eligible` flag is sufficient for the demonstration. A production schema should retain a bounded reason such as stale event, future timestamp, guard feedback, or unsupported observation context.

## Keep poison data bounded

Quarantine is not a limitless second database. Cap record count, sample size, and retention. Do not copy credentials into an error message. Avoid returning detailed server internals to a producer. The laboratory stores only a short validation reason and timestamp. Production operations may need a redacted sample, but that is a deliberate addition with access controls.

## Exercise

The API inserts ten events, returns 200, and then crashes before creating detector jobs. Is retrying the same batch enough to recover?

## Answer

Not if duplicate handling skips the already inserted events and no durable pending work exists. The system can permanently miss their detection effects. Insert events and durable jobs in one transaction, or make detector discovery of unprocessed events a durable, repeatable scan. The lab avoids the gap by completing detection effects within its ingestion transaction.
