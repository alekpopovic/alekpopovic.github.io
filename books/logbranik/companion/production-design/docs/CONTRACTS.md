# Protocol contracts v1

All timestamps use UTC RFC3339 with a Z suffix. Parse strictly with bounded sizes. Production
transport verifies CA, hostname and client identity; do not disable TLS verification. Unknown
protocol versions fail validation. Files in examples/contracts are unsigned structural samples.

## Event ingestion

`POST /v1/events:batch` accepts `application/x-ndjson`, one JSON event per line, including
an optional final newline. Support bounded gzip after decoded-size enforcement. Defaults:
1 MiB decoded body, 500 events, 16 KiB line, 2,048-character path. Validate at both ingress
and application; never buffer an unbounded body. Collector maximum batch bytes must fit.

Each raw log event has: `schema_version` (1), `request_id` (Nginx-generated 32 hex chars),
`event_time` (UTC normalized from Nginx timestamp), `site_id` (configured by deployment),
`client_ip`, `method`, `path` (no query), `status`, `request_time_ms`, `bytes_sent`,
`enforcement` (`allow`, `block`, `would_block`, `bypass`, `unavailable`, or `unknown`).
Wire numeric log strings are converted by Vector before API validation. The source log
uses request_time_seconds; normalize to request_time_ms in the collector.

Node identity comes from the certificate. A node is authorized only for registered sites.
Use `(node_id, request_id)` uniqueness; duplicate identical payloads count once, while
duplicate IDs with conflicting fields create a security counter/quarantine and cannot
replace the original. An immutable ingress hash supports this check. Never trust a client
header as the request ID, client IP, or site scope.

Successful commit: `200 {accepted, duplicates, quarantined}`. Invalid individual records are
durably quarantined with a capped redacted sample and do not force endless retries of valid
neighbors. A malformed whole request uses 400/413/415 and alerts; authentication failure
uses 401/403; overload uses 429; transient storage failure uses 503. Validate Vector's actual
retry behavior against this contract and surface all permanent drops. Return no success
before durable commit. An empty batch is 400. A JSON array is not NDJSON.

## Local check

`GET /v1/check` on the agent Unix socket only. Headers: `X-Guard-IP`, `X-Guard-Site`.
Nginx overwrites these and forwards no original visitor headers or body. Output: 204 allow,
403 block, 400 invalid trusted input, 503 state not ready. `X-Guard-Outcome` records the
outcome; `X-Guard-Revision` records the local revision. No visitor-readable evidence or
control details are required. Unknown site fails check validation rather than becoming a
global decision. The optional Nginx availability profile handles 503, not 403 or 400.

## Snapshot structure and signature

`POST /v1/snapshots` on the agent mTLS control listener accepts an envelope with
`key_id`, `payload_b64`, `signature_b64`. Ed25519 signs exactly:
`UTF8("nginx-guard/snapshot/v1") || 0x00 || BASE64_DECODE(payload_b64)`.
Use standard base64. Verify these exact bytes before parsing payload JSON; do not reserialize
JSON for signature checks. Reject duplicate JSON keys, unknown envelope keys, unknown
key IDs, malformed encodings, oversized input and unsupported versions. Public verification
keys are provisioned independently; an untrusted message cannot add a trusted key.

Decoded payload fields:

| Field | Contract |
|---|---|
| schema_version | Integer 1 |
| agent_id | Must match this provisioned agent |
| epoch | Provisioned random stream epoch; never auto-accept a replacement |
| revision | Monotonic positive integer <= 2^63-1 per agent/epoch |
| issued_at | Issuance timestamp, within allowed clock skew |
| valid_until | Delivery window, default issued_at + 120 seconds |
| sites | Full authorized site list with monitor/enforce mode |
| allowlist | Exact IP or manually approved CIDR, site or global scope |
| decisions | Complete active desired bans for this agent |

