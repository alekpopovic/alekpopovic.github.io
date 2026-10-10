# 011 — RBAC Profile and Cache Boundaries

Phase: A | Complexity: High | Dependency: 010

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 011
Implement namespace-scoped installation and explicit trusted-writer documentation. Review all generated RBAC. The default role reads Secret data in the declared scope, updates only contract status and writes events. It must not write Secrets or workloads.
Document exactly whether the standard cache holds full Secret objects. Do not describe a label filter as an authorization boundary. If implementing a metadata-watch profile, use direct authorized reads and test that the cached client cannot silently start a full Secret informer for that path.
Add negative access tests using the operator ServiceAccount, not the administrator test client. Separate leader-election Lease permissions in the manager namespace. Clearly reject or document unsupported arbitrary Secret selection with resourceNames-limited informer lists.

Acceptance: negative tests prove cross-namespace and write restrictions; chart/RBAC output and runtime watch scope agree; cache exposure is truthful.
```
