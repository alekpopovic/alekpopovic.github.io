# Chapter 15 - Events, Audits, and Notification Boundaries

Atlas API changed replicas, a task failed and an operator wants to know what happened. Three different records may answer parts of that question: a domain event says a change occurred, a diagnostic log explains a code path, and an audit record attributes an operation to an actor. A webhook adds a fourth concern: delivering a selected observation to another system. Treating all four as one durable stream would hide their different storage and failure semantics.

This chapter assumes the service lifecycle and transaction discussion. You will reconstruct an actual in-process Atlas event sequence, trace actor/redaction fields and examine a notification retry without claiming an exactly-once external effect. Default MemoryService history remains process-local. The original durable-events prompt title is historical requested scope, not proof that the default binary persists its event history.

## Events, Diagnostic Logs, and Audits

Domain events have an ID, namespace, type, severity, source, message, related-object identity and timestamp. Their purpose is to connect observations to service/task/node changes. Diagnostic logs instead describe the executing code's behavior, such as a failed Engine call or retry. An audit record adds actor type/ID, action, target, request ID, source IP, outcome and redacted metadata. [Claim ch15.record-types](../../validation/evidence/ch15.json).

A single Atlas scale request can therefore produce a service.scaled event and an audit operation while also generating diagnostic logs. Their identifiers and ordering are related only where the implementation explicitly connects them. An event's source string agent is not the same thing as a cryptographically attributable audit identity. A log line containing a service name is not a durable mutation receipt.

The teaching fixture used the real MemoryService methods to register a node, create atlas-api, accept pulling/created/running/healthy reports and scale to two. It did not execute a container: the report source is explicitly injected, and its container ID says fixture-container-no-docker. The [actual event capture](../../validation/labs/ch15/atlas-events-corrected.json) contains seven events with generated IDs and UTC timestamps. [Claim ch15.timeline](../../validation/evidence/ch15.json).

Read that capture in chronological order because ListEvents returns the newest observations first. It contains node.registered, service.created, four task.status events and service.scaled. The task.status messages are generic; their event text alone does not encode every reported lifecycle value. The fixture's request sequence supplies that additional context. This is a useful limit on reconstructing a deployment exclusively from human-readable messages.

| Record | Primary question | Example scope |
| --- | --- | --- |
| Domain event | What state-related observation occurred? | service.scaled related to a service ID |
| Diagnostic log | What did this execution path encounter? | Runtime error while polling a task |
| Audit | Who attempted which operation with what outcome? | Actor, action, target and request metadata |
| Notification delivery | Was a selected event sent to a sink? | HTTP attempts and final response |

The actual process/Docker deployment has separate evidence in the book's runtime lab. Do not substitute the in-process timeline for proof of image pull, network reachability or workload execution. The value of this fixture is that it exercises the real event-generation methods with a tightly controlled sequence while keeping those physical effects out of scope.

## Attribution, Redaction, and History

The API's recordAudit path derives an actor, constructs a Log and appends it through the configured audit store. An authenticated principal supplies a user subject. Agent routes can use node metadata, while absent identity has explicit fallback values such as unknown or anonymous. A fallback value is a signal of limited attribution, not proof a named human performed the request.

Request ID and source IP help correlate observations, but their trust depends on how the request reached the server. The code accepts forwarded metadata; a deployment that exposes the API directly must not assume every forwarded value came from a trusted reverse proxy. Correlation is useful even when a field is untrusted, provided it is not silently promoted to an authenticated identity claim.

Audit.Normalize trims fields, supplies defaults, normalizes timestamps to UTC and calls RedactMetadata. Redaction inspects metadata keys for markers such as password, token, secret, authorization and credential. URL metadata can have embedded user information replaced. This is a concrete heuristic with a known input shape, not a universal parser for all secrets in arbitrary prose.

