# Chapter 27 - Namespaces and the Limits of Multi-Tenancy

Two teams want a service called atlas-api. Renaming every object globally would make ownership awkward, while allowing every request to see every ID would undermine the separation. Orch namespaces solve a specific part of that problem: selecting logical object scope and authorization context. They do not create separate Docker hosts or independent networking domains.

This chapter assumes authentication, secret references and the ordinary service path. You will trace the namespace from HTTP header or CLI selection into domain lookups, distinguish an invisible cross-namespace ID from a forbidden namespace request, and examine the data loss hidden in a namespace down migration. The Atlas lab deliberately proves logical isolation only, using in-process services with no real tenant workloads.

## Namespace Context and Local Names

Normalize trims whitespace, lowercases the name and maps an empty value to default. Validate accepts one to 63 lowercase alphanumeric characters or hyphens with alphanumeric ends. The context helpers carry the normalized selection under a private key. FromContext returns a normalized value, including default when no selection exists. [Claim ch27.context](../../validation/evidence/ch27.json).

The API selects X-Orch-Namespace first when nonempty, otherwise the namespace query parameter, and then normalizes it. Middleware validates the selection and places it in request context before reaching protected operations. The CLI's namespace option is sent through its client configuration to the corresponding HTTP selection. A CLI flag is not an independent permission grant: the server still authenticates the caller and checks its role for the selected scope.

[internal/api/api.go, lines 1303–1308](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1303-L1308) at the locked revision.

```go
func selectedNamespace(r *http.Request) string {
	if value := strings.TrimSpace(r.Header.Get("X-Orch-Namespace")); value != "" {
		return namespace.Normalize(value)
	}
	return namespace.Normalize(r.URL.Query().Get("namespace"))
}
```

Context selection has an important internal nuance. Selected distinguishes an explicitly supplied context value from an absent one. Matches allows all object namespaces when selection was not explicit, but compares normalized names when it was. This supports internal operations that need broader inventory. It also means direct library calls with context.Background are not equivalent to authenticated HTTP requests, whose middleware supplies explicit scope. Do not use an unscoped internal list as evidence that the API leaks every tenant.

The MemoryService service uniqueness check combines namespace and name. The namespace migration makes the corresponding SQL constraint UNIQUE(namespace, name), and changes secret/registry primary keys to include namespace. Thus team-a/atlas-api and team-b/atlas-api can be separate objects with different IDs. Names become convenient local handles; IDs remain distinct object identities and still require scoped access checks.

A practical incident bundle should record both namespace and ID. An alert saying only atlas-api can point to the wrong team's service; a copied ID without context can return not-found to a properly scoped operator. Adding namespace to URLs or CLI output improves operational clarity, but the authoritative separation still belongs in server lookup predicates rather than display conventions.

The focused source tests use the same name api in team-a and team-b, with zero replicas. They verify distinct IDs and filtered listing without starting Docker containers. The name is incidental to the invariant; the Atlas exercise applies the same contract to atlas-api. A successful create here proves stored logical objects, not two physically running application instances.

## Cross-Namespace IDs and Secret References

GetService checks both whether the ID exists and whether namespace.Matches permits that object. When an explicit team-a context asks for a team-b ID, it returns ErrNotFound. This prevents the object lookup from disclosing a distinct exists-but-in-another-namespace outcome. It is a domain visibility decision, not proof of secrecy against every timing or operational side channel. [Claim ch27.visibility](../../validation/evidence/ch27.json).

