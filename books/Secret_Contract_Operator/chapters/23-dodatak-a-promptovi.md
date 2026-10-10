# Appendix A. Thirty Detailed Codex Prompts

This appendix is a development plan. Creating the book did not execute these prompts. Copy the shared context below into `AGENTS.md` or load it with each task; all 30 files in the companion directory contain their own context.

## A.0 Shared Context

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.
```

## A.1 Inventory, Working Rules, and AGENTS.md

**ID 001 · Phase A · Medium · Previous task: none.**

```text
Inspect the repository before changing files. Preserve an existing module path and any unrelated work. Create AGENTS.md, docs/specification.md and docs/security.md from the canonical decisions in this book. Use SecretContract in secrets.codepop.tech/v1alpha1 as the proposed API, and clearly mark any existing different group as a migration concern.
Define validation-only as both runtime behavior and RBAC. Document the validation-oracle threat: contract authors must already be authorized to learn properties of the referenced Secret. Forbid Secret values, substrings, raw parser errors and content hashes in all outputs. Distinguish application health from contract readiness.
Create tracking records for every numbered task with pending, in_progress, blocked, implemented, verified and accepted states. Preserve the real current status; do not mark planned work complete. Record available tools and missing prerequisites without printing environment variables or kubeconfig contents.

Acceptance: repository inventory and security assumptions exist; no operator implementation or cluster mutation is performed; tracking starts truthfully.
```

## A.2 Kubebuilder Scaffold and Tool Pinning

**ID 002 · Phase A · Medium · Previous task: 001.**

```text
Initialize a Go Kubebuilder project only if no scaffold exists. Proposed module is github.com/CodepopTech/secret-contract-operator, domain codepop.tech, group secrets, version v1alpha1, kind SecretContract. When a scaffold already exists, inspect and extend it instead of regenerating over user code.
Select a mutually compatible Kubebuilder, Go, controller-runtime and Kubernetes library set from the scaffold. Record exact versions in the repository. Do not independently upgrade every dependency to latest. Preserve PROJECT, generated Makefile conventions, CRD generation and the manager entrypoint.
Build the unmodified scaffold, run its relevant tests, make generate and make manifests. Explain which tests require envtest binaries and whether those were actually available. Add a reproducible local setup document and ignore local binaries and test credentials.

Acceptance: a clean scaffold builds, generated API/controller files exist, no business logic is introduced, and actual command results are recorded.
```

## A.3 Threat Model and Architecture Decisions

**ID 003 · Phase A · High · Previous task: 002.**

```text
Write architecture decision records before expanding the controller. Cover namespace-local references, trusted contract authors, Secret read scope, cache exposure, static safe diagnostics, no content hashes, no default mutation, no ownership of referenced resources and no finalizer in the read-only MVP.
Design authorization boundaries explicitly. A user-controlled allow flag or annotation inside SecretContract is not an authorization mechanism. For the first deployment profile, contract writers must be trusted administrators with rights to the target Secret. Document a future protected grant model without claiming that it is already implemented.
Describe a confused-deputy risk for injection into a workload controlled by another actor. Define the two independent approvals needed before mutation. Document the remaining time-of-check/time-of-use race and that Ready alone never blocks Kubernetes deployment.

Acceptance: ADRs identify actors, new privileges and failure cases; security claims have matching planned tests; no unsupported multi-tenant safety promise remains.
```

## A.4 Canonical API Types

**ID 004 · Phase A · High · Previous task: 003.**

```text
Implement the book canonical API, not the earlier inconsistent sketch. Define local secretRef, map-like requiredKeys with unique names, optional envName, pointer required/nonEmpty defaults, byte-based minLength/maxLength, pattern and None/JSON/URI/PEM formats.
Add the bounded ExternalSecret reference, workloadRefs with explicit containers, includeInitContainers and Any/EnvFrom/EnvVars consumption, injection.mode default Disabled, and rotation with restartOnChange false, maxAge and rotatedAtAnnotation. Policies are requireExternalSecretReady, requireWorkloadReference and requireRotationPolicy. Missing Secret must never satisfy Ready.
Status contains observedGeneration, observedSecret name/UID/resourceVersion, safe violations, counts, workload results, conditions and lastCheckedTime. Conditions use metav1.Condition and list-map semantics by type. If optional mutation fields are accepted before implementation, report FeatureNotEnabled rather than silently pretending to act. Add printer columns backed by real scalar status fields.

