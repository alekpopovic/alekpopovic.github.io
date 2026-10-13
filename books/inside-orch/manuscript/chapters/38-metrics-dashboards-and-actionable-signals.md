# Chapter 38 - Metrics, Dashboards, and Actionable Signals

Atlas's dashboard shows a growing “Task State Counts” panel while the current service has only two replicas. Nothing is necessarily wrong with the workload. The panel sums a counter of reported state changes, so it accumulates transitions rather than displaying current task inventory. Before using the panel to trigger an incident, the team must understand what its metric actually measures.

This chapter follows a signal from emission to exposition, scrape configuration, alert expression, dashboard query, and operator action. You will distinguish counters from gauges, detect misleading proxy names, and identify when a collector exists without an active caller. Atlas's lab injects one synthetic runtime failure and observes the real metrics wrapper and registry output. Alert evaluation and live Grafana operation remain separate, unclaimed activities.

## Metric Emission and Meaning

Metrics begin at a call site, not a dashboard. The server registry defines API request counters and duration histograms, scheduler/reconciler collectors, task and rollout counters, autoscaling gauges, leadership gauges, and DNS counters. The [collector definitions provide exact names and labels](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L41-L132). Their presence establishes an available instrument; it does not prove that a particular executable path emits observations into it.

The server actually supplies metrics to its scheduler and rollout controller. API middleware records recognized method/route/status combinations, and the agent binary wraps its runtime with instrumentation. In contrast, a registered reconciler or leadership collector does not mean the default server starts those components through that instrumented path. Read the constructor and loop together before interpreting a zero value as successful idle operation.

The [access-log middleware records only paths recognized by metricRoute](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1426-L1434). Route normalization is an important cardinality boundary: a route template should represent many object IDs. Using raw user-controlled paths as labels would create new time series for arbitrary URLs. A missing unrecognized path in this metric is therefore not proof that no HTTP request occurred; logs and request metrics have different selection rules.

Even an apparently simple counter needs a precise event definition. The task-failure metric increments after an accepted agent request whose requested status is failed. The [call site does not test whether this is the first failed transition](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L689-L704). Duplicate accepted failure reports may therefore increment the counter while the control-plane event logic remains idempotent. Treat tasks_failed_total as counted accepted failure reports, not an exact count of distinct failed task identities.

The Docker wrapper has a particularly clear definition:

```go
func (r *instrumentedRuntime) measure(operation string, call func() error) error {
	r.metrics.IncDockerOperation(operation)
	err := call()
	if err != nil {
		r.metrics.IncDockerOperationError(operation)
	}
	return err
}
```

