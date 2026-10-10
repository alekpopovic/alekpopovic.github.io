## Appendix B - REST API Blueprint

### Endpoint overview

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/v1/auth/login` | create human session |
| `POST` | `/api/v1/auth/refresh` | rotate refresh token |
| `GET` | `/api/v1/organizations` | list memberships |
| `GET` | `/api/v1/subjects` | list authorized subjects |
| `POST` | `/api/v1/subjects` | create subject |
| `GET` | `/api/v1/devices` | list devices |
| `POST` | `/api/v1/device-enrollments` | begin mobile enrollment |
| `POST` | `/api/v1/tracking-sessions` | start session |
| `POST` | `/api/v1/location-batches` | ingest device locations |
| `GET` | `/api/v1/live/snapshot` | current-state snapshot |
| `GET` | `/api/v1/subjects/{id}/history` | bounded history |
| `GET` | `/api/v1/subjects/{id}/trips` | derived trips |
| `POST` | `/api/v1/geofences` | create geofence |
| `GET` | `/api/v1/alerts` | list alert incidents |
| `POST` | `/api/v1/public-shares` | create scoped share |
| `POST` | `/api/v1/exports` | request asynchronous export |
| `POST` | `/api/v1/webhooks` | create webhook subscription |

### Pagination

Use opaque cursors. A list response:

```json
{
  "items": [],
  "page": {
    "next_cursor": "eyJ2IjoxLCJ0Ijoi...",
    "has_more": true
  }
}
```

The cursor is signed or authenticated and includes sort position, filters, and version. Do not expose a raw offset for large changing datasets.

### Conditional updates

A resource response includes version:

```json
{
  "id": "0195...",
  "name": "Courier 42",
  "status": "active",
  "version": 7
}
```

An update carries expected version:

```http
PATCH /api/v1/subjects/0195...
If-Match: "7"
```

A conflict returns `409` or `412` according to the chosen convention with current version and stable error code.

### Error envelope

```json
{
  "error": {
    "code": "subject_version_conflict",
    "message": "The subject was changed by another operation.",
    "request_id": "0195...",
    "details": {
      "expected_version": 7,
      "current_version": 8
    }
  }
}
```

### Live snapshot

```http
GET /api/v1/live/snapshot?team_id=0195...
```

```json
{
  "snapshot_version": 990120,
  "generated_at": "2026-10-10T10:11:13Z",
  "subjects": [
    {
      "subject_id": "0195...",
      "name": "Courier 42",
      "kind": "person",
      "recorded_at": "2026-10-10T10:11:12Z",
      "freshness_seconds": 1,
      "connection_status": "online",
      "movement_status": "moving",
      "position": {
        "latitude": 44.8123,
        "longitude": 20.4611,
        "precision": "exact"
      },
      "version": 883
    }
  ]
}
```

### History

```http
GET /api/v1/subjects/0195.../history\
?from=2026-10-10T08:00:00Z\
&to=2026-10-10T10:00:00Z\
&limit=5000
```

The server enforces a maximum interval and row count. Long requests become exports.

### Public share

```json
{
  "subject_id": "0195...",
  "session_id": "0195...",
  "expires_at": "2026-10-10T18:00:00Z",
  "precision_policy": "rounded_100m",
  "delay_seconds": 300,
  "allowed_fields": ["position", "status", "eta"]
}
```

The response displays the raw token once. Only its hash is stored.

### Idempotency

Commands that may be retried accept `Idempotency-Key`. The server binds the key to principal, route, and payload hash for a defined period. Reuse with a different payload returns an idempotency conflict.

### Rate limits

Return documented headers without relying on them for security:

```text
RateLimit-Limit
RateLimit-Remaining
RateLimit-Reset
Retry-After
```

Limits may vary by principal type, endpoint, and plan. Sensitive login and public-link endpoints use additional abuse controls.
