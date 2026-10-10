# Modern CI state-machine laboratory

Run from this directory with an installed Go toolchain:

```bash
go test -count=1 ./...
go test -race -count=1 ./...
go vet ./...
go run ./cmd/demo
```

The module uses the standard library only. The `go` directive is a language
baseline, not a recommendation to deploy an unsupported toolchain. Use a
currently supported Go release for new work; the recorded local checks state
the toolchain actually used.

The examples cover deterministic DAG validation, fenced attempt ownership,
explicit uncertainty, idempotent result handling, bounded log sequencing,
webhook HMAC validation and exact deployment-approval identity. They are not a
server, durable queue, credential vault, container executor or distributed
scheduler. Process exit discards all ledger and log state.

`go test -race` requires a supported platform and an enabled C toolchain.
The tests use controlled timestamps rather than sleeping to simulate expiry.
No remote repository, cloud account or Docker daemon is required.

The demonstration intentionally loses a lease, refuses a blind retry,
reconciles execution, rejects the stale result, and accepts the current one.
See [the runbook](../../manuscript/a-laboratory-runbook.md) for interpretation.
