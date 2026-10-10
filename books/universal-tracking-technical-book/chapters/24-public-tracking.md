## Chapter 24 - Public Tracking and Precision Controls

Public tracking is useful for deliveries, races, safety check-ins, and temporary sharing. It is also an easy path to accidental surveillance. Treat a share link as a scoped capability with its own identity and policy.

### Capability record

Store only a hash of the bearer token:

```text
public_share_links
  id
  organization_id
  token_hash
  subject_id
  session_id
  purpose
  valid_from
  expires_at
  revoked_at
  precision_policy
  delay_seconds
  history_window_seconds
  allowed_fields
  max_views
  view_count
  created_by
```

The URL contains a high-entropy random token. The database record contains scope. A leaked link cannot be expanded by query parameters.

### Response minimization

A public endpoint returns only allowed data. Possible modes include:

- exact live position;
- rounded position within a configured radius;
- delayed position;
- approximate area;
- route progress without marker;
- ETA and status only;
- last checkpoint only.

Precision reduction occurs on the server. Example grid snapping should use a geospatial method appropriate to latitude and desired distance; naive decimal rounding has different physical size by latitude.

### Private zones

A subject can define home or sensitive zones where sharing is hidden, delayed, or replaced with an area. Private zones must be applied before public data is serialized. They may also apply to internal roles depending on policy.

A route leaving home can begin outside a privacy radius rather than revealing the driveway. Similarly, the end of a public exercise route can be truncated.

### Expiry and revocation

Links have short default expiry and can be revoked immediately. A worker marks expired links, but request authorization must also compare the current time so correctness does not depend on the worker.

Revocation should invalidate active WebSocket subscriptions. The realtime gateway receives a durable event and closes or downgrades the connection.

### Public application

The public Angular application should be lightweight and isolated from the authenticated dashboard. It displays:

- purpose and shared subject label;
- current status and freshness;
- map or ETA according to scope;
- expiration time;
- privacy notice;
- no organization navigation or hidden API features.

Avoid third-party analytics that receive the tracking token or precise URL. Use a strict referrer policy and content security policy.

### Caching

Public responses are sensitive. Default to private or no-store caching unless a deliberate edge-caching design uses token-independent, policy-safe keys. A CDN log can itself become a location access log, so retention and access must be considered.

### Abuse controls

Protect links with:

- high-entropy tokens;
- request rate limits;
- optional PIN or recipient verification for sensitive cases;
- maximum views;
- anomaly detection for broad geographic access;
- revocation UI;
- access audit without excessive fingerprinting.

Do not use sequential share IDs as the secret.

### Public WebSocket

A public socket authenticates with the capability token and subscribes only to the share's logical channel. The server applies precision, delay, and field filters to each delta. It never publishes a precise internal event and relies on the browser to hide fields.

Delayed sharing needs a durable buffer or query of eligible events by occurrence time. Do not use an in-memory timer as the only mechanism.

### Chapter checklist

Safe public tracking uses:

- hashed high-entropy capability tokens;
- immutable server-side scope;
- short expiry and immediate revocation;
- server-side precision and private-zone controls;
- a minimal isolated public application;
- conservative caching and referrer policy;
- abuse controls and meaningful access audit;
- policy-filtered realtime messages.
