## Chapter 12 - Offline Delivery, Idempotency, Sequencing, and Data Quality

Mobile networks duplicate requests, reorder uploads, delay points, and fail after the server commits but before the client receives a response. The ingestion model must treat these as ordinary conditions.

### Three identifiers with different jobs

Use distinct identifiers for:

- **batch ID**: idempotency of a request payload;
- **sequence number**: ordered device observations within an epoch or stream;
- **point ID**: stable identity of an individual locally persisted point.

A batch may be retried with the same batch ID. A point may later appear in a different batch after a partial response. Sequence numbers detect gaps and order. Point IDs protect against cases where a device restarts its sequence.

A durable batch table can store:

```text
location_batches
  organization_id
  device_id
  batch_id
  payload_hash
  received_at
  status
  result JSONB
```

If the same batch ID arrives with a different payload hash, reject it as an idempotency conflict.

### Sequence epochs

Some devices reset counters after reinstall, firmware reset, or rollover. Represent an epoch or credential generation:

```text
(device_id, sequence_epoch, sequence_number)
```

The server creates a new epoch through enrollment or an explicit reset handshake. Do not guess that a lower sequence always means a reset; it may be a replay attack.

### Out-of-order points

A late point is not necessarily invalid. Store by `recorded_at` and keep `received_at`. Derived algorithms can reconcile a bounded lateness window.

Policies should distinguish:

- in-order current point;
- duplicate;
- late but accepted point;
- stale point outside normal analytics window;
- future point within clock-skew tolerance;
- impossible future point;
- point outside assignment or session;
- replay from an old credential epoch.

The latest-location projection updates only when the incoming observation is newer according to a deterministic comparison. A delayed upload must not move the live marker backward.

### Quality classification

Do not reduce quality to valid or invalid. Suggested statuses include:

```text
valid
low_accuracy
stale
future_timestamp
impossible_speed
teleport_jump
mocked_location
out_of_order
missing_sensor_context
quarantined
```

A point can carry multiple flags. The raw accepted values remain available for controlled analysis. Product views decide which qualities to show or exclude.

### Plausibility checks

A speed plausibility calculation uses geodesic distance and elapsed recording time:

```text
implied_speed = distance(previous_point, current_point) / delta_time
```

Do not apply one threshold to all subjects. A pedestrian, racing bicycle, aircraft, and cargo ship have different expected ranges. Accuracy also matters: two noisy low-accuracy points can imply a large false jump.

A robust classifier considers:

- subject and activity profile;
- reported speed versus implied speed;
- reported accuracy;
- elapsed time;
- known indoor or tunnel context;
- device source and capability;
- clock skew;
- whether the location is OS-marked as mocked.

A suspicious point should usually be stored with a flag, not discarded silently. Safety applications may prefer availability over aggressive filtering.

### Clock normalization

Keep the device-provided `recorded_at`. Also store `received_at` and derived skew:

```text
clock_skew_ms = received_at - recorded_at
```

For protocols that provide GPS time and device time, record their provenance. A protocol adapter can normalize the representation but should not hide which clock was used.

Large skew can affect session authorization. Use an explicit tolerance and quarantine path. Administrators should be able to diagnose a misconfigured tracker.

### Idempotent database insertion

A unique constraint can protect point identity:

```sql
CREATE UNIQUE INDEX location_point_identity_uq
ON location_points (
    recorded_at,
    organization_id,
    device_id,
    sequence_epoch,
    sequence_number
);
```

Because a partitioned unique index must include the partition key, `recorded_at` appears in the identity. A separate compact deduplication table may be preferable when sequence identity must remain unique across time partitions. The trade-off is an additional write and lifecycle process.

For mobile points with a stable UUID, store it and enforce uniqueness in a dedicated device-point registry or in partitions where the constraint is valid. Benchmark both designs.

### Partial acceptance and retries

Suppose a batch contains 100 points and three fail authorization. The server can accept 97 and return exact rejection codes. The client removes accepted points and retains rejected diagnostics. If the response is lost, a retry returns the stored result or re-evaluates idempotently.

Never let a client infer success from a network disconnect. It retains data until explicit acknowledgement.

### Quarantine

Some data should be preserved without entering normal history:

- malformed but parseable vendor packets;
- points with impossible timestamps;
- unknown external device identifiers;
- valid protocol frames from a revoked device;
- payloads that exceed metadata rules.

Quarantine storage has strict retention, restricted access, redaction, and size limits. It exists for diagnostics, not as an unlimited raw-packet archive.

### Chapter checklist

Resilient ingestion requires:

- separate batch, point, and sequence identities;
- explicit sequence epochs;
- safe acceptance of bounded out-of-order data;
- quality flags rather than silent rewriting;
- activity-aware plausibility checks;
- preserved device and server timestamps;
- idempotent partial acceptance;
- bounded, access-controlled quarantine.
