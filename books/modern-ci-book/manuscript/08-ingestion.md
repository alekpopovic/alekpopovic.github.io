# 8. Commit requests before acknowledging events


## A receipt is part of the transaction

A source webhook may arrive twice, a manual request may be retried after a timeout, and a browser may repeat a submission. Design idempotency as durable data. An in-memory set of recently seen delivery identifiers disappears on restart and diverges across API instances.

For a manual run request, require a project-scoped idempotency key. Record a digest of the normalized request with the response identity. An identical retry returns the existing run. The same key with a different payload returns a conflict. Without the digest, a client can accidentally reuse a key and receive a response to a different request.

For a provider event, use a uniqueness boundary such as provider, installation, and delivery identifier. The event receipt and its durable processing instruction must be committed before acknowledging accepted work. Parsing and authorization failures can receive explicit responses without creating a run.

## Verify exact bytes

GitHub webhook validation uses a secret-derived HMAC signature, supplied in `X-Hub-Signature-256`. Verification must operate on the raw request body and use a timing-safe comparison; decoding and reserializing JSON changes the signed bytes. The included helper demonstrates only this byte-level check. [S15](e-sources.md#s15)

Limit the request body before loading it into memory. Verify content type and expected event kind. Treat the installation and repository identities as untrusted fields until tied to the configured integration. Do not fetch a user-controlled URL from the payload simply because the signature is valid.

Signature validation is not deduplication. A correctly signed payload can be delivered again. GitHub recommends webhook secrets, HTTPS, prompt responses, and identifying deliveries; our design combines those delivery practices with a durable inbox. [S16](e-sources.md#s16)

## Inbox, run, and outbox

One transaction can insert the receipt, create the frozen run, and append an outbox entry describing a notification or scheduling wakeup. If compilation is too expensive for the request path, first commit a durable inbox job, acknowledge it, and let a worker perform the rest. Do not acknowledge an event that exists only in a process-local queue.

An outbox dispatcher reads committed records and sends external notifications. It marks completion after a successful response according to the adapter's contract. A network failure after the remote service acted is ambiguous, so retry with a provider-supported idempotency key where available. Otherwise, tolerate a duplicate notification rather than falsely promising exactly-once delivery.

The scheduler always rereads database state. Losing a wakeup does not lose a run; it merely delays discovery until the next scan. Periodic recovery makes the event transport an optimization instead of a second source of truth.

## Avoid duplicate intent and preserve distinct intent

Deduplication must not collapse two genuinely different source events. A push event and a manually requested rebuild for the same commit may be distinct, legitimate runs. Use event identity and request identity, not source commit alone, as the deduplication key.

Policy can still suppress redundant work intentionally, such as cancelling an older pending branch run when a newer commit arrives. That is a separate, audited scheduling decision. It must not erase the history of a run that has already started deploying.

Provider status updates should name the exact run and commit they represent. A delayed result for an older branch head must not replace the visible status of a newer run through an imprecise lookup such as “most recent project build.”

## Exercise

An API instance inserts a run, sends a notification, and then commits the transaction. The transaction aborts. What do users see, and how should the flow change?

## Worked answer

Users may see a notification referring to a run that never existed durably. The notification can also trigger dependent behavior outside the database. Insert the run and an outbox record within the same transaction, commit, and let a dispatcher send the notification afterward. The dispatcher needs its own idempotency and recovery policy because commit and external delivery cannot be made atomic merely by placing them near each other in code.

## Completion evidence

Test duplicate deliveries across two API instances, conflicting idempotency keys, an abort before commit, a lost response after commit, and a dispatcher crash after sending but before recording completion.
