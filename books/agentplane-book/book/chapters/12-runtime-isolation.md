# 12. Build Runtime Profiles for the Actual Threat Model

**Part III — Kubernetes Integration**

A runtime profile combines an image, resource bounds, operating-system settings,
identity and network constraints. Its purpose is to make execution assumptions
explicit and reviewable. It cannot turn a conventional shared container into a
perfect security boundary by adding a reassuring name.

## Separate trusted development from hostile execution

An internal developer running a reviewed test suite in a dedicated cluster is not
the same scenario as a public user submitting arbitrary code. The latter deserves
stronger runtime isolation, admission controls, node separation and independent
security review. A development profile using the default runtime must be labeled
and prevented from becoming a public production profile accidentally.

Kubernetes Pod Security Standards define useful pod-level restrictions. They do
not constitute a complete sandbox for hostile code. Runtime isolation mechanisms
such as gVisor address a different part of the boundary and still have documented
assumptions. [S05](../references.md#s05) [S06](../references.md#s06)

## Make templates immutable after use

A published runtime-template version should bind an immutable image reference,
runtime class, resource limits, workspace policy, network policy and identity
references. Existing sessions retain that version. Editing a template creates a
new version; it does not silently change the meaning of historical evidence.

An image digest identifies bytes, not safety. Signature verification establishes
an expected signing identity or provenance relationship, not that the software is
non-malicious. Vulnerability scanning is another signal, not a proof of absence.
Keep the trust policy, evidence and exceptions reviewable.

## Restrict pod authority

Prefer non-root execution, no privilege escalation, dropped Linux capabilities,
a reviewed seccomp profile, disabled automatic service-account token mounting and
a read-only root filesystem where the runtime permits it. Provide bounded writable
locations for the workspace and temporary files. Do not mount the Docker socket,
host filesystem or connector credential directory into the workload.

Avoid host networking, host process namespaces and privileged mode. A profile
requesting them should fail policy validation, not merely produce a warning in
the interface. Protect the admission path too: a compromised connector should not
be able to bypass restrictions by submitting a different pod shape.

The example renderer in [examples/kubernetes](../../examples/kubernetes/README.md)
requires a real image digest and runtime class. It emits a reviewable teaching
manifest and never applies it. Even a syntactically valid result needs a real
cluster test before use.

## Bound resources beyond CPU and memory

Set ephemeral-storage bounds, execution deadlines, concurrent process limits
where supported, output limits, file-transfer limits and workspace quotas. A
workload can exhaust the platform through logs, file count, network connections
or API requests without using much CPU. Resource limits must be enforced at the
layer that can actually observe and control the resource.

CPU requests help scheduling; they are not measured usage. Memory limits can
cause termination rather than graceful recovery. An OOM event should produce a
clear observed failure reason and preserve the distinction between runtime
failure and user cancellation.

## Runtime images need a maintenance process

Build from reviewed bases, pin dependencies, generate an SBOM and keep rebuild
provenance. Do not leave a floating package installation step in an otherwise
immutable-looking Dockerfile. The runtime server must be compatible with the
adapter and have its own authentication and request-limiting design.

Separate untrusted workspace content from executable runtime infrastructure.
Installing a repository dependency may execute lifecycle scripts; treat that as
execution under the same sandbox restrictions. A package manager is not a safe
exception to the network or credential policy.

## Define removal and quarantine

If a runtime image is revoked, block new sessions from it. Decide whether existing
sessions should be allowed to finish, quarantined or terminated based on the
risk. Preserve evidence and avoid a blanket cleanup that destroys information
needed for investigation. The response should be an explicit policy operation,
not an invisible background replacement of the image digest.

## Exercise

Review a runtime profile for an agent that runs Python tests and reads one private
repository. Remove every permission unrelated to that task. Explain where Git
credentials are available, how long they last, what outbound destinations are
permitted and how a compromised dependency is contained.

## Primary sources

[Kubernetes Pod Security Standards](../references.md#s05) · [gVisor security model](../references.md#s06)