Each decision has `decision_id`, `site_id` (or explicit `*` manual scope), `ip`,
`issued_at`, `expires_at`, `reason_code`, `source` (`automatic` or `manual`),
`rule_version` (or null), and bounded `evidence_ids`. Decisions do not execute commands
and cannot name files, sockets or arbitrary URLs. Exact IP parsing uses standard address
libraries; normalize IPv4-mapped IPv6 consistently, reject zone identifiers and hostnames.

Snapshot body limit: 8 MiB; active decision default limit: 50,000, with both limits enforced.
Automatic bans: initial 15 minutes; configured maximum 24 hours. Manual TTL is mandatory,
maximum 7 days by default. Site IDs must be registered. Agent validates TTL independently.
Local emergency allowlist is provisioned separately and overrides every remote block.
Central allowlist also wins; block rules cannot remove the local emergency controls.

## Revision and freshness rules

Persist epoch, highest applied revision, exact payload hash and state together. A newer valid
revision replaces the complete state. A lower revision is rejected. An identical revision with
the same payload hash is an idempotent acknowledgement and never republishes state;
same revision with different bytes is a conflict. For that exact duplicate only, an expired
delivery window may still receive the recorded acknowledgement, because nothing is applied.
All new applications require a valid delivery window. Serialize update handlers.

Every newly serialized snapshot, including refreshed issuance timestamps or changed
allowlists/site modes, gets a new revision from the database transaction. Retries reuse the
stored bytes while fresh. An expired undelivered envelope is superseded by a new revision
recomputed from current desired state. Old deliveries cannot resurrect a revoked ban.
Empty decisions is a legitimate signed replacement that clears remote bans.

Persist and publish before responding `200 {agent_id, epoch, revision, payload_sha256,
applied_at}`. Sender checks all identity/revision/hash fields before marking delivery applied.
Use 409 for revision/epoch conflicts, 422 for semantic invalidity, 401/403 for identity failure,
413 for oversize and 503 for temporary persistence failures. Revision gaps are allowed
because snapshots are complete. Mixed-version rolling upgrades fail safely.

## Reconciliation and lifecycle

Agent authenticates to `GET /v1/agents/{self}/snapshot?after_revision=N`. Central returns
204 when current or a fresh signed envelope otherwise; it reissues expired pending content
with a new revision. Default poll 15 seconds with jitter, independent of push. A fresh
snapshot reconciles from desired state; it does not reset individual decision expiries.
Heartbeats report revision, bypass state, clock health, version and capacity every 30 seconds.
Never allow a collector credential to use agent or operator endpoints.

On startup, verify the saved signed snapshot against pinned keys, epoch and hash, then retain
only unexpired decisions. The delivery validity window does not invalidate an already applied
persisted state on restart. A first-ever unsynchronized agent reports not-ready until it receives
a valid snapshot (including an empty one). An offline agent prunes expired decisions.
Clock monitoring and monotonic deadlines while running prevent backward-clock extension;
after restart with an untrusted clock, do not enforce unverifiable remaining TTLs: alert and
enter the documented unavailable state until time/reconciliation is healthy.

After central database restore, an older revision must not override an agent. Recover the
revision high-water mark using authenticated agent reports and operator reconciliation,
or explicitly re-enroll a new epoch through an operator-controlled local provisioning step.
After loss of local state, bootstrap from fresh central state; a tamper-resistant monotonic
counter against a compromised root user is outside this system's trust model.

## Operator API

`GET /v1/nodes`, `/v1/sites`, `/v1/events`, `/v1/detections`, `/v1/decisions`,
`/v1/deliveries`, `/v1/audit`; bounded pagination and scope filters.
`POST /v1/decisions` creates a manual TTL decision with idempotency key and reason.
`POST /v1/decisions/{id}:revoke` changes desired state and writes outbox atomically.
Allowlist and site mode writes use optimistic concurrency. Distinguish desired, queued,
applied, expired and revoked status; a committed central change is not yet proof of enforcement.
