# Practice questions

Keep answers separate while attempting the required artifact. Each rubric criterion is worth two points; partial answers must state their missing assumption. Source links refer to the pinned baseline.

## DEV-01 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 10 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

Two scheduler attempts hold the same pending task snapshot and expected UpdatedAt. Explain why one assignment wins, how the loser is represented, and whether exactly one runtime process is thereby guaranteed.

Required artifact: A three-step claim trace and the isolated test log.

Source: [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go).

Scoring: one successful claim (2 points); one assignment event (2 points); physical fencing remains unproven (2 points).

Hint: Inspect persistAssignment and the fixture’s success/event assertions.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/scheduler -run '^(TestConcurrentSchedulerAttemptsAssignTaskOnce)$'
```

## DEV-02 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 14 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

An assigned service task reports unhealthy while its policy permits replacement. Trace report status, stored actual state and replacement identity; distinguish a non-restartable service.

Required artifact: A status/identity table plus the named local test log.

Source: [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go).

Scoring: incoming unhealthy retained in trace (2 points); stored failed for restartable branch (2 points); new identity instead of resurrection (2 points).

Hint: Find the policy conversion before task state storage.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/controlplane -run '^(TestUnhealthyRestartableTaskIsMarkedFailed)$'
```

## DEV-03 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 18 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

A task is actual failed. Compare a removed report under desired running and desired stopped, then show which evidence completes service deletion.

Required artifact: Two guard evaluations and a cleanup trace plus the test log.

Source: [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go).

Scoring: running-intent removal rejected (2 points); cleanup-intent removal accepted (2 points); all actual tasks removed required (2 points).

Hint: Read AgentCanReportTaskStatus in branch order.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/controlplane -run '^(TestAgentTaskStatusAllowsFailedTaskRemovalDuringDeletion)$'
```

## DEV-04 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 17 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

For desired replicas two, MaxSurge one and MaxUnavailable one, explain why a running new task may not permit old-task retirement or successful completion.

Required artifact: A version/status budget table and the rollout test log.

Source: [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go).

Scoring: active budget 3 (2 points); minimum available 1 (2 points); new running is not newHealthy (2 points).

Hint: Compare newHealthy with the shared old availability helper.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/rollout -run '^(TestControllerSuccessfulRollout)$'
```

## DEV-05 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 27 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

Team A knows Team B’s service UUID. Predict GetService under A’s context, then distinguish this service test from a blanket claim about every workload endpoint.

Required artifact: A two-namespace lookup matrix and the namespace test log.

Source: [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go).

Scoring: A list excludes B (2 points); B UUID yields not found for A (2 points); new workload paths require separate review (2 points).

Hint: Inspect the fixture’s cross-namespace GetService assertion.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/controlplane -run '^(TestNamespaceIsolationAndDuplicateNames)$'
```

## DEV-06 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 28 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

Two one-replica services share MaxReplicas three. Concurrent requests each scale one service to two. Determine allowed final total and request outcomes without naming the winning service.

Required artifact: A race timeline and the quota test log.

Source: [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go).

Scoring: one success (2 points); one quota denial (2 points); final total 3 independent of winner (2 points).

Hint: The fixture synchronizes goroutines with a shared start channel.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/controlplane -run '^(TestConcurrentScaleCannotExceedQuota)$'
```

## DEV-07 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 30 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

A local GitOps source manages api. Re-sync unchanged content, remove its manifest in a new local commit, and explain the prune boundary.

Required artifact: A revision/service-version trace and the local Git fixture test log.

Source: [internal/gitops/gitops.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go).

Scoring: unchanged revision no new version (2 points); prune limited to managed identity (2 points); model deletion differs from runtime cleanup (2 points).

