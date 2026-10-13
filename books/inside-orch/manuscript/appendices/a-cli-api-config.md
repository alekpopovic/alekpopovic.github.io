# Appendix A - CLI, API, and Configuration Reference

A command name is an interface, not an operational guarantee. This reference describes the pinned v0.3.0 implementation and distinguishes locally executable commands from requests that need a running server. The machine-readable companion records all 61 explicitly constructed Cobra nodes, 75 registered HTTP method/path pairs, 49 top-level and nested configuration fields, their exact source provenance, and the comparison with OpenAPI. The constructor inventory replaces the machine-specific CLI configuration path with the explicit `REFERENCE_CONFIG.yml` option; this privacy override is not the production default path. Server and agent defaults are captured before the separate precedence example sets its environment override. Automatic help and completion nodes are excluded from the authored-command count; Cobra creates those during execution.

## CLI lookup

The five persistent options are `--server`, `--token`, `--namespace`/`-n`, `--output`, and `--config`. Output accepts `table` or `json`; an unsupported value is rejected before a command runs. This does not make every command a tabular resource listing: validation, version printing and delete acknowledgments have their own output. Usage export additionally supports its own `--format` selection.

The CLI has **no built-in server URL**. This differs from the agent’s default connection address. Local `version`, `validate`, and generated help do not need a connection. Commands that construct an API client require a server URL from flags, environment or configuration. A group node such as `orch service` is a navigation parent, not an independent service operation.

The table records explicit source commands. “No validator” means Cobra does not enforce argument arity at that node; it does not authorize adding undocumented operands. Exact flag types, defaults, shorthands and accepted argument-count probes are retained in the companion inventory instead of being guessed from usage text.

| Command | Operands | Local options |
| --- | --- | --- |
| `orch audit` | `none` | `--action`, `--actor-id`, `--actor-type`, `--limit`, `--outcome`, `--since`, `--target-id`, `--target-type` |
| `orch cluster` | `none` | inherited only |
| `orch cluster check-upgrade` | `none` | inherited only |
| `orch cronjob` | `none` | inherited only |
| `orch cronjob apply` | `<file.yaml>` | inherited only |
| `orch cronjob ls` | `none` | inherited only |
| `orch cronjob resume` | `<id>` | inherited only |
| `orch cronjob suspend` | `<id>` | inherited only |
| `orch delete` | `<service-name-or-id>` | inherited only |
| `orch deploy` | `<file.yaml>` | inherited only |
| `orch endpoints` | `<service-name-or-id>` | `--include-unhealthy` |
| `orch events` | `none` | `--follow`, `--service`, `--severity`, `--type` |
| `orch gitops` | `none` | inherited only |
| `orch gitops add` | `none` | `--branch`, `--drift-policy`, `--interval`, `--path`, `--prune`, `--repo` |
| `orch gitops delete` | `<id>` | inherited only |
| `orch gitops diff` | `<service>` | inherited only |
| `orch gitops ls` | `none` | inherited only |
| `orch gitops status` | `none` | inherited only |
| `orch gitops sync` | `<id>` | inherited only |
| `orch job` | `none` | inherited only |
| `orch job logs` | `<job>` | inherited only |
| `orch job ls` | `none` | inherited only |
| `orch job run` | `<file.yaml>` | inherited only |
| `orch logs` | `<service-name-or-id>` | `--follow`, `--tail`, `--task` |
| `orch maintenance` | `none` | inherited only |
| `orch maintenance create` | `<name>` | `--duration`, `--enabled`, `--global`, `--operations`, `--schedule`, `--timezone` |
| `orch maintenance delete` | `<id>` | inherited only |
| `orch maintenance ls` | `none` | inherited only |
| `orch namespace` | `none` | inherited only |
| `orch namespace create` | `<name>` | inherited only |
| `orch namespace delete` | `<name>` | inherited only |
| `orch namespace ls` | `none` | inherited only |
| `orch node` | `none` | inherited only |
| `orch node drain` | `<node-id>` | `--force` |
| `orch node drain-status` | `<node-id>` | inherited only |
| `orch node inspect` | `<node-id>` | inherited only |
| `orch node ls` | `none` | inherited only |
| `orch node uncordon` | `<node-id>` | inherited only |
| `orch quota` | `none` | inherited only |
| `orch quota get` | `none` | inherited only |
| `orch quota set` | `none` | `--max-cpu-millicores`, `--max-memory-bytes`, `--max-public-ports`, `--max-registry-credentials`, `--max-replicas`, `--max-secrets`, `--max-services` |
| `orch retention` | `none` | inherited only |
| `orch retention prune` | `none` | `--dry-run` |
| `orch retention status` | `none` | inherited only |
| `orch rollback` | `<service-name-or-id>` | `--force` |
| `orch rollout` | `<service-name-or-id>` | `--force`, `--image`, `--max-surge`, `--max-unavailable` |
| `orch rollout status` | `<service-name-or-id>` | inherited only |
| `orch scale` | `<service-name-or-id>` | `--force`, `--replicas` |
| `orch service` | `none` | inherited only |
| `orch service inspect` | `<service-name-or-id>` | inherited only |
| `orch service ls` | `none` | inherited only |
| `orch service ps` | `<service-name-or-id>` | inherited only |
| `orch usage` | `none` | `--from`, `--to` |
| `orch usage export` | `none` | `--format` |
| `orch validate` | `<file.yaml>` | inherited only |
| `orch version` | `none` | inherited only |
| `orch volume` | `none` | inherited only |
| `orch volume create` | `<name>` | `--node` |
| `orch volume inspect` | `<id>` | inherited only |
| `orch volume ls` | `none` | inherited only |

