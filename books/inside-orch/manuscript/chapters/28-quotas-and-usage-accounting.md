# Chapter 28 - Quotas and Usage Accounting

Atlas API requests CPU and memory for each replica. A namespace operator wants to prevent uncontrolled growth and later understand its declared footprint. Both tasks require arithmetic, but neither is the same as measuring CPU consumption or charging money. An accepted quota check can bound an organization's declared intent while still leaving runtime enforcement and commercial accounting unresolved.

This chapter assumes resource quantities, namespaces and guarded mutations. You will calculate requested usage, explain why concurrent changes need one acceptance boundary, and follow snapshots into CSV export. The Atlas failure scenario is two simultaneous scale requests that each appear safe against the same old total. A second failure is interpreting summed snapshots as an invoice-ready duration measure.

## Requested Resource Arithmetic

ResourceUsage includes service count, replica count, CPU millicores, memory bytes, public-port declarations, secrets and registry credentials. addServiceUsage adds requests multiplied by replicas for CPU/memory. It increments service count once per service and public ports once per positive published-port declaration. It does not multiply public-port declarations by replica count. [Claim ch28.arithmetic](../../validation/evidence/ch28.json).

[internal/controlplane/controlplane.go, lines 2177–2187](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2177-L2187) at the locked revision.

```go
func addServiceUsage(usage *types.ResourceUsage, spec types.ServiceSpec) {
	usage.Services++
	usage.Replicas += spec.Replicas
	usage.CPUMillicores += spec.ResourceRequirements.Requests.CPU * int64(spec.Replicas)
	usage.MemoryBytes += spec.ResourceRequirements.Requests.Memory * int64(spec.Replicas)
	for _, port := range spec.Ports {
		if port.PublishedPort > 0 {
			usage.PublicPorts++
		}
	}
}
```

Suppose Atlas has two replicas, each requesting 250m CPU and 128Mi memory, and its spec declares one positive published TCP port. The service contributes one service, two replicas, 500 millicores, 268435456 memory bytes and one public-port declaration. A dynamic declaration with published_port zero does not add that same positive-port count at this boundary. This is declared service usage, not the number of actual host socket bindings.

Resource limits are not the quantities summed by this helper. A service requesting 250m with a larger limit contributes250m per replica to requested accounting. Likewise, an idle process and a busy process with the same declaration produce the same requested total. These distinctions are necessary when capacity planning, quota acceptance and observed utilization appear in one dashboard.

Deleted services are excluded from the usage inventory. A service scaled to zero can still contribute one service and its declared positive public ports, while contributing no requested CPU/memory through replicas. That behavior can surprise an operator who expects every dimension to become zero at scale zero. The code defines each dimension independently; document them before using an aggregate for decisions.

ResourceQuota uses zero as unlimited for each checked dimension. quota.Validate rejects negative configured limits. Check compares only positive limits against the projected usage and returns the first exceeded dimension in a fixed order. A zero CPU maximum is therefore not a request to prohibit CPU use; it disables that particular ceiling. Choose an explicit positive bound when the intended policy is finite.

StorageClaims appears in usage snapshots, but the current quota type/check does not add a corresponding storage-capacity limit. Counting claims is not measuring bytes stored, provisioned capacity or I/O. The source's implemented dimensions should not be broadened because a report contains a storage-related column.

## Atomic Quotas Under Concurrent Changes

MemoryService performs usage recomputation, quota checking and relevant state mutation under its mutex. For scale, it builds a candidate and computes usage with the old service excluded and the replacement included. Counting both would wrongly double-charge the update; counting neither would permit under-accounting. The lock is what makes the check and mutation one local acceptance boundary. [Claim ch28.concurrent-memory](../../validation/evidence/ch28.json).

The focused concurrency fixture starts two one-replica services under a three-replica quota. Two goroutines attempt to scale different services to two at the same time. Each change would be valid alone: total three. Both succeeding would produce total four. The executed test asserts exactly one success and one typed quota denial. It proves the MemoryService boundary for that scenario, not distributed coordination across independent server processes.

