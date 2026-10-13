# Chapter 37 - Failure Injection and Recovery Evidence

Atlas has a service with one healthy replica and an upgrade waiting to roll out. Before approving the change, an operator asks what happens if the agent disappears after starting the replacement. “The chaos tests pass” is not yet an answer. The test might replay a status report, reconstruct a controller around retained memory, or actually terminate a process. Each experiment crosses a different failure boundary.

This chapter teaches you to choose an invariant before injecting a fault, identify the state retained by a simulation, and build a recovery timeline from observed events. You will inspect the upstream chaos cases, run selected deterministic failures, and compare them with the actual fresh-server/Docker experiment. The Atlas outcome is a small failure dossier whose conclusions remain proportional to the fault that was injected.

## Define the Invariant Before the Fault

A useful drill begins with a specific statement that should remain true. For an agent retry, the same task should not acquire a second managed container. For a failed scheduler write, no assignment event should claim an assignment that never persisted. For service deletion during rollout, desired cleanup must take precedence over new workload progression. These are separate invariants with different observation points.

The upstream [chaos suite starts with repeated running reports against one memory control plane](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L19-L39). That case is named “agent restarts during task start.” Its actual injected condition is a repeated status report using the same container ID. It checks that one running task remains. No agent process is killed, no engine object is inspected, and no volatile agent state is reconstructed. The test is useful for report idempotency within its stated scope.

The case named “server restarts during rollout” likewise retains the same control-plane object. It constructs a rollout controller and runs one pass against existing service and deployment records. This tests recomputation from retained state, not persistence across a fresh server process. The [relevant code contains no new MemoryService after the rollout begins](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L41-L61). Atlas must not turn the subtest's name into a stronger durability claim.

This precision is an operational advantage. If a later incident loses service records after a process restart, the team can immediately see that the controller-reconstruction test never covered that boundary. A misleading resilience label would instead send investigators looking for a regression in a guarantee that did not exist. Fault names should describe both the failed component and the retained state.

