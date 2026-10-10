# 15. Observe the guard as an operating system

## Metrics should answer an action question

A count of requests is useful context. It does not tell you whether a desired ban reached the edge. An agent health status does not tell you whether log observations are current. Start each metric with the question an operator needs to answer.

For collection, ask whether observations are arriving and how old the oldest pending event is. For ingestion, ask whether commits succeed, duplicates rise unexpectedly, or validation conflicts appear. For detection, ask how many events are eligible and which rule is creating decisions. For delivery, ask how long desired state has remained unapplied. For the agent, ask which revision is active, whether time is healthy, and whether emergency bypass is enabled.

Avoid high-cardinality labels such as every client IP or request ID in metrics. Those belong in bounded event queries or logs. Metrics describe rates, capacity, and state classes. Unbounded labels can turn a defensive service into its own memory problem.

## Separate latency distributions

Measure request-check latency at the edge, not only inside the authorization function. Nginx pays for socket transport, scheduling, and response handling as well as a map lookup. Use a baseline with the guard disabled and compare an enabled run under the same workload and host conditions.

Measure completion-to-ingest delay and decision-to-applied delay separately. A detector may finish quickly while the collector batches for several seconds. A delivery worker may transmit quickly while an overloaded agent takes longer to persist policy. A single average hides both bottlenecks and tail behavior.

The source pack proposes initial targets of decision-to-applied p95 at most five seconds at 100 events per second and added authorization p95 at most two milliseconds at 1,000 requests per second. These are provisional acceptance targets. This edition has not measured them and does not use them as marketing claims.

## Capacity has several dimensions

Events per second, active decisions, assigned sites, edges per fleet, snapshot size, and retention length scale different components. A system handling many requests with few bans can have a cheap request view and a large history store. A fleet with many active bans can have low event traffic but expensive snapshot fanout.

Full snapshots simplify convergence. They also serialize the entire desired state for an edge. Coalesce rapid changes, cap bytes and entries, and measure serialization and transfer cost. Do not introduce a delta protocol until its ordering, missing-delta recovery, and compaction contracts are clear.

The lab's periodic push demonstrates safe replacement but creates a new revision and outbox record repeatedly. It is a teaching process, not a storage-efficient production dispatcher. Its database will grow during a long session. Stop it when the exercise is complete. The production retention and outbox cleanup tasks are part of the sixty-step pack.

## Retention is operational work

Set a short raw-event retention aligned with troubleshooting needs. Index the queries you actually run. Observe database disk use, cleanup duration, and how deletion affects active processing. Retaining history and retaining enough explanation for a decision are related but separate policies.

Do not put credentials in debug logs while diagnosing TLS failures. Report a bounded identity or fingerprint when appropriate, without serializing private keys or entire certificates into routine logging. Treat operator audit records as privileged evidence and scope access accordingly.

## Exercise

An operator sees no new bans, low CPU, and a healthy agent. Collection lag is twenty minutes and the future-event counter is zero. What should they investigate first, and why would increasing detector sensitivity be a poor response?

## Answer

Investigate the collector, transport, and ingestion backlog first. The analyzer's knowledge is stale even though the local agent is healthy. Increasing sensitivity does not make missing fresh observations arrive and may amplify false positives when the backlog drains. The freshness policy should keep those old observations from creating fresh bans.
