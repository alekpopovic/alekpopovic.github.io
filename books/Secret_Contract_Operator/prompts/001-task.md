# 001 — Inventory, Working Rules, and AGENTS.md

Phase: A | Complexity: Medium | Dependency: none

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 001
Inspect the repository before changing files. Preserve an existing module path and any unrelated work. Create AGENTS.md, docs/specification.md and docs/security.md from the canonical decisions in this book. Use SecretContract in secrets.codepop.tech/v1alpha1 as the proposed API, and clearly mark any existing different group as a migration concern.
Define validation-only as both runtime behavior and RBAC. Document the validation-oracle threat: contract authors must already be authorized to learn properties of the referenced Secret. Forbid Secret values, substrings, raw parser errors and content hashes in all outputs. Distinguish application health from contract readiness.
Create tracking records for every numbered task with pending, in_progress, blocked, implemented, verified and accepted states. Preserve the real current status; do not mark planned work complete. Record available tools and missing prerequisites without printing environment variables or kubeconfig contents.

Acceptance: repository inventory and security assumptions exist; no operator implementation or cluster mutation is performed; tracking starts truthfully.
```
