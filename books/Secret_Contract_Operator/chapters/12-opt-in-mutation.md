# 12. Optional Injection and Safe Workload Changes

## 12.1 Why This Is Outside the Initial Profile

Adding a Secret reference to a workload may grant access to a secret that workload could not previously use. An operator with workload `patch` permission becomes a privileged intermediary. Injection is therefore a security decision as well as a developer convenience.

The proposed `v0.2` initially supports explicitly authorized Deployments. StatefulSet and DaemonSet support follows only after strategy checks and appropriate E2E tests. The API can restrict supported kinds in advance, but release notes must clearly identify the mutation paths actually supported.

## 12.2 Required Prechecks

Mutation is allowed only when the installation enables the feature and write RBAC, the contract is authorized, the Secret and all relevant configured security rules are valid, the target workload is approved, and named containers exist. A conflict at one target must not lead to undocumented partial changes at other targets.

Plan every change before the first write, with status for each target. Kubernetes provides no atomic transaction across multiple workloads: if the third patch fails after the first two succeed, status must honestly describe the partial result, and the next reconcile must continue idempotently.

## 12.3 Modes and Field Ownership

`injection.mode: Disabled` is the default. `EnvFrom` adds one reference without changing the existing order or creating duplicates. `EnvVars` adds only missing explicit mappings. An existing environment-variable name with another source is a conflict and is not overwritten.

Do not put real values into `env.value`. Do not manage images, commands, service accounts, volumes, or sidecars. Do not remove user configuration merely because it is absent from the contract. Document narrow field ownership before implementing the first patch.

## 12.4 Patching Without Lost Changes

A merge patch over a container list can unintentionally overwrite a concurrent change when based on a stale object. Use read-modify-patch with an optimistic version check or a well-defined server-side apply model with narrow ownership. Do not use `force` as the default escape from ownership conflicts.

After a conflict, reload the workload, check approval, rebuild the plan, and only then retry the write. Otherwise, a new sidecar, environment entry, or securityContext added by another controller may disappear.

## 12.5 GitOps Ownership

If GitOps and the operator repeatedly change the same field, drift loops and repeated rollouts follow. The simplest production default remains: Git/Helm renders environment references, and the operator validates them.

For managed injection, document the exact paths owned by the operator and the configuration of the chosen GitOps tool. Do not ignore all of `spec.template` in diffs. That could hide a security-relevant image or service-account change.

## 12.6 Protected Approval

One approval concept is an annotation on the workload object containing the approved contract's UID. An admission or administrative rule must protect that annotation from unauthorized changes. The string alone is insufficient protection.

```yaml
metadata:
  annotations:
    secrets.codepop.tech/approved-contract-uid: >-
      317d81e8-2222-4444-8888-7491f91aa744
```

This is a proposed mechanism, not an already implemented Kubernetes feature. A more advanced system could use a separate grant resource with controlled authorship. In both cases, recheck Secret and workload approval on every change, not just when the contract is first created.

## 12.7 Idempotence and Disabling the Feature

A second reconcile does not add another identical reference. Disabling mutation immediately stops new changes without automatically removing previously added environment references. This is a conservative availability policy; removal requires an explicit administrative procedure.

Do not attempt an automatic revert if the workload has changed in the meantime. An old snapshot does not authorize overwriting new state. The operator should report what it did and what it stopped doing, rather than acting as a general configuration backup system.

**Checkpoint.** Test two simultaneous patches: one adds an environment reference through the operator, while the other adds a legitimate user change. Neither change may be silently lost.
