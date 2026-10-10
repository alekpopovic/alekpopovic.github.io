## Chapter 5 - PostgreSQL and PostGIS as the Platform Core

PostgreSQL is the only mandatory infrastructure service in the reference architecture. This makes database design an application architecture concern, not an implementation detail. The database stores business state, raw observations, current projections, durable events, background jobs, audit history, and spatial shapes. Each workload needs deliberate tables, indexes, connection budgets, and lifecycle rules.

### Bootstrap extensions and roles

A minimal bootstrap enables required extensions and separates privileges:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE ROLE tracking_owner NOLOGIN;
CREATE ROLE tracking_app LOGIN;
CREATE ROLE tracking_migrator LOGIN;
CREATE ROLE tracking_readonly LOGIN;
```

The migration role owns schema changes. The application role receives only runtime privileges. A read-only role can support controlled reporting. Production secrets are injected rather than embedded in SQL files.

Use a schema convention consistently. A single application schema is simpler than many schemas for a modular monolith, but either can work when object ownership and search paths are explicit.

### Types and units

Recommended defaults include:

- `uuid` for identifiers;
- `timestamptz` for moments in time;
- `date` only for calendar concepts;
- `bigint` for device sequence numbers;
- `double precision` for sensor measurements;
- constrained `text` or lookup tables for evolving categories;
- `jsonb` for bounded extension data, not core fields;
- `geography(Point, 4326)` for Earth-distance calculations;
- `geometry` for shapes and map operations where a chosen projection is appropriate.

Store canonical units. Convert at presentation boundaries. A database column named `speed` is ambiguous; `speed_mps` is not.

### Spatial types

PostGIS distinguishes `geometry` and `geography`. Geography treats coordinates on an ellipsoidal Earth and is convenient for meter-based distance between latitude/longitude points. Geometry operates in a planar coordinate reference system and supports a broader set of operations with projection-dependent units.

For raw global location points:

```sql
position geography(Point, 4326) NOT NULL
```

Construct a point with longitude first:

```sql
ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
```

For a geofence polygon, storing a validated geometry can make containment queries efficient. Large or cross-dateline shapes require more care. Document the accepted geometry rules and reject invalid shapes at creation time.

### Connection pools

Every process role has its own pool. The sum of maximum pool sizes must remain below the database connection budget after reserving connections for migrations, monitoring, maintenance, replication, and emergencies.

Example budget:

```text
PostgreSQL max_connections: 200
reserved operations/admin:   20
api replicas: 4 * 20 =       80
workers: 4 * 15 =            60
scheduler: 2 * 3 =            6
gateway: 2 * 8 =             16
headroom:                     18
```

More connections do not automatically increase throughput. They can increase lock contention, memory use, and context switching. Measure queueing time and database CPU before changing pool sizes.

Set timeouts deliberately:

```sql
SET statement_timeout = '5s';
SET lock_timeout = '1s';
SET idle_in_transaction_session_timeout = '10s';
```

Values differ by role and query. Long report jobs should not inherit the same timeout as a live-map snapshot.

### Transactions

Application services own transaction boundaries. Repositories accept a transaction-capable interface rather than starting hidden transactions.

```go
type DBTX interface {
    Exec(context.Context, string, ...any) (pgconn.CommandTag, error)
    Query(context.Context, string, ...any) (pgx.Rows, error)
    QueryRow(context.Context, string, ...any) pgx.Row
}
```

A use case can then atomically update domain state, append an audit record, and write an outbox event.

Retry only transactions that are safe to repeat and only for recognized transient failures. An idempotency key is not a substitute for understanding transaction side effects.

### Constraints before application checks

The database should reject impossible data even if application validation is bypassed. Examples include:

```sql
CHECK (battery_percent BETWEEN 0 AND 100),
CHECK (accuracy_m IS NULL OR accuracy_m >= 0),
CHECK (heading_deg IS NULL OR
       (heading_deg >= 0 AND heading_deg < 360)),
CHECK (valid_until IS NULL OR valid_until > valid_from)
```

Use unique constraints for natural idempotency keys and exclusion constraints for interval overlap. Application code converts constraint violations into stable domain errors.

### Indexes from queries

Index every foreign key that participates in deletes or common joins, but do not index every column. The location workload usually needs:

- B-tree on `(organization_id, subject_id, recorded_at DESC)`;
- GiST on `position` for spatial predicates;
- BRIN on `recorded_at` for large, naturally ordered partitions;
- targeted partial indexes for active devices, pending jobs, and unprocessed events.

Validate with `EXPLAIN (ANALYZE, BUFFERS)` using realistic distributions. A query that is fast with one organization and one thousand rows may fail with skewed tenants and billions of points.

### Migrations

Migrations are immutable after release. A migration tool applies numbered SQL files and records their state. Every deployment validates that the expected migration set is present before serving traffic.

A safe column rename is not an immediate `ALTER COLUMN RENAME` when old and new processes overlap. Instead:

1. add the new column;
2. write both fields;
3. backfill in bounded batches;
4. read the new field with fallback;
5. stop writing the old field;
6. verify no old processes remain;
7. remove the old field in a later release.

This pattern is slower than a single migration and far safer.

### Chapter checklist

The database foundation is ready when:

- roles and privileges are separated;
- types encode units and time semantics;
- geography and geometry choices are documented;
- pool budgets are calculated across all roles;
- transaction ownership is explicit;
- constraints enforce important invariants;
- indexes are justified by measured queries;
- migrations support rolling compatibility.
