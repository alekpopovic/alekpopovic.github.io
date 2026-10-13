# Site-root execution sequence

Install beneath books/inside-orch. All tasks execute from the website repository root.

| Task | Phase | Prompt |
| --- | --- | --- |
|000|Research and source contracts|[Establish a separate, reproducible book workspace](prompts/000-workspace-and-baseline.md)|
|001|Research and source contracts|[Inventory the implementation and its executable entrypoints](prompts/001-source-inventory.md)|
|002|Research and source contracts|[Reconstruct the engineering history with verifiable milestones](prompts/002-commit-timeline.md)|
|003|Research and source contracts|[Reconcile all original prompts with implementation evidence](prompts/003-development-prompt-reconciliation.md)|
|004|Research and source contracts|[Build the capability ledger that governs every chapter](prompts/004-capability-and-integration-ledger.md)|
|005|Research and source contracts|[Resolve stale documentation through code-first comparison](prompts/005-documentation-conflict-ledger.md)|
|006|Research and source contracts|[Freeze the dependency and compatibility assumptions](prompts/006-compatibility-and-dependency-record.md)|
|007|Research and source contracts|[Design an isolated laboratory with honest prerequisites](prompts/007-safe-lab-environment.md)|
|008|Research and source contracts|[Turn the outline into three coherent learning paths](prompts/008-reader-paths-and-learning-contract.md)|
|009|Research and source contracts|[Extract the decisions and tradeoffs behind the code](prompts/009-architectural-decisions.md)|
|010|Research and source contracts|[Establish immutable citations and a compact bibliography](prompts/010-reference-and-link-policy.md)|
|011|Research and source contracts|[Select and lock the book’s source listings](prompts/011-code-excerpt-registry.md)|
|012|Research and source contracts|[Design one progressive case study across the whole book](prompts/012-running-case-study.md)|
|013|Research and source contracts|[Define the evidence that proves each operational lesson](prompts/013-observation-contract.md)|
|014|Research and source contracts|[Build a precise failure and recovery matrix](prompts/014-failure-model.md)|
|015|Research and source contracts|[Map trust boundaries before writing security chapters](prompts/015-threat-model.md)|
|016|Research and source contracts|[Prepare author metadata and an explicit rights record](prompts/016-rights-and-attribution.md)|
|017|Research and source contracts|[Define a readable multi-format book design](prompts/017-publication-design-system.md)|
|018|Research and source contracts|[Freeze chapter scope, dependencies and evidence coverage](prompts/018-freeze-table-of-contents.md)|
|019|Research and source contracts|[Review the sample and approve the book’s technical stance](prompts/019-sample-and-foundation-gate.md)|
|020|Chapter writing|[Chapter 01: Why Build a Container Orchestrator?](prompts/020-chapter-01-why-build-a-container-orchestrator.md)|
|021|Chapter writing|[Chapter 02: A Repository Built for Reasoning](prompts/021-chapter-02-a-repository-built-for-reasoning.md)|
|022|Chapter writing|[Chapter 03: Boot the Lab and Deploy the First Service](prompts/022-chapter-03-boot-the-lab-and-deploy-the-first-service.md)|
|023|Chapter writing|[Chapter 04: Domain Models and State Machines](prompts/023-chapter-04-domain-models-and-state-machines.md)|
|024|Chapter writing|[Chapter 05: Service Specifications, Resources, and Ports](prompts/024-chapter-05-service-specifications-resources-and-ports.md)|
|025|Chapter writing|[Chapter 06: Follow One Request Through the Control Plane](prompts/025-chapter-06-follow-one-request-through-the-control-plane.md)|
|026|Chapter writing|[Chapter 07: HTTP Contracts and Compatible APIs](prompts/026-chapter-07-http-contracts-and-compatible-apis.md)|
|027|Chapter writing|[Chapter 08: A CLI That Operators Can Automate](prompts/027-chapter-08-a-cli-that-operators-can-automate.md)|
|028|Chapter writing|[Chapter 09: Persistence, Transactions, and Optimistic Concurrency](prompts/028-chapter-09-persistence-transactions-and-optimistic-concurrency.md)|
|029|Chapter writing|[Chapter 10: A Deterministic Scheduler](prompts/029-chapter-10-a-deterministic-scheduler.md)|
|030|Chapter writing|[Chapter 11: Reconciliation as Repeated Convergence](prompts/030-chapter-11-reconciliation-as-repeated-convergence.md)|
|031|Chapter writing|[Chapter 12: Idempotent Docker Operations and Drift](prompts/031-chapter-12-idempotent-docker-operations-and-drift.md)|
|032|Chapter writing|[Chapter 13: Agents, Heartbeats, and Task Reports](prompts/032-chapter-13-agents-heartbeats-and-task-reports.md)|
|033|Chapter writing|[Chapter 14: Health Checks That Respect Trust Boundaries](prompts/033-chapter-14-health-checks-that-respect-trust-boundaries.md)|
|034|Chapter writing|[Chapter 15: Events, Audits, and Notification Boundaries](prompts/034-chapter-15-events-audits-and-notification-boundaries.md)|
|035|Chapter writing|[Chapter 16: Log Streaming Without Losing Control](prompts/035-chapter-16-log-streaming-without-losing-control.md)|
|036|Chapter writing|[Chapter 17: Rolling Updates and Rollback Invariants](prompts/036-chapter-17-rolling-updates-and-rollback-invariants.md)|
|037|Chapter writing|[Chapter 18: Safe Deletion and Resource Cleanup](prompts/037-chapter-18-safe-deletion-and-resource-cleanup.md)|
|038|Chapter writing|[Chapter 19: Offline Nodes, Draining, and Rescheduling](prompts/038-chapter-19-offline-nodes-draining-and-rescheduling.md)|
|039|Chapter writing|[Chapter 20: Endpoint Discovery and Internal DNS](prompts/039-chapter-20-endpoint-discovery-and-internal-dns.md)|
|040|Chapter writing|[Chapter 21: Ingress, Host Networking, and the Overlay Roadmap](prompts/040-chapter-21-ingress-host-networking-and-the-overlay-roadmap.md)|
|041|Chapter writing|[Chapter 22: Autoscaling Decisions and Missing Integration](prompts/041-chapter-22-autoscaling-decisions-and-missing-integration.md)|
|042|Chapter writing|[Chapter 23: Authentication, Authorization, and Node Trust](prompts/042-chapter-23-authentication-authorization-and-node-trust.md)|
|043|Chapter writing|[Chapter 24: Encrypted Secrets and Configuration Redaction](prompts/043-chapter-24-encrypted-secrets-and-configuration-redaction.md)|
|044|Chapter writing|[Chapter 25: Registry Credentials and Immutable Image Identity](prompts/044-chapter-25-registry-credentials-and-immutable-image-identity.md)|
|045|Chapter writing|[Chapter 26: Security Contexts, Admission, and Policy](prompts/045-chapter-26-security-contexts-admission-and-policy.md)|
|046|Chapter writing|[Chapter 27: Namespaces and the Limits of Multi-Tenancy](prompts/046-chapter-27-namespaces-and-the-limits-of-multi-tenancy.md)|
|047|Chapter writing|[Chapter 28: Quotas and Usage Accounting](prompts/047-chapter-28-quotas-and-usage-accounting.md)|
|048|Chapter writing|[Chapter 29: Supply Chain Designs Without False Guarantees](prompts/048-chapter-29-supply-chain-designs-without-false-guarantees.md)|
|049|Chapter writing|[Chapter 30: GitOps, Drift, and Controlled Reconciliation](prompts/049-chapter-30-gitops-drift-and-controlled-reconciliation.md)|
|050|Chapter writing|[Chapter 31: Finite Jobs and Time-Based Work](prompts/050-chapter-31-finite-jobs-and-time-based-work.md)|
|051|Chapter writing|[Chapter 32: Local Volumes, Claims, and Workload Topology](prompts/051-chapter-32-local-volumes-claims-and-workload-topology.md)|
|052|Chapter writing|[Chapter 33: Extension Interfaces and a Plugin Roadmap](prompts/052-chapter-33-extension-interfaces-and-a-plugin-roadmap.md)|
|053|Chapter writing|[Chapter 34: Leader Election and the Durable HA Boundary](prompts/053-chapter-34-leader-election-and-the-durable-ha-boundary.md)|
|054|Chapter writing|[Chapter 35: Upgrades, Migrations, Maintenance, and Retention](prompts/054-chapter-35-upgrades-migrations-maintenance-and-retention.md)|
|055|Chapter writing|[Chapter 36: Fakes, Property Tests, Fuzzing, and Contracts](prompts/055-chapter-36-fakes-property-tests-fuzzing-and-contracts.md)|
|056|Chapter writing|[Chapter 37: Failure Injection and Recovery Evidence](prompts/056-chapter-37-failure-injection-and-recovery-evidence.md)|
|057|Chapter writing|[Chapter 38: Metrics, Dashboards, and Actionable Signals](prompts/057-chapter-38-metrics-dashboards-and-actionable-signals.md)|
|058|Chapter writing|[Chapter 39: Performance and Scale Tests That Say What They Measure](prompts/058-chapter-39-performance-and-scale-tests-that-say-what-they-measure.md)|
|059|Chapter writing|[Chapter 40: Release a System You Can Honestly Operate](prompts/059-chapter-40-release-a-system-you-can-honestly-operate.md)|
|060|Appendices|[Appendix A — CLI, API, and configuration reference](prompts/060-appendix-a-cli-api-config.md)|
|061|Appendices|[Appendix B — Lifecycle and invariants reference](prompts/061-appendix-b-lifecycle-invariants.md)|
|062|Appendices|[Appendix C — Annotated commit and prompt history](prompts/062-appendix-c-annotated-history.md)|
|063|Appendices|[Appendix D — Exercises and solutions](prompts/063-appendix-d-exercises-solutions.md)|
|064|Appendices|[Appendix E — Operational playbooks and measurement contracts](prompts/064-appendix-e-ops-measurement.md)|
|065|Appendices|[Appendix F — Glossary and annotated bibliography](prompts/065-appendix-f-glossary-bibliography.md)|
|066|Eight labs|[Lab 01 — Initialize the teaching cluster and observe process restart](prompts/066-lab-01-initialization-restart.md)|
|067|Eight labs|[Lab 02 — Deterministic placement and concurrent task claims](prompts/067-lab-02-scheduler-placement-concurrency.md)|
|068|Eight labs|[Lab 03 — Reconciliation and Docker drift ownership](prompts/068-lab-03-reconciler-docker-drift.md)|
|069|Eight labs|[Lab 04 — Rollout, rollback, and availability accounting](prompts/069-lab-04-rollout-rollback-availability.md)|
|070|Eight labs|[Lab 05 — Secrets, authorization, and healthcheck trust boundaries](prompts/070-lab-05-secrets-auth-ssrf.md)|
|071|Eight labs|[Lab 06 — Namespace scoping and atomic quota admission](prompts/071-lab-06-namespaces-quotas.md)|
|072|Eight labs|[Lab 07 — GitOps drift, finite jobs, and cron scheduling](prompts/072-lab-07-gitops-jobs-cron.md)|
|073|Eight labs|[Lab 08 — Backup, migration, load, and recovery boundaries](prompts/073-lab-08-backup-migration-load-recovery.md)|
|074|Technical and editorial review|[Synchronize and verify exact source excerpts](prompts/074-excerpt-sync.md)|
|075|Technical and editorial review|[Compile and test runnable teaching examples](prompts/075-code-compilation.md)|
|076|Technical and editorial review|[Execute all eight connected laboratory exercises](prompts/076-lab-execution.md)|
|077|Technical and editorial review|[Review composition, invariants and architectural guarantees](prompts/077-architect-review.md)|
|078|Technical and editorial review|[Review source-guided explanations for working developers](prompts/078-developer-review.md)|
|079|Technical and editorial review|[Review operations, recovery and troubleshooting guidance](prompts/079-devops-review.md)|
|080|Technical and editorial review|[Review security claims, threat paths and redaction](prompts/080-security-review.md)|
|081|Technical and editorial review|[Audit every technical claim and its guarantee boundary](prompts/081-claim-guarantee-audit.md)|
|082|Technical and editorial review|[Verify CLI commands, API routes and configuration examples](prompts/082-command-api-fidelity.md)|
|083|Technical and editorial review|[Copyedit technical prose without changing its meaning](prompts/083-copyedit.md)|
|084|Technical and editorial review|[Review exercises and independently justify worked answers](prompts/084-exercises-solutions.md)|
|085|Technical and editorial review|[Lock and validate all source, history and cross-reference links](prompts/085-evidence-link-lock.md)|
|086|PDF, EPUB, online and site integration|[Create final metadata, cover and catalog material](prompts/086-metadata-cover-and-catalog.md)|
|087|PDF, EPUB, online and site integration|[Build a navigable print-quality PDF](prompts/087-pdf-typesetting.md)|
|088|PDF, EPUB, online and site integration|[Render and inspect the actual final PDF](prompts/088-pdf-visual-review.md)|
|089|PDF, EPUB, online and site integration|[Build an accessible reflowable EPUB edition](prompts/089-accessible-epub.md)|
|090|PDF, EPUB, online and site integration|[Validate EPUB structure and real reading behavior](prompts/090-epub-validation.md)|
|091|PDF, EPUB, online and site integration|[Implement the native Jekyll reader adapter](prompts/091-native-jekyll-reader-adapter.md)|
|092|PDF, EPUB, online and site integration|[Wire the orch publisher and source catalog into the existing build](prompts/092-native-publisher-and-catalog.md)|
|093|PDF, EPUB, online and site integration|[Ship three original posts, glossary and updates with the native book](prompts/093-site-posts-glossary-and-integration.md)|
|094|PDF, EPUB, online and site integration|[Verify native discovery, accessibility and publication behavior](prompts/094-site-accessibility-search-and-downloads.md)|
|095|PDF, EPUB, online and site integration|[Create the offline edition and reproducible release inputs](prompts/095-offline-and-reproducible-package.md)|
|096|Release and handoff|[Run the complete edition gate and resolve blockers](prompts/096-release-gate.md)|
|097|Release and handoff|[Challenge the book as three skeptical readers](prompts/097-independent-review.md)|
|098|Release and handoff|[Freeze final archives, hashes and edition provenance](prompts/098-final-archives-and-handoff.md)|
|099|Release and handoff|[Prepare the exact next publication action without a surprise deployment](prompts/099-reviewable-publication-handoff.md)|
