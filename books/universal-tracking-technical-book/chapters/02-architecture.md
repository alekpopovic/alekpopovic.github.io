## Chapter 2 - A Modular Monolith with Multiple Runtime Roles

The system benefits from one domain model and several independently scalable process roles. This is not a contradiction. A modular monolith describes code ownership and dependency rules; runtime roles describe how the same codebase is executed.

![The reference runtime uses multiple Go roles over one PostgreSQL/PostGIS service.](../assets/diagrams/runtime-topology.png){width=94%}

### Why not begin with microservices

Location platforms contain natural domains: identity, registry, ingestion, realtime, geofences, tasks, integrations, and reporting. Turning each domain into a network service on day one adds contract versioning, deployment coordination, distributed tracing, retry storms, and data ownership questions before the team has measured where isolation is needed.

The highest-volume path is clear - location ingestion and projection. Even so, it can begin as a distinct package and process role inside one repository. The boundary is enforced by interfaces and schemas rather than by a network hop. If the path later needs a separate deployment or language, its contract already exists.

The modular-monolith approach provides:

- one repository and one set of domain terms;
- atomic database changes where they are genuinely needed;
- simple local development;
- fewer operational components;
- consistent authorization and audit behavior;
- a controlled path to later extraction.

It does not mean one giant package, one global dependency container, or one process that performs every task.

### Runtime roles

The reference binary exposes subcommands or builds equivalent binaries:

```text
tracking-platform api
tracking-platform worker
tracking-platform scheduler
tracking-platform gps-gateway
tracking-platform migrate
tracking-platform simulator
```

The roles share configuration parsing, database access, domain packages, telemetry, and contracts, but they have separate startup graphs and resource budgets.

**`api`** serves the REST API, WebSocket endpoint, authentication, organization management, history queries, current-state snapshots, and public pages. It should be horizontally replaceable and must shut down gracefully.

**`worker`** leases durable jobs, processes outbox events, calculates derived facts, delivers webhooks, creates exports, and performs retention work. Multiple workers cooperate through database leases.

**`scheduler`** creates recurring jobs and manages future partitions. It uses PostgreSQL advisory locks so only one replica schedules a given task at a time.

**`gps-gateway`** owns long-lived TCP/UDP/HTTP device connections, bounded frame parsing, protocol acknowledgements, and normalization to the internal ingestion contract.

**`migrate`** performs explicit, versioned database migrations. Application roles never auto-migrate at startup.

**`simulator`** generates deterministic routes, device failures, reconnect bursts, and protocol traffic for tests and capacity studies.

### Package boundaries

A practical repository separates domain modules from adapters:

```text
cmd/tracking-platform/
internal/
  app/
  auth/
  authorization/
  organizations/
  registry/
  locations/
  realtime/
  outbox/
  jobs/
  scheduler/
  geofences/
  alerts/
  trips/
  tasks/
  integrations/
  privacy/
  audit/
  protocols/
pkg/
api/
migrations/
web/
mobile/
native/
deployments/
tests/
```

Packages under `internal` are not a miscellaneous bucket. Each domain owns its types, use cases, repository interfaces, validation, and tests. Cross-domain calls pass through explicit application services or events. Database row structs do not become global domain objects.

The `pkg` directory should remain small. Code belongs there only when it is genuinely reusable outside the application. Most "shared" helpers are better kept internal so their API can evolve.

### Dependency direction

A useful rule is:

```text
transport adapters -> application use cases -> domain rules -> repository interfaces
                                          <- infrastructure implementations
```

An HTTP handler may parse JSON and call `RegisterDevice`. It should not construct SQL, publish a WebSocket message, and write an audit row itself. The use case coordinates those concerns through dependencies. The database adapter implements repository interfaces. Realtime delivery reacts to durable events rather than being a hidden side effect of the handler.

A small application constructor makes the graph visible:

```go
type App struct {
    DB            *pgxpool.Pool
    Subjects      *registry.SubjectService
    Devices       *registry.DeviceService
    Locations     *locations.Service
    Authorization *authorization.Engine
    Audit         *audit.Service
}

func NewApp(cfg Config, db *pgxpool.Pool) (*App, error) {
    // Construct repositories first, then domain services, then adapters.
    // Return an error when a mandatory dependency cannot be initialized.
    return &App{/* ... */}, nil
}
```

Avoid reflection-based service locators. Explicit construction is easier to review, test, and profile.

### Contracts before transports

Public REST schemas, WebSocket messages, native mobile bridge messages, and GPS normalized envelopes are versioned contracts. Define them independently from transport implementation details.

For example, the canonical accepted location event can contain:

```json
{
  "schema_version": 1,
  "event_id": "0195...",
  "organization_id": "0195...",
  "subject_id": "0195...",
  "device_id": "0195...",
  "session_id": "0195...",
  "sequence": 9482,
  "recorded_at": "2026-10-10T12:20:51.442Z",
  "position": {
    "latitude": 44.8124,
    "longitude": 20.4612,
    "accuracy_m": 7.1,
    "speed_mps": 4.8,
    "heading_deg": 183.0
  },
  "quality": "valid"
}
```

A durable event should be understandable without importing an internal Go struct. This allows reprocessing, external tools, and future service extraction.

### One database does not mean uncontrolled coupling

A shared PostgreSQL cluster can still have strong ownership:

- tables are grouped by module and documented;
- writes occur through owning application services;
- cross-module foreign keys are deliberate;
- reporting views prevent ad hoc joins from becoming public contracts;
- outbox events communicate important changes;
- migrations use expand-migrate-contract;
- integration tests detect unauthorized table access.

The goal is not to pretend the database is physically separate. The goal is to keep business rules from leaking into every query and handler.

### Failure domains and graceful degradation

Different roles fail differently. The API should continue serving history if the worker is unavailable. Ingestion should commit points even if a WebSocket client is slow. The worker should retry webhook delivery without blocking trip calculation. The scheduler should be safely redundant. The GPS gateway should shed abusive connections without exhausting API resources.

This suggests independent process limits:

- database connection pools sized per role;
- separate CPU and memory limits;
- separate readiness checks;
- bounded internal queues;
- distinct structured log fields;
- role-specific metrics and alerts.

The platform remains one product, but an overloaded binary protocol listener should not consume every file descriptor available to the dashboard API.

### Extraction criteria

Do not extract a service because a diagram looks cleaner. Extract only when evidence shows a concrete need, such as:

- independent scaling cannot be achieved with process roles;
- a module requires a different data lifecycle or security boundary;
- deployments are blocked by unrelated release cadence;
- database contention remains after query and partition work;
- the team structure has stable ownership and operational capacity;
- a protocol boundary is already versioned and tested.

Record the decision in an ADR with current measurements, target improvement, migration strategy, rollback plan, and the new failure modes being accepted.

### Chapter checklist

A healthy modular monolith has:

- explicit runtime roles rather than one overloaded process;
- package dependency rules enforced by tests or tooling;
- public contracts independent from database structs;
- durable events for cross-module facts;
- role-specific resource budgets and health checks;
- measurable criteria for any future service extraction.
