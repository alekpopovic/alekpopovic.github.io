## Chapter 9 - The Tracking Registry

The registry is the control-plane source of truth for subjects, devices, assignments, sessions, teams, and relationships. It changes more slowly than location history but determines whether each incoming observation is legitimate.

### Subject lifecycle

A subject lifecycle can include:

```text
pending -> active -> suspended -> archived
```

Archiving prevents new tracking while preserving history and audit records. A person subject may also have employment or participation dates that are distinct from the platform lifecycle.

Create commands validate kind-specific profiles. A vehicle profile may require a registration identifier only in products that need it; a package profile may require a customer reference; a person profile must minimize personal attributes.

Keep display names separate from immutable external references. Names change. External references may map to an ERP, HR, race, or warehouse system and should be unique within a documented namespace.

### Device registration

Mobile registration begins after human authentication. The mobile app creates a device record and exchanges an enrollment grant for a device credential. The credential belongs to the installation, not to the human session.

A dedicated tracker may be provisioned through an administrator or imported in bulk. Store vendor identifiers separately from internal IDs. Normalize case and separators according to the protocol's rules.

Device status should distinguish:

- pending enrollment;
- active;
- suspended;
- compromised;
- retired.

A device can be suspended without deleting historical provenance.

### Credential rotation

Device credentials are hashed at rest and versioned. The server can issue a new credential while briefly accepting the old one during a controlled overlap. A compromised credential is revoked immediately.

For devices that support asymmetric keys, the registry can store public keys and challenge signatures. Simpler trackers may require pre-shared secrets. The protocol adapter translates their authentication into the canonical device identity.

### Assignment rules

Assignments are temporal. The platform checks the point's `recorded_at`, not only request receipt time, because an offline device can upload older observations.

The acceptance rule can be expressed as:

```sql
SELECT id
FROM device_assignments
WHERE organization_id = $1
  AND device_id = $2
  AND subject_id = $3
  AND valid_from <= $4
  AND (valid_until IS NULL OR valid_until > $4)
LIMIT 1;
```

For sessions that explicitly bind the device and subject, the session can provide an additional authorization path. The exact precedence must be documented.

Changing an assignment does not rewrite points. If an administrator made a mistake, use a controlled correction workflow that records who changed the association, why, which interval was affected, and whether derived facts were recomputed.

### Teams and groups

Teams support operational views and authorization. A subject may belong to multiple teams, and membership may be time-bounded. Examples include a delivery zone, race wave, construction crew, or maintenance group.

Do not use teams as a substitute for organizations. Organizations are tenant and billing boundaries. Teams are internal grouping and policy units.

A team model often includes:

```text
teams
team_memberships          -- human users
team_subject_memberships  -- tracked subjects
team_device_memberships   -- optional operational grouping
```

The dashboard can subscribe to a team channel and receive only subjects that currently belong to that team.

### Session creation

A session starts only when:

- the subject and device are active;
- the device is assigned or explicitly authorized;
- the activity type is permitted;
- a person-tracking basis is present where required;
- no conflicting exclusive session exists;
- the caller or device has permission to start it.

The server returns a session ID and policy snapshot:

```json
{
  "session_id": "0195...",
  "status": "active",
  "started_at": "2026-10-10T07:00:00Z",
  "location_policy": {
    "moving_interval_seconds": 5,
    "stationary_interval_seconds": 30,
    "minimum_accuracy_m": 50,
    "batch_size": 50,
    "maximum_offline_age_hours": 24
  }
}
```

The mobile app treats the policy as guidance constrained by OS behavior and safety. The server remains authoritative about what it accepts.

### Clock and interval issues

Devices have imperfect clocks. A session boundary based on server time can conflict with points recorded by a clock that is several minutes wrong. The ingestion pipeline should calculate clock skew and classify points near boundaries rather than silently accepting arbitrary times.

Possible policy:

- accept small skew and record it;
- quarantine points with large future timestamps;
- accept delayed historical points within a retention window;
- reject points outside any valid assignment or session after a documented tolerance;
- never move a point's `recorded_at` silently to server time.

### Registry events

Important changes create outbox events:

```text
subject.created
subject.suspended
device.enrolled
device.credential_rotated
device.compromised
assignment.started
assignment.ended
tracking_session.started
tracking_session.completed
team.membership_changed
```

These events support audit, realtime UI updates, notifications, and downstream recomputation without making the HTTP handler responsible for every side effect.

### Chapter checklist

The registry should provide:

- explicit subject and device lifecycles;
- separate mobile enrollment and device credentials;
- temporal assignment validation against `recorded_at`;
- time-bounded teams and relationships;
- policy-aware tracking session creation;
- documented clock-skew behavior;
- durable events for important registry changes.
