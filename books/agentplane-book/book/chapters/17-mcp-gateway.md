# 17. Discover Tools Without Trusting Their Descriptions

**Part V — Tool Governance**

A tool registry is an inventory and configuration system. It is not a trust
oracle. A server can report a tool named `read_report` whose behavior is more
powerful than its name suggests. Descriptions and schemas help clients understand
an interface, but authorization must come from platform policy and verified
identity.

## Separate registration, discovery and approval

Registration records the proposed server endpoint, ownership, transport,
authentication mode and credential reference. Discovery contacts the server through
a controlled path and records capabilities. Approval determines whether those
capabilities may be exposed to a particular workload. These are separate state
transitions and should not collapse into “server added.”

A metadata change can alter the meaning of an existing integration. Version the
discovered tool schema and retain a digest. Decide whether new or changed tools
remain blocked pending review. Do not automatically grant a newly discovered tool
because it matches a broad name pattern.

## Discovery creates an SSRF surface

MCP-related metadata and authorization discovery may direct clients to additional
URLs. Validate those destinations, redirects, resolution and TLS behavior under a
versioned security policy. The MCP security guidance discusses token audience,
proxy risks and SSRF in these flows. [S10](../references.md#s10)

Do not fetch arbitrary server metadata from the SaaS network without considering
its internal reachability. In BYOC mode, discovery can occur from a constrained
customer-cluster component. That component still needs protections against cloud
metadata and unrelated private services. Moving SSRF into the customer cluster
is not a mitigation by itself.

## Preserve token audiences

The credential presented by an agent to the gateway is not automatically valid
for the downstream tool service. Validate the inbound credential for the intended
resource and obtain downstream authority through a reviewed mechanism. Avoid
blind token passthrough. Keep actor identity, client identity and service identity
distinct in decisions and logs.

Different MCP protocol versions and authentication extensions may have different
state and transport assumptions. Pin the negotiated version and test it. Do not
copy a claim about sessions or enterprise authorization from an earlier design
into every future integration without rechecking the specification.

## Integrate a gateway instead of inventing a proxy

agentgateway is a candidate data-plane component for this architecture. Its
release-specific documentation should determine which Kubernetes resources,
policies and authorization extension points are actually available.
[S11](../references.md#s11)

Build an adapter that compiles AgentPlane registry and policy intent into the
chosen gateway configuration. Keep product concepts independent from the exact
upstream object shape. A feature that the release cannot enforce must be marked
unsupported or implemented through a supported extension point—not silently
approximated by a weaker rule.

## Keep tool execution out of registry handlers

A registry connectivity test should perform a bounded health or metadata operation,
not execute a dangerous tool to prove the server works. Discovery must not become
an arbitrary command-execution API. Local process-based transports require a
separate sandboxed execution design; do not spawn an untrusted server command
inside the SaaS API process.

Use strict response-size and time limits. Treat server names, descriptions and
error strings as untrusted content in the web console. Do not render arbitrary
HTML or feed tool descriptions into privileged operator instructions.

## Show the effective state

A useful server detail page shows registered owner, endpoint classification,
authentication mode, discovered schema version, approved tools, effective policy,
last successful check and observation age. Displaying only “connected” conceals
whether the server is approved for use and whether the current schema matches the
approved one.

## Exercise

Create a harmless mock server with one read-only tool and one approval-required
tool. Change the latter's schema after approval and verify that the platform
requires a policy decision for the new version. Test a discovery redirect to an
unapproved internal address without contacting any real sensitive endpoint.

## Primary sources

[MCP security best practices](../references.md#s10) · [agentgateway documentation](../references.md#s11)
