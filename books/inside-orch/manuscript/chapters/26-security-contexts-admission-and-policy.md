# Chapter 26 - Security Contexts, Admission, and Policy

Atlas API should run with fewer host privileges than the process managing Docker. That requirement has two parts: refuse dangerous workload intent, and carry accepted security fields into actual container creation. A policy rejection is useful evidence, but it is not the same observation as inspecting an Engine HostConfig. We need both field tracing and a clear limit on what a shared worker can isolate.

This chapter assumes service validation, agent DTOs and the Docker adapter. You will identify supported security-context fields, follow them through the ordinary service task path, and distinguish built-in admission from proposed external policy engines. The Atlas failure scenario is an unsafe manifest submitted through a second entry point after an operator believes the CLI already validated everything.

## Container Security Fields That Reach Docker

For ordinary service tasks, ListAssignedTasks copies service.Spec.SecurityContext into the agent payload. ensureTask calls dockerSecurityContext and places the resulting value in ContainerSpec.Security. Unlike the missing resource-enforcement edge discussed earlier, these security fields have an explicit mapping through the agent. The mapping includes user, read-only root filesystem, privileged mode, added/dropped capabilities, host network, host PID and host-path mounts. [Claim ch26.fields](../../validation/evidence/ch26.json).

[internal/agent/agent.go, lines 323–333](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L323-L333) at the locked revision.

```go
	return orchdocker.SecurityContext{
		User:                   context.User,
		ReadOnlyRootFilesystem: context.ReadOnlyRootFilesystem,
		Privileged:             context.Privileged,
		CapAdd:                 append([]string(nil), context.CapAdd...),
		CapDrop:                append([]string(nil), context.CapDrop...),
		HostNetwork:            context.HostNetwork,
		HostPID:                context.HostPID,
		HostPathMounts:         mounts,
	}
}
```

The Engine adapter sets Config.User and HostConfig.Privileged, ReadonlyRootfs, CapAdd and CapDrop. It adds bind mounts, selects host network mode when requested and selects host PID mode when requested. The cap-drop helper defaults an empty configured list to NET_RAW. This is a source-derived default worth naming precisely rather than inferring the daemon's unrelated defaults. File access inside the image can still fail when the chosen user lacks permissions, so accepted configuration is not proof the application will start successfully.

A read-only root filesystem applies to that filesystem boundary. Writable bind mounts remain writable if their own mode permits it. Dropping capabilities narrows particular process privileges; it does not remove the agent's authority over the Docker socket or establish a separate kernel for each tenant. A non-root user can also execute vulnerable application code. These fields have concrete value without being a complete hostile-code sandbox.

Host-path mounts deserve particular care. The built-in rule cleans a path and requires equality with an allowed prefix or a child separated by a slash. A raw substring match would incorrectly accept similarly named sibling directories. The code's lexical prefix check is still not a general guarantee against every host filesystem alias or administrator-selected dangerous path. Keep an allowlist narrow and understand what data is visible through an accepted mount.

For the safe lab, the security field path is inspected and fake creation tests supply deterministic coverage. Do not run a privileged container merely to demonstrate rejection: a rejected intent can be tested entirely in-process. Actual Engine inspection of a harmless accepted user/read-only/cap-drop combination would be a separate local observation. No such host inspection is inferred from an admission unit test.

## Admission Order and Policy Decisions

Admission's Request includes actor, operation, namespace, spec and ClusterPolicy. Evaluate accumulates Violation values containing field, rule and message. Controller.Admit returns an Error with operation, namespace and that collection, and optionally records a rejection through an AuditSink. This creates an error shape that callers can inspect without parsing one human sentence. [Claim ch26.admission](../../validation/evidence/ch26.json).

