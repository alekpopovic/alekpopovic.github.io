# Operations review — commands, ownership and recovery scope

Source pin: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. The JSON contains the ten-playbook matrix, exact source-inventory command checks, execution scope and acceptance findings. Review follows the DevOps path from installation/configuration through deployment, health/logs, secrets, drain, observability and recovery. It distinguishes cross-author review from own-chapter self-checks and records the exact scope of each executed fixture.

## Command and environment fidelity

All observation commands in the playbook matrix resolve to the actual constructor-derived CLI inventory. Flags/configuration use the locked binary forms: no invented wait/force/default-server behavior is introduced. CLI inspect emits a direct object and ps emits an array. Nonempty flags override environment, then file; empty strings do not universally clear secrets. Source-export builds use the matching Go 1.25.0 GOROOT and `-buildvcs=false` because the export lacks `.git`, without repairing source.

Root development Compose is `compose.yaml`; production/systemd examples are deployment examples, not evidence that live state is durable. The agent's Docker access is privileged host authority. Configured DockerSocketPath does not substitute for tracing the actual SDK FromEnv transport. Listener permission and ephemeral loopback selection are explicit prerequisites. An inspected example using the daemon or global ports does not count as an executed command.

The retained CLI exercise observed no-node pending state, then authenticated injected running reports. This proves CLI/config/report behavior and carefully excludes real running workload processes. Root's real-Docker flow separately captures actual owned IDs, HTTP/log/event behavior, scale and exact cleanup. Direct-adapter HostConfig comparison confirms the resource propagation gap rather than teaching that an admitted CPU/memory request is enforced.

## Recovery and runbook matrix

| Playbook | Evidence lane | Crucial boundary |
| --- | --- | --- |
| Pending tasks | Actual CLI/report exercise | Intent acceptance differs from runtime convergence |
| Unhealthy workload | Local probes and report fixtures | Worker-local health differs from gateway reachability |
| Enrollment | Issuer/API tests | User JWT, bootstrap and issued node token have different roles |
| Node loss | Uncached control-plane/agent tests | Timeout does not stop an isolated container |
| Drain | Uncached named drain tests | Desired-stop completion does not prove physical removal |
| Failed rollout | Lab 04 controller/checkpoints | Healthy targets authorize stops; availability counts are not traffic measurements |
| Git drift | Lab 07 real local Git | Failed apply can mutate earlier files; name-based prune has ownership limits |
| Quota denial | Lab 06 handler/concurrency | Memory atomicity is not PostgreSQL advisory-lock evidence |
| Memory restart | Fresh real process | Existing PostgreSQL schema does not retain active maps or credentials |
| Database restore | Owned full-schema extension | Restored rows/retained key do not restore default live memory or volume data |

Each row's JSON record retains trigger, observations, bounded action/stop condition, verification and supported mode. A supported CLI path is checked separately from a full live playbook replay; the latter is never implied by a focused fixture. OPS-001 records a corrected review mapping: Lab 03 covers reconciliation drift. Node loss and drain instead cite the independently executed control-plane/agent tests, including stale stateless replacement, no stateful replacement, insufficient capacity, uncordon, offline-during-drain and returned-agent cleanup. This repair changes the review evidence map, not the application or its capability claims.

The full-schema experiment applied all sixteen migrations, repeated Up, refused unapproved Down, restored into a distinct owned child database, compared canary digests and refused a wrong envelope key. It also observed one assignment winner/one conflict and the retained session advisory lock after local cancellation. These are valuable database-package observations. They do not wire PostgreSQL into the server or restore Docker volumes, a registry, telemetry storage or missing master keys. Cancellation/Release returning nil is not proof a pooled physical session released its lock.

Migration reversal is reviewed as potentially destructive SQL, not a safe rollback because a file exists. The untouched upstream store fixture's migrations 1–14 omission and agent_version failure remain preserved. A corrected full-schema teaching run does not erase that failure. Schema check must be explicitly enabled; passing a schema range check still leads to MemoryService construction.

## Observability and capacity

Registered metric names, types and label keys are tied to actual constructors and consumers. Route normalization limits cardinality; raw user paths and values are not invented dimensions. Autoscaler and leadership collectors do not imply active default loops. Source-based dashboards and alert proxies retain their conditions rather than become promises about current desired state. The fixed-seed load command is a fake in-process planner/reconciler measurement, not real container density or PostgreSQL throughput.

The reviewer independently ran ten deterministic packages with `-count=1`: 186 pass events and no skips. The other independent editorial run explicitly retains its unconfigured Docker skip. Mandatory eight-lab repetition passed under 076, in order, with root as the sole PostgreSQL executor and unique records. No shared database reset, production failure or broad container/volume prune was performed by this review.

The acceptance boundary is an accurate source-based operational edition: supported commands, observed scoped mandatory drills, explicit owned cleanup and backup boundaries. It is not an assertion that the baseline can meet HA, fencing, durable recovery, remote gateway or stateful failover requirements that have no implementation. Proposed procedures retain their proposed status and required future tests.

OPS-002 resolved a narrow quota triage ambiguity in both playbook representations. CPU/memory requests multiply by replicas; positive published-port declarations count once per service. A replacement projection excludes the previous service usage. This wording now matches the inspected helper and actual Lab 06 reservation cases; no application or fixture behavior changed.
