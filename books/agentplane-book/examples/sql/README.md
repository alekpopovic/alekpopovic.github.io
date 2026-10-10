# PostgreSQL Tenant Isolation Lab

This is an integration exercise. It requires a **disposable PostgreSQL database**
and a setup role allowed to create the test role. Never run it against an
application database. The setup is deliberately not rerunnable over existing
objects: a name collision stops rather than destroying prior state.

```sh
psql "$DISPOSABLE_DATABASE_URL" -f examples/sql/schema.sql
psql "$DISPOSABLE_DATABASE_URL" -f examples/sql/test.sql
```

`test.sql` switches to the restricted application role inside a transaction. It
checks a scoped read/write, a cross-organization write, an invalid project
reference, another tenant's read and missing context. Inserted session data is
rolled back. Setup objects and the cluster-wide NOLOGIN test role remain; remove
them only through the disposable environment's explicit teardown procedure.

The schema illustrates sessions only; it is not the full SaaS schema. The
application role can change its tenant setting, so this does not establish
isolation against arbitrary SQL injection. `quota.sql` is a parameterized design
fragment, not an executed migration. See the validation report for actual results.
