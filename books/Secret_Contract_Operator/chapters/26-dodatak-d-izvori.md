# Appendix D. Glossary and Bibliography

## D.1 Glossary

**Admission.** Checking or modifying a request before the Kubernetes API accepts it.

**Condition.** A typed state signal with status, reason, and generation.

**Contract.** A declaration of expected secret properties and consumption.

**Controller.** A process that repeatedly reconciles desired and observed state.

**CRD.** A definition of a custom resource type in the Kubernetes API.

**EnvFrom.** A grouped source of environment variables for a container.

**EnvVars.** This project's name for explicit secretKeyRef mapping mode.

**Generation.** The version of an object's relevant specification that a controller must observe.

**Grant.** A protected decision about who may read or modify a specific target.

**Idempotence.** Repeating the same operation causes no additional unwanted effect.

**Informer.** A mechanism for watching resources and maintaining local observations.

**Mutation.** Changing a resource; in this book, mainly PodTemplate references or annotations.

**Observation.** A snapshot of inputs that the controller actually checked.

**Oracle.** Output that allows inference about otherwise inaccessible data.

**Owner reference.** A Kubernetes ownership link; it must not be added to another party's resource without authorization.

**PodTemplate.** A declaration from which a workload controller creates pods.

**Reconcile.** One attempt to align the current state.

**ResourceVersion.** An API-object version identifier; used here for equality checks.

**Rotation.** Changing the underlying credential, not necessarily every Secret object change.

**Secret.** A Kubernetes resource for sensitive configuration data.

**Status subresource.** A separate API path for reporting custom-resource state.

**TOCTOU.** The gap between checking state and using that state later.

**UID.** The identity of one object lifetime, distinct from its name.

**Workload.** A resource managing pod execution, such as a Deployment.

## D.2 Primary Sources

The original edition records these sources as checked on October 10, 2026. Documentation using `latest` or unversioned paths can change. For implementation, use documentation matching the project's pinned versions. These sources do not constitute an audit of our operator.

### S01 — Kubernetes — Secrets

Native Secret objects and consumption methods. [Open official source](https://kubernetes.io/docs/concepts/configuration/secret/).

### S02 — External Secrets Operator — ExternalSecret

Synchronization, target, refreshTime, and conditions. [Open official source](https://external-secrets.io/latest/api/externalsecret/).

### S03 — Kubernetes — Operator pattern

Custom resources and the operator pattern. [Open official source](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

### S04 — Kubebuilder — Introduction

Scaffolding and Kubernetes API development. [Open official source](https://book.kubebuilder.io/).

### S05 — Kubernetes — API Concepts

Object versioning, reads, and concurrency. [Open official source](https://kubernetes.io/docs/reference/using-api/api-concepts/).

### S06 — controller-runtime — client package

Clients, readers, and optimistic merge patches. [Open official source](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/client).

### S07 — Kubernetes — RBAC Good Practices

Privileges, Secret reads, and indirect access. [Open official source](https://kubernetes.io/docs/concepts/security/rbac-good-practices/).

### S08 — Kubernetes — Good Practices for Secrets

Access controls and secret handling. [Open official source](https://kubernetes.io/docs/concepts/security/secrets-good-practices/).

### S09 — Kubebuilder — Generating CRDs

Markers, status subresources, and schema generation. [Open official source](https://book.kubebuilder.io/reference/generating-crd.html).

### S10 — Kubebuilder — Configuring envtest

API server and etcd without a full workload control plane. [Open official source](https://book.kubebuilder.io/reference/envtest.html).

### S11 — Go — regexp package

Regexp semantics and linear execution. [Open official source](https://pkg.go.dev/regexp).

### S12 — Go — Fuzzing

Built-in fuzz testing. [Open official source](https://go.dev/doc/security/fuzz/).

### S13 — Kubernetes — Extend API with CRDs

Structural schemas, defaults, and subresource capabilities. [Open official source](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/).

### S14 — Kubebuilder — Watching Resources

Watches, event mapping, and predicates. [Open official source](https://book.kubebuilder.io/reference/watching-resources.html).

### S15 — controller-runtime — cache package

Informer-cache configuration and scope. [Open official source](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/cache).

### S16 — Kubernetes — Define Environment Variables

Container environment configuration. [Open official source](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).

### S17 — Kubernetes — Distribute Credentials Securely

Secret consumption and environment-value updates. [Open official source](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/).

### S18 — Kubernetes — Deployments

PodTemplate changes and rollout strategies. [Open official source](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

### S19 — Kubernetes — StatefulSets

RollingUpdate, OnDelete, and partition behavior. [Open official source](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

### S20 — Kubernetes — DaemonSet

DaemonSet lifecycle and updates. [Open official source](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/).

### S21 — Kubernetes — Disruptions

PDBs and limitations during workload rolling updates. [Open official source](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/).

### S22 — Kubernetes — Admission Webhook Good Practices

Availability, scope, and admission-control risks. [Open official source](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/).

### S23 — Prometheus — Metric and Label Naming

Units, naming, and cardinality. [Open official source](https://prometheus.io/docs/practices/naming/).

### S24 — Helm — Custom Resource Definitions

CRD installation and lifecycle limitations. [Open official source](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/).

### S25 — OpenAI — Custom Instructions with AGENTS.md

Project instructions for a coding agent. [Open official source](https://developers.openai.com/codex/guides/agents-md/).

### S26 — GitHub — Secure Use of Actions

Permissions, untrusted input, and Actions pinning. [Open official source](https://docs.github.com/en/actions/reference/security/secure-use).

### S27 — Kubernetes — Versions in CRDs

Served/storage versions, conversion, and migration. [Open official source](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/).

## D.3 Maintaining This Edition

Implementation changes update the canonical specification and tests first, then examples, prompts, and documentation. PDF, EPUB, and combined Markdown must be rebuilt from the same text. Individual chapter files are the editorial source; editing only the PDF manually is not a maintainable workflow.

For the next edition, recheck library dates and behavior, but do not change tool versions without a tested matrix. Add a book changelog for every API, security-guarantee, or lab-code change.
