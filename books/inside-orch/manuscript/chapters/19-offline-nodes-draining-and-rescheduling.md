# Chapter 19 - Offline Nodes, Draining, and Rescheduling

Atlas needs a worker upgrade. During planned maintenance the operator can ask the control plane to drain that worker and observe replacements. During an unexpected partition, the server instead sees silence and must infer whether to replace work. These situations may produce similar replica movement, but they carry different knowledge. A cooperative worker can acknowledge stopping; an isolated worker may continue running while the server declares it offline.

This chapter follows the active node monitor, drain progress and late-container cleanup. You will calculate the timeout boundary, distinguish drain from disappearance, and explain why replacement is not fencing. Prerequisites are the scheduler and agent chapters plus Chapter 18's separation of deletion intent from actual removal. Atlas remains stateless for replacement experiments; stateful ownership is a deliberate boundary, not a test to perform on valuable data.

## Heartbeat Expiry and Offline Status

Default orch-server constructs node.NewMonitor with configured HeartbeatTimeout and NodeMonitorInterval and runs it in a goroutine. The architectural roadmap contains older wording treating monitoring as future work; current startup and internal/node/monitor.go are the authority. Package presence would not be sufficient evidence, but here the executable caller is explicit.

Monitor.Run calls CheckOnce immediately, then checks on its ticker. An initial check error returns from the loop; later pass errors are logged and the loop continues. Server startup logs a stopped monitor rather than silently supervising a restart. Operators should therefore distinguish a monitor that is healthy but has no stale nodes from one that stopped before entering its recurring checks.

MemoryService.MarkStaleNodesOffline computes cutoff as now minus timeout. It examines ready or draining nodes and skips a zero heartbeat. A heartbeat must be strictly before cutoff; equality is not stale in this comparison. With a thirty-second timeout and a heartbeat at noon, a check exactly at 12:00:30 does not mark the node offline. A later check can. The five-second default monitor cadence adds observation phase, so thirty seconds is not an exact externally guaranteed detection latency.

Unchanged source excerpt — [internal/controlplane/controlplane.go:681–690](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L681-L690):

```go
	cutoff := now.Add(-timeout)
	offline := make([]types.Node, 0)
	for id, node := range s.nodes {
		if node.Status != types.NodeReady && node.Status != types.NodeDraining {
			continue
		}
		if node.LastHeartbeatAt.IsZero() || !node.LastHeartbeatAt.Before(cutoff) {
			continue
		}
		if err := types.ValidateNodeTransition(node.Status, types.NodeOffline); err != nil {
```

After a valid transition, the method records offline, updates the node, marks its active tasks lost, emits node.offline.detected and reconciles services. Repeating the method does not repeatedly transition an already-offline node through the same branch. This guards one state mutation but does not prevent every source of duplicate external effects; runtime acknowledgement is elsewhere.

Heartbeat age is server-side evidence about the last accepted report. A metrics endpoint responding is different evidence; an unreachable metrics target is not the same predicate as stale LastHeartbeatAt. Collect both when troubleshooting, and record the configured interval/timeout rather than relying on remembered defaults after configuration changes.

## Drain Versus Node Disappearance

DrainNode is a planned API operation with maintenance and identity checks. It marks the node draining and immediately reconciles replacement work. Ready-node selection excludes the draining worker. If there are no ready replacements, the workflow stays pending and emits a warning rather than pretending a task has safely moved.

The memory drain path counts off-node active tasks for each service, creating assigned replacements on ready nodes until the desired count is represented. It then waits for available off-node tasks before requesting stops on the old worker. In this implementation available means running or healthy; the drain test explicitly advances a replacement with a running report. Do not transfer Chapter 17's new-rollout-target healthy-only predicate to this workflow.

Unchanged source excerpt — [internal/controlplane/controlplane.go:2401–2415](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2401-L2415):

```go
		if availableTaskCount(offNodeActive) < service.Spec.Replicas {
			continue
		}
		for _, task := range drainingTasks {
			if task.DesiredStatus == types.TaskStopped || task.DesiredStatus == types.TaskRemoved {
				continue
			}
			if err := types.ValidateTaskDesiredTransition(task.DesiredStatus, types.TaskStopped); err != nil {
				continue
			}
			task.DesiredStatus = types.TaskStopped
			task.UpdatedAt = timestamp
			s.tasks[task.ID] = task
		}
	}
```

