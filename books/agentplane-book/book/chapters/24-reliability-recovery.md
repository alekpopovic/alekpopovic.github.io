# 24. Design Recovery Before the First Production Incident

**Part VII — Product and Operations**

Availability is not one percentage shared by every feature. The API can remain
available while cluster commands are delayed; a customer workload can continue
while the SaaS is unavailable; evidence exports can lag while execution works.
Define service indicators around actual user journeys and trust boundaries.

## State objectives as targets until measured

A proposed provisioning latency target is an engineering goal. A recovery time
objective is a planning requirement. Neither is an observed guarantee until a
test or production measurement establishes it under stated conditions. Record the
environment, sample size and start/end definitions for every result.

Separate control-plane RPO from customer-workspace RPO. A database backup may
preserve session metadata without preserving customer files. A workspace snapshot
may preserve files without preserving recent approval or audit records. Recovery
must reconcile these timelines.

## Restore durable state carefully

Back up PostgreSQL, permitted object storage, configuration and the external
signer's recovery material according to its provider design. Keep encryption-key
availability in the restore plan. An encrypted backup that cannot be decrypted
is not a useful recovery artifact.

Restore into an isolated environment first. Validate schema, application-role
permissions, tenant isolation, audit integrity and outbox state. Do not point a
restored control plane at live customer connectors immediately. The restored
state may be older than the cluster resources and credential revocations.

## Old state can resurrect dangerous authority

A database restored from before a certificate revocation may mark that certificate
valid again. An old approval record may look unused even though its action
already executed. An outbox event may be replayed after its external effect
completed. These are security problems, not only data-consistency problems.

Maintain a recovery procedure that treats restored authorization state as stale
until reconciled. Reestablish current revocation and connection epochs, preserve
independent audit checkpoints and quarantine ambiguous execution records. Do not
blindly replay historical approval or execution commands.

## Rebuild transport from intent, not wishful replay

If PostgreSQL is the system of record, the transport can often be reconstructed
from durable operations and outbox state. But replay must preserve event IDs,
command IDs and downstream effect identity. Losing the inbox deduplication
history can make an old message dangerous again.

Retain deduplication and execution history for at least the recovery horizon
required by the operation contract. For external effects that cannot be proven,
return an unknown result and reconcile with the target system or an authorized
operator. Replaying everything is not a recovery strategy.

## Recover customer resources by observation

After restoring the control plane, compare current cluster resources with restored
intent. A sandbox created after the backup may be absent from the database. Do
not immediately delete it as an orphan. Enter a recovery mode that inventories,
quarantines or adopts resources only through a reviewed procedure.

Local workspace ownership and retention remain the customer's responsibility
according to the deployment contract. The SaaS must not claim that restoring its
own database restored every customer workload or file.

## Build incident runbooks around decisions

A useful runbook identifies symptoms, initial checks, containment, evidence
preservation, recovery and exit criteria. Include the permissions needed and the
risk of each action. Avoid a page containing only commands without explaining
when they are safe to run.

For a suspected connector compromise, containment may include gateway revocation,
local connector shutdown, workload quarantine, credential-provider revocation and
review of recent operations. Central revocation alone is insufficient if the
cluster is disconnected or local credentials remain valid.

## Exercise

Design a tabletop drill: the control database is restored from two hours ago,
a connector certificate was revoked one hour ago and a sensitive tool action
completed thirty minutes ago. Identify the records that can no longer be trusted
without reconciliation. Define how the platform avoids reauthorizing or repeating
the action while recovering service.
