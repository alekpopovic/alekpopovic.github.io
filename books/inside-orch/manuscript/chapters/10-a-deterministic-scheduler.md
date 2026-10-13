# Chapter 10 - A Deterministic Scheduler

Two Atlas API replicas need somewhere to run. A casual placement rule might select the first available node and hope Docker accepts the request. A deterministic scheduler instead makes its decision from an explicit snapshot, applies named constraints and returns a result that can be calculated and tested. Its value comes from knowing both what the algorithm guarantees and which live requests actually pass through it.

This chapter assumes resource quantities from chapter 5, executable composition from chapter 6 and guarded assignment from chapter 9. You will calculate a three-node placement, identify every eligibility filter and follow a plan into the store's conflict path. The key distinction is between a valid plan, a persisted task claim and enforced resource consumption. Those are three different pieces of evidence.

## Candidate Ordering and Deterministic Choice

Plan accepts pending tasks, nodes, running tasks and a service map. It returns assignments without contacting Docker or writing to a database. This separation lets the same input be evaluated repeatedly, including with reordered input slices, while keeping the side effects outside the algorithm. The planner sorts tasks and nodes before iterating; it does not rely on map iteration or the incidental order returned by a store. [Claim ch10.plan](../../validation/evidence/ch10.json).

[internal/scheduler/scheduler.go, lines 270–290](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L270-L290) at the locked revision.

```go
func Plan(input PlanInput) []Assignment {
	pending := sortedTasks(input.PendingTasks)
	nodes := sortedNodes(input.Nodes)
	state := newClusterState(nodes, input.RunningTasks, input.Services)

	assignments := make([]Assignment, 0, len(pending))
	for _, task := range pending {
		if task.ActualStatus != types.TaskPending {
			continue
		}
		service, ok := input.Services[task.ServiceID]
		if !ok && task.JobID != "" {
			service, ok = jobTaskService(task)
		}
		if !ok {
			continue
		}
		node, ports, ok := bestNode(task, service, nodes, state)
		if !ok {
			continue
		}
```

For each pending task, the planner finds its service specification. Finite job tasks can be represented through jobTaskService when they have a JobID and no ordinary service entry. Missing specifications cannot be safely guessed, so an unresolvable task is skipped. After choosing a node, the planner updates its temporary clusterState. Later tasks in the same invocation see the CPU, memory, ports and volume writers reserved by earlier decisions.

Candidate scoring is specific rather than a generic claim of balanced utilization. It first prefers more memory remaining after placement, then fewer tasks of the same service, then fewer total tasks, then lexical node ID. CPU participates in eligibility but is not the leading score. A node with slightly more remaining memory can therefore win despite a greater CPU load, provided the request still fits. Read the actual score comparator before calling the strategy round robin, bin packing or least loaded.

Stable tie-breaking has practical consequences. If two nodes have identical available memory and task counts, lexical ID decides. A shuffled store response should not change the result. Determinism makes a failure reproducible and a unit test precise; it does not guarantee that the snapshot remains valid until persistence finishes. Nor does it promise a globally optimal placement for all future workloads.

## Ready Nodes, Labels, Capacity, and Ports

Eligibility starts with readiness. An offline or draining node is excluded even if it advertises abundant capacity. Volume mounts can require a particular node, and a writable ReadWriteOnce mount can have an existing owner. Placement labels are compared using the supported equality and inequality operators. An unknown operator is rejected rather than interpreted loosely.

Free resources equal advertised Allocatable minus resources accounted for by existing tasks. Requests use millicores for CPU and bytes for memory. They are not current utilization measurements. A task requesting 400m and 128Mi consumes those declared amounts in this accounting model whether its process is idle or busy. Container cgroup limits require a separate field path into Docker HostConfig, which the ordinary agent path does not complete at this baseline.

Port allocation adds another finite resource. A fixed published TCP port cannot be reused on the same node in one plan. Dynamic ports come from the planner's 30000–32767 interval, excluding reservations already seen in the snapshot or selected earlier in the current plan. A port failure can remain reserved in accounting to avoid immediately repeating an observed conflict. This logic concerns node-scoped host bindings; it is not a cluster-wide virtual service address.

The following fixture is calculated before running it. Atlas requests 400m CPU, 128Mi memory and fixed published port 31080. There are two pending tasks, atlas-01 and atlas-02, processed in ID order. Node b already runs an unrelated service using 100m, 64Mi and port 31080.

