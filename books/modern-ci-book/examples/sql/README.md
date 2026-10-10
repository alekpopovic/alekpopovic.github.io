# PostgreSQL transaction illustrations

These files explain chapter 9. They are **not a complete persistence layer**
and were not executed against PostgreSQL for this edition. Use a disposable
empty database, never an existing service database.

`schema.sql` defines ownership and current-attempt relationships. `claim.sql`
contains a prepared statement that claims one eligible row, increments its
fence and inserts an attempt atomically. `complete.sql` accepts a terminal
result only from the matching, still-live attempt.

For a disposable database that you have explicitly created, a single psql
session can load the files and execute a smoke example:

```sql
\i examples/sql/schema.sql
\i examples/sql/claim.sql
\i examples/sql/complete.sql
INSERT INTO jobs (id, project_id, pool_id)
VALUES ('job-1', 'project-1', 'pool-1');
EXECUTE claim_job('project-1', 'pool-1', 'runner-1', '60 seconds', 'attempt-1');
EXECUTE complete_job('job-1', 'attempt-1', 1, 'runner-1', 'succeeded');
```

The psql working directory must be the book repository root. The session
must commit before a runner starts work. Do not keep a transaction open
while executing a command. Supply production values through driver parameters;
do not interpolate input into SQL strings.

An identical completion retry returns no rows in this illustration. A service
must read the stored attempt and distinguish an identical terminal result from
a conflicting or unauthorized message. A result timeout after commit is also
ambiguous: reconcile before attempting more work.

Omissions are deliberate: permission checks, capacity reservations, DAG readiness,
retry policy, expiry reconciliation, terminal-receipt fingerprints, transactional
outbox, tenant row policies and deployment target locks. Claim and capacity
reservation must be coordinated in the full design. A fresh attempt identifier
must not be reused for a different job.

Required live tests include competing claimers, aborted transactions, duplicate
attempt IDs, connection loss after commit, expired completions, matching project
and pool scopes, deadlock recovery and bounded concurrency. Go laboratory tests
do not validate this SQL.
