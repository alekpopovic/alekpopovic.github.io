# Appendix D - Worked Exercises and Design Solutions

A useful exercise produces an artifact another reader can inspect: a state trace, a calculation, a failing boundary, a test result or a recovery decision. It does not reward repeating the word reliable. The chapter exercises introduce mechanisms where they are taught; this appendix adds twenty-four substantial practice problems that combine those mechanisms and keep questions separate from worked answers.

There are eight developer, eight DevOps and eight architect exercises. Each has a stable ID, prerequisites, an estimated duration, a pinned source mechanism, a required artifact, hints and three objective scoring criteria worth two points each. Full credit is six points. A correct answer can conclude that the requested guarantee is absent; inventing missing persistence or enforcement loses credit even if the proposed design sounds plausible.

The eight developer entries are executable offline through existing pinned tests. Their tasks are source analysis and test-oracle interpretation, so no incomplete coding scaffold is required. Tests run in a separate module copy because Go internal-package rules and immutable evidence prohibit treating the Jekyll root as the application module. The GitOps test creates only a temporary local Git repository. None of these eight entries requires a Docker daemon, PostgreSQL connection or live registry.

## Additional practice index

| ID | Audience | Chapter | Required artifact |
| --- | --- | --- | --- |
| DEV-01 | developer | 10 | A three-step claim trace and the isolated test log. |
| DEV-02 | developer | 14 | A status/identity table plus the named local test log. |
| DEV-03 | developer | 18 | Two guard evaluations and a cleanup trace plus the test log. |
| DEV-04 | developer | 17 | A version/status budget table and the rollout test log. |
| DEV-05 | developer | 27 | A two-namespace lookup matrix and the namespace test log. |
| DEV-06 | developer | 28 | A race timeline and the quota test log. |
| DEV-07 | developer | 30 | A revision/service-version trace and the local Git fixture test log. |
| DEV-08 | developer | 31 | An occurrence/active-job table and both named test results. |
| OPS-01 | devops | 24 | A recovery checklist with key/ciphertext ownership and stop conditions. |
| OPS-02 | devops | 3 | A before/after identity inventory and re-enrollment decision record. |
| OPS-03 | devops | 39 | A fully specified measurement sheet with run status and a claim boundary. |
| OPS-04 | devops | 05 | A field-flow diagram from service through assignment to ContainerSpec and engine inspection. |
| OPS-05 | devops | 23 | An authentication timeline with stored-hash/client-token divergence and safe stop condition. |
| OPS-06 | devops | 19 | Two task/condition traces and a fencing risk decision. |
| OPS-07 | devops | 37 | A three-layer health table with a verification probe for each layer. |
| OPS-08 | devops | 35 | A canary/digest recovery plan with key backup, schema, downtime and rollback criteria. |
| ARC-01 | architect | 17 | A budget calculation and counterexample timeline. |
| ARC-02 | architect | 5 | A unit-correct table and an enforcement boundary statement. |
| ARC-03 | architect | 34 | A labeled future-extension dependency graph and crash-test plan. |
| ARC-04 | architect | 34 | A two-pool lock ownership diagram and a corrected release contract. |
| ARC-05 | architect | 26 | A resolver/redirect policy diagram with a zero-hit loopback oracle. |
| ARC-06 | architect | 27 | An authorization matrix for known/unknown/foreign IDs and a test-gap entry. |
| ARC-07 | architect | 25 | A syntax/resolution/content verification ladder. |
| ARC-08 | architect | 38 | A measurement contract with start/stop events, clock origin, censoring and scope. |

Read the [separate practice questions](../../exercises/questions.md) first, then compare your artifact with the [worked practice solutions](../solutions/appendix-d.md). A hint should help locate an enforcing boundary without handing you a fictional result. Estimated times assume the stated prerequisites are available; missing tools are a setup issue to record, not a reason to assert a pass.

