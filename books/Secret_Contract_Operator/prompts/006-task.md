# 006 — Pure Data Validator

Phase: A | Complexity: High | Dependency: 005

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 006
Build internal/contract as a pure Go package with no Kubernetes client, logger, clock or network access. Adapt the standalone contractlab example rather than importing its educational module path. The result contains only key identifiers, bounded reason codes and sorted missing-key lists.
Implement required/optional handling, nonEmpty without whitespace normalization, byte length, Go regexp semantics, syntactic JSON, absolute URI without network lookup and strict PEM block validation. Distinguish malformed spec from invalid data. Limit per-value and total input budgets without truncating values before evaluation.
Do not expose parser errors, values, value lengths, snippets or hashes. Do not claim that length proves entropy or that parsing proves credential validity. Ensure map iteration cannot alter public result ordering.

Acceptance: table-driven tests cover positive, negative, optional and budget cases; the package can be tested independently of a cluster; output serialization is safe.
```
