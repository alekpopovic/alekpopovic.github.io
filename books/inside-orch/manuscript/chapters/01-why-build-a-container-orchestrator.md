# Chapter 1 - Why Build a Container Orchestrator?

## A Small Cluster Is Still a Distributed System

At nine in the morning, the Atlas operator has three Docker hosts, an HTTP service, and a deployment checklist. The checklist says to pull the new image, stop the old container, start its replacement, and check an endpoint. At nine fifteen, a laptop connection disappears between the stop and start commands. Another operator repeats the checklist on a different host. The team now needs an answer to a question the shell history cannot settle: which version should be running, where, and who is responsible for getting it there?

That is a sufficient problem to study orchestration. It does not require thousands of containers. Multiple machines, delayed observations, and interrupted actions already create a distributed system. Atlas needs repeatable intent, identifiable work, and a way to compare desired state with reports from workers. The smallest useful controller must decide what happens after an action succeeds but its acknowledgement is lost. Adding a pleasant deployment command without answering that question merely moves the uncertainty behind a different interface.

By the end of this chapter, you should be able to trace a service request through the actual server and agent, identify the owner of each state, and decide which engineering claims the default binary supports. You should also be able to explain why building a small orchestrator can be a useful learning or internal-tool exercise without presenting its existence as a production recommendation. The rest of the book follows those questions through source rather than treating a list of modules as a finished platform.

Atlas uses the name `atlas-api` for the continuing case study. Its first job is a stateless HTTP endpoint on disposable infrastructure. Later chapters introduce update failures, disconnected workers, resource constraints, and finite jobs. This identity is a teaching scenario, not an assertion that this repository has operated a particular commercial cluster. We can reason concretely about ownership and failure without inventing deployment history, adoption numbers, or availability measurements.

An orchestrator is useful when repeating a desired result is more valuable than remembering a sequence of imperative commands. “Keep two replicas of this service at this version” survives an operator leaving the terminal. “Run these six commands” does not specify what to do halfway through a failure. The distinction also changes how errors should be reported: an accepted service is a stored intention, while a running task is a later observation. The API can succeed before an image pull fails.

For a small team, this separation can clarify operational responsibilities. It can also create responsibilities the team previously delegated to an established platform: identity, authorization, capacity, durable state, safe replacement, observability, upgrades, and recovery. Evaluate those obligations before choosing to run a custom system. A source-based book can teach how they fit together; it cannot transfer a production guarantee from the author's confidence to your environment.

## Who Owns Desired and Observed State?

The domain begins with five nouns. A service describes desired workload configuration. A task identifies one execution attempt for a service version. A node describes a worker and its reported capacity and status. An agent executes work assigned to that node. A Docker container is the local runtime object the agent creates or adopts. These nouns are related, but none is a synonym for another. Deleting a service record is not equivalent to stopping a container on a disconnected worker.

The [ServiceSpec definition](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L208-L226) contains image, replicas, environment, resource requirements, security context, and other declared inputs. The server stores a service with an ID and deployment version. A task then binds an execution identity to a node and tracks desired and actual status. The agent polls its task assignment and performs the image/container operations through an interface. The [container creation call](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253-L265) is the concrete bridge from task identity to a local Docker request.

| Object | Owner of the relevant decision | Evidence it does not supply by itself |
| --- | --- | --- |
| Service | Operator intent accepted by control plane | A container is running |
| Task | Server assignment and agent reports | Remote side effect happened exactly once |
| Node | Registration, heartbeat and monitor | A silent worker has stopped serving |
| Agent | Local execution and observations | Cluster state survives server replacement |
| Container | Docker daemon on one host | Other replicas agree with this version |

Consider one Atlas replica. The CLI submits a service. The API checks the request and invokes the control-plane service. The server creates or reconciles task state. The worker polls the assignment, pulls the image, creates a labeled container, starts it, and reports progress. A health observation may follow. Each step has an identifiable owner and a failure boundary. The word “deployment” spans the sequence; it does not turn the sequence into one transaction.

The agent does not decide that the service needs three replicas instead of two. The scheduler does not start a container. The Docker adapter does not know whether a deployment is commercially successful. Keeping those boundaries narrow makes errors easier to investigate. When Atlas has a task but no container, inspect the agent/runtime path. When there is no task, investigate control-plane intent and placement. When Docker shows a container but the API does not, investigate observation, identity, and state ownership before creating a replacement.

There is also a difference between desired state and reported state. A report can be stale, delayed, or lost. The server's status is a record of what it accepted, not an independent measurement of the worker at the instant you read it. Later laboratories compare API state, agent reports, Docker inspection, and a direct endpoint request. Agreement across those observations is stronger evidence than a single green status field, although it remains scoped to the observation window.

## What the Default Binary Actually Runs

Start the architecture review at the composition root. In [server startup](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L142-L148), the selected state owner is explicit:

```go
	controlPlane := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope), controlplane.WithClusterPolicy(cfg.ClusterPolicy), controlplane.WithRetentionConfig(cfg.Retention))
	controlPlane.SetNotificationDispatcher(notifications.NewDispatcher(controlPlane, nil))
	serverMetrics := metrics.NewServer()
```

Exact source: [cmd/orch-server/main.go:146–148](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L148).

