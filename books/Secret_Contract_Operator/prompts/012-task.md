# 012 — Optional ESO Adapter

Phase: B | Complexity: High | Dependency: 011

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 012
Add bounded unstructured ExternalSecret integration without importing ESO Go APIs. Limit API versions to a documented install-level allowlist and keep kind fixed to ExternalSecret. Do not accept an arbitrary user-controlled GVK.
Support clusters where ESO is absent. Implement discovery plus a documented polling/watch strategy that still reconciles a referenced ESO object after updates. Check the effective target Secret name as well as Ready. A healthy ExternalSecret targeting another Secret must fail with ExternalSecretTargetMismatch.
Sanitize all external conditions to local reason codes. Do not infer credential rotation age from refreshTime. Test missing CRD, missing object, absent/malformed conditions, false/true Ready and default/explicit target behavior. Document whether installing ESO after startup requires rediscovery or restart.

Acceptance: ordinary contracts work without ESO; required ESO failures block Ready; real ESO compatibility is not claimed until its e2e test is run.
```