Acceptance: generate DeepCopy and CRD manifests; examples match the types; status subresource exists; no output type has a Secret value or content fingerprint field.
```

## A.5 CRD Schema and Specification Validation

**ID 005 · Phase A · High · Previous task: 004.**

```text
Add structural schema constraints and defaults. Bound requiredKeys to 1..256, pattern size and workload list sizes. Reject duplicate key names, negative lengths, minLength greater than maxLength, unsupported kinds and malformed local references. Separate valid Secret key names from the project conservative environment-name policy.
Require the corresponding reference when an enforcement policy is enabled. Require positive supported duration syntax such as 720h rather than assuming 30d parses. Reject invalid annotation keys. Use native schema/CEL where suitable; do not add a mandatory webhook just for defaults already supported by the schema.
Implement a defensive Go spec validator for cases that cannot safely be enforced in the chosen schema, including regex compilation. A malformed existing object must become a safe InvalidSpec result, not panic. Do not copy raw pattern text or parser errors into public diagnostics.

Acceptance: schema and pure spec tests cover all boundary cases; default false is distinguishable from omitted default true; generated manifests are clean.
```

## A.6 Pure Data Validator

**ID 006 · Phase A · High · Previous task: 005.**

```text
Build internal/contract as a pure Go package with no Kubernetes client, logger, clock or network access. Adapt the standalone contractlab example rather than importing its educational module path. The result contains only key identifiers, bounded reason codes and sorted missing-key lists.
Implement required/optional handling, nonEmpty without whitespace normalization, byte length, Go regexp semantics, syntactic JSON, absolute URI without network lookup and strict PEM block validation. Distinguish malformed spec from invalid data. Limit per-value and total input budgets without truncating values before evaluation.
Do not expose parser errors, values, value lengths, snippets or hashes. Do not claim that length proves entropy or that parsing proves credential validity. Ensure map iteration cannot alter public result ordering.

Acceptance: table-driven tests cover positive, negative, optional and budget cases; the package can be tested independently of a cluster; output serialization is safe.
```

## A.7 Fuzzing and Leakage Tests

**ID 007 · Phase A · High · Previous task: 006.**

```text
Expand validator tests using synthetic inputs only. Include invalid UTF-8, Unicode byte boundaries, malformed URI escapes, PEM bundles, junk before and after PEM blocks, malformed first PEM blocks followed by valid blocks, regex errors, empty JSON and scalar JSON.
Add deterministic fuzz seeds and a bounded fuzz target checking no panic, deterministic results and safe result shape. Add sentinel tests for raw, base64, hex and deterministic digest representations in serialized outputs. Ensure test failures do not dump the full input.
State explicitly what sentinel testing proves and what it does not prove: it is a regression test for direct channels, not a proof against a validation oracle. Add an authorized-writer policy test separately; do not let a logging test substitute for access control.

Acceptance: unit, race and a recorded bounded fuzz run complete where tools support them; any unrun command is listed as not run.
```

## A.8 Deterministic Status Builder

**ID 008 · Phase A · High · Previous task: 007.**

```text
Create a status builder independent of Kubernetes I/O. Encode the exact Ready formula from the book. Unconfigured optional checks are True/NotConfigured; configured checks can be True, False or Unknown. Enforced missing configuration is invalid spec.
Set observedGeneration on every condition, preserve meaningful lastTransitionTime and sort violations/workload results. Clear obsolete findings after recovery. Bound messages and result lists. Never copy upstream ExternalSecret messages or raw errors.
Do not mutate lastCheckedTime on every no-op reconcile. Define an observation key using contract generation, authorized dependency metadata and scheduled evaluation triggers. A status update is necessary only for a relevant new observation or semantic transition. Treat authorization revocation as a new negative result and remove details no longer authorized for publication.

