# Lab 06 — Namespace boundaries and competing quota admissions

By Aleksandar Popovic. Source edition: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`.

## Problem and experiment boundary

Atlas Payments and Observability both need a service named `api`. An operator must distinguish namespace lookup, authorization, resource admission and physical isolation. This executable teaching extension constructs the actual API handler and MemoryService, sends real HTTP request objects through them, and records generated object IDs. It uses `httptest.NewRecorder`, without binding a socket. There is no connected host, Docker daemon or PostgreSQL request in this lab. Injected JWTs use a synthetic process-local key and are never printed.

Prerequisites are the locked disposable Orch source copy, Go 1.25.0, cached locked dependencies and the book fixtures. The previous lab's security observations inform the permission predictions; its process state is deliberately not reused. This lab initializes its own namespaces and quota state. Lab 07 likewise initializes independent state and carries the namespace/admission lessons forward rather than inheriting these objects.

Inspect `internal/namespace/context.go`, `internal/api/namespace_test.go`, `internal/controlplane/namespace_test.go`, both quota test files, `internal/quota/quota.go`, store locking methods and migrations 000011/000012. Consult `docs/MULTI_TENANCY.md` as documentation and compare it with the selected namespace implementation.

## Inputs and setup

`fixtures/tenants.json` describes distinct labels for identifying the scenario. Those labels are fixture annotations: ServiceSpec has no arbitrary Labels field. The actual service uses supported non-sensitive `Env` markers for the team. `fixtures/api-base.json` supplies one replica, 100 millicores, 64 MiB and one positive public-port declaration. `fixtures/quota.json` sets all seven limits:

| Limit | Value | Measured object |
| --- | ---: | --- |
| Services | 2 | Active services |
| Replicas | 3 | Desired service replicas |
| CPU | 300 millicores | Request times desired replicas |
| Memory | 201326592 bytes | 3 × 64 MiB |
| Public ports | 2 | Positive declarations in ServiceSpec, once per service |
| Secrets | 1 | Namespace-local secrets |
| Registry credentials | 1 | Namespace-local credentials |

Never run the program in `evidence/orch`. Copy the canonical `examples/teaching-extensions/lab06/main.go` into `.book-labs/namespaces-quotas/main.go` under a verified disposable export of the pinned module. The recorded execution used `/tmp/inside-orch-labs-cbfc94ade5b5/orch`. From that copy run, with your toolchain environment configured:

```sh
go run ./.book-labs/namespaces-quotas /absolute/site/books/inside-orch/labs/06-namespaces-quotas/fixtures
```

The exact executed argv, working directory, UTC interval and exit code are in `validation/labs/lab06-canonical-fixtures.json`; stdout contains all 28 structured observations. This command has already executed with Go 1.25.0; the placeholder absolute path above is reader setup, not an additional observed run. Export `GOTOOLCHAIN=local`, use the verified Go 1.25.0 `GOROOT`, and set `GOFLAGS=-buildvcs=false` for the exported source tree without `.git`. The standard recorded runner can retain a new run using a new output name. It refuses overwriting prior evidence.

## Predictions and observed results

Predict the response before reading `06-check.json`:

| Question | Prediction from source | Actual scoped result |
| --- | --- | --- |
| Can both tenants create `api`? | Yes, distinct generated IDs | Passed; IDs captured |
| Can Payments fetch Observability's service ID? | 404, including cluster-admin actor with selected Payments scope | Passed |
| Which selector wins? | `X-Orch-Namespace` before query; query fallback before default | Passed; documentation's header/default shorthand is incomplete |
| Does a viewer cross scopes? | Own scope 200, other scope 403 | Passed |
| Can namespace admin list cluster namespaces? | 403; cluster admin 200 | Passed |
| Do same-name secrets share data? | Independent; cross-scope reference rejected | Passed; plaintext absent from output |
| Does denied scale mutate desired replicas? | No; scale 1→4 exceeds replica quota | 409 structured `quota_exceeded`, replicas stay 1 |
| What happens to two scale requests competing for one slot? | One succeeds, one quota denial | Passed; final total exactly three replicas |
| Can quota zero mean no replicas? | No; zero means unlimited | 1000 desired replicas admitted in separate no-node fixture |
| Is namespace deletion always possible after service deletion? | No; retained history can block it | Passed; 409 retained and explained |
| Do independently constructed memory servers share a tenant? | No | Second handler returns 404 and only has default namespace |

The arithmetic starts at one service × one replica: 100 millicores, 67108864 bytes, one public-port declaration. Adding a portless worker gives two services and two replicas. Two concurrent updates each request a second replica on a different service. Exactly one update is admitted: three replicas, 300 millicores, 201326592 bytes, one public-port declaration. This proves the in-memory admission operation's tested atomicity, not PostgreSQL serialization. Quota error `Used` and `Requested` represent projected totals in this implementation; they are not old usage and an incremental delta.

Deleting the worker releases its desired-resource accounting. The secret and registry tests separately exceed their one-object quotas and check structured errors without recording their values. Conflicting usage query and selected header returns 404. The default namespace remains undeletable. No test reaches into internal maps to erase history.

## Independent assertions and troubleshooting

From the site root:

```sh
python3 books/inside-orch/scripts/verify_namespace_workload_labs.py --lab 06
```

This offline verifier checks the frozen input/output hashes, exact source pin, response records, arithmetic and required cases. It validates retained observations; it does not repeat the experiment. A fresh program run produces new IDs and timestamps and must be retained separately. If a quota denial is unexpectedly absent, inspect current projected usage and the selected namespace before changing limits. If a scope test fails, inspect role claims and header/query precedence before assuming object corruption.

PostgreSQL is a separate prerequisite and storage experiment. Require a dedicated `_test` database, verified lab-only container labels, loopback address, all sixteen migrations and exclusive ownership before testing transaction/advisory-lock quota admission. The upstream test reset applies migrations 1–14 and omits `agent_version` from migration 16; root intake retains the observed 42703 failure. Do not inherit this lab's success into a PostgreSQL status. `06-check.json` explicitly says PostgreSQL quota execution was not performed.

## Cleanup, rerun and architecture review

All objects are process-local. The harness attempts supported deletions, observes history preventing namespace deletion, then discards the process. It touches no shared database or daemon. Rerun by starting a fresh process, not by forcibly clearing namespace history. Synthetic values never become production credentials.

| Boundary | Implemented and measured here | Extension still needed |
| --- | --- | --- |
| Logical lookup | Namespace-qualified names and hidden cross-scope IDs | Review every new route for selector propagation |
| RBAC | Scoped viewer/admin and cluster administration | Hostile tenant threat model and identity lifecycle |
| Admission | In-memory atomic desired-resource accounting | Separately executed persistent transaction path |
| Runtime isolation | No claim from namespace metadata | Network, daemon, filesystem and workload isolation |
| Failure domains | Independent servers do not share active memory | Explicit shared state and recovery integration |
| Durable recovery | None supplied by this memory harness | Backup, restore, keys and tenant-history procedures |

A namespace is useful organization and an authorization boundary within the tested API. It does not create a separate Docker daemon, network or durable control plane.
