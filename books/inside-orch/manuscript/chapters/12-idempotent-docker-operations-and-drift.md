# Chapter 12 - Idempotent Docker Operations and Drift

An Atlas task was created, but the agent lost the response before the control plane recorded its container ID. The next polling pass asks for the same work again. If create always means allocate another container, retries become a duplication mechanism. If create instead searches for the task's existing runtime identity, a retry can converge. The difference lives in concrete labels, lookup behavior and error handling rather than in the word idempotent.

You should already know lifecycle ownership and the executable's memory boundary. This chapter follows the Runtime interface into the Engine adapter and back through agent adoption. You will predict repeated operations, explain a manually stopped or missing container, and reject cleanup that cannot establish ownership. Docker socket permission is part of the experiment's privilege boundary, not a harmless prerequisite to tick off.

## A Typed Runtime Boundary

The runtime interface names image pull, container create/start/stop/remove, inspection, managed-container listing and log streaming. Health probes belong to the agent’s separate checker dependency, rather than a Runtime interface method. Its arguments use typed ContainerSpec, ContainerID and status structures. Controllers can express intent without importing Engine client details, while the agent owns the adapter that actually changes containers. [Claim ch12.runtime](../../validation/evidence/ch12.json).

ContainerSpec contains more than image and name. It can carry environment, published ports, labels, resource limits, security context, command and volumes. Support in that type is not proof that every application path populates every field. The agent copies task.Command and volume mounts into the spec, but omits Resources in its creation literal at this baseline. Direct adapter resource tests and ordinary service enforcement are therefore distinct claims.

The Engine adapter validates the spec before asking Docker to create it. It builds configuration and HostConfig using the supplied fields, then passes them to the client. An invalid image or identity should fail before an ambiguous side effect. A successful create response yields a container ID, but running is a separate operation; the agent reports created before StartContainer and running afterwards.

FakeRuntime implements the same interface with in-memory containers, an operation log and injected failures. Its create path is synchronized and keyed by task ID. Tests can assert a sequence such as pull, create, start without needing a daemon. The fake does not model kernel networking, cgroup enforcement, registry availability or every Engine error. Passing a fake test is valuable protocol evidence within that model, not a substitute for real adapter integration.

## Managed Labels as Resource Identity

managedLabels copies supplied labels and overwrites the orchestrator's identity labels: managed marker, service ID, task ID, node ID and version. These labels allow the agent and adapter to rediscover a container when an earlier response was lost. Container name alone is not the identity contract; names can collide and a manually created container can resemble an expected name.

[internal/docker/docker.go, lines 486–497](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L486-L497) at the locked revision.

```go
func managedLabels(spec ContainerSpec) map[string]string {
	labels := make(map[string]string, len(spec.Labels)+5)
	for key, value := range spec.Labels {
		labels[key] = value
	}
	labels[ManagedLabel] = "true"
	labels[ServiceIDLabel] = spec.ServiceID
	labels[TaskIDLabel] = spec.TaskID
	labels[NodeIDLabel] = spec.NodeID
	labels[VersionLabel] = strconv.FormatInt(spec.Version, 10)
	return labels
}
```

The Engine create operation first searches for a managed container with the same task ID. If it finds one, it returns that ID rather than creating again. If ContainerCreate returns a conflict, it repeats the lookup to recover a possible concurrent creation. Other lookup or create errors are propagated. [Claim ch12.create](../../validation/evidence/ch12.json).

That lookup is narrower than a complete spec comparison. The adapter's task-based idempotence must be combined with the agent's richer adoption checks before treating a discovered container as correct current work. The agent compares managed/node/task/service/version metadata and, when available, image identity. It does not compare every environment value, port binding, mount or security field. Exact task identity and full desired-spec equivalence are different invariants.

The ordinary service case uses a nonempty ServiceID. Finite jobs introduce an additional edge: taskWorkloadID labels their workload as job-<JobID>, while the shared matching helper compares the service label with task.ServiceID. That discrepancy needs its own job adoption test; do not extend a service-adoption result to every workload merely because both use the same create function. Chapter 31 follows the finite-work path separately.

