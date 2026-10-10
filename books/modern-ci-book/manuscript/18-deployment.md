# 18. Deploy an approved immutable release


## An environment is a policy-bearing resource

A production environment is not just a string in YAML. It has an owner, authorized projects, approved target adapters, allowed credential references, concurrency rules, approval policy, and an audit history. The server enforces these rules independently of the pipeline author's requested configuration.

A deployment request binds a release artifact to an environment and target configuration. The artifact must be finalized and immutable. Record a configuration digest alongside the image digest, because changing environment settings can materially change the deployment even when the image stays the same.

Do not allow a job author to remove an obligatory production approval by deleting a YAML field. The compiled plan can request deployment, but the environment policy decides whether dispatch is allowed.

## Approve a subject, not a label

An approval should identify project, environment, artifact digest, configuration digest, and policy revision. It should include approver identity, time, expiry, and any required separation-of-duties rule. “Approve release latest” is not a stable authorization.

The included approval helper compares an exact subject and refuses expired or revoked approvals. It does not implement membership or approver-role checks; the product must evaluate those at the service boundary and recheck relevant revocations before dispatch.

If the artifact, target configuration, or approval policy changes, the old approval no longer matches. Ask for a new decision rather than silently attaching the old human action to a different operation. The interface should make the changed field visible so reapproval is meaningful.

## Serialize access to the target

Acquire an environment or target reservation before mutation. Keep its identity in the deployment record and executor plan. A second deployment to the same target must wait unless the adapter's concurrency model explicitly supports overlap.

An SSH adapter should accept a registered target with a pinned host identity, restricted account, known commands or release procedure, and a specific artifact. Do not disable host-key verification to make onboarding easy. A user-supplied host and shell fragment create a much broader product than a controlled deployment adapter.

Stage the release, verify expected inputs, perform the documented transition, and probe health through a target-specific contract. Record what was observed, not simply that the SSH process exited with zero. Some services launch asynchronous rollout work and return before the new version is healthy.

## Observe the deployed identity

A deployment can be requested, approved, dispatched, applying, verifying, healthy, failed, or uncertain. Keep these states separate from the upstream build's status. A successful image build does not mean that the application is running in production.

The target observation should identify the actual deployed digest or release revision where the platform can inspect it. Store health-check parameters and results. A generic `200 OK` from an unrelated route is weak evidence if it cannot establish which version answered.

Notifications come after committed state transitions through the outbox. Include environment, release identity, and a link to the deployment record. Avoid messages whose wording suggests that receiving a notification is itself proof of a healthy rollout.

## Exercise

An approver authorizes digest D1. A developer changes the deployment configuration and reuses the approval because the image digest is unchanged. Is that valid under this design?

## Worked answer

No. The configuration digest is part of the subject. Changing a database endpoint, feature flag, volume, or runtime command can change the operation substantially. Compile a new subject and obtain the required approval. The old decision remains valid only for the exact operation it named.

## Completion evidence

Test artifact substitution, configuration changes, revoked approver access, policy changes, concurrent deployment requests, host-key mismatch, asynchronous rollout failure, and verification that reports the wrong deployed identity.
