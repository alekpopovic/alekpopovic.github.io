# Isolated laboratory contract

Source edition: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. Commands below are procedures, not captured results. Actual runs belong in `validation/labs/` with UTC start/end, command, exit status, prerequisites and working directory. The read-only capability report is `validation/intake/lab-environment.json`.

## Two tracks

**Source-only track:** copy the locked source outside the website, build with Go 1.25 or newer (`GOFLAGS=-buildvcs=false` for the source export without .git; set GOROOT to the chosen toolchain, GOENV=off and run-owned caches) and run `go test ./...` with external integration environment variables unset. Scheduler, lifecycle, resource parser, API/FakeRuntime, rollout, namespace, policy and deterministic controller assertions need neither Docker nor PostgreSQL. Tests may open loopback HTTP listeners. An ordinary pass does not mean gated Docker/database tests ran. Fuzz targets are separate timed exercises; build caches and downloaded dependencies belong outside canonical evidence.

**Disposable execution track:** run separately built CLI/server/agent binaries, then opt into Docker and PostgreSQL experiments. Docker socket access grants broad control of the host daemon; use a dedicated disposable daemon/VM where practical. An agent launched against the regular host socket can affect other orch-labelled workloads, so never use broad adoption/cleanup on a shared worker. Database integration code in `internal/store/postgres_test.go` executes `DROP SCHEMA public CASCADE`; the guard below must identify a dedicated container before invocation. A PostgreSQL server beside `orch-server` does not persist `MemoryService` maps.

## Explicit owned resources

| Resource | Scope and privilege | Planned endpoint/identity | Cleanup |
| --- | --- | --- | --- |
| Application copy | User-owned temporary files; immutable source copied, never executed in evidence | `/tmp/inside-orch-labs-cbfc94ade5b5/orch` | Remove only after evidence archived; preserve the canonical corpus |
| Go/cache/output | Compiler and downloaded module bytes; no system install | `/tmp/inside-orch-go`, `/tmp/inside-orch-gomod`, `/tmp/inside-orch-gocache`; binaries under run directory | Delete only exact run-owned paths, never global Go cache |
| API process | Loopback listener; disposable tokens and state | `ORCH_SERVER_ADDR=127.0.0.1:18090` | Send TERM to recorded PID and wait; do not kill by process name |
| Agent process | Docker socket privileged; set actual supported configuration | `ORCH_AGENT_ADDR=127.0.0.1:18091`, `ORCH_ADVERTISE_ADDRESS=http://127.0.0.1:18091` | Stop recorded PID before removing containers |
| Database | Destructive schemas allowed only in owned throwaway container | `inside_orch_lab_<run>`, PostgreSQL16; host binding `127.0.0.1:<allocated-port>:5432` | Remove exact labelled container and its exact dedicated volume, if created |
| Service containers | Docker create/start/remove; nginx image, dynamic host port | `atlas-api` in explicit lab namespace; record container IDs from API/Docker; orch labels alone insufficient ownership | Stop controller/agent, inspect each recorded ID, remove only exact owned IDs |
| Finite job container | Explicit once-only command, disposable alpine image | `atlas-count`; use JobSpec rather than the upstream redis service called worker | Remove exact recorded task/container IDs |
| GitOps repo | User-owned temp Git repository, no push/credentials | `/tmp/inside-orch-<run>/gitops`, service identity remains atlas-api | Remove exact repo after recording commits and outputs |
| Storage fixture | Separate local directory/volume; no user paths | `/tmp/inside-orch-<run>/volumes` | Exact fixture only; no volume prune |

Ports18090/18091 are suggestions and must be checked before binding; if occupied choose new loopback ports and record them. Workload published ports may bind all interfaces because the pinned Docker adapter does not expose a loopback HostIP field. Run those experiments in an isolated daemon/VM or accept that disposable workload exposure explicitly; do not claim `ORCH_SERVER_ADDR` restricts workload port binding. Dynamic allocation is node-scoped, not a cluster-wide reservation.

