# 07. Design APIs for Work That Finishes Later

**Part II — Control Plane**

Creating a sandbox is not a short database mutation. It can involve quota
reservation, image policy, cluster dispatch, scheduling, storage provisioning and
runtime readiness. A synchronous endpoint that hides all of this behind a long
HTTP timeout turns normal delays into ambiguous failures.

## Return an operation, not a false completion

A proposed create request is accepted only after authentication, authorization,
validation, quota reservation and durable intent recording. It returns an
operation ID and a session ID. The client observes progress separately. The
operation carries its own lifecycle: accepted, dispatched, running, succeeded,
failed, canceled or outcome unknown. Session lifecycle is related but distinct.

```json
{
  "operation_id": "op_example_001",
  "session_id": "session_example_001",
  "operation_status": "accepted",
  "desired_state": "running",
  "observed_state": "not_observed",
  "observed_at": null
}
```

This is an AgentPlane design example, not a response from an implemented API.
Keeping `observed_at` empty is more useful than inventing a current timestamp for
an event that has not happened.

## Bind idempotency to request identity

Store an idempotency record under authenticated scope, operation type and a
client-supplied key. Bind it to a canonical request digest and the resulting
operation ID. Reuse of the same key with the same request returns the original
operation. Reuse with a different request returns a conflict. Concurrent first
requests must converge through a unique database constraint, not through an
in-memory check.

Define canonicalization. Arbitrary JSON serialization can change ordering or
numeric representation. A typed request digest should cover the semantic inputs
that determine the operation, including scope and template version. Do not include
volatile tracing headers. Treat digests of sensitive small inputs as potentially
revealing: hashing is not encryption and can permit guessing attacks.

Idempotency records need a retention contract. If the server forgets a record
after a day, a retry after two days may create a new operation. Document the
window and make SDK behavior respect it. Long-lived external side effects may
need longer identity retention than ordinary read caches.

## Distinguish retryable failures

A temporary inability to reach the gateway can be retried before execution begins.
An unknown result after the process started is different. A script may have
updated an external system even if its result was lost. Blind retry can duplicate
that side effect. Return an explicit unknown outcome and require reconciliation
or an action-specific idempotency mechanism.

For safe reads, retries can use bounded exponential backoff with jitter. For
writes, reuse the original idempotency key. Never let an SDK create a fresh key
on every retry while claiming the operation is idempotent. Cancellation is a
request to stop remaining work; it is not a rollback of completed external work.

## Use optimistic concurrency for changing intent

A session has an intent version. A client changing lifetime or requesting
termination supplies the version it observed. The server rejects a conflicting
update or explicitly resolves it according to documented rules. Terminal intent
must dominate stale resume requests. Avoid generic “last write wins” for security
and lifecycle state.

Workers should check current intent before starting expensive work. A queued
create operation may have been canceled while the cluster was offline. The
connector also checks the operation's expiry and local policy. One initial
validation does not authorize a command forever.

## Define errors for humans and automation

Use stable machine-readable codes with safe messages. Include a request ID and,
where relevant, an operation ID. Separate invalid input, unauthorized scope,
resource conflict, quota exhaustion, unsupported capability, temporary
unavailability and unknown execution outcome. Clients should not parse English
message text to decide whether to retry.

Do not expose raw Kubernetes error objects that may reveal names outside the
project. Preserve detailed diagnostics in authorized operational channels after
redaction. Bound request bodies, filter fields and pagination sizes. A rich list
endpoint is still an authorization and denial-of-service surface.

## Exercise

Write three create-session tests: simultaneous duplicate requests, a changed
request under the same idempotency key and a retry after the server commits but
before the client receives its response. Then write an execution test where the
external effect succeeds and the response is lost. Explain why that final case
requires more than HTTP idempotency middleware.
