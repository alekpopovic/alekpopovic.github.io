## Chapter 34 - Capacity Planning and Evolution

The provider-neutral architecture is intentionally simple, but simplicity is not the same as unlimited scale. Capacity planning identifies which limit will be reached first and provides an evidence-based path forward.

### Point-rate model

Estimate:

```text
points_per_second = active_subjects / average_interval_seconds
```

Then account for bursts. Ten thousand devices reporting every ten seconds average one thousand points per second. If half reconnect after a one-hour outage and upload sixty points per batch, the short-term batch and point rate can be much higher.

Model separately:

- HTTP requests per second;
- points per second;
- bytes per second;
- current-state updates;
- outbox events;
- WebSocket messages after coalescing;
- spatial evaluations;
- WAL generation;
- stored bytes per retention window.

### Database bottlenecks

Potential limits include:

- write IOPS and WAL flush latency;
- CPU for indexes and spatial functions;
- lock contention on latest-state rows;
- connection saturation;
- autovacuum lag;
- checkpoint spikes;
- partition and catalog overhead;
- long history queries evicting useful cache;
- worker queues competing with ingest.

Mitigations should follow measurements:

- increase batch size within latency goals;
- remove unused indexes;
- separate report replicas;
- tune checkpoints and storage;
- isolate worker concurrency;
- improve query predicates and partition pruning;
- precompute summaries;
- scale application roles horizontally;
- upgrade database hardware.

### WebSocket limits

Memory per connection, file descriptors, TLS cost, and message fan-out determine realtime capacity. Coalescing reduces message rate dramatically. Separate API and realtime process roles when connection load interferes with request latency, even if they share the same code and database.

Multiple realtime replicas can continue using outbox reconciliation and notifications until database event reads become the bottleneck.

### When to add a cache

Add a distributed cache only when a measured access pattern cannot meet targets through:

- a compact projection table;
- proper indexes;
- local bounded caches;
- read replicas;
- query reduction;
- client coalescing.

Document consistency requirements and invalidation. A cache must not become the only copy of current state.

### When to add a broker

A broker may be justified when:

- outbox dispatch database load is a significant measured bottleneck;
- consumers require independent replay and retention at high throughput;
- cross-region event distribution is needed;
- queue isolation and database maintenance interfere;
- the organization can operate the added system reliably.

The migration path is straightforward if event schemas are already versioned: an outbox publisher writes to the broker, consumers move gradually, and PostgreSQL remains the source of business facts. Keep a rollback path until delivery and replay are proven.

### When to split the database

Database separation is a major change. Consider it when the high-volume history workload and control-plane transactions have incompatible scaling, backup, or retention needs that cannot be solved by partitions, replicas, and hardware.

A possible evolution is:

- control-plane PostgreSQL;
- location-history PostgreSQL or specialized store;
- durable event bridge between them;
- explicit consistency model;
- replay and reconciliation tooling.

This introduces distributed transaction problems. It should not be the first response to a slow query.

### Multi-region

Active-active location ingestion across regions requires globally unique identifiers, subject ordering, device routing, conflict policy, and user-session strategy. PostgreSQL replication alone does not create a safe active-active design.

A simpler first step is:

- one write region;
- warm disaster-recovery region;
- replicated encrypted backups;
- tested DNS or endpoint failover;
- documented temporary offline mobile buffering.

The mobile queue gives the platform useful tolerance while a write region recovers.

### Cost model

Track cost drivers independent of provider:

- compute hours by process role;
- database CPU, memory, and storage;
- write and backup I/O;
- network ingress and egress;
- map tiles, routing, and geocoding;
- SMS or push integrations;
- support and on-call labor;
- retention duration.

Cost per active tracked hour or per million accepted points is more informative than total infrastructure cost alone.

### Chapter checklist

Capacity planning should:

- model points, requests, events, messages, WAL, and storage separately;
- include offline reconnect bursts;
- identify the current bottleneck with measurements;
- optimize PostgreSQL before adding systems;
- define evidence thresholds for cache, broker, or database separation;
- prefer a tested single-write-region DR plan before active-active complexity;
- measure cost per product unit.
