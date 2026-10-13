---
layout: post
title: "An offline node is not proof that its workload stopped"
description: "Heartbeat expiry supports a replacement decision, but preventing a disconnected workload from continuing requires a separate authority boundary."
category: Reliability
book_id: inside-orch
chapter_slug: 19-offline-nodes-draining-and-rescheduling
illustration: network
tags: [orchestration, heartbeats, partitions, fencing, recovery]
---

A worker stops sending heartbeats. The control plane marks it offline and schedules replacement work elsewhere. Meanwhile, the old worker still reaches the application database and its container keeps running.

Both observations can be true. Losing communication with the controller does not establish that a workload lost power, runtime access, or permission to affect another system.

## Read what the timeout changes

In the pinned orch implementation, `MarkStaleNodesOffline` compares heartbeat timestamps with a cutoff. It updates eligible nodes to offline, records lost-task state, emits an event, and reconciles services when nodes have expired. This is a control-plane state transition. See the [timeout implementation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L670-L712).

The code does not establish that Docker on an unreachable worker stopped a container before the replacement decision. That is a different fact requiring another observation or mechanism.

This distinction is especially important for side effects. In an illustrative report-processing service, an old and replacement instance could both reach the system receiving reports. Whether duplicate work occurs depends on that application's coordination and idempotency contract; a missed heartbeat alone does not resolve it.

## Inspect the stateful exception

orch's lost-task handling marks active tasks with a `NodeLost` condition. For services not marked stateful, it also changes desired state to removed and actual state to failed, with a `node_lost` reason. Stateful services retain their task state rather than following that same automatic replacement path. See [markNodeLostTasksLocked](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2073-L2093).

That exception is useful evidence of a cautious replacement policy. It does not create replicated storage, revoke an old writer's database credentials, or prove exclusive access to data. Keeping the uncertain task visible and enforcing exclusive write authority are separate responsibilities.

The incident interface should reflect that uncertainty. “Controller cannot reach node” conveys a known observation. “Workload definitely stopped” would require evidence the controller has not obtained through this timeout path.

## Fencing belongs where authority is enforced

A stronger design might use node isolation or an external resource that rejects writes from an obsolete owner. For example, a proposed monotonic ownership token can help only if the receiving system checks it before accepting each protected operation.

Merely storing a token in the controller is insufficient. The disconnected workload might continue presenting an older token to a resource that never validates it. Similarly, a controller leadership lock limits controller participation; it does not automatically revoke authority from an existing application container.

These are architectural options, not implemented orch fencing guarantees. Their acceptance tests must include the resource that ultimately decides whether the operation is allowed.

## A drain exercises a different failure path

A planned drain updates node status and reconciles workloads through an explicit control-plane operation. With a reachable worker, task removal can flow through the normal agent path. See [DrainNode](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L994-L1022).

Successful drain tests therefore do not establish partition safety. A disconnected agent cannot necessarily fetch its new desired task state. In orch, assigned-task reconciliation follows a successful heartbeat response in the [agent loop](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L155-L175).

## Observe both sides of the partition

For a disposable experiment, interrupt only worker-to-controller communication while keeping the workload's external destination reachable. Record the server's node/task state and independently observe whether the old workload still acts. Then inspect replacement behavior, recovery after connectivity returns, and residual containers.

Those are proposed observation criteria, not recorded test results. A useful recovery claim names the scope proved: detection, replacement, eventual cleanup, or rejection of stale work. It earns stronger exclusivity language only when the final authority boundary has been tested.
