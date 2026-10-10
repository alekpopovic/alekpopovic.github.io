# 1. The Problem We Are Solving

## 1.1 From an Available Secret to Usable Configuration

A typical platform successfully transfers a secret from AWS Secrets Manager, Vault, or another system into Kubernetes, yet the application still fails to start. A key name changed, a value is empty, JSON is invalid, or a Deployment references an old Secret. Synchronization technically succeeded; the contract between configuration and the application did not.

Kubernetes supports consuming Secret data through `envFrom`, `secretKeyRef`, and volumes. A required but unavailable Secret, or an individual required key, can prevent a container from starting. However, `envFrom` does not know that the application expects an additional key absent from the Secret object. Another layer must check semantic correctness. [S01](https://kubernetes.io/docs/concepts/configuration/secret/)

Secret Contract Operator makes that rule explicit. Instead of tribal knowledge and manual comparisons of `.env.example` files, the team gets a versioned declaration: the application expects `DB_USERNAME`, a nonempty `DB_PASSWORD`, and valid JSON in `PROVIDER_CONFIG`.

## 1.2 The Product's Precise Value

The operator's main result is not another copy of a secret, but **explainable contract state**. Users see which requirement was not met and which contract generation the controller checked. A pipeline can inspect that state before changing a workload. A platform team can alert on regressions after rotation without adding an SDK to every application.

A good first user is a team already using ESO and GitOps whose incidents occur at the boundary between secrets and applications. A poor initial target is a platform seeking a central password generator, database credential issuance, token revocation, and complete control over application restarts. That is a different product.

## 1.3 What the Operator Guarantees

For an approved reference and a successfully read Secret snapshot, the operator checks the declared rules and records the result with the identity of that observation. It does not write actual values, fragments of values, deterministic hashes of values, or parser errors that may contain data into status, events, or metrics.

This guarantee concerns outputs controlled by the implementation. It cannot remove a secret from kube-apiserver memory, TLS-protected transport, the Go heap, or a previously configured audit system. A safe operator must constrain these surfaces rather than claim they do not exist.

## 1.4 What the Operator Does Not Guarantee

A contract does not prove that a remote database accepts the password. `minLength: 32` does not prove entropy. JSON validation does not establish that the provider recognizes an API key. PEM decoding does not establish that a certificate is trusted, currently valid, or paired with a private key.

A contract does not control an already running process. Even after a successful rollout, the application may have its own cache, an incorrect variable name, or a misconfigured connection pool. Application readiness remains an independent signal.

## 1.5 Boundaries of the First Release

The proposed `v0.1` includes one local Secret per contract, key rules, stable status, an optional read-only ESO check, reference checks for Deployments, StatefulSets, and DaemonSets, metrics, and a namespace-scoped installation. It does not create Secrets, copy them between namespaces, use a mutation webhook, perform network credential tests, or automatically delete pods.

The proposed `v0.2` adds strictly authorized PodTemplate modification and a restart signal. Admission-based deployment blocking, aggregation of multiple contracts, and support for complex rollout controllers may follow. These version labels describe a development plan, not existing releases.

| User Need | MVP Response | Not Promised |
|---|---|---|
| Missing key | `KeysValid=False` and the key name | Filling in the secret |
| Invalid JSON | Stable `InvalidJSON` code | Repairing the content |
| ESO not ready | Optional blocking of `Ready` | Repairing cloud access |
| Deployment does not use the Secret | `WorkloadsConfigured=False` | Workload changes in v0.1 |
| Secret changed | A new observation and validation | Updating a running process's environment |

## 1.6 Success Criteria

The first release is useful when a new user can install the operator with understandable permissions, apply three small manifests, and receive an accurate diagnosis without reading the implementation. A demonstration with one valid Secret is not enough.

A public project also needs negative evidence: an unauthorized reference was not read, an invalid secret did not cause a restart, an unchanged contract did not produce endless status writes, and uninstalling the operator did not delete application data.

**Checkpoint.** Before implementation, write one sentence that distinguishes secret transfer, contract validation, and application health. If the product describes them as one thing, its scope is not yet precise enough.