`orch-server migrate status|up|down` is dispatched by the server entrypoint before ordinary server flags are parsed. It is not an `orch migrate` Cobra command. Migration options include `--database-url` and `--allow-down`; status and up are schema operations, while down requires explicit permission. Execute schema changes only against the disposable database defined in a laboratory. Merely printing help must never perform a migration.

## Configuration precedence without a connection

For CLI connection settings, precedence is nonempty explicit flag, nonempty environment variable, YAML file, then the empty/default value. Namespace falls back to `default`. This fully specified example demonstrates the addresses without sending traffic:

```sh
reference_dir=$(mktemp -d /tmp/orch-reference.XXXXXX)
cat > "$reference_dir/cli.yaml" <<'YAML'
server_url: http://127.0.0.1:18079
namespace: atlas-reference
YAML
ORCH_SERVER_URL=http://127.0.0.1:18080 \
  orch --config "$reference_dir/cli.yaml" \
  --server http://127.0.0.1:18082 version
```

Version printing is local and therefore does not itself reveal the selected URL. The companion offline constructor harness separately calls `config.LoadCLI` with the same file/environment/override values and observes `http://127.0.0.1:18082`, namespace `atlas-reference`. This is an executed precedence check, not a successful connection to that address. All three addresses are deliberate loopback examples. Remove only the temporary directory created by this example after retaining any evidence you need.

Server and agent configuration follow defaults, YAML, environment, then explicit overrides. Blank strings generally do not erase earlier nonempty settings. Boolean pointer overrides preserve an explicit false; do not generalize string behavior to every field. File configuration is decoded through dedicated structs and YAML unmarshalling rather than the stricter service-manifest decoder. A misspelled config key therefore needs an explicit review, even if loading succeeds.

| Configuration family | Loaded/validated | Actual consumer and boundary |
| --- | --- | --- |
| Server address and shutdown TTL | Address required; TTL positive | HTTP listener and bounded shutdown |
| Database URL | Required nonempty | Migration runner and optional schema check; does not select live persistence |
| JWT secret/users/bootstrap token | Loaded; principal parsing and handler checks | Optional user JWT gate, static role override, agent enrollment |
| Secret key | Nonempty required | Local envelope provider; loss prevents decrypting retained ciphertext |
| Heartbeat timeout/monitor interval | Positive durations | Node monitor; expiry is suspicion, not fencing |
| Debug address/pprof | Address required when enabled | Separate debug listener; profiling defaults off |
| Retention | Durations must not be negative | Memory history pruning; zero passes validation despite “positive” error wording |
| Cluster policy | Maximums must not be negative | Admission decisions; field propagation must still be checked |
| Agent name/address/labels | Required name and addresses | Registration, heartbeat and log listener identity |
| Agent Docker socket path | Loaded and required | **Ignored by runtime construction**; Docker SDK environment chooses its transport |
| CLI server/token/namespace | Selected by precedence | API client URL, bearer header and namespace header |