## How to attempt an offline exercise

Make a disposable copy of the locked Orch module and use Go 1.25.0 with its declared dependencies. Run the exact test filter named in the question. Preserve command, working directory, source SHA, Go version, UTC timestamps and exit code. Read the assertion that would reject the specified incorrect behavior; a package-level pass with zero matching tests is not completion.

The delivered exercise check actually ran all eight selected command groups and observed nine requested test passes, because the cron entry intentionally includes two tests. This is evidence for those deterministic package fixtures. It does not establish Docker execution, cross-process durability or an actual production incident. A separate artifact grader accepts the serialized expected outcomes and rejects an intentionally wrong field for each executable entry; this checks grading discrimination. Separately, eight controlled semantic mutations in disposable source copies were each rejected by the selected package tests, as recorded in the [mutation results](../../validation/exercises/mutation-runs.json). Those counterexamples demonstrate sensitivity to eight specified faults; they do not establish exhaustive mutation coverage.

When a fixture uses an injected clock, name that seam. The cron package does; not every subsystem exposes the same interface. Concurrent tests may guarantee one winner while leaving the winner’s identity nondeterministic. Preserve that distinction in your answer instead of relying on timing or sleeping until a preferred goroutine wins.

## Traces, calculations and operational artifacts

For a task trace, include ID, DesiredStatus, ActualStatus, owning NodeID, service/deployment version and relevant conditions. Conditions such as node_lost remain separate metadata. Show the initial state, message or policy decision, authorization check and resulting state. Do not move failed directly to healthy to simplify a diagram: replacement gets a new identity, while cleanup has its own permitted edge.

For resource arithmetic, keep CPU in integer millicores and memory in bytes. Five replicas at 250 millicores and 128 Mi reserve 1250 millicores and 671088640 bytes. State whether other namespace reservations exist before asserting a quota decision. Requested capacity, limits forwarded to Docker and observed process consumption are three different artifacts. Arithmetic can be correct while propagation is missing.

Operational answers need a bounded target, a verification step and a stop condition. A restore plan must retain the matching envelope key and compare canary content, not merely show a successful database process exit. A memory-server restart plan must acknowledge that live intent was never written into that database. A node-loss plan must address an old process that can still run after its heartbeat expires.

Architecture answers should label proposals. A dependency graph connecting a durable service/store, transactional claim path and leader-loss cancellation is a future composition unless the source actually constructs it. Describe the smallest change and a falsifying crash window. A consensus paper or package interface supplies useful vocabulary; neither supplies proof that the default binary has activated HA.

## Chapter exercise and answer map

Use this map to revisit each chapter’s original exercises and independently worked companion. Chapter answers are separate from the twenty-four additional practice solutions, so readers can attempt either set without immediately exposing the other.

