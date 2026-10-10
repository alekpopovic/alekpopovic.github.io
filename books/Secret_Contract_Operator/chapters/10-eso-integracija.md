# 10. Integration with External Secrets Operator

## 10.1 Keeping the Integration Optional

A cluster without ESO must be able to run the validation-only operator with ordinary Kubernetes Secrets. Startup must therefore not unconditionally wait for an informer for a CRD that may not be installed.

The first implementation can discover supported ESO versions and use bounded polling only when a contract has `externalSecretRef`. A more advanced version registers a watch when the CRD is present, with rediscovery or a documented restart if ESO is installed later. Both strategies are acceptable when explicit and tested.

## 10.2 Unstructured Reads with a Fixed Scope

```go
// Reference snippet: apiVersion has already passed the allowlist.
es := &unstructured.Unstructured{}
es.SetAPIVersion(ref.APIVersion)
es.SetKind("ExternalSecret")
err := r.APIReader.Get(ctx, client.ObjectKey{
    Namespace: contract.Namespace,
    Name:      ref.Name,
}, es)
```

An unstructured approach avoids depending on ESO's Go API package, but does not remove schema and compatibility requirements. The code must handle missing `status.conditions`, incorrect field types, and an unavailable API without panicking. It must not accept an unrestricted user-supplied kind or API group.

## 10.3 What We Check

Check that the referenced ESO object exists, targets the same Secret the contract validates, and has the appropriate `Ready` condition set to `True`. Calculate the effective target according to the supported ESO schema, including its documented default when `spec.target.name` is unset.

If a healthy ExternalSecret produces a completely different Secret, the contract must report `ExternalSecretTargetMismatch`. Matching the ExternalSecret object's name alone does not prove the target.

Do not copy ESO's `message` or arbitrary `reason` verbatim. Use local reasons: `ExternalSecretNotReady`, `ExternalSecretNotFound`, `ExternalSecretAPINotAvailable`, and `ExternalSecretTargetMismatch`. An unknown schema shape means `UnsupportedExternalSecretSchema`, not automatic `Ready=True`.

## 10.4 Freshness and Age Are Different

ESO's `refreshTime` concerns fetching and refreshing the target Secret, while `Ready` has a defined synchronization meaning. Neither proves when the underlying credential changed at the provider. [S02](https://external-secrets.io/latest/api/externalsecret/)

If the same database password is successfully synchronized every two minutes, its business age may still be six months. Do not calculate `maxAge` from `refreshTime` or call it “password age.” Separate synchronization freshness, current-content validation, and trustworthy rotation evidence.

## 10.5 Connection Example

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: payments-source
  namespace: payments
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: team-secret-store
    kind: SecretStore
  target:
    name: payments-api-secrets
    creationPolicy: Owner
  dataFrom:
    - extract:
        key: production/payments-api
---
apiVersion: secrets.codepop.tech/v1alpha1
kind: SecretContract
metadata:
  name: payments-api
  namespace: payments
spec:
  secretRef:
    name: payments-api-secrets
  requiredKeys:
    - name: DB_PASSWORD
      minLength: 16
  externalSecretRef:
    name: payments-source
    apiVersion: external-secrets.io/v1
  policy:
    requireExternalSecretReady: true
```

This example assumes that `team-secret-store` is already securely configured. It contains no cloud credentials and prescribes no new provider authentication model. Secret Contract Operator needs no permission to read SecretStore configurations themselves to check an application contract.

## 10.6 Compatibility and Testing

For every officially supported ESO version, test at least: explicit target, default target, Ready True/False, absent condition, incorrectly typed condition, absent CRD, deleted object, and changed target. If an API version is unsupported, show a clear reason rather than silently falling back.

Envtest can install a minimal test CRD and test the adapter, but this does not replace a kind test with an actual supported ESO release. A fake schema often misses differences in defaults and status behavior.

**Checkpoint.** Remove ESO from the test cluster. A contract without an ESO reference should keep working; one requiring an ESO check should clearly report the unavailable integration.
