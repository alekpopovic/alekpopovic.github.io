# 3. Architecture and Data Flow

## 3.1 The Control Plane

The architecture separates observation, a deterministic evaluator, and result publication. The observation layer reads approved objects. The evaluator knows nothing about Kubernetes networking and does not log. The publication layer translates findings into bounded status, metrics, and events.

![Figure 3.1 — Responsibility boundaries: synchronization, validation, and application startup.](../assets/architecture.svg)

The MVP has no Secret-data flow into Git, CI output, or a separate database. Data exists in the Kubernetes Secret and temporarily in operator memory. Status contains observation metadata and finding codes. Types must express this distinction too: the validator result has no `Value`, `Actual`, `Input`, or `Snippet` field.

## 3.2 Components

`api/v1alpha1` defines the public API. `internal/contract` implements data validation. `internal/controller` manages reconciliation. `internal/status` constructs a stable result. `internal/dependencies` reads ESO and workload state. `internal/authorization` checks installation-level scope and approvals. `internal/telemetry` works only with safe results.

In a later phase, `internal/mutation` receives a separate interface. It accepts a change plan containing references and metadata, but no Secret content. This boundary reduces the risk of accidentally turning values into inline `env.value` entries.

## 3.3 One Reconcile as an Observation Transaction

The controller loads the contract and checks whether its namespace is allowed. It then checks that the reference is authorized before reading content. Only then does it load the Secret and record its `UID` and `resourceVersion` pair. Pure validation, optional dependency checks, and condition calculation follow.

This operator treats `resourceVersion` as an equality-check identifier without numeric arithmetic. Current Kubernetes documentation permits certain ordering comparisons for the same API resource type under specified conditions; our algorithm does not need them. Versions from different resource types are not compared as a shared transaction. The API supports optimistic concurrency, but does not provide an atomic update of an arbitrary Secret and Deployment. [S05](https://kubernetes.io/docs/reference/using-api/api-concepts/)

Compare the result with existing semantic status. If there is no difference, do not write. If a difference exists, use a status patch with an appropriate conflict check. On conflict, reread and recalculate rather than repeatedly writing the previously calculated status.

## 3.4 Event Sources

The main events are a `SecretContract` generation change, a referenced Secret change or deletion, a relevant workload change, and changes to the optional ESO object. A timer is needed for rotation age and any polling integration. Without a timer, a contract can remain green after its maximum age expires if no object changes.

Indexes map dependency names to contracts within the same namespace. An event from one namespace must not wake a contract using the same name in another. Mapping uses namespace and name; observations distinguish object recreation through the UID.

## 3.5 Cache as a Deliberate Decision

The controller-runtime client may use a cache for reads while sending writes directly to the API server. The library provides cache-behavior options and a separate uncached reader. Verify configuration against the project's version. [S06](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/client)

A simple namespaced MVP may use a standard Secret informer, but its cache then stores Secret content from the watched scope. This is not “metadata only.” Restricting namespaces reduces scope without removing the process's sensitivity.

A stricter profile can watch metadata and individually fetch approved Secrets through a direct reader. This reduces persistent cache retention, but increases API calls and watch-implementation complexity. Adding a label selector to a cache is not itself a security boundary: RBAC still determines actual permissions.

## 3.6 Error Handling

Invalid content is an expected negative result, not an infrastructure error. Set `Ready=False` without aggressive retries. A Secret `NotFound` is also a dependency state. `Forbidden`, an unavailable API, and discovery failure are different infrastructure findings.

Do not automatically copy an external error into public status. Some parsers and clients include input in their messages. Instead, use a stable code such as `DependencyAccessDenied` with a locally written message that excludes the original payload.

**Architecture invariant.** Data enters the validator but does not leave that boundary as diagnostic text. The rest of the system uses only controlled identifiers, counters, timestamps, and references.
