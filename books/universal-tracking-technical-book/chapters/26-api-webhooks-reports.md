## Chapter 26 - Developer API, Webhooks, Exports, and Reports

External systems need stable access without inheriting internal database structure. The developer surface includes scoped API clients, signed webhooks, asynchronous exports, and documented limits.

### API clients

An API client belongs to an organization and has explicit scopes:

```text
api_clients
  id
  organization_id
  name
  status
  scopes
  allowed_cidrs
  created_by

api_client_credentials
  id
  client_id
  secret_hash
  expires_at
  revoked_at
```

Display a new secret once. Store only its hash. Support overlap during rotation and audit every credential change.

Machine tokens use a distinct audience and principal type. They do not inherit a human owner's full permissions.

### REST design

External endpoints should be conservative:

- stable `/api/v1` contracts;
- cursor pagination;
- explicit field and time filters;
- bounded history windows;
- idempotency for commands;
- rate-limit headers;
- deprecation notices;
- deterministic error codes;
- OpenAPI examples and generated clients.

Do not expose internal numeric database tuning fields or outbox details as public contracts.

### Webhooks

A webhook subscription contains URL, event types, secret version, status, and delivery policy. Before activation, validate the endpoint and defend against server-side request forgery.

SSRF controls include:

- require HTTPS in production;
- resolve and reject loopback, link-local, private, and reserved addresses unless explicitly allowed;
- revalidate DNS on delivery to reduce rebinding risk;
- restrict redirects;
- limit ports;
- set connect and response timeouts;
- limit response bytes;
- use an egress policy at the network layer.

### Signature

Sign the exact transmitted bytes with a timestamp and event ID:

```text
X-Tracking-Event-Id: 0195...
X-Tracking-Timestamp: 1791630000
X-Tracking-Signature: v1=hex(hmac_sha256(secret, timestamp + "." + body))
```

Receivers verify timestamp tolerance, event ID deduplication, and constant-time signature comparison. During rotation, include the key version or accept two secrets for a bounded overlap.

### Delivery lifecycle

Each webhook event creates a delivery job with an idempotent event ID. Store attempts and a bounded response summary. Retry transient failures with backoff. Disable or pause subscriptions after a documented failure policy and notify an administrator.

External delivery is at least once. Receivers must deduplicate.

### Exports

Large CSV, JSON, GPX, or spreadsheet exports run asynchronously:

1. validate authorization and requested scope;
2. create an export request with policy snapshot;
3. enqueue a job;
4. stream database rows without loading all data into memory;
5. write to provider-neutral storage;
6. checksum and mark ready;
7. provide a short-lived authorized download;
8. delete after expiry.

Defend against spreadsheet formula injection by escaping cells beginning with characters such as `=`, `+`, `-`, or `@` when producing CSV/XLSX for untrusted data.

### Reports

Reports read derived summaries for long intervals and raw points only for bounded detail. Each report records:

- generation time;
- source interval;
- timezone used for calendar grouping;
- algorithm versions;
- filters;
- data-quality exclusions;
- report version.

A customer should be able to reproduce why two reports differ after an algorithm update.

### Developer sandbox

A sandbox can run the same API with synthetic organizations and a simulator. Provide examples for:

- creating a subject and device;
- enrolling a mobile installation;
- uploading a batch;
- subscribing to realtime updates;
- receiving and verifying a webhook;
- querying bounded history;
- creating a public link.

Never put production personal data in a shared sandbox.

### Chapter checklist

The integration surface should provide:

- organization-scoped API clients and rotating secrets;
- stable versioned contracts and limits;
- SSRF-resistant webhook delivery;
- signed at-least-once events;
- streaming asynchronous exports;
- reproducible versioned reports;
- a synthetic developer sandbox and working examples.
