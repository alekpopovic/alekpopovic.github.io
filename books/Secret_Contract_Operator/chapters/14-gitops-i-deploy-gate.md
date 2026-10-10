# 14. CI, GitOps, and Actual Deployment Control

## 14.1 Status Is Not Enforcement

Kubernetes will not reject a Deployment simply because a `SecretContract` has `Ready=False`. A relationship exists only if a pipeline, GitOps configuration, or separate admission layer establishes it. Status is a signal, not automatic enforcement.

The minimal CI pattern is: apply the Secret contract, wait for a result for the expected generation, apply the workload, wait for workload consumption checks, and verify application rollout. The pipeline does not read Secret values.

## 14.2 The Stale Ready Problem

A plain `kubectl wait --for=condition=Ready` may encounter a positive condition from a previous generation. The gate therefore verifies that `status.observedGeneration` and `Ready.observedGeneration` match the expected generation and that the contract UID has not changed.

Even after these checks pass, the Secret may change before a pod is created. This is a race between checking and use. It would be inaccurate to call such a pipeline atomic or race-free.

## 14.3 Reference Gate Script

This script checks contract identity and generation without reading the Secret. It belongs in a future repository implementing the canonical status. It deliberately avoids displaying the whole object on failure.

```bash
#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-payments}"
CONTRACT="${CONTRACT:-payments-preflight}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || exit 2

initial="$(kubectl -n "$NS" get scn "$CONTRACT" -o json)"
uid="$(jq -er '.metadata.uid' <<<"$initial")"
gen="$(jq -er '.metadata.generation' <<<"$initial")"
deadline=$((SECONDS + TIMEOUT_SECONDS))

while (( SECONDS < deadline )); do
  if object="$(kubectl -n "$NS" get scn "$CONTRACT" -o json)"; then
    if jq -e --arg uid "$uid" --argjson gen "$gen" '
      .metadata.uid == $uid and
      .metadata.generation == $gen and
      .status.observedGeneration == $gen and
      (.status.observedSecret.uid | length) > 0 and
      any(.status.conditions[]?;
        .type == "Ready" and
        .status == "True" and
        .observedGeneration == $gen)
    ' <<<"$object" >/dev/null; then
      echo "Secret contract accepted for expected generation."
      exit 0
    fi
  fi
  sleep 2
done

echo "Secret contract gate timed out." >&2
exit 1
```

If the contract receives a new generation while the script waits, the script does not accept the new configuration's result as belonging to the original request. A team can extend it with an earlier exit and an explicit identity-change message.

Stricter freshness requires a designed protocol for manually requested checks with an acknowledged request ID in status, or a specific binding to a versioned Secret. This script provides neither guarantee and should not be presented as though it does.

## 14.4 Two Phases for the First Deployment

A preflight contract has no required workload reference. It checks content and any ESO dependency. After it is accepted, apply the Deployment with Git-owned environment references. A second contract or post-deployment phase checks that consumers use the correct Secret.

This separation removes the circular dependency in which a contract waits for a Deployment that the pipeline has not yet permitted. In subsequent releases, an existing workload does not change the fact that status confirms only the checked PodTemplate, not a future Git change that has not been applied.

## 14.5 The GitOps Model

The chosen GitOps tool must understand how to interpret custom-resource health and synchronization dependencies. File application order alone does not prove that the previous resource became ready. Implement the integration according to the chosen tool's official documentation and test it in a dedicated cluster.

This book defaults to Git-owned environment references. Enable managed injection only in an installation with an explicit ownership agreement. Avoid a cycle where GitOps removes an annotation, the operator restores it, and the application repeatedly restarts.

## 14.6 Synchronous Admission Rejection

A separate validating webhook could reject certain workload writes. However, the webhook becomes a critical dependency: timeouts, TLS, availability, failure policy, namespace scope, dry-run behavior, and a break-glass procedure all need resolution. Kubernetes guidance recommends narrowly targeted, reliable admission controls and considering built-in alternatives where appropriate. [S22](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/)

A webhook checking only stale `Ready` is not automatically safe. Reading a Secret live reduces one race but still does not guarantee atomically that a pod will later read the same mutable value. For stricter control, consider immutable, versioned Secret references and authorized contract bindings to an exact target.

## 14.7 Guarantees to Avoid

Do not claim that CRD schema validation can arbitrarily read another Secret. Do not claim that `Ready` protects an application from every subsequent invalid rotation. Do not call `fail-open` a hard prohibition, or enable `fail-closed` across the whole cluster without a recovery plan.

**Checkpoint.** Draw the timeline from validation through workload modification to reading environment variables at process startup. Every gap marks a guarantee boundary that documentation must acknowledge.