[internal/admission/admission.go, lines 75–87](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission.go#L75-L87) at the locked revision.

```go
func (controller *Controller) Admit(ctx context.Context, request Request) error {
	violations := Evaluate(request.Spec, request.Policy)
	if len(violations) == 0 {
		return nil
	}
	if controller != nil && controller.sink != nil {
		controller.sink.RecordAdmissionRejection(ctx, Rejection{
			Actor: request.Actor, Operation: request.Operation, Namespace: request.Namespace,
			Service: request.Spec.Name, Violations: violations,
		})
	}
	return &Error{Operation: request.Operation, Namespace: request.Namespace, Violations: violations}
}
```

The evaluator covers required CPU/memory requests and limits, privilege/host namespaces, capabilities, host paths, approved registries, digest/mutable/latest rules, healthcheck presence and replica/public-port ceilings. It is deterministic code with supplied inputs. It does not execute Rego, contact a remote policy endpoint or scan an image. Actor and operation are useful request context even where the present evaluator's rules depend mainly on spec and static policy.

Follow the actual create order rather than relying exclusively on the design document. CreateService resolves image metadata, validates the candidate, calls admission, applies resource defaults through NormalizeServiceSpec, validates again, then enters the state lock for namespace/reference/quota checks and mutation. Consequently a require-resource rule can reject a missing explicit request before normalization supplies a default. The design's phrase normalized candidate must be qualified by this real sequence.

A structurally invalid manifest can fail before admission and need not produce a policy-violation collection. A structurally valid but disallowed privileged request reaches the policy branch. A missing secret reference or quota exhaustion occurs later and has its own error type. Those are different acceptance boundaries. Keep tests for each rather than expecting every rejected manifest to produce the same rule identifier.

The API converts admission.Error into a structured rejection with violations, operation and namespace. Human-facing Error() emphasizes the first violation, while the structured collection preserves multiple findings. A UI should display stable field/rule values and useful messages, not treat message punctuation as a machine contract. Rejection auditing records rule context rather than raw secret values.

The failure window is a caller that bypasses the checked mutation method. Local CLI parsing alone cannot protect an HTTP client that submits a candidate directly. Conversely, a central method protects several ordinary entry points only if those callers actually invoke it. Every new mutation path needs the same trace; the presence of an admission package does not automatically intercept arbitrary map changes.

## The Same Checks Across Entry Points

The CLI-assisted deployment parses supported YAML and submits the resulting service request. The API calls the control-plane service method. GitOps receives cli.ParseDeploy as its parser and applies through ApplyService, which uses the checked create/update paths. These shared calls are stronger evidence than three independent copies of loosely equivalent validation code. They also make one policy change visible to several ordinary entry points. [Claim ch26.entry-points](../../validation/evidence/ch26.json).

Scale and rollout construct candidates from current service intent, change the relevant field and invoke admission before committing the operation. The focused control-plane test creates an allowed service, rejects a scale above the policy maximum and rejects a latest-image rollout. It checks structured rule information for scale and failure audit records for both operations. The [actual focused suite](../../validation/labs/ch26/focused-tests.json) passed these rejection assertions alongside policy/admission tests.

That result should be stated at its actual scope. It demonstrates the selected built-in rules and tested mutation paths using in-process state. It does not prove every conceivable endpoint or future controller cannot bypass admission. Nor does it prove accepted resource limits reach Docker: chapter 5's field-path concern remains even if policy requires the declaration. Presence validation and runtime propagation answer different questions.

GitOps has an additional exception that matters for this boundary. Its ordinary fetch/parse/apply path uses shared admission, but MemoryService.GitOpsStatus can auto-revert a drifted service by restoring stored DesiredSpec directly. That branch does not call Admit again in the inspected method. Chapter 30 examines its implications. Therefore describe the checked ordinary apply path precisely and avoid a universal claim that every internal state restoration reruns current policy.

Finite jobs also have a distinct CreateJob path. Their JobSpec validation and resource defaulting are not the ordinary ServiceSpec admission sequence. A service policy test cannot certify every Job field or workload type. If an organization needs the same policy across all workloads, first define the common candidate contract, identify the missing paths, and add independently tested checks rather than broadening the documentation by analogy.

| Boundary | What it checks | What it does not establish |
| --- | --- | --- |
| YAML/domain validation | Supported structure and field relationships | Organization policy compliance |
| Built-in admission | Candidate against static policy rules | Runtime field propagation |
| Agent/Engine mapping | Accepted security options reach create arguments | Full host isolation |
| Logical namespace access | Selected object visibility and roles | Independent worker kernel/network |

The table is a map of responsibilities, not a ranking of security strength. An attacker can exploit a gap between any two rows. For Atlas, record both the rejected candidate's stable violation and the source path of the accepted security field. That makes the evidence actionable: one test protects admission, another protects propagation, and the operational deployment still owns the host trust decision.

## What Admission Does Not Isolate

The worker agent can change Docker resources, and the daemon is a powerful host boundary. A policy that denies privileged mode prevents one dangerous declaration; it does not revoke the agent's daemon authority. Shared networking, kernel behavior, mounted data and resource competition remain relevant. Logical namespaces and declarative constraints should not be sold as certification for mutually hostile tenants.

The repository's policy-engine design proposes dynamic providers, revisioned bundles and an OPA-compatible evaluator boundary. Those ideas are useful architecture work. The inspected MVP contains built-in Go rules and no active external Rego execution in this path. A future adapter would need bounded requests, authenticated policy material, explicit outage behavior and versioned decision evidence. None of those guarantees follows from writing an interface name in a design document.

A fail-closed decision can protect the acceptance boundary while reducing deployment availability when its dependency is unavailable. A fail-open decision can preserve deployments while weakening the intended control. Such tradeoffs must be explicit, scoped and tested. The present local evaluator avoids that remote dependency, but it still relies on a correctly configured static policy and on all relevant callers using it.

History distinguishes implementation from proposal. [a140c4190af17969d207b5738cc7527e4ad96075](https://github.com/alekpopovic/orch/commit/a140c4190af17969d207b5738cc7527e4ad96075) adds container security policy and related runtime fields. [9e78fed31df03d7a985a9f4ceae4770739b05014](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014) batches admission/API policy and namespaces. Their changed hunks explain actual evolution; the broader policy design remains classified separately.

Reproduce the safe Atlas rejection lab from the disposable source module with Go 1.25 and the environment contract. No Docker, PostgreSQL or external policy server is needed. The checked command is:

```sh
go test ./internal/policy ./internal/admission ./internal/controlplane \
  -run 'Test.*(Policy|Admission|Security)' -count=1 -v
```

Before execution, predict that a privileged candidate under default policy is denied, a scale beyond the configured maximum yields replicas.maximum, and a latest rollout under the relevant rule fails without changing accepted intent. Read the actual test assertions rather than assuming every possible rule was selected by the expression. The linked log records the cases that ran. Cleanup is process exit; no unsafe container was created to obtain a denial.

For an optional extension, submit the same valid-but-disallowed service through CLI, direct API and a local committed GitOps fixture. Assert matching stable rules and unchanged service intent, while preserving distinct request/actor context. Use disposable identities and no secret-bearing bodies. Also include a previously allowed stored GitOps desired state under changed policy, because it exposes the internal restoration exception rather than merely repeating the happy path.

## Exercises

1. Trace read-only root filesystem from ServiceSpec to the Engine create arguments. Why does a writable bind mount remain a separate concern?
2. Why can require_resource_requests reject a candidate before defaults exist? Identify the real ordering rather than quoting the design's normalized-candidate phrase.
3. Compare a malformed YAML request, a privileged policy denial and a quota rejection. Which should produce admission violations?
4. Explain why passing scale/rollout admission tests does not certify every Job or GitOps restoration path, or establish a hostile-tenant sandbox.

[Worked answers](../solutions/ch26.md) connect the field path and acceptance sequence. The defensible promise is built-in rejection on inspected mutation paths plus explicit Engine mappings, with host trust and unintegrated policy proposals kept visible.
