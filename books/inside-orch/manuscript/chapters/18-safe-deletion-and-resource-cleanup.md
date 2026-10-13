# Chapter 18 - Safe Deletion and Resource Cleanup

An operator deletes Atlas API after its rollout experiment. One worker stops its container, then fails during removal. The HTTP delete request has already succeeded, so a second operator assumes the host is clean and reuses a resource. That assumption crosses an acknowledgement boundary: the server accepted deletion intent, but Docker has not confirmed the final side effect. The remaining object is exactly what the deletion workflow must preserve and revisit.

You will follow active, deleting and deleted services; distinguish desired task state from observed removal; identify which process owns retries; and decide what evidence permits finalization. Chapter 12 established Docker identity and Chapter 17 established operation precedence. Here those definitions become a cleanup protocol. The objective is precise convergence without removing unrelated objects, rather than making an API list look empty as quickly as possible.

## Soft Deletion Is a State Machine

DeleteService first finds the service in the selected namespace. A missing or invisible service returns not found. An existing deleting or deleted service returns success again. Thus idempotency means repeating the same owned operation does not create a competing cleanup workflow; it does not mean every arbitrary unknown identifier is a successful deletion.

For an active service, the method validates the transition, cancels active deployments, records deleting, and changes tasks toward stopped unless removal is already desired or observed. The deletion-started event records this request-side milestone. The service remains in the memory map; hard deletion is not the mechanism. This retained identity lets later agent reports be correlated with the same service instead of becoming unowned terminal messages.

Unchanged source excerpt — [internal/controlplane/controlplane.go:1454–1463](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L1454-L1463):

```go
	s.cancelActiveDeploymentsLocked(id, now, "service deletion requested")
	service.Status = types.ServiceDeleting
	service.UpdatedAt = now
	s.services[id] = service
	for taskID, task := range s.tasks {
		if task.ServiceID == id {
			if task.DesiredStatus != types.TaskRemoved && task.ActualStatus != types.TaskRemoved {
				if err := types.ValidateTaskDesiredTransition(task.DesiredStatus, types.TaskStopped); err != nil {
					return fmt.Errorf("%w: %v", store.ErrInvalidState, err)
				}
```

Notice the ordering: deletion wins over the old rollout, then task directives change. The source does not call Docker from inside the server mutex. Doing so would conflate authoritative intent with a remote runtime effect and make a slow daemon block unrelated state operations. Instead the agent retrieves the changed assignments and performs the stop/remove sequence. That design creates a visible waiting state whenever the worker cannot communicate.

The standalone reconciler also has a deletion path and tests. Those are useful package evidence, but default startup does not instantiate that reconciler. Trace MemoryService.DeleteService, ListAssignedTasks, the active agent and ReportTaskStatus for the default binary. A diagram showing the standalone package between every request and agent would teach the wrong ownership graph even if the diagram looked plausible.

## Stop and Remove Ownership

The agent's ensureTask checks desired state before attempting normal execution. Stopped or removed intent goes to removeAssignedTask, which resolves a container it is authorized to remove. A provided ContainerID alone is insufficient: inspection must establish that the managed object's labels match the assigned node and task. If that inspection fails, the runner searches managed containers using the node/task labels and evaluates ownership again.

This guard protects a concrete failure case. A stale or corrupted task report could point at an unrelated container ID. Blindly deleting that ID would make control-plane metadata an unrestricted host deletion command. TestReconcileDoesNotRemoveNonManagedAssignedContainerID exercises the opposite contract: the agent must preserve an object that lacks the required management identity even when the assignment references it.

When a matching container exists, removeLocalContainer stops it and then removes it. An error in either action returns before the agent reports removed. When no matching object exists, the task can still be reported removed, because desired cleanup has no remaining owned object to delete. The distinction is between an object proven absent and an ownership check that forbids deleting an unrelated object; capture drift evidence where those paths differ.

Unchanged source excerpt — [internal/agent/agent.go:634–639](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L634-L639):