Acceptance: repeated identical observations yield an equal status; transitions, stale generation, error recovery and authorization revocation have direct unit tests.
```

## A.9 Basic Read-only Reconciler

**ID 009 · Phase A · High · Previous task: 008.**

```text
Implement the first controller using the pure spec/data validators and status builder. Read the contract, authorize the reference before reading Secret data, fetch the same-namespace Secret and record UID/resourceVersion for the actual observation.
Handle deleted contracts, missing Secret, Forbidden, API timeout, invalid spec, invalid data and success as distinct cases. Publish only safe status and bounded events. Use optimistic status patching and recompute on conflict; do not reuse an old desired status against a new generation.
Do not mutate Secrets or workloads. Do not add finalizers or ownerReferences to external objects. Configure event-driven recovery and reasonable transient-error backoff. Ensure an old positive status is not reported as a newly successful check after a failed read.

Acceptance: envtest covers missing/valid/invalid/deleted Secret and observedGeneration; two no-op reconciles cause no further status writes.
```

## A.10 Indexes, Watches, and Namespace Isolation

**ID 010 · Phase A · High · Previous task: 009.**

```text
Index SecretContract by secretRef.name. Watch non-owned Secret resources and enqueue only dependent contracts in the same namespace. Add workload/dependency index helpers without granting ownership of those resources.
Do not apply GenerationChangedPredicate indiscriminately to Secret updates. Filter primary status-only updates while preserving authorization metadata changes that must trigger reconciliation. Handle delete and recreate using identity metadata, not name alone.
Write event-driven envtest cases without manually invoking Reconcile to cause the expected update. Include two namespaces with identically named Secrets, multiple contracts sharing one Secret, a changed contract reference and index/list failure behavior. Avoid cluster-wide fallback scans and avoid logging event objects.

Acceptance: create/update/delete events reach only correct dependents; no status feedback loop or cross-namespace wakeup bug remains.
```

## A.11 RBAC Profile and Cache Boundaries

**ID 011 · Phase A · High · Previous task: 010.**

```text
Implement namespace-scoped installation and explicit trusted-writer documentation. Review all generated RBAC. The default role reads Secret data in the declared scope, updates only contract status and writes events. It must not write Secrets or workloads.
Document exactly whether the standard cache holds full Secret objects. Do not describe a label filter as an authorization boundary. If implementing a metadata-watch profile, use direct authorized reads and test that the cached client cannot silently start a full Secret informer for that path.
Add negative access tests using the operator ServiceAccount, not the administrator test client. Separate leader-election Lease permissions in the manager namespace. Clearly reject or document unsupported arbitrary Secret selection with resourceNames-limited informer lists.

Acceptance: negative tests prove cross-namespace and write restrictions; chart/RBAC output and runtime watch scope agree; cache exposure is truthful.
```

## A.12 Optional ESO Adapter

**ID 012 · Phase B · High · Previous task: 011.**

```text
Add bounded unstructured ExternalSecret integration without importing ESO Go APIs. Limit API versions to a documented install-level allowlist and keep kind fixed to ExternalSecret. Do not accept an arbitrary user-controlled GVK.
Support clusters where ESO is absent. Implement discovery plus a documented polling/watch strategy that still reconciles a referenced ESO object after updates. Check the effective target Secret name as well as Ready. A healthy ExternalSecret targeting another Secret must fail with ExternalSecretTargetMismatch.
Sanitize all external conditions to local reason codes. Do not infer credential rotation age from refreshTime. Test missing CRD, missing object, absent/malformed conditions, false/true Ready and default/explicit target behavior. Document whether installing ESO after startup requires rediscovery or restart.

