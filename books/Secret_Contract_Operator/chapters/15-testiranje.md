# 15. Testing Strategy and Proving Invariants

## 15.1 This Project's Test Pyramid

Most tests belong to the pure validator and status builder. Envtest checks the real API, defaults, the status subresource, and event-driven reconcile. Kind tests check installation, RBAC, actual workload rollout, and integration with a supported ESO release.

These groups serve different purposes. A green unit suite does not prove that the Helm chart grants correct permissions. A green kind demonstration does not prove that an unusual parser error cannot leak data from the validator.

## 15.2 Validator Matrix

| Area | Positive case | Negative case |
|---|---|---|
| Required keys | Key exists | Key absent |
| Optional keys | Absent optional key skipped | Present optional key invalid |
| Emptiness | One or more bytes | Zero bytes |
| Length | Inclusive boundaries | Below minimum / above maximum |
| UTF-8 | Explicit byte semantics | Incorrect character-count assumption |
| Regexp | Anchored and substring cases | Invalid pattern / mismatch |
| JSON | Object and scalar | Malformed JSON |
| URI | Absolute network and opaque URIs | Relative URI |
| PEM | Single block and bundle | Garbage before or after a block |
| Budget | Boundary size | Oversized input |

Each case has a clear expected reason. Checks must not depend on Go map iteration order. Compare sorted findings and a stable JSON representation of the result.

## 15.3 Envtest Matrix

The basic scenario creates a contract before its Secret and expects `Ready=False`. Creating the Secret must update status through the watch, without a manual call to the reconcile method. Then remove a key, restore it, and delete the Secret. Check every transition.

Separately test generation, no-op writes, two contracts referencing the same Secret name in different namespaces, manager restart, and approval changes. Envtest has no standard workload controllers, so check the PodTemplate patch rather than actual pod availability. [S10](https://book.kubebuilder.io/reference/envtest.html)

A conflicting status write must trigger another read. Deliberately change the CR between the first observation and the patch in this test. A fake client that always accepts changes is insufficient.

## 15.4 Security-output Tests

Use a sentinel distinct from key and rule names. Capture status JSON, event messages, log records, annotation changes, and metrics exposition. Check for the sentinel's raw, base64, and hex representations, as well as common deterministic digests.

This is not mathematical proof that no fragment of a value can ever leak. Combine it with result types that have no input-value fields and review every error formatter. Test malformed URIs and PEM specifically, because parser errors may format payloads differently.

Do not use real secrets in fixtures. Test failures should not print the full input or a complete Kubernetes Secret object. Even synthetic examples should model safe handling.

## 15.5 Negative RBAC Tests

Start the manager with a namespaced Role. Confirm that it cannot read a Secret from another namespace, create or modify a Secret, or patch a workload in the validation-only profile.

Use an explicit ServiceAccount identity. Successfully modifying a workload using an administrator's kubeconfig proves nothing about operator permissions. For the mutation profile, also check the negative case with no approval on the target.

## 15.6 E2E Scenarios

A real cluster should verify chart installation, manager readiness, CRD defaults, successful and failed contracts, Secret changes, operator restart, cleanup, and the absence of unintended application-resource deletion.

For optional restart, test Deployment RollingUpdate, a paused Deployment, StatefulSet OnDelete, supported StatefulSet RollingUpdate, and DaemonSet modes. Check new pod counts and final rollout status through metadata and workload status, without `kubectl exec env`.

## 15.7 Chaos and Degradation

Interrupt API access in a controlled test, revoke one RBAC permission, remove the ESO CRD, send multiple rapid Secret changes, and stop the active leader. The operator must not dump data into logs, restart the application uncontrollably, or permanently lose the latest finding.

Clock tests use injected time rather than multi-minute `sleep` calls. Test the expiration boundary, allowed skew, the distant future, and a controller restart just before the deadline.

## 15.8 Acceptance Criteria

Every PR must state which tests ran and which could not run. CI artifacts contain test output without secret payloads. Coverage percentage is a supporting signal, not a substitute for authorization, status freshness, and idempotence coverage.

The proposed release minimum is: unit and race checks, envtest for each supported Kubernetes minor version advertised by the release, chart rendering checks, and at least one kind scenario for every active integration. These are criteria the project still needs to meet, not an already completed matrix.

**Checkpoint.** Find at least one test for each public guarantee that would fail if the guarantee were broken. A guarantee without such a test requires additional review.
