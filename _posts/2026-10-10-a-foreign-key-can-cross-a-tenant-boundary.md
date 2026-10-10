---
layout: post
title: "A foreign key can cross a tenant boundary"
description: "A valid project ID proves existence. A scoped reference also proves that the project belongs to the right organization."
category: Security
book_id: agentplane
chapter_slug: 05-tenant-data
illustration: network
tags: [tenancy, postgresql, authorization, database, isolation]
---

A session creation request carries an organization ID and a project ID. Both refer to real rows. The insert passes every foreign-key check, yet the session belongs to one customer and points at another customer's project.

The database enforced the constraints it was given. The missing constraint was the relationship between those two identities.

## Put scope into the relationship

Imagine organization `north` owns project `analysis`, while organization `south` owns project `reports`. A session for `north` must never reference `south`'s project, even if a handler accidentally passes its ID.

Make `(organization_id, project_id)` a referenced key on the project table. The session's foreign key then carries both columns. The database can reject the mismatched pair during insertion, rather than waiting for an application query to discover it later.

This does not establish that a caller may use the project. Request authorization still needs to check the actor's rights. It establishes a narrower structural rule: the stored relationship cannot cross organizations.

## Follow the boundary beyond inserts

The same mistake can hide in a lookup cache. A cache indexed by `template-name` can return the first customer's runtime template to the next customer asking for that name.

Include organization and project identity wherever the resource's meaning depends on them. Review cache keys, background-job payloads and idempotency records alongside SQL queries. A scoped schema cannot repair an unscoped result retrieved before the database is consulted.

Use stable resource IDs for delayed work. A deleted project name may be reused; an old queued operation must not silently become work for the replacement project.

## Test through the real application role

Row-level security adds another boundary, but tests performed as a migration owner can tell a misleading story. Exercise the actual runtime role, including empty context and attempts to insert a row for another organization.

For pooled connections, set the authenticated organization inside the transaction that executes the protected queries. A session-wide setting left on a reusable connection can become the next request's inherited context.

## Manufacture the wrong association

Create two organizations with similarly named projects. Attempt a valid session insert, then substitute the other organization's project ID. Verify that the database rejects the second insert even when the application deliberately omits its ownership check.

Repeat through a background worker and a reused connection. The useful result is a boundary enforced along each path, with a clear explanation of which layer rejected the operation.