Acceptance: ordinary contracts work without ESO; required ESO failures block Ready; real ESO compatibility is not claimed until its e2e test is run.
```

## A.13 Workload Reference Validator

**ID 013 · Phase B · High · Previous task: 012.**

```text
Implement read-only extraction of PodTemplateSpec from supported apps/v1 workloads. Enforce explicit named consumers, all-consumer semantics and optional init-container selection. Missing selected containers fail validation.
Validate EnvFrom, EnvVars and Any according to the canonical API. Respect envName mapping and required secretKeyRef optional=false behavior. Detect explicit env overrides and ambiguous later envFrom sources conservatively. Do not read additional unapproved Secret values to resolve precedence.
Never print conflicting inline env values. Return safe paths and reason codes. Add tests for sidecars, init containers, mismatched key/name, prefix, optional references, duplicate names and conflicts. Explain the first-deploy deadlock when requiring an absent workload before deployment.

Acceptance: all supported consumers are evaluated correctly; no workload mutation occurs; ambiguous precedence never yields a misleading positive result.
```

## A.14 Time-based Rotation Policy

**ID 014 · Phase B · High · Previous task: 013.**

```text
Implement maxAge validation without automatic restarts. Parse the configured annotation as RFC3339 using an injected clock. Report missing/invalid/future timestamps and expiration with stable reason codes.
Document that the annotation is a claim by its authorized writer, not proof of credential rotation. Do not use Secret creationTimestamp, resourceVersion or ESO refreshTime as a substitute. Use positive supported duration syntax and a documented clock-skew tolerance.
Schedule reconciliation at the next relevant deadline, so expiration is detected without any object update. Avoid a zero-delay loop after expiry. Apply requireRotationPolicy exactly as documented; advisory failures may leave Ready true while the dedicated condition is false.

Acceptance: fake-clock tests cover boundary times, skew, invalid dates and restart before expiry; the next requeue deadline is deterministic and bounded.
```

## A.15 Metrics and Safe Events

**ID 015 · Phase B · Medium · Previous task: 014.**

```text
Add the documented metric set and safe events. Use bounded result enums, duration units and explicit Unknown/NotConfigured handling. Per-contract name/namespace labels are an opt-in cardinality decision; do not add key names, patterns, values, UID or resourceVersion labels.
Emit transition-based events and avoid repeated warnings for identical state. Clear per-object gauge series when contracts disappear. Ensure multiple manager replicas do not create misleading dashboards for leader versus standby data.
Secure or scope the metrics endpoint and make ServiceMonitor optional. Add metrics/event serialization tests using synthetic sentinels. Document health of the manager separately from contract validity and application availability.

Acceptance: registration is idempotent, deleted-object metrics are removed, event volume is bounded, and a safe metrics reference document exists.
```

## A.16 Envtest Integration Matrix

**ID 016 · Phase B · High · Previous task: 015.**

```text
Build a reliable envtest suite around a real manager and watches. Use unique namespaces and eventual assertions rather than arbitrary sleeps. Install the actual generated CRD schema and any minimal test-only optional CRDs explicitly.
Cover missing-to-valid-to-invalid Secret transitions, deletion/recreation UID changes, generation-aware status, authorization revocation, namespace isolation, no-op writes, concurrency conflicts and timer-driven expiration. Assert status/event/log outputs are free of sentinels.
Do not wait for Pods to be created by Deployment controllers in envtest because those controllers are not part of envtest. Reserve actual rollout assertions for kind. Record downloaded envtest binary versions and make the CI setup reproducible.

