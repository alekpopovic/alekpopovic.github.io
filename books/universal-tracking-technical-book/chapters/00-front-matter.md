# Engineering a Universal Real-Time Tracking Platform {.unnumbered .unlisted .internal-title}

**Go, PostgreSQL, PostGIS, WebSockets, Mobile Location, and Native GPS Protocols**

**Aleksandar Popovic**

First Edition - October 2026

# Copyright and Edition {.unnumbered .unlisted}

Copyright (c) 2026 Aleksandar Popovic. All rights reserved.

This publication may contain code fragments intended for education and adaptation. The reader is responsible for validating security, privacy, licensing, regulatory, and operational requirements before production use.

Product names and trademarks remain the property of their respective owners.

# Preface {.unnumbered}

Real-time tracking is often described as a map with moving markers. That description is useful for a demo and dangerously incomplete for a production system. A real platform must accept delayed and duplicated measurements, preserve tenant boundaries, survive mobile network loss, protect people from invisible surveillance, decode devices that speak binary protocols, provide useful live updates without losing durable facts, and remain operable when the only mandatory infrastructure service is PostgreSQL.

This book presents a complete engineering approach for that problem. The target product can track people, vehicles, bicycles, packages, equipment, pets, event participants, and custom movable assets. It includes a Go API, a Go WebSocket gateway, PostgreSQL with PostGIS, an Angular operations dashboard, a public tracking experience, an Angular/Ionic/Capacitor mobile application, native Android and iOS location engines, and a native Go TCP/UDP/HTTP GPS gateway.

The architecture deliberately excludes mandatory cloud services, external message brokers, Redis, and an external GPS tracking server. That constraint is not a rejection of those technologies. It is a design exercise in building a strong, portable core with clear seams. When measured scale later justifies another component, the system can adopt it behind an interface instead of rewriting its domain.

The central claim of the book is simple:

> **PostgreSQL can be more than storage without becoming a trap, provided durable state, wake-up signals, background leases, spatial processing, and real-time delivery are assigned distinct responsibilities.**

The examples favor explicit SQL, bounded Go components, observable failure modes, and operational procedures that can be tested. Code samples are intentionally compact. They demonstrate the shape of a solution rather than replacing project-specific validation, threat modeling, or benchmarking.

## Who this book is for {.unnumbered}

This book is written for backend engineers, DevOps engineers, platform engineers, mobile engineers, technical founders, and architects who need to build or evaluate a location platform. Familiarity with Go, SQL, HTTP, Docker, and modern web development is helpful. Prior PostGIS or GPS protocol experience is not required.

## What you will build {.unnumbered}

By the end of the book, you will understand how to build a platform with the following capabilities:

- multi-tenant organizations, users, roles, permissions, and audit history;
- generic tracking subjects and time-bounded device assignments;
- explicit tracking sessions with activity and privacy context;
- batched, idempotent, sequence-aware location ingestion;
- immutable, time-partitioned history in PostgreSQL/PostGIS;
- a fast current-state projection for live maps;
- a PostgreSQL transactional outbox and leased job queue;
- WebSocket delivery that uses `LISTEN/NOTIFY` only as a wake-up signal;
- geofences, trips, stops, alerts, routes, and activity summaries;
- a resilient mobile queue with native Android and iOS location engines;
- public tracking links with expiration and precision controls;
- a bounded Go GPS protocol gateway for HTTP, TCP, and UDP devices;
- portable Docker Compose deployment, Nginx routing, backups, metrics, and disaster-recovery drills.

## Architectural constraints {.unnumbered}

The reference implementation follows these non-negotiable constraints:

1. All server-side application code is written in Go.
2. PostgreSQL with PostGIS is the only mandatory infrastructure service.
3. PostgreSQL is the durable source of truth.
4. `LISTEN/NOTIFY` carries identifiers or high-watermarks, not the only copy of an event.
5. Background work is stored in PostgreSQL and claimed with leases.
6. The web clients use Angular, strict TypeScript, Tailwind CSS, and MapLibre GL JS.
7. The mobile shell uses Angular, Ionic, and Capacitor, while background location uses native Kotlin and Swift.
8. Deployment remains provider-neutral through containers, files, standard protocols, and portable scripts.
9. Tracking people must be visible, bounded by policy, and auditable.
10. New infrastructure may be introduced only after measurements identify a real bottleneck and an accepted architectural decision records the migration.

## How to read the book {.unnumbered}

The chapters are arranged in dependency order. Parts I and II establish the domain and control plane. Part III builds the location data plane. Part IV covers clients. Part V adds business and device integrations. Part VI turns the software into an operable production system. The appendices provide schemas, contracts, and checklists that can be adapted directly.

A reader designing a new product should proceed in order. A reader reviewing an existing platform can start with the relevant chapter, but should also read Chapters 3, 6, 12, 15, 16, 28, and 31 because those chapters contain the most important cross-cutting invariants.

## Conventions {.unnumbered}

- Times are stored and exchanged in UTC unless explicitly stated otherwise.
- Database timestamps use `timestamptz`.
- Coordinates use longitude before latitude in PostGIS constructors.
- Distances are represented in meters and speeds in meters per second internally.
- Identifiers are opaque. Examples use UUID-like strings without depending on a specific library.
- HTTP examples use `/api/v1` for the public versioned surface.
- Error responses use stable machine-readable codes and separate human-readable messages.
- Shell examples assume a Unix-like environment.

## Safety and legal notice {.unnumbered}

Location data can reveal homes, workplaces, habits, health-related activity, and personal relationships. This book provides technical guidance, not legal advice. Production deployments must be reviewed against the laws, employment rules, consent requirements, and safety obligations that apply to the relevant jurisdictions and use cases.

# Acknowledgments {.unnumbered}

This book is authored by **Aleksandar Popovic**. It is informed by production patterns from distributed systems, mobile engineering, PostgreSQL operations, geospatial processing, and secure software design. The project favors boring, inspectable mechanisms over opaque convenience and treats operational evidence as part of the implementation.