| Chapter | Exercise context | Worked answers |
| --- | --- | --- |
| 1 | [Why Build a Container Orchestrator?](../chapters/01-why-build-a-container-orchestrator.md) | [Chapter 1 answers](../solutions/ch01.md) |
| 2 | [A Repository Built for Reasoning](../chapters/02-a-repository-built-for-reasoning.md) | [Chapter 2 answers](../solutions/ch02.md) |
| 3 | [Boot the Lab and Deploy the First Service](../chapters/03-boot-the-lab-and-deploy-the-first-service.md) | [Chapter 3 answers](../solutions/ch03.md) |
| 4 | [Domain Models and State Machines](../chapters/04-domain-models-and-state-machines.md) | [Chapter 4 answers](../solutions/ch04.md) |
| 5 | [Service Specifications, Resources, and Ports](../chapters/05-service-specifications-resources-and-ports.md) | [Chapter 5 answers](../solutions/ch05.md) |
| 6 | [Follow One Request Through the Control Plane](../chapters/06-follow-one-request-through-the-control-plane.md) | [Chapter 6 answers](../solutions/ch06.md) |
| 7 | [HTTP Contracts and Compatible APIs](../chapters/07-http-contracts-and-compatible-apis.md) | [Chapter 7 answers](../solutions/ch07.md) |
| 8 | [A CLI That Operators Can Automate](../chapters/08-a-cli-that-operators-can-automate.md) | [Chapter 8 answers](../solutions/ch08.md) |
| 9 | [Persistence, Transactions, and Optimistic Concurrency](../chapters/09-persistence-transactions-and-optimistic-concurrency.md) | [Chapter 9 answers](../solutions/ch09.md) |
| 10 | [A Deterministic Scheduler](../chapters/10-a-deterministic-scheduler.md) | [Chapter 10 answers](../solutions/ch10.md) |
| 11 | [Reconciliation as Repeated Convergence](../chapters/11-reconciliation-as-repeated-convergence.md) | [Chapter 11 answers](../solutions/ch11.md) |
| 12 | [Idempotent Docker Operations and Drift](../chapters/12-idempotent-docker-operations-and-drift.md) | [Chapter 12 answers](../solutions/ch12.md) |
| 13 | [Agents, Heartbeats, and Task Reports](../chapters/13-agents-heartbeats-and-task-reports.md) | [Chapter 13 answers](../solutions/ch13.md) |
| 14 | [Health Checks That Respect Trust Boundaries](../chapters/14-health-checks-that-respect-trust-boundaries.md) | [Chapter 14 answers](../solutions/ch14.md) |
| 15 | [Events, Audits, and Notification Boundaries](../chapters/15-events-audits-and-notification-boundaries.md) | [Chapter 15 answers](../solutions/ch15.md) |
| 16 | [Log Streaming Without Losing Control](../chapters/16-log-streaming-without-losing-control.md) | [Chapter 16 answers](../solutions/ch16.md) |
| 17 | [Rolling Updates and Rollback Invariants](../chapters/17-rolling-updates-and-rollback-invariants.md) | [Chapter 17 answers](../solutions/ch17.md) |
| 18 | [Safe Deletion and Resource Cleanup](../chapters/18-safe-deletion-and-resource-cleanup.md) | [Chapter 18 answers](../solutions/ch18.md) |
| 19 | [Offline Nodes, Draining, and Rescheduling](../chapters/19-offline-nodes-draining-and-rescheduling.md) | [Chapter 19 answers](../solutions/ch19.md) |
| 20 | [Endpoint Discovery and Internal DNS](../chapters/20-endpoint-discovery-and-internal-dns.md) | [Chapter 20 answers](../solutions/ch20.md) |
| 21 | [Ingress, Host Networking, and the Overlay Roadmap](../chapters/21-ingress-host-networking-and-the-overlay-roadmap.md) | [Chapter 21 answers](../solutions/ch21.md) |
| 22 | [Autoscaling Decisions and Missing Integration](../chapters/22-autoscaling-decisions-and-missing-integration.md) | [Chapter 22 answers](../solutions/ch22.md) |
| 23 | [Authentication, Authorization, and Node Trust](../chapters/23-authentication-authorization-and-node-trust.md) | [Chapter 23 answers](../solutions/ch23.md) |
| 24 | [Encrypted Secrets and Configuration Redaction](../chapters/24-encrypted-secrets-and-configuration-redaction.md) | [Chapter 24 answers](../solutions/ch24.md) |
| 25 | [Registry Credentials and Immutable Image Identity](../chapters/25-registry-credentials-and-immutable-image-identity.md) | [Chapter 25 answers](../solutions/ch25.md) |
| 26 | [Security Contexts, Admission, and Policy](../chapters/26-security-contexts-admission-and-policy.md) | [Chapter 26 answers](../solutions/ch26.md) |
| 27 | [Namespaces and the Limits of Multi-Tenancy](../chapters/27-namespaces-and-the-limits-of-multi-tenancy.md) | [Chapter 27 answers](../solutions/ch27.md) |
| 28 | [Quotas and Usage Accounting](../chapters/28-quotas-and-usage-accounting.md) | [Chapter 28 answers](../solutions/ch28.md) |
| 29 | [Supply Chain Designs Without False Guarantees](../chapters/29-supply-chain-designs-without-false-guarantees.md) | [Chapter 29 answers](../solutions/ch29.md) |
| 30 | [GitOps, Drift, and Controlled Reconciliation](../chapters/30-gitops-drift-and-controlled-reconciliation.md) | [Chapter 30 answers](../solutions/ch30.md) |
| 31 | [Finite Jobs and Time-Based Work](../chapters/31-finite-jobs-and-time-based-work.md) | [Chapter 31 answers](../solutions/ch31.md) |
| 32 | [Local Volumes, Claims, and Workload Topology](../chapters/32-local-volumes-claims-and-workload-topology.md) | [Chapter 32 answers](../solutions/ch32.md) |
| 33 | [Extension Interfaces and a Plugin Roadmap](../chapters/33-extension-interfaces-and-a-plugin-roadmap.md) | [Chapter 33 answers](../solutions/ch33.md) |
| 34 | [Leader Election and the Durable HA Boundary](../chapters/34-leader-election-and-the-durable-ha-boundary.md) | [Chapter 34 answers](../solutions/ch34.md) |
| 35 | [Upgrades, Migrations, Maintenance, and Retention](../chapters/35-upgrades-migrations-maintenance-and-retention.md) | [Chapter 35 answers](../solutions/ch35.md) |
| 36 | [Fakes, Property Tests, Fuzzing, and Contracts](../chapters/36-fakes-property-tests-fuzzing-and-contracts.md) | [Chapter 36 answers](../solutions/ch36.md) |
| 37 | [Failure Injection and Recovery Evidence](../chapters/37-failure-injection-and-recovery-evidence.md) | [Chapter 37 answers](../solutions/ch37.md) |
| 38 | [Metrics, Dashboards, and Actionable Signals](../chapters/38-metrics-dashboards-and-actionable-signals.md) | [Chapter 38 answers](../solutions/ch38.md) |
| 39 | [Performance and Scale Tests That Say What They Measure](../chapters/39-performance-and-scale-tests-that-say-what-they-measure.md) | [Chapter 39 answers](../solutions/ch39.md) |
| 40 | [Release a System You Can Honestly Operate](../chapters/40-release-a-system-you-can-honestly-operate.md) | [Chapter 40 answers](../solutions/ch40.md) |

