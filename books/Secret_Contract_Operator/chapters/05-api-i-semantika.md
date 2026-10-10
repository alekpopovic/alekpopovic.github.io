# 5. Canonical API and Contract Semantics

## 5.1 The API as a Public Promise

The most expensive mistake in an early operator is often an unclear public field rather than a faulty algorithm. Two boolean fields controlling the same decision, or a “smart” default whose meaning changes with context, make testing, migration, and support harder.

This book therefore consolidates the initial sketch. A missing Secret always prevents a contract from being satisfied. The `nonEmpty` rule belongs to individual keys; there is no conflicting global rule. Injection has one mode instead of a combination of `enabled` and `managed`. Fields that default to `true` use pointers where an omitted field must be distinguished from an explicit `false`.

The CRD uses an OpenAPI schema, a status subresource, and list-map semantics for conditions. Kubebuilder markers generate the corresponding schema and make maintenance easier. [S09](https://book.kubebuilder.io/reference/generating-crd.html)

## 5.2 A Complete Example of the Proposed API

The following manifest describes the **target API**, including fields planned for a later version. In v0.1, injection remains `Disabled` and restart remains `false`. This is not a manifest for an already installed third-party operator.

```yaml
apiVersion: secrets.codepop.tech/v1alpha1
kind: SecretContract
metadata:
  name: payments-api
  namespace: payments
spec:
  secretRef:
    name: payments-api-secrets
  requiredKeys:
    - name: DB_USERNAME
      required: true
      nonEmpty: true
    - name: DB_PASSWORD
      required: true
      minLength: 16
      maxLength: 256
    - name: provider.json
      envName: PROVIDER_CONFIG
      required: true
      format: JSON
  externalSecretRef:
    name: payments-api-secrets
    apiVersion: external-secrets.io/v1
  workloadRefs:
    - apiVersion: apps/v1
      kind: Deployment
      name: payments-api
      containers: [api]
      includeInitContainers: false
      consumption: EnvVars
  injection:
    mode: Disabled
  rotation:
    restartOnChange: false
    maxAge: 720h
    rotatedAtAnnotation: secrets.codepop.tech/rotated-at
  policy:
    requireExternalSecretReady: true
    requireWorkloadReference: true
    requireRotationPolicy: false
```

## 5.3 Key Rules

`requiredKeys` is a list of rules with unique `name` values, with a proposed maximum of 256. `required` and `nonEmpty` default to `true`. An absent optional key is skipped. If an optional key is present, all its declared rules still apply.

`minLength` and `maxLength` measure **bytes in the decoded value**, not Unicode characters or the length of its base64 representation. `nonEmpty` rejects zero bytes; it does not trim whitespace or normalize content automatically. Changing the original value is not the validator's job.

`pattern` uses Go regexp semantics. By default, the rule looks for a match; an author uses anchors to match the entire value. `format` is `None`, `JSON`, `URI`, or `PEM`. JSON means syntactically valid JSON, including scalar values. URI means an absolute URI with a scheme; network access is prohibited. PEM means one or more correctly decoded blocks, with no other content between them.

`envName` is used only for explicit environment-variable mapping. The Secret key `provider.json` is valid, but a platform may require the portable variable name `PROVIDER_CONFIG`. A conservative environment-variable naming rule is a project decision, not a claim that every modern Kubernetes version permits the same characters.

## 5.4 References and Policies

All references are local to the contract's namespace. `externalSecretRef` has the fixed kind `ExternalSecret`; its API version comes from an installation-level list of supported ESO versions. Users cannot read arbitrary resources by supplying a GVK.

`workloadRefs` supports `apps/v1` Deployments, StatefulSets, and DaemonSets. `containers` explicitly selects consumers. When the list is omitted in validation-only mode, all regular containers are checked. Init containers are included only explicitly. Mutation mode requires an explicit container list to avoid unintentionally exposing a secret to a sidecar.

The policies `requireExternalSecretReady`, `requireWorkloadReference`, and `requireRotationPolicy` determine whether the corresponding finding contributes to aggregate `Ready`. A required policy must have its corresponding configuration. Do not accept `requireExternalSecretReady: true` without a reference.

## 5.5 Conditions and Ready Logic

The conditions are `SecretExists`, `KeysValid`, `ExternalSecretReady`, `WorkloadsConfigured`, `RotationPolicySatisfied`, and aggregate `Ready`. An unconfigured optional check receives `True` with reason `NotConfigured`. A configured check that has not yet been evaluated receives `Unknown`.

The proposed formula is:

```text
Ready = authorized
    AND validSpec
    AND SecretExists
    AND KeysValid
    AND (not requireExternalSecretReady OR ExternalSecretReady)
    AND (not requireWorkloadReference OR WorkloadsConfigured)
    AND (not requireRotationPolicy OR RotationPolicySatisfied)
```

A positive result is valid only for conditions from the contract's current generation. An infrastructure failure that prevents a required check is not a positive result. `Ready` may be `Unknown` while checks are pending, or `False` when there is a definite negative finding.

`WorkloadsConfigured=True` means that the declared PodTemplate correctly references the Secret. It does not mean that pods are running or the application is healthy. Automatic restart, when introduced, has a separate action status; it should not be hidden inside the meaning of `Ready`.

## 5.6 Status for One Observation

```yaml
status:
  observedGeneration: 3
  observedSecret:
    name: payments-api-secrets
    uid: 53f81e06-1111-4444-8888-84fd83655102
    resourceVersion: "84721"
  lastCheckedTime: "2026-10-10T08:30:00Z"
  missingKeys: []
  violations: []
  missingKeyCount: 0
  violationCount: 0
  conditions:
    - type: KeysValid
      status: "True"
      observedGeneration: 3
      lastTransitionTime: "2026-10-10T08:30:00Z"
      reason: RulesSatisfied
      message: All declared key rules are satisfied.
```

This example shows part of the status, not the complete output. Every condition has `observedGeneration`. Conditions are treated as a map keyed by `type`, not a list whose order has semantic meaning. `missingKeys` and `violations` are sorted deterministically.

`lastCheckedTime` is updated for a new relevant observation or a scheduled check, not on every pass through the event queue. A timestamp change alone must not keep the reconcile loop running.

## 5.7 Limits and Types

Duration fields use the format supported by the selected Go/Kubernetes type: for example, `24h` or `720h`, rather than an assumed `30d`. Negative and zero maximum ages are rejected. A future timestamp outside the allowed clock-skew window is a metadata error.

The total number of status findings is bounded, with an indicator when results are truncated. Rules have a pattern-length limit; the evaluator limits individual values and the total content processed. These limits belong in the versioned specification and tests.

**Checkpoint.** Document each field's default, validation, and effect on `Ready`. If this cannot fit in one clear table, simplify the API further.
