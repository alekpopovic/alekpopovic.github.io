# PostgreSQL Tenant Isolation

## Prerequisites

Disposable PostgreSQL database and explicit permission to create a test role.

## Procedure

Read examples/sql/README.md. Execute schema.sql and test.sql only in that disposable database. Add a reused-connection test with transaction-local tenant context.

## Acceptance criteria

Verify using the NOLOGIN application role through SET LOCAL ROLE. Capture expected rejection without real customer identifiers. Explain the application-controlled-context limitation. Teardown only the environment you created.

## Evidence record

Record date, source revision, environment, exact commands, expected result, actual result, limitations and teardown status. Never attach secrets or customer payloads. A written procedure is not an executed result.
