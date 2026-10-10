# Appendix B. From chapters to eighty implementation work items

The book presents the design in reading order. Product implementation has a different dependency order. The map below preserves eighty bounded work items for the eight-repository application workspace. These are specifications for future implementation, not claims that the companion examples complete the platform.

Every item starts as **planned** in `implementation/work-items.json`. Track implementation in the application workspace, with real child commits, a workspace snapshot, executed checks, and an evidence record. Completing a reading exercise is not enough to mark a product item complete. Never infer completion from a file's presence alone.

For a cross-repository change, identify producer contracts first, update consumers, test applications independently, commit child repositories, then update the workspace pins. Record blocked prerequisites explicitly. Preserve failed experiment output alongside the eventual fix.

## Foundations

Reading route: Chapters 1, 2, 3, 4, 5.

| Item | Implementation outcome |
|---|---|
| 000 | Repository audit, toolchain locks, and architectural decisions |
| 001 | Go workspace and modular process skeletons |
| 002 | Local development infrastructure without mandatory Kubernetes |
| 003 | Database migrations, query generation, and persistence conventions |
| 004 | Versioned HTTP API and generated client contract |
| 005 | Angular application shell and design foundation |
| 006 | Shared integration fixtures and CI quality gates |
| 007 | Execution state machines and trust-boundary contracts |

## Identity

Reading route: Chapters 6, 17.

| Item | Implementation outcome |
|---|---|
| 008 | Installation bootstrap and secure local authentication |
| 009 | Organizations, projects, memberships, and explicit RBAC |
| 010 | Append-oriented audit events and administrative history |
| 011 | Encrypted scoped secret storage and key management |
| 012 | Runner pools, enrollment tokens, and capability policies |
| 013 | Scoped API tokens and initial CLI authentication |
| 014 | Administrative settings and secret-management user experience |
| 015 | Identity and secret-security acceptance gate |

## Authoring

Reading route: Chapters 7, 8, 20.

| Item | Implementation outcome |
|---|---|
| 016 | Versioned pipeline YAML schema and bounded parser |
| 017 | DAG compiler and dependency validation |
| 018 | Typed parameters and restricted conditions |
| 019 | Immutable run snapshots and definition version history |
| 020 | Manual triggering, idempotency, and run creation API |
| 021 | Freestyle jobs using the same pipeline model |
| 022 | Pipeline editor, graph viewer, and validation feedback |
| 023 | Pipeline compiler and authoring acceptance gate |

## Scheduling

Reading route: Chapters 9, 10, 19.

| Item | Implementation outcome |
|---|---|
| 024 | PostgreSQL queue and atomic job leasing |
| 025 | Authorized runner matching and scoped claim API |
| 026 | Heartbeats, fencing, and idempotent result acceptance |
| 027 | Failure classification, retry budgets, and reconciliation |
| 028 | Cancellation, deadlines, and timeout propagation |
| 029 | Concurrency limits, capacity accounting, and resource locks |
| 030 | Durable events, live state updates, and queue explanations |
| 031 | Scheduler crash and concurrency acceptance gate |

## Execution

Reading route: Chapters 11, 12, 13.

| Item | Implementation outcome |
|---|---|
| 032 | Outbound runner service and durable local identity |
| 033 | Container executor with explicit isolation limits |
| 034 | Deterministic and credential-safe Git checkout |
| 035 | Sequential steps and bounded command lifecycle |
| 036 | Durable log segments, redaction, and upload resumption |
| 037 | Runner restart reconciliation and orphan cleanup |
| 038 | Run detail screen and resumable live log viewer |
| 039 | First real CI job and execution reliability gate |

## Source automation

Reading route: Chapters 8, 16.

| Item | Implementation outcome |
|---|---|
| 040 | GitHub App connection and signed webhook ingestion |
| 041 | Branch and pull-request discovery with trust policies |
| 042 | GitHub checks, commit statuses, and delivery reconciliation |
| 043 | Scheduled runs, cron timezones, and catch-up policy |
| 044 | Bounded matrix jobs and conditional fan-out |
| 045 | Automation timeline, run comparison, and actionable history |
| 046 | Scoped notifications and safe outbound delivery |
| 047 | Git automation and trigger-security acceptance gate |

## Build outputs

Reading route: Chapters 14, 15.

| Item | Implementation outcome |
|---|---|
| 048 | Artifact upload, integrity, and storage abstraction |
| 049 | Artifact retention, secure downloads, and explicit job handoff |
| 050 | JUnit reports and test-result visualization |
| 051 | Dependency cache with trust-aware namespaces |
| 052 | BuildKit image builds and immutable registry outputs |
| 053 | Registry build cache and measurable build performance |
| 054 | SBOM and provenance records for release artifacts |
| 055 | Artifact, cache, and build acceptance gate |

## Delivery

Reading route: Chapters 17, 18, 19.

| Item | Implementation outcome |
|---|---|
| 056 | Environments and server-enforced deployment policy |
| 057 | Deployment records, orchestration, and uncertain outcomes |
| 058 | Approval gates with immutable subject binding |
| 059 | Restricted SSH deployment executor |
| 060 | Container release rollout, health checks, and controlled rollback |
| 061 | Opt-in workload OIDC and short-lived cloud credentials |
| 062 | Environment dashboards and deployment audit experience |
| 063 | Deployment safety and recovery acceptance gate |

## Operator experience

Reading route: Chapters 20, 21.

| Item | Implementation outcome |
|---|---|
| 064 | Complete operational CLI with streaming and safe exits |
| 065 | Operational dashboards and efficient search |
| 066 | Operational quotas and abuse-resistant limits |
| 067 | Versioned reusable templates and isolated action contracts |
| 068 | Limited Jenkins migration analyzer and explicit unsupported cases |
| 069 | Guided onboarding and operator diagnostics |
| 070 | Accessibility, responsive behavior, and browser reliability |
| 071 | Feature-complete self-hosted acceptance and migration demo |

## Release hardening

Reading route: Chapters 22, 23, 24.

| Item | Implementation outcome |
|---|---|
| 072 | OpenTelemetry, Prometheus, and actionable alerts |
| 073 | Backup, restore, and recovery consistency |
| 074 | Multi-scheduler hardening and safe schema upgrades |
| 075 | Self-hosted packaging, TLS topology, and runner installation |
| 076 | Release build pipeline and software supply-chain checks |
| 077 | Security regression, fuzzing, and release threat-model review |
| 078 | Load, chaos, and operational endurance verification |
| 079 | Self-hosted release-candidate audit and repository handoff |

## Evidence attached to a completed item

Record the exact source commits for changed repositories, the workspace commit that pins them, the contracts/schema version, commands executed, exit statuses, output paths, and the acceptance decision. Use real immutable references, not example hashes. A release build also needs independently resolvable dependencies and confirmed output digests.

A blocker is not a failed project. It is a precise statement that a necessary prerequisite is missing: a published dependency, a test database, an authorized target, a review decision, or a runtime capability. Resolve that prerequisite or revise the scope explicitly. Do not silently skip it while retaining the same completion claim.

## Repository ownership rule

Use Chapter 3's repository boundaries when assigning ownership; the workspace records the tested composition.
