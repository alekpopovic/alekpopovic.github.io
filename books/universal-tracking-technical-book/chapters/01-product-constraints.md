# Part I - Foundations {.part}

## Chapter 1 - Define the Product Before the Architecture

A universal tracking platform is not a fleet application with extra labels. The platform must represent any subject that can move, any device that can observe movement, and any policy that determines when the observation is legitimate. This distinction changes the database, the API, the mobile user experience, and the security model.

![The platform sits between tracked subjects, devices, operators, and external systems.](../assets/diagrams/system-context.png){width=96%}

### Start with actors and outcomes

The first design artifact should not be a service diagram. It should be a list of actors and decisions they need to make.

An operations dispatcher wants to know which couriers are available, which jobs are late, and whether an apparently stationary marker is a real stop or stale data. A runner wants accurate pace and route history without being visible after the session ends. A fleet owner wants vehicle history and maintenance signals, while a driver needs proof that private movement outside a shift was not recorded. A recipient wants a short-lived page showing an approaching delivery, not access to the courier's full history. An integrator wants stable contracts, idempotency, and signed webhooks.

Those outcomes produce the major product surfaces:

- an operations dashboard for organizations and teams;
- a mobile tracker for people carrying phones;
- public tracking pages for carefully scoped sharing;
- device ingestion for dedicated hardware;
- an API and webhooks for customer systems;
- reporting and export workflows;
- privacy and audit controls that are visible to the tracked person.

### Model capabilities, not verticals

A common mistake is to split the product immediately into "fleet," "courier," "sports," and "family" applications. The result is duplicated location storage, duplicated device registration, and inconsistent privacy behavior. A better strategy is to build one location core and compose vertical capabilities around it.

The core answers questions such as:

- Who or what is being tracked?
- Which device was authorized to observe it at this time?
- Which session, task, shift, event, or consent record allowed tracking?
- Which measurements were accepted, duplicated, delayed, suspicious, or rejected?
- What is the latest trusted state?
- Which derived facts were produced from which raw observations and algorithm version?
- Who viewed or shared the data?

Vertical modules then add business meaning. A delivery module adds stops, proofs, and recipient links. A sports module adds laps, pace, and elevation. A fleet module adds vehicle metadata and maintenance. They share subjects, devices, sessions, positions, routes, and authorization.

### Establish non-functional requirements

"Real time" is not a single number. Define separate service objectives:

- **ingestion acceptance latency**: time from request arrival until the batch is durably committed;
- **location freshness**: difference between `recorded_at` on the device and the current time;
- **live propagation latency**: time from commit until an authorized client receives a delta;
- **history availability**: how soon accepted points become queryable;
- **alert latency**: time from a qualifying observation until a notification job is created or delivered;
- **recovery objectives**: maximum acceptable data loss and service restoration time.

The device-to-server path is partly outside the platform's control. A phone may be offline for twenty minutes. A dedicated tracker may buffer packets. Therefore, server latency should be measured from `received_at`, while product UX should expose both `recorded_at` and freshness.

A reasonable first production objective might be:

| Capability | Initial objective |
|---|---:|
| Ingest API availability | 99.95% |
| Control API availability | 99.9% |
| P95 accepted-batch latency | under 300 ms |
| P95 commit-to-live-map latency | under 2 s |
| Durable loss after acceptance | zero by design |
| WebSocket reconnect recovery | under 10 s |
| Restore-point objective | measured and tested, not assumed |

These are targets, not promises. They must be validated by load and recovery tests on the actual hardware and data model.

### Estimate data volume early

Location systems become large through multiplication, not through large individual records. The daily point count is approximately:

```text
active subjects * seconds per day / reporting interval
```

For 10,000 active subjects reporting every 10 seconds:

```text
10,000 * 86,400 / 10 = 86,400,000 points per day
```

If each stored row, including indexes and tuple overhead, consumes several hundred bytes, the daily footprint can be tens of gigabytes. The exact value depends on columns, index selection, fill factor, compression opportunities, and retention. This is why the architecture needs batching, partitioning, a separate latest-state table, route simplification, and explicit retention before launch.

Do not size only for average traffic. Mobile clients reconnect after outages and upload accumulated batches. A race may start thousands of sessions within a minute. A carrier network recovery can create a synchronized burst. The ingestion API and database must absorb these patterns without forcing every live viewer to receive every historical point.

### Write product invariants

Invariants are rules that remain true across services, tables, and releases. Useful starting invariants include:

1. A location point is associated with exactly one organization, subject, device, and recording time.
2. A device can report for a subject only while a valid assignment or explicitly authorized session exists.
3. A human, a tracking device, an API client, and a public-share visitor are different identity classes.
4. A public link never expands access beyond its stored scope.
5. Raw accepted observations are not silently rewritten by derived algorithms.
6. Derived trips, stops, transitions, and alerts record their algorithm version and source interval.
7. Every tenant-owned query is scoped in Go, and critical tables also enforce row-level security.
8. Tracking of a person is visible and bounded by a recorded basis.
9. Normal logs do not contain exact coordinates, raw packets, tokens, or personal route history.
10. Database changes remain compatible with rolling processes until the contract phase is complete.

Invariants prevent a feature request from quietly changing the meaning of existing data. They also give tests something stronger to assert than individual endpoint responses.

### Use a staged product boundary

A production-capable first release does not need every vertical feature. It does need the full reliability chain. The minimum meaningful scope is:

- organizations, users, roles, and audit;
- generic subjects, devices, assignments, and sessions;
- mobile location capture with offline persistence;
- batched ingestion with idempotency and sequencing;
- partitioned history and latest state;
- a live map with reconnect recovery;
- basic geofences and alerts;
- public links with expiration and precision limits;
- backup, restore, monitoring, and field validation.

A large feature list without recovery behavior is still a prototype. A narrower system that survives duplicate uploads, process restarts, database failover, and mobile outages is the beginning of a product.

### Chapter checklist

Before designing components, confirm that the project has:

- named actors and decisions rather than only screens;
- explicit data retention and privacy expectations;
- separate latency objectives for acceptance, freshness, and propagation;
- realistic point-volume estimates and burst scenarios;
- domain invariants approved by engineering and product owners;
- a first release that includes operations and recovery, not only features.
