## Appendix F - Glossary and Further Reading

### Glossary

**ABAC**  
Attribute-based access control. Authorization based on attributes of the principal, resource, action, and context.

**Assignment**  
A time-bounded relationship authorizing a device to track a subject.

**Current-state projection**  
A compact representation of the latest accepted state, rebuildable from durable history.

**Device principal**  
The authenticated identity of a tracking device, separate from a human user.

**Geofence**  
A spatial shape and policy used to detect enter, exit, dwell, or proximity conditions.

**Idempotency**  
The property that repeating an operation with the same identity does not create additional effects.

**Location freshness**  
The age of an observation, usually current time minus `recorded_at`.

**Outbox**  
A database table containing durable events written in the same transaction as business state.

**PostGIS**  
A PostgreSQL extension providing spatial types, indexes, and functions.

**Public capability**  
A high-entropy bearer token whose database record defines narrow, expiring access.

**RLS**  
PostgreSQL row-level security, used here as defense in depth for tenant-owned rows.

**Sequence epoch**  
A generation that distinguishes valid device sequence ranges across reinstall, reset, or rotation.

**Snapshot plus delta**  
A realtime pattern in which a client loads current state and then applies versioned changes.

**Subject**  
The person, vehicle, package, equipment, animal, or custom asset being tracked.

**Tracking session**  
An explicit period of tracking with subject, device, activity, purpose, and privacy context.

**Wake-up signal**  
A non-durable notification that prompts a process to inspect durable state.

### Further reading

Use the current official documentation for implementation details and version-specific behavior:

- The Go programming language documentation and standard library reference.
- PostgreSQL documentation for transactions, locking, partitioning, RLS, `LISTEN/NOTIFY`, advisory locks, backup, and replication.
- PostGIS reference for geography, geometry, spatial predicates, indexes, and validity.
- Angular documentation for standalone components, signals, security, and build configuration.
- MapLibre GL JS documentation for sources, layers, clustering, and performance.
- Capacitor documentation for native plugin contracts and platform integration.
- Android documentation for foreground services, location permissions, background limits, and power behavior.
- Apple Core Location documentation for authorization, background modes, accuracy, and relaunch behavior.
- Nginx documentation for HTTP proxying, WebSocket upgrade, TLS, request limits, and stream proxying.
- OWASP guidance for authentication, authorization, SSRF, file upload, logging, API security, and secure headers.

### Closing note

The exact libraries and supported platform versions will evolve. Preserve the architecture by pinning reviewed dependencies, writing contracts before transports, measuring real behavior, and keeping durable facts independent from delivery mechanisms.
