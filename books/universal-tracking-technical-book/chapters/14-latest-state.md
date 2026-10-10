## Chapter 14 - Latest State, Presence, and Movement

The live dashboard should not search billions of history rows to find one marker per subject. Maintain a compact `latest_locations` projection and update it conditionally.

### Latest-location table

```sql
CREATE TABLE latest_locations (
    organization_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    device_id uuid NOT NULL,
    session_id uuid,
    location_id uuid NOT NULL,
    recorded_at timestamptz NOT NULL,
    received_at timestamptz NOT NULL,
    position geography(Point, 4326) NOT NULL,
    accuracy_m double precision,
    speed_mps double precision,
    heading_deg double precision,
    battery_percent smallint,
    activity_type text,
    movement_status text NOT NULL,
    connection_status text NOT NULL,
    quality_flags text[] NOT NULL DEFAULT '{}',
    version bigint NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, subject_id)
);
```

Update only when the new observation wins a deterministic comparison:

```sql
INSERT INTO latest_locations (...)
VALUES (...)
ON CONFLICT (organization_id, subject_id)
DO UPDATE SET
    device_id = EXCLUDED.device_id,
    location_id = EXCLUDED.location_id,
    recorded_at = EXCLUDED.recorded_at,
    position = EXCLUDED.position,
    version = latest_locations.version + 1,
    updated_at = now()
WHERE (EXCLUDED.recorded_at, EXCLUDED.location_id)
    > (latest_locations.recorded_at,
       latest_locations.location_id);
```

The tie-breaker ensures deterministic behavior when timestamps are equal.

### Current truth versus last observation

"Latest" does not mean "currently online." Store or calculate separate dimensions:

- last observed location;
- age of that observation;
- last server contact;
- active session status;
- connection status;
- movement status;
- data quality.

A marker can be last seen moving but currently offline. The UI should not display it as live movement.

### Presence

For phones using batched HTTP, presence is inferred from recent successful contact. For connected TCP trackers or WebSockets, the gateway may know connection state, but network connection is not proof of current GPS quality.

Define thresholds by device and use case:

```text
online: last contact <= expected interval * tolerance
stale:  older than online threshold but within display window
offline: older than offline threshold
unknown: never contacted or policy cannot evaluate
```

The scheduler or worker transitions devices to offline and emits an event. The calculation must be idempotent because multiple workers may evaluate the same row.

### Movement state

Reported speed alone is noisy. A movement detector can use hysteresis:

- moving begins after speed or displacement exceeds a start threshold for a minimum duration;
- stopped begins after speed remains below a lower threshold for a dwell period;
- low-accuracy points do not cause rapid toggling;
- activity type influences thresholds.

Store the algorithm version and transition time. A simple first implementation can be deterministic and explainable.

```go
type MovementConfig struct {
    StartSpeedMPS float64
    StopSpeedMPS  float64
    StartDuration time.Duration
    StopDuration  time.Duration
    MaxAccuracyM  float64
}
```

### Distance accumulation

Do not blindly sum every consecutive point. GPS jitter while stationary can create significant false distance. Consider:

- minimum accuracy;
- minimum displacement relative to accuracy radius;
- maximum plausible speed;
- activity-specific sampling;
- gap boundaries;
- map matching only when justified.

Keep raw points and calculate distance as a versioned derived metric. The latest state may contain a session distance estimate for immediate UI, later reconciled by a worker.

### Snapshot query

The dashboard initial snapshot can retrieve authorized subjects and latest state in one bounded query. It should return freshness fields and policy-reduced coordinates when necessary.

```json
{
  "subject_id": "0195...",
  "recorded_at": "2026-10-10T10:11:12Z",
  "received_at": "2026-10-10T10:11:13Z",
  "freshness_seconds": 3,
  "movement_status": "moving",
  "connection_status": "online",
  "position": {
    "latitude": 44.8123,
    "longitude": 20.4611
  },
  "quality": ["valid"],
  "version": 883
}
```

The `version` supports snapshot-plus-delta recovery.

### Rebuilding projections

`latest_locations` is a projection, not the only source of truth. Provide a command that rebuilds it from accepted history and registry state. Rebuilds can target one subject, organization, partition interval, or all data.

A rebuild should write to a shadow table or use careful upserts so the live system remains available. Compare counts and sampled rows before switching.

### Chapter checklist

A live-state projection should:

- be separate from raw history;
- update only for deterministically newer observations;
- separate freshness, connection, movement, and quality;
- use hysteresis for movement;
- avoid summing GPS jitter as distance;
- return a version for realtime recovery;
- be rebuildable from durable facts.