```go
func (r *Runner) removeLocalContainer(ctx context.Context, containerID orchdocker.ContainerID) error {
	if err := r.runtime.StopContainer(ctx, containerID, 10*time.Second); err != nil {
		return err
	}
	return r.runtime.RemoveContainer(ctx, containerID, true)
}
```

The Engine adapter tolerates already-stopped and already-missing objects. That is necessary for retry after a lost response: Docker might have completed an action even though the agent saw an error. A repeated stop/remove must not require resurrecting the object or treating absence as a new failure. It also must not broaden its selector from one task to every managed container on the host.

## Retries After Partial Cleanup

Return to the failed removal. At the first poll, the container is running and desired state is stopped. Stop succeeds; remove fails. The agent returns an error and does not send the final removed report. Server state therefore remains deleting with an unfinished task, while Docker now holds a stopped object. Those observations disagree in a useful way: the workflow has progressed, but final acknowledgement is intentionally withheld.

At the next successful poll, identity still points to the same task. Inspecting the stopped object is sufficient to locate it; stop is harmless on repetition, removal can succeed, and only then is removed reported. If removal succeeded but the report response disappeared, the next poll can find no object and repeat the removed report. These are two different retry windows with the same convergence goal.

| Interruption | Server evidence | Docker evidence | Required next observation |
| --- | --- | --- | --- |
| Before agent poll | deleting, desired stopped | May still run | Assignment retrieval and owned stop |
| After stop, before removal | Task not removed | Stopped object remains | Retry exact object removal |
| After removal, before report | Task not removed | Object absent | Repeat scoped removed report |
| After accepted report | Finalization can advance | Object should remain absent | Verify all service tasks, not just one |

A network partition delays this sequence. Neither an accepted delete nor a central timeout remotely fences the container. Operators must avoid interpreting “deleting” as a guarantee that the old process cannot serve or write. For a resource that must not have concurrent writers, observed host cleanup or a separate fencing mechanism is required before ownership is reused.

The runner returns the first task execution error after handling assigned tasks and cleanup. The surrounding loop retries through later reconciliation, rather than repairing the server's records by pretending success. This is an important reason to preserve errors and task identity in the incident worksheet. Suppressing the error would make a lingering object indistinguishable from successful cleanup.

## When Finalization Is Safe

MemoryService.maybeFinalizeServiceDeletionLocked requires every task belonging to the service to have ActualStatus removed. Stopped and failed are insufficient in this default path. If the service has no tasks, the loop has no blocker and deletion can complete. The condition is explicit and stronger than a prose description that says “terminal or removed.” Use the actual implementation's distinction.

Unchanged source excerpt — [internal/controlplane/controlplane.go:2646–2658](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2646-L2658):

```go
	service, ok := s.services[serviceID]
	if !ok || service.Status != types.ServiceDeleting {
		return
	}
	for _, task := range s.tasks {
		if task.ServiceID != serviceID {
			continue
		}
		if task.ActualStatus != types.TaskRemoved {
			return
		}
	}
	if err := types.ValidateServiceTransition(service.Status, types.ServiceDeleted); err != nil {
```

ReportTaskStatus invokes finalization after accepting removed, and detaches task volumes at that point. Its task/node ownership and lifecycle guards still apply. A late running report cannot resurrect stopped ownership merely because Docker once had a live object. Tests cover failed-task removal during deletion and rejection of a running resurrection, making the permitted cleanup transition visible without redefining the lifecycle.

The service is then marked deleted and an event is appended; the retained record is not necessarily erased immediately. Retention is a later concern with its own preservation rules. Container deletion also does not automatically imply destruction of all volume data. Local-volume claims, attachment bookkeeping and actual named-volume data have separate lifetimes; Chapter 32 examines that distinction. An operator should never use broad volume pruning as the hidden final step of service deletion.

A fresh default server process complicates the protocol because it loses the service and task maps. Surviving managed Docker objects can outlive the records that explain why they should be removed. This is a process-durability limitation rather than evidence that labels are useless. Labels support adoption and scoped cleanup while identities remain available; they do not reconstruct every desired replica count, deployment history or secret reference.

