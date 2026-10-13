# Chapter 17 - Rolling Updates and Rollback Invariants

Atlas API already has useful replicas. Its next image adds a feature, but the operator must change those replicas without confusing a deployment request with successful replacement. One new container can be created before it is ready, one old task can be told to stop before Docker acknowledges removal, and traffic can still use an endpoint cached before either change. A rolling update is therefore a sequence of observations and bounded decisions, not an atomic exchange of images.

This chapter assumes the task lifecycle, agent report path and health thresholds from Chapters 4, 13 and 14. You will calculate surge and availability bounds, distinguish failed target versions from previous successful versions, and identify conflicting user actions. The concrete mechanism is the rollout controller used by default server startup. Its state and history still reside in MemoryService; learning its count invariants does not remove the process-loss boundary established earlier.

## Service Versions and Deployment Ownership

RolloutService changes the service's desired image, increments DeploymentVersion and saves a versioned specification before recording a pending deployment. FromVersion and ToVersion identify the transition. The API returns ownership of an operation that will advance later; it does not wait for every agent to start a container. The controller retrieves deployments in pending, running and rolling_back states, sorting by creation time and ID. This makes iteration order inspectable without making the collection durable.

A deployment is interpreted against current service replicas and tasks. Task.Version matters: an old image running under an old task belongs to a different cohort from a new target. A task from neither deployment version is ignored by this particular accounting function. That is a reason to retain versioned evidence during triage rather than merely count every container with the service's name.

The source distinguishes active tasks, available old tasks and healthy new tasks. Old availability uses the lifecycle helper accepting running or healthy. New readiness is stricter: only actual healthy increments newHealthy. A new task whose container is merely running occupies active capacity but cannot authorize stopping an old replica. This difference is easy to lose when a dashboard compresses every live task into a green count.

