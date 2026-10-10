# 20. Meter Usage and Reserve Capacity Without Double Counting

**Part VI — State and Evidence**

A usage system must explain what it measured, how it handled missing observations
and how corrections work. It is not enough to multiply a session's age by its
configured CPU count and label the result actual consumption.

## Keep dimensions distinct

Requested vCPU-seconds, measured CPU time, reserved memory-seconds, actual memory
observations, persistent storage and tool calls are different dimensions. Name
them accordingly. A session requesting two vCPUs for ten minutes has 1,200
requested vCPU-seconds. That arithmetic says nothing about how busy the CPUs were.

Every event needs a stable identity, scope, resource, dimension, quantity, unit,
period and source. Include whether the quantity is measured, estimated or
allocated. Keep raw events append-only and derive aggregates reproducibly.
Corrections should reference the original event rather than silently rewriting
history.

## Deduplicate by event identity

A reconnect can deliver the same interval twice. A retry can publish the same
usage event twice. Use a unique constraint on source and event identity and keep
the original payload digest to detect conflicting reuse. Do not deduplicate by
rounded timestamp alone; two legitimate events can occur at the same instant.

For duration accounting, define interval endpoints and overlap behavior. A
monotonic local clock helps measure elapsed time, while wall-clock timestamps
locate the interval in a billing period. Clock correction can create apparent
negative or overlapping intervals. Retain sufficient provenance to reconcile
rather than silently clamping every anomaly.

## Reserve before provisioning

A concurrency quota should be reserved transactionally before the create command
is dispatched. A conditional counter update or row lock can serialize competing
reservations. An in-memory limit on each API replica cannot enforce a global
organization quota.

The Go teaching example demonstrates a concurrency-safe local reservation model.
It intentionally does not replace a database transaction shared by multiple
replicas. The SQL design shows the durable boundary; the lab requires a real
PostgreSQL execution to validate it. [S08](../references.md#s08)

Release a reservation when the corresponding obligation is actually resolved.
A lost heartbeat is not proof that compute stopped. Track uncertain allocations
and apply an explicit reconciliation or administrative override policy.

## Budgets are not ordinary rate limits

A rate limit controls request frequency over a window. A budget controls an
accumulated quantity or cost. A plan entitlement controls whether a feature is
available. Keep these mechanisms separate so that a billing-provider outage does
not unexpectedly become an authorization grant or a destructive workload action.

Soft thresholds generate notices and permit continued work. Hard thresholds
require a defined action: reject new sessions, stop renewing leases, prevent
particular tools or terminate according to a prior agreement. Do not silently
kill customer workloads because an aggregation job ran late.

## Model costs without inventing prices

A useful hypothetical model is:

```text
monthly operating cost = control-plane base
                       + managed active compute
                       + warm capacity
                       + persistent storage and snapshots
                       + network transfer
                       + telemetry and evidence retention
                       + support and incident response
```

BYOC moves much of execution compute to the customer, but it does not eliminate
control-plane hosting, support, integration maintenance or security work. A
managed mode also needs abuse prevention, payment risk and capacity planning.
Obtain real provider prices and workload measurements before making a commercial
forecast.

For a planning exercise, choose your own unit prices and label them assumptions.
Show sensitivity to active hours, warm capacity and retention. A margin that looks
excellent only when support time is assumed to be zero is not a useful business
model.

## Billing requires evidence and dispute handling

Customer-controlled connectors can be modified. Their metering reports are not
independent attestation of consumption. Decide whether billing is based on a
platform subscription, declared capacity, independently measured managed compute
or another auditable contract. Keep correction and dispute workflows separate
from security incident handling.

## Exercise

Simulate duplicate, overlapping and late usage events across a month boundary.
Produce the same aggregate from the same raw event set twice. Then apply a
correction event and explain the difference without deleting the original.
Stress the local quota example with concurrent requests and identify the
additional database invariant needed for multiple service replicas.

## Primary sources

[PostgreSQL 18 explicit locking](../references.md#s08)
