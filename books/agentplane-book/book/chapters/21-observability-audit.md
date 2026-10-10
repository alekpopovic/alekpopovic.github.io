# 21. Observe the System Without Collecting the Customer

**Part VI — State and Evidence**

Operational telemetry and audit evidence serve different purposes. Telemetry
explains performance and failure. Audit records explain authority and sensitive
state changes. Neither requires collecting every prompt, command output, file or
tool argument by default.

## Instrument boundaries rather than payloads

Trace API acceptance, outbox publication, gateway dispatch, connector receipt,
runtime start and final result. Propagate correlation identity across HTTP,
messages and cluster operations. A trace should answer where time was spent and
which boundary failed without copying the user's entire request body.

Use bounded-cardinality metrics for service health: request rates, latency
buckets, queue depth, heartbeat age, reconciliation failures and certificate
expiry. Per-session IDs in metric labels can create an unbounded series count.
Use scoped event records or queryable logs for high-cardinality investigation
instead of turning every object ID into a Prometheus dimension.

OpenTelemetry's sensitive-data guidance emphasizes reducing and controlling the
data collected. Apply that principle at instrumentation time, not only in a
central processor after sensitive content has already crossed the boundary.
[S20](../references.md#s20)

## Define an audit event schema

Record event identity, sequence, scope, actor type, actor ID, action, resource,
outcome, policy version, request identity and a safe timestamp. Prefer typed
metadata over arbitrary maps containing whatever a handler happened to know.
Explicitly exclude credentials, file bodies, process output and raw tool inputs
unless a separate approved retention policy requires them.

For operations that must not occur without evidence, write audit metadata in the
same transaction as intent. A non-critical telemetry exporter can fail without
blocking the API; an audit-critical transaction may need to fail closed. State
which category each event belongs to.

## Hash chains have a trust boundary

A chain links each event hash to the previous hash. Modification, reordering and
removal can be detected when checked against a trusted checkpoint containing the
expected count and head. Without a checkpoint outside the attacker's rewrite
boundary, an attacker can recalculate a new chain. Tail truncation especially
requires an expected end state.

The Python program in [examples/audit](../../examples/audit/README.md) demonstrates
this distinction. It is an educational verifier with a caller-supplied trusted
checkpoint. It is not a public signing service, immutable ledger or replacement
for protected storage. Its tests deliberately show why an internally consistent
rewritten chain is not sufficient evidence.

## Serialize append and anchor independently

A production per-tenant chain needs a serialized append boundary. Use a locked
head row or an equivalent transactional mechanism. Multiple workers cannot
independently append to the same previous hash and still produce one linear
history. At higher scale, use partitioned chains and explicit aggregation rather
than pretending one uncoordinated global chain exists.

Publish signed checkpoints through a key boundary separate from ordinary database
writers, and retain them in a location with a distinct administrative trust
model. A signer whose key is stored next to the writable audit table does not
provide strong protection against compromise of both.

## Evidence bundles are scoped exports

An evidence bundle can include versioned policy, runtime image identity, lifecycle
metadata, approval decisions, usage summaries and a relevant audit range. Include
a manifest of file hashes and the verification method. Verify signatures against
an independently trusted key, not a public key supplied only inside the same
untrusted archive.

Use expiring, authorized downloads and record the export request. Exports can
reveal names, timestamps and business relationships even when they contain no
secret values. Limit retention and protect tenant scope throughout the asynchronous
job, storage key and download endpoint.

## Avoid compliance claims the product cannot prove

Technical evidence can support a review. It does not make an organization
automatically compliant with a law or certification framework. Map controls with
qualified domain review and preserve the exact evidence source and observation
period. A report generated today from old observations is not current assurance.

## Exercise

Run the audit demo and tamper tests. Remove the final event while retaining the
old trusted checkpoint, then build a fresh chain over modified data with a new
untrusted checkpoint. Explain why the first should fail and why the second
requires an external trust decision rather than a better hash function.

## Primary sources

[OpenTelemetry sensitive-data handling](../references.md#s20)