TestDrainCreatesReplacementAndStopsOldTaskAfterReplacementRuns is precise about the ordering: the old task starts on node A; node B is registered; drain creates a distinct replacement; reporting that replacement running changes the old desired status to stopped. The task ID is new even when service identity is stable. The test proves memory-state ordering, not packet-level availability or a physical worker shutdown.

Drain progress also needs careful interpretation. nodeDrainStatusLocked counts RemainingTasks whose desired status is neither stopped nor removed. Once those directives are set, it can report DrainComplete even while the old Docker object has not yet acknowledged removal. That result is completion of the control-plane drain decisions, not proof that a technician can instantly unplug the host without checking runtime consequences.

Uncordon sets the node ready again. The fixture that uncordons before replacement readiness confirms the old task can remain desired running and drain status becomes not_draining. This is a useful cancellation window, but it is not a transactional rollback of every replacement ever created. Inspect both cohorts before interpreting uncordon as restoration of the original layout.

## Replacement Tasks and Rescheduling

When a heartbeat timeout marks tasks lost, each active task gets a node_lost condition. For a stateless service, the memory method sets desired removed, actual failed, failure reason node_lost and a finish timestamp. Reconciliation can then create replacement identity on a ready node. The original task record remains the reference for late-report guards and returning-worker cleanup.

Unchanged source excerpt — [internal/controlplane/controlplane.go:2078–2092](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2078-L2092):

```go
		task.Conditions = upsertTaskCondition(task.Conditions, types.TaskCondition{
			Type:               types.TaskConditionNodeLost,
			Message:            "node heartbeat timed out",
			LastTransitionTime: timestamp,
		})
		service := s.services[task.ServiceID]
		if !service.Spec.Stateful {
			task.DesiredStatus = types.TaskRemoved
			task.ActualStatus = types.TaskFailed
			task.FailureReason = "node_lost"
			task.FinishedAt = timestamp
		}
		task.UpdatedAt = timestamp
		s.tasks[taskID] = task
	}
```

For Stateful services, that mutation is intentionally withheld: the condition and updated timestamp remain, but the old task is not automatically converted to removed/failed by this branch. TestMarkStaleNodesOfflineDoesNotReplaceStatefulTask captures this conservative distinction. The flag does not implement distributed storage, leader fencing or data recovery. It simply avoids one automatic replacement policy that would otherwise risk competing writers.

Normal service replacement still uses MemoryService's immediate placement, not the standalone planner's full resource-fit logic. “Insufficient capacity” in the drain progress response principally checks whether ready replacement nodes exist in this path; it must not be read as proof that CPU, memory, host ports and local data have all been globally reserved. Trace the exact fields when deciding whether a proposed maintenance move can fit.

On return, a worker can heartbeat back to ready. Its agent compares local managed objects with current assignments and removes objects no longer assigned to its node. TestReturnedNodeRemovesNodeLostUnassignedContainer exercises that later cleanup. The original and replacement task IDs must remain distinct in the worksheet, otherwise an operator can confuse adoption of a still-owned object with removal of obsolete work.

## Partitions Without a Fencing Promise

Consider two workers, A and B. Atlas serves on A. A loses connectivity to the server, but its Docker daemon and application keep running. After the heartbeat deadline, the server marks A offline and replaces stateless work on B. B starts a new task. Both HTTP endpoints can now exist even though the server's current desired set excludes A's task.

There is no contradiction: central records and remote side effects have different owners. A failed or removed record is not a remote power switch. Without connectivity, A cannot necessarily receive the directive or report its cleanup. After the partition heals, label-aware reconciliation can remove the obsolete container. It cannot undo requests or writes processed during overlap.

For a stateless HTTP service, temporary overlap may be acceptable if clients and data stores tolerate it. For a single-writer workload, it can violate a safety invariant. A real fencing design might use storage generations or an external authority that rejects stale writes, but none is implied by the node timeout. Such a design belongs to a separately tested extension, not an optimistic explanation of the baseline.

