---
layout: post
title: "Follow a resource limit all the way to Docker"
description: "A valid resource field and a tested scheduler do not prove that a running container receives the corresponding CPU and memory controls."
category: Verification
book_id: inside-orch
chapter_slug: 05-service-specifications-resources-and-ports
illustration: queue
tags: [Docker, resources, CPU, memory, scheduling, verification]
---

A deployment declares CPU and memory. Validation accepts it, the scheduler has capacity tests, and the Docker adapter knows how to set limits. It is tempting to conclude that the container will receive those controls.

The conclusion depends on a chain of transformations. A field can be understood at several layers and still disappear before the final runtime request.

## Separate three resource questions

Consider a hypothetical service with three replicas, each requesting 500 millicores and 256 MiB. Its requested aggregate is 1,500 millicores and 768 MiB. That arithmetic describes capacity accounting. A larger declared limit describes a different intended boundary for each running container.

Parsing answers whether the values are valid. Placement answers whether a chosen node satisfies the planner's admission rules. Runtime enforcement answers what Docker actually configures. Evidence for one question does not automatically settle the others.

orch represents requests and limits in [ResourceRequirements](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L516-L519). The names establish the domain shape. To establish enforcement, follow those values out of that shape and into the container-creation call.

## Check the adapter and its caller

The Docker adapter's conversion is concrete: `Memory` comes from `spec.Resources.Memory`, and `NanoCPUs` comes from `spec.Resources.CPUMilli * 1_000_000`. A supplied value can therefore become Docker host configuration. See [dockerContainerConfig](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L412-L451).

Now inspect the active agent. Its `ensureTask` method constructs a `ContainerSpec` with image, task identity, environment, ports, security context, command, and volume mounts. In this pinned source, that literal does not populate `Resources`. The adapter's supported feature is consequently not evidence that ordinary service containers receive their declared limits through this path. See the [agent's create call](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253-L266).

There is an earlier transport boundary too. The [AgentTask response type](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L130-L137) carries several workload fields but has no explicit resource requirements field. A complete repair must inspect the whole contract rather than adding an assignment at the final call and assuming the required data exists.

## Verify which placement path your service uses

A similar question applies to scheduling. The standalone planner has meaningful constraint logic. Normal MemoryService service reconciliation can create tasks already assigned to ready nodes. Those paths require separate analysis; planner tests alone cannot prove that an ordinary service followed the planner.

The [service reconciliation method](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2249-L2311) makes that distinction visible. Describe guarantees according to the path actually executed, including any checks that path performs. Avoid turning a useful library invariant into a system-wide capacity promise.

## Use two complementary acceptance tests

A focused test should capture the `ContainerSpec` the agent passes to its runtime and compare its resource values with the assigned workload contract. This identifies missing propagation without requiring a live Docker daemon.

A disposable Docker integration test should then inspect the created container's `HostConfig.Memory` and `HostConfig.NanoCpus`. That proves the final API configuration for the tested path. Workload measurements can investigate behavior under pressure, but they should remain separate from assertions about configured fields.

These are proposed tests, not executed results. The practical review rule is to preserve the field's identity through parsing, storage, assignment, transport, and runtime conversion. When a link is absent, document the gap and test the eventual change at both the caller boundary and Docker boundary.
