# 026 — Rollout Strategies and Storm Prevention

Phase: C | Complexity: High | Dependency: 025

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 026
Add explicit eligibility checks for supported rollout strategies. Handle paused Deployments, unsupported Recreate policy if not deliberately allowed, StatefulSet OnDelete/partition cases and DaemonSet OnDelete. Unsupported cases must not be reported as completed automatic restart.
Implement a documented debounce and minimum restart interval with persistent/reconstructible state where needed. Preserve the newest pending observation and revalidate it before patching. Test manager restart during the waiting window and changes arriving while rollout is progressing.
Do not claim that a PDB protects every controller-driven rolling update. Do not change the workload update strategy to make automation convenient. Separate action requested, template patched and rollout observed states.

Acceptance: fake-clock and concurrency tests prevent repeat storms and lost newest updates; unsupported strategies are explicit and do not delete Pods.
```
