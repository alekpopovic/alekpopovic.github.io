# Primary Sources and Verification Notes

Documentation reviewed for this edition on **October 10, 2026**.

These are primary-source pointers, not copies of upstream documentation. AgentPlane service boundaries, APIs, policies and exercises are proposed designs unless the validation report identifies an executed teaching example. A source URL does not establish a tested compatibility matrix. Public documentation may move after this edition.

## S01

**Agent Sandbox documentation**

<https://agent-sandbox.sigs.k8s.io/docs/>

Resource concepts and documentation entry point. Upstream capability is not an AgentPlane implementation claim.

## S02

**Agent Sandbox source repository**

<https://github.com/kubernetes-sigs/agent-sandbox>

Inspect release-specific APIs, runtime server, router and extension resources before implementing adapters.

## S03

**Kubernetes multi-tenancy**

<https://kubernetes.io/docs/concepts/security/multi-tenancy/>

Namespace isolation, shared infrastructure and tenancy tradeoffs.

## S04

**Kubernetes Network Policies**

<https://kubernetes.io/docs/concepts/services-networking/network-policies/>

Additive allow rules, implementation dependencies and network-policy limitations.

## S05

**Kubernetes Pod Security Standards**

<https://kubernetes.io/docs/concepts/security/pod-security-standards/>

Restricted pod configuration is not a complete hostile-code isolation system.

## S06

**gVisor security model**

<https://gvisor.dev/docs/architecture_guide/security/>

Isolation design, assumptions and responsibilities outside the sandbox.

## S07

**PostgreSQL 18 row security**

<https://www.postgresql.org/docs/18/ddl-rowsecurity.html>

RLS semantics, owner bypass, BYPASSRLS and policy behavior.

## S08

**PostgreSQL 18 explicit locking**

<https://www.postgresql.org/docs/18/explicit-locking.html>

Row locks and transaction concurrency. The SQL lab requires independent execution.

## S09

**NATS JetStream concepts**

<https://docs.nats.io/concepts/jetstream>

Persistence and delivery semantics; transport guarantees do not make arbitrary business effects exactly once.

## S10

**MCP security best practices**

<https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices>

Audience separation, proxy risks, discovery SSRF and untrusted tool metadata. Protocol assumptions must be versioned.

## S11

**agentgateway documentation**

<https://agentgateway.dev/docs/>

Verify the deployed release, Kubernetes resources and external-authorization capabilities rather than assuming them.

## S12

**Kubernetes volume snapshots**

<https://kubernetes.io/docs/concepts/storage/volume-snapshots/>

CSI snapshot resources and support requirements; not a general memory checkpoint.

## S13

**Kubernetes Secrets**

<https://kubernetes.io/docs/concepts/configuration/secret/>

Secret objects, projections and access boundaries.

## S14

**OWASP session management**

<https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>

Session lifecycle, cookies and browser attack surfaces.

## S15

**OpenAI AGENTS.md guidance**

<https://developers.openai.com/codex/guides/agents-md/>

Repository instructions for coding agents. This book does not prescribe unverified model IDs or reasoning settings.

## S16

**GitHub Pages custom workflows**

<https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>

Pages artifact deployment, permissions and environment requirements.

## S17

**Mistune usage guide**

<https://mistune.lepture.com/en/latest/guide.html>

The small Markdown renderer used by this book build.

## S18

**CC BY-SA 4.0 legal code**

<https://creativecommons.org/licenses/by-sa/4.0/legalcode.en>

License for original narrative text, diagrams and prompts. License scope is defined in LICENSE.md.

## S19

**MIT License**

<https://opensource.org/license/mit>

License for original program code and configuration examples.

## S20

**OpenTelemetry sensitive-data handling**

<https://opentelemetry.io/docs/security/handling-sensitive-data/>

Minimize, redact and govern telemetry rather than recording everything.

## S21

**Kubernetes Leases**

<https://kubernetes.io/docs/concepts/architecture/leases/>

Coordination mechanism; resource-side fencing remains a separate design requirement.

## S22

**Kubernetes operator pattern**

<https://kubernetes.io/docs/concepts/extend-kubernetes/operator/>

Reconciliation-based extensions and controllers.

## S23

**Go traversal-resistant file APIs**

<https://go.dev/blog/osroot>

Root-relative operations and filesystem race considerations; API availability depends on Go version.

## S24

**GitHub Actions secure use**

<https://docs.github.com/en/actions/reference/security/secure-use>

Least-privilege workflows, untrusted inputs and immutable action references.
