# Compatibility and dependency baseline

Snapshot `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`, reviewed2026-10-13. This is the inspected version baseline, not advice to upgrade dependencies. `go.mod` requires **Go1.25.0**; go.mod/go.sum hashes are preserved in [toolchain.json](../validation/intake/toolchain.json). The initial tool survey is historical: exact Go1.25.0 has since been downloaded and verified by the root task. The downloaded executable needs its matching GOROOT and an isolated module/cache directory; that observation does not yet assert successful application tests.

## Direct dependencies

| Module | Locked version |
| --- | --- |
| github.com/docker/docker | v28.5.2+incompatible |
| github.com/docker/go-connections | v0.8.1 |
| github.com/jackc/pgx/v5 | v5.10.0 |
| github.com/opencontainers/image-spec | v1.1.1 |
| github.com/prometheus/client_golang | v1.24.1 |
| github.com/spf13/cobra | v1.10.2 |
| gopkg.in/yaml.v3 | v3.0.1 |

Do not promote these versions to newest/current upstream releases. Dependency sums protect downloaded content; they do not certify runtime behavior, absence of vulnerabilities, license availability or compatibility with every host. No dependency upgrades were performed.

## Four independent compatibility questions

**Compile/toolchain:** Go1.25.0 must parse/type-check the source and selected dependency modules. GOTOOLCHAIN behavior is distinct from host `go version`; record the actual executable and matching GOROOT. **Wire/API:** `/v1` DTOs, error envelopes and additive compatibility rules determine client/server communication. **Database/schema:** version.Info advertises expected16 and accepted15–16; optional startup checking rejects older/newer values. **Rolling upgrade:** sequential live replacement, pending tasks, credentials and storage continuity must be tested with actual mixed binaries. Advertised ranges alone do not establish this scenario.

Constants at internal/version/version.go11–18: server0.3.0, minimum agent0.2.0, maximum tested agent0.3.0, expected schema16, minimum15, maximum16; Info emits APIv1. RegisterNode checks CheckAgent at controlplane.go544; HeartbeatNode does so at605. Too-old agents are rejected; newer versions can receive warnings. Empty agent version defaults to server version in CheckAgent, so absence is not proof a real binary is0.3.0. Agent heartbeat/register report version metadata; CLI cluster check-upgrade queries these advertised values. Startup schema check is gated by ORCH_SCHEMA_CHECK=true at main107; migration subcommands open the separate runner regardless of ordinary memory-state composition.

## CI and what can silently skip

Locked CI uses ubuntu-latest, postgres:16-alpine, Go from go.mod and golangci-lintv2.13.1. The first two are floating identities: record actual runner/database versions for laboratory evidence. Quality steps download modules, check gofmt, vet, parse/path-test OpenAPI, lint and run atomic coverage. A separate job runs race detector. CI sets only ORCH_E2E_DATABASE_URL; it does not enable store integration URL, Docker integration or real Docker E2E. Uploaded coverage is evidence of the code exercised in that invocation, not proof skipped suites ran.

| Suite | Enabling input | Isolation and honest scope |
| --- | --- | --- |
| Docker adapter | ORCH_DOCKER_INTEGRATION=1 | Dedicated daemon/workloads; inspect exact labels and cleanup |
| Real Docker E2E | ORCH_E2E_DOCKER=1 | Own server/agent endpoints and host ports |
| PostgreSQL store | ORCH_INTEGRATION_DATABASE_URL | Destructively resets public schema; disposable database only |
| PostgreSQL E2E | ORCH_E2E_DATABASE_URL | Separate disposable database if package tests concurrent; initial-schema test covers only000001 |
| Thousand-service workload | -tags=scale | In-process MemoryService/fake node transitions, not PostgreSQL or real Docker throughput |

Run `go test -v` or JSON output and preserve Skip records. Loopback httptest/probe suites need local listener permission. GitOps tests need the git executable and temporary fixture repositories. Race instrumentation is a distinct binary/host requirement. Database packages may run concurrently with go test ./...; using the same resettable database for both env vars creates cross-package schema races. Use separate databases or run the suites sequentially. Never point destructive tests at the application database.

## Platforms and listing policy

INSTALLATION.md documents Linux/macOS/Windows on amd64/arm64, tar.gz for Unix and zip for Windows. This is documented target coverage, not a checked set of released artifacts or proof agent capacity detection has identical semantics on each OS. The baseline agent memory detection reads /proc/meminfo; non-Linux behavior needs its own test. Teach verified source builds first, and label network installer/release examples unverified until actual asset checks pass.

Each executable listing must identify source SHA, tool versions, working directory, enabling flags, destructive scope and cleanup. Expected output stays expected until a recorded command establishes observations. A future edition requires deliberate new source lock, hashes, dependency comparison, migration/API compatibility analysis, refreshed examples and review; ordinary book builds never advance the source lock.

## Primary references checked for external semantics

PostgreSQL16 distinguishes session and transaction advisory lock lifetime: [explicit locking](https://www.postgresql.org/docs/16/explicit-locking.html#ADVISORY-LOCKS). pgxv5.10.0 documents pool connection release: [Conn.Release](https://pkg.go.dev/github.com/jackc/pgx/v5@v5.10.0/pgxpool#Conn.Release). Returning a live session to a pool is not equivalent to terminating it; the orch cancellation-risk claim remains a hypothesis until measured. Go explains its toolchain-selection model: [Go Toolchains](https://go.dev/doc/toolchain). These links were retrieved2026-10-13; none claims the entire platform was exercised.

Verification: versions extracted from locked Go/source/CI files; external docs retrieved; test prerequisites and destructive reset paths inspected. No application build/test run claimed by this report. Next: reader contracts007.

## Fresh execution finding: original database fixture

Root execution record validation/intake/postgres-store-owned.json reports two guarded PostgreSQL store tests failing with SQLSTATE42703 (missing agent_version). The original fixture applies migrations1–14 while current node queries expect agent_version introduced by migration16 (000016_operations_safety.up.sql:6). This is a demonstrated fixture/schema mismatch, not an invented runtime failure or a source change. Full-schema extension execution is tracked separately; it cannot retroactively turn the original suite green.
