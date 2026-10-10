# AgentPlane — Table of Contents

**Building a Kubernetes-Native Platform for AI Agents**

English edition 0.1.0 · October 10, 2026

[Preface](preface.md) · [Repository guide](../README.md)

## Part I — Foundations

- [01. Choose a Product Boundary Before a Technology Stack](chapters/01-product-boundary.md)
- [02. Separate the Control Plane from the Execution Plane](chapters/02-architecture.md)
- [03. Turn the Threat Model into Testable Invariants](chapters/03-threat-model.md)
- [04. Create a Reproducible Engineering Workspace](chapters/04-engineering-workspace.md)

## Part II — Control Plane

- [05. Design Tenant-Safe PostgreSQL Data](chapters/05-tenant-data.md)
- [06. Keep Human, Service and Cluster Identities Distinct](chapters/06-identity.md)
- [07. Design APIs for Work That Finishes Later](chapters/07-asynchronous-api.md)
- [08. Enroll Clusters Without Exporting Their Authority](chapters/08-connector-pki.md)
- [09. Make Delivery Durable Without Promising Exactly-Once Effects](chapters/09-durable-messaging.md)

## Part III — Kubernetes Integration

- [10. Use Kubernetes Reconciliation Without Expanding Authority](chapters/10-reconciliation.md)
- [11. Integrate Agent Sandbox Through a Capability Adapter](chapters/11-upstream-adapters.md)
- [12. Build Runtime Profiles for the Actual Threat Model](chapters/12-runtime-isolation.md)

## Part IV — Safe Execution

- [13. Model Sessions, Executions and Uncertainty Separately](chapters/13-session-lifecycle.md)
- [14. Execute Commands and Handle Files Without Hidden Privilege](chapters/14-execution-files-git.md)
- [15. Make Network Policy an Enforced Property](chapters/15-network-policy.md)
- [16. Broker References, Not Customer Secret Values](chapters/16-secrets-workload-identity.md)

## Part V — Tool Governance

- [17. Discover Tools Without Trusting Their Descriptions](chapters/17-mcp-gateway.md)
- [18. Bind Authorization and Approval to the Exact Action](chapters/18-approvals.md)

## Part VI — State and Evidence

- [19. Preserve Workspaces Without Inventing Checkpoint Guarantees](chapters/19-workspaces-snapshots.md)
- [20. Meter Usage and Reserve Capacity Without Double Counting](chapters/20-metering-budgets.md)
- [21. Observe the System Without Collecting the Customer](chapters/21-observability-audit.md)

## Part VII — Product and Operations

- [22. Build Interfaces That Preserve Scope and Uncertainty](chapters/22-console-sdks.md)
- [23. Deploy and Upgrade Without Crossing the Trust Boundary](chapters/23-deployment-upgrades.md)
- [24. Design Recovery Before the First Production Incident](chapters/24-reliability-recovery.md)
- [25. Build Evidence for Every Important Claim](chapters/25-verification.md)

## Part VIII — Implementation and Publication

- [26. Use Coding Agents as Bounded Engineering Collaborators](chapters/26-coding-agents.md)
- [27. Deliver One Complete Vertical Slice](chapters/27-capstone.md)
- [28. Maintain an Open Book Like a Software Project](chapters/28-open-publication.md)

## Appendices and Companion Material

- [Appendix A. A Working Vocabulary](appendices/a-glossary.md)
- [Appendix B. Decision Records and Interface Contracts](appendices/b-design-records.md)
- [Appendix C. Review Answers and Failure Scenarios](appendices/c-review-exercises.md)
- [Appendix D. Companion Files and Build Commands](appendices/d-companion-files.md)
- [Primary sources](references.md)
- [Teaching labs](../labs/README.md)
- [Implementation prompt pack](../prompts/README.md)
- [Validation report](../reports/VALIDATION.md)
