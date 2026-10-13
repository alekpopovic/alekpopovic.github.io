# Chapter 23 - Authentication, Authorization, and Node Trust

A viewer is allowed to inspect Atlas's deployment but must not replace its image. An agent is allowed to report the state of its assigned task but must not impersonate another node. Both requests reach the same server, yet they require different identities and different checks. Treating every bearer value as one universal token would erase the distinction between human authority, enrollment authority and ongoing worker ownership.

You will trace a user mutation and a node report through their separate authentication paths, inspect role selection and optional enablement, and explain the trust granted to Docker access. API contracts and agent report ownership are prerequisites. The source edition uses local HS256 user JWTs and short-lived node credentials; this chapter does not imply OAuth, an external identity provider or mutual TLS.

## User JWTs and Role Checks

Default main parses static users and passes cfg.JWTSecret and the resulting user map into the API handler. userAuthMiddleware selects a namespace, validates it and asks requiredRole about the request. For a nonempty JWT secret on a protected route, it parses a bearer token, verifies its signature/claims and establishes the principal before the handler runs. A bad identity returns unauthorized; an authenticated but insufficient role returns forbidden.

Unchanged source excerpt — [internal/api/api.go:1267–1275](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1267-L1275):

```go
		required, ok := requiredRole(r)
		if !ok || s.jwtSecret == "" {
			next.ServeHTTP(w, r)
			return
		}
		token, err := auth.ParseBearer(r.Header.Get("Authorization"))
		if err != nil {
			s.writeAuthError(w, r, http.StatusUnauthorized, "unauthorized", "missing or invalid bearer token")
			return
```

The empty-secret condition is essential. Built-in server configuration leaves user JWT auth disabled unless configured, even though the development bootstrap token is nonempty. That distinction is a development default, not an assertion that every endpoint is publicly accessible: agent routes perform their own credential checks. A deployment review should record effective settings rather than infer user protection from the existence of auth code.

ValidateJWT accepts HS256 only, checks the HMAC, parses claims and requires a subject plus either a valid global role or namespace-role map. Each namespace role must be valid. Expiration is enforced when ExpiresAt is positive; a missing exp is not made mandatory by this implementation. IssuedAt is represented but not a complete replay-prevention protocol. The claims contract is narrower than a general-purpose identity-provider integration.

RoleForNamespace prefers a valid global role; otherwise it looks up the normalized namespace. Static users can override the token's role with a configured global role and clear namespace roles. This can be convenient for local administration, but it changes the authority model. An operator investigating an unexpected permission must inspect both token claims and static-user configuration, without printing the token itself.

Roles have ordered authority: viewer, operator and admin. Reading services/tasks/events/logs is viewer-level; deploying, scaling, rolling back and deleting services is operator-level; node drain/uncordon, namespace management, quota changes and audit access require admin in their named routes. Unrecognized protected paths fall back to admin rather than silently bypassing authorization. Exact route/method combinations, not friendly UI labels, define the check.

## Agent Bootstrap Is a Different Trust Path

Registration accepts a configured bootstrap token through its header or bearer form. If the configured token is empty, this specific registration check permits enrollment; built-in configurations instead provide a known development value that must not be confused with a private production secret. The server issues a new random node credential after successful registration and stores only its hash and expiry in the node record.

The issuer reads thirty-two random bytes, base64url encodes the bearer value, calculates expiry and returns a separate record containing Hash and ExpiresAt. The default lifetime is fifteen minutes. This is a node credential represented as an opaque token, not a user JWT with viewer/operator/admin claims. The AgentIdentity interface is an extension seam; the current token format does not itself carry a certificate-bound node identity.

