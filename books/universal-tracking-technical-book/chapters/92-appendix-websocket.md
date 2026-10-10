## Appendix C - WebSocket Protocol Blueprint

### Connection

```text
wss://track.example.com/ws/v1
```

Authentication can use a short-lived ticket created through REST, avoiding long access tokens in URLs. Browser origin is validated.

### Client hello

```json
{
  "protocol_version": 1,
  "type": "hello",
  "client_id": "dashboard-installation-id",
  "snapshot_version": 990120,
  "capabilities": ["location-v1", "alerts-v1"]
}
```

### Server hello

```json
{
  "protocol_version": 1,
  "type": "hello.accepted",
  "connection_id": "0195...",
  "server_time": "2026-10-10T10:11:13Z",
  "heartbeat_seconds": 25,
  "maximum_subscriptions": 100
}
```

### Subscribe

```json
{
  "protocol_version": 1,
  "type": "subscribe",
  "request_id": "client-77",
  "channel": "teams:0195...:live"
}
```

### Subscription accepted

```json
{
  "protocol_version": 1,
  "type": "subscription.accepted",
  "request_id": "client-77",
  "subscription_id": "0195...",
  "channel": "teams:0195...:live"
}
```

### Location delta

```json
{
  "protocol_version": 1,
  "type": "location.updated",
  "message_id": "0195...",
  "subscription_id": "0195...",
  "sequence": 883,
  "occurred_at": "2026-10-10T10:11:13.101Z",
  "payload": {
    "subject_id": "0195...",
    "recorded_at": "2026-10-10T10:11:12Z",
    "position": {
      "latitude": 44.8123,
      "longitude": 20.4611,
      "precision": "exact"
    },
    "speed_mps": 5.8,
    "heading_deg": 182.0,
    "movement_status": "moving",
    "connection_status": "online",
    "version": 883
  }
}
```

### Alert delta

```json
{
  "protocol_version": 1,
  "type": "alert.opened",
  "message_id": "0195...",
  "payload": {
    "alert_id": "0195...",
    "subject_id": "0195...",
    "severity": "critical",
    "rule_type": "sos",
    "opened_at": "2026-10-10T10:11:13Z"
  }
}
```

### Gap and resynchronization

When the server cannot replay from the requested cursor:

```json
{
  "protocol_version": 1,
  "type": "resync.required",
  "reason": "cursor_expired",
  "snapshot_endpoint": "/api/v1/live/snapshot"
}
```

The client pauses delta application, obtains a new snapshot, and resubscribes.

### Close behavior

Document close codes for:

```text
normal shutdown
authentication expired
permission revoked
protocol violation
message too large
rate limited
slow consumer
server restart
```

Clients reconnect only for retryable codes and use exponential backoff with jitter.
