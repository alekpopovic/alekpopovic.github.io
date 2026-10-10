# Practical Examples

## A. Standalone Go Validator

`contractlab/` is an executable Go module using only the standard library. It runs no operator and requires no cluster. From that directory:

```bash
go test -count=1 ./...
go test -race -count=1 ./...
go vet ./...
go test -run='^$' -fuzz=FuzzValidator -fuzztime=3s -parallel=2
```

The lab uses synthetic values. See `../TEST_REPORT.md` for recorded checks.

## B. Future Kubernetes Labs

The YAML files demonstrate the **proposed API**, not resources of an operator already implemented in this package. Before cluster labs, implement and test the CRD and manager following the book's development plan. Use only a dedicated test cluster and check `kubectl config current-context`.

Sequence: create the test namespace with `00-namespace.yaml`, apply `01-missing-key.yaml`, and expect an unsatisfied contract. `02-valid-secret.yaml` then adds the missing synthetic key. Replace the image placeholder in `03-workload-template.yaml` with a verifiable test-image digest before applying the workload, followed by post-deployment contract `04-workload-contract.yaml`.

Do not run `kubectl apply -f manifests/` over the entire directory: the examples deliberately represent successive, different scenarios. The package contains no production credentials. Operator readiness does not replace application readiness.

## C. Generation-aware Deployment Gate

`contract-gate.sh` checks the UID, generation, and Ready observation of the proposed contract. It requires `bash`, `kubectl`, `jq`, and an implemented canonical status. It neither reads Kubernetes Secrets nor prints the complete contract.

```bash
NS=sco-lab CONTRACT=demo TIMEOUT_SECONDS=120 ./contract-gate.sh
```

This gate is not an atomic transaction: a secret may change between checking and use. Test the integration in a dedicated cluster before adopting it in CI/CD. The book also explains the circular dependency created by a preflight contract requiring a workload that does not yet exist.