PostgreSQL has a distinct implementation. lockQuota acquires a transaction advisory lock derived from the namespace, and lockAndCheckQuota loads current usage plus the replacement/additions before checking. Store mutations using that helper execute within the transaction-scoped store. The lock lifetime and complete caller path matter: a helper called outside the encompassing transaction would not provide the intended serialized mutation. [Claim ch28.concurrent-store](../../validation/evidence/ch28.json).

[internal/store/postgres.go, lines 149–165](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L149-L165) at the locked revision.

```go
func lockQuota(ctx context.Context, db postgresDB, namespaceName string) error {
	_, err := db.Exec(ctx, `SELECT pg_advisory_xact_lock(hashtextextended($1, 0))`, namespaceName)
	return mapPostgresError(err)
}

func lockAndCheckQuota(ctx context.Context, db postgresDB, namespaceName string, replaceID types.ServiceID, replacement *types.ServiceSpec, addSecrets int, addRegistries int) error {
	if err := lockQuota(ctx, db, namespaceName); err != nil {
		return err
	}
	value, usage, err := loadQuotaAndUsage(ctx, db, namespaceName, replaceID, replacement, false)
	if err != nil {
		return err
	}
	usage.Secrets += addSecrets
	usage.RegistryCredentials += addRegistries
	return quota.Check(value, usage)
}
```

The default server remains MemoryService, so do not present this SQL protocol as the live executable's quota backend. The untouched PostgreSQL integration fixture also has the schema mismatch recorded earlier. Its failure is not a passing quota race. Source inspection supports the intended transaction/lock mechanism; a separate actual all-schema quota contention experiment would be needed before recording that specific database behavior as executed.

Typed quota.Error contains namespace, resource, limit, used and requested. In the current Check helper, Used and Requested are both set to the projected total being checked. They do not necessarily mean old total and incremental delta. If Atlas scale would project four replicas under a limit of three, the consumer should interpret the actual fields rather than subtracting a fictional delta.

The API returns a structured conflict for quota exhaustion. This differs from admission policy rejection and from malformed domain input. A client can explain which resource exceeded which limit without parsing English Error() text. The [focused executed suite](../../validation/labs/ch28/focused-tests.json) passed MemoryService allow/deny, concurrent scale, secret/credential quota and structured API conflict assertions.

The failure window is check-then-write without shared serialization. Reading total two in two independent requests and both approving an increment to three would violate the intended combined maximum. The mutex fixture catches this locally. Across processes, the SQL path must hold its namespace lock through the actual write; across other mutation paths, each path must participate. Jobs and GitOps restoration deserve separate inventories rather than being assumed covered by a service-scale test.

## Usage Snapshots and CSV Units

CaptureUsageSnapshots locks MemoryService, computes current requested service usage for each namespace, counts volume claims and accumulates task runtime from StartedAt to FinishedAt or the current time. It appends one snapshot per namespace and sorts the returned snapshots by namespace. The timestamp is the capture instant, not a billing-period boundary. [Claim ch28.snapshots](../../validation/evidence/ch28.json).

TaskRuntimeSeconds is particularly important. Each capture sums the lifetime-to-date duration of retained started tasks. It is not an incremental duration since the previous snapshot. A task started at12:00 and still running contributes60 seconds at12:01 and 120 seconds at12:02. Summing those two snapshots produces180 in report totals even though only120 seconds elapsed since start. This is how the current aggregation behaves; it must not be labeled integrated task-seconds for that interval.

GetUsageReport defaults its end to now and start to24 hours earlier when omitted. It selects snapshots whose timestamps fall within the supplied bounds, including equal endpoints, and sums each selected field into Totals. CPU and memory totals are therefore sums of sampled requested quantities, not time-weighted core-hours or byte-seconds. Sampling frequency changes those sums even if actual intent is constant.

