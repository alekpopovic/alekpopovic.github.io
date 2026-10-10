# 18. CI/CD, Releases, and the Supply Chain

## 18.1 CI as a Verifiable Contract

The pull-request pipeline should check formatting, static analysis, unit tests, race tests, envtest, API artifact regeneration, chart linting, and container builds without pushing. These checks require no production cloud credentials.

Generated files belong to the source code. After `make generate` and `make manifests`, `git diff --exit-code` should be empty. Do not repair stale CRDs only in the release pipeline; the error should be visible in the PR.

## 18.2 GitHub Actions Security

GitHub recommends minimal token permissions, careful handling of untrusted input, and pinning third-party Actions to full commit SHAs for immutable references. Running untrusted PR code with a privileged token is particularly risky. [S26](https://docs.github.com/en/actions/reference/security/secure-use)

An ordinary PR needs `contents: read` and only the permissions its tests actually require. Do not push images from an unverified fork PR. Do not interpolate branch names or PR titles directly into shell code. Do not use `pull_request_target` to check out and execute untrusted head code.

## 18.3 Proposed Pipeline Stages

```text
pull request
  format + vet
  unit + race
  envtest
  generated-diff check
  chart render + RBAC policy checks
  container build
  optional kind integration

signed/reviewed release tag
  repeat required validation
  multi-arch build
  push immutable digest
  generate SBOM + provenance
  sign and publish artifacts
```

The diagram describes a target organization, not an existing workflow. Choose and pin exact Actions versions when implementing the pipeline. Do not put invented SHAs in documentation to make it look complete.

## 18.4 Release Artifacts

A release contains images for supported architectures, a CRD manifest, an installation manifest or Helm package, checksums, an SBOM, and release notes. Publish the image digest alongside the tag so users can pin exact contents.

An artifact signature proves provenance under the chosen trust model, not operator correctness. The README should show how to verify the signature and which publisher identity to expect. Without that verification, “signed image” is merely a technical label.

## 18.5 Distinguishing Versions

Application release, chart version, and CRD API version are different. A `v0.1.3` binary release may still serve `secrets.codepop.tech/v1alpha1`. A chart patch can change resources or documentation without changing the CRD schema.

Changing `Ready` semantics, authorization defaults, or restart-token calculation is not harmless merely because the YAML fields retain their names. Release notes must describe the impact on existing contracts and possible rollouts.

## 18.6 Upgrade Testing

Install the previous actual release in kind, create contracts and synthetic Secrets, and then apply the new CRD and operator version. Check that old contracts remain valid, status acquires the expected new semantics, and no unplanned restarts occur.

Rolling back the operator image can be safe only if the previous binary understands the currently stored CR data and schema. Do not promise rollback of every API change with a single `helm rollback` call.

## 18.7 What Must Stay Out of Release Attachments

Exclude kubeconfigs, full cluster dumps, real Secrets, heap profiles, and debug logs with unchecked payloads. Even E2E test artifacts require a redaction review before public publication.

`TEST_REPORT.md` records what actually passed, on which version, and what was not run. “CI planned” is different from “CI passing.”

**Checkpoint.** A release should be reproducible from a clean, tagged commit without secret manual steps on a maintainer's laptop.
