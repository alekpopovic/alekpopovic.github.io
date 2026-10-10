# 16. Broker References, Not Customer Secret Values

**Part IV — Safe Execution**

The control plane should store the identity of a credential provider and an
approved binding, not the customer's secret value. A binding describes who may
request which credential for which workload, with which audience, scope and
lifetime. Resolution happens in the customer environment.

## Prefer identity over copied credentials

A workload identity lets a runtime obtain authority based on its authenticated
workload context. Where a provider supports it, this avoids copying permanent
keys into application configuration. The exact trust conditions matter: issuer,
subject, audience, project mapping and maximum lifetime must all be constrained.
A broad role trust relationship can turn short-lived credentials into broad
short-lived compromise.

Kubernetes Secrets and projected credentials have specific access and storage
properties. Their existence is not proof that only the intended process can read
them. Kubernetes documents the responsibilities around Secret handling and
projections. [S13](../references.md#s13)

## Define a binding contract

A proposed binding contains organization, project, provider identifier, approved
resource reference, allowed runtime-template versions, delivery mechanism,
maximum lease and revocation behavior. It must not contain a secret value or a
free-form instruction to fetch any arbitrary provider path.

Do not let a caller replace a approved binding with another provider identifier
from the same organization without authorization. Scope checks apply to every
reference. The connector validates the binding against customer-local policy in
addition to the control-plane decision.

## Delivery is a security choice

Projected files, CSI mounts, local broker sockets and environment variables have
different exposure characteristics. Prefer a mechanism that supports rotation,
limited access and cleanup for the runtime. Environment variables are easy to
inherit and accidentally print; file delivery is not automatically safe either
if other processes can read the file or if it is included in a snapshot.

Place credentials outside the persistent workspace where possible. Use an
appropriate ephemeral location and permissions. Exclude credentials from archive
exports and diagnostic bundles. A filesystem snapshot can preserve secrets that
were temporarily written to a persistent volume, so storage policy and identity
policy cannot be designed independently.

## Lease metadata is not revocation

A platform can record that a lease is revoked while the downstream provider
continues accepting an already-issued credential. State the provider's actual
revocation behavior. Some credentials become unusable only when they expire;
others can be invalidated earlier. The broker must not promise instantaneous
revocation unless the full path supports and tests it.

Keep maximum lifetime short enough for the risk model without creating a renewal
storm. A disconnected cluster needs a rule for renewal failure. Do not silently
substitute a permanent fallback credential because the normal provider is down.
For sensitive actions, inability to obtain a valid credential should stop the
action.

## Keep connector authority separate

The connector's credential authenticates management traffic. It must never be
mounted into an agent sandbox. Kubernetes service accounts used for management,
runtime execution and tool access should be separate where their authorities
differ. A single powerful account reused everywhere makes lateral movement much
easier to achieve and harder to explain.

A customer administrator can often read or replace cluster workloads. Document
that trust assumption. BYOC can keep infrastructure ownership with the customer,
but it does not inherently provide cryptographic secrecy from the customer's
administrators or all cloud operators.

## Audit without leaking the credential

Useful events include binding approved, lease requested, lease issued, renewal
failed and revocation requested. Record safe provider identifiers, lease IDs,
expiration and outcome. Avoid secret values, authorization headers and raw
provider error bodies. Even a secret path may reveal business context, so decide
which metadata is exposed to developers versus security administrators.

## Exercise

Design a Git read-only credential binding for one repository. State how the
runtime obtains it, where it appears in memory or files, whether it can enter a
snapshot and what happens during provider outage. Then test that another project
cannot reference the binding even when it knows the binding ID.

## Primary sources

[Kubernetes Secrets](../references.md#s13)
