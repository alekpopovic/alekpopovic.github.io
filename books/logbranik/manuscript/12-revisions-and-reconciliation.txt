# 12. Order updates across retries and restores

## A signature does not make a message recent

A revoked ban can still exist inside an old valid signature. Without ordering, replaying that envelope could reintroduce it. The agent therefore remembers the highest applied revision for its provisioned stream epoch. An incoming lower revision is rejected even if its signature is valid and its delivery interval looks acceptable.

A full snapshot is a complete replacement of remote desired state. It lists every assigned site, the central allowlist, and the active decisions. Missing decisions are removed. An empty decision list is a legitimate policy that clears remote bans. Revision gaps are harmless because the agent does not need every intervening change to reconstruct the latest state.

## Three ordering cases

| Incoming revision | Payload digest | Result |
| --- | --- | --- |
| Lower than applied | Any | Reject stale policy |
| Equal to applied | Equal | Return existing acknowledgement |
| Equal to applied | Different | Reject revision conflict |
| Higher than applied | Valid new policy | Persist and publish replacement |

An exact duplicate can be acknowledged after its delivery window expires because it changes nothing. A new revision cannot use that exception. Its delivery window must still be valid when applied. This distinction lets a sender recover a lost response without reopening a stale update path.

The acknowledgement contains agent identity, epoch, revision, and exact payload digest. A generic 200 is not enough. The sender checks that the receiver applied the content it intended to deliver. The companion's HTTPS push function performs those checks before reporting success.

## Persist the high-water mark with state

The revision, payload hash, and policy must survive a restart together. Saving a revision in one file and a ban list in another creates inconsistent crash states. The lab persists the signed envelope atomically and derives its verified high-water mark on restore. Production may use a different on-disk representation, but it must preserve that atomic relationship.

Update handlers are serialized. Request checks read one published immutable view. During a replacement, they can observe the old view or the new view, but never a partially mutated decision map. The test suite runs checks during publication and accepts only complete old or new outcomes.

## Push and pull have different jobs

Push reduces reaction time. Periodic authenticated pull reconciliation repairs a missed push and supports outbound-only edges. Both routes should pass through the same policy validator. Implementing one validator for push and a looser one for pull creates a second update protocol by accident.

The production design starts with a jittered fifteen-second reconciliation interval. That is a design default, not a measured service guarantee. The compact lab uses periodic push and does not implement an independent pull endpoint. Treat pull as a production task with its own timeout, authorization, revision, and expiry tests.

When a pending envelope expires before application, recompute current desired state and issue a new revision. Keep each existing decision's original expiry. Refreshing an envelope's delivery interval must not refresh the contained bans. Retrying a still-fresh envelope can reuse its exact stored bytes.

## Recover from central restore

A database restored from backup may have a revision counter lower than one already applied at an edge. The agent is correct to reject those older messages. Do not fix the error by disabling revision checks. Recover authenticated edge high-water marks and reconcile central counters under operator control, or explicitly re-enroll an agent with a new locally provisioned epoch.

The epoch is a stream identity, not a random field central may replace on every restart. The agent does not auto-accept a different epoch from a remote policy. Losing the edge's local state similarly requires a controlled fresh bootstrap; it is not evidence that an older snapshot should be trusted.

## Exercise

An edge has applied revision 42. Central is restored to revision 30 and sends a freshly signed revision 31. What should the agent do? What must an operator recover?

## Answer

The agent rejects revision 31. A fresh signature and timestamp do not make it newer than applied state. The operator must restore a central revision high-water mark consistent with authenticated edge reports, or deliberately provision a new epoch through the controlled recovery procedure. The lab has no automatic epoch reset command because that would conceal the trust decision.
