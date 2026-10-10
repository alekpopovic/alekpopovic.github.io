# 013 — Workload Reference Validator

Phase: B | Complexity: High | Dependency: 012

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 013
Implement read-only extraction of PodTemplateSpec from supported apps/v1 workloads. Enforce explicit named consumers, all-consumer semantics and optional init-container selection. Missing selected containers fail validation.
Validate EnvFrom, EnvVars and Any according to the canonical API. Respect envName mapping and required secretKeyRef optional=false behavior. Detect explicit env overrides and ambiguous later envFrom sources conservatively. Do not read additional unapproved Secret values to resolve precedence.
Never print conflicting inline env values. Return safe paths and reason codes. Add tests for sidecars, init containers, mismatched key/name, prefix, optional references, duplicate names and conflicts. Explain the first-deploy deadlock when requiring an absent workload before deployment.

Acceptance: all supported consumers are evaluated correctly; no workload mutation occurs; ambiguous precedence never yields a misleading positive result.
```