The upstream compose file publishes PostgreSQL5432, server8080, agent8081, demo18080, Traefik8088/8082/8443 and Prometheus9090 without loopback restriction. Do not launch it unchanged on a shared host. The Traefik profile uses `api.insecure=true`, and monitoring images include moving latest tags: these are upstream local examples, not a secure production prescription. Docker images for a measured run must have their resolved image IDs/digests recorded. No image or installer is fetched implicitly by the prerequisite checker.

## Read-only capability check

From the website root:

```sh
python3 books/inside-orch/scripts/check_lab_prerequisites.py \
  --go /path/to/existing/go \
  --output books/inside-orch/validation/intake/lab-environment.json
```

Add `--probe-docker` only when a read-only Docker daemon version request is appropriate. The helper runs tool version commands with `GOTOOLCHAIN=local`, so invoking Go does not download a toolchain. It starts no process services, changes no infrastructure, and reports unavailable tools. The output file is an explicitly requested book evidence artifact.

## Database reset guard

Provision a uniquely named disposable PostgreSQL container with labels `inside-orch.lab=true` and `inside-orch.run=<unique-run>`, `POSTGRES_DB=inside_orch_lab_<run>`, and only a `127.0.0.1` host binding for5432. Record its ID, image ID and binding. Keep its disposable password out of logs; provide the URL through `INSIDE_ORCH_LAB_DATABASE_URL` in the current process environment. Do not reuse any existing real database.

```sh
python3 books/inside-orch/scripts/run_database_tests.py \
  --container <recorded-container-id> \
  --working-copy /tmp/inside-orch-labs-cbfc94ade5b5/orch \
  --go /path/to/existing/go --check-only
```

Only after that passes, repeat without `--check-only`. The helper rejects remote hosts, wrong database names, missing ownership labels, mismatched published ports and altered source copies. It sets only `ORCH_INTEGRATION_DATABASE_URL` for the store suite. It deliberately does not enable E2E database tests, which exercise a different migration scope. The checker is a scope guard, not a guarantee against a malicious Docker daemon or concurrent administrator.

## Interrupted-run recovery

Keep `run-resources.json` in the run evidence with exact PIDs, container IDs, volume names, namespace/service/task IDs and temp directories. Stop recorded server/agent PIDs first; verify PID command lines if recovering after interruption to avoid reused PIDs. Inspect each recorded container's labels/name/image and remove that ID only. Never run `docker system prune`, `docker volume prune`, killall, or a broad `orch.managed=true` deletion. Remove only the explicitly named throwaway database. If ownership cannot be re-established, leave the resource and document the unresolved cleanup rather than guessing. Export observations before deleting state; redact bearer/bootstrap/registry credentials. Restart means a new process and new `MemoryService`, not reusing an object in a unit test.

Configuration anchors: `internal/config/config.go` server environment handling starts313; agent handling starts353. Default composition: `cmd/orch-server/main.go`142–158. Source documentation: `docs/DEVELOPMENT.md`, `docs/TESTING.md`; all references resolve under the pinned snapshot.

## Observed baseline database fixture defect

The guarded run `validation/intake/postgres-store-owned.json` executed all three PostgresStore tests on the designated disposable database. `TestPostgresStoreWithTxRollsBackOnError` passed. The integration and concurrent-assignment tests failed with SQLSTATE42703 because node operations select `agent_version`, but their reset helper applies migrations000001–000014 and that column arrives in000016. This is an observed fixture/schema mismatch, not missing PostgreSQL tooling and not proof that assignment concurrency is broken. Preserve the failing raw log. The separately recorded all16-migration teaching fixture, validation/intake/full-schema-recovery-corrected.json, passed its guarded assignment and recovery checks; it is not silently substituted for the untouched upstream suite. The PostgreSQL E2E fixture applies only000001 and cannot establish later schema compatibility.