The CLI export writes snapshot rows with a stable header: namespace, timestamp, cpu_millicores, memory_bytes, replicas, services, task_runtime_seconds, public_ports and storage_claims. Timestamp uses RFC3339 and runtime seconds are formatted to three decimal places. The export exposes observations for downstream analysis; it does not silently normalize them into commercial units.

| Column | Unit/meaning | Unsafe interpretation |
| --- | --- | --- |
| cpu_millicores | Requested CPU at capture | Measured CPU time |
| memory_bytes | Requested memory at capture | Peak resident memory |
| task_runtime_seconds | Retained task lifetime accumulated at capture | Incremental billable seconds |
| public_ports | Positive service declarations | Actual host bindings across replicas |
| storage_claims | Namespace claim count | Stored bytes or replicated capacity |

The actual snapshot aggregation test creates a two-replica service with 250m requests and one claim. It checks500 millicores and one storage claim, then verifies report service/replica totals. That is executed evidence for those assertions. It does not validate every export consumer, arbitrary time intervals or a complete accounting model. Preserve the distinction between inspected CSV formatting and the specific test cases that ran.

A robust downstream calculation would first decide which quantity it needs. To estimate reserved CPU-time, integrate the requested CPU value over well-defined intervals with a missing-sample policy. To estimate actual CPU-time, collect a different trustworthy measurement. To charge task runtime, avoid summing repeated cumulative lifetimes and define how deletion, retries and overlap affect identity. These are additional designs, not automatic meanings of the existing totals.

## An Export Boundary, Not a Billing System

The repository supplies operational quota decisions and usage reporting. It does not define prices, money, taxation, invoices, payment collection, customer contracts or dispute resolution. The original tenant-billing-export prompt motivates the report; its title is not evidence of a commercial billing engine. Calling the output a usage export accurately describes its current role.

Memory snapshots disappear with the default server's process state. Retention can also remove source task history or old observations according to its own rules. An operator relying on external historical analysis must arrange collection and storage outside this memory lifetime, while avoiding secrets in exported records. A present API response does not promise reconstruction of every past sample after a restart.

The known report dimensions also leave gaps. Pending desired replicas contribute requested usage even if no container has started. Job attempts and local storage need their own accounting interpretation. A claim count says nothing about whether a volume remains after workload deletion. These are reasons to document definitions, not to guess additional columns or invent measured values.

History starts with [f2836eabfff8e442d38984433f3e1f5c642667d1](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1), which batches quotas, image pinning and GitOps. [7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d) includes later operational usage/report work. Their actual changed code provides the historical connection; it does not certify invoice accuracy or deployment adoption.

For the safe Atlas lab, use only the disposable module and Go 1.25. No Docker or database is needed for the selected MemoryService/API tests. Predict one winner and one denial for concurrent scale, a projected usage error at the bound, and 500 millicores for the two-replica snapshot. Run:

```sh
go test ./internal/quota ./internal/controlplane ./internal/api \
  -run 'TestResourceQuota|TestConcurrentScaleCannotExceedQuota|TestSecretAndRegistryCredentialQuotas|TestUsageSnapshotAggregation|TestQuotaAPI' \
  -count=1 -v
```

The linked execution record preserves actual output and selected cases. Cleanup is process exit. An optional export exercise can use a separately owned in-process server and a bounded date range, then compare its CSV header and units with the code. Do not point the chapter at a production account or treat a synthetic task duration as a real host measurement.

## Exercises

1. Calculate CPU, memory, service, replica and public-port usage for the two-replica Atlas example. Which dimension is not multiplied by replicas?
2. Explain why two individually valid scale requests cannot both succeed under the three-replica fixture. Name the MemoryService and PostgreSQL mechanisms separately.
3. A task contributes60 seconds and then120 seconds in two snapshots. What does the current report total, and why is that not120 billable seconds?
4. Design a bounded operational export interpretation that avoids claiming measured utilization, storage bytes or invoices from the present columns.

[Worked answers](../solutions/ch28.md) show the arithmetic and evidence scope. Quota acceptance, sampled intent and task lifetime are useful quantities when named precisely; none should acquire a stronger meaning merely because it is exported as CSV.
