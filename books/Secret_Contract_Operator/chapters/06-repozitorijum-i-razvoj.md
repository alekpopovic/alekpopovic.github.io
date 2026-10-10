# 6. Repository and Development Environment

## 6.1 Reproducibility Before Implementation

The repository must record exact versions of the Go toolchain, Kubebuilder, controller-runtime, controller-gen, envtest binaries, and the kind node image. This book does not call an untested combination the “latest compatible” one. Compatibility follows from the chosen scaffold and test results.

Generate the initial `toolchain-report.txt` locally without kubeconfig contents, environment dumps, or credentials. `go version`, `kubebuilder version`, `kubectl version --client`, `helm version`, and hashes of the relevant configuration files are sufficient.

## 6.2 Bootstrap Commands

The following commands are a proposal for an empty repository. Do not run them over an existing project without reviewing it first.

```bash
mkdir secret-contract-operator
cd secret-contract-operator

git init
kubebuilder init \
  --domain codepop.tech \
  --repo github.com/CodepopTech/secret-contract-operator

kubebuilder create api \
  --group secrets \
  --version v1alpha1 \
  --kind SecretContract \
  --resource --controller

make generate
make manifests
go test ./...
```

If the local Kubebuilder version requires different flags or an additional plugin choice, follow its `--help` output and record the choice. Do not change Go modules at random just to make the command succeed. Preserve `PROJECT` and the generated Makefile as part of the scaffold contract. [S04](https://book.kubebuilder.io/)

## 6.3 Project Structure

```text
secret-contract-operator/
  AGENTS.md
  api/v1alpha1/
  cmd/
  internal/
    authorization/
    contract/
    controller/
    dependencies/
    mutation/
    status/
    telemetry/
  config/
    crd/
    manager/
    rbac/
    samples/
  charts/secret-contract-operator/
  examples/
  test/e2e/
  docs/adr/
  prompts/
  tracking/
```

Do not create every empty package immediately. `mutation` can wait until the second phase. Keeping the pure validator free of accidental dependencies on an event recorder or cloud client matters more than making the directory structure look large.

## 6.4 AGENTS.md as an Engineering Contract

Codex supports project instructions in `AGENTS.md`; the instruction hierarchy allows general context and more specific guidance in individual directories. This is more useful than repeating the entire context in every task. [S25](https://developers.openai.com/codex/guides/agents-md/)

For this project, the root instructions define feature boundaries, prohibit leakage, require namespace-local references, exclude mutation permissions from the MVP, and require tests. They contain no real secrets, production endpoints, or rule authorizing automatic deployment to a real cluster.

```text
Read docs/specification.md before changing public API.
Read docs/security.md before touching Secret handling.
Never serialize Secret objects to diagnostics.
Default profile is validation-only, including RBAC.
Do not overwrite unrelated work or existing env entries.
Record executed tests; never mark an unrun test as passed.
```

## 6.5 Development Checks

`gofmt` and `go vet` check basic hygiene, but they do not prove reconcile correctness. `make generate` refreshes DeepCopy code. `make manifests` refreshes CRD and RBAC artifacts. CI must confirm that generation leaves no diff.

`go test ./...` must not silently require a real production cluster. Unit tests and envtest use clearly separated test setups. E2E tests against kind run through a separate target and a dedicated kubeconfig.

## 6.6 A Fake Cluster Is Different from envtest

The controller-runtime fake client is useful for certain unit tests, but it does not represent an API server with all defaulting and status-subresource rules. Envtest starts an API server and etcd, without a kubelet or standard workload controllers. Consequently, an envtest must not wait for a Deployment to actually create pods. [S10](https://book.kubebuilder.io/reference/envtest.html)

The first goal is a small set of clear tests: create a contract, check its status, change its Secret, and perform a no-op second reconcile. Add optional integrations and full-cluster tests afterward.

**Checkpoint.** A clean checkout should have a documented path to unit tests without cloud credentials. Explicitly identify anything that requires network access, tool downloads, or a local cluster.
