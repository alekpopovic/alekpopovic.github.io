# AgentPlane — Table of Contents

**Building a Kubernetes-Native Platform for AI Agents**

English edition 0.1.0 · October 10, 2026

[Preface](book/preface.md) · [Repository guide](README.md)

## Part I — Foundations

- [01. Choose a Product Boundary Before a Technology Stack](book/chapters/01-product-boundary.md)
- [02. Separate the Control Plane from the Execution Plane](book/chapters/02-architecture.md)
- [03. Turn the Threat Model into Testable Invariants](book/chapters/03-threat-model.md)
- [04. Create a Reproducible Engineering Workspace](book/chapters/04-engineering-workspace.md)

## Part II — Control Plane

- [05. Design Tenant-Safe PostgreSQL Data](book/chapters/05-tenant-data.md)
- [06. Keep Human, Service and Cluster Identities Distinct](book/chapters/06-identity.md)
- [07. Design APIs for Work That Finishes Later](book/chapters/07-asynchronous-api.md)
- [08. Enroll Clusters Without Exporting Their Authority](book/chapters/08-connector-pki.md)
- [09. Make Delivery Durable Without Promising Exactly-Once Effects](book/chapters/09-durable-messaging.md)

## Part III — Kubernetes Integration

- [10. Use Kubernetes Reconciliation Without Expanding Authority](book/chapters/10-reconciliation.md)
- [11. Integrate Agent Sandbox Through a Capability Adapter](book/chapters/11-upstream-adapters.md)
- [12. Build Runtime Profiles for the Actual Threat Model](book/chapters/12-runtime-isolation.md)

## Part IV — Safe Execution

- [13. Model Sessions, Executions and Uncertainty Separately](book/chapters/13-session-lifecycle.md)
- [14. Execute Commands and Handle Files Without Hidden Privilege](book/chapters/14-execution-files-git.md)
- [15. Make Network Policy an Enforced Property](book/chapters/15-network-policy.md)
- [16. Broker References, Not Customer Secret Values](book/chapters/16-secrets-workload-identity.md)

## Part V — Tool Governance

- [17. Discover Tools Without Trusting Their Descriptions](book/chapters/17-mcp-gateway.md)
- [18. Bind Authorization and Approval to the Exact Action](book/chapters/18-approvals.md)

## Part VI — State and Evidence

- [19. Preserve Workspaces Without Inventing Checkpoint Guarantees](book/chapters/19-workspaces-snapshots.md)
- [20. Meter Usage and Reserve Capacity Without Double Counting](book/chapters/20-metering-budgets.md)
- [21. Observe the System Without Collecting the Customer](book/chapters/21-observability-audit.md)

## Part VII — Product and Operations

- [22. Build Interfaces That Preserve Scope and Uncertainty](book/chapters/22-console-sdks.md)
- [23. Deploy and Upgrade Without Crossing the Trust Boundary](book/chapters/23-deployment-upgrades.md)
- [24. Design Recovery Before the First Production Incident](book/chapters/24-reliability-recovery.md)
- [25. Build Evidence for Every Important Claim](book/chapters/25-verification.md)

## Part VIII — Implementation and Publication

- [26. Use Coding Agents as Bounded Engineering Collaborators](book/chapters/26-coding-agents.md)
- [27. Deliver One Complete Vertical Slice](book/chapters/27-capstone.md)
- [28. Maintain an Open Book Like a Software Project](book/chapters/28-open-publication.md)

## Appendices and Companion Material

- [Appendix A. A Working Vocabulary](book/appendices/a-glossary.md)
- [Appendix B. Decision Records and Interface Contracts](book/appendices/b-design-records.md)
- [Appendix C. Review Answers and Failure Scenarios](book/appendices/c-review-exercises.md)
- [Appendix D. Companion Files and Build Commands](book/appendices/d-companion-files.md)
- [Primary sources](book/references.md)
- [Teaching labs](labs/README.md)
- [Implementation prompt pack](prompts/README.md)
- [Validation report](reports/VALIDATION.md)
