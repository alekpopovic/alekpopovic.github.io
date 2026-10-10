# 016 — Envtest Integration Matrix

Phase: B | Complexity: High | Dependency: 015

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 016
Build a reliable envtest suite around a real manager and watches. Use unique namespaces and eventual assertions rather than arbitrary sleeps. Install the actual generated CRD schema and any minimal test-only optional CRDs explicitly.
Cover missing-to-valid-to-invalid Secret transitions, deletion/recreation UID changes, generation-aware status, authorization revocation, namespace isolation, no-op writes, concurrency conflicts and timer-driven expiration. Assert status/event/log outputs are free of sentinels.
Do not wait for Pods to be created by Deployment controllers in envtest because those controllers are not part of envtest. Reserve actual rollout assertions for kind. Record downloaded envtest binary versions and make the CI setup reproducible.

Acceptance: tests pass repeatedly from a clean setup without real cloud credentials; flakes, unrun cases and limitations are documented honestly.
```
