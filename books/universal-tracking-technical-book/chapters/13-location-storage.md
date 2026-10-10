## Chapter 13 - Partitioned Location Storage and Query Design

Location history is append-heavy, time-oriented, tenant-scoped, and frequently queried by subject and interval. A single unpartitioned table can work for a prototype and become painful precisely when retention and maintenance matter most.

### Canonical table

A simplified parent table is:

```sql
CREATE TABLE location_points (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    device_id uuid NOT NULL,
    session_id uuid,
    sequence_epoch integer NOT NULL,
    sequence_number bigint NOT NULL,
    recorded_at timestamptz NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    position geography(Point, 4326) NOT NULL,
    altitude_m double precision,
    accuracy_m double precision,
    speed_mps double precision,
    heading_deg double precision,
    battery_percent smallint,
    activity_type text,
    quality_flags text[] NOT NULL DEFAULT '{}',
    source text NOT NULL,
    attributes jsonb NOT NULL DEFAULT '{}',
    PRIMARY KEY (recorded_at, id),
    CHECK (battery_percent IS NULL OR
           battery_percent BETWEEN 0 AND 100)
) PARTITION BY RANGE (recorded_at);
```

A parent primary key includes the partition key. Additional identity enforcement may use a separate table as described in Chapter 12.

### Partition interval

Choose daily or monthly partitions based on point volume and operational behavior. The target is not an arbitrary row count; it is manageable index size, vacuum work, backup granularity, and retention drops.

Monthly partitions are simple for moderate workloads. Daily partitions reduce per-partition size at high volume. Hourly partitions usually create too many objects unless traffic is extreme and retention is short.

Create partitions ahead of time:

```sql
CREATE TABLE location_points_2026_10
PARTITION OF location_points
FOR VALUES FROM ('2026-10-01T00:00:00Z')
         TO   ('2026-11-01T00:00:00Z');
```

The scheduler maintains future partitions and alerts if a default partition receives rows. A missing future partition must not become a surprise outage.

### Partition indexes

Create consistent indexes on every partition through migration or automation:

```sql
CREATE INDEX ON location_points_2026_10
    (organization_id, subject_id, recorded_at DESC);

CREATE INDEX ON location_points_2026_10
    USING gist (position);

CREATE INDEX ON location_points_2026_10
    USING brin (recorded_at);
```

A GiST index on every large partition has a write and storage cost. Keep it only if spatial history queries need it. Geofence processing can often use current points against a separate indexed geofence table rather than searching all historical points spatially.

### Batch insertion

Use `pgx.CopyFrom` or bounded multi-row inserts inside the ingestion transaction. Copying directly into the partitioned parent allows PostgreSQL to route rows.

```go
rows := make([][]any, 0, len(points))
for _, p := range points {
    rows = append(rows, []any{
        p.ID,
        p.OrganizationID,
        p.SubjectID,
        p.DeviceID,
        p.SessionID,
        p.SequenceEpoch,
        p.Sequence,
        p.RecordedAt,
        p.ReceivedAt,
        p.Longitude,
        p.Latitude,
        p.AccuracyM,
        p.SpeedMPS,
    })
}
```

When using `COPY`, spatial values may be created in a staging table or through typed values. Benchmark the simplest correct method before adding a complex ingest pipeline.

### History query

A common query is:

```sql
SELECT
    id,
    recorded_at,
    ST_Y(position::geometry) AS latitude,
    ST_X(position::geometry) AS longitude,
    accuracy_m,
    speed_mps,
    heading_deg,
    quality_flags
FROM location_points
WHERE organization_id = $1
  AND subject_id = $2
  AND recorded_at >= $3
  AND recorded_at < $4
ORDER BY recorded_at, id
LIMIT $5;
```

Always require a bounded time range. Protect endpoints from year-long high-frequency downloads unless they use an export job.

Cursor pagination should include `(recorded_at, id)` so equal timestamps remain deterministic.

### Simplified routes

A map rarely needs every point at every zoom level. Build route representations at different tolerances or use server-side simplification on bounded intervals. Preserve source points separately.

Possible layers:

- raw points for forensic detail;
- one-second or distance-filtered points for close playback;
- simplified polylines for day overview;
- trip summary lines for long-term history.

Do not simplify geographic coordinates with an arbitrary planar tolerance without understanding projection and distance. For display, project appropriately or use algorithms designed for geodesic data.

### Retention by partition

Partitioning makes retention predictable. Instead of deleting millions of rows, detach and drop an expired partition after checking legal holds and policy exceptions.

A safe lifecycle is:

1. determine that every row in a partition is eligible;
2. verify no legal hold or longer tenant policy applies;
3. export or aggregate required summaries;
4. detach the partition;
5. wait through a safety interval;
6. drop or archive it;
7. record the action in audit.

Mixed retention within one partition complicates this. Large tenants or special policies may require separate partitions, tables, or a move-to-retention-bucket process.

### Vacuum and statistics

Append-only partitions still need autovacuum for visibility maps, dead rows from corrections, and index maintenance. Tune per table based on churn. Analyze new partitions after significant load so the planner has useful statistics.

Monitor:

- partition size and growth;
- dead tuples;
- autovacuum lag and duration;
- index size and unused indexes;
- query buffer reads;
- checkpoint and WAL volume;
- insert latency during maintenance.

### Chapter checklist

Production history storage has:

- range partitions created ahead of time;
- indexes matched to measured queries;
- batch insertion;
- bounded time-range APIs;
- deterministic cursors;
- derived simplified routes;
- policy-aware partition lifecycle;
- vacuum, statistics, and growth monitoring.