A cleanup audit should also distinguish request identity from object ownership. Namespace selection restricts which service the caller sees, while the worker label check restricts which runtime object the agent may remove. Those protections occur at different layers and neither replaces the other. An administrator reading an old incident record should match the original namespace, service ID, task ID, node ID and full container ID before taking a manual action. Reusing a friendly service name after a previous run is insufficient, because a new service can have the same name and a different owner identity. Retaining the deletion record makes that comparison possible until retention deliberately expires it.

## Atlas Lab: Preserve an Unrelated Container

Start with the disposable pinned source copy and Go 1.25. The smallest useful experiment runs the current agent, Docker-adapter and control-plane fixtures. Keep an explicit list of the named tests rather than interpreting an unrelated green suite as evidence of this failure window.

```bash
go test ./internal/agent -run 'TestReconcile(RemovesAssignedStoppedTask|DoesNotRemoveNonManagedAssignedContainerID|RemovesUnassignedManagedContainers|IgnoresNonManagedContainers)$' -count=1 -v
go test ./internal/docker -run 'Test(StopContainerAlreadyStoppedIsSuccess|RemoveContainerAlreadyRemovedIsSuccess)$' -count=1 -v
go test ./internal/controlplane -run 'Test(DeleteService|AgentTaskStatusAllowsFailedTaskRemovalDuringDeletion|AgentTaskStatusCannotResurrectStoppedTask)' -count=1 -v
```

Expected assertions establish idempotent adapter behavior, label-aware agent removal, repeated deletion intent and finalization after agent return. The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) records the fake/local assertions with caching disabled and explicitly lists the unconfigured real-Docker integration test as skipped. They do not by themselves inject a real daemon failure. A book-side failure fixture may wrap the fake runtime to fail the first RemoveContainer and delegate the second call; it is a teaching extension and needs its own acceptance test. Do not edit the immutable application fixture or present an unimplemented wrapper as an observed result.

For the separate real Atlas experiment, create only run-owned containers and a deliberately unrelated sentinel. Record each full ID before requesting deletion. Pause only the owned agent to observe the deleting window, resume it, then inspect the specific task containers and sentinel independently. If using a disposable daemon or proxy to inject removal failure, document that boundary and verify the failure happened at remove rather than at stop or assignment retrieval.

Abort when a selector contains no recorded task/node identity, an inspected object lacks expected labels, or the sentinel changes. Cleanup must remove the exact run-owned residual IDs after restoring connectivity. There is no legitimate broad-prune shortcut for a missing acknowledgement. Store request/status snapshots, runtime inspection and final sentinel proof separately, with UTC timestamps and command exits. Until such a record is attached, these remain expected experiment instructions.

## Exercises

1. Why does repeated delete of an existing deleting service succeed while delete of an unknown service may return not found?
2. A stopped container remains after the first remove failure. Identify which component retries and why the server must not finalize yet.
3. A task's stored ContainerID points at an unmanaged sentinel. Explain why ownership labels are checked before removal and what evidence should remain.
4. After all task records say stopped, an operator deletes every local Docker volume. Identify both unsupported assumptions and design a scoped finalization observation instead.

[Worked answers](../solutions/ch18.md) justify the cleanup decisions. The chapter's evidence ledger remains source-inspected until the specific failure injection and runtime observations have matching command records.

## Development history and source references

Original development prompts 16, 25 supply the requested scope. The inspected implementation history includes [2084f5f77bd3](https://github.com/alekpopovic/orch/commit/2084f5f77bd35ba2a4114d29c7e5588c0fd1f3e7), [66cfb7049fc1](https://github.com/alekpopovic/orch/commit/66cfb7049fc1fbceeec9e36a7067febe8cbab698). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L1-L558)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L1-L2770)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L1-L951)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L1-L623)
- [docs/RECONCILER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md#L1-L90)
- [docs/RELIABILITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RELIABILITY.md#L1-L120)
