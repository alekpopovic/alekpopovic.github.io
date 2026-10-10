# 16. Metrics, Events, and Operational Signals

## 16.1 Three Separate Questions

Is the operator healthy? Do contracts satisfy their rules? Are applications running successfully? These are three different signal classes. `Ready=False` for one contract should not fail manager liveness, and a healthy manager does not mean every contract is green.

Liveness checks whether the process can continue running. Manager readiness checks operational prerequisites such as controller startup and required initialization. Contract metrics describe domain results.

## 16.2 Proposed Metrics

| Metric | Type | Meaning |
|---|---|---|
| `secret_contract_ready` | Gauge | 1 only for confirmed current Ready |
| `secret_contract_missing_keys` | Gauge | Number of missing required keys |
| `secret_contract_violations` | Gauge | Published or total findings; define explicitly |
| `secret_contract_checks_total` | Counter | Evaluations by bounded outcome |
| `secret_contract_check_duration_seconds` | Histogram | Evaluation duration |
| `secret_contract_mutations_total` | Counter | Approved mutation operations by outcome |

Prometheus recommends stable names, clear units, and controlled label cardinality. Each distinct set of label values creates a new time series. [S23](https://prometheus.io/docs/practices/naming/)

`namespace` and contract name may be acceptable for opt-in per-object metrics, but can still become expensive. Global counters use a small outcome enum. Do not add UIDs, resourceVersions, every Secret key name, patterns, error messages, or values as labels.

## 16.3 Unknown and Unconfigured Checks

For the main `ready` gauge, 1 means confirmed True and 0 means everything else. An additional condition metric can distinguish True, False, and Unknown through a bounded enum. Do not use NaN as an unexplained signal in the basic dashboard.

An unconfigured optional integration is not an error. The dashboard should display `NotConfigured` or omit the corresponding per-integration series, following a documented rule. An ESO alert must not fire for contracts that do not use ESO.

## 16.4 Cleaning Up Series

When a contract is deleted, remove its gauge series from the collector. Otherwise a nonexistent contract remains red or green until the operator restarts. With multiple replicas, per-object metric exposure must avoid confusion between leader and standby views.

Per-object counters require extra care because of churn; prefer aggregate counters and bounded per-object gauges. Test creation and deletion of many short-lived contracts.

## 16.5 Events

Emit `ContractReady` on a relevant transition. Emit `SecretValidationFailed` for a new set of findings, not every identical reconcile. `WorkloadPatched` means a successful API patch, not a completed rollout.

Messages are generated locally, remain short, and contain no raw parser or provider errors. For example: “Required key DB_PASSWORD is missing.” A stricter metadata mode may say “One or more required keys are missing.”

## 16.6 Protecting the Metrics Endpoint

Metrics can reveal application names, namespaces, and internal-system state. Do not expose the endpoint publicly without controls. The installation defines TLS and authentication or another documented private transport model, with NetworkPolicy where the network implementation supports it.

ServiceMonitor is optional and exists only when the corresponding Prometheus Operator CRD is present. Enabling it must not break the default installation on a cluster without Prometheus Operator.

## 16.7 Suggested Alerts

An alert for a contract that remains invalid for more than five minutes can be an initial operational policy, not a universal standard. High reconcile error rates belong to the operator maintainer. Application failures belong to the application owner. Do not send every alert to everyone.

Monitor prolonged absence of new observations when changes are expected, frequent API conflicts, metadata-only restart storms, and persistent ESO adapter unavailability. Reason names should remain stable between patch releases.

**Checkpoint.** The metrics endpoint must not reveal secret contents, per-key value lengths, or deterministic fingerprints. Check unnecessary cardinality as well.
