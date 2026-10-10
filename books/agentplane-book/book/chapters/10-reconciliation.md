# 10. Use Kubernetes Reconciliation Without Expanding Authority

**Part III — Kubernetes Integration**

A controller observes a resource and moves dependent state toward its desired
configuration. Reconciliation must tolerate repeats, partial progress and stale
observations. The operator pattern provides a useful structure for AgentPlane's
cluster-local policy resources. [S22](../references.md#s22)

## Own only what the product adds

Upstream sandbox resources already model much of workload lifecycle. AgentPlane
needs additional intent such as runtime governance, egress constraints, secret
references and tool policy bundles. A proposed API group might contain
`RuntimeProfile`, `EgressPolicy`, `SecretBinding` and `PolicyBundle`. These names
are design examples, not installed CRDs in this repository.

Avoid a catch-all resource containing arbitrary Kubernetes YAML. It would make
the connector a remote deployment administrator and defeat the typed command
boundary. A small schema makes invalid and dangerous requests easier to reject.

## Separate spec, status and observation

Spec describes the requested state. Status reports what the controller observed.
Include an observed generation and conditions with stable reason codes. A useful
condition distinguishes invalid policy, unsupported provider, dependency missing,
compilation pending, applied and degraded. Do not reduce every condition to a
single green/red field.

A newer spec should not inherit an older successful condition without an updated
observed generation. The SaaS must compare versions before showing policy as
active. Otherwise a failed security update can look applied because a previous
version succeeded.

## RBAC is necessary but not sufficient

Namespace-scoped roles are safer than blanket cluster authority, but Kubernetes
RBAC does not generally restrict create requests by arbitrary object content.
A role allowed to create Pods in a namespace can be powerful. Admission policies,
namespace ownership and controller-side validation must limit the configuration
that can actually be created.

Similarly, watching cluster-scoped resources can reveal information beyond the
project. Request only the discovery fields needed to establish capability, and
report a sanitized summary. Separate inventory access from mutation authority
where practical. Do not grant `cluster-admin` to simplify installation.

## Reconcile safely

Use deterministic names derived from stable IDs rather than user-supplied names.
Validate ownership before updating an existing object. If an object with the same
name belongs to another controller or tenant, report a conflict instead of
adopting it silently. Avoid broad label selectors whose membership a workload
can change.

Patch narrowly. When multiple controllers touch an object, define field ownership
and conflict handling. Do not continuously overwrite customer-owned fields merely
because they differ from a cached SaaS representation. Drift can be intentional,
unauthorized or a result of another controller; the recovery action depends on
which case occurred.

## Finalizers are operational commitments

A finalizer can delay deletion while cleanup is pending. It can also block a
namespace indefinitely when its controller is unavailable. Use finalizers only
where the cleanup requirement is real. Document timeout, escalation and manual
removal procedures, including the risk of leaked resources.

Never automatically remove a finalizer just to make a dashboard look healthy.
The correct user-visible state may be “cleanup requires operator action.” A
retained volume with customer data is not an ordinary disposable cache.

## Test beyond object creation

Unit tests cover policy compilation and deterministic naming. Controller tests
cover repeated reconciliation, observed-generation handling, stale resources,
missing dependencies and deletion. A real cluster is required to verify admission,
RBAC, network enforcement and runtime behavior. A fake API server cannot prove
that a packet was denied or that a syscall was isolated.

## Exercise

Design the status conditions for an egress policy that requests domain filtering
on a cluster without that capability. The policy must not silently degrade to a
CIDR rule. Explain how the API, connector, operator and UI all preserve that
failure rather than converting it into a successful deployment.

## Primary sources

[Kubernetes operator pattern](../references.md#s22)