Unchanged source excerpt — [internal/auth/agent.go:56–66](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go#L56-L66):

```go
func (i *TokenAgentCredentialIssuer) Validate(_ context.Context, token string, record AgentCredentialRecord, now time.Time) error {
	if record.Revoked {
		return ErrInvalidToken
	}
	if record.Hash == "" || token == "" || HashAgentToken(token) != record.Hash {
		return ErrInvalidToken
	}
	if !record.ExpiresAt.IsZero() && !now.UTC().Before(record.ExpiresAt.UTC()) {
		return ErrInvalidToken
	}
	return nil
```

Validation rejects revoked credentials, missing/mismatching hashes and expired records. The server fetches the specific NodeID's stored record before validating the presented token, binding the request to current node authority. Heartbeats issue another credential and replace the stored hash, so rotation changes which value is current. Raw credentials are returned only as needed to the registering/heartbeating agent and must not appear in publication evidence.

Rotation has an acknowledgement window. If the server records a new hash but the response carrying the new value is lost, the client may retain an older token that no longer matches. Source-based recovery expectations must account for that path rather than promise seamless indefinite retries. Expiry and revocation also need a re-enrollment policy; having an interface for future identity mechanisms does not implement one automatically.

RevokeNode sets the node's AgentRevoked flag. SetAgentCredential clears that flag when establishing a fresh credential. Thus revocation prevents use of the current record, but continued access to enrollment authority can matter for re-registration. It is not a permanently revoked certificate authority. Protect the bootstrap path separately from ordinary reporting.

## Which Routes Require Which Identity

requiredRole excludes /v1/agent routes from user JWT handling. That means they proceed to agent-specific handlers, not that they are unprotected. Agent task retrieval and heartbeat call authorizeAgentCredential with the relevant node ID. Task status first validates that node credential, then ReportTaskStatus checks the task is assigned to the same node and the lifecycle permits the requested state. Authentication and assignment authorization remain distinct decisions.

A malicious or mistaken node token for node A cannot legitimately report a task owned by node B merely because both nodes are registered. The server also rejects status spellings outside the allowed agent states. A late running report against desired stopped must satisfy lifecycle guards rather than overwrite current authority. These checks protect record mutation; they do not physically fence an already-running isolated container.

User reads have their own subtleties. Secret GET access returns metadata rather than plaintext, and audit reads require admin. The Traefik provider endpoint is viewer-protected when user JWT is active, so an external consumer's polling must be configured accordingly. /healthz, /readyz and /metrics bypass user roles; their responses should not be described as privileged proof of full system health.

Server-to-agent log streaming uses the bootstrap-token authority on the agent listener, separate from the short-lived credential the agent presents to server routes. This asymmetry deserves explicit operational documentation. A user authorized to request logs relies on the server's proxy and node address handling; the worker's local listener has its own trust boundary. Do not copy the user's JWT into every downstream hop or assume node credentials protect an unrelated listener.

| Request | Identity/authority | Additional boundary |
| --- | --- | --- |
| User service rollout | Configured JWT and operator-or-higher role | Namespace, admission and operation ordering |
| Node registration | Configured bootstrap token | Current enrollment policy |
| Task status report | Current credential for claimed NodeID | Task ownership and lifecycle guard |
| Server-to-agent logs | Bootstrap token at agent listener | Container/task selection and streaming scope |

The table identifies current behavior, not a recommendation to share all credentials. It allows an operator to rotate the right authority and a developer to test each rejection at the correct layer.

## Docker Access and Missing Mutual TLS

The trusted agent speaks to the Docker daemon. A caller with that socket authority can create powerful workloads, inspect environment and affect host resources. API admission can restrict submitted security options, but it does not turn the agent's daemon credential into a harmless read-only capability. Compromise of that trust path has a different consequence from compromise of a viewer JWT.

Native server/agent communication in this edition uses HTTP. Token possession authenticates requests according to server records; it does not encrypt transport or bind a peer certificate to a node. External TLS termination can protect selected links when configured, but mutual TLS, certificate issuance, renewal and revocation are not implemented merely because a future credential interface exists. State those missing responsibilities precisely instead of describing token auth as equivalent security.

Namespaces and roles are API boundaries. They do not create isolated Docker daemons, kernels or tenant networks. A legitimate operator can still deploy a workload within allowed policy, and an agent administrator can inspect local execution. Chapter 27 examines that isolation scope; Chapter 24 follows plaintext secrets to the same execution boundary.

The Atlas failure scenario combines these facts. User auth is enabled and viewer mutation is correctly forbidden. A worker's heartbeat then rotates its credential, but the response is lost. The next heartbeat uses the old credential and fails. That does not show the viewer bypassed RBAC; it shows a different identity's acknowledgement/recovery window. Incident analysis should retain rejection code, node/task ID and request time while redacting every bearer value.

## Atlas Lab: Prove Rejection Without Publishing Tokens

Use Go 1.25 in the disposable pinned source copy. Existing tests generate their own synthetic credentials and verify outcomes without a real worker or external identity service. Avoid shell arguments containing actual owner tokens and do not copy signed fixture tokens into chapter listings.

```bash
go test ./internal/auth -run TestAgentCredential -count=1 -v
go test ./internal/api -run 'Test(UserAuth|AgentRegisterRequiresBootstrapToken|AuditRequiresAdminRole)' -count=1 -v
```

Expected observations include unauthorized missing/invalid user credentials, forbidden viewer mutation, accepted authorized reads and invalid/expired/revoked node credentials. The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) records authentication and API assertions with caching disabled. The [security laboratory](../../labs/05-security-boundaries/README.md) separately exercises controlled wrong-node and authorization boundaries; neither result establishes mTLS or hostile-host isolation. For a separate route-matrix fixture, generate local viewer/operator/admin JWTs in memory, send requests through an httptest handler and record only method, path, status and whether state changed.

Include the empty-JWT-secret case explicitly so the test distinguishes disabled user auth from a valid identity. Test a node A credential on a node B task report and assert both rejection and unchanged task state. Add the rotation-response-loss case only as a labeled teaching extension, preserving the original implementation. Any stronger recovery proposal requires its own tested protocol rather than changing expected output to fit the story.

Abort if a fixture points to a live server, captures an Authorization header or uses a real enrollment token. Cleanup discards generated identities and temporary logs after retaining sanitized outcome evidence. A pass establishes these handler/issuer contracts, not end-to-end TLS, Docker host containment or complete tenant isolation.

## Exercises

1. Why can an empty user JWT secret disable role checks while agent task routes still reject a missing node credential?
2. A token grants a namespace viewer role, but static users configure its subject as operator. Which authority does this middleware select?
3. Trace the lost heartbeat-rotation response window. Which stored field changes and why can a previously valid credential stop working?
4. Explain why a protected viewer API and short-lived node tokens do not establish mutual TLS or containment after Docker socket compromise.

[Worked answers](../solutions/ch23.md) identify current authorities and their limits rather than treating every successful authentication as universal trust.

## Development history and source references

Original development prompts 18, 19, 51 supply the requested scope. The inspected implementation history includes [403a9fc9d900](https://github.com/alekpopovic/orch/commit/403a9fc9d9005aca95ade9f5edfbbc77acd1a911), [4f25e78c229b](https://github.com/alekpopovic/orch/commit/4f25e78c229ba040c07a84801490485b5a0cbb2e), [a5cb0c5fb4ca](https://github.com/alekpopovic/orch/commit/a5cb0c5fb4cab92130b1cdfd15df88256267bcb7). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/auth/auth.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/auth.go#L1-L191)
- [internal/auth/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go#L1-L72)
- [internal/auth/agent_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent_test.go#L1-L67)
- [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1-L2036)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md#L1-L170)
- [docs/SECURITY_REVIEW.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY_REVIEW.md#L1-L150)
