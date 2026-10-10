# 15. Make Network Policy an Enforced Property

**Part IV — Safe Execution**

A deny-by-default network design begins with the absence of permissions, then
adds narrowly justified paths. It does not begin with unrestricted internet
access and a growing list of suspicious hosts. The cluster's networking
implementation must actually enforce the requested policies.

## Understand standard policy semantics

Kubernetes NetworkPolicy is based on additive allow rules. Applicable policies
combine their allowances; a deny-all policy does not override another policy
that allows traffic. The API also depends on a network implementation that
supports enforcement. These details are central to AgentPlane's compiler and
acceptance tests. [S04](../references.md#s04)

The teaching manifest in [examples/kubernetes](../../examples/kubernetes/README.md)
creates a default-deny policy in a dedicated lab namespace. It is not proof of
packet filtering until tested with a policy-enforcing CNI. Inspect all policies
selecting the workload, not just the one created by AgentPlane.

## Design a policy compiler

The product policy describes allowed services, CIDRs, ports and optionally domain
names. The compiler targets a known provider. Standard NetworkPolicy does not
supply general domain-name enforcement. A domain rule therefore requires a
verified provider-specific capability or a controlled application proxy. If the
required provider is absent, reject the policy rather than replacing a domain
with an unstable IP snapshot and claiming equivalent protection.

Separate compilation success from enforcement readiness. The controller can
report that manifests were accepted while a later probe reports a blocked or
unexpectedly reachable destination. Keep both observations.

## DNS is necessary but not automatically harmless

A typical workload needs cluster DNS. Allowing access to the resolver does not
mean arbitrary domains are allowed for application traffic. It also does not
prevent DNS-based data exfiltration. Where this matters, use a constrained DNS
policy or proxy and test its behavior with the actual resolver and CNI.

Avoid broad namespace-only DNS rules that also authorize unrelated workloads in
a system namespace. Select the intended resolver endpoints and ports. Node-local
DNS, host networking and provider-specific packet translation may require a
different verified configuration. Do not copy a manifest across clusters without
checking the path it actually selects.

## Block infrastructure escape paths

Cloud metadata, link-local addresses, loopback behavior, private networks and the
Kubernetes API need explicit treatment. Include IPv6 and IPv4-mapped IPv6 when
relevant. HTTP redirects and DNS changes can turn a seemingly approved URL into
a request to a different destination.

A public MCP endpoint may legitimately be hosted behind changing infrastructure.
That is a reason to use a suitable enforcement layer, not to allow all outbound
traffic. Restrict the gateway's own discovery requests as well as sandbox traffic;
an SSRF problem in the gateway can bypass a perfectly configured sandbox policy.

## Make the gateway path unavoidable

Tool authorization is ineffective if the workload can reach the tool directly
using the same credentials. Restrict network reachability and downstream
credentials so privileged traffic must traverse the intended policy boundary.
The tool server should validate its own caller identity too. Do not rely only on
an HTTP proxy environment variable: untrusted code can ignore it.

Domain allowlists are not business authorization. An approved host can expose
many paths, tenants and APIs, and may itself be compromised. Apply tool-level
permissions and resource-specific credentials in addition to network constraints.

## Update policies without an unintended open interval

Creating a permissive replacement before deleting the old policy can expand
access because rules are additive. Design rollout ordering and temporary
restrictions deliberately. A tightening update may require a gate that prevents
new execution until the target version is active. Test existing connections,
because enforcement behavior for established flows can vary by implementation.

## Exercise

Run the network lab only in a disposable cluster. Prove an allowed service works,
an unapproved service fails and an unrelated broad allow policy changes the
result. Remove that policy and repeat. Record the CNI, resolver arrangement,
policy objects and observed traffic rather than only the `kubectl apply` output.

## Primary sources

[Kubernetes Network Policies](../references.md#s04)