Exact source: [internal/docker/metrics.go:96–103](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/metrics.go#L96-L103).

It counts the attempted operation before calling the next runtime, and counts an error when that call returns a non-nil error. It does not measure a container's eventual application health. A successful start call can still be followed by an immediate application exit; healthcheck and task-status observations belong to separate signals.

Commit [b3e29e593f46b4e90899a56bd9391c03d7c42f1a](https://github.com/alekpopovic/orch/commit/b3e29e593f46b4e90899a56bd9391c03d7c42f1a) introduced observability code. Later alert and dashboard commits added consumers. History helps explain why collectors and panels evolved separately, but the current source and actual emission determine the meaning available to Atlas now.

## Labels, Cardinality, Counters, and Gauges

A counter accumulates observations and normally resets when its process restarts. A gauge describes a sampled value that may increase or decrease. A histogram records observations across cumulative buckets with count and sum. Confusing these types changes the question a query answers. Summing a state-change counter cannot reconstruct the current number of running tasks after arbitrary transitions and restarts.

Agent metrics label Docker operations by operation and task state changes by status. These are bounded vocabularies. API labels use method, normalized route, and status. Leadership uses controller names. The autoscaler recommendation gauge uses service_id, which is a deliberate higher-cardinality exception to the general low-cardinality guidance in the observation documentation. Atlas should budget and review that series lifecycle rather than claim every collector avoids object identifiers.

Labels also define aggregation boundaries. Summing Docker errors across every agent can identify a broad runtime problem but hides which instance failed. A dashboard grouped by operation can distinguish image pulls from start failures; an operator then needs instance-level detail or logs to find the node. Do not add secret-bearing image URLs or arbitrary workload labels simply to make a convenient drill-down.

The [registry handler exposes Prometheus text for its own registry](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L165-L173). Separate server and agent registries produce different series. A successful server scrape does not establish that the agent's runtime metrics were collected, nor that PostgreSQL exporter credentials work. Atlas should verify each configured target and retain the job/instance labels added by Prometheus.

The bundled [scrape configuration uses fifteen-second scrape and evaluation intervals](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/prometheus.yml#L1-L22). It names server, agent, and postgres jobs with explicit container-network targets. Those names matter because availability rules filter by job. Copying only an expression into another Prometheus deployment with different job labels can silently produce no series. Configuration is part of the signal chain.

## Alert Expressions and Dashboard Proxies

The Docker error alert is named DockerOperationErrorsHigh. Its exact expression is `sum(rate(docker_operation_errors_total[5m])) > 0.1`, held for ten minutes. The corresponding dashboard panel sums the same rate grouped by operation. The [rule aggregates across agents](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/prometheus-rules.yaml#L107-L116), whereas the panel preserves the operation dimension. Atlas's first response should inspect affected agent logs, Docker daemon availability, socket permissions, and the failed operation type.

One failed pull in a unit test does not make that alert fire. A rate requires a time series across samples, and the rule's for interval requires the condition to remain true. The chapter's lab observes an increment and text exposition; it does not run Prometheus's evaluator for ten minutes. Keep that missing observation explicit rather than presenting a fabricated alert screenshot.

Other rules are proxies with potentially surprising names. NodeOffline checks `up{job="orch-agent"} == 0`, meaning Prometheus cannot scrape the agent target. It is not the control plane's authoritative node-offline condition. DatabaseUnavailable similarly checks exporter scrape availability rather than directly testing database transactions. A failed scrape may result from endpoint, credentials, routing, or process failure.

The heartbeat rule checks `increase(heartbeat_success_total{job="orch-agent"}[2m]) == 0` for five minutes. An absent series is not automatically the number zero. A broken scrape path can remove the heartbeat observations while a separate up rule detects target failure. Atlas needs both data availability and behavioral progress signals. Reading one expression literally prevents assuming that it covers every missing-heartbeat situation.

The dashboard's Task State Counts panel sums task_state_changes_total by status. Its Node Status Counts panel counts successful and failed agent scrapes. Its rollout “success” expression subtracts failures from accepted rollout/rollback requests over an hour. These are useful operational proxies if labeled accordingly; none is a direct current-state inventory or a verified count of completed successful deployments.

The API error-rate rule divides 5xx request rate by a denominator clamped to at least one request per second. At low traffic, that differs from the literal fraction of failed requests. A single failing low-volume endpoint can produce a lower displayed ratio than an operator expects from counting requests. Atlas should understand this choice and test any proposed replacement expression against intended low-traffic behavior before changing alert policy.

| Artifact | What it observes | What operators must verify separately |
| --- | --- | --- |
| Docker error counter | Runtime calls returning errors | Daemon state and affected workloads |
| Agent up series | Scrape reachability | Control-plane heartbeat/node status |
| State-change counter | Reports by status | Current task inventory |
| Rollout request minus failure query | Windowed request/failure counters | Terminal deployment outcomes |

Commit [357903ef7cb95a7d6d8fad5f426a48ed48bc0b76](https://github.com/alekpopovic/orch/commit/357903ef7cb95a7d6d8fad5f426a48ed48bc0b76) added alerts; [aa44e586fd79147173588f0bf86763814bd23ec4](https://github.com/alekpopovic/orch/commit/aa44e586fd79147173588f0bf86763814bd23ec4) added the starter dashboard. The source-pinned artifacts remain starting points. Their existence does not establish an Atlas SLO, a live monitoring installation, or tested alert routing.

## Operator Action and the Atlas Signal Lab

The [teaching fixture](../../examples/teaching-extensions/ch38/metrics_contract_test.go) constructs an actual agent registry and wraps an upstream FakeRuntime with the actual instrumentation wrapper. It injects a synthetic pull error, invokes PullImage once, and exposes the registry through an in-process HTTP recorder. No listener, Docker daemon, database, or external monitoring service is involved.

Run it from a disposable module overlay:

```bash
go test ./.book-labs/ch38 -count=1 -v
```

The [recorded execution](../../validation/labs/ch38/failed-pull-emission.json) passed. It observed docker_operations_total with operation pull_image equal to one and docker_operation_errors_total with the same label equal to one. Those are actual collector outputs from an actual wrapped call, with the runtime failure deliberately simulated. The separately captured [upstream metrics tests](../../validation/labs/ch38/metrics-tests.json) exercise collector exposition for additional instruments.

The complete conceptual chain is now inspectable: the wrapped pull returns an error; measure increments the operation/error counters; the agent registry exposes them; the scrape configuration selects the agent endpoint; the alert consumes an error rate; the dashboard groups by operation; the operator investigates image-pull failure causes. Only the first three steps were executed in this chapter's fixture. The remaining steps were inspected as configuration and expected operational procedure.

Atlas should attach an action to each signal before enabling a page. For pull errors, determine whether the image reference exists, credentials are valid, the registry is reachable, and the node has disk capacity. For start errors, inspect port conflicts and engine errors. For a failed agent scrape, verify the endpoint and control-plane heartbeat independently. This prevents a dashboard name from dictating the diagnosis.

Before enabling the bundled rules, Atlas should check target-label alignment and inspect whether each producer is actually wired. A collector that remains zero because its controller never starts can make a rate-based alert appear quiet forever. Add a separate acceptance check for expected producer activity or configuration, and treat that as monitoring coverage evidence rather than manufacturing samples to make the graph look populated.

An alert also needs a recovery observation. Seeing the counter stop increasing is different from seeing a failed task replaced and healthy. Counters retain history after the incident ends, so the rate window must age out. A successful recovery should include workload state and runtime evidence, while the monitoring record shows when the condition stopped holding. The chapter does not invent that timeline from one synthetic increment.

Cleanup removes only test-local state. No host monitoring profile was launched, so there is no Prometheus volume or Grafana instance to delete. Future live evaluation should use owned infrastructure, a bounded duration, synthetic labels, and saved rule/query versions. Retain absent data, mismatched labels, and false positives as findings rather than hiding them behind a screenshot of a green panel.

Atlas's monitoring contract is now sharper: every displayed number has a producer, type, label set, aggregation, and operational interpretation. Gaps such as unwired collectors, proxy panels, and missing current-state gauges remain visible engineering work. That is how observability supports decisions without becoming a collection of reassuring names.

## Exercises

1. Trace docker_operation_errors_total from a failed wrapped call to its collector, scrape target, alert, and dashboard panel. Mark which steps the lab executed.
2. Explain why duplicate accepted failed reports can inflate tasks_failed_total without duplicating task-failed events.
3. Rewrite the description of Task State Counts and Node Status Counts to match their actual queries. Identify the additional source needed for authoritative current counts.
4. Design a live alert acceptance drill for a short pull-failure burst, sustained failure, and absent agent scrape. Explain why a single synthetic counter increment cannot establish alert firing or recovery.

Worked answers are in [Chapter 38 solutions](../solutions/ch38.md), with emission and configuration claims in the [ledger](../../validation/evidence/ch38.json).
