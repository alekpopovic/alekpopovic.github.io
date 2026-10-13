# Inside orch — frozen reading order

The preface is section zero. Stable chapter/appendix IDs and titles remain exactly as supplied in the outline. The canonical47 sectionmanifest is `manuscript/Book.txt`; unfinished paths are not registered in the live website. This scope freeze is a writing contract, not evidence that the book exists.

## Front matter

- [Preface](../manuscript/00-preface.md) — audience, edition, execution boundary, laboratory and evidence expectations.

## I — Establish the System
- 1. [Why Build a Container Orchestrator?](../manuscript/chapters/01-why-build-a-container-orchestrator.md)
- 2. [A Repository Built for Reasoning](../manuscript/chapters/02-a-repository-built-for-reasoning.md)
- 3. [Boot the Lab and Deploy the First Service](../manuscript/chapters/03-boot-the-lab-and-deploy-the-first-service.md)
- 4. [Domain Models and State Machines](../manuscript/chapters/04-domain-models-and-state-machines.md)
- 5. [Service Specifications, Resources, and Ports](../manuscript/chapters/05-service-specifications-resources-and-ports.md)
- 6. [Follow One Request Through the Control Plane](../manuscript/chapters/06-follow-one-request-through-the-control-plane.md)

## II — Implement the Core
- 7. [HTTP Contracts and Compatible APIs](../manuscript/chapters/07-http-contracts-and-compatible-apis.md)
- 8. [A CLI That Operators Can Automate](../manuscript/chapters/08-a-cli-that-operators-can-automate.md)
- 9. [Persistence, Transactions, and Optimistic Concurrency](../manuscript/chapters/09-persistence-transactions-and-optimistic-concurrency.md)
- 10. [A Deterministic Scheduler](../manuscript/chapters/10-a-deterministic-scheduler.md)
- 11. [Reconciliation as Repeated Convergence](../manuscript/chapters/11-reconciliation-as-repeated-convergence.md)
- 12. [Idempotent Docker Operations and Drift](../manuscript/chapters/12-idempotent-docker-operations-and-drift.md)
- 13. [Agents, Heartbeats, and Task Reports](../manuscript/chapters/13-agents-heartbeats-and-task-reports.md)
- 14. [Health Checks That Respect Trust Boundaries](../manuscript/chapters/14-health-checks-that-respect-trust-boundaries.md)

## III — Change and Recover
- 15. [Events, Audits, and Notification Boundaries](../manuscript/chapters/15-events-audits-and-notification-boundaries.md)
- 16. [Log Streaming Without Losing Control](../manuscript/chapters/16-log-streaming-without-losing-control.md)
- 17. [Rolling Updates and Rollback Invariants](../manuscript/chapters/17-rolling-updates-and-rollback-invariants.md)
- 18. [Safe Deletion and Resource Cleanup](../manuscript/chapters/18-safe-deletion-and-resource-cleanup.md)
- 19. [Offline Nodes, Draining, and Rescheduling](../manuscript/chapters/19-offline-nodes-draining-and-rescheduling.md)
- 20. [Endpoint Discovery and Internal DNS](../manuscript/chapters/20-endpoint-discovery-and-internal-dns.md)
- 21. [Ingress, Host Networking, and the Overlay Roadmap](../manuscript/chapters/21-ingress-host-networking-and-the-overlay-roadmap.md)
- 22. [Autoscaling Decisions and Missing Integration](../manuscript/chapters/22-autoscaling-decisions-and-missing-integration.md)

## IV — Enforce Boundaries
- 23. [Authentication, Authorization, and Node Trust](../manuscript/chapters/23-authentication-authorization-and-node-trust.md)
- 24. [Encrypted Secrets and Configuration Redaction](../manuscript/chapters/24-encrypted-secrets-and-configuration-redaction.md)
- 25. [Registry Credentials and Immutable Image Identity](../manuscript/chapters/25-registry-credentials-and-immutable-image-identity.md)
- 26. [Security Contexts, Admission, and Policy](../manuscript/chapters/26-security-contexts-admission-and-policy.md)
- 27. [Namespaces and the Limits of Multi-Tenancy](../manuscript/chapters/27-namespaces-and-the-limits-of-multi-tenancy.md)
- 28. [Quotas and Usage Accounting](../manuscript/chapters/28-quotas-and-usage-accounting.md)
- 29. [Supply Chain Designs Without False Guarantees](../manuscript/chapters/29-supply-chain-designs-without-false-guarantees.md)
- 30. [GitOps, Drift, and Controlled Reconciliation](../manuscript/chapters/30-gitops-drift-and-controlled-reconciliation.md)

## V — Extend the Platform
- 31. [Finite Jobs and Time-Based Work](../manuscript/chapters/31-finite-jobs-and-time-based-work.md)
- 32. [Local Volumes, Claims, and Workload Topology](../manuscript/chapters/32-local-volumes-claims-and-workload-topology.md)
- 33. [Extension Interfaces and a Plugin Roadmap](../manuscript/chapters/33-extension-interfaces-and-a-plugin-roadmap.md)
- 34. [Leader Election and the Durable HA Boundary](../manuscript/chapters/34-leader-election-and-the-durable-ha-boundary.md)
- 35. [Upgrades, Migrations, Maintenance, and Retention](../manuscript/chapters/35-upgrades-migrations-maintenance-and-retention.md)

## VI — Prove and Operate
- 36. [Fakes, Property Tests, Fuzzing, and Contracts](../manuscript/chapters/36-fakes-property-tests-fuzzing-and-contracts.md)
- 37. [Failure Injection and Recovery Evidence](../manuscript/chapters/37-failure-injection-and-recovery-evidence.md)
- 38. [Metrics, Dashboards, and Actionable Signals](../manuscript/chapters/38-metrics-dashboards-and-actionable-signals.md)
- 39. [Performance and Scale Tests That Say What They Measure](../manuscript/chapters/39-performance-and-scale-tests-that-say-what-they-measure.md)
- 40. [Release a System You Can Honestly Operate](../manuscript/chapters/40-release-a-system-you-can-honestly-operate.md)

## Appendices
- A. [CLI, API, and Configuration Reference](../manuscript/appendices/a-cli-api-config.md)
- B. [Lifecycle States and Invariant Reference](../manuscript/appendices/b-lifecycle-invariants.md)
- C. [Commit Atlas and Original Prompt Crosswalk](../manuscript/appendices/c-annotated-history.md)
- D. [Worked Exercises and Design Solutions](../manuscript/appendices/d-exercises-solutions.md)
- E. [Operator Runbooks and Measurement Contracts](../manuscript/appendices/e-ops-measurement.md)
- F. [Glossary, Bibliography, and Boundary Index](../manuscript/appendices/f-glossary-bibliography.md)