This is **runtime-integrated** behavior: ordinary startup constructs `controlplane.NewMemoryService`, attaches notification dispatch, and creates server metrics. The memory service allocates maps for nodes, services, tasks, deployments, secrets, and additional objects. Those maps belong to the process. A database URL does not change the selected constructor. The optional startup schema check opens PostgreSQL for compatibility inspection and closes the runner; it is not a storage injection mechanism.

The server does start useful loops. The [GitOps, cron and scheduler construction](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L165-L190) is followed by usage snapshots, retention pruning, the rollout controller, and node monitoring. Optional DNS and a separate debug listener have their own configuration gates. This is more specific than saying “the server runs controllers.” It tells us which controllers, which store they share, and which effects disappear if their goroutine stops.

Several substantial packages are absent from this graph. PostgreSQL store code is an **implemented package**, not the active server service. Standalone reconciliation is another implemented package; default memory mutations perform a different immediate reconciliation path. Leadership and autoscaling packages are not constructed by ordinary startup. Calling them implemented is fair. Saying two default server processes form an HA control plane, or an autoscaling policy automatically enables a metrics-driven loop, would add behavior the composition does not provide.

Even a constructed scheduler needs a caller-sensitive explanation. [Immediate service reconciliation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2249-L2316) chooses ready, volume-eligible nodes and creates assigned tasks. The independent scheduler plans pending tasks. Ordinary service tasks can therefore be assigned before the planner encounters them. An algorithm's presence does not mean every assignment passed through it. We will trace this difference before teaching resource or placement guarantees.

The history helps explain how these boundaries arose. [Architecture conventions](https://github.com/alekpopovic/orch/commit/6f90183927991506de435a55582b5c283212ff09) established the project shape. The [first REST API](https://github.com/alekpopovic/orch/commit/64a0725387b8130be988948b81774aea7051c718) selected an in-memory implementation. Original development prompts 00 and 26 describe architectural intent and a review request, but early prompt files were committed after the June implementation. They are retrospective associations, not proof that a particular instruction was executed before a particular commit.

## The First Capability Boundary

The first Atlas failure window is a server process replacement. Before the interruption, maps contain the service and its tasks. During the interruption, Docker may continue running containers on workers. After the replacement, a new memory service has fresh maps. The continuing existence of a local container does not recreate the missing service intention. Conversely, an empty API response does not prove no old container remains. Those are different observations about different owners.

This explains why a readiness endpoint cannot establish recovery. The [health and readiness handlers](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L436-L442) return fixed success responses. They show that the selected handler is reachable. They do not query durable cluster state, compare replicas, establish leadership, or verify that old credentials remain valid. Atlas should record reachability and workload recovery separately rather than using the former as a substitute for the latter.

There is a precise engineering choice here. For disposable learning, a memory-backed control plane makes experiments cheap and state ownership visible. For a system whose desired state must survive process loss, that composition is insufficient. Replacing it requires more than choosing a database library: service semantics, all required object types, transaction boundaries, credential recovery, migrations, and process restart tests must agree. The book studies those requirements without silently patching the baseline to claim they already exist.

Use the capability question at every new subsystem: where is this behavior connected to the running system? Then ask who owns its state, what side effect it performs, and what evidence would distinguish success from a convincing status report. A package, schema table, test name, or completed progress tracker can help you navigate. None independently answers all four questions. This discipline is valuable even if you eventually choose a different orchestrator.

## Atlas Lab: draw the actual boundary

Prerequisites are the immutable source snapshot, Python, and a disposable directory for any later builds. No daemon or database is needed for this first source experiment. From the website repository root, read the lock and inspect the composition without running application commands inside the website source tree:

```bash
python3 -c 'import json; print(json.load(open("books/inside-orch/evidence/source-lock.json"))["baseline_sha"])'
sed -n '142,234p' books/inside-orch/evidence/orch/cmd/orch-server/main.go
```

Draw the server, memory owner, API, active loops, worker, and Docker daemon. Put PostgreSQL beside the graph as a package/migration boundary, without an arrow that pretends it owns normal server state. Annotate the worker connection as polling/reporting, and annotate container existence as local daemon state. Success means each arrow has a constructor or call site; reject a diagram whose only support is a roadmap sentence.

The source map and exact SHA were mechanically checked during this edition's research. The process-restart and real-container comparisons are separate experiments, not results of these two commands. Record your own UTC time, command exit status, source SHA, and diagram notes. This source-only step creates no containers or services; cleanup removes only your drawing or notes if desired. Retain the map as the initial Atlas evidence artifact.

## Exercises

1. Explain why an accepted service and a healthy replica are separate facts. Name the owner of each fact.
2. Find the constructor that owns live state. Explain why a successful PostgreSQL migration does not change its selection.
3. An operator sees `/readyz` succeed after restarting the server and declares recovery complete. Identify two observations still missing.
4. Decide whether Atlas should use this baseline for a disposable training cluster or a payroll workload requiring restart-safe desired state. Justify the decision using composition rather than product labels.

[Worked answers](../solutions/ch01.md) connect each decision to its specific source boundary. The architecture decision for the next chapter is to follow interfaces and constructors before searching for additional features. Claims are indexed in the chapter evidence ledger; CAP-001, CAP-003, CAP-004 and DOC-001/002 remain controlling boundaries for later explanations.
