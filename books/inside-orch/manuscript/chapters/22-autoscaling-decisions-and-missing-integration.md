# Chapter 22 - Autoscaling Decisions and Missing Integration

Atlas receives a burst of requests. An operator sees CPU utilization rise and expects the autoscaling fields in its specification to add replicas. The source edition contains a meaningful CPU recommendation controller and a fake metrics provider, yet default orch-server never starts that controller. Understanding the equation is valuable; expecting the default binary to execute it is a composition mistake. The first operational diagnosis is therefore whether there is an active consumer of the policy.

You will calculate scale-up and bounded scale-down recommendations, trace cooldown and rollout exclusion, and identify production metrics and wiring gaps. This chapter follows scheduler arithmetic, rollout ownership and quota accounting. It treats autoscaling as an implemented package with tests, not as an automatically enabled production feature. Atlas provides concrete numbers for reasoning without sending artificial load to the user's host.

## The CPU Recommendation Equation

MetricsProvider.ServiceCPUUtilization receives a service and returns one floating-point utilization value or an error. The controller does not define that value's measurement window by itself. The fake tests use values 100, 50 and 25 as percentages in the same scale as TargetCPUUtilization; supplying a fraction 0.7 where the target is 70 would produce a different and incorrect interpretation. A real provider must establish units before the controller's arithmetic can be trusted.

recommendation first raises current to MinReplicas when necessary. For a positive target, it computes the ceiling of current multiplied by observed utilization divided by the target. It then clamps to the minimum and, when positive, the maximum. The function is deterministic over these inputs; it does not consult Docker, node free capacity, request rate or a percentile distribution.

Unchanged source excerpt — [internal/autoscaler/autoscaler.go:213–228](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L213-L228):

```go
func recommendation(current int, cpuUtilization float64, policy types.AutoscalingPolicy) int {
	if current < policy.MinReplicas {
		current = policy.MinReplicas
	}
	recommended := current
	if policy.TargetCPUUtilization > 0 {
		recommended = int(math.Ceil(float64(current) * cpuUtilization / float64(policy.TargetCPUUtilization)))
	}
	if recommended < policy.MinReplicas {
		recommended = policy.MinReplicas
	}
	if policy.MaxReplicas > 0 && recommended > policy.MaxReplicas {
		recommended = policy.MaxReplicas
	}
	return recommended
}
```

Let Atlas have three replicas, target 60 and observed utilization 90. The raw result is ceil(3×90/60), or ceil 4.5, producing five. With maximum four, the final recommendation is four. That clamp prevents desired replicas exceeding the policy's configured maximum; it does not prove four tasks can fit the cluster or that the new replicas reduce CPU. The scaling path and runtime observations still need their own checks.

For scale-down, take six replicas, observed 20, target 60 and minimum three. The raw result is ceil 2, then the minimum raises it to three. This protects the policy floor rather than a workload-specific availability SLO. If one of the three desired replicas cannot start, the equation does not independently compensate unless the provider's next sample and subsequent controller decisions reflect that situation.

There is also a scale-from-zero boundary. With current zero and MinReplicas zero, multiplication stays zero even if the supplied utilization is positive. This CPU formula has no request-queue activation signal. A service with a positive minimum can acquire a nonzero arithmetic base, but that is different from a complete scale-to-zero/activation mechanism. Do not infer features merely from a lower bound permitting zero elsewhere.

## Bounds, Cooldown, and Rollout Exclusion

reconcileService checks active rollout before obtaining metrics. If GetServiceRollout succeeds with a nonterminal deployment, it records skip_rollout and leaves desired replicas alone. This preserves the deployment's ownership of its count transition. If the rollout lookup returns an error, hasActiveRollout returns false; the source does not treat every lookup failure as a fail-closed exclusion. That is a bounded behavior worth testing in a stronger composition.

Next, effectivePolicy substitutes a one-minute cooldown when the field is nonpositive. The controller compares its current clock with lastScaleAt for this service. A timestamp inside the interval produces skip_cooldown before calling the provider. At exactly the interval boundary, the less-than guard no longer skips. The clock is injected in tests, allowing a reproducible boundary without waiting in real time.

