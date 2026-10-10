# 017 — Helm Chart for the Read-only MVP

Phase: B | Complexity: Medium | Dependency: 016

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 017
Create charts/secret-contract-operator for the implemented MVP. Include image digest/tag selection, manager deployment, ServiceAccount, namespace-scoped reader roles/bindings, scoped Lease permissions, resources and hardened security contexts.
Default workload mutation permissions must be absent. Configure metrics and optional ServiceMonitor without requiring Prometheus Operator. Do not require cert-manager when no webhook is deployed. Document exact Secret cache and watch scope.
Choose an explicit CRD lifecycle strategy with a separate generated CRD artifact or carefully documented crds directory usage. Do not claim helm upgrade automatically migrates CRDs. Add render tests that reject wildcard and forbidden write permissions.

Acceptance: helm lint and template checks pass; CRD and controller installation order is documented; validation-only RBAC is mechanically verified.
```
