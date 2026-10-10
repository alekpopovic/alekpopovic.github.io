# 17. Packaging, RBAC, and Installation

## 17.1 Two Installation Profiles

The default profile is namespace-scoped and validation-only. The controller reads within the approved scope, updates contract status, and publishes events. It optionally reads ESO and workload resources. It cannot create, modify, or delete Secrets and has no workload write permission.

The mutation profile is enabled separately, adding minimal workload `patch` permission and the required authorization implementation. Helm's `values.yaml` should not install a more powerful ClusterRole by default simply because the binary contains a future feature.

## 17.2 Namespaced Reader Role

The following manifest is a reference RBAC excerpt for an observed application namespace. Define leader-election and manager-namespace permissions separately. Include the ESO rule only when that integration is active.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-contract-reader
  namespace: payments
rules:
  - apiGroups: [secrets.codepop.tech]
    resources: [secretcontracts]
    verbs: [get, list, watch]
  - apiGroups: [secrets.codepop.tech]
    resources: [secretcontracts/status]
    verbs: [get, patch, update]
  - apiGroups: [""]
    resources: [secrets]
    verbs: [get, list, watch]
  - apiGroups: [apps]
    resources: [deployments, statefulsets, daemonsets]
    verbs: [get, list, watch]
  - apiGroups: [""]
    resources: [events]
    verbs: [create, patch]
```

This Role permits reading all Secrets in the namespace. It does not provide per-Secret isolation. A stricter profile must align actual `get` permissions, the watch model, and approved references. `resourceNames` is no magic solution for an arbitrary informer listing all objects.

## 17.3 Identity and Leader Election

The manager receives a dedicated ServiceAccount without cluster-admin privileges. A RoleBinding in the application namespace can reference a ServiceAccount in the operator namespace. Restrict leader-election Lease permissions to the manager namespace and the specific resources needed.

Two replicas with leader election improve control-component availability but do not automatically double reconcile capacity. The standby process may still have cache and metrics characteristics that need verification in the selected configuration.

## 17.4 Pod Hardening

```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
containers:
  - name: manager
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        memory: 256Mi
```

These are initial values for testing, not measured operator requirements. A read-only filesystem may require an explicit temporary volume for certain features; do not disable hardening without explanation. The image should contain no shell unless the runtime needs one.

NetworkPolicy should allow required API communication and metrics scraping, with DNS only where necessary. The exact API endpoint and network implementation behavior depend on the cluster; do not promise that a generic manifest is a universally applicable firewall.

## 17.5 The Helm Chart Contract

The chart should expose image digest, resources, watched namespaces, securityContext, ServiceAccount, reader RBAC, optional mutation RBAC, metrics, and optional ServiceMonitor configuration. A production example must not leave the image tag implicitly at `latest`.

The default chart does not require cert-manager when there is no webhook. If a webhook is introduced later, document whether cert-manager or another supported mechanism supplies TLS. Cert-manager is not an inherent requirement of every operator.

## 17.6 The CRD Lifecycle

Helm CRD files in `crds/` have a special lifecycle: standard installation is different from automatically managing CRD upgrades and deletion. Official Helm documentation warns about these limitations and the limits of dry-run checking. [S24](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/)

Publish the CRD manifest as a separate release artifact and document the sequence: check compatibility, apply the new CRD schema, upgrade the controller, and only then use new CR features. Do not delete the CRD as part of an ordinary `helm uninstall` flow.

## 17.7 Installing an Actual Release

Once the project publishes a release, the README uses an exact version and verifiable artifacts. Until then, commands use the local chart and a locally built image. Do not invent a public registry tag that users cannot download.

```bash
# Prerequisite: the operator is implemented and the chart exists.
helm lint charts/secret-contract-operator
helm template sco charts/secret-contract-operator \
  --namespace secret-contract-system > rendered.yaml

# Review rendered.yaml before applying anything to a cluster.
```

**Checkpoint.** Render the validation-only chart and automatically check that no rule grants `patch`, `update`, `create`, or `delete` on Secrets or workloads, apart from explicitly permitted status/event operations.
