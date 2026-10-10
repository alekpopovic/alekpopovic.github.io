# 23. Deploy and Upgrade Without Crossing the Trust Boundary

**Part VII — Product and Operations**

Deployment design should preserve the architecture's authority boundaries. Keep
customer execution workloads out of the SaaS control-plane cluster. Separate
control-plane packaging from customer-cluster components so installation does not
silently grant unrelated capabilities.

## Two installation packages

The control-plane package contains the API, worker, connector gateway, web assets
and required configuration references. PostgreSQL, transport and object storage
are external production dependencies or explicitly chosen managed services. The
customer package contains the connector, policy operator and approved upstream
integrations. Optional features stay optional.

Do not bundle a development database and message broker into the production
chart as an invisible default. Likewise, do not install a cluster-wide runtime,
CNI or certificate authority merely because a user asked to connect an existing
cluster. These are customer infrastructure decisions with substantial impact.

## Pin artifacts and verify policy

Release images should use immutable references and retained provenance. Chart
values should reference existing Secrets or approved secret integrations rather
than contain plaintext credentials. Enforce security contexts, resource bounds,
health probes and network policy in rendered manifests.

A successful Helm template render proves syntax and templating behavior, not
cluster compatibility. Run schema checks, admission tests and a real install and
upgrade exercise against the intended versions. Keep CRD lifecycle separate from
ordinary deployment lifecycle; deleting a CRD can remove its custom resources.

## Reference AWS deployment

An AWS reference design can use EKS for the control services, a managed PostgreSQL
database, object storage for permitted evidence exports, an external signing
integration and workload identities. Use private database networking, constrained
security groups, encrypted storage and restricted administrative access.

NAT gateways, private endpoints, load balancers, multi-zone capacity and telemetry
retention affect cost. This book provides a design framework, not current pricing
or a tested Terraform stack. Obtain prices and verify provider support when
implementing the deployment. Do not claim a region or engine version is supported
without checking the current provider documentation.

## Migrate databases with expand and contract

Add compatible columns and behavior before removing old fields. During rolling
upgrades, old and new API and worker versions may coexist. A migration that works
only when every process changes simultaneously is a deployment risk.

Keep schema ownership and application access separate. Back up before risky
changes and test restoration. A down migration is not a credible rollback when it
would discard data introduced by the new version. In such cases, document forward
repair or restore procedures explicitly.

## Drain long-lived connections

A connector gateway cannot be upgraded like a stateless page server without
considering open streams. Stop accepting new streams, notify or drain existing
connections, persist ownership transitions and let connectors reconnect with
backoff. Use fencing and operation identity so overlap does not duplicate work.

A PodDisruptionBudget can reduce some voluntary disruption, but it does not prove
continuous availability. Node failure, configuration errors and incompatible
protocol changes remain possible. Measure reconnect and recovery behavior in the
actual deployment.

## Keep release authority explicit

Build, test, sign, publish and deploy are separate actions. A coding agent can
prepare artifacts without receiving production publishing credentials. Protected
release environments, scoped workload identity and least-privilege workflows
reduce the consequences of a compromised build step.

The book's own GitHub Pages workflow follows the same separation: pull requests
validate the publication; deployment uses a separate job with Pages permissions.
GitHub documents the required Pages artifact and environment flow.
[S16](../references.md#s16)

## Exercise

Write an upgrade plan in which the API is upgraded first, the worker second and
half the connectors remain on the prior protocol. State the supported overlap,
rollback trigger and commands that must remain safe throughout. Include a
certificate rotation occurring during the same interval.

## Primary sources

[GitHub Pages custom workflows](../references.md#s16) · [GitHub Actions secure use](../references.md#s24)