## Self-review and instructor guidance

First attempt a question using only its stated prerequisites. If the solution depends on an unstated constructor, clock, namespace context or resource unit, revise the question before grading. The second pass should compare every rubric criterion against the actual artifact, not against an impression that the answer sounds experienced. For a trace, distinguish wrong ownership from wrong arithmetic: both matter, but they require different feedback.

An operational artifact earns credit when another person can identify the exact disposable target, evidence origin, decision point and safe stop. It does not need to mutate a real service. An architecture artifact earns credit when it specifies state owners, failure domains and a test that could disprove the desired property. A proposal that simply adds PostgreSQL or a leader flag without changing callers is incomplete.

These exercises can be adapted to a future durable extension by adding explicit store construction, schema/key recovery and leadership fencing assumptions. Retain the original source-derived answer beside the extension answer. That comparison teaches how composition changes a guarantee without rewriting history or silently repairing the immutable baseline.

The exercise catalog is versioned with stable IDs and chapter links. Keep answers explicit about inspected, executed, expected and proposed evidence. Future revisions may change code and prerequisites; they must not turn the current edition’s bounded observations into universal production promises.

Source-backed boundary statements for this appendix are indexed in the [appendix claim record](../../validation/evidence/appendices.json). Detailed command, state, exercise and reference tables retain their own source provenance.
