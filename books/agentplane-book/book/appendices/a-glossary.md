# Appendix A. A Working Vocabulary

**Adapter.** A boundary that translates the platform's stable contract into a
particular upstream release. It should expose capabilities and limitations, not
silently imitate missing functionality.

**Admission.** A decision made before a Kubernetes object is accepted. Admission
is one control; runtime and network enforcement remain separate.

**Approval.** A bounded authorization decision for one identity, action, input and
policy revision. Consuming it is not proof of an exactly-once external effect.

**Audit checkpoint.** A trusted record of a chain head and sequence that makes
later alteration detectable within the checkpoint's trust assumptions.

**BYOC.** Bring your own cloud or cluster. Compute can remain customer-owned even
when an enabled relay exposes output to the SaaS. Specify the actual data path.

**Capability.** A reported and verified implementation property. Discovery alone
is not an entitlement, authorization decision or security guarantee.

**Control plane.** The system managing ownership, desired state and policy.

**Data plane / execution plane.** The environment that runs workloads and carries
customer data. Its boundary is defined by actual processing, not a label.

**Fencing.** Rejection of stale authority by the resource or effect recipient.
A leader-election lease without recipient-side checks is not complete fencing.

**Idempotency.** Repeating a request under its defined identity does not introduce
an additional intended effect. The identity must include scope and payload rules.

**Inbox.** Durable records of consumed messages or command attempts used to detect
replay and resume work. Retention must match the possible replay horizon.

**Lease.** A time-bounded claim or credential. Expiry has an effect only where it
is checked and enforced.

**MCP.** Model Context Protocol. Tool discovery, authorization and execution are
distinct concerns; server-provided metadata is untrusted input.

**Observed state.** The latest verified state and its observation time. It may be
stale while the desired state is newer.

**Outbox.** Events written in the same database transaction as business intent,
then published asynchronously.

**RLS.** Row-level security. Database policies can constrain ordinary roles, but
role privileges and application-controlled context remain part of the model.

**RuntimeClass.** Kubernetes selection of a configured runtime handler. A name
alone does not install or prove a particular isolation implementation.

**Snapshot.** A storage point-in-time artifact under the provider's consistency
contract. It is not automatically a memory, process or application checkpoint.

**Unknown outcome.** A truthful execution state when the system cannot establish
whether an external effect completed. It should not become a silent retry.

**Warm pool.** Preallocated capacity intended to reduce allocation delay. Its
isolation, reset procedure and idle cost need explicit handling.
