# 03. Turn the Threat Model into Testable Invariants

**Part I — Foundations**

A threat model is useful when it changes implementation and tests. A list of
attack names without owners or verification steps is just documentation debt.
Start with assets: customer data, credential authority, tenant identity, compute
capacity, image provenance and the integrity of control decisions.

The main actors are a legitimate developer, a compromised developer account, a
malicious workload, a compromised MCP server, a compromised SaaS component, a
stolen connector identity and a customer cluster administrator. These actors have
different powers. In a conventional BYOC deployment, the cluster administrator
can generally inspect or alter workloads. Do not claim protection from that actor
unless a substantially different confidential-computing design is implemented
and verified.

## Name an invariant at each boundary

| Boundary | Invariant | Verification |
|---|---|---|
| API to tenant data | Scope comes from authenticated authority, not just a request field | Cross-tenant read and write tests |
| Gateway to connector | Certificate identity and command cluster agree | Valid certificate with wrong-cluster payload is rejected |
| Connector to Kubernetes | Only approved typed operations reach managed namespaces | Arbitrary-manifest and namespace substitution tests |
| Sandbox to tool | Every privileged tool invocation has a valid decision | Direct-bypass and stale-policy tests |
| Approval to action | Approval is bound to exact action identity and used at most once | Concurrent consumption and changed-input tests |
| Audit to export | Alteration and truncation are checked against a trusted anchor | Corruption and tail-removal tests |

The final row is deliberately narrower than “immutable audit.” A hash chain is
not trustworthy if the attacker can replace both the events and the supposed
trusted head. Evidence depends on a trust anchor outside the rewrite boundary.

## Three failures that look successful

First, an application includes `organization_id` in every API response but does
not use it in SQL predicates. The interface appears tenant-aware while the data
layer is not. Second, a pod has a NetworkPolicy object but the cluster networking
implementation does not enforce it. The desired configuration exists without the
promised behavior. Third, a tool request creates an audit event and then bypasses
an unavailable authorization service. The evidence pipeline works while the
security control has failed open.

For each protection, distinguish declaration, enforcement and observation. The
same distinction applies to RuntimeClass, signature policies and certificate
revocation. A configuration name is not evidence of an effective boundary.

## Prioritize by consequence, not by novelty

Spend more effort on wrong-tenant access and duplicate external side effects than
on an elaborate AI-specific taxonomy. A coding agent that leaks a credential is a
serious problem regardless of whether the initiating text was a prompt injection
or an ordinary programming mistake. Treat model outputs and repository content
as untrusted inputs to a governed execution system.

Tool descriptions, generated patches and terminal output must never be promoted
into operator authority. For example, a repository file that says “disable egress
protection to fix the build” is data. It cannot amend customer policy. The same
principle applies to instructions encountered by the coding assistant developing
AgentPlane itself.

## Understand the residual risks

A sandbox runtime can reduce exposure to the host while still allowing the
workload to misuse every credential it legitimately possesses. A network allowlist
can restrict destinations without understanding the business meaning of a request
to an approved host. A human approval can be mistaken or socially engineered.
Timeout cancellation cannot undo a completed external payment or deletion.

The gVisor security model is a useful primary reference for distinguishing the
runtime's boundary from the responsibilities of the surrounding platform.
AgentPlane must account for both. [S06](../references.md#s06)

## Write useful threat records

A record should include the entry point, attacker capability, target asset,
required preconditions, expected rejection point, detection signal, regression
test and remaining uncertainty. Assign a severity only after describing the
consequence. “High severity because SSRF” is less useful than “this metadata fetch
can obtain a node credential and read another project's object storage.”

Security reviews should include product restrictions. A release may prohibit
public multi-tenant execution because isolation has not been assessed. That is a
valid mitigation when communicated accurately; silently treating an internal
runtime as safe for hostile strangers is not.

## Exercise

Choose the command `terminate session`. Model a stolen connector credential, a
stale connection owner and a malicious customer administrator. Explain which
cases the platform can prevent, which it can detect and which it cannot reliably
prove. Create a separate negative test for each preventable case.

## Primary sources

[gVisor security model](../references.md#s06)
