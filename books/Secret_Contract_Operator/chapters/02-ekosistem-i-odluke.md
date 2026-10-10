# 2. Its Place in the Kubernetes Ecosystem

## 2.1 Compose Rather Than Duplicate

External Secrets Operator translates declarations such as `ExternalSecret` into Kubernetes Secret objects. Its `Ready` condition describes the state of the synchronized target Secret, while refresh policies determine when external values are fetched. This is the boundary at which our operator takes over application-contract validation. [S02](https://external-secrets.io/latest/api/externalsecret/)

Secret Contract Operator receives no AWS keys, Vault tokens, or access to external APIs. Its minimum network requirement is the Kubernetes API, with an optional protected metrics endpoint. Separate responsibilities reduce the range of incident causes that one component must understand.

## 2.2 An Operator, Admission Control, or a CI Script

The Kubernetes operator pattern combines a custom resource with a controller that reconciles state. It is suitable when rules must be rechecked after initial deployment, such as when a dependency changes. [S03](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

A CI script is simpler for a one-time staging-configuration check, but it does not automatically react to a later rotation. An admission webhook can reject an object write before the API accepts it, but becomes part of that write's critical path. An operator that publishes status stays outside that path, at the cost of its result not automatically blocking the write.

The design decision is therefore: the operator maintains contract state; CI/GitOps uses that state as an explicit checkpoint; synchronous blocking remains a separate, optional layer. The MVP consequently does not depend on another webhook server's availability.

## 2.3 Go and Kubebuilder

Kubebuilder scaffolds Kubernetes API types, controllers, CRD generation, and supporting development artifacts. controller-runtime provides a client, manager, cache, event handling, and reconciliation machinery. Their versions must align with the scaffold and Kubernetes libraries. [S04](https://book.kubebuilder.io/)

Do not manually combine the newest individual `k8s.io` library with an older controller-runtime minor version merely because the import resolves. The version selected for the project is pinned in `go.mod` and accepted only after passing the local and CI test matrix.

## 2.4 Proposed Project Identity

| Element | This Book's Canonical Value |
|---|---|
| Name | Secret Contract Operator |
| Repository | `secret-contract-operator` |
| Proposed Go module | `github.com/CodepopTech/secret-contract-operator` |
| Proposed API group | `secrets.codepop.tech` |
| Initial API version | `v1alpha1` |
| Kind / plural | `SecretContract` / `secretcontracts` |
| Short name | `scn` |
| Annotation prefix | `secrets.codepop.tech/` |

The `secrets.platform.io` group in an earlier draft was an example. A published project should use DNS space controlled by its maintainer. This book consistently uses the proposed Codepop namespace; that is not an automatic migration of an existing cluster. If a CRD is already installed under another group, changing the group creates another API and requires an object-copying and validation plan.

## 2.5 Decisions That Avoid Early Technical Debt

One contract references one Secret in the same namespace. An ESO reference is not an arbitrary GVK: it is an `ExternalSecret` restricted to supported API versions. Workload references contain an explicit consumer list. The operator does not modify `ownerReferences` on Secrets or workloads owned by others.

The default installation has no workload write permissions. Validation-only operation is expressed through a real RBAC profile, not merely an `if` statement. There is no automatic takeover of application ownership and no finalizer that turns contract deletion into an availability problem.

## 2.6 Alternatives

If an application already performs reliable startup validation, the operator should provide earlier diagnostics rather than replace it. If secrets are consumed exclusively as files through CSI, this MVP cannot claim to validate those values because it does not read the pod's filesystem. If an organization mandates policy-engine controls, a contract can provide an additional signal without bypassing existing authorization boundaries.

It has not been established that no similar project exists. This design's value depends on a carefully bounded API, honest guarantees, and reliable behavior under load, rather than a claim of complete originality.

**Checkpoint.** Before the first commit, adopt the API group, minimum supported profile, and explicit list of features outside the MVP. These are architecture decisions, not README details.