An untrusted actor with Docker socket access can manipulate labels and runtime objects. Labels are useful engineering metadata, not a security boundary against that actor. Treat the worker and its daemon as part of the trusted computing base. A cleanup command must not assume that every container whose label says orch.managed belongs to this particular book run.

## Repeated Create, Start, Stop, and Remove

CreateContainer's first retry can return the existing ID. StartContainer treats Docker's not-modified response as success, which lets a repeated start converge on already-running state. StopContainer first inspects; a missing or already-stopped container is successful completion of the desired stop. RemoveContainer similarly treats not-found as success. [Claim ch12.operations](../../validation/evidence/ch12.json).

[internal/docker/docker.go, lines 191–219](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L191-L219) at the locked revision.

```go
func (r *EngineRuntime) CreateContainer(ctx context.Context, spec ContainerSpec) (ContainerID, error) {
	if err := spec.Validate(); err != nil {
		return "", err
	}

	existing, err := r.findContainerForTask(ctx, spec.TaskID)
	if err == nil {
		return existing.ID, nil
	}
	if err != nil && !errdefs.IsNotFound(err) {
		return "", err
	}

	config, hostConfig, err := dockerContainerConfig(spec)
	if err != nil {
		return "", err
	}
	response, err := r.client.ContainerCreate(ctx, config, hostConfig, &network.NetworkingConfig{}, nil, spec.Name)
	if err != nil {
		if errdefs.IsConflict(err) {
			existing, findErr := r.findContainerForTask(ctx, spec.TaskID)
			if findErr == nil {
				return existing.ID, nil
			}
		}
		return "", fmt.Errorf("create container for task %s: %w", spec.TaskID, err)
	}
	return ContainerID(response.ID), nil
}
```

These semantics eliminate several normal retry hazards. They do not mean every call is free of side effects or that any error can be ignored. A permission failure, unavailable daemon or incompatible configuration still matters. In particular, CreateContainer must not interpret an arbitrary inspection failure as proof the container is absent. The agent fixture verifies that Docker unavailability does not trigger reckless recreation.

There is also a separation between repeating the same operation and changing intent. Reusing a task ID with a different version or image is not necessarily an idempotent retry. The agent can identify mismatched managed metadata, remove a container that belongs to the same assigned task/node scope, and then create correct work. Such replacement is an explicit convergence decision, not a hidden property of create.

The creation/reporting failure window is easy to describe. Docker creates container C; the agent tries to report created with C's ID; the HTTP request fails or its response is lost. On a later pass the server can still present a task without that ID. The agent must search labels and adopt C before creating another. A retained task ID makes that recovery possible; a fresh default server that forgets the task entirely is a different process-durability problem.

| Repeated request | Baseline adapter response | Important limit |
| --- | --- | --- |
| Create same task identity | Return existing managed container when found | Lookup is not full spec equivalence |
| Start running container | Not-modified accepted | Other Engine errors returned |
| Stop stopped/missing container | Success | Ownership must already be established |
| Remove missing container | Success | Remove can delete attached anonymous volumes |

The remove implementation requests RemoveVolumes. That makes cleanup scope particularly important for storage experiments. A teaching fixture should never attach a user's real data merely to demonstrate retry behavior. Keep local volume cases explicitly separate, with exact run-owned names and a clear record of which data is disposable.

## Drift From Manual Docker Changes

A user can stop or delete a managed container outside the agent. currentTaskContainer first inspects the task's recorded container ID, then falls back to managed node/task lookup. A missing container generates a drift observation when task state implies one should exist. A matching stopped service container can be started again; a nonzero exit is instead reported failed according to the execution path.

The agent records three drift categories: managed container missing, unexpected managed container and managed-container state mismatch. Those categories describe observed discrepancies. They do not imply a centralized durable incident store; the configured recorder/logger determines where the observation goes. A test can verify the category without claiming an operator actually saw a production alert.

Removal requires its own identity check. A recorded ContainerID can point at a nonmanaged or differently owned object; the agent must not blindly remove it because the task says so. removableAssignedContainer checks the managed marker plus node and task ownership. The focused fixture verifies that a nonmanaged recorded container is not deleted. [Claim ch12.cleanup](../../validation/evidence/ch12.json).

