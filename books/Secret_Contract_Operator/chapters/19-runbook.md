# 19. Operational Procedures and Incidents

## 19.1 Diagnosis Without Displaying Secrets

Inspect contract status and manager events first, rather than Secret contents. Operator status should suffice for most common errors. Reading values directly is a separate authorized operation, performed only when necessary.

```bash
kubectl -n payments get scn
kubectl -n payments describe scn payments-api
kubectl -n payments get scn payments-api \
  -o jsonpath='{.status.conditions}'

kubectl -n secret-contract-system get deploy,pods
kubectl -n secret-contract-system logs \
  deployment/secret-contract-operator --tail=100
```

These commands assume the stated installation name. They do not use `kubectl get secret -o yaml`, `printenv`, or `exec env`. Review logs locally before forwarding them publicly, and only do so after checking their contents.

## 19.2 A Contract Is Not Ready

| Reason | Most likely investigation | Safe action |
|---|---|---|
| `SecretNotFound` | Wrong name or failed synchronization | Check reference and ESO status |
| `MissingRequiredKey` | Changed contract or provider structure | Compare key names |
| `InvalidJSON` | Incorrect source format | Secret owner corrects the contents |
| `AccessNotApproved` | Revoked or missing grant | Check administrative approval |
| `SecretAccessDenied` | Incorrect Role/RoleBinding | Check operator identity |
| `ContainerNotFound` | Renamed container | Correct the workload reference |
| `AmbiguousEnvPrecedence` | Multiple conflicting sources | Simplify environment mapping |

Do not “fix” an incident by globally escalating privileges to cluster-admin. Identify the exact missing permission and whether it should exist at all. The same applies to disabling a required policy merely to turn status green.

## 19.3 Status Appears Stale

Check `metadata.generation`, `status.observedGeneration`, condition generations, and the observed Secret identity. Verify that the manager is running and the namespace is within its watch scope. A Secret change must have a path through the index and map handler.

If only time-based rules are stale, inspect requeue calculations and the clock. If a newly installed ESO is undiscovered, follow the documented discovery/restart procedure. Do not randomly restart application pods to “refresh” operator status.

## 19.4 A Restart Loop

Temporarily disable mutation at the installation level without changing Secret values. Record only metadata history: which contract issued the token, for which Secret UID/RV, and which workload generations resulted.

Look for another controller changing the same annotation, GitOps reverts, ESO metadata churn, or an overly short debounce rule. After removing the cause, check the latest approved state before re-enabling restart.

## 19.5 Invalid Rotation

If new contents are invalid, confirm that the operator issued no new restart signal. The source owner repairs or rolls back the credential using their own runbook. After correction, check synchronization, the contract, and application health as separate phases.

Do not assume old pods will necessarily survive. Independent failures or scaling may remove them. Critical applications need a versioned rotation procedure and a sufficiently long credential overlap period where the source supports it.

## 19.6 Suspected Leakage

Treat a published value as potentially compromised. Restrict access to logging and metrics systems, stop the risky operator feature, preserve redacted evidence, and initiate authorized rotation of affected credentials. Deleting a log line does not replace rotation.

In the technical incident record, state which channel leaked, how long it was available, and which components had access. Do not copy the actual secret into a ticket as proof of leakage.

## 19.7 Uninstall and Recovery

An ordinary uninstall removes the controller, its ServiceAccount, and related installation resources. It should not delete application Secrets or workloads. Remove a CRD only through a separate decision, because deletion affects every instance of that custom resource.

Before disabling the mutation profile, document which references and annotations remain. The next configuration owner must know what Git owns and what the operator previously added. Backing up contract specifications does not back up actual credentials.

**Checkpoint.** The operator must have a shutdown procedure that does not require reading or restoring real Secret values from its own state.