[internal/audit/audit.go, lines 92–107](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/audit/audit.go#L92-L107) at the locked revision.

```go
func redactMetadataValue(key string, value string) string {
	if isSensitiveMetadataKey(key) {
		return "[REDACTED]"
	}
	if strings.Contains(strings.ToLower(key), "url") {
		parsed, err := url.Parse(value)
		if err == nil && parsed.Scheme != "" && parsed.Host != "" && parsed.User != nil {
			parsed.User = url.User("[REDACTED]")
			return parsed.String()
		}
	}
	return value
}

func isSensitiveMetadataKey(key string) bool {
	normalized := strings.ToLower(strings.ReplaceAll(strings.TrimSpace(key), "-", "_"))
```

If a secret appears under a harmless-looking key or in an unrecognized message format, a key-based rule may not find it. Conversely, a key containing a sensitive substring can be redacted even when the value is not secret. Prefer constructing minimal metadata at the source rather than treating the sanitizer as permission to include entire request bodies, environment maps or raw credentials. [Claim ch15.redaction](../../validation/evidence/ch15.json).

The API audit append is best effort in the inspected path: failure is logged rather than automatically rolling back the completed user operation. That distinction differs from transaction-scoped strict domain events used by some controllers. An operator can receive successful mutation behavior while the audit write fails. If a future requirement demands every privileged mutation have an atomic durable audit record, it needs an explicit transaction/operation design.

The domain events helper also makes its mode visible. Emit defaults missing timestamps/severity and attempts AppendEvent. In best-effort mode, append failure is logged and Emit returns nil. With Strict, the append error is returned so a transactional caller can abort. Strict emission without a transactional enclosing mutation is still not a complete atomicity guarantee: the mutation may already have occurred elsewhere.

## Notification Delivery as an External Effect

The notifier has an explicit set of event types eligible for delivery. Dispatcher.Notify ignores unrelated types, loads sinks and sends to them sequentially. Sender.Deliver validates a sink, redacts the event, builds a JSON Delivery payload and performs HTTP POST attempts. Default settings are three attempts, 100 millisecond base exponential backoff and a client timeout. [Claim ch15.delivery](../../validation/evidence/ch15.json).

[internal/notifications/notifications.go, lines 86–105](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go#L86-L105) at the locked revision.

```go
	var last error
	for attempt := 0; attempt < s.attempts; attempt++ {
		req, err := http.NewRequestWithContext(ctx, http.MethodPost, sink.URL, bytes.NewReader(payload))
		if err != nil {
			return err
		}
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("User-Agent", "orch-notifier/1")
		if sink.SigningSecret != "" {
			mac := hmac.New(sha256.New, []byte(sink.SigningSecret))
			_, _ = mac.Write(payload)
			req.Header.Set("X-Orch-Signature", "sha256="+hex.EncodeToString(mac.Sum(nil)))
		}
		resp, err := s.client.Do(req)
		if err == nil {
			_, _ = io.Copy(io.Discard, resp.Body)
			_ = resp.Body.Close()
			if resp.StatusCode >= 200 && resp.StatusCode < 300 {
				return nil
			}
```

When a signing secret exists, the sender attaches an HMAC-SHA256 signature over the payload. That lets a correctly configured receiver verify payload authenticity relative to the shared key. It does not encrypt the payload, authenticate every downstream workflow or prevent the receiver from processing the same event twice. The payload contains a timestamp and event identity that can support receiver-side deduplication, but no exactly-once receiver behavior is implemented here.

The failure window is an HTTP response lost after the receiver accepted the request. The sender sees a transport failure and retries; the receiver may now observe the same notification more than once. A two-hundred response establishes acceptance by that HTTP endpoint, not successful completion of whatever incident workflow it triggers. Reliable external automation should be designed around idempotent event identity and explicit handling of duplicates.

The actual focused notifier fixture uses a fake RoundTripper. It returns service-unavailable twice, then success, captures the body and signature and checks that selected secret values are absent. The second fixture exercises delivery failure and the dispatcher event filter. These tests [passed](../../validation/labs/ch15/focused-tests.json). They do not send a real webhook, validate arbitrary receiver software or prove every possible secret representation is redacted.

A separate integration concern is how notifications are invoked. MemoryService appends an event to its in-memory slice, then launches a goroutine calling Notify with context.Background and discards its returned error. The user mutation does not wait for delivery, which isolates its immediate latency from the sink. It also means there is no durable delivery queue, retry-after-process-restart record or guaranteed shutdown drain in that path.

Repeated failures can consume goroutines and outbound requests while the process remains alive; losing the process loses those transient delivery activities. A teaching outbox design would store the event and a delivery intent transactionally, then process bounded attempts with deduplication and retention. That is a prospective extension, not a capability inferred from the current Sender type.

## When History Is Not Durable

The default server's event and audit collections belong to MemoryService. Retention settings can remove older entries from those collections, but they do not persist them. A fresh server process starts new maps/slices. The PostgreSQL store and event tables exist as implemented packages, yet their existence does not redirect the running application's writes. [Claim ch15.durability](../../validation/evidence/ch15.json).

This changes the operational interpretation of an empty history page. It may mean no matching events, a filter mismatch, retention or process state loss. An API response containing zero events is not proof no operation ever happened. Preserve critical lab output before intentionally restarting or deleting the service; use UTC timestamps and IDs to distinguish a fresh run from an earlier one.

Events and audits also have different visibility permissions and filters. A service filter is useful for a timeline but can omit node-level observations relevant to a task failure. Audit access requires its actual API authorization, not the same assumption used for reading application logs. Build an incident bundle deliberately: service/task/node state, relevant domain events, authorized audit metadata and diagnostic/runtime logs each contribute different evidence.

History begins with [7ff58cef0f736ac9076942ce3ef1039d1fe72c72](https://github.com/alekpopovic/orch/commit/7ff58cef0f736ac9076942ce3ef1039d1fe72c72), which adds event APIs/helpers and related fields. [7935c334dcd264e70abb9e795889010b9ecdb03b](https://github.com/alekpopovic/orch/commit/7935c334dcd264e70abb9e795889010b9ecdb03b) adds audit attribution/redaction paths. [4d641bbe8913da568d6d9f4697a0144314e10b87](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87) batches notification work with jobs, storage and DNS. Do not invent a separate commit for every late development prompt. Original13 is retrospective intent;46 and 80 identify later audit/notification requests.

## Atlas Lab: Capture a Timeline and Test a Sink

The safe lab needs Go 1.25 and the disposable source copy, with no Docker or database. Copy examples/teaching-extensions/ch15/main.go into book-events beneath that module, then run it using the pinned toolchain and run-owned caches. The fixture asserts that service creation, scaling and task-status events exist and emits the real event fields as JSON.

```sh
go run ./book-events
go test ./internal/events ./internal/notifications \
  -run 'TestEmit|TestDelivery' -count=1 -v
```

The actual fixture had an initial compile error in its teaching registration field name; that raw attempt is preserved separately. The corrected fixture uses the real NodeRegistration.Name field and passed. No upstream source changed. This is why the reproducible artifact is the corrected canonical fixture plus its named execution record, not a rewritten claim that the first attempt worked.

Inspect event IDs and related-object IDs, reverse the returned order for a chronological display and identify where generic messages need request context. Then examine the fake sink's three attempts, signature prefix and redacted payload assertions. The fake transport avoids external requests and cannot change a real incident-management account. Cleanup is ordinary process exit and optional removal of the copied teaching directory.

For an optional live Atlas capture, run events with an explicit server, namespace and service filter, save the actual output before cleanup and keep node-level history separately. Never include bearer tokens or secret request values. A local HTTP sink should bind loopback, be owned by the run and use disposable signing material. Record its received event IDs to detect duplicates rather than assuming a successful sender return means unique processing.

## Exercises

1. Why do four generic task.status events not independently prove four specific lifecycle values? Which additional record supplies that meaning?
2. Compare best-effort Emit, strict Emit and a strict event inside a database transaction. Which failure can roll back the mutation?
3. Explain how a notifier can deliver twice after only one event was appended. What receiver key should be used for deduplication?
4. An operator restarts the default server and sees an empty event list. Enumerate plausible interpretations and the evidence needed to distinguish them.

[Worked answers](../solutions/ch15.md) connect record shape, atomicity and delivery scope. Preserve separate evidence channels and name their storage lifetime before using history as an operational guarantee.
