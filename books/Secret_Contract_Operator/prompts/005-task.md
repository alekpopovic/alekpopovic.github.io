# 005 — CRD Schema and Specification Validation

Phase: A | Complexity: High | Dependency: 004

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 005
Add structural schema constraints and defaults. Bound requiredKeys to 1..256, pattern size and workload list sizes. Reject duplicate key names, negative lengths, minLength greater than maxLength, unsupported kinds and malformed local references. Separate valid Secret key names from the project conservative environment-name policy.
Require the corresponding reference when an enforcement policy is enabled. Require positive supported duration syntax such as 720h rather than assuming 30d parses. Reject invalid annotation keys. Use native schema/CEL where suitable; do not add a mandatory webhook just for defaults already supported by the schema.
Implement a defensive Go spec validator for cases that cannot safely be enforced in the chosen schema, including regex compilation. A malformed existing object must become a safe InvalidSpec result, not panic. Do not copy raw pattern text or parser errors into public diagnostics.

Acceptance: schema and pure spec tests cover all boundary cases; default false is distinguishable from omitted default true; generated manifests are clean.
```