Hint: Separate the previous managed set from the current manifest names.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/gitops -run '^(TestControllerSyncsLocalFixtureRepositoryAndPrunes)$'
```

## DEV-08 — developer

Estimated time: 35 minutes. Prerequisites: Read Chapter 31 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence. Go 1.25.0 and cached dependencies; Git installed for the GitOps fixture.

Using the fake-clock fixtures, compare Forbid and Replace with one active job, then explain catch-up with three missed minutes and MissedScheduleLimit two.

Required artifact: An occurrence/active-job table and both named test results.

Source: [internal/cronjobs/cronjobs.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go).

Scoring: Forbid no extra job (2 points); Replace changes identity (2 points); catch-up jobs 2 (2 points).

Hint: The cron controller has an explicit Clock seam; do not assume every package does.

Offline command in the disposable module:

```sh
go test -count=1 ./internal/cronjobs -run '^(TestParseAndRunWithFakeClock|TestConcurrencyForbidAndReplace)$'
```

## OPS-01 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 24 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

Ciphertext and its database backup survived, but the envelope key was lost. Design the recovery decision and secret-safe evidence collection.

Required artifact: A recovery checklist with key/ciphertext ownership and stop conditions.

Source: [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go).

Scoring: matching key required (2 points); synthetic canary only (2 points); no automatic plaintext recovery claim (2 points).

Hint: Separate encryption metadata from recoverable key material.

## OPS-02 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 03 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A supervisor restarts the default server and /readyz becomes green. Services and node credentials disappeared. Explain the incident and bound the recovery action.

Required artifact: A before/after identity inventory and re-enrollment decision record.

Source: [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go).

Scoring: MemoryService named (2 points); readiness independent of data (2 points); owned runtime reconciliation before replay (2 points).

Hint: Start at the constructor rather than the migration directory.

## OPS-03 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 39 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A fake-agent run reports high placement throughput. Prepare a report that keeps the result useful while rejecting a Docker or PostgreSQL performance claim.

Required artifact: A fully specified measurement sheet with run status and a claim boundary.

Source: [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go).

Scoring: full reproducibility inputs (2 points); fake-agent scope explicit (2 points); no Docker/database inference (2 points).

Hint: Read the runtime constructor used by the load tool.

## OPS-04 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 05 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

The workload requests 250 millicores and 134217728 bytes. Docker inspection on the ordinary agent path reports both limits zero, while direct adapter construction applies them. Write a triage plan.

Required artifact: A field-flow diagram from service through assignment to ContainerSpec and engine inspection.

Source: [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go).

Scoring: missing Resources field identified (2 points); request/reservation distinct (2 points); actual inspect boundary retained (2 points).

Hint: Compare the agent literal with the adapter’s HostConfig mapping.

## OPS-05 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 23 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A heartbeat rotates a node credential, but its response is lost. The worker retries with the old token. Design a bounded diagnosis and enrollment recovery.

Required artifact: An authentication timeline with stored-hash/client-token divergence and safe stop condition.

Source: [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go).

Scoring: rotation/receipt separate (2 points); no token logging (2 points); bounded authorized recovery (2 points).

Hint: Treat credential issuance and response receipt as separate events.

## OPS-06 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 19 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A node goes offline while hosting stateless Atlas API and stateful local-volume work. Explain replacement choices and how an old worker can still be running.

Required artifact: Two task/condition traces and a fencing risk decision.

Source: [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go).

Scoring: stateless replacement trace (2 points); stateful locality retained (2 points); no physical fencing inference (2 points).

Hint: Keep Task conditions independent from actual/desired status.

## OPS-07 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 37 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

All /healthz and /readyz requests succeed while work is pending and the database is unavailable. Build an observation plan that distinguishes these facts.

Required artifact: A three-layer health table with a verification probe for each layer.

Source: [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go).

Scoring: process/workload/store separated (2 points); startup check not continuous (2 points); missing data remains unknown (2 points).

Hint: Read readyz, then find the actual server store constructor.

## OPS-08 — devops

Estimated time: 45 minutes. Prerequisites: Read Chapter 35 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

Design a future PostgreSQL restore rehearsal for an explicitly wired durable extension while preserving the default-server boundary.

Required artifact: A canary/digest recovery plan with key backup, schema, downtime and rollback criteria.

Source: [internal/migrations/manager.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go).

Scoring: all 16 schema and canary (2 points); envelope key retained (2 points); default memory limit explicit (2 points).

Hint: Restore completeness is an application-level property as well as a database command result.

## ARC-01 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 17 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

For desired replicas 5, MaxSurge 2 and MaxUnavailable 1, compute the active and minimum-available budgets and identify which snapshots can violate a real availability promise.

Required artifact: A budget calculation and counterexample timeline.

Source: [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go).

Scoring: max active 7 (2 points); min available 4 (2 points); stale observation counterexample (2 points).

Hint: Separate arithmetic from the freshness of its inputs.

## ARC-02 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 05 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

Five replicas each request 250 millicores and 128 Mi. Compare their reservation with quota 1500 millicores and 700 Mi, then explain why passing arithmetic is not measured capacity.

Required artifact: A unit-correct table and an enforcement boundary statement.

Source: [pkg/types/types.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go).

Scoring: CPU 1250 (2 points); memory 671088640 (2 points); reservation not observed usage (2 points).

Hint: Use binary Mi=1048576 bytes and keep CPU in millicores.

## ARC-03 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 34 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

Propose the minimum composition changes for durable intent and activated leader ownership, including a failure test that could falsify your design.

Required artifact: A labeled future-extension dependency graph and crash-test plan.

Source: [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go).

Scoring: live owner replaced (2 points); leader loss reaches side effects (2 points); crash-window oracle (2 points).

Hint: List callers and ownership changes, not just new packages.

## ARC-04 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 34 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A canceled lease closes Done and Release returns nil, but another pool cannot acquire until the first pool closes. Explain the session-level failure and design a release test.

Required artifact: A two-pool lock ownership diagram and a corrected release contract.

Source: [internal/leadership/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go).

Scoring: original session ownership (2 points); Done not unlock proof (2 points); two independent pools (2 points).

Hint: Track database session identity across cancellation and deferred Release.

## ARC-05 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 26 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

An HTTP probe’s first destination is allowed, but it redirects to loopback metadata-like space. Define a safe synthetic test and the limitation of a URL-only validation check.

Required artifact: A resolver/redirect policy diagram with a zero-hit loopback oracle.

Source: [internal/health/health.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go).

Scoring: owned fixture only (2 points); redirect/dial policy evaluated (2 points); forbidden hits 0 (2 points).

Hint: The final connection target matters as much as the original URL.

## ARC-06 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 27 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

A newer resource lookup takes only a global ID. Specify the minimum object-level namespace test even if user authentication already requires admin.

Required artifact: An authorization matrix for known/unknown/foreign IDs and a test-gap entry.

Source: [internal/controlplane/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go).

Scoring: foreign lookup matrix (2 points); mutation coverage separate (2 points); test gap not hidden (2 points).

Hint: Separate global role power from the method’s declared tenancy contract.

## ARC-07 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 25 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

An image string contains a syntactically valid sha256 digest. Explain which supply-chain claims remain unproved and propose additional evidence.

Required artifact: A syntax/resolution/content verification ladder.

Source: [internal/image/reference.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go).

Scoring: syntax support only (2 points); remote/content evidence distinct (2 points); future workflow labeled (2 points).

Hint: A reference parser does not perform remote registry resolution.

## ARC-08 — architect

Estimated time: 45 minutes. Prerequisites: Read Chapter 38 and the pinned source mechanism. Use only a disposable module copy; never mutate evidence.

Define a task-convergence latency metric for an experiment with missing reports and restarts. Explain why an unconfigured alert is only a proposal.

Required artifact: A measurement contract with start/stop events, clock origin, censoring and scope.

Source: [internal/metrics/prometheus.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go).

Scoring: version-matched event boundaries (2 points); censored missing data (2 points); alert proposal explicit (2 points).

Hint: Define missing data before calculating a percentile.
