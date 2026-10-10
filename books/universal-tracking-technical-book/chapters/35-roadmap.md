## Chapter 35 - Delivery Roadmap and Production Readiness

A tracking platform is best delivered in vertical slices that preserve architectural invariants. Building every database table first and integrating clients at the end delays the discovery of mobile, realtime, and operational failures.

### Phase 1 - Foundation

Deliver:

- repository and ADRs;
- Go runtime roles;
- PostgreSQL/PostGIS bootstrap;
- migrations and fixtures;
- typed configuration;
- logging, health, and metrics;
- CI quality gates;
- Angular workspace;
- local Compose environment.

Exit criteria: a fresh environment boots deterministically, migrations run, tests use real PostGIS, and no forbidden infrastructure is required.

### Phase 2 - Identity and registry

Deliver:

- users, authentication, sessions, and MFA;
- organizations, memberships, roles, and policies;
- audit subsystem;
- subjects, profiles, devices, credentials;
- assignments, teams, relationships, and sessions;
- tenant isolation and RLS tests.

Exit criteria: cross-tenant penetration tests pass, identity classes are separate, and session/assignment invariants are enforced.

### Phase 3 - End-to-end location slice

Deliver one complete path:

1. mobile or simulator records points;
2. SQLite persists them;
3. batch API accepts and acknowledges them;
4. PostgreSQL stores partitioned history;
5. latest state updates;
6. outbox event wakes realtime;
7. Angular map receives snapshot and delta;
8. reconnect recovers correctly.

Exit criteria: the slice survives duplicate requests, process kill after commit, network loss, and rolling API restart.

### Phase 4 - Derivation and alerts

Deliver:

- movement and presence;
- trips and stops;
- route playback;
- geofences;
- alert incidents and notification jobs;
- late-data reconciliation;
- algorithm versioning.

Exit criteria: canonical scenarios produce deterministic derived outcomes and reprocessing does not duplicate alerts.

### Phase 5 - Mobile production behavior

Deliver:

- Android foreground service;
- iOS background location;
- native SQLite migrations;
- enrollment and secure credentials;
- session UX and diagnostics;
- field study and battery report.

Exit criteria: supported devices pass multi-hour and multi-day tests with documented limitations.

### Phase 6 - Business and external surfaces

Deliver:

- public share links and privacy precision;
- tasks and delivery workflow;
- file proofs;
- API clients and webhooks;
- reports and exports;
- first dedicated GPS protocols.

Exit criteria: public and machine identities are scoped, webhook delivery is SSRF-resistant, and protocol parsers pass fuzz and conformance tests.

### Phase 7 - Production operations

Deliver:

- hardened images and Compose topology;
- Nginx routing and TLS;
- backups, WAL archive, and restore drills;
- deployment and rollback scripts;
- dashboards and alerts;
- incident runbooks;
- load, fault, and security regression suites.

Exit criteria: an independent operator can deploy, diagnose, restore, and roll back using documentation and sealed secrets.

### Go-live review

A production readiness review should require evidence for:

**Correctness**

- migrations from empty and previous supported version;
- idempotent ingestion and jobs;
- deterministic state transitions;
- tenant and policy tests;
- late-data behavior.

**Reliability**

- load and endurance targets;
- reconnect-storm results;
- fault-injection outcomes;
- backup and PITR drill;
- rollback rehearsal.

**Security and privacy**

- threat-model review;
- secret and key rotation;
- RLS verification;
- public-link privacy tests;
- person-tracking visibility;
- retention and deletion test;
- SBOM and vulnerability triage.

**Operations**

- SLO dashboards;
- actionable alerts;
- capacity headroom;
- on-call ownership;
- incident and data-integrity runbooks;
- known limitations.

### Release package

The release package includes:

```text
container image digests
source revision and provenance
SBOM
migration set and checksum
OpenAPI and WebSocket schemas
mobile build identifiers
configuration reference
backup and restore procedures
load-test report
security review
known limitations
rollback instructions
operator handover
```

### The final engineering rule

The strongest design choice in this architecture is not Go, PostgreSQL, or Angular. It is the insistence that every fast path has a durable truth, every background operation has a retry and recovery story, every person-tracking feature has visible policy, and every production claim has evidence.

A real-time map is the visible surface. The product is the system of facts, permissions, recovery mechanisms, and operational decisions underneath it.
