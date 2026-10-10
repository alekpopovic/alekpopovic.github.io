# Go Core Teaching Examples

Three in-memory examples illustrate versioned state transitions, single-use
approval binding and scoped quota reservation. They do not implement PostgreSQL,
Kubernetes, network isolation, a durable authorization service or external effects.

```sh
cd examples/go-core
go test -race ./...
go vet ./...
```

Go 1.23 or later is sufficient for these dependency-free teaching programs.
That minimum is not the version baseline for a production AgentPlane service.
The tests include concurrency, replay, changed scope, expiry and terminal-state
checks. Production equivalents require persistent records and recipient-side
fencing. The maps intentionally retain identities without a retention subsystem;
never expose these examples as unbounded public services.
