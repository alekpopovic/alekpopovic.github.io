## Chapter 33 - Simulation, Load, Fault, and Field Testing

A tracking platform is a distributed system spanning sensors, mobile operating systems, networks, processes, and a database. Unit tests cannot establish production readiness on their own.

### Deterministic simulator

Build a Go simulator that generates:

- routes from fixtures or mathematical paths;
- walking, running, cycling, and vehicle profiles;
- accuracy noise;
- clock skew;
- delayed and duplicated batches;
- sequence gaps and resets;
- network outages and reconnect bursts;
- low battery and sensor attributes;
- device protocol frames;
- WebSocket viewers.

A seed produces the same scenario. Store expected outcomes such as accepted count, trip count, and geofence transitions.

### Canonical scenarios

Maintain end-to-end scenarios:

1. courier starts a shift, accepts a task, goes offline, completes stops, reconnects, and uploads;
2. runner shares a delayed public link and enters a private zone;
3. vehicle tracker reconnects and sends buffered binary records;
4. device credential is revoked during an active session;
5. late point changes a stop within the reconciliation window;
6. organization role is removed while a WebSocket subscription is active;
7. retention expires a partition except for a legal hold;
8. backup restores to a point before an accidental deletion.

These scenarios are executable documentation.

### Ingestion benchmarks

Measure at several levels:

- request decoding and validation;
- database transaction with batch sizes such as 10, 50, 100, and 500;
- partition routing and indexes;
- latest-state upsert;
- outbox insertion;
- mixed current and delayed points;
- burst after offline recovery;
- sustained endurance over hours.

Record hardware, PostgreSQL configuration, data volume, partition count, connection pools, and exact commit. A requests-per-second number without context is not useful.

### WebSocket tests

Test:

- connection establishment and authentication;
- subscription authorization;
- normal fan-out;
- thousands of marker updates with coalescing;
- slow readers;
- send-queue overflow;
- reconnect storm during rolling deployment;
- role revocation;
- missed `NOTIFY` reconciliation;
- snapshot and delta gap recovery.

Measure memory per connection and CPU per message class.

### Database capacity tests

Populate realistic skew:

- one very large organization;
- many small organizations;
- hot current day and cold older partitions;
- different subject reporting intervals;
- route queries with varied duration;
- retention and partition detach during ingest.

Inspect `EXPLAIN (ANALYZE, BUFFERS)`, WAL volume, checkpoint behavior, autovacuum, and index growth.

### Fault injection

Inject failures deliberately:

- kill API after commit but before response;
- kill worker after external delivery but before completion update;
- terminate a WebSocket replica;
- pause database network traffic;
- exhaust a connection pool;
- fill a test disk;
- delay or fail WAL archive;
- skew device and server clocks;
- corrupt or truncate protocol frames;
- deny filesystem writes;
- restart processes during migration overlap.

The expected behavior is documented before the test. A fault exercise is not random chaos without hypotheses.

### Fuzzing

Go fuzz tests are particularly useful for:

- JSON ingestion edge cases;
- geometry input;
- cursor parsing;
- WebSocket frames;
- Teltonika and GT06 decoders;
- file metadata and CSV export;
- public-link token parsers.

Assertions include no panic, bounded allocation, bounded runtime, no invalid accepted state, and deterministic errors.

### Mobile field study

A real-device study measures:

- point completeness against a reference route;
- observed interval distribution;
- battery consumption;
- background survival;
- offline queue recovery;
- timestamp and accuracy quality;
- behavior across manufacturers and OS versions;
- user-visible indicators and stop controls.

Run multi-day soak tests. Include stationary periods because GPS jitter and power policy often behave differently than during motion.

### Release evidence

A release candidate should include:

- clean-room build results;
- schema bootstrap and upgrade tests;
- end-to-end scenario results;
- load and endurance reports;
- fault-injection outcomes;
- backup restore evidence;
- mobile field results;
- known limitations and accepted risks;
- rollback verification.

### Chapter checklist

Production evidence includes:

- deterministic simulation;
- executable cross-component scenarios;
- sustained and burst ingestion benchmarks;
- WebSocket slow-client and reconnect tests;
- realistic database skew and maintenance load;
- hypothesis-driven fault injection;
- parser and contract fuzzing;
- real-device battery and background validation.
