# Chapter 11 - Reconciliation as Repeated Convergence

Atlas API should have two replicas, but the store currently contains one running task and one failed task. The operator's intent has not changed. Something must decide whether to create another task, preserve the failure, or wait for an in-progress operation. Reconciliation is that repeated comparison between intent and recorded state. Its correctness depends on counting the right objects and assigning each side effect to the right owner.

You already know the task lifecycle, MemoryService composition and optimistic store boundary. Here you will predict what successive iterations read and write, explain why pending tasks count before Docker starts, and distinguish controller restart from process recovery. The standalone reconciler package is an implemented library; the default server's immediate MemoryService path must be traced separately. [Claim ch11.composition](../../validation/evidence/ch11.json).

## Replica Convergence Without Docker Calls

The reconciler's Store interface exposes services, task collections, active deployments, task creation/stopping, service status changes and events. It contains no Docker Runtime. That boundary is deliberate and visible: the controller decides desired work in the store, the scheduler chooses placement for pending work, and the agent acts on containers. Confusing these roles would make a successful task-row insertion sound like a running application.

ReconcileOnce first checks cancellation and store presence, then acquires its configured LeaderLock and releases the lease when the iteration returns. The default lock is NoopLeaderLock. An interface named LeaderLock does not demonstrate distributed exclusivity, and a fake lease test only proves that the expected call was made. Actual shared leadership, session cleanup and fencing are considered in chapter 34.

The internal reconcile pass loads services and a set of services with pending, running or rolling-back deployments. It sorts services by ID and dispatches based on service status. Active services with an active rollout are skipped, preventing the ordinary replica loop from fighting the rollout controller. Deleting services follow a different path; deleted services are not treated as active intent. A final orphan scan stops nonterminal tasks whose service is no longer known.

For an active service, reconcileService loads and sorts its tasks. Current-version nonterminal tasks enter the current set; nonterminal tasks from another version enter the outdated set and are stopped. Failed current-version tasks with a non-restartable policy are counted separately. This last detail prevents a never-restart workload from being recreated endlessly just to satisfy a replica number. [Claim ch11.counting](../../validation/evidence/ch11.json).

[internal/reconciler/reconciler.go, lines 304–322](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L304-L322) at the locked revision.

```go
	for _, task := range tasks {
		if task.Version != service.DeploymentVersion {
			if isNonTerminal(task) {
				outdated = append(outdated, task)
			}
			continue
		}
		if isNonTerminal(task) {
			current = append(current, task)
			continue
		}
		if task.ActualStatus == types.TaskFailed && !restartAllowed(service.Spec.RestartPolicy) {
			nonRestartableFailed++
		}
	}

	for _, task := range stopOrder(outdated) {
		if err := ctx.Err(); err != nil {
			return result, err
```

The effective count is current nonterminal work plus non-restartable failures. If that count is below desired replicas, the controller creates the deficit as pending tasks. If the current set exceeds desired replicas, it selects extras to stop. Pending, assigned, pulling and created tasks are not absent replicas merely because they are not yet healthy. Counting only running tasks would cause every slow image pull to produce more tasks on the next iteration.

Notice the difference between replica convergence and availability. Two pending tasks can satisfy the controller's work-count requirement while zero tasks serve HTTP. Health and rollout accounting use additional observations for availability decisions. A dashboard that collapses these dimensions into one green replica count would hide a real operational distinction.

## Repeated Iterations and Restart Idempotency

Consider a fresh fixture with Atlas desired replicas two and no tasks. The first pass reads an empty task list, calculates a deficit of two and creates two pending tasks. The second pass reads those pending tasks, counts both as current work and creates nothing. Its successful outcome is a no-op, not another pair of creation events. [Claim ch11.repeated](../../validation/evidence/ch11.json).