Acceptance: tests pass repeatedly from a clean setup without real cloud credentials; flakes, unrun cases and limitations are documented honestly.
```

## A.17 Helm Chart for the Read-only MVP

**ID 017 · Phase B · Medium · Previous task: 016.**

```text
Create charts/secret-contract-operator for the implemented MVP. Include image digest/tag selection, manager deployment, ServiceAccount, namespace-scoped reader roles/bindings, scoped Lease permissions, resources and hardened security contexts.
Default workload mutation permissions must be absent. Configure metrics and optional ServiceMonitor without requiring Prometheus Operator. Do not require cert-manager when no webhook is deployed. Document exact Secret cache and watch scope.
Choose an explicit CRD lifecycle strategy with a separate generated CRD artifact or carefully documented crds directory usage. Do not claim helm upgrade automatically migrates CRDs. Add render tests that reject wildcard and forbidden write permissions.

Acceptance: helm lint and template checks pass; CRD and controller installation order is documented; validation-only RBAC is mechanically verified.
```

## A.18 GitHub Actions CI

**ID 018 · Phase B · Medium · Previous task: 017.**

```text
Add CI for pull requests and main changes with least privilege. Run format, vet, unit, race, envtest, generation checks, chart validation and container build. Use exact supported tool versions and pin third-party Actions to verified immutable commits where appropriate.
Do not give fork pull requests write tokens or cloud credentials. Avoid unsafe pull_request_target execution of untrusted head code. Treat branch names, titles and other PR metadata as untrusted input, not shell code.
Fail when generated files differ after make generate/manifests. Keep e2e separated or clearly configured. Record actual execution and make test output safe for public CI artifacts. Do not publish an image from ordinary PR checks.

Acceptance: a clean checkout runs the workflow locally where possible; valid YAML and job permissions are reviewed; no fake Action hashes or secret credentials are committed.
```

## A.19 Kind E2E for the MVP

**ID 019 · Phase B · High · Previous task: 018.**

```text
Create an isolated kind e2e workflow using a pinned node image and local operator image. Never silently reuse the current user cluster. Require an explicit context and clean up only resources created by the test.
Install CRDs and the actual chart, wait for manager readiness, create synthetic examples, verify contract transitions and confirm validation-only RBAC with the actual ServiceAccount. Restart the manager and verify convergence. Test uninstall without deleting application Secret/workload resources.
Where ESO integration is advertised, add a scenario with an actual supported ESO release and a safe fake/test provider. Do not require real AWS/Vault credentials. Capture redacted status and metadata only; do not archive raw Secret objects.

Acceptance: make e2e has a documented reproducible flow and safe cleanup; results clearly distinguish executed from planned integration scenarios.
```

## A.20 Documentation, Examples, and CI Gate

**ID 020 · Phase B · Medium · Previous task: 019.**

```text
Write README, API reference, security model, troubleshooting, metrics and examples matching the implemented schema. Include a missing-key example, a valid preflight example, ESO target validation and workload consumption validation.
Provide a generation-aware gate script that checks contract UID, current generation and Ready.observedGeneration without reading Secret values. Explain the initial-workload deadlock and use two deployment phases. Explicitly state the remaining race and that Ready is not automatic admission enforcement.
Use only synthetic credentials and verified image references or clearly labeled placeholders. Mark future mutation, webhook and rollout features as future. Ensure every quickstart command has its prerequisite and expected safe output.

Acceptance: examples validate against the generated CRD in the test environment; documentation does not advertise unimplemented or untested guarantees.
```

## A.21 MVP Security Audit

**ID 021 · Phase B · High · Previous task: 020.**

```text
Audit source, tests, chart and docs for leaks and privilege mistakes. Trace every use of Secret.Data, string conversion, error wrapping, structured logger, event, metric, annotation and status field. Remove raw object formatting and unsafe upstream messages.
Review the validation-oracle model and ensure contract-writer permissions match declared trust assumptions. Check authorization before data reads. Verify the default chart cannot mutate workloads or Secrets. Review pprof/debug exposure, cache contents and public CI artifacts.
Add regression tests for confirmed issues. Produce SECURITY.md and a concise audit report with findings, fixes and residual risks. This is an internal engineering audit, not a claim of independent certification.

