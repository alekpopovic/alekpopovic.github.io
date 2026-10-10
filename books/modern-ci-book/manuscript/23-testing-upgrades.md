# 23. Test failures and upgrade through compatible states


## Test the boundary that makes the claim

Unit tests should cover graph validity, state transitions, signature checks, approval identity, and size limits. Contract tests should exercise actual serialized requests and version combinations. Integration tests should use PostgreSQL, object storage, and the selected container runtime. End-to-end tests should follow a real repository through execution and controlled deployment.

Each layer answers a different question. The companion laboratory demonstrates a subset of unit-level semantics. Its race test does not validate PostgreSQL, and its approval helper does not establish a secure user interface. Keep the verification report explicit about those limits.

For stateful behavior, generate sequences of operations and assert invariants after every step: at most one current claim, monotonic fences, immutable terminal attempt results, no unauthorized credential redemption, no unlocked uncertain target, and no artifact reference to unfinalized bytes.

## Put faults at the commit boundary

The most revealing failures happen just before and just after a state transition becomes durable. Drop the reply after a successful database commit. Kill the runner after starting a container but before writing its journal. Fail object metadata insertion after bytes were uploaded. Interrupt a deployment after the target applied the change but before the runner received confirmation.

These experiments should yield supported recovery states, not unexplained panics or duplicate side effects. Use disposable fixtures and registered test targets. Do not turn a failure test into an unsupervised production deployment.

Security tests need negative cases: cross-project identifiers, expired capabilities, forged runner identity, hostile archive paths, excessive matrix size, malicious report text, disallowed outbound destinations, and credential material in diagnostics. A successful authorized path does not imply that the denied path is correctly enforced.

## Upgrade producers before removing old contracts

An additive protocol change can allow old and new runners to coexist temporarily. A schema expansion can let old and new server versions operate during a rollout. Plan these states explicitly and test them using built binaries, not only matching source from one workspace.

A migration should have a bounded operation strategy for large tables. Avoid locking a busy queue table for an uncontrolled duration during normal dispatch. Backfill separately when needed, track progress, and define an abort or resume path.

After the new representation is fully in use and the downgrade window is closed deliberately, a later release can remove the old field. Document that cutoff. A semantic change may be incompatible even when the field name and data type remain unchanged.

## Make evidence refer to exact inputs

Record application commits, contracts revision, schema version, built image digests, test configuration, tool versions, start time, exit status, and output location. A green check attached to a different source snapshot is not evidence for the release being published.

Do not overwrite failed-run evidence with the next successful run. Keep a concise history so maintainers can see what changed and which failure was resolved. An operator must be able to distinguish “test passed,” “test skipped,” “not run,” and “blocked by missing infrastructure.”

The book's implementation ledger uses the same principle for work items: evidence is required before marking a task complete. It does not claim to execute or verify the entire product automatically.

## Exercise

A compatibility test compiles the newest server and newest runner against the same local contracts checkout. The release plan allows a six-month-old runner to remain connected. What test is missing?

## Worked answer

Run the new server against the actual supported older runner binary and exercise every relevant message and recovery flow. Also test rejection outside the supported range. Building both newest components from one checkout only proves a same-source combination, not the rolling-upgrade promise.

## Completion evidence

Maintain an executable failure matrix and a supported-version matrix. Release gates fail when required tests are missing, not only when an executed test reports an error.
