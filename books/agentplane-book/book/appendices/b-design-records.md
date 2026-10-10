# Appendix B. Decision Records and Interface Contracts

Use these templates to record choices in the implementation repository. They are
proposed AgentPlane contracts, not upstream API definitions.

## Architecture decision record

```text
Title: Customer-owned local policy envelope
Status: Proposed / Accepted / Superseded
Context: The SaaS can send commands over an outbound connection.
Decision: Local bounds cannot be widened by normal SaaS commands.
Alternatives: Full SaaS authority; completely disconnected operation.
Consequences: Some changes require customer-side administration.
Verification: Attempt an authenticated command outside local bounds.
Recovery: Explain how an administrator repairs an invalid envelope.
Owner: Assign in the real implementation repository.
```

## Asynchronous operation envelope

```json
{
  "operation_id": "op-example",
  "organization_id": "org-example",
  "project_id": "project-example",
  "resource_id": "session-example",
  "desired_state": "running",
  "observed_state": "provisioning",
  "observed_at": "2026-10-10T00:00:00Z",
  "status": "pending",
  "reason_code": "AWAITING_RUNTIME_READINESS"
}
```

These identifiers are illustrative strings. A real API must validate its chosen
identifier format, tenant scope and timestamps. Avoid exposing raw cluster error
objects or credential-bearing messages in `reason_code`.

## Dependency verification record

| Field | What to record |
|---|---|
| Component | Controller, router, runtime server or SDK |
| Exact artifact | Release, commit and image digest |
| API surface | CRD version and supported fields |
| Required capabilities | Execution, file operations, suspend, snapshots |
| Local changes | Configuration and patches, preferably none |
| Tests | Specific commands, cluster profile and results |
| Failure policy | Reject, degrade or disable unsupported features |
| Review date | Date the record was actually checked |

Keep rows independent. A controller and runtime server may have different release
cadences. Do not infer SDK compatibility from an unrelated repository tag.

## Command envelope invariants

A command identity binds organization, project, cluster, operation ID, payload
hash, protocol revision, expiry and connection epoch. Authenticating the stream
is necessary but does not replace checking those fields. Every effect-capable
recipient needs a defined replay and stale-authority behavior.

## Result vocabulary

Use results that distinguish accepted, in-progress, succeeded, failed,
unsupported, expired, rejected and unknown. Include a safe machine-readable reason
and a correlation identifier. Do not turn unsupported into succeeded merely
because a provider returned no error.

## Threat-to-test record

```text
Invariant: Tenant A cannot subscribe to tenant B's output stream.
Attempt: Use a valid A credential with B's stream ticket and session ID.
Expected: Rejection before subscribing to runtime output.
Evidence: API result, safe audit metadata and stream-access counter.
Variants: Expired ticket, changed project, revoked user, reconnect.
Limit: Does not prove runtime isolation or host security.
```