Acceptance: no critical known leak or authorization bypass remains; negative tests pass; residual risks and unperformed external reviews are explicit.
```

## A.22 Preparing the First MVP Release

**ID 022 · Phase B · High · Previous task: 021.**

```text
Prepare, but do not publish without explicit authorization, the first MVP release. Freeze the v1alpha1 schema, regenerate artifacts, reconcile docs/examples and execute the agreed test matrix.
Prepare release notes, installation manifests, chart package, checksums, image build instructions, SBOM/provenance generation and signing verification guidance. Use real generated digests only; no fabricated release URLs or registry tags.
Document supported versions solely from tested evidence. Separate application version, chart version and CRD API version. List known limitations including no hard deployment gate, trusted contract authors and no default mutation. Record release acceptance status in tracking.

Acceptance: a reviewer can reproduce the local release candidate; unrun checks block verified/accepted status instead of being silently waived.
```

## A.23 Protected Mutation Approval

**ID 023 · Phase C · High · Previous task: 022.**

```text
Design and implement the authorization boundary for optional mutation after the read-only MVP is accepted. Require install-level enablement, separate write RBAC, an explicit contract request and a protected workload/Secret approval tied to contract UID.
Do not treat a freely editable annotation or contract boolean as proof of authorization. Choose and document an enforceable administrative protection or grant mechanism. If the necessary protection cannot be provided, leave mutation disabled and mark the task blocked.
Allow at most one mutation-owning contract per workload in the first version. Read-only contracts may coexist. Recheck approval on every action and immediately stop new actions when it is revoked. Do not inherit approval on same-name object recreation.

Acceptance: unauthorized, revoked, conflicting and recreated-contract cases cannot mutate the target; default installation privileges remain unchanged.
```

## A.24 Minimal EnvFrom and EnvVars Injection

**ID 024 · Phase C · High · Previous task: 023.**

```text
Implement the canonical opt-in injection modes for explicitly selected supported consumers. Add references only; never materialize Secret values into env.value. Do not mutate init containers unless the API explicitly supports and tests that path.
Plan changes before writing. EnvFrom adds a non-duplicated reference; EnvVars maps envName or key name and respects optional rules. Existing conflicting names are reported, not overwritten. Preserve unrelated env order, image, securityContext and all other fields.
Use concurrency-safe minimal patches and re-read/replan on conflict. Avoid force ownership takeover. Document partial success across multiple workload objects because Kubernetes does not provide a multi-object atomic patch. Clarify GitOps field ownership and deletion behavior.

Acceptance: disabled and unapproved cases make no changes; repeated reconcile is a no-op; concurrent user updates are preserved; conflict cases have safe status.
```

## A.25 Metadata Restart Token

**ID 025 · Phase C · High · Previous task: 024.**

```text
Implement optional restart signaling using only Secret UID/resourceVersion and contract UID. Use a valid bounded annotation key under the project prefix; never hash Secret content. The value must distinguish Secret deletion/recreation.
Require all mutation preconditions and valid content before changing PodTemplate. An invalid new Secret must not trigger a rollout. Document that metadata-only Secret changes may trigger restart and that first enablement causes an initial template change.
Do not delete Pods directly. Compare the current token before patching. Revalidate the relevant fresh observation before the action, while documenting that this cannot create an atomic Secret/workload transaction. Do not claim the annotation proves processes are using the new value.

Acceptance: tests cover initial enablement, same-version no-op, update, recreation, invalid data and absence of content fingerprints.
```

## A.26 Rollout Strategies and Storm Prevention

**ID 026 · Phase C · High · Previous task: 025.**

```text
Add explicit eligibility checks for supported rollout strategies. Handle paused Deployments, unsupported Recreate policy if not deliberately allowed, StatefulSet OnDelete/partition cases and DaemonSet OnDelete. Unsupported cases must not be reported as completed automatic restart.
Implement a documented debounce and minimum restart interval with persistent/reconstructible state where needed. Preserve the newest pending observation and revalidate it before patching. Test manager restart during the waiting window and changes arriving while rollout is progressing.
Do not claim that a PDB protects every controller-driven rolling update. Do not change the workload update strategy to make automation convenient. Separate action requested, template patched and rollout observed states.