[internal/namespace/context.go, lines 44–55](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go#L44-L55) at the locked revision.

```go
func Selected(ctx context.Context) (string, bool) {
	if ctx == nil {
		return Default, false
	}
	name, ok := ctx.Value(contextKey{}).(string)
	return Normalize(name), ok
}

func Matches(ctx context.Context, objectNamespace string) bool {
	selected, explicit := Selected(ctx)
	return !explicit || selected == Normalize(objectNamespace)
}
```

At the HTTP authorization layer, a caller lacking any qualifying role for the selected namespace can instead receive forbidden before object lookup. These cases must not be conflated. A viewer allowed in team-a but selecting team-b is denied at the role boundary; an authorized request within team-a for an invisible team-b ID reaches scoped lookup and looks absent. Tests should state which boundary they exercise.

Secret resolution uses namespacedKey with the workload's namespace and secret name. Service creation checks the reference there, and assignment resolution decrypts that same namespace-local record. A secret database in team-a therefore cannot satisfy team-b's reference merely because the text name matches. The focused cross-namespace secret test expects an invalid-state rejection for the missing local reference.

Registry credentials follow the same namespace-local key pattern for ordinary service tasks. This limits accidental cross-team references, but an administrator with cluster-wide authority can still act across scopes. A credential intentionally recreated in two namespaces is two records even if it ultimately authenticates to the same registry account. Keep external account ownership separate from internal namespaced identity.

The [executed focused suite](../../validation/labs/ch27/focused-tests.json) passed namespace object and secret-reference isolation cases, plus API namespace-role tests. It uses in-process handlers and disposable test signing material. It does not contact a production identity provider, run network isolation probes or certify a tenant security boundary.

The Atlas failure window is a copied service ID submitted under the wrong namespace. An operator might interpret not-found as deletion, then create a new service with the same local name. Before concluding state was lost, verify the selected header/flag, caller role and object namespace. Conversely, do not add a globally unscoped fallback lookup merely to make that operator error more convenient; doing so changes the visibility contract.

## Namespace Roles and Cluster Administration

Principal can contain a global Role or a NamespaceRoles map. RoleForNamespace returns a valid global role first; otherwise it looks up the normalized namespace in the map. The role hierarchy distinguishes viewer, operator and admin capabilities in the API. Namespace selection and role selection must therefore be evaluated together. [Claim ch27.roles](../../validation/evidence/ch27.json).

A global viewer has a broader scope than a viewer entry only for team-a, even if both can read a service in team-a. Similarly, a namespace-scoped admin entry should not silently become cluster administration. The middleware has special handling for namespace-management routes so a role map alone does not grant the global namespace operation. The actual required role for each route still matters; a claim shape does not replace the route's authorization check.

| Request | Relevant boundary | Expected interpretation |
| --- | --- | --- |
| Team-a viewer selects team-a | Namespace role and read permission | Authorized scope |
| Same viewer selects team-b without role | Authorization before domain lookup | Forbidden |
| Team-a scoped lookup uses team-b ID | Object namespace match | Not found |
| Namespace-only role attempts cluster namespace management | Cluster role requirement | No automatic cluster authority |

The table describes source/test paths, not a universal response for requests with invalid tokens or malformed names. Those fail earlier. Tests should retain valid authentication while varying only namespace scope when measuring this distinction, otherwise an unauthorized response can hide whether the scoped object check was reached.

Migration 000011 introduces a default namespace and assigns existing relevant rows to it. It adds namespace columns and indexes to services, tasks, deployments, events, secrets, registry credentials and audit logs. Foreign-key relationships and uniqueness become part of the stored logical model. Applying that migration is still a database operation separate from the default server's memory-owned state.

The down migration is destructive. It explicitly deletes non-default rows from several tables, including services, tasks, deployments, events, secrets, registry credentials and audit history, before removing namespace columns and restoring older uniqueness. It also deletes related service versions. This is not a reversible transformation preserving both teams' data under globally unique names. The appendix recovery runbook must require backup/restore review rather than presenting down/up as harmless housekeeping. [Claim ch27.rollback](../../validation/evidence/ch27.json).

A schema downgrade can also affect evidence: removing non-default audit rows destroys part of the incident record. Keep operational exports and database backups according to the actual retention/recovery plan before considering such a change. A passing migration build does not mean a production rollback has acceptable data semantics. The safe chapter lab does not execute this destructive downgrade.

## Logical Isolation on Shared Workers

Namespaces organize API state, local names, roles, secrets and selected accounting. Nodes remain shared cluster resources. The agent can receive tasks across namespaces, and the Docker daemon still has host authority. A logical boundary that hides a service ID does not stop one host process from exploiting kernel vulnerabilities, exhausting an unbounded resource or reaching an exposed port.

The ordinary service path's scheduler/resource limitations are especially relevant. Namespace quotas account declared requests, while actual host enforcement needs a complete field path. A namespace name is not a cgroup, a network policy or a disk allocation. Do not infer physical isolation from a successful accounting rejection or an HTTP404.

Volume naming needs a separate review as well. Namespaced metadata can distinguish equal local names, but the Docker adapter ultimately receives a named volume string. If that string does not incorporate a unique namespace/volume identity, two logical names may share a physical daemon namespace. Chapter 32 examines the exact mapping. Cross-namespace secret tests do not cover this storage path.

This leads to a useful operational choice: treat shared workers as a common trust domain until stronger isolation mechanisms are independently implemented and tested. Separate hostile workloads at a boundary that matches the threat model. The book does not prescribe a particular product or claim certification; it identifies what the source actually enforces so the reader can avoid relying on absent mechanisms.

The real history is [9e78fed31df03d7a985a9f4ceae4770739b05014](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014), which batches namespace/API policy work. Original prompt 65 records requested namespace intent. The current code and tests establish the logical checks; a tracking entry or design paragraph cannot expand them into physical multi-tenancy.

For the safe Atlas lab, use the disposable source module, pinned Go 1.25 and no server/database/Docker process. Predict two distinct same-name services, one visible service per explicit team context, a cross-scope ID looking absent and a missing local secret reference being rejected. Run:

```sh
go test ./internal/namespace ./internal/auth ./internal/controlplane ./internal/api \
  -run 'TestNamespace|TestSecretReferencesCannotCrossNamespace' -count=1 -v
```

The execution log records actual selected cases. Inspect their request headers and assertions; a test that only checks different IDs would not prove list filtering or role behavior. Cleanup is test process exit and temporary-file removal. No real tenant data or credentials are needed.

An extension can create two Atlas-named services through an in-process API handler with an explicitly scoped principal. Capture status codes and sanitized IDs, then vary one request dimension at a time: scope, object ID or role. Keep the expected forbidden/not-found distinction explicit. A live shared-host penetration or storage-isolation claim is outside this lab and requires a separate authorized threat model and evidence.

## Exercises

1. Explain why context.Background can permit a broader internal Matches result than an explicit default namespace context.
2. Distinguish forbidden namespace selection from a not-found cross-namespace object ID. Which layer decides each?
3. Trace a same-named secret reference in team-b when only team-a owns that secret. What result should the service method produce?
4. An operator proposes the namespace down migration as a reversible cleanup. Identify data and evidence at risk, then explain why logical isolation still does not establish hostile-worker isolation.

[Worked answers](../solutions/ch27.md) retain the layer distinctions and destructive rollback semantics. Namespace controls are valuable when their scope stays explicit: object visibility and authorization are implemented; independent host, network and storage isolation are separate guarantees.
