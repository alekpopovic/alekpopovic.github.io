# Part II - Identity and the Control Plane {.part}

## Chapter 6 - Tenant Isolation and Row-Level Security

A multi-tenant location platform stores unusually sensitive data. A missing organization filter is not a cosmetic defect; it can expose a person's historical movements. Tenant isolation therefore needs independent layers.

### Organization scope in every owned row

Every tenant-owned table contains `organization_id`, including child tables whose parent already has it. The duplication is intentional. It enables direct policies, partition-friendly indexes, and queries that prove scope without trusting a join.

```sql
CREATE TABLE tracking_subjects (
    id uuid PRIMARY KEY,
    organization_id uuid NOT NULL
        REFERENCES organizations(id),
    kind text NOT NULL,
    name text NOT NULL,
    status text NOT NULL,
    version bigint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (organization_id, id)
);
```

Composite foreign keys can ensure a child and parent belong to the same organization:

```sql
FOREIGN KEY (organization_id, subject_id)
REFERENCES tracking_subjects (organization_id, id)
```

### Request-scoped tenant context

The authenticated principal selects an organization through an explicit request context, not a client-controlled filter. The authorization layer verifies membership before opening a tenant transaction.

Within the transaction, set a local parameter:

```sql
SELECT set_config('app.organization_id', $1, true);
SELECT set_config('app.user_id', $2, true);
```

The third argument makes the setting transaction-local. This matters with connection pools: a tenant value must never leak into a later request using the same connection.

A Go transaction helper can enforce the sequence:

```go
func WithTenantTx(
    ctx context.Context,
    pool *pgxpool.Pool,
    tenantID uuid.UUID,
    userID uuid.UUID,
    fn func(pgx.Tx) error,
) error {
    tx, err := pool.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback(ctx)

    if _, err = tx.Exec(ctx,
        `select set_config('app.organization_id', $1, true)`,
        tenantID.String(),
    ); err != nil {
        return err
    }
    if _, err = tx.Exec(ctx,
        `select set_config('app.user_id', $1, true)`,
        userID.String(),
    ); err != nil {
        return err
    }
    if err = fn(tx); err != nil {
        return err
    }
    return tx.Commit(ctx)
}
```

Production code should also set timeouts, record transaction metrics, and classify retryable errors.

### Row-level security as defense in depth

Enable RLS on sensitive tables and create policies that compare the row's organization with the request context:

```sql
ALTER TABLE tracking_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracking_subjects FORCE ROW LEVEL SECURITY;

CREATE POLICY subjects_tenant_policy
ON tracking_subjects
USING (
    organization_id =
    nullif(current_setting('app.organization_id', true), '')::uuid
)
WITH CHECK (
    organization_id =
    nullif(current_setting('app.organization_id', true), '')::uuid
);
```

`USING` controls visible rows; `WITH CHECK` controls inserted and updated rows. `FORCE ROW LEVEL SECURITY` also applies policies to the table owner unless bypass privileges are used. The runtime role should not have `BYPASSRLS`.

RLS is not a reason to omit organization predicates in SQL. Explicit predicates improve query clarity and index use, while RLS protects against mistakes.

### Background workers

Workers process many organizations. They should claim a job in a system transaction, then execute tenant work in a new transaction with the job's organization context. Avoid a broad worker role that bypasses all policies for convenience.

Some truly global tables, such as migration metadata or a public permission catalog, do not need tenant scope. Document the exception. Do not let "global" become a default category.

### Public links and API clients

A public-share request does not become a user session. It resolves a hashed token to a capability record containing:

```text
organization_id
subject or session scope
allowed time window
precision policy
fields allowed
expires_at
revoked_at
```

The capability still establishes tenant context before reading data. API clients similarly carry organization and permission scopes. Separate identity classes reduce accidental privilege reuse.

### Cross-tenant tests

Every repository and endpoint that reads tenant data should have a negative isolation test. A reusable suite can create two organizations with similar objects and assert that principals cannot:

- fetch by a foreign ID;
- infer existence from different errors;
- update or delete a foreign object;
- reference a foreign subject in a child record;
- subscribe to a foreign WebSocket channel;
- export a foreign route;
- exploit pagination cursors across tenants.

Run direct SQL tests with the runtime role and missing context. The expected result is no rows or a policy error, not global visibility.

### Avoid side channels

Isolation includes more than rows. Review:

- cache keys, even for in-process caches;
- metrics labels;
- file paths and download handlers;
- error messages and timing differences;
- sequential external identifiers;
- WebSocket channel names;
- audit and search indexes;
- background job payloads;
- exported filenames and temporary directories.

Do not put raw organization names, user email addresses, or precise coordinates in metric labels. Labels create long-lived high-cardinality data and may be visible to broader operations roles.

### Chapter checklist

Tenant isolation requires:

- `organization_id` on every tenant-owned row;
- explicit organization predicates in repositories;
- transaction-local database context;
- RLS policies with `USING` and `WITH CHECK`;
- runtime roles without RLS bypass;
- tenant-scoped worker execution;
- separate public and API-client capabilities;
- automated cross-tenant penetration tests.
