# Delivery, Fencing and Unknown Outcomes

## Prerequisites

An implementation of the command pipeline in a disposable environment.

## Procedure

Repeat a command before and after acknowledgement. Interrupt the handler after an effect but before result persistence. Reconnect with a newer epoch and submit an older command.

## Acceptance criteria

Keep IDs stable. Assert deduplication and stale-authority rejection. For an irreversible effect with no recipient idempotency, show unknown outcome instead of automatic replay. This is an integration assignment, not implemented by the book.

## Evidence record

Record date, source revision, environment, exact commands, expected result, actual result, limitations and teardown status. Never attach secrets or customer payloads. A written procedure is not an executed result.
