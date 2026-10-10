## Chapter 4 - Repository Design and Engineering Workflow

A tracking platform spans Go, SQL, Angular, Capacitor, Kotlin, Swift, Docker, and operational scripts. The repository must make cross-language contracts visible without turning every change into a full rebuild of unrelated components.

### Repository layout

A practical monorepo is:

```text
tracking-platform/
  cmd/tracking-platform/
  internal/
  pkg/
  api/
    openapi/
    websocket/
    schemas/
  migrations/
  web/
    dashboard/
    public-tracking/
    shared/
  mobile/tracker-app/
  native/android/
  native/ios/
  deployments/
    docker/
    compose/
    nginx/
  scripts/
  tests/
    integration/
    e2e/
    load/
    fixtures/
  docs/
    adr/
    runbooks/
    progress/
```

The Go module is at the repository root unless there is a strong reason to use multiple modules. Angular applications can use a pnpm workspace. Generated clients and schemas live in predictable locations and are verified in CI.

### Architecture decision records

An ADR records a decision that would otherwise be rediscovered through code archaeology. Good early ADRs cover:

- modular monolith and runtime roles;
- PostgreSQL/PostGIS as the only mandatory infrastructure;
- transactional outbox and database job queue;
- `LISTEN/NOTIFY` as a wake-up signal only;
- UUID and timestamp standards;
- public API and WebSocket versioning;
- tenant isolation with Go filters plus RLS;
- native mobile location engines;
- provider-neutral file storage;
- criteria for adding a broker or cache later.

An ADR should state context, decision, alternatives, consequences, migration conditions, and status. It should not read like marketing copy.

### Configuration

Configuration is parsed once at startup into typed structures. Required values fail fast. Secrets can come from mounted files or environment variables, but secret values are never printed.

```go
type DatabaseConfig struct {
    URL             string
    MaxConnections  int32
    MinConnections  int32
    ConnectTimeout  time.Duration
    StatementTimeout time.Duration
}

type HTTPConfig struct {
    Address            string
    ReadHeaderTimeout  time.Duration
    IdleTimeout        time.Duration
    ShutdownTimeout    time.Duration
}
```

Provide a command that prints a redacted effective configuration and build metadata. This is valuable during incidents and prevents ambiguity about which defaults are active.

### API conventions

Define conventions before endpoints multiply:

- version prefix and deprecation policy;
- request and response media types;
- error envelope and stable codes;
- cursor pagination;
- idempotency key behavior;
- optimistic concurrency through versions or entity tags;
- correlation IDs;
- maximum body sizes;
- timestamp and unit conventions;
- partial update semantics;
- filtering and sorting grammar.

A stable error response can look like:

```json
{
  "error": {
    "code": "device_assignment_inactive",
    "message": "The device is not assigned to this subject at the recorded time.",
    "request_id": "0195...",
    "details": {
      "point_index": 17
    }
  }
}
```

Do not expose SQL errors, token parsing details, or internal stack traces.

### Testing layers

The platform needs more than unit tests:

- **unit tests** for state machines, validation, route math, and policy decisions;
- **SQL tests** for constraints, RLS, partition routing, and query plans;
- **integration tests** with a real PostGIS database;
- **contract tests** for OpenAPI, WebSocket, native bridge, and protocol schemas;
- **end-to-end tests** spanning mobile batch upload to dashboard delta;
- **fuzz tests** for parsers, public JSON, and binary protocols;
- **benchmarks** for ingestion, history queries, and fan-out;
- **restore tests** for backups;
- **field tests** on real phones and trackers.

Mocks are useful at process boundaries, but a mocked PostgreSQL transaction cannot prove RLS or `SKIP LOCKED` behavior. Use disposable real databases in CI.

### Determinism

Location tests are easily made flaky by wall clocks, random IDs, and floating-point tolerances. Inject clocks and ID generators. Seed route simulations. Store expected distance ranges instead of comparing unrounded floating-point results for exact equality.

```go
type Clock interface {
    Now() time.Time
}

type IDGenerator interface {
    New() uuid.UUID
}
```

A deterministic simulator should produce the same points, network failures, and battery values for a given seed. This makes performance regressions reproducible.

### Generated artifacts

Generated code is acceptable when the source of truth is clear. Examples include:

- OpenAPI clients;
- `sqlc` query code;
- protocol field tables;
- build metadata;
- TypeScript event types.

CI should regenerate and fail if the working tree changes. A generated file must identify its source and generation command. Never hand-edit it.

### Change workflow

A safe change sequence is:

1. Read project constraints and relevant ADRs.
2. Inspect the current repository and database migration state.
3. Write or update the contract first when public behavior changes.
4. Add the migration using expand-migrate-contract.
5. Implement the smallest coherent application change.
6. Run focused tests, then affected broader suites.
7. Update runbooks, diagrams, and examples.
8. Record exact test commands and honest outcomes.
9. Commit one reviewable intent.

Database migrations are especially important. Do not combine a destructive contract step with the application code that stops using the old field. First expand, then deploy compatible code, then migrate data, and only later contract.

### CI quality gates

A baseline pipeline should verify:

```text
go fmt / vet / test / race where practical
static analysis and dependency policy
SQL migration bootstrap and rollback policy
sqlc generation
OpenAPI and schema generation
Angular format, lint, test, and production build
native unit tests where supported
container build and vulnerability scan
license and SBOM generation
secret scanning
generated-file cleanliness
```

Critical tests should not be silently skipped when an environment variable is missing. Either provision the dependency or fail with a clear reason.

### Chapter checklist

A production repository has:

- visible module boundaries and runtime entry points;
- ADRs for cross-cutting choices;
- typed and redacted configuration;
- consistent API conventions;
- deterministic clocks, IDs, fixtures, and simulators;
- real PostGIS integration tests;
- generated-artifact verification;
- expand-migrate-contract as a normal workflow.