Unchanged source excerpt — [internal/rollout/rollout.go:376–384](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go#L376-L384):

```go
		if task.ActualStatus == types.TaskFailed {
			state.newFailed++
		}
		if isActive(task) {
			state.newActive++
			if task.ActualStatus == types.TaskHealthy {
				state.newHealthy++
				state.available++
			}
```

The claim here is bounded: this controller uses reported states from its store. It does not independently probe the application or synchronously update every proxy. A routing consumer must also observe the new endpoint set before client continuity can be evaluated. Its arithmetic can be correct while a client still reaches a stale or unreachable endpoint. Keep controller evidence and traffic observations separate throughout the experiment.

## Max Surge and Max Unavailable Arithmetic

Take Atlas at three replicas, MaxSurge one and MaxUnavailable zero. The creation ceiling is three plus one: four active tasks. Initially three old tasks are available and there are no targets. One pass may create a target, filling the fourth slot. Because that target is pending, no old task can stop. Repeating the pass without new reports cannot manufacture progress: the surge slot is already occupied and newHealthy remains zero.

When the first target reports healthy, the controller can stop an old task while keeping three available replicas. Its stop guard calculates the unavailable count after the prospective stop. With four available tasks, stopping one leaves three, so three minus three is zero. A second stop would leave two, making the unavailable count one and violating this deployment's zero allowance. The next pass uses desired/store accounting: a task whose desired status is stopped or removed no longer counts active, even before the agent acknowledges a physical stop. Capacity in this calculation can therefore be reused while its old container still runs.

Unchanged source excerpt — [internal/rollout/rollout.go:244–252](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go#L244-L252):

```go
	for _, task := range oldTasks {
		if state.newHealthy <= state.oldStopped+stopped {
			break
		}
		if service.Spec.Replicas-(state.available-stopped-1) > deployment.MaxUnavailable {
			break
		}
		transactional := c.transactional()
		stoppedTask := types.Task{}
```

There is another guard before that arithmetic: newHealthy must exceed oldStopped plus the stops planned in this pass. It relates each removed old replica to replacement readiness. Consequently MaxUnavailable is not a command to stop that many old tasks immediately. For example, a three-replica deployment with surge zero can stall because no target can be created and no healthy replacement exists to authorize stopping. The source's conservative ordering is more specific than a generic rolling-update policy description.

The creation loop tracks totalActive after each successful task write; stopping tracks the same local pass. Neither count turns a distributed runtime observation into a transaction over Docker. Desired stopped/removed excludes a task from active accounting before its actual state becomes terminal, and a stop directive can coexist with a container that has not received it. The controller also decrements its pass-local oldActive and totalActive immediately after a successful StopTask; it can declare rollout success while physical cleanup remains pending. Developers should identify whether a suspected limit violation concerns desired objects, reported task states or actual live processes before changing the arithmetic.

| Atlas observation | Old active | New active | New healthy | Controller consequence |
| --- | --- | --- | --- | --- |
| Before update | 3 | 0 | 0 | One surge slot can be filled |
| Target pending | 3 | 1 | 0 | Wait; no old stop authorized |
| Target healthy | 3 | 1 | 1 | One old stop can preserve availability |
| One old task desired stopped, actual stop unacknowledged | 2 in controller accounting | 1 | 1 | Desired intent frees a count slot; physical container may remain live |

This table is a source-derived scenario, not a captured execution trace. In a real run, attach the task IDs and timestamps that make each row meaningful.

## Failed Targets and Previous Successful Versions

A target in TaskFailed causes the deployment to become failed. TaskUnhealthy is a different state: rolloutStateFor does not increment newFailed for it. The agent reports unhealthy after its threshold; MemoryService.ReportTaskStatus converts that report to failed when the service restart policy permits replacement. Without that conversion, an unhealthy stored target is distinct from failed. The rollout controller does not interpret raw probe responses directly. During the intermediate window the target can occupy a surge slot while progress waits.

Imagine a healthy first target and then a second target whose application returns an error. The first target may already have allowed one old replica to stop. A later target failure marks the rollout failed; it does not atomically resurrect the stopped container. The remaining old and new cohorts are evidence of a partially advanced deployment. An operator needs their versions, states and endpoints before selecting recovery.

RollbackService finds a previous successful version and restores its specification as the desired target. It records a new deployment from the current version to the earlier one, preserving the failed deployment's history. TestRollbackAfterFailedRollout asserts version two returning to version one and confirms that the failed forward deployment remains failed. TestRollbackWhenNoPreviousVersionExists rejects a rollback without such a version. These are actual source assertions, not proof every runtime image remains pullable.

An in-flight rollback is idempotent: repeated calls return the existing operation rather than generate another reverse transition. That property is valuable when the response to the first request is lost. It is scoped to the same live control plane and operation identity. A new default server has neither the version history nor the prior operation maps, so retrying after process loss is a different situation.

The failed-image timeline should therefore name five events: forward request accepted, target created, target health degrades, deployment becomes failed, reverse deployment accepted. Add a sixth observation for reverse completion only when task reports establish it. Preserving the failed operation allows an incident report to explain why rollback was necessary instead of rewriting history into a smooth success story.

## Locks Against Conflicting User Actions

Operation locks are enforced through service/deployment state under the memory service's mutex. An identical repeated rollout can return the active deployment. A different rollout conflicts, and rollback during an active forward rollout conflicts. These rules avoid two callers claiming incompatible desired versions at once. They do not constitute a distributed lock across independent servers.

Deletion has precedence. TestDeleteWinsOverActiveRollout requests delete, checks that the active deployment becomes failed, and rejects a later rollout against the deleting service. TestScaleAndDeleteOperationOrdering shows that scale after delete conflicts while scale before delete can complete before deletion wins. Repeated delete is idempotent. The practical rule is to classify an error as an operation conflict before retrying a different request; a blind retry can obscure the operator's intended order.

A failed deployment is terminal, so the operator can explicitly start rollback after failure. There is no need to invent a force flag merely because the original development prompt mentions one possible policy. Use the actual CLI and control-plane behavior. The lock tests are particularly useful because they make the ordering contract visible without requiring a timing-sensitive terminal demonstration.

## Atlas Lab: Separate Count Invariants from Traffic

Use the disposable pinned source copy with Go 1.25 and an owned cache. Run the named deterministic tests first; they need no Docker or database. Their fakes explicitly mark tasks healthy, which is exactly why they can prove controller decisions reproducibly but cannot prove uninterrupted application traffic.

```bash
go test ./internal/rollout -run 'TestController(SuccessfulRollout|FailsWhenNewTaskFails|RespectsMaxUnavailable|RespectsMaxSurge|IdempotentResume|CompletesRollback)$' -count=1 -v
go test ./internal/controlplane -run 'Test(Rollback|RolloutWhileRolloutInProgress|DeleteWinsOverActiveRollout|ScaleAndDeleteOperationOrdering)' -count=1 -v
```

Expected observations are the assertions just described: a bounded target cohort, no old stop before replacement health, failed forward history preserved, an idempotent reverse operation and clear conflicts. The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) includes the rollout/control-plane assertions with caching disabled. Its fakes establish model behavior, not continuous client availability. The [rollout laboratory](../../labs/04-rollout-rollback/README.md) separately captures seven actual controller checkpoints; deployment success can precede acknowledgement of the final pending stop.

For a separate real Atlas run, record initial service version, all task/container IDs and direct HTTP responses. Use the case-study health-enabled manifest and an owned second image. Request rollout with one surge slot, then observe deployment status, task version/status and endpoint changes after each interval. Inject a failing target using the dedicated unhealthy manifest or nonexistent lab image; never modify a user service. Record both the failed deployment and the reverse operation.

Abort if the service name resolves outside the recorded run namespace, if expected old endpoints disappear before the recorded availability permits it, or if the selected failure affects an unrelated container. Cleanup deletes only Atlas resources created by that run and checks residual container IDs. A passing count fixture cannot waive this cleanup or routing evidence. The engineered decision is to trust each observation for the boundary it actually measures.

## Exercises

1. Atlas has three old available replicas, one healthy target, surge one and unavailable zero. How many old replicas may stop in the next decision, and which guard prevents the second stop?
2. Explain why a new running target cannot replace an old running replica in this controller even though both appear live.
3. A rollout has one healthy target and one unhealthy target. Is failure status guaranteed immediately? Trace the restart-policy conversion needed and identify the waiting window.
4. The first rollback response disappears. Contrast retrying against the same live server with retrying after a fresh default server process. Which evidence would establish operation identity?

[Worked answers](../solutions/ch17.md) provide calculations and source-based reasoning. Claims and exact listings are recorded in the companion evidence ledger; their inspected status must not be upgraded without an actual execution record.

## Development history and source references

Original development prompts 14, 15, 42 supply the requested scope. The inspected implementation history includes [de5900bced92](https://github.com/alekpopovic/orch/commit/de5900bced92ad9d5786cd258ff7941d67369d33), [430a061fe7f0](https://github.com/alekpopovic/orch/commit/430a061fe7f01df966e33d0b86654c627b7d5e39), [5bfb4ac394a6](https://github.com/alekpopovic/orch/commit/5bfb4ac394a609469263de9e14d25d5c2660ee8f). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go#L1-L414)
- [internal/rollout/rollout_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout_test.go#L1-L343)
- [internal/controlplane/rollback_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/rollback_test.go#L1-L107)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go#L1-L126)
- [docs/ROLLOUTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ROLLOUTS.md#L1-L88)
