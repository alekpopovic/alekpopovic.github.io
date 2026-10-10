# 14. Give operators precise controls

## An automatic system still needs intervention

An operator must be able to inspect evidence, change a site mode, revoke a decision, protect known infrastructure through an allowlist, and activate a local recovery mechanism. Those are different operations with different authority. A button labelled "unblock" can be ambiguous if it merely edits desired state while an edge remains disconnected.

Use status language that tells the operator what is known. A revocation can be committed centrally, queued for delivery, acknowledged by one edge, and pending on another. The central audit should record the intention. The applied-revision record should show the effect. Do not overwrite one with the other.

## Practice revocation in the lab

Create the lesson 4 fixture, switch to enforce mode, and inspect the decision:

```bash
python3 -m logbranik decisions
```

Copy its actual ID into the revoke command:

```bash
python3 -m logbranik revoke ACTUAL_DECISION_ID
```

The token above denotes the ID you just inspected; it is not a literal example ID that the program knows. With the delivery loop running, a new full policy omits that decision. Check the local handler again and confirm allow. If the control connection is offline, central revocation alone does not remove already applied state. Local expiry remains the maximum lifetime boundary.

The lab does not provide a full operator HTTP API or a fleet dashboard. Its CLI is an intentionally small administration surface for one demonstration site. The production pack specifies authenticated roles, bounded queries, idempotency keys, audit records, and desired/applied status separation.

## Manual decisions

A production manual block needs an exact target, an explicit site or global scope, a reason, an operator identity, and a mandatory TTL. A global scope must be explicit rather than inferred from a missing site. Automatic network-range decisions are excluded from the baseline design because their blast radius is larger than an exact-address decision.

Make manual requests idempotent. A CLI command can time out after the central transaction commits. Retrying with the same idempotency key should return the original effect rather than creating another ban with a new lifetime. A repeated command and a deliberate new intervention are different actions.

Mode and allowlist changes benefit from optimistic concurrency. An operator should know if another person changed the configuration between reading it and saving it. Silent last-writer-wins behavior can remove a newly added exemption or re-enable enforcement after a maintenance decision.

## Keep emergency controls local

A remote signed policy must not be able to remove the edge's independent emergency address list or bypass setting. Central may control ordinary policy, but recovery authority should remain available when central credentials or logic are the source of the incident.

Local bypass needs visible state. Include it in health responses and heartbeat reports, display it prominently in the operator interface, and alert if it remains active beyond the intended maintenance period. A recovery mechanism that becomes a forgotten permanent mode defeats the reason for the guard.

## Evidence retention

An explanation may outlive raw event retention. Store bounded evidence references and a concise detection summary when making a decision. Otherwise an operator can see a ban but find that its explanation disappeared during cleanup. Retain only what the investigation and policy require; keeping every raw observation indefinitely creates cost and access risks.

The teaching decision table has a reason code and timestamps. Its evidence is found through the associated site/address/window observations. The production schema should attach explicit evidence identities or summaries so that historical explanations remain stable after unrelated database maintenance.

## Exercise

Design the response to a manual revoke request for an address enforced on two edges, one of which is offline. Which states should the operator see immediately and later?

## Answer

Immediately, the central decision is revoked and delivery is pending for both relevant edges. Later, the connected edge reports the new revision and the revocation becomes applied there. The offline edge remains pending until reconciliation or the original local expiry. The response must not claim fleet-wide enforcement has already changed merely because the central transaction succeeded.