Commit [fe385251b7a2051b10af3dd6caaad8bb4821fa21](https://github.com/alekpopovic/orch/commit/fe385251b7a2051b10af3dd6caaad8bb4821fa21) introduced these deterministic cases. Earlier [66cfb7049fc1fbceeec9e36a7067febe8cbab698](https://github.com/alekpopovic/orch/commit/66cfb7049fc1fbceeec9e36a7067febe8cbab698) hardened agent recovery and failure reporting. Their changed hunks explain how recovery logic evolved; the present chapter's executed records establish which selected tests ran now.

## Runtime Failure, Node Loss, and Partitions

A failed inspection is not equivalent to a missing container. The agent's unavailable-runtime test injects errors into both inspect and managed-container listing, then asserts that no new status reports were made and no create call occurred. The desired invariant is conservative behavior while reality cannot be observed. Creating a replacement immediately could duplicate a workload whose original container is still running.

```go
	if err := runner.reconcileAssignedTasks(context.Background(), nodeID); err != errDockerUnavailable {
		t.Fatalf("expected docker unavailable error, got %v", err)
	}
	wantRuntimeCalls := []string{"inspect:container-1", "list", "list"}
	if !equalStrings(runtime.OperationStrings(), wantRuntimeCalls) {
		t.Fatalf("expected runtime calls %#v, got %#v", wantRuntimeCalls, runtime.OperationStrings())
	}
	if len(client.statuses) != 0 {
		t.Fatalf("expected no status reports while Docker availability is unknown, got %#v", client.statuses)
	}
```

Exact source: [internal/agent/agent_test.go:198–207](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent_test.go#L198-L207).

The [fake options permit pull, create, start, inspect, and list failures](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go#L70-L98) to be chosen independently. This makes the injection point explicit. A pull failure occurs before a new container exists; a start failure may leave a created container; an inspection failure leaves existence uncertain. Atlas should select the option that represents the intended failure window rather than use a generic error everywhere.

The broad chaos suite's “docker runtime fails to start container” case reports a failed status with a reason directly to the control plane. It checks storage and event behavior after that report. It does not execute the Docker adapter's StartContainer method. Selected lower-level agent/runtime tests provide the missing call-path evidence. Combining layers is useful only when the report identifies which layer supplied each observation.

Node loss introduces a harder distinction between authority and reality. The server can mark a node offline and remove a stateless task from its active assignment set. The isolated host may still run its old container. Replacement on another ready node can temporarily coexist with that old workload. The return path can eventually remove the stale managed container, but eventual cleanup does not establish zero overlap during a partition.

The [returned-node test supplies no active assignment and a managed stale container](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent_test.go#L446-L472). It asserts list, stop, remove, and a removed report. This proves the fake-runtime cleanup behavior for the modeled task on return. It does not provide network fencing, volume fencing, or a proof that two replicas never served requests simultaneously. Stateful recovery requires stronger ownership rules and operator decisions beyond that fixture.

Ownership labels are part of safe cleanup. The agent's separate non-managed-container test keeps a foreign object intact. Atlas drills should likewise create a captured object with exact test identity and check cleanup against that identifier. Broad commands deleting all nginx containers or all objects with a partial name are inappropriate on a shared host. Cleanup is an assertion about ownership, not an afterthought after the interesting fault.

## Recovery Timelines and Residual Work

A recovery timeline has at least four boundaries: the fault injection, detection, corrective intent, and observed completion. These may be in different components. A server heartbeat timeout changes its view of a node; the agent on that node may know nothing about that change until connectivity returns. A task marked removed in API state is not automatically an engine observation that its container has stopped.

The suite's scheduler-write case injects an AssignTask error and checks the event slice remains empty. That [assertion prevents a false assignment history](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L139-L148). It does not emulate a PostgreSQL transaction rollback, database failover, or ambiguous commit response. The fake store returns a deliberate error before the successful-assignment path. Actual concurrent claim and transaction behavior need separate database tests.

Deletion during rollout checks that the service reaches deleting or deleted and records deletion-started history. This is an intent and control-plane state check. It does not assert every container is already gone at that point. Atlas should distinguish accepted deletion, task cleanup directives, agent removal, and terminal service state. The residual work between those stages is exactly what an interrupted cleanup drill should inspect.

For the executed deterministic lab, use a disposable locked source copy and run:

```bash
go test ./internal/e2e ./internal/agent ./internal/docker \
  -run 'Test(ChaosScenarios|ReconcileAssignedTaskDoesNotRecreateWhenDockerUnavailable|ReturnedNodeRemovesNodeLostUnassignedContainer|FakeRuntimeFailureInjection)$' \
  -count=1 -v
```

From the disposable pinned module, run `go test ./internal/e2e ./internal/agent ./internal/docker -run 'Test(ChaosScenarios|ReconcileAssignedTaskDoesNotRecreateWhenDockerUnavailable|ReturnedNodeRemovesNodeLostUnassignedContainer|FakeRuntimeFailureInjection)$' -count=1 -v` with live integration variables cleared. The [actual fault-test record](../../validation/labs/ch37/fault-tests.json) passed all eight chaos subcases and the selected agent/fake assertions. It used no Docker daemon, database, real node partition, or killed application process. Its zero-looking printed test durations are rounded framework output, not measured recovery objectives. No production recovery-time claim follows from those lines.

The independent [combined restart experiment](../../validation/labs/ch06/combined-restart.json) crossed a real process boundary. It manually created a cached nginx container with no published ports, associated its exact ID with a task through an authenticated report, stopped the first server binary, and started a fresh second server. The second process had empty service/task/node lists while the same captured container remained running. The owned container was then removed and absence verified.

That experiment is intentionally scoped. The agent Runner did not create or adopt the container; the harness supplied the association. Its purpose was to observe the relationship between lost memory state and a surviving engine process. It cannot be cited as automatic agent recovery or PostgreSQL restoration. It does establish that restarting the default server and waiting for healthy HTTP does not restore the earlier control-plane records.

| Drill | Fault or modeled condition | Evidence boundary |
| --- | --- | --- |
| Repeated report | Same running report twice | One memory task remains |
| Controller reconstruction | New rollout controller, retained store | Progress recomputed from existing records |
| Runtime unavailable | Fake inspect/list errors | No speculative replacement or status |
| Returned node | Stale managed fake object, no assignment | Stop/remove cleanup on reconciliation |
| Fresh server | Actual first process stopped, second started | Memory state lost while captured Docker object survives |

The table is a failure map, not a ranking of test quality. Deterministic fixtures make narrow invariants cheap and repeatable. Process experiments expose ownership and persistence boundaries. Real runtime experiments expose kernel and daemon behavior. Atlas needs all relevant kinds without pretending that one can replace the others.

## The Scope of Fake Chaos

A chaos experiment should preserve a useful result even when recovery fails. Record initial IDs, the exact injected condition, expected invariant, actual observations, error path, and cleanup. Do not delete the failed run because a later harness revision passes. The original failure can reveal a misunderstanding of the test or a real implementation boundary. A corrected run should identify precisely what changed.

Atlas's prior real-Docker flow illustrates this discipline. A first log-check guard inspected the wrong task association and failed. The corrected harness scoped log retrieval to the captured task and passed deploy, scale, logs, and deletion. Both records were retained. Describing only “Docker passed” would hide the harness correction and prevent a reader from understanding which behavior was actually tested.

A safe escalation from fake to live fault should add one uncontrolled boundary at a time. Start with a deliberately failed runtime call and an exact operation-history assertion. Next use an owned disposable engine object with no published host ports. Then, if authorized and supported, test a process or network failure while retaining captured identities. A live shared production node is not a convenient substitute for missing disposable infrastructure.

Recovery acceptance also needs a stopping rule. If the desired state cannot be recovered because the default control plane is empty, repeatedly restarting the same binary will not create durable history. Stop the drill, preserve evidence, clean owned objects, and record the architectural prerequisite. For Atlas, that prerequisite is durable server composition, not a longer polling timeout.

A drill owner should also record who decides that recovery has completed. API task state, agent acknowledgement, and engine inspection are distinct witnesses; none should silently substitute for another. When they disagree, retain all three observations and investigate the interval rather than selecting the most reassuring result.

The final reliability statement should be concrete: selected fake failure paths preserve their asserted state/event rules; the actual fresh-server experiment loses memory state; returned-node cleanup is eventual and does not fence a partitioned workload. These findings guide engineering priorities without inventing production guarantees. A small honest failure dossier is more useful than a broad resilience label whose test boundaries nobody can explain.

## Exercises

1. Rename two upstream chaos cases so their titles state the actual modeled action and retained state. Explain which stronger claim the original names might invite.
2. Run the selected fault tests and identify the operation history proving no speculative container create during runtime unavailability.
3. Draw a written timeline for node partition, stateless replacement, and returned-node cleanup. Identify the interval in which an old container may remain live.
4. Compare controller reconstruction with the combined fresh-server experiment. Define the evidence required before claiming durable rollout recovery and a cleanup plan that touches only captured resources.

Worked answers are in [Chapter 37 solutions](../solutions/ch37.md). The [claim ledger](../../validation/evidence/ch37.json) distinguishes source assertions, simulated faults, and actual process observations.
