# 06. Keep Human, Service and Cluster Identities Distinct

**Part II — Control Plane**

AgentPlane has at least four identity classes: human users, service accounts,
cluster connectors and local workloads. Sharing one authentication mechanism
across all four makes authority difficult to reason about. A browser session
should not authenticate a connector, and a connector certificate should not
become an organization administrator credential.

## Human sessions

For a same-origin web console, an opaque server-side session is a straightforward
starting point. Put the session identifier in a Secure, HttpOnly cookie and
protect state-changing requests against CSRF. Choose SameSite behavior to match
the actual deployment and authentication flow rather than applying a setting
without testing it. Session rotation, expiration and server-side revocation are
part of the design. [S14](../references.md#s14)

Store hashes of reset and verification tokens. Make them single-use and bounded
by expiry. Avoid account enumeration in both responses and timing where
practical. Use a reviewed password-hashing library and calibrate resource costs
on the actual service environment. A copied parameter set is not a substitute
for performance and abuse testing.

An external identity provider can reduce first-party credential handling, but it
does not remove authorization. Validate issuer, audience, redirect binding and
other protocol requirements through maintained libraries. Keep the mapping from
identity-provider subject to local membership explicit.

## Authorization is a separate decision

A role is a named collection of permissions. A permission is not a plan feature.
A billing administrator may manage subscription settings without executing code.
A developer may execute a session without changing cluster-local security
bounds. Effective authorization is the intersection of identity permissions,
resource scope, organization policy and product entitlements.

Define a small permission vocabulary before adding arbitrary custom roles:
`cluster.enroll`, `runtime.manage`, `sandbox.create`, `sandbox.execute`,
`policy.manage`, `approval.decide`, `audit.read` and `billing.manage`. Deny by
default. Protect the last organization owner and prevent a delegating user from
granting powers they are not allowed to delegate.

Do not let a hidden UI button become the security boundary. The server must check
every operation, including WebSocket subscriptions, file downloads and export
status endpoints. When membership changes, long-lived operations need a defined
revalidation or revocation policy.

## Service-account credentials

Use a public key identifier and a high-entropy secret component. Store a secure
verifier rather than the full secret. Display new credentials once, support
rotation overlap and make revocation observable. Bind a service account to
organization and project scope; optionally allow explicit organization-wide
permissions where the product requires them.

Rate-limit failed verification before it becomes an expensive database or hash
operation. Do not record credentials in CLI debug output, reverse-proxy logs or
error reports. A one-time reveal screen must not leak the secret into browser
analytics or persistent client state.

## Stream authorization

An interactive terminal is a privileged channel, not a read-only dashboard
widget. Authorize the session and execution being attached. A short-lived,
single-use stream ticket can avoid placing a long-lived API credential in a
WebSocket URL. Still consider proxy access logs: any ticket in a URL can appear
there. Prefer a reviewed handshake flow that avoids query-string credentials,
and ensure expiration and replay handling are tested.

Disconnect streams when the user logs out, changes project context or loses the
necessary permission according to the chosen revocation policy. Bound the delay
if authorization is cached. “Immediate revocation” is not credible when an
unbounded cache or a never-rechecked stream remains active.

## Keep authorization evidence useful

Record actor type, actor ID, scope, operation, outcome, policy version and request
ID. Do not record passwords, complete tokens or tool input bodies. Failed
authorization can reveal sensitive resource existence, so user-facing errors may
need a consistent not-found response while protected operational logs retain the
specific reason.

## Exercise

Construct a permission matrix for owner, developer, security administrator,
viewer and billing administrator. Add a service account allowed only to create
sessions from one template. Test that its credentials cannot approve its own
requests, discover another project or subscribe to another execution's stream.

## Primary sources

[OWASP session management](../references.md#s14)