The inventory identifies each remaining field individually, including nested policy switches and retention durations. Sensitive fields are replaced wholesale in `orch-server config print --config <dedicated-file>` and `orch-agent config print --config <dedicated-file>`. These are actual executable options. Redaction removes database URLs, token/key material and user maps rather than merely hiding a password substring. It does not sanitize arbitrary workload logs, terminal history or all error messages.

`DATABASE_URL` reaches the server migration dispatcher; the ordinary configuration loader reads that same variable. `ORCH_SCHEMA_CHECK=true` opens the configured database to validate its schema before serving. After that check, the executable still constructs `controlplane.NewMemoryService`. A valid schema and a green startup cannot make desired services, node credentials or operations survive process restart.

## HTTP boundaries

All public workload requests select `X-Orch-Namespace` before the `namespace` query value; normalization supplies the default namespace. This is selection, not authorization. User JWT enforcement is conditional on a nonempty signing secret. With that configured, viewers read the older resource surfaces, operators perform the explicitly classified service mutations, and administrators own namespace/quota and newer fallback routes. In particular, the job, cron, volume, notification and operation surfaces fall through to admin rather than inheriting a guessed operator role.

The four `/v1/agent/` operations form a different trust surface. Registration exchanges bootstrap authority for an issued node credential. Heartbeat and assignment/status operations validate that credential and the relevant node identity; task reports additionally require assignment ownership and valid desired/actual transitions. Public OpenAPI deliberately omits these four agent routes.

Requests propagate or generate `X-Request-ID`; normal application errors contain an error code, message and request ID, with redacted details when supplied. Typical mappings include not found, invalid argument, conflict, quota exceeded, unauthorized, forbidden, failed precondition, unavailable and internal error. Inspect the route-specific response symbol and status rather than expecting every success to be 200: creates use 201, asynchronous rollout/rollback uses 202, and deletes commonly use 204. Raw mux errors and established streaming responses can differ from the JSON envelope.

Deletion of a service is soft: its lifecycle changes to deleting, and cleanup must reach removed tasks before the service becomes deleted. An accepted request is not proof of container disappearance. Operational conflicts such as an incompatible concurrent rollout return a conflict rather than silently replacing the active operation. `/healthz` and `/readyz` report process status without querying a durable backing store.

## Units and discrepancy ledger

JSON API DTOs use integer CPU millicores and memory bytes. Deployment YAML accepts human-readable CPU/memory quantities and converts its single resource pair into both requests and limits. It is not a separate arbitrary requests/limits hierarchy. Durations in domain JSON use Go `time.Duration` integer nanoseconds, while deployment YAML and file configuration accept textual duration formats through their respective parsers. Configuration’s fallback integer parser treats an integer string as seconds; do not reuse that rule for JSON DTO integers.

The static OpenAPI and registered user handlers have four coverage differences: `/metrics`, `/v1/discovery/services`, `/v1/discovery/services/{name}`, and `/v1/integrations/traefik/config` are implemented but absent from the specification. Every documented method/path has a registered handler at this revision. Parameter-name normalization was used only for comparison; the companion preserves the actual path names and wildcard suffix.

Documentation advertises a Docker socket flag; the field loads and validates, but the agent constructor calls `NewEngineRuntimeFromEnv` without it. A reader changing only that flag can target the wrong engine. Documentation’s volume overview refers broadly to claims, while the CLI creates/inspects volumes and the API separately exposes claims. Neither wording creates an unimplemented CLI claim command. These discrepancies remain visible rather than being corrected in the immutable application snapshot.

Source anchors: [Cobra tree](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go), [workload commands](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/workloads.go), [configuration](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go), [registered handlers and middleware](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go), [server composition](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go), [agent runtime construction](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-agent/main.go), [OpenAPI](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/api/openapi.yaml), and [deployment parser](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go). Generated help for all 61 authored command nodes, one complete Atlas service manifest, and both redacted config-print paths were also executed locally with zero exits. None contacts an API or Docker engine. This appendix is a source reference plus scoped offline execution, not a connected-cluster certification.

Source-backed boundary statements for this appendix are indexed in the [appendix claim record](../../validation/evidence/appendices.json). Detailed command, state, exercise and reference tables retain their own source provenance.
