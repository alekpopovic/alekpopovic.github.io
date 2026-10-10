# 004 — Canonical API Types

Phase: A | Complexity: High | Dependency: 003

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 004
Implement the book canonical API, not the earlier inconsistent sketch. Define local secretRef, map-like requiredKeys with unique names, optional envName, pointer required/nonEmpty defaults, byte-based minLength/maxLength, pattern and None/JSON/URI/PEM formats.
Add the bounded ExternalSecret reference, workloadRefs with explicit containers, includeInitContainers and Any/EnvFrom/EnvVars consumption, injection.mode default Disabled, and rotation with restartOnChange false, maxAge and rotatedAtAnnotation. Policies are requireExternalSecretReady, requireWorkloadReference and requireRotationPolicy. Missing Secret must never satisfy Ready.
Status contains observedGeneration, observedSecret name/UID/resourceVersion, safe violations, counts, workload results, conditions and lastCheckedTime. Conditions use metav1.Condition and list-map semantics by type. If optional mutation fields are accepted before implementation, report FeatureNotEnabled rather than silently pretending to act. Add printer columns backed by real scalar status fields.

Acceptance: generate DeepCopy and CRD manifests; examples match the types; status subresource exists; no output type has a Secret value or content fingerprint field.
```
