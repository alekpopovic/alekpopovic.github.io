# 04. Create a Reproducible Engineering Workspace

**Part I — Foundations**

A reproducible repository records inputs, build steps and observed results. It
does not merely contain a convenient startup command. For AgentPlane, distinguish
the documentation workspace, the teaching examples and the future application
workspace. This repository builds the book. The prompt pack targets a separate
application repository unless you explicitly choose otherwise.

## Establish a small command surface

A useful application repository eventually exposes `format`, `generate`, `lint`,
`test`, `build` and `verify`. Keep commands composable so a contributor can run a
single layer without provisioning infrastructure. A command named `verify` must
not quietly create paid cloud resources or install cluster-wide components.

This book's commands are intentionally smaller:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_book.py
python scripts/test_examples.py
python scripts/build_book.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

The renderer is pinned in `requirements.txt`. The validation report identifies the
actual Python and Go versions used locally. The Go teaching module uses an older
language baseline for portability; this is not advice to deploy an unsupported
Go toolchain. Production tools need a separately maintained compatibility record.

## Record a version matrix, not a wish list

For each production dependency, record an exact version, source URL, artifact
digest, license, date reviewed and the integration tests run with it. A row with
no successful test is a candidate, not a supported version. Keep the Kubernetes
server version separate from client libraries, CRD versions, the runtime daemon,
the sandbox router and the CNI. They can change independently.

Do not write guessed version numbers into generated manifests to make them look
complete. A configuration template that requires a verified digest is more honest
than a fabricated immutable-looking digest. The Kubernetes example renderer in
this repository requires explicit operator input and produces a manifest for
review; it does not deploy it.

## Make generated contracts reproducible

The public API should have one schema source. Generate low-level server and
client types from that source, then add a handwritten application layer. Keep
protobuf command envelopes separate from public HTTP resources. Their consumers
and compatibility requirements differ.

Record the generator version and invocation. A regeneration check should fail
when generated files differ from the repository, rather than overwriting them
and reporting success. Review generated changes as part of the source change.
Generated code can contain a breaking API change just as handwritten code can.

## Use a layered local environment

The smallest loop needs no cluster: domain tests, authorization tests, state
transitions and rendering. The next loop adds a disposable PostgreSQL instance
for migrations, RLS and concurrency. A third loop adds a Kubernetes cluster with
a policy-enforcing CNI and a chosen sandbox runtime. The final loop tests a
specific cloud deployment and identity integration.

A default Kind installation is not automatically an adequate network-policy or
hostile-code laboratory. Verify the installed CNI and runtime behavior. When the
required capabilities are absent, skip the integration explicitly and mark the
result unvalidated. Never substitute “object created” for “policy enforced.”

## Preserve a useful evidence trail

Store commands, exit codes, test counts, environment identifiers and sanitized
reports. Keep logs bounded. Do not collect every environment variable, pod log or
workspace archive on failure: diagnostics often contain the secrets that normal
logging correctly excludes.

Separate a proposed benchmark target from a measured result. For example, a
provisioning target belongs in an SLO proposal. A result belongs in a report with
hardware, versions, sample size and a clearly defined start and end point. A warm
pool claim and a cold node provision are different measurements.

## Keep publication permissions narrow

Book pull requests should run checks without deployment permission. Publishing a
Pages artifact belongs in a separate protected job. The included workflows use
reviewed action commit references and do not use pull-request content in shell
commands. GitHub's secure-use guidance explains the rationale for these trust
boundaries. [S24](../references.md#s24)

## Exercise

Create a dependency record for the sandbox controller and runtime server. List
which integration tests would have to be repeated after changing either one.
Then identify the smallest local command that can still give useful feedback
when Docker and Kubernetes are unavailable.

## Primary sources

[Mistune usage guide](../references.md#s17) · [GitHub Actions secure use](../references.md#s24)