Unchanged source excerpt — [internal/autoscaler/autoscaler.go:148–158](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L148-L158):

```go
	policy := effectivePolicy(service.Spec.Autoscaling)
	if last := c.lastScaleAt[service.ID]; !last.IsZero() && c.now().Sub(last) < policy.Cooldown {
		c.metrics.IncAutoscalerDecision("skip_cooldown")
		c.emit(ctx, service, events.TypeAutoscalerSkipped, types.EventInfo, "autoscaling skipped during cooldown", map[string]string{"reason": "cooldown"})
		return nil
	}
	utilization, err := c.provider.ServiceCPUUtilization(ctx, service)
	if err != nil {
		c.metrics.IncAutoscalerDecision("skip_metrics")
		c.emit(ctx, service, events.TypeAutoscalerSkipped, types.EventWarning, "autoscaling skipped because metrics are unavailable", map[string]string{"reason": "metrics_unavailable"})
		return nil
```

lastScaleAt is a map on Controller. It is updated only after ScaleService succeeds, and a new controller starts with an empty map. A failed scale does not create a completed-action cooldown record. Reconstructing the controller loses the previous cooldown even if the supplied service object still exists. A fresh default server loses much more, because its MemoryService also starts anew; neither behavior supports a durable cooldown claim.

StabilizationWindow is declared and validated in AutoscalingPolicy, but this recommendation controller does not use it. There is no ring of previous recommendations or maximum-over-window downscale calculation here. Parsing and validating the duration establishes a field contract, not an enforced smoothing algorithm. An operator who tunes only that field should not expect this source edition's package to damp oscillation through it.

| Policy concept | Implemented effect | Boundary |
| --- | --- | --- |
| Minimum/maximum | Clamp arithmetic recommendation | Does not reserve node resources |
| Cooldown | Skip decisions after successful scale within controller-local interval | Lost on controller reconstruction |
| Active rollout | Skip when lookup returns nonterminal deployment | Lookup errors treated as no active rollout |
| Stabilization window | Field exists and rejects negative durations | No recommendation-history enforcement |

These distinctions are more useful than saying the controller “supports autoscaling policies” without naming which fields actually change behavior.

## Fake Metrics and Package Tests

FakeMetricsProvider clones its initial map, protects updates with a mutex and supports Set and SetError. ServiceCPUUtilization returns an unavailable error for a service without a value. This makes it appropriate for deterministic decisions and missing-metrics tests; it is not a simulator of scrape lag, per-container utilization or production sampling noise.

TestAutoscalerScalesUpAndDown starts two replicas at target 50, supplies 100 and asserts four. It then supplies 25 after the configured cooldown and asserts two, along with one scale_up and one scale_down decision and two events. TestAutoscalerRespectsCooldown advances an injected clock by thirty seconds within a one-minute interval and keeps the first scaled count. Tests for clamping and active rollout complete the package's explicit contracts.

Provider errors produce skip_metrics and an autoscaler.skipped event, then return nil for that service. Thus a successful RunOnce can mean “metrics unavailable; no scale attempted.” Developers should not equate a nil return with convergence. Operators need decision labels/events and the provider's actual sample freshness to explain why desired replicas did not change.

RunOnce also skips disabled autoscaling and non-active services. A service error during reconciliation increments the controller error metric and returns from the pass, leaving later services for another pass. The Run loop logs errors and repeats at its cadence. Ordering and failure isolation therefore matter when extending the package to a large catalogue; the current implementation is not a proof that every service was evaluated during a successful or failed interval.

The source updates desired replicas through the same ScaleService seam used by API/CLI operations, preserving an important place for admission, maintenance and quota decisions. It does not bypass those rules by creating containers itself. A later integration must therefore account for a valid recommendation being rejected by the control plane, and must observe whether the approved desired count actually becomes available.

## The Provider and Server Wiring Gaps

Searching the default composition root finds scheduler, rollout, node monitoring, GitOps and cron loops, but no autoscaler.NewController invocation. No production MetricsProvider is selected there. The presence of autoscaler metric declarations in the shared metrics package cannot activate a controller: declarations are storage for observations, not a scheduler of work.

