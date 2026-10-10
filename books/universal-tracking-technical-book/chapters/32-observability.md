## Chapter 32 - Observability and Incident Response

Observability should answer whether the platform is accepting facts, keeping them fresh, processing work, serving authorized clients, and approaching resource limits. It must do so without leaking exact locations or creating high-cardinality metric explosions.

### Structured logs

Use JSON logs with stable fields:

```json
{
  "time": "2026-10-10T10:11:13.120Z",
  "level": "INFO",
  "message": "location batch accepted",
  "service_role": "api",
  "request_id": "0195...",
  "trace_id": "a93f...",
  "organization_ref": "hash:7b12...",
  "device_ref": "hash:91cd...",
  "batch_id": "0195...",
  "accepted_count": 48,
  "duplicate_count": 2,
  "rejected_count": 0,
  "duration_ms": 37
}
```

Use hashed or internal references only when necessary. Do not log coordinates, tokens, raw protocol frames, recipient addresses, or entire payloads.

### Health endpoints

Provide separate endpoints:

- liveness: process event loop and fatal state;
- readiness: ability to serve the role safely;
- startup: optional long initialization check;
- detailed internal diagnostics protected from public access.

A database outage can make API readiness false while liveness remains true. Kubernetes is not required to benefit from these semantics; Nginx, systemd, and monitoring can use them.

### Metrics

Expose Prometheus-format metrics such as:

```text
http_requests_total
http_request_duration_seconds
location_batches_total
location_points_accepted_total
location_points_rejected_total
location_commit_duration_seconds
location_freshness_seconds
websocket_connections
websocket_send_queue_depth
outbox_oldest_pending_seconds
jobs_pending
jobs_oldest_pending_seconds
db_pool_acquire_duration_seconds
db_transactions_total
gps_connections
gps_frames_invalid_total
partition_bytes
wal_archive_last_success_timestamp
backup_last_success_timestamp
```

Labels should be low-cardinality: route template, status class, job type, service role, protocol. Organization, subject, device, task, and request IDs do not belong in metric labels.

### Traces

Optional OpenTelemetry traces are useful across HTTP, database, outbox, and worker processing. Propagate a trace or correlation context through durable jobs, but do not assume the original trace remains sampled or available days later.

A durable event stores correlation IDs for investigation. Workers create new spans linked to the originating context.

### Service-level indicators

Useful SLIs include:

- proportion of batches committed successfully;
- P95/P99 commit latency;
- live propagation latency from `received_at` or commit time;
- percentage of active sessions with fresh data;
- job backlog age by class;
- webhook delivery success within target;
- backup and WAL archive freshness;
- restore drill success;
- false transition or data-quality rate from sampled review.

Alert on symptoms and user impact, not every small metric movement.

### Alert design

Examples:

- ingest error rate exceeds threshold for several minutes;
- database pool acquisition latency rises with saturation;
- oldest critical job exceeds target;
- WebSocket reconnects spike after deployment;
- no points arrive for an organization with active sessions;
- default location partition receives rows;
- disk free space crosses projected safety window;
- WAL archive is stale;
- backup or restore verification fails;
- GPS invalid-frame rate spikes by protocol.

Every alert links to a runbook and has an owner. Avoid pages for conditions that resolve without action.

### Incident timeline

During an incident, record:

- detection time and source;
- user impact;
- recent deployments and migrations;
- metric and log evidence;
- mitigation decisions;
- data integrity checks;
- recovery time;
- follow-up actions.

Do not copy precise customer location data into a general incident channel. Use controlled references.

### Post-incident review

A useful review asks:

- Why did the system allow this failure?
- Which signal should have detected it earlier?
- Which safeguard or runbook was missing?
- Did recovery preserve data integrity and privacy?
- Could a smaller blast radius have been designed?
- Which action is automated and tested, not merely documented?

Avoid blame. The goal is better systems and decisions.

### Chapter checklist

Observability should provide:

- structured, redacted logs;
- distinct liveness and readiness;
- low-cardinality technical and business metrics;
- correlation across durable jobs;
- user-oriented SLIs;
- actionable alerts with runbooks;
- privacy-safe incident handling;
- post-incident actions verified by tests or drills.