Now replace the Reconciler object between passes while keeping the same fake store. The new controller still sees the pending tasks, so it also creates nothing. The upstream restart-hardening test does exactly this: New(store), one iteration, another New(store), another iteration. That is useful controller reconstruction evidence. It is not a fresh process, a database reload or a persisted-state recovery test.

The distinction explains what the restart invariant actually requires. The controller must derive its next action from stored tasks rather than an unpersisted local list of tasks it remembers creating. If an action's result is already recorded, a restarted controller should recognize it. If the store itself disappears, there is no retained result to recognize. Default MemoryService process loss therefore remains outside the proof.

Creation and its event can share a transaction when the supplied store supports Transactor. Without it, the generic helper executes directly and event emission is best effort. There is also no automatic transaction covering the entire read-count-create sequence across all services and controller instances. Two independent controllers can read the same deficit before either writes. A local idempotence test is not a substitute for durable ownership or a cross-controller serialization strategy.

This is the concrete failure window: pass A and pass B both observe one missing replica; each creates a distinct pending task. Task IDs are unique, but the total desired work is now excessive. A later iteration may scale down, yet temporary over-creation still happened. The appropriate claim is eventual correction under the tested model, not an invented exactly-once creation guarantee under arbitrary concurrent controllers.

## Failed Tasks, Restart Policy, and Scale-Down

For Atlas with restart on failure, one running task and one failed task against desired count two yields one replacement. The following pass includes that replacement's pending state and does not create another. The failed historical task remains useful evidence, but it no longer inflates the active count. The executed tests verify both the single replacement and the absence of duplicate replacement events.

With restart policy never, the failed task instead contributes to effectiveCount. That choice respects the configured no-restart intent even though it leaves the service below running availability. The algorithm's restartAllowed helper accepts empty, always and on_failure conditions and rejects others. Do not invent an exponential delay, retry budget or backoff schedule merely because the domain RestartPolicy type has additional fields; trace what this particular controller reads.

Scale-down similarly needs stable selection. stopOrder begins with stable task sorting and applies stop priorities, using descending task ID as a tie-breaker. The fixture with three running tasks and desired one stops task-c then task-b. The next pass does not issue the same desired-stop mutations again. This makes tests reproducible and avoids gratuitously changing which replica is retained.

[internal/reconciler/reconciler.go, lines 435–446](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L435-L446) at the locked revision.

```go
func (r *Reconciler) stopTask(ctx context.Context, task types.Task, reason string) (bool, error) {
	if task.DesiredStatus == types.TaskStopped || task.DesiredStatus == types.TaskRemoved {
		return false, nil
	}
	transactional := r.transactional()
	stopped := false
	err := store.WithTx(ctx, r.store, func(txCtx context.Context, tx Store) error {
		stoppedTask, err := tx.StopTask(txCtx, task.ID, task.UpdatedAt)
		if err != nil {
			return err
		}
		if err := events.Emit(txCtx, tx, types.Event{
```

stopTask first returns a no-op if desired state is already stopped or removed. Otherwise it attempts a guarded store update using the task's UpdatedAt. A lost conflict or missing task is treated as no completed stop, while other failures are returned. The controller reports only successful desired-state changes in its counters. It has still not issued Docker StopContainer; the agent owns that later action.

Deletion extends the same separation. A deleting service remains deleting until its tasks report actual removed state. If the agent is absent, changing intent does not physically remove a container. A safe interface should show the intermediate state rather than claiming deletion completed merely because the HTTP request was accepted. The chapter 18 cleanup trace follows that sequence in detail.

## How This Controller Is Invoked

The default server constructs MemoryService and calls immediate service reconciliation as part of its own mutations and observations. It does not construct internal/reconciler.Reconciler. Inside reconcileServiceTasksLocked, ordinary missing replicas are created directly with a node and assigned state, using ready/volume-compatible nodes. That differs from this library's creation of pending tasks for a separate scheduler.

