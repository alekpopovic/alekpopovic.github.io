# 13. Rotation and Controlled Rollout

## 13.1 Three Different Events

An object change, a successful synchronization, and credential rotation are different events. A label update changes a Kubernetes object without changing a password. ESO can confirm the same content without business rotation. A provider can change a password before the new content reaches the cluster.

The operator therefore records the observed Secret identity, the state of the declared rotation policy, and any requested workload change separately. It does not call every new `resourceVersion` a “new password.”

## 13.2 Environment Values in a Running Process

A container using a Secret as environment variables does not automatically receive new values when the Secret changes. The corresponding process or pods must restart. Kubernetes documentation explicitly describes this distinction. [S17](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

The proposed restart mechanism changes a PodTemplate annotation, giving the corresponding workload controller a new template. Secret Contract Operator does not delete pods directly or command a process to reload configuration.

## 13.3 A Token Without Secret Contents

```text
annotation key:
  secrets.codepop.tech/restart-<contract-uid>

annotation value:
  <secret-uid>:<secret-resource-version>
```

The contract UID is a metadata identity that distinguishes a recreated contract. The Secret UID distinguishes a new object with an old name. `resourceVersion` is used only as an observed-version identifier; the token contains no data hash.

This book's default policy is **restart on an approved Secret object change**, not precisely “only when values change.” A metadata update can also trigger a rollout. Document this limitation in the README, or users will perceive the behavior as a bug.

When the feature is first enabled, setting the annotation itself changes the template and may trigger an initial rollout. This edition chooses an explicit initial rollout instead of hidden baseline state. Users enable the option during a planned window.

## 13.4 Do Not Restart for an Invalid New Secret

If a new Secret fails required-key checks or security policy, existing pods should not automatically be replaced with invalid ones. The operator reports the finding and leaves the restart annotation unchanged.

This is still incomplete protection: a pod independently recreated after node failure may read the currently invalid Secret. Keeping an old process running is therefore different from a safe rotation model. For stricter control, use versioned, immutable Secret objects and switch references deliberately after validation.

![Figure 13.1 — Security checks precede the rollout signal; failed validation leaves the template unchanged.](../assets/rotation.svg)

## 13.5 Workload Strategies

A Deployment rollout must check whether the Deployment is paused and which update strategy it uses. `RollingUpdate` has availability parameters configured by the application owner; `Recreate` has different availability semantics. The operator should not silently change the strategy for rotation. [S18](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

A StatefulSet using `OnDelete` does not automatically replace pods after a template change. `RollingUpdate` may have a partition limiting which pods are updated. The initial restart profile should require a supported RollingUpdate form without unhandled restrictions; report other cases as `UnsupportedRolloutStrategy`. [S19](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

DaemonSets also require understanding their update mode. Do not represent `OnDelete` as a successful automatic restart. Accept support for this kind only after an E2E test verifies actual pod replacement with the chosen strategy. [S20](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)

A PodDisruptionBudget is not universal protection for this operation. Rolling updates managed by a Deployment or StatefulSet are not constrained by a PDB in the same way as the Eviction API. Configure availability through the particular workload strategy, readiness, and cluster capacity. [S21](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

## 13.6 Maximum-age Policy

`maxAge: 720h` means 30 periods of 24 hours. The operator reads an approved annotation as an RFC3339 timestamp and compares it with an injected clock. A missing annotation produces `RotationTimestampMissing`, an invalid date `RotationTimestampInvalid`, a future date outside tolerance `RotationTimestampInFuture`, and an expired deadline `SecretTooOld`.

This check confirms only a trusted metadata writer's assertion. If users can arbitrarily change the timestamp, they can reset the declared age without rotating credentials. Real control requires documented provenance and authorization to write that metadata.

## 13.7 Storm Control

Rapid Secret changes can create multiple rollout requests. Add a documented minimum interval between restart requests and a short debounce window, without losing the latest approved version. Recheck a pending observation before writing.

A new version arriving during a rollout does not require immediately issuing ten more patches. The first implementation can allow one active cycle per workload, then check the latest observed version. This policy adds a state machine and requires tests covering operator restarts.

## 13.8 The Rollback Boundary

The operator never restores an old secret from its memory or status, because it does not store it there. Credential rollback belongs to the trusted source and its procedure. Rolling back an application does not automatically restore its previous password, and restoring a password does not guarantee that the provider accepts it again.

**Checkpoint.** A rotation demonstration must include an invalid new value, a metadata-only change, Secret recreation, and an incompatible rollout strategy.