| Node | Status | Allocatable CPU/memory | Existing reservation | First Atlas result |
| --- | --- | --- | --- | --- |
| a | offline | 4000m /4096Mi | None | Rejected by status |
| b | ready | 1000m /512Mi | 100m /64Mi, TCP 31080 | Rejected by fixed port |
| c | ready | 1000m /256Mi | None | atlas-01 assigned |

After atlas-01, node c has 600m and 128Mi free. atlas-02 would fit its CPU and memory exactly, but port 31080 is now reserved. Node b remains port-conflicted and node a remains offline, so the second task has no assignment. The limiting factor is the published port, not CPU. Changing the request's public port to dynamic would create a different experiment rather than retroactively changing this result.

The independent book fixture produced exactly that one assignment and confirmed that permuting node and pending-task input order left the plan unchanged. [Executed hand calculation](../../validation/labs/ch10/hand-plan.json) records the actual command, source pin and output. The fixture is a teaching addition compiled inside the disposable Orch module; it does not alter the scheduler or claim a real container was started.

## One Assignment Under Concurrent Work

Scheduler.RunOnce reads pending tasks and ready nodes, loads existing task/resource state and services, then invokes Plan. It persists assignments individually. Each assignment carries ExpectedUpdatedAt from the task snapshot. persistAssignment passes that token to AssignTask and, where supported, combines the mutation with a strict assignment event in one transaction. [Claim ch10.claim](../../validation/evidence/ch10.json).

[internal/scheduler/scheduler.go, lines 170–187](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L170-L187) at the locked revision.

```go
func (s *Scheduler) persistAssignment(ctx context.Context, task types.Task, assignment Assignment) (Assignment, bool, error) {
	assignment.ExpectedUpdatedAt = assignment.ExpectedUpdatedAt.UTC()
	if assignment.ExpectedUpdatedAt.IsZero() {
		assignment.ExpectedUpdatedAt = task.UpdatedAt.UTC()
	}
	transactional := false
	if _, ok := any(s.store).(store.Transactor); ok {
		transactional = true
	}
	assigned := false
	err := store.WithTx(ctx, s.store, func(txCtx context.Context, tx Store) error {
		assignedTask, err := tx.AssignTask(txCtx, assignment.TaskID, assignment.NodeID, assignment.Ports, assignment.ExpectedUpdatedAt)
		if err != nil {
			return err
		}
		assignedAt := assignedTask.UpdatedAt.UTC()
		if assignedAt.IsZero() {
			assignedAt = s.now().UTC()
```

A conflict or a disappearing task is treated as a lost race rather than a fatal scheduler failure. The scheduler increments assignment-conflict metrics and omits that assignment from its successful result. Other store errors are returned with task context. This is useful differentiation: a competing worker's successful claim should not be reported as a database outage, while malformed SQL should not disappear as harmless contention.

The two-writer store experiment now has two distinct records. The untouched upstream suite failed before reaching assignment because its migration fixture omitted agent_version. The separate [full-schema verification fixture](../../validation/intake/full-schema-recovery-corrected.json) applied all 16 migrations and observed one assignment winner and one conflict. Preserve both. The latter supports the tested conditional claim; it does not transform the former into a passing upstream suite.

Per-task uniqueness is narrower than globally safe reservation. Suppose two scheduler instances read the same free node capacity but plan different tasks. Each can win its own task's update. Unless capacity and port reservations are checked atomically across their shared state, the sum of both accepted plans can exceed the snapshot budget. The local clusterState protects ordering within one Plan call, while optimistic assignment protects ownership of one task. Neither scope should be silently expanded.

The failure window is between reading resources and persisting a set of choices. A third actor can create an assignment or bind a host port during that interval. A robust future design would need a shared reservation transaction, a serialized planner, or retryable revalidation of the relevant resource set. Such a change belongs in a separately tested teaching extension; it is not implied by the existence of an AssignTask transaction.

## Planner Guarantees Versus Live Placement

The server does construct a scheduler loop, so it would be inaccurate to call the entire package disconnected. The important qualification is the normal MemoryService service path: reconcileServiceTasksLocked creates assigned tasks directly after choosing eligible ready/volume-compatible nodes. Those tasks are already assigned when the scheduler later asks for pending tasks. [Claim ch10.active-path](../../validation/evidence/ch10.json).