Both paths address desired-state convergence, but their placement, restart and transaction contexts are not interchangeable. A reader who searches only for the package named reconciler can miss the actual executable behavior. Conversely, a reader studying only the memory path would miss a useful independently testable library. Keep the call graph attached to each explanation instead of declaring one conceptual diagram true for all paths.

| Question | Standalone reconciler | Normal MemoryService path |
| --- | --- | --- |
| Where is replica work decided? | ReconcileOnce over Store snapshots | reconcileServiceTasksLocked under memory mutex |
| How are missing tasks introduced? | Pending desired-running tasks | Directly assigned tasks when eligible nodes exist |
| Does this code call Docker? | No | No; agent still owns runtime actions |
| What survives a default process restart? | Depends on supplied store | Process-local maps do not survive |

The history shows why these distinctions matter. [208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3](https://github.com/alekpopovic/orch/commit/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3) introduced the reconciler implementation. [a11cec091a69720c14b9713d8be68f38fe6df332](https://github.com/alekpopovic/orch/commit/a11cec091a69720c14b9713d8be68f38fe6df332) added active-deployment skipping and restart/no-op regression coverage. [316ba80ac1ea7ba465f1b0826b655233a651c043](https://github.com/alekpopovic/orch/commit/316ba80ac1ea7ba465f1b0826b655233a651c043) hardened task-state idempotency in the control plane. These are related improvements, not proof every package shares one invocation path. Original prompts 10 and 24 are retrospective intent; prompt 32 names the later restart audit.

## Atlas Lab: Observe Reads Before Counting Success

The source-only experiment needs Go 1.25 and the disposable pinned source copy. It does not need Docker, a database or an active server. Run the focused upstream fixtures from that copy, with external integration flags unset and the selected GOROOT/cache configuration from the environment contract.

```sh
go test ./internal/reconciler -run TestReconcile -count=1 -v
```

The [actual focused run](../../validation/labs/ch11/focused-tests.json) passed. Its raw output names the repeated no-op, controller reconstruction, failed-task replacement and scale-down cases. The observation is constrained to fake-store controller behavior; it is not an Atlas container deployment or database process restart.

When reading each test, write three columns: tasks read on pass one, mutations emitted on pass one, and tasks read on pass two. For the two-missing-replica case, the last column must include the pending tasks created earlier. For the failed-replacement case, it must include the new task as current work. This exercise detects whether the test actually models retained state rather than merely counting calls on a mock that returns the same old snapshot forever.

A further safe extension can place a barrier between two reads to expose simultaneous deficit decisions. That experiment should assert the actual over-creation or conflict behavior, not weaken its expectation to obtain a green test. Keep its source under teaching-extensions and record which store/lock it supplies. Cleanup consists only of test process termination and optional removal of copied teaching files; no host containers are created.

A reconciliation result is also a statement about the state that was read. If Atlas changes replicas while a pass is computing its deficit, a later pass must observe that newer intent. The first pass should not be presented as a snapshot of the cluster at the instant its result is displayed. In a safe race fixture, pause after ListTasksByService, modify the desired service in the fake store, then release the pass and inspect both the emitted mutations and the next pass. Such a test can reveal stale intent without creating containers. Record which object revisions the fixture preserves; simply asserting eventual replica count can hide an unnecessary intermediate creation or stop.

## Exercises

1. Atlas has desired two, one running task and one pulling task of the current version. Predict the next create count and explain why health is irrelevant to that count.
2. Repeat the calculation with one running and one failed task under restart never, then under on_failure.
3. Identify what survives in the controller-restart fixture. Why would deleting its fake store invalidate the claimed guarantee?
4. Design a two-controller race fixture and state which additional mechanism would be required before calling creation globally unique.

[Worked answers](../solutions/ch11.md) include the counted sets and the concurrency reasoning. Use the library to study convergence, keep observed state separate from actual container availability, and require the executable call path before transferring its invariants to a live deployment.
