# Chapter 39 - Performance and Scale Tests That Say What They Measure

Atlas wants to know whether the system can manage a thousand services. The repository contains a thousand-service test, but the number alone is not a capacity answer. A simulated running report is cheaper than pulling an image, starting a container, performing a healthcheck, or committing a database transaction. The first task is to identify what work is actually inside the measured interval.

This chapter teaches you to read benchmark inputs, preserve repeated measurements, distinguish fake-agent convergence from runtime startup, and use profiling without exposing an administrative endpoint. Atlas's result is a bounded benchmark record, a small simulated-load observation, and a scoped interpretation of the optional scale test. None is presented as a production throughput promise.

## Fake-Agent Load and Real Runtime Capacity

The load tool constructs MemoryService, creates fake nodes, creates services, and reports assigned tasks running through direct control-plane calls. It does not start an HTTP server or an agent Runner. Its [initial convergence loop includes service creation and synthetic running reports](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go#L89-L121). The container identifiers are strings prefixed with fake, not observed Docker objects.

The simulation then runs until a duration deadline, occasionally changes node heartbeat state, and probabilistically reports running tasks failed. It sleeps one hundred milliseconds between ticks. SchedulerIterations counts simulation ticks, not invocations of the scheduler's Plan function. ReconciliationIterations counts initial service creations. Naming a summary field does not change the operations performed beneath it.

The configured duration begins after initial convergence, so total command runtime includes setup plus the requested simulation interval and any final work. Failure rate is a probability per eligible running task per tick, not failures per second or a measured production incident rate. Atlas should not compare runs with different tick counts as if they experienced identical failure exposure.

A fixed seed constrains pseudorandom choices, but it does not make elapsed timing deterministic. Generated object IDs, iteration order, scheduler activity in other experiments, and host contention can still affect the result. Preserve the seed alongside the exact source and flags. For a regression about a particular workload identity, save the concrete fixture rather than expecting one integer to reconstruct every external circumstance.

The actual [bounded fake-load run](../../validation/labs/ch39/bounded-fake-load.json) used ten nodes, one hundred services, three replicas, failure probability 0.02, one second, and seed 42. It reported 323 task records, 260 running and 63 failed, with zero reported scheduler/reconciler errors, ten simulation ticks, and one hundred reconciliation iterations. These are observed output values from that run, not an expected transcript for every repeat.

Its average initial per-service convergence was 84.619 microseconds, and total initial convergence was 8.758617 milliseconds. Those intervals cover memory operations and synthetic reports. They do not include image transfer, container initialization, application readiness, persistent transactions, or network hops. The coexistence of failed historical tasks and replacement task records also means total task records should not be equated with desired live replicas.

## Benchmark Inputs and Repeatable Results

The scheduler benchmark is more narrowly defined. It prepares one hundred ready nodes, each with eight CPU cores represented as eight thousand millicores and sixteen GiB allocatable memory. It prepares one thousand pending tasks, each requesting one hundred millicores and sixty-four MiB, then repeatedly calls Plan on the same input. Setup occurs before ResetTimer.

```go
	input := PlanInput{PendingTasks: tasks, Nodes: nodes, Services: services}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = Plan(input)
	}
}
```

Exact source: [internal/scheduler/benchmark_test.go:21–26](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/benchmark_test.go#L21-L26).

This isolates planner computation and allocation behavior. The repeated input has no existing running-task inventory, no placement labels, and no published ports. A change that improves this benchmark can still regress a label-heavy or reservation-heavy case. Atlas should preserve representative input families rather than use one attractive number as the universal scheduler cost.

The actual bounded benchmark command selected only scheduler scoring and service/task list handlers, used a one-hundred-millisecond benchmark target, repeated three times, and set the benchmark CPU count to two. The [record](../../validation/labs/ch39/bounded-benchmarks.json) pins Go 1.25.0, Linux amd64, source SHA, UTC times, command flags, and raw output. The host identified its processor as AMD Ryzen 5 5500. Other concurrent work on this shared host was not controlled.

For scheduler scoring, the three measured results were:

| Sample | Iterations | Time per Plan call | Allocated bytes per call | Allocations per call |
| --- | --- | --- | --- | --- |
| 1 | 9 | 11,991,457 ns | 718,664 | 630 |
| 2 | 9 | 12,012,169 ns | 718,664 | 630 |
| 3 | 9 | 12,050,878 ns | 718,664 | 630 |

The median is 12,012,169 nanoseconds per operation, with the observed range shown by the samples. Three short samples do not justify a confidence interval, a tail-latency claim, or a host-independent benchmark. The [summary artifact](../../validation/labs/ch39/scheduler-summary.json) derives those figures mechanically from the raw scheduler lines and records its limitations. It intentionally does not attribute interleaved API logging lines to guessed benchmark names.

The HTTP list benchmarks use an in-process recorder and a prepared memory control plane containing one thousand services. They include handler processing and JSON output, but not a TCP exchange, TLS, a reverse proxy, or database reads. Default logging also contributes observable work. Comparing these with a network client benchmark would mix different costs unless the experimental design explicitly accounts for them.

Commit [7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d) added these benchmark and scale artifacts in a broader operations batch. Earlier [7fcdaf5877145b77bb484b2bc7cabae8eb75acab](https://github.com/alekpopovic/orch/commit/7fcdaf5877145b77bb484b2bc7cabae8eb75acab) added the load tool. Their commit boundaries do not supply a performance history by themselves; measurements require comparable recorded runs.

## Profiles and the Debug Boundary

A profile helps identify where measured work occurs; it does not create a trustworthy workload definition. Atlas can capture a scheduler CPU profile from the benchmark without opening a server listener. Use an owned output directory and retain the matching test binary so symbol interpretation corresponds to the captured program. A very short profile provides few samples and should be treated as a diagnostic sketch.

The chapter's [profile capture](../../validation/labs/ch39/scheduler-profile-absolute.json) succeeded against the same deterministic planner fixture. The downloaded toolchain lacked a prebuilt pprof executable, so the ordinary go tool invocation failed and that failure remains recorded. A source-built tool fallback is separately recorded; it must not be confused with a successful invocation of a missing binary.

The source-built fallback actually succeeded, as preserved in profile-top-source-tool.json. It reported a 301.20-millisecond capture with 120 milliseconds of CPU samples; map lookup and comparison work appeared in the short top listing. That observation suggests where to investigate the planner fixture, but the sampling interval is too small to declare a stable optimization priority. Keep the profile and matching binary identities together, and repeat a longer bounded capture before making a substantial change based on those percentages.

The application also offers an optional debug listener. The [debug handler registers pprof routes only when enabled](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/debug.go#L8-L20), and main starts it on a separate configured address. The default address is loopback. The handler itself has no authentication middleware, so a configuration change exposing it on a public interface changes the security boundary. Being separate from the public listener is useful but does not make every configured address safe.

Profiles can contain operational paths, command-line material, and memory-related data. For a real server procedure, keep access on an approved management path, bound the capture, and handle output as sensitive. This chapter did not enable that listener or collect a live service profile. Its fixture contains synthetic service/task identifiers and no production credentials.

The failure window for performance investigation is often the investigation itself. Enabling an unrestricted debug endpoint during an incident can expose information or add load. Atlas should prepare a reviewed profiling procedure before an outage and test that disabled public routes remain unavailable. Do not turn an urgent performance question into an unreviewed change to network access.

## Interpreting a Thousand-Service Test

The optional [scale test is behind the scale build tag](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/scale_test.go#L1-L19). It runs fifty fake nodes, one thousand services, three replicas, a one-percent failure probability, one second of simulation, and seed 42. Its acceptance checks at least three thousand task records and exactly one thousand initial reconciliation iterations. It does not assert that all desired replicas are healthy at the end.

The [actual tagged execution](../../validation/labs/ch39/thousand-service-scale.json) passed. This establishes that the specified fake-memory scenario completed and met its two assertions in this environment. It does not establish one thousand real containers, PostgreSQL throughput, a production admission rate, or durable recovery under load. A database process running beside it would not alter that scope because the command never uses it as active state.

For Atlas's lab, use the disposable copy and the exact bounded commands in the records. Keep ordinary tests excluded from the benchmark command and separate the tagged scale invocation. Observe output and sample variation rather than rewriting expected numbers into a passing assertion. No host containers, published ports, or databases are created by these commands.

A production-shaped follow-up needs a different design. Define the number of services, replicas, images, image-cache state, update rate, placement constraints, event retention, database schema, network path, and readiness criterion. Measure end-to-end acceptance and convergence separately from planner CPU. Include errors, pending work, recovery after injected faults, and cleanup duration. Those dimensions are proposed requirements, not missing columns that can be filled by extrapolating this benchmark.

When comparing a candidate optimization, keep the old and new fixture definitions identical, run repeated samples under the same toolchain and CPU setting, and preserve rejected alternatives. A faster result obtained by removing capacity checks would violate correctness rather than improve it. The comparison must include the existing property and constraint tests, while the benchmark records the cost of preserving those semantics. Report both the time change and allocation change, and distinguish measured variation from a repeated directional result.

Resource cost also grows outside the hot function. Event and task history can expand while replicas remain constant; list endpoints may serialize large responses; retained failures can consume memory; agents and container logs add independent load. Atlas should observe steady state and bounded history as well as initial creation. The small chapter experiment intentionally avoids pretending that a brief creation burst covers those longer timelines.

The final performance statement is therefore specific: a pinned pure planner fixture produced three short observed samples; a bounded fake-memory load completed; an optional thousand-service simulation met its limited acceptance checks. These results help locate regressions and guide further experiments. They do not set a safe production cluster limit, and Atlas should retain that distinction in release notes and capacity decisions.

## Exercises

1. Identify which operations are included in average_convergence_time and which real runtime costs are absent. Explain the actual meanings of SchedulerIterations and ReconciliationIterations.
2. Reproduce the scheduler benchmark with the recorded flags. Compare the sample range without inferring a production capacity or statistical confidence interval from three short runs.
3. Explain why a debug listener bound to a public address remains dangerous even though pprof is absent from the public API handler.
4. Design a production-shaped thousand-service acceptance experiment. Include authoritative readiness, durable state, runtime work, retained history, failures, and scoped cleanup rather than extrapolating the fake scenario.

Worked answers are in [Chapter 39 solutions](../solutions/ch39.md); classifications and measurement limits are in the [claim ledger](../../validation/evidence/ch39.json).
