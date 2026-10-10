# 11. Integrate Agent Sandbox Through a Capability Adapter

**Part III — Kubernetes Integration**

Agent Sandbox provides a core `Sandbox` resource and extension concepts including
`SandboxTemplate`, `SandboxClaim` and `SandboxWarmPool`. Its source repository
also distinguishes orchestration from lower-level runtime isolation. AgentPlane
should integrate these capabilities rather than relabeling ordinary Pods as a
complete agent security system. [S01](../references.md#s01)
[S02](../references.md#s02)

## Do not infer API compatibility from a feature name

“Execute a command” may involve a runtime server inside the sandbox, an SDK, a
router and the Kubernetes resource managing the workload. These components have
separate responsibilities. A working controller does not imply that an arbitrary
OCI image exposes the execution or filesystem API expected by the SDK.

Record a compatibility tuple: Kubernetes server, sandbox CRD release, controller,
extensions, router, runtime server, client SDK, container runtime and CNI. Test the
tuple that you intend to support. Reading documentation does not populate a
successful compatibility matrix.

## Create a narrow internal interface

The application-facing adapter should express product operations without leaking
upstream object structures:

```text
CreateFromTemplate(scope, templateVersion, operationID)
Observe(resourceIdentity)
Terminate(resourceIdentity, intentVersion)
Capabilities(clusterIdentity)
StartExecution(executionIdentity, request)
QueryExecution(executionIdentity)
```

This is interface pseudocode. Optional operations such as hibernation, snapshots
and file transfer belong behind explicit capability checks. A missing capability
returns a typed unsupported result. It must not trigger an unsafe fallback such
as privileged `kubectl exec` under a broad service account.

## Keep orchestration and execution separate

The Kubernetes adapter creates and observes sandbox resources. The runtime
adapter performs allowed operations inside them. The router transports requests;
it is not automatically an authorization policy engine. Validate which layer
checks identity, scope, timeout and request size. Do not assume that because an
SDK is official, every product-level requirement is already enforced.

Restrict runtime endpoints to the appropriate caller identities and networks.
A runtime API that accepts arbitrary commands is a privileged interface even
when it listens only inside the cluster. A compromised neighboring workload must
not be able to call it directly.

## Define support states precisely

Use separate states for discovered, compatible, configured and verified. A CRD
may be present while its controller is unavailable. A runtime class may exist
without any schedulable nodes configured to use it. A snapshot class may exist
without a working driver. Capability discovery is a starting observation; a
successful probe and workload test provide stronger evidence.

Expose these distinctions in onboarding. For example, “runtime API not verified”
is more useful than a generic cluster-connected badge. It tells the operator
which acceptance test is still missing.

## Handle upgrades as compatibility changes

Pin the release artifacts used by an application environment. Capture checksums
and inspect CRD schemas before applying updates. New fields, renamed status
conditions or changed runtime endpoints can break an adapter even when the user
journey sounds unchanged. Maintain fixtures from supported releases and run
contract tests against each intended version.

An adapter can support multiple release families, but each additional family has
maintenance cost. Prefer a narrow tested range over an untested promise to work
with every Kubernetes cluster. If an old version is incompatible, stop new
provisioning while preserving a documented path to observe and terminate existing
sessions safely.

## Treat warm pools and hibernation carefully

Warm pools reduce some startup work by preparing capacity in advance. They do not
eliminate policy binding, identity assignment or readiness checks. A pooled
workspace must not carry credentials or files from a previous tenant. Prefer
fresh unclaimed capacity over recycling arbitrary used sessions.

Hibernation semantics depend on the upstream release and runtime. Do not promise
process-memory preservation simply because storage persists or a resource can
scale to zero. Represent restartable workspace suspension separately from any
verified process checkpoint capability.

## Exercise

Complete the compatibility worksheet in the appendices for one chosen release.
Identify the exact runtime image providing command execution. Write a test that
creates a sandbox successfully but fails runtime readiness, and confirm that the
product does not mark the session ready for execution.

## Primary sources

[Agent Sandbox documentation](../references.md#s01) · [Agent Sandbox source repository](../references.md#s02)
