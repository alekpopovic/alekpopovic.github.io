# 05. Design Tenant-Safe PostgreSQL Data

**Part II — Control Plane**

Tenant isolation is not a field naming convention. It is a property of every
query, reference, transaction and administrative path. AgentPlane uses an
organization as the top-level customer boundary and a project as a narrower
operational boundary. Resources belong to both whenever project scope applies.

## Use references that carry scope

A sandbox row should reference a project through the pair
`(organization_id, project_id)`. A plain `project_id` foreign key can prove that a
project exists while failing to prove that it belongs to the sandbox's
organization. Composite references make an important class of accidental
cross-tenant association impossible at the database boundary.

The teaching schema in [examples/sql](../../examples/sql/README.md) creates
organizations, projects and sessions with composite keys and a row-security
policy. It is intentionally smaller than the final domain. Expanding it into a
production database requires migrations, deletion policy, indexes, operational
roles and measured query plans.

```sql
-- Design fragment: authenticated organization context must be set inside
-- the same transaction that issues the protected query.
BEGIN;
SELECT set_config('app.organization_id', $1, true);
SELECT id, status
FROM agentplane_book.sessions
WHERE organization_id = $1::uuid AND project_id = $2::uuid;
COMMIT;
```

This fragment uses bind parameters; it is not a standalone psql script. The third
argument to `set_config` makes the setting transaction-local. Reusing a pooled
connection after a session-level setting can otherwise carry one tenant's
context into another request.

## RLS is defense in depth

PostgreSQL row-level security can restrict visible and writable rows. Table
owners normally bypass it unless forced, and roles with `BYPASSRLS` or superuser
privileges are not constrained in the ordinary way. Therefore test the actual
application role, not only a migration owner. [S07](../references.md#s07)

Use `USING` for visible rows and `WITH CHECK` for new row values. Enable and force
RLS for tenant-owned tables where appropriate. Keep the runtime role separate
from schema ownership and grants administration. Revoke unnecessary schema
creation rights and avoid casually introducing `SECURITY DEFINER` functions.

An application-controlled tenant setting is not cryptographic authorization.
Anyone who gains arbitrary SQL execution as the application role may be able to
change that setting. RLS helps contain accidental query omissions; it does not
replace parameterized SQL, application authorization or separate databases when
a stronger tenant threat model requires them.

## Scope caches and uniqueness

Cache keys need organization and project identity just as SQL queries do. A cache
indexed only by `runtime-name` can return another tenant's template. Idempotency
keys need scope too: include the authenticated actor or service account, tenant,
operation and request digest. A globally unique idempotency key accidentally
becomes a cross-tenant coordination channel.

Use unique constraints for public resource names only within their intended
scope. Decide whether soft-deleted names can be reused. Partial unique indexes
can express active-name uniqueness, but historical operations must retain stable
resource IDs so a retry never targets a new resource with an old display name.

## Keep transactions bounded

Do not hold a database transaction open while waiting for Kubernetes or a human
approval. Write intent, audit metadata and the outbox event together, commit,
then do external work. If dispatch fails, a worker can retry from the outbox.
The transaction establishes a durable decision boundary, not end-to-end success.

For quota reservation, lock a small per-scope counter row or use a conditional
update. Avoid “count sessions, then insert” without concurrency control. Two
requests can observe the same count and both exceed the limit. PostgreSQL row
locks provide the necessary coordination, but long lock duration and inconsistent
lock order can create deadlocks. [S08](../references.md#s08)

## A practical test matrix

Test read, insert, update, delete and foreign-key substitution as the runtime
role. Include an empty tenant context, malformed context, another organization,
another project in the same organization and a reused pooled connection. Verify
that a batch endpoint cannot mix authorized and unauthorized resource IDs.

Administrative exports need an explicit scoped job identity. Do not solve every
background-job problem with a permanent unrestricted connection. Maintenance and
migration roles may need stronger permissions, but their use should be separate,
audited and unavailable to normal request handlers.

## Exercise

Run the SQL lab in a disposable database. Record both a successful scoped read
and a rejected cross-organization insert. Explain why a successful test as a
superuser says little about application RLS behavior. Extend the lab with a
runtime-template table whose references cannot cross project boundaries.

## Primary sources

[PostgreSQL 18 row security](../references.md#s07) · [PostgreSQL 18 explicit locking](../references.md#s08)
