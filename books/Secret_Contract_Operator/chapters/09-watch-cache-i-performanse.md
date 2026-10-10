# 9. Watches, Indexes, and Performance

## 9.1 From a Dependency to Its Contracts

A Secret change should trigger only contracts that use that Secret. Listing all contracts and filtering them manually for every event works in a small demonstration, but creates unnecessary work in a larger cluster.

Register an index for `spec.secretRef.name` when the manager starts. For a Secret event, the controller lists contracts with the matching field in the same namespace. A workload index uses a composite key such as `apps/v1|Deployment|payments-api`, with the namespace as a separate constraint.

```go
// Reference snippet. The field name is a private index constant.
const secretNameIndex = "contract.secretName"

err := mgr.GetFieldIndexer().IndexField(
    ctx,
    &apiv1.SecretContract{},
    secretNameIndex,
    func(obj client.Object) []string {
        c := obj.(*apiv1.SecretContract)
        if c.Spec.SecretRef.Name == "" {
            return nil
        }
        return []string{c.Spec.SecretRef.Name}
    },
)
```

The corresponding map handler does not log the Secret object. If the indexed list fails, record a safe operational reason; do not silently fall back to an unlimited cluster-wide search.

## 9.2 Owned and Non-owned Resources

Secrets and Deployments are not objects this operator owns. Do not add `Owns(Secret)` and expect correct mapping when no owner reference exists. Use an explicit watch and mapping function for external dependencies.

Kubebuilder documents watch and predicate mechanisms for filtering events and directing reconciliation. Choose a model that reflects actual object ownership. [S14](https://book.kubebuilder.io/reference/watching-resources.html)

## 9.3 A Predicate Is Not a Universal Filter

For the primary CR, ignoring status-only changes and reacting to generation changes is useful. However, the same `GenerationChangedPredicate` must not automatically apply to Secret events: Secret changes need not have the same generation semantics as a CR specification.

For Secrets, watch relevant version changes, creation, and deletion. For workloads, observe the PodTemplate and relevant approvals without turning harmless status updates from the workload controller into an intensive loop.

If authorization depends on annotations or grant resources, their updates must trigger a watch. A filter that responds only to `.spec` could miss revoked access.

## 9.4 The Metadata-only Profile

The controller-runtime cache can be configured by type and namespace scope. These choices affect both memory usage and read consistency. [S15](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/cache)

For the hardened profile, a metadata watch is different from reading a full Secret and deleting `Data` after logging. Sensitive data should never enter a general cache that the evaluator does not need. Use a direct reader after checking approval, without leaving the data in an additional application-level cache.

This profile requires concrete tests against the chosen library: which object the event handler receives, whether an accidental `Get` through the cached client can start a full informer, and how watch reconnection behaves. Without these tests, do not claim that the cache is “secret-free.”

## 9.5 Load Budget

If `N` contracts are polled every `T` seconds, the approximate baseline is `N/T` evaluations per second, before retries and actual changes. For 10,000 contracts and a 300-second interval, this is approximately 33.3 evaluations per second. This is a planning calculation, not a measured implementation result.

If each contract directly reads three dependencies, API requests grow proportionally. Indexes do not remove this work; they remove unnecessary consumer searches when an event arrives. Schedule time checks around expiration deadlines, with bounded fallback polling where needed.

## 9.6 Backpressure and Fairness

Set a bounded number of concurrent reconcile workers. Test whether one Secret with many contracts can crowd out others. Jitter prevents all contracts from repeating time checks simultaneously after a restart.

Do not hold a global mutex while reading the API. Keep critical sections minimal for small cache and limit structures. A contract's controller must remain safe when an error quickly returns the same key to the queue.

## 9.7 Measurement Without False Promises

A benchmark report records namespace count, contract count, key count, value sizes, changes per second, cache profile, CPU and memory limits, and exact tool versions. Measure P50/P95/P99 latency to new status, API requests, and status writes.

Targets such as “P95 below five seconds” can be initial acceptance thresholds, but must not be published as performance results until measured. Do not present a simulated workload as a production benchmark.

**Checkpoint.** Changing one Secret should cause the expected number of dependent reconciles, not a cluster-wide recalculation. Measure the second reconcile without changes as well.
