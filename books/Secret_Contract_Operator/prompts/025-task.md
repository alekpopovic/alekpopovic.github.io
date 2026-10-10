# 025 — Metadata Restart Token

Phase: C | Complexity: High | Dependency: 024

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 025
Implement optional restart signaling using only Secret UID/resourceVersion and contract UID. Use a valid bounded annotation key under the project prefix; never hash Secret content. The value must distinguish Secret deletion/recreation.
Require all mutation preconditions and valid content before changing PodTemplate. An invalid new Secret must not trigger a rollout. Document that metadata-only Secret changes may trigger restart and that first enablement causes an initial template change.
Do not delete Pods directly. Compare the current token before patching. Revalidate the relevant fresh observation before the action, while documenting that this cannot create an atomic Secret/workload transaction. Do not claim the annotation proves processes are using the new value.

Acceptance: tests cover initial enablement, same-version no-op, update, recreation, invalid data and absence of content fingerprints.
```
