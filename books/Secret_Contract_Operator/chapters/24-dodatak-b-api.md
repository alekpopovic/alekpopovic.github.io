# Appendix B. Concise API and Reason Reference

## B.1 Spec Fields

This is the book's normative design reference. Source Go types and the generated CRD schema should align with it. Fields planned for the mutation phase do not mean the feature is already available in the MVP.

| Path | Type / default | Rule |
|---|---|---|
| `secretRef.name` | Required string | Local Secret name |
| `requiredKeys` | List of 1–256 | Unique by `name` |
| `requiredKeys[].name` | String | Valid Secret key name |
| `requiredKeys[].envName` | Optional string | Explicit portable environment-variable name |
| `requiredKeys[].required` | Pointer bool / true | Absent required key is an error |
| `requiredKeys[].nonEmpty` | Pointer bool / true | Empty means zero bytes |
| `requiredKeys[].minLength` | Optional integer | Minimum decoded bytes |
| `requiredKeys[].maxLength` | Optional integer | Maximum decoded bytes |
| `requiredKeys[].pattern` | Optional string | Go regexp, bounded length |
| `requiredKeys[].format` | Enum / None | None, JSON, URI, PEM |
| `externalSecretRef.name` | Optional block, required name | Fixed kind ExternalSecret |
| `externalSecretRef.apiVersion` | Default ESO v1 | From installation-level allowlist |
| `workloadRefs[].apiVersion` | apps/v1 | Supported workload group |
| `workloadRefs[].kind` | Enum | Deployment, StatefulSet, DaemonSet |
| `workloadRefs[].name` | String | Local workload name |
| `workloadRefs[].containers` | Name list | All selected containers must pass |
| `workloadRefs[].includeInitContainers` | false | Explicit inclusion |
| `workloadRefs[].consumption` | Any | Any, EnvFrom, EnvVars |
| `injection.mode` | Disabled | Later EnvFrom or EnvVars |
| `rotation.restartOnChange` | false | Later approved feature |
| `rotation.maxAge` | Optional duration | Positive, e.g. 720h |
| `rotation.rotatedAtAnnotation` | Project key | Trusted RFC3339 metadata |
| `policy.requireExternalSecretReady` | false | Required ESO result |
| `policy.requireWorkloadReference` | false | Required correct consumption |
| `policy.requireRotationPolicy` | false | Required age policy |

## B.2 Status Fields

`observedGeneration` is the checked specification's generation. `observedSecret` contains the name, UID, and resourceVersion of the Secret actually read. `lastCheckedTime` marks a relevant evaluation, not an arbitrary heartbeat. `missingKeys`, `violations`, and their counts are bounded and deterministic.

`workloadStatuses` contains identity and check results per workload and consumer. Optional action status in a later version separates requesting a change from observing its rollout. `conditions` use a unique `type`, True/False/Unknown status, observedGeneration, reason, message, and lastTransitionTime.

Never add fields such as `actualValue`, `sample`, `secretHash`, `valuePreview`, `rawError`, `decodedJSON`, or a complete `Secret` object. Metadata identifiers must not become unbounded metric label values either.

## B.3 Core Reason Catalog

| Reason | Category | Expected response |
|---|---|---|
| `InvalidSpec` | Configuration | Correct the contract |
| `AccessNotApproved` | Authorization | Obtain administrative approval |
| `SecretNotFound` | Dependency | Check name and source |
| `SecretAccessDenied` | Infrastructure | Check RBAC |
| `MissingRequiredKey` | Data | Correct the source or name |
| `EmptyValue` | Data | Supply an approved value |
| `TooShort` / `TooLong` | Data | Check the declared boundary |
| `InvalidPattern` | Specification | Correct the regexp rule |
| `PatternMismatch` | Data | Check the source format |
| `InvalidJSON` | Data | Correct JSON syntax |
| `InvalidURI` | Data | Correct the absolute URI |
| `InvalidPEM` | Data | Correct PEM structure |
| `EvaluationBudgetExceeded` | Budget | Reduce or justify scope |
| `ExternalSecretNotReady` | Integration | Check ESO |
| `ExternalSecretTargetMismatch` | Integration | Align the target |
| `ContainerNotFound` | Consumption | Correct container selection |
| `EnvConflict` | Consumption | Resolve environment-variable ownership |
| `AmbiguousEnvPrecedence` | Consumption | Simplify sources |
| `RotationTimestampMissing` | Metadata | Add a trusted signal |
| `SecretTooOld` | Policy | Initiate approved rotation |
| `FeatureNotEnabled` | Configuration | Do not expect an inactive feature |
| `UnsupportedRolloutStrategy` | Mutation | Use a supported procedure |

These names are intended as stable identifiers. Define central constants instead of repeating free-form strings across packages. Adding a reason is an API event for users of alerts and dashboards.

## B.4 Release Checklist

Before public publication, accept the canonical schema, security assumptions, authorization, leakage prevention, status freshness, event-driven recovery, time checks, RBAC profile, and operational runbook. Actual unit/envtest/kind results are required for advertised features.

For a mutation release, additionally check grant revocation, ownership conflicts, preservation of concurrent changes, invalid-secret suppression, OnDelete/partition cases, anti-storm policy, and uninstall behavior. Marketing must not imply automatic restart when only an annotation patch was tested.
