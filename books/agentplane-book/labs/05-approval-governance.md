# Approval and Gateway Bypass

## Prerequisites

Local harmless MCP tool, implemented policy boundary and distinct test identities.

## Procedure

Discover the tool without enabling execution. Test default denial, exact binding, changed input, expiry, self-approval policy, concurrent consumption and direct access around the gateway.

## Acceptance criteria

Only the intended action is authorized once. Downstream effects retain their own idempotency contract. Record actual enforcement locations and fail-closed behavior during authorization-service interruption.

## Evidence record

Record date, source revision, environment, exact commands, expected result, actual result, limitations and teardown status. Never attach secrets or customer payloads. A written procedure is not an executed result.
