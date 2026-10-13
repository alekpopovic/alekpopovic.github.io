---
layout: post
title: "A ready server may have forgotten your cluster"
description: "Trace active state ownership before using a healthy HTTP response as evidence that an orchestrator recovered its workloads."
category: Reliability
book_id: inside-orch
chapter_slug: 06-follow-one-request-through-the-control-plane
illustration: package
tags: [orchestration, recovery, persistence, Go, readiness]
---

An operator restarts a control-plane process. The HTTP endpoint answers, the application still serves requests, and PostgreSQL is reachable. Those observations look reassuring. They answer three separate questions, however: whether an HTTP handler is available, whether a workload remains alive, and whether a database accepts connections.

They leave the recovery question open: does the new process know which services, versions, tasks, and agents it owns?

## Find the owner of active state

In the pinned orch source, normal `orch-server` startup constructs `controlplane.NewMemoryService`. The surrounding configuration accepts a database URL, and the repository contains a PostgreSQL store. Neither fact changes that constructor. The active implementation remains the memory service selected by the executable. See the [server composition root](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L142-L149).

This is a useful source-review technique for any service with interchangeable backends. Begin at startup, follow the concrete value supplied to handlers and controllers, and identify where its records live. Reading a persistence interface alone cannot establish that production requests reach it.

The distinction also changes backup planning. A PostgreSQL backup protects the records written to PostgreSQL. It cannot capture live records that this executable keeps elsewhere. State ownership has to be established before writing a recovery runbook around a database restore.

## Give readiness a precise meaning

At this snapshot, orch's `/readyz` handler returns a fixed `ready` response and a current timestamp. It does not reconstruct missing services, compare persisted task identities, or prove that agent credentials survived a restart. Read the [actual readiness handler](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L440-L442).

A readiness result can still be useful within that scope. The mistake is assigning it a larger meaning than its checks establish. A deployment gate should name the conditions it requires: API availability, durable state availability, controller authority, or successful workload recovery. Each needs its own evidence.

For an orchestrator, an existing container is another independent observation. Docker can keep a workload running while its control plane loses the records needed to manage it. A responding application does not reveal whether the new server can scale that service or resume its interrupted rollout.

## Design the experiment around preserved identity

Use a disposable source-pinned environment. Before restarting the server, record a service identity, its version, task identities, and the expected node relationship. After a fresh process starts, query those same identities. Creating replacement objects after restart would conceal the failure you intend to investigate.

Then check the management path: can the server recognize the existing task, authorize its agent report, and continue the intended operation? Keep application reachability in a separate observation column. An answer can be positive for traffic and negative for orchestration ownership.

These are proposed acceptance criteria, not a report of an executed recovery experiment. The [control-plane implementation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go) supplies the source boundary that the experiment should test.

## A persistence change needs a recovery contract

A durable backend must support the domain operations the API and controllers actually use, including later workload features and credentials. Replacing a constructor without checking interface coverage, transaction behavior, and restart recovery leaves important questions unanswered.

Write the acceptance test before calling the integration complete. Terminate the process after a committed mutation, restart it, and verify the same logical objects. Add a case where Docker created a container before its status report arrived. Stable identity and repeatable reconciliation become essential when the outcome of an external effect is uncertain.

A green endpoint earns its documented meaning. Recovery earns a stronger claim only after the system demonstrates preserved ownership across a real process boundary.