cleanupUnassigned lists managed containers for the current node and removes those whose task is absent from the fetched assignment set. This is meaningful only if that assignment set is successfully obtained and authoritative for the scope. In the inspected code, a failure to list assignments returns before cleanup. A temporarily unreachable server therefore differs from a successful empty assignment response. That distinction protects against one dangerous outage-to-deletion conversion.

A successful empty set after a fresh memory-backed server restart remains a different risk: the server may have genuinely forgotten tasks while containers still exist. The agent cannot infer the former desired state from the missing API records alone. The safe lab records exact container IDs before restart and separates this scenario from ordinary drift repair. Do not promise that container adoption repairs lost authoritative service intent.

## History and Atlas Lab

The Docker adapter entered the project in [2969dfcebd0b15dea99cdf97b5ccdd1ddfd36b41](https://github.com/alekpopovic/orch/commit/2969dfcebd0b15dea99cdf97b5ccdd1ddfd36b41). The deterministic fake arrived in [c69f9ffa830284692aabf9e65ab9eb1f79d3a114](https://github.com/alekpopovic/orch/commit/c69f9ffa830284692aabf9e65ab9eb1f79d3a114), and [cf9769553d6599d798fafaffe1495d3d739fe993](https://github.com/alekpopovic/orch/commit/cf9769553d6599d798fafaffe1495d3d739fe993) added drift-specific recording and stronger matching. Original prompt 06 is retrospective intent; prompts 33 and 41 relate to the later fake and drift work. The patches show changed code and assertions, not an automatic record of a live Docker experiment.

The safe source-only lab runs the adapter-client and FakeRuntime tests together with the agent's missing/stopped/mismatched/nonmanaged cases. Use the disposable source copy with Go 1.25 and no external integration flags. The [focused execution record](../../validation/labs/ch12/focused-tests.json) passed and names its exact selection. No daemon or host containers were used by this run.

```sh
go test ./internal/docker ./internal/agent \
  -run 'TestFakeRuntime|TestCreateContainer|TestStopContainer|TestRemoveContainer|TestReconcileAssignedTask(Recreates|Restarts|Replaces)|TestReconcileIgnoresNonManaged|TestReconcileDoesNotRemoveNonManaged' \
  -count=1 -v
```

Read the resulting operation strings alongside created-spec and container-count assertions. Two create requests can appear in an operation log while only one container exists; counting calls alone would misclassify idempotence. For a manually missing container, expect a new container for the same orchestration task and an updated report. For an unrelated nonmanaged container, expect no removal operation against its ID.

An optional real experiment needs a dedicated disposable daemon or VM and the environment contract's exact ownership record. Stop only the recorded Atlas container, observe the agent's response, then delete only that same owned ID to exercise missing-state repair. Keep image ID, task ID, labels and before/after inspection in the log. Stop the agent before final cleanup so it does not recreate what the cleanup removes. Never use docker system prune or a global managed-label deletion.

Consider a manual label change on an otherwise running Atlas container. A task-ID lookup can now fail to find the object, while its process still owns a published port. Creating another container may then produce a port-binding failure rather than restoring service. The right incident record includes the task's recorded container ID, the inspected object's ownership labels and the exact Engine error. A broad search by image name would be dangerous because another workload can use the same image legitimately. Ownership mismatch is therefore both a convergence problem and an authorization boundary.

For the lab, use a fake runtime to present that mismatch first. Assert which object was inspected and that the unrelated object was not stopped or removed. If the same scenario is later repeated on a real daemon, create the altered object within the run's resource inventory and restore or remove only that object. A successful replacement does not justify sweeping all containers with similar names, nor does a failed replacement justify changing the ownership predicate to accept arbitrary running processes.

## Exercises

1. Why can two CreateContainer operation records still establish an idempotent result? Name the additional assertion needed.
2. Describe the safe response when InspectContainer returns a daemon transport error rather than not-found.
3. A task's ContainerID points at a user's nonmanaged container. Trace the checks that prevent deletion and explain why the task record alone is insufficient.
4. Design a real adoption experiment after a lost created-report response. State what it proves and why it does not prove default-server process durability.

[Worked answers](../solutions/ch12.md) distinguish task identity, runtime identity and desired-spec comparison. Preserve those distinctions when interpreting drift, and keep the authority to touch Docker resources narrower than the convenience of a broad label selector.
