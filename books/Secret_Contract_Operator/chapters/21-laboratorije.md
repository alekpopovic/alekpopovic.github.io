# 21. Practical Labs

## 21.1 Prerequisites and Safe Scope

Lab A runs without a cluster. Labs B–E require an operator implemented according to this book's specification, an installed CRD, and a dedicated test namespace. These labs do not claim that an operator binary already ships with the book.

Check the context before every cluster test. Use a separate kubeconfig or a kind cluster. All values are test fixtures. No command should print a container's environment or the contents of a production Secret.

```bash
kubectl config current-context
kubectl create namespace sco-lab
```

## 21.2 Lab A: Local Validator

In the accompanying `examples/contractlab`, run the tests, race check, and vet. Add a `minLength` rule for a value containing a multibyte Unicode character. Demonstrate byte semantics with a test.

Then add an invalid URI containing a sentinel and verify that the public result does not contain its text. The goal is not merely for the validator to return `false`, but to return a controlled code and a safe result.

**Expected outcome:** tests pass, invalid cases produce predictable reasons, and no Kubernetes dependencies are needed.

## 21.3 Lab B: Missing Key

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: demo-secrets
  namespace: sco-lab
type: Opaque
stringData:
  DB_USERNAME: demo-user
---
apiVersion: secrets.codepop.tech/v1alpha1
kind: SecretContract
metadata:
  name: demo
  namespace: sco-lab
spec:
  secretRef:
    name: demo-secrets
  requiredKeys:
    - name: DB_USERNAME
    - name: DB_PASSWORD
      minLength: 16
```

Apply the manifest to the test cluster. Expect `SecretExists=True`, `KeysValid=False`, `Ready=False`, and `DB_PASSWORD` among the missing keys. Add a synthetic `DB_PASSWORD` through a file dedicated to the lab, then apply the manifest again.

**Expected outcome:** the Secret watch triggers another reconcile automatically and the contract becomes ready. No manual contract update is needed.

## 21.4 Lab C: Correct Explicit Consumption

The accompanying Deployment manifest uses an explicit image placeholder for a test application. Before running it, replace the placeholder with a verifiable digest of your own minimal application that does not print secrets.

```yaml
spec:
  template:
    spec:
      containers:
        - name: api
          image: YOUR_TEST_IMAGE_BY_DIGEST
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: demo-secrets
                  key: DB_PASSWORD
```

Add a workload reference with `containers: [api]`, `consumption: EnvVars`, and `requireWorkloadReference: true`. Then change the key reference to an incorrect name. The operator must update `WorkloadsConfigured`, but must not attempt to repair the Deployment automatically in the validation-only profile.

**Expected outcome:** findings follow actual consumer configuration; the operator has no workload patch permission.

## 21.5 Lab D: Stale Generation

Wait for `Ready=True`, then change the contract to require a new key that does not exist. Run the gate from chapter 14. The old Ready condition must not satisfy checks for the new generation.

Then deliberately stop the operator and repeat the scenario. The gate must time out or fail, rather than accepting a stale observation as new. Restarting the manager should resume normal reconciliation.

**Expected outcome:** a generation-aware gate demonstrates the value of versioned status, while documentation still acknowledges the race between checking and later reading the Secret.

## 21.6 Lab E: Rotation Policy Without Restart

Add a trusted test timestamp and `maxAge` to the contract. Use an injected fake clock to advance time without a long wait. Confirm that `RotationPolicySatisfied` becomes False even without a new Secret change.

When `requireRotationPolicy` is optional, aggregate Ready may remain True; when it becomes required, Ready must not. The test verifies the documented policy rather than whatever currently feels intuitive.

## 21.7 Lab F: Optional Restart

This lab applies only after the mutation phase is implemented. Enable installation-level permission, protected approval, and contract restart. Save the initial PodTemplate token, apply a valid synthetic Secret change, and check the new token and workload rollout.

Repeat with invalid content. The token must not change. Repeat with a metadata-only change; this book's policy permits a restart. Finally, test an OnDelete strategy and expect an unsupported mode, not a false-positive “restart completed.”

## 21.8 Cleanup

Remove lab contracts and workloads from the test cluster, then remove the namespace. Do not remove a shared operator CRD from a cluster used by others. With a dedicated kind cluster, deleting the cluster provides a clear cleanup boundary.

**Checkpoint.** The lab report states the scenarios actually run and their results. An example file does not prove that a scenario ran.