Acceptance: fake-clock and concurrency tests prevent repeat storms and lost newest updates; unsupported strategies are explicit and do not delete Pods.
```

## A.27 E2E Matrix for Mutation Features

**ID 027 · Phase C · High · Previous task: 026.**

```text
Extend kind tests using the actual mutation profile and protected approvals. Verify supported Deployment rollout, unchanged behavior when disabled, revocation, env conflicts, same-name Secret recreation and invalid-rotation suppression.
Add supported StatefulSet/DaemonSet cases only when their implementation is complete. Include OnDelete and partition/paused negative cases. Observe Pod identities and workload rollout status without exec env or printing credentials.
Test simultaneous GitOps-like changes and the operator patch. Ensure restart storms stop when mutation is disabled. Confirm uninstall preserves application resources and documents retained references. Capture only sanitized metadata artifacts.

Acceptance: advertised mutation support is backed by actual e2e evidence; read-only installation remains least privilege; unexecuted scenarios are not labeled passing.
```

## A.28 Optional Webhook: ADR and Narrow Prototype

**ID 028 · Phase D · High · Previous task: 027.**

```text
Evaluate whether any remaining requirement truly needs an admission webhook. Prefer structural schema/CEL for local spec checks. Keep a hard workload gate as a separate optional component, not an implied effect of Ready.
Write an ADR covering scope, failure policy, TLS lifecycle, high availability, API call budget, dry-run, break-glass and dependency cycles. A webhook that only trusts stale Ready does not provide strong freshness. A live Secret read still does not make later Pod startup atomic.
Implement only a narrow prototype if these requirements are satisfied and explicitly approved in project configuration. Otherwise deliver the design and a blocked implementation record. Default installation must remain usable without cert-manager or admission infrastructure.

Acceptance: no broad cluster-wide blocking behavior appears by default; limitations and recovery procedure are tested for any implemented prototype.
```

## A.29 Compatibility and Upgrade Tests

**ID 029 · Phase D · High · Previous task: 028.**

```text
Build compatibility tests from actual prior release manifests and documented schema versions. Do not simulate a nonexistent historical release as evidence. Track served and storage API versions separately if a new CRD version is introduced.
Test install-old/upgrade-new, defaults, old object readability, safe status transitions and absence of unintended mutation. Document CRD migration and why Helm rollback alone cannot guarantee data-schema rollback.
Review all changed condition reasons, defaults, restart-token rules and authorization semantics as compatibility surfaces. Add migration notes for any earlier sketch field names only when corresponding real users or code exist.

Acceptance: upgrade evidence identifies exact tested versions; migration risks are explicit; no destructive CRD deletion is hidden in routine upgrade.
```

## A.30 Final Review and Release Candidate

**ID 030 · Phase D · High · Previous task: 029.**

```text
Perform a repository-wide release review. Recheck API coherence, generation-aware conditions, namespace authorization, cache exposure, value-free outputs, event cardinality, timer behavior, idempotent mutation and workload strategy support.
Run the available complete test matrix, generation checks, chart policy checks and container build. Record exact commands and distinguish failures, blocked prerequisites and not-run checks. Review every advertised feature against actual code and tests.
Produce a release readiness checklist, residual-risk report, installation/upgrade/uninstall procedure and prioritized follow-up issues. Prepare signed/reproducible artifacts only from an accepted commit. Do not publish externally or claim production certification without explicit user authorization and evidence.

Acceptance: reviewers can trace each public claim to code, tests and documentation; release acceptance remains blocked for unresolved critical issues.
```
