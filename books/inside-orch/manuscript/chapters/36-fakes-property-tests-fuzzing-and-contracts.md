# Chapter 36 - Fakes, Property Tests, Fuzzing, and Contracts

Atlas's test suite is green, yet the team has already observed a resource request disappear between its API and Docker. The lesson is not that tests are useless. It is that a passing test answers the question encoded by its fixture and assertions. A fake runtime can validate reconciliation order while overlooking a field that nobody asserted. A parser fuzz target can survive malformed input while accepting a value with the wrong meaning.

This chapter teaches you to read tests as executable contracts. You will separate fake behavior from runtime behavior, reproduce seeded scheduler properties, run a bounded fuzz campaign against an actual target, and choose an independent assertion for an orchestration boundary. The Atlas result is an evidence-backed testing plan that records what passed, what was skipped, and which important claims remain outside each test's scope.

## Fakes as Executable Specifications

The runtime fake implements the same narrow interface used by the agent. It keeps container state, operation history, created specifications, and injectable errors under a mutex. This makes it useful for assertions about sequencing, repeated work, and concurrent access. The [creation implementation deduplicates by task identity](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go#L135-L166), while separate methods model start, stop, inspect, and removal. Those choices define the simulation the tests inhabit.

A fake is not automatically a faithful engine. It does not allocate Linux namespaces, enforce cgroups, pull image layers, bind real host ports, or reproduce every Docker daemon error. Tests using it should say which fake transitions are relied upon. If Atlas needs proof of a memory limit, inspect the ContainerSpec supplied to the fake and then separately observe a real engine's configured limit. A successful fake start is insufficient.

The upstream [fake-runtime tests check recorded operations and concurrent same-task creation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake_test.go#L11-L83). The repeated identifier assertion is an idempotency contract. The concurrent case tests mutex-protected behavior within one fake instance. Neither proves deduplication across independent engine adapters after process failure. That stronger claim needs stable managed labels, engine inspection, and an actual uncertainty/retry scenario.

The end-to-end test uses a real handler, client, agent Runner, and fake runtime. Its [default entry point selects the fake explicitly](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/orchestrator_test.go#L29-L42), while real Docker is separately gated by ORCH_E2E_DOCKER. It exercises deploy, logs, scale, and deletion through multiple components. Calling it an integration test is justified by those relationships; calling it a live container deployment would be false when the selected runtime is fake.

Contracts also include the fixture's assumptions. The end-to-end log assertion looks for a fake-container start line. A real nginx image does not necessarily emit that text. Setting a Docker flag without reading the shared assertion can therefore fail for a harness reason rather than a workload failure. Preserve the failure and distinguish an adapted real-runtime harness from the original test. Do not silently weaken assertions and retain the old coverage label.

Commit [c69f9ffa830284692aabf9e65ab9eb1f79d3a114](https://github.com/alekpopovic/orch/commit/c69f9ffa830284692aabf9e65ab9eb1f79d3a114) introduced the fake boundary; [903ece1ea30c5a0f4902b3f2e9cb475fdea41fdc](https://github.com/alekpopovic/orch/commit/903ece1ea30c5a0f4902b3f2e9cb475fdea41fdc) added the MVP flow. Read their changed code alongside current assertions. A historical test name is evidence of intent and implementation history, not proof that it ran in the present environment.

## Seeded Scheduler Properties

Example-based tests pick a specific placement and compare its result. Property tests generate many inputs and assert invariants that must hold across them. The scheduler's [randomized invariant test uses five fixed seeds](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go#L11-L21): 1, 7, 42, 99, and 20260821. Each subtest constructs nodes with varied readiness, labels, capacity, service requests, and occasional published ports. Fixed seeds make a failed state reproducible.

The same input is planned twice and compared for determinism. Assignments are then checked for unique task IDs, ready nodes, matching placement labels, aggregate CPU/memory bounds, and per-node port uniqueness. This is stronger than expecting a particular distribution from one hand-picked cluster. It still covers a finite generated domain, and it exercises Plan rather than every active assignment path in the server.

```go
			first := Plan(input)
			second := Plan(input)
			if !reflect.DeepEqual(first, second) {
				t.Fatalf("seed %d: nondeterministic", seed)
			}
			nodeByID := map[types.NodeID]types.Node{}
```

Exact source: [internal/scheduler/property_test.go:46–51](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go#L46-L51).

The failure messages retain the seed, allowing Atlas to rerun the precise subtest. Keep the seed and the source revision together: changing input-generation code can produce a different cluster from the same integer. For a durable regression, preserve the minimized concrete input as well as the seed. A random number is a reproducibility aid, not a permanent specification independent of the generator.

Coverage also depends on input shape. The property fixture starts with generated pending tasks and no occupied-node task inventory. It does not thereby cover every preexisting allocation, reservation, or concurrent store race. Atomic assignment remains a different layer. A planner can propose a legal assignment and still lose its claim when another scheduler commits first. That conflict should trigger recomputation, not be treated as a planner-property violation.

Atlas's independent review question is whether the invariant matches the operational claim. Capacity safety should sum requested resources by selected node, not compare the output against another copy of the planner's scoring function. Port safety should inspect collisions in the resulting assignments and occupied ports, not merely assert that a helper returned true. A test that repeats implementation logic can preserve the same mistake on both sides.

The [seeded execution record](../../validation/labs/ch36/seeded-properties.json) passed all five generated subtests, concurrent fake creation, and selected repeated-reconciliation tests. These were actual uncached executions. They used the locked disposable source and no Docker or database. Package and subtest pass lines are retained separately so their count is not inflated into a claim about unique production scenarios.

## Fuzz Inputs and Minimal Reproductions

Fuzzing explores malformed and unexpected byte sequences using coverage feedback. The actual [port target is named FuzzPortSpec](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/fuzz_test.go#L11-L16). The testing document instead gives an example using FuzzParsePortSpec. Atlas must resolve that name against source before copying the command. This small documentation conflict is recorded rather than repaired inside immutable evidence.

The port target seeds ordinary mappings, UDP, zero, an out-of-range number, and arbitrary text. Its callback ignores both parsed values and returned errors. The resulting property is primarily that the parser does not panic on supplied inputs. It does not assert that every accepted port is semantically safe or that rejected ports receive an ideal error message. Those require explicit table or property assertions over the result.

The same distinction applies to service YAML and resource quantities. A parser may return an error for malformed input and correctly satisfy a panic-resistance target. Conversely, it may accept a surprising value without violating that target. Atlas should pair fuzzing with meaningful semantic checks such as bounds, round trips under a defined canonical form, or rejection of a known unsafe syntax. Do not describe ignored return values as comprehensive validation coverage.

The bounded experiment used one worker and a two-second campaign:

```bash
go test ./pkg/types -run '^$' -fuzz '^FuzzPortSpec$' -fuzztime 2s -parallel 1
```

The [actual fuzz record](../../validation/labs/ch36/bounded-port-fuzz.json) passed after 42,919 executions, with five baseline seeds and sixty-three newly interesting inputs reported. These are observed figures for this run. “Interesting” means useful coverage feedback, not a confirmed bug or a distinct real-world port configuration. No crash was discovered, so there is no invented minimized failing input to present.

The command deliberately excludes ordinary tests, selects one exact fuzz target, bounds duration, and limits parallelism. This keeps the exercise predictable on the shared machine. A two-second campaign is a smoke observation, not an argument that all possible inputs are safe. The command record's toolchain, source pin, and UTC interval make it possible to repeat the experiment under a larger approved budget later.

If a future campaign fails, preserve its original record before editing anything. Reproduce the generated input with the exact target, inspect whether the failure comes from the parser or the harness, and minimize it without losing the invariant. Then add a stable regression case in a separate teaching extension or an authorized application change. The book's immutable snapshot must remain unchanged, even when the discovered behavior is inconvenient.

## Contracts Across Boundaries

Atlas's resource-loss incident suggests a test that belongs between two existing layers. The API accepts requested CPU/memory, the service stores it, the agent receives a task DTO, and Docker receives a ContainerSpec. Checking only the service record cannot prove that the runtime received the fields. Checking only the engine adapter with a manually complete ContainerSpec cannot prove that the normal agent path supplied them.

The observed real-Docker boundary experiment did both and found different outcomes: direct adapter limits were present while the ordinary handler/Runner path yielded zero runtime limits. This is a contract failure in propagation, not evidence that Docker cannot enforce the limits. A good regression would assert the same requested values at each handoff and then inspect the actual engine configuration. Until such an upstream fix exists, the book preserves the limitation.

Repeated convergence deserves similar care. The [reconciler test reruns reconciliation and checks duplicate work](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler_test.go#L124-L160), but process restart requires identifying which state survives. Recreating a controller around the same store tests recomputation against retained state. Creating a fresh MemoryService tests a different boundary. Atlas should name both the restarted component and its retained dependencies in every result.

| Test form | Useful evidence | Boundary to retain |
| --- | --- | --- |
| Fake adapter contract | Call order, supplied fields, replay behavior | No kernel/container enforcement |
| Seeded planner property | Finite generated invariants and determinism | Not concurrent persistence |
| Parser fuzz target | Bounded exploration of callback assertions | Ignored results are not semantic proof |
| Cross-layer acceptance | Values and effects across real handoffs | Scope depends on selected adapters |

The full baseline suite and race detector are separate captured evidence. Their explicit Docker/PostgreSQL skips remain skips. A passing ungated suite does not certify the gated paths, and a clean race run detects only races reached under its execution. Combining those records with targeted contracts gives a more honest confidence statement than counting green checks.

For the lab, begin with a disposable locked copy and clear live integration variables. Run `go test ./internal/scheduler -run '^TestSchedulerRandomizedInvariants$' -count=1 -v` for all five seeded cases, then run the bounded fuzz target. Observe subtest names and rejected/accepted outcomes rather than expecting an invented terminal transcript. No host containers or databases are created. Fuzz corpus caches belong to the configured disposable cache; retain useful failures explicitly before deleting owned temporary files.

Atlas should now ask a sharper question in review: which invariant would fail if this boundary dropped, duplicated, delayed, or renamed a value? That question turns fakes, properties, and fuzzing into complementary tools. It also prevents a passing simulation from becoming an unsupported claim about durable recovery, kernel isolation, or production capacity.

## Exercises

1. Identify one fake behavior that supports a useful agent test and one real Docker behavior it cannot establish.
2. Run the seed_42 scheduler subtest and explain why the seed must be recorded with the generator revision. Add a proposed occupied-port input without duplicating the scoring algorithm as the oracle.
3. Run the bounded port fuzz command. Explain exactly which failure its callback can detect and why newly interesting inputs are not bug counts.
4. Design a resource-propagation acceptance test across API, agent DTO, ContainerSpec, and engine inspection. Explain why testing only the direct adapter would miss the observed gap.

Worked answers are in [Chapter 36 solutions](../solutions/ch36.md), with scoped claims in the [evidence ledger](../../validation/evidence/ch36.json).
