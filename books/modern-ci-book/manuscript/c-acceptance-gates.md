# Appendix C. Acceptance gates and failure experiments

## Gate 1: source and build independence

From a clean environment, retrieve the workspace and all pinned child commits using the access level promised to readers. Build each application independently. For Go consumers, disable local workspace resolution. For the web, install from its own lockfile and verify its generated client receipt. Build each container from its declared context. Fail the gate if sibling source or unpublished dependencies are required without a documented verification path.

Evidence should identify dependency versions, commits, generator versions, and the clean-environment procedure. A successful build in the maintainer's long-lived checkout is insufficient.

## Gate 2: identity and policy

Create two organizations, two projects per organization, and principals with deliberately different roles. Attempt cross-scope reads, mutations, log subscriptions, signed downloads, secret redemption, and runner-pool selection. Revoke access while a session and a pending run exist. Verify that client-side visibility is never the only denial mechanism.

Exercise runner enrollment twice with the same one-use credential. Rotate and revoke the resulting identity. Verify that browser, CLI, and runner credential classes cannot be substituted for one another. Check that audit events contain useful identities without plaintext secrets.

## Gate 3: compilation and immutable intent

Submit missing dependencies, cycles, duplicate identifiers, oversized configurations, unknown keys, wrong parameter types, and excessive matrices. Verify that no partial runnable graph is committed. Compile the same accepted input repeatedly and compare its normalized identity. Change a branch or toolchain alias after compilation and confirm that the existing run keeps its frozen inputs.

Change a permission after compilation and verify that dispatch can become more restrictive. The snapshot must preserve intent without preserving revoked authority indefinitely.

## Gate 4: queue concurrency and ownership

Run multiple real schedulers against PostgreSQL. Compete for one job, then many jobs with shared capacity limits. Inject deadlocks, transaction aborts, statement timeouts, and connection loss after commit. Verify current-claim uniqueness and atomic capacity reservation.

Expire a lease without stopping its worker. Ensure the job becomes uncertain rather than automatically safe to repeat. Deliver an old completion after an authorized retry and verify that it cannot replace the new attempt. Identical terminal reports should remain idempotent; conflicting reports should remain visible as conflicts.

## Gate 5: executor and storage boundaries

Use the actual selected container runtime on a dedicated test host. Test resource limits, controlled mounts, network policy, image policy, timeout escalation, process exit observation, and cleanup ownership. Restart the runner during execution and reconcile its journal against runtime objects.

Interrupt log and artifact uploads after bytes arrive but before metadata commits. Retry identical segments, submit conflicts, exceed quotas, and use expired upload capabilities. Test unsafe archive paths and expansion limits. Confirm that unrelated projects and attempts cannot finalize or read the objects.

## Gate 6: source and credential security

Send correctly and incorrectly signed webhooks, replay delivery IDs across two API instances, and reuse an idempotency key with different content. Verify that acknowledgements follow durable receipt creation. Test restricted contribution builds with no production credentials and no trusted-cache write path.

For workload federation, validate the actual provider configuration in a dedicated test environment. Test wrong audience, subject, issuer, expiry, and signing key. A local mock is not sufficient evidence for this gate. Record the provider-side policies and the resulting effective permissions without publishing credentials.

## Gate 7: deployment uncertainty

Use a disposable target and a uniquely identified release. Change the artifact or configuration after approval and verify rejection. Compete for the same target from two runs. Disconnect before mutation, during mutation, and after the target acts but before acknowledgement. Verify that uncertain state keeps the target reservation.

Reconcile from a trustworthy target observation, then perform the documented next action. Test rollback compatibility and the point beyond which data changes cannot be reversed by changing application images. Preserve the complete operation history.

## Gate 8: interface and operations

Test the browser with duplicated, missing, and out-of-order events; revoked access; large logs; malicious display text; and keyboard navigation. Verify CLI stdout/stderr behavior, exit statuses, context selection, and stale previews.

Restore a real backup with object data and required keys into an isolated environment. Keep dispatch paused, reconcile leases and targets, and document the controlled resume. Exercise the supported binary-version matrix during schema expansion and contraction. Measure load using a stated workload and record recovery after the load ends.

## Release decision

The release record should name which gates ran, which evidence belongs to the exact source snapshot, what was skipped or blocked, and which limitations remain. Do not translate “not observed to fail” into “verified.” Public release notes must match the evidence, including the supported trust model and deployment scope.

These gates are requirements for a future full platform. The book's preparation evidence covers its own publication build and isolated Go laboratory, not a completed product deployment.
