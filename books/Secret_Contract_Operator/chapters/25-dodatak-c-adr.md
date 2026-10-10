# Appendix C. Architecture Decision Register

## C.1 ADR-001: Local References

**Decision:** Secret, ESO, and workload references remain in the contract's namespace. **Reason:** simpler authorization and a limited incident scope. **Consequence:** cross-namespace consumption is unsupported; a namespace alone still cannot isolate untrusted users within it. **Acceptance evidence:** a negative test using the same name in another namespace.

## C.2 ADR-002: Trusted Contract Authors

**Decision:** the first profile permits authorship only by subjects authorized to learn properties of the corresponding secret. **Reason:** a validation result can be an oracle. **Consequence:** the MVP is not a general self-service system for untrusted tenants. **Later option:** a protected grant model constraining rules and targets.

## C.3 ADR-003: Read-only Is More Than a Runtime Flag

**Decision:** the default chart has no workload write permissions and never has Secret write permissions. **Reason:** a programming error should not exploit permissions the default feature does not need. **Consequence:** mutation uses a separate installation profile. **Evidence:** automated rendered-RBAC inspection and negative ServiceAccount tests.

## C.4 ADR-004: Results Without Contents

**Decision:** the validator returns only controlled codes, key identifiers, and aggregates. **Reason:** fewer direct leakage channels. **Consequence:** parser errors are mapped rather than forwarded. **Boundary:** results still convey information, so they do not replace authorization. **Evidence:** sentinel-output tests and review of every formatter.

## C.5 ADR-005: Metadata Tokens Instead of Hashes

**Decision:** the restart signal uses the Secret UID/RV and contract UID. **Reason:** no public fingerprint of a low-entropy value. **Consequence:** a metadata-only update may trigger a restart, and initial enablement changes the template. **Boundary:** this proves neither rotation nor the identity of a value inside a process.

## C.6 ADR-006: Status Without a Feedback Loop

**Decision:** semantically identical status is not written. **Reason:** lower API load and more stable behavior. **Consequence:** check time has a defined update event and is not a heartbeat for every reconcile. **Evidence:** a test counting status writes after stabilization.

## C.7 ADR-007: Ready Is Not Admission

**Decision:** the main operator maintains status; a pipeline or separate layer decides whether deployment may continue. **Reason:** simpler MVP availability. **Consequence:** an explicit generation-aware gate and a documented race between checking and use. **Later:** an optional admission-component design with a recovery plan.

## C.8 ADR-008: A Constrained ESO Adapter

**Decision:** use a fixed ExternalSecret kind and version allowlist, without direct cloud access. **Reason:** a smaller privileged scope and clear responsibility. **Consequence:** the adapter also checks the target name and does not promise support for every future schema shape. **Evidence:** absent-CRD and target-mismatch tests.

## C.9 ADR-009: Git-owned Environment References

**Decision:** the basic mode expects environment references from Git/Helm configuration. **Reason:** avoiding two owners of the same fields. **Consequence:** managed injection is optional and requires precise ownership and approval. **Evidence:** the default profile never patches workloads.

## C.10 ADR-010: A Time Signal Does Not Prove Rotation

**Decision:** maxAge calculates the declared age of trusted metadata, not proven credential age. **Reason:** Kubernetes and ESO metadata do not automatically provide business rotation time. **Consequence:** document the authorized timestamp writer and use timer-driven checks.

## C.11 ADR-011: No Takeover of Others' Ownership

**Decision:** no owner-reference takeover or cleanup finalizer for a read-only contract. **Reason:** deleting a contract must not delete an application or secret. **Consequence:** simpler uninstall; later mutation references may remain according to an explicit policy. **Evidence:** deletion and uninstall E2E tests.

## C.12 ADR-012: A Tested Support Matrix

**Decision:** advertise supported versions only from a matrix that actually ran. **Reason:** scaffold compatibility and production behavior are different. **Consequence:** a release may support fewer versions than tool documentation theoretically permits. **Evidence:** a versioned test report and reproducible CI.