| Situation | Server knows | Server cannot conclude |
| --- | --- | --- |
| Planned drain with replacement report | Replacement reached running/healthy; stop intent can be set | Old runtime already removed |
| Heartbeat timeout | Last accepted heartbeat predates cutoff | Worker is powered off |
| Returning agent cleanup | Current assignment set excludes obsolete task | No overlap occurred during partition |
| Stateful node_lost condition | Owner became unreachable | Data safely moved to another node |

An incident narrative should preserve the interval between replacement start and old-container stop. Measuring that interval in an actual lab is useful; inventing a zero-overlap result from unit tests is not. Chapter 34 later separates leader coordination from worker fencing for the same reason.

The late-report boundary deserves its own check. A returning agent credential establishes who sent a message, while TaskID and NodeID establish which assignment it concerns. Lifecycle guards then decide whether the requested status can advance that particular record. Authentication alone cannot make an obsolete running report authoritative. Conversely, an idempotent report for still-owned work may legitimately be accepted. Test the desired/actual state combination produced by your fault instead of claiming that every report older than a timeout is rejected. The relevant question is current ownership and permitted transition, not whether the packet feels stale to an observer.

## Atlas Lab: Pause One Owned Agent

Use Go 1.25 and the disposable pinned source copy for deterministic fixtures. No physical worker is needed for the first stage. Source-checked tests expose stale detection, stateless/stateful policy, pending drain and returning cleanup.

```bash
go test ./internal/node -run TestMonitor -count=1 -v
go test ./internal/controlplane -run 'Test(MarkStaleNodesOffline|HeartbeatReturnsOfflineNodeReady|Drain|UncordonBeforeDrainCompletion|NodeOfflineDuringDrainStatus)' -count=1 -v
go test ./internal/agent -run TestReturnedNodeRemovesNodeLostUnassignedContainer -count=1 -v
```

The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) includes these node/control-plane cases with caching disabled. Their fake clocks and records establish the selected transition scenarios; they do not pause an actual worker or fence a remote process. For an actual two-agent Atlas run, record server/agent PIDs, node IDs, task IDs, direct endpoints and Docker IDs before the fault. Pause only the recorded disposable agent process; never stop a production host, shared daemon or host firewall. Keep a bounded pause and an explicit resume/terminate cleanup handler.

During the pause, sample LastHeartbeatAt, node status, lost-task condition, replacement identity and direct reachability of the old endpoint. Do not assume a particular detection timestamp; retain actual samples. Resume the agent, observe the new assignment set and check the old container's removal independently. Abort if replacement capacity is absent, the selected process is not run-owned, or any operation targets a stateful user workload.

The planned-maintenance variant drains A while A remains connected. Record replacement readiness and old desired stop, then inspect physical cleanup. Uncordon only the recorded node if the test requires cancellation. At the end, resume every paused process, stop the run-owned agents and remove exact lab objects. A trustworthy result explains residual effects rather than hiding them behind a final green status.

## Exercises

1. Why does a heartbeat exactly at the timeout cutoff remain eligible on that check, and how does the monitor cadence affect observed detection?
2. A drain reports complete while Docker still lists the old container. Is that necessarily a bug? Name the completion predicate and the missing observation.
3. Explain the stateless and Stateful mutations after node loss. Which one proves exclusive access to data?
4. Design a partition worksheet that can demonstrate overlap without touching external hosts. Which identities and two independent endpoint observations must it retain?

[Worked answers](../solutions/ch19.md) connect these decisions to the exact guards. The source evidence supports a timeout-and-reconciliation mechanism with explicit limits, not an invisible worker-fencing protocol.

## Development history and source references

Original development prompts 39, 40 supply the requested scope. The inspected implementation history includes [42d4caa4451f](https://github.com/alekpopovic/orch/commit/42d4caa4451f4dea24113d48eb1e9e47f2cef558), [a5d4bfb37f70](https://github.com/alekpopovic/orch/commit/a5d4bfb37f70a3119bc6e2d49f8fefc5a1c748a5). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/node/monitor.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/monitor.go#L1-L72)
- [internal/node/monitor_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/monitor_test.go#L1-L59)
- [internal/controlplane/drain_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/drain_test.go#L1-L184)
- [internal/controlplane/offline_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/offline_test.go#L1-L193)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L1-L195)
- [docs/OPERATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OPERATIONS.md#L1-L301)
