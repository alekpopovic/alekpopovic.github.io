# 023 — Protected Mutation Approval

Phase: C | Complexity: High | Dependency: 022

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 023
Design and implement the authorization boundary for optional mutation after the read-only MVP is accepted. Require install-level enablement, separate write RBAC, an explicit contract request and a protected workload/Secret approval tied to contract UID.
Do not treat a freely editable annotation or contract boolean as proof of authorization. Choose and document a enforceable administrative protection or grant mechanism. If the necessary protection cannot be provided, leave mutation disabled and mark the task blocked.
Allow at most one mutation-owning contract per workload in the first version. Read-only contracts may coexist. Recheck approval on every action and immediately stop new actions when it is revoked. Do not inherit approval on same-name object recreation.

Acceptance: unauthorized, revoked, conflicting and recreated-contract cases cannot mutate the target; default installation privileges remain unchanged.
```
