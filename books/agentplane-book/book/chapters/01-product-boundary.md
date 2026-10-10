# 01. Choose a Product Boundary Before a Technology Stack

**Part I — Foundations**

The useful product is not “Kubernetes with an AI label.” It is a reliable answer
to a customer question: *Can our software agents perform useful work without
receiving unrestricted access to our infrastructure?* AgentPlane addresses the
execution and governance part of that question. It does not decide whether a
model's business reasoning is correct.

Consider a fictional customer, Northstar Analytics. Its internal agent clones a
repository, runs tests, prepares a report and requests access to a reporting tool.
Northstar already owns a Kubernetes cluster. It wants predictable isolation,
limited credentials and an explanation of who authorized each tool operation.
The platform is successful when Northstar can operate this workflow with less
custom glue and a clearer security review. The example is a design scenario, not
a customer reference.

## The first supported journey

A project administrator installs a connector in a dedicated development cluster.
A developer selects a reviewed runtime template, creates a session and executes a
harmless test command. The session cannot reach an arbitrary internet endpoint.
It can reach one approved tool through a gateway. A sensitive call requires a
second person's approval. The developer terminates the session and obtains a
metadata-only activity report.

This single journey is a better first milestone than a menu containing every
possible agent feature. It crosses the important boundaries: human identity,
tenant authorization, cluster identity, workload isolation, network policy,
tool identity and lifecycle cleanup. Each crossing becomes a test later.

## What the first release excludes

Do not include model training, a GPU scheduler, a general-purpose hosting service
or an unreviewed marketplace in the first release. These expand the trust and
operational surface without being necessary for the journey above. Keep managed
public execution separate from BYOC. A service executing arbitrary code from
unrelated strangers is a different risk profile from an internal team using its
own dedicated cluster.

Avoid promising “zero data access.” Commands, filenames, tool inputs and output
streams are data too. A control-plane relay that transports them can observe
plaintext unless an additional end-to-end design prevents that. The more honest
initial promise is that workspace storage and secret-provider access remain in
the customer environment, while a documented set of metadata and optional
interactive streams passes through the control plane.

## Define acceptance by behavior

| Requirement | Observable acceptance condition |
|---|---|
| Tenant isolation | A project-B credential cannot read or mutate a project-A session |
| Bounded execution | A timed-out process is canceled and its uncertain outcome is visible |
| Network control | A request to an unapproved destination fails in the actual CNI environment |
| Tool governance | A request without the required approval never reaches the tool server |
| Recoverability | A connector restart does not blindly repeat an unknown execution |
| Cleanup | Termination has a visible pending state until resources are confirmed removed |

Do not accept a screenshot as evidence for these conditions. A screenshot shows
an interface at a moment in time. Tests and retained observations establish the
behavior behind it.

## A small deployment model

Use Go for API and cluster-facing components, PostgreSQL for durable application
state and Angular for the management console. These are project choices, not
claims of universal superiority. Keep application-domain modules separable even
when the API and worker share a process during early development. Deploy the
connector and operator independently because they live across a trust boundary.

NATS JetStream becomes useful when command distribution and event throughput
justify a dedicated transport. The first local proof can use a PostgreSQL outbox
and a simple worker. Preserve the message contract so that transport can change
without changing authorization or lifecycle semantics. Operational simplicity is
a design benefit, provided it does not erase the trust boundaries.

Upstream Agent Sandbox supplies sandbox-oriented Kubernetes resources. Its
controller and the chosen runtime still require a deployment-specific integration
review. AgentPlane should add policy and product semantics, not duplicate every
upstream feature under a different name. [S01](../references.md#s01)

## Validate the product without invented market numbers

Interview teams that already execute agent-generated code. Ask which actions
require manual approval, where credentials currently live, how they investigate
failures and what they cannot permit an external service to observe. Request an
example workflow with synthetic data. A willingness to run that workflow in a
pilot is more meaningful than a positive response to a feature list.

A pricing experiment can compare a platform fee per organization, a cluster
management fee and managed-compute charges. Treat any proposed price as a
hypothesis. Do not describe an unmeasured margin or conversion rate as a forecast.

## Exercise

Write a one-page product contract for Northstar. State the protected assets, the
first workflow, the data that leaves its cluster, the operations requiring human
approval and the conditions that block a pilot. Remove any feature that does not
help prove this contract.

## Primary sources

[Agent Sandbox documentation](../references.md#s01)