A correct production provider would need to define utilization units, aggregation across task versions, stale or missing samples, authentication to its metrics source and bounded query latency. Consider a rollout containing old and new images: averaging whichever containers happen to appear can create a recommendation based on an incoherent population. A provider contract must state whether it measures current desired task identity and how it handles newly started replicas with no sample.

Then composition must select the provider, inject metrics/events, establish namespace coverage and supervise the controller. Leadership and durable cooldown are additional decisions, not automatic consequences of constructing one goroutine. A separately tested teaching extension could demonstrate a Prometheus adapter or a local runner, but it must remain outside immutable evidence and cannot be described as the pinned server's behavior.

The Atlas failure timeline makes the gap concrete. At timeA, the YAML validates. At time B, the service is created with autoscaling enabled. At time C, CPU rises. The default binary has no autoscaler consumer, so no automatic replica change follows from that policy. This outcome is different from a running controller skipping stale metrics or cooldown. Diagnose the missing caller before searching for a bug in the recommendation equation.

A review should also keep demand and enforcement separate. Desired replica arithmetic can be sound while ordinary MemoryService service placement bypasses the planner's resource fits, and the active agent omits CPU/memory limit propagation. Autoscaling therefore cannot be used as evidence that node capacity or Docker cgroups are protected. Revisit those earlier field paths when evaluating a stronger composition.

## Atlas Lab: Change Samples, Not Host Load

Use the disposable pinned source copy and Go 1.25. Existing package tests need neither Docker nor PostgreSQL. Their injected clock and FakeMetricsProvider exercise decisions without burning CPU on the actual machine.

```bash
go test ./internal/autoscaler -run 'TestAutoscaler(ScalesUpAndDown|RespectsCooldown|ClampsMaxAndMinReplicas|SkipsActiveRollout)$' -count=1 -v
```

The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) includes the autoscaler decisions with caching disabled. The injected provider and clock establish deterministic package behavior; the default server still does not start this controller. For a separate teaching fixture, initialize Atlas with three replicas, min two, max four and target 60. Supply 90, check desired four, then supply 15 during cooldown and verify it remains four. Advance the injected clock beyond cooldown and check the bounded reduction. This is a package composition, explicitly different from deploying policy through default server startup.

Add a missing-sample case and observe skip_metrics rather than inferring a failed process. Reconstruct the controller over the same service and show that lastScaleAt is empty; if you propose durable cooldown, test the different implementation independently. Compare a positive StabilizationWindow with zero using otherwise identical inputs and explain why this baseline makes no history-based difference.

Abort if the exercise starts a real stress workload, targets a non-lab service or silently patches startup to hide the missing integration. Cleanup discards only fake objects and owned temporary files. A later real provider experiment needs sample timestamps and explicit source credentials kept outside logs, plus a bounded workload and cluster scope. Passing the deterministic equation tests cannot establish production load handling or automatic scaling in a binary that never starts the controller.

## Exercises

1. Compute Atlas's recommendation for three replicas, observed 90, target 60, minimum two and maximum four. Identify which step produces each intermediate value.
2. Explain why reconstructing a controller during cooldown can permit another decision even when the service count persists in a fixture.
3. What do a nonzero StabilizationWindow and a successful RunOnce prove about actual stabilization and metrics availability?
4. Draft an acceptance boundary for a production provider and explain why adding autoscaling YAML to the default server cannot satisfy it.

[Worked answers](../solutions/ch22.md) preserve the distinction between calculation, policy enforcement, observation and executable composition.

## Development history and source references

Original development prompts 54, 55 supply the requested scope. The inspected implementation history includes [cf4766ccc7ae](https://github.com/alekpopovic/orch/commit/cf4766ccc7ae05dffda1337d9fe89a7bf33bc9e2), [b575252d6c5f](https://github.com/alekpopovic/orch/commit/b575252d6c5ff0918439e2f209af9d9695eebbb6). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/autoscaler/autoscaler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L1-L272)
- [internal/autoscaler/autoscaler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler_test.go#L1-L217)
- [docs/AUTOSCALING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AUTOSCALING.md#L1-L57)
- [docs/AUTOSCALING_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AUTOSCALING_DESIGN.md#L1-L223)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L1-L304)