Consequently, the pure planner's CPU, memory and label filters do not automatically constrain every ordinary service deployment. A constrained comparison must send the same declared service/node intent through both paths and examine the resulting tasks. Creating a very large lab machine would hide the distinction; advertising a 500m/128Mi fake node and requesting 600m/256Mi makes it visible without stressing any real host.

Do not turn the comparison into a stronger accusation than the evidence supports. The planner can be internally correct while the application's ordinary service mutation path bypasses it. Conversely, showing one bypass does not prove every task type avoids the scheduler: pending finite jobs and other package paths need their own trace. Classification is attached to the path and guarantee, not to an entire repository as a single badge.

The seeded property tests add breadth. They generate varied node readiness, labels, resource requests and ports, then assert repeatability, unique task assignment and capacity/port invariants. Fixed seeds make a failing generated case reproducible. Those assertions remain about Plan's supplied model; they do not contact the Engine, validate kernel throttling or model every race between separate planner instances.

## Development History and Atlas Experiment

The scheduler began with [fce0a657651c00ffb697bf4a4aba12d0b171f463](https://github.com/alekpopovic/orch/commit/fce0a657651c00ffb697bf4a4aba12d0b171f463). The concurrency audit [1a1c216e8cfb442465f4d3c2c114d20da0342795](https://github.com/alekpopovic/orch/commit/1a1c216e8cfb442465f4d3c2c114d20da0342795) introduced guarded claim handling and related metrics; [3bfcef82a54dec457cf9d4187705fa70cc7215cf](https://github.com/alekpopovic/orch/commit/3bfcef82a54dec457cf9d4187705fa70cc7215cf) added port-awareness changes. Their actual patches, not their titles alone, connect these concepts to implementation. Original prompts 09 and 17 are retrospective development intent; prompt 31 is the later concurrency request.

To reproduce the hand calculation, copy the canonical teaching fixture under examples/teaching-extensions/ch10 into book-scheduler beneath the disposable source module. Use the pinned Go toolchain and run-owned caches. No Docker, database, operator token or service process is required.

```sh
GOTOOLCHAIN=local GOFLAGS=-buildvcs=false go run ./book-scheduler
```

Run that only from the disposable Orch copy, after copying the fixture and verifying the source bytes. Expected success is one assignment for atlas-01 to node c, atlas-02 absent, and an unchanged result after input permutation. The actual recorded run passed. Remove only the book-scheduler teaching directory when finished; never modify or build in the immutable snapshot.

For further exploration, change a copy of the fixture to dynamic ports and predict both assignments before executing it. Record that as a new fixture result. A live Docker comparison is optional and must use the isolated daemon contract because workload published ports can expose all interfaces. Do not remove a host container merely because it occupies the port needed by your experiment.

A failed placement should preserve enough input to explain its rejection. For Atlas, an operator needs node readiness, advertised capacity, existing reservations, the requested port and the task's expected update time. A bare unable-to-place event cannot distinguish a port collision from insufficient memory. Keep a sanitized snapshot beside the planner output when investigating the lab. Avoid substituting live CPU percentage for declared requests: doing so changes the model being evaluated.

Now remove only the existing reservation on node b in a copied fixture. Both ready nodes become eligible for the first task, but node b has more memory remaining after placement and wins that comparison. Its chosen fixed port then prevents the second Atlas task from sharing node b, while node c remains available. Predict two assignments to different nodes before running the changed fixture. This small change demonstrates why a constraint must be applied before a score: a high-scoring node with a conflicting fixed port was previously ineligible, whereas the same node without that reservation can participate. Keep the modified result separate from the recorded baseline experiment.

## Exercises

1. Calculate why node b loses despite having more free memory than node c. Which condition precedes scoring?
2. Change only Atlas to two dynamic published ports. Predict whether the second task can now fit node c and which score comparison matters.
3. Explain how two successful claims for different task IDs can still violate a shared capacity assumption.
4. An operator cites the seeded property suite to claim every deployed Atlas container is CPU-limited. Identify the two missing evidence edges.

[Worked answers](../solutions/ch10.md) justify each result. The operational decision is to name planner invariants precisely, retain the per-task conflict guard, and require an explicit integration/reservation trace before promising placement or runtime enforcement beyond this tested scope.
