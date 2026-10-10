# Appendices {.part}

## Appendix A - Canonical Schema Blueprint

This appendix is a blueprint, not a drop-in final migration. Production migrations should be split into reviewable files, include comments and privileges, and match the exact domain rules of the implementation.

### Organizations and users

```sql
CREATE TABLE organizations (
    id uuid PRIMARY KEY,
    name text NOT NULL,
    slug text NOT NULL UNIQUE,
    status text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    version bigint NOT NULL DEFAULT 1
);

CREATE TABLE users (
    id uuid PRIMARY KEY,
    email_normalized text NOT NULL UNIQUE,
    email_display text NOT NULL,
    password_hash text NOT NULL,
    status text NOT NULL,
    email_verified_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    version bigint NOT NULL DEFAULT 1
);

CREATE TABLE organization_memberships (
    organization_id uuid NOT NULL REFERENCES organizations(id),
    user_id uuid NOT NULL REFERENCES users(id),
    status text NOT NULL,
    joined_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, user_id)
);
```

### Roles and permissions

```sql
CREATE TABLE roles (
    id uuid PRIMARY KEY,
    organization_id uuid,
    name text NOT NULL,
    built_in boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE NULLS NOT DISTINCT (organization_id, name)
);

CREATE TABLE role_permissions (
    role_id uuid NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission text NOT NULL,
    PRIMARY KEY (role_id, permission)
);

CREATE TABLE membership_roles (
    organization_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role_id uuid NOT NULL REFERENCES roles(id),
    PRIMARY KEY (organization_id, user_id, role_id),
    FOREIGN KEY (organization_id, user_id)
        REFERENCES organization_memberships(organization_id, user_id)
        ON DELETE CASCADE
);
```

### Subjects, devices, and assignments

```sql
CREATE TABLE tracking_subjects (
    id uuid NOT NULL,
    organization_id uuid NOT NULL REFERENCES organizations(id),
    kind text NOT NULL,
    name text NOT NULL,
    external_reference text,
    status text NOT NULL,
    privacy_classification text NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    version bigint NOT NULL DEFAULT 1,
    PRIMARY KEY (organization_id, id),
    UNIQUE (organization_id, external_reference)
);

CREATE TABLE tracking_devices (
    id uuid NOT NULL,
    organization_id uuid NOT NULL REFERENCES organizations(id),
    kind text NOT NULL,
    display_name text NOT NULL,
    external_identifier text,
    status text NOT NULL,
    capabilities jsonb NOT NULL DEFAULT '{}',
    last_seen_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    version bigint NOT NULL DEFAULT 1,
    PRIMARY KEY (organization_id, id),
    UNIQUE (organization_id, external_identifier)
);

CREATE TABLE device_assignments (
    id uuid PRIMARY KEY,
    organization_id uuid NOT NULL,
    device_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    valid_from timestamptz NOT NULL,
    valid_until timestamptz,
    reason text,
    created_by uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (valid_until IS NULL OR valid_until > valid_from),
    FOREIGN KEY (organization_id, device_id)
        REFERENCES tracking_devices(organization_id, id),
    FOREIGN KEY (organization_id, subject_id)
        REFERENCES tracking_subjects(organization_id, id)
);
```

Where exclusive assignments are required, add a GiST exclusion constraint using a time range and the `btree_gist` extension.

### Sessions

```sql
CREATE TABLE tracking_sessions (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    device_id uuid NOT NULL,
    activity_type text NOT NULL,
    status text NOT NULL,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    privacy_context jsonb NOT NULL DEFAULT '{}',
    shift_id uuid,
    task_id uuid,
    consent_record_id uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    version bigint NOT NULL DEFAULT 1,
    PRIMARY KEY (organization_id, id),
    CHECK (ended_at IS NULL OR ended_at >= started_at),
    FOREIGN KEY (organization_id, subject_id)
        REFERENCES tracking_subjects(organization_id, id),
    FOREIGN KEY (organization_id, device_id)
        REFERENCES tracking_devices(organization_id, id)
);
```

### Location batches and history

```sql
CREATE TABLE location_batches (
    organization_id uuid NOT NULL,
    device_id uuid NOT NULL,
    batch_id uuid NOT NULL,
    payload_hash bytea NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    result jsonb,
    PRIMARY KEY (organization_id, device_id, batch_id)
);

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
    CHECK (accuracy_m IS NULL OR accuracy_m >= 0),
    CHECK (heading_deg IS NULL OR
           (heading_deg >= 0 AND heading_deg < 360)),
    CHECK (battery_percent IS NULL OR
           battery_percent BETWEEN 0 AND 100)
) PARTITION BY RANGE (recorded_at);
```

### Current state

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

### Outbox and jobs

```sql
CREATE TABLE outbox_events (
    id uuid PRIMARY KEY,
    organization_id uuid,
    aggregate_type text NOT NULL,
    aggregate_id uuid NOT NULL,
    event_type text NOT NULL,
    schema_version integer NOT NULL,
    payload jsonb NOT NULL,
    occurred_at timestamptz NOT NULL,
    available_at timestamptz NOT NULL DEFAULT now(),
    claimed_at timestamptz,
    claimed_by text,
    processed_at timestamptz,
    attempts integer NOT NULL DEFAULT 0,
    last_error text
);

CREATE INDEX outbox_pending_idx
ON outbox_events (available_at, occurred_at)
WHERE processed_at IS NULL;

CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    organization_id uuid,
    queue text NOT NULL,
    job_type text NOT NULL,
    payload jsonb NOT NULL,
    idempotency_key text,
    status text NOT NULL DEFAULT 'pending',
    priority integer NOT NULL DEFAULT 0,
    run_at timestamptz NOT NULL DEFAULT now(),
    attempts integer NOT NULL DEFAULT 0,
    max_attempts integer NOT NULL DEFAULT 10,
    locked_at timestamptz,
    locked_by text,
    last_error_code text,
    last_error_summary text,
    completed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

### Geofences

```sql
CREATE TABLE geofences (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    name text NOT NULL,
    shape geometry(Geometry, 4326) NOT NULL,
    shape_type text NOT NULL,
    enabled boolean NOT NULL DEFAULT true,
    buffer_m double precision NOT NULL DEFAULT 0,
    active_from timestamptz,
    active_until timestamptz,
    policy jsonb NOT NULL DEFAULT '{}',
    version bigint NOT NULL DEFAULT 1,
    PRIMARY KEY (organization_id, id),
    CHECK (ST_IsValid(shape))
);

CREATE INDEX geofences_shape_gist
ON geofences USING gist (shape);
```

### RLS template

```sql
ALTER TABLE tracking_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracking_subjects FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_tracking_subjects
ON tracking_subjects
USING (
    organization_id =
    nullif(current_setting('app.organization_id', true), '')::uuid
)
WITH CHECK (
    organization_id =
    nullif(current_setting('app.organization_id', true), '')::uuid
);
```

Apply equivalent policies to tenant-owned tables and test them using the actual runtime role.
