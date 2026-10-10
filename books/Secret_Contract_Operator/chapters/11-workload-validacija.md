# 11. Validating Consumers and Environment Configuration

## 11.1 A Reference Is Different from an Effective Variable

A Deployment can contain an `envFrom` reference to the correct Secret, while explicit `env` entries override the same variable. A reference alone is insufficient to claim that the application receives the value the contract checks.

Kubernetes supports explicit and grouped environment-variable sources; source precedence must be considered when checking consumption. This project's conservative policy is to withhold a positive workload finding for conflicting or indeterminate configuration. [S16](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)

## 11.2 Selecting Containers

Every named consumer must exist. With `containers: [api]`, a healthy `metrics` sidecar cannot satisfy the contract on behalf of the `api` container. When multiple containers are selected, each must satisfy the rule; do not use “at least one consumes the secret” logic.

Init containers are excluded by default. Checking them must be explicit, and mutation must remain disabled until separately supported. A secret needed by the application may be inappropriate for a migration or utility init container.

## 11.3 EnvFrom Mode

This mode requires an `envFrom.secretRef.name` pointing to the target Secret. For required consumption, `optional: true` does not satisfy a strict contract. A prefix must be absent or explicitly supported by the API; this initial API does not add implicit prefix support.

If `DB_PASSWORD` is explicitly defined in `env`, check its source. If it comes from another Secret or an inline value, report a conflict. If a later `envFrom` source could overwrite keys and the operator does not inspect its contents, report `AmbiguousEnvPrecedence` instead of guessing.

Do not read arbitrary additional Secrets merely to resolve precedence. That would silently expand the operator's sensitive scope through workload validation. This product's advantage is predictability rather than compatibility with every complex configuration.

## 11.4 EnvVars Mode

Each required key needs its corresponding environment-variable name: `envName`, when provided, or the key name. The reference must specify the exact Secret name and key. For a required rule, `optional` must be omitted or `false`.

```yaml
env:
  - name: PROVIDER_CONFIG
    valueFrom:
      secretKeyRef:
        name: payments-api-secrets
        key: provider.json
        optional: false
```

The contract does not set a variable through `value`; it only checks the reference. An optional rule does not require consumption of an absent key. If managed injection is added later, its `secretKeyRef.optional` must follow the optional-key semantics.

## 11.5 Any Mode

`Any` accepts one of the supported, unambiguous bindings. It does not mean that mentioning the Secret name anywhere in a PodSpec is sufficient. A volume mount, process argument, or annotation is not automatically environment-variable consumption.

Volume and CSI models may become separate consumption strategies in the future. In the MVP, status should report `UnsupportedConsumptionMode` for unsupported configuration rather than claiming that file contents were checked.

## 11.6 Workload Status

For each workload, retain its identity, the list of checked containers, `configured`, and a stable reason. Useful reasons include `WorkloadNotFound`, `ContainerNotFound`, `RequiredReferenceMissing`, `OptionalReferenceNotAllowed`, `EnvConflict`, and `AmbiguousEnvPrecedence`.

Output may contain environment-variable names and keys, but never the existing inline value that caused a conflict. Diagnose a conflict by its path, such as `containers[api].env[DB_PASSWORD]`, without displaying its contents.

## 11.7 The First-deployment Trap

If `requireWorkloadReference: true` and the workload does not yet exist, `Ready` cannot become True. A pipeline that waits for that Ready before creating the workload introduces a circular dependency.

Separate the phases: before the first workload deployment, check only the Secret contract or create a separate preflight contract without a required workload reference. After applying the workload, check consumption and application rollout. Do not hide the problem by temporarily declaring a nonexistent workload valid.

**Checkpoint.** Add a deliberate inline `DB_PASSWORD` conflict to a test Deployment. The operator must report it without revealing the inline value.
