# 4. Security Model and Authorization

## 4.1 Why This Is a Privileged Component

An operator that reads Secrets can access real credentials even when its README says “read-only.” Kubernetes security guidance emphasizes that `list` and `watch` on Secrets can expose their content, and creating workloads can provide a route to secrets available in the namespace. [S07](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)

Risk therefore depends on more than the number of RBAC verbs. Relevant questions include which namespaces are covered, who can create and modify contracts, who sees status, and who controls a consumer that might eventually receive an injected secret.

## 4.2 Threat Model

| Actor or Failure | Potential Problem | Design Control |
|---|---|---|
| Untrusted contract author | Probing another party's secret properties | Restrict authorship and approvals |
| Attacker able to modify a workload | Exfiltrating injected values | Separate mutation authorization |
| Parser defect | Value appears in an error message | Static codes; no raw errors |
| Compromised operator | Reading all permitted secrets | Namespaced RBAC and smaller scope |
| Excessive rule count | CPU and status load | Count and size limits |
| API outage | Stale positive status | Check generation and observation |
| CI debug mode | Accidental data output | No `set -x`; no Secret dumps |

## 4.3 Validation Oracle: Leakage Without Logging

Suppose a user can modify a `pattern` rule for a secret they otherwise cannot read, and can inspect the result. Repeated checks let that user infer properties of the content. The problem has not disappeared merely because status says “rule not satisfied” without showing a value.

Length, validity of a particular format, and even key existence can be sensitive. This follows from the system's design: every conditional result about a secret carries information. In the MVP, only trusted administrators already authorized for the corresponding Secret may create and modify contracts. Status readers receive only the metadata scope the organization accepts as visible.

For multiple untrusted tenants, adding `allowed: true` inside the contract is insufficient: the author could approve themselves. A separate protected grant policy, managed by another role, must bind the contract, Secret, allowed rule types, and any workload.

## 4.4 Why a Namespace Is Not Complete Authorization

Prohibiting cross-namespace references prevents a straightforward class of mistakes, but users within one namespace need not have equal rights. Two teams sharing a namespace may share application infrastructure without sharing secrets.

The proposed safe starting profile uses one namespace per trust boundary and trusted contract authorship. If this is unacceptable, implement and test the grant model first. Only then may the product claim support for untrusted contract authors.

## 4.5 Dual Approval for Mutation

In a later release, workload modification requires the installation to explicitly enable mutation, the corresponding RBAC profile to include workload `patch`, the contract to request the feature, and the workload administrator to approve the target. A single annotation that anyone can change is not a security control.

Protected approval binds to the contract UID, not just its name. Deleting and recreating a contract under the same name does not automatically inherit its previous approval. The mutation MVP permits only one contract to manage changes to a workload; multiple read-only contracts are allowed.

## 4.6 Leakage Surfaces

Secret values must not appear in structured log fields, `%+v` object dumps, panic payloads, tracing attributes, HTTP diagnostics, event messages, metrics, snapshot tests, or CLI debug output. Plain content hashes are also prohibited: for weak or predictable values, such a hash can help verify guesses.

Do not enable a public `pprof` endpoint. A heap dump contains actual process memory and may include secrets. Go provides no simple general guarantee of reliably erasing every copy of a value from the heap. Reduce copying, retention duration, and cached object count without claiming “zeroization guaranteed.”

Kubernetes recommends encryption of sensitive data at rest and restricted access. Base64 in a manifest is not encryption. For managed clusters, verify the provider's actual configuration rather than assume identical defaults across platforms. [S08](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

## 4.7 Admission Validation of the Operator's API

The CRD schema should reject duplicate keys, negative lengths, oversized lists, and inconsistent policy. However, a schema cannot prove that the author is entitled to learn properties of an arbitrary other secret. That is a separate authorization decision.

An operator using the grant model rechecks the grant during reconciliation. Revocation must stop new reads and new mutation operations. Replace old status with `Ready=False`, reason `AccessNotApproved`, excluding earlier validation details that should no longer be displayed under the new permissions.

## 4.8 Security Threshold for the First Public Release

Before release, tests must show that unauthorized references are rejected before data is read, all safe outputs exclude the sentinel value and its common encodings, mutation is disabled by default, and parser failures do not expose data.

Status and metrics carry a bounded number of findings. Key names are treated as metadata that may still be internal. Strict mode may display only a failure count and contract reason, but even that mode does not entitle untrusted authors to probe a secret without limits.

**Checkpoint.** A security review should answer: “Who can learn something new about a secret through this operator?” The answer “nobody, because we do not log” is insufficient.
