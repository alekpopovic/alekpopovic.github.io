# Preface: How to Use This Book

**Secret Contract Operator** is a Kubernetes operator design that checks whether an application receives the secrets it expects, in a form it can use. The book follows the path from the initial problem through API design, safe implementation, testing, packaging, and maintenance of a public open-source project.

This is not a conversation repackaged as a PDF. The earlier operator proposal and development prompts are consolidated into one technical specification. Ambiguous behaviors receive explicit decisions: what `Ready` means, who may create a contract, what happens during an invalid rotation, how to avoid a status-update loop, and why automatic variable injection is not part of the default mode.

## Who This Book Is For

The primary audience is DevOps and platform engineers familiar with Deployments, Secrets, namespaces, and basic RBAC. Implementation requires practical Go knowledge, but complexity is introduced gradually: a pure validator without Kubernetes dependencies, then a controller, followed by integrations and optional mechanisms that modify workloads.

Readers building the first public MVP should follow Chapters 1–11, 15–20, and Lab A. Chapters on injection, automatic restarts, and admission control describe a later phase. Cluster maintainers may prefer to begin with the security model, installation, observability, and operating procedures.

## Publication Status and Verification Limits

This book is a **design specification and development guide, edition 1.0**, prepared on October 10, 2026. It does not claim that the entire operator has been implemented, released, or security-certified. The proposed GitHub path, image repository, and API group are project configuration choices, not confirmation that public releases exist.

Three kinds of examples are distinguished. An **executable laboratory example** is a small standalone program in the companion `examples/contractlab` directory. A **reference snippet** illustrates a pattern to integrate into a real scaffold. A **future feature specification** describes a requirement that is implemented and accepted only after testing. YAML for a new CRD becomes applicable only after the corresponding schema is implemented and installed.

Book verification covers the generated formats, consistency of examples, and local tests of the isolated Go validator. Envtest, kind, a real ESO installation, Helm installation, and production-cluster operation remain development checks: the book prescribes them without claiming they have run.

## Conventions

The term **secret** refers to a sensitive value; `Secret` refers to a Kubernetes object. A **contract** is a `SecretContract` instance. A **consumer** is a selected container within a workload. A **reconcile** is one attempt to bring observed and desired state into agreement. Code identifiers use English naming for compatibility with Go and the Kubernetes ecosystem.

All password-like values in the labs are synthetic. They must not be reused in production. Commands that modify a cluster run only in a dedicated test environment until the release checklist has been completed.

References such as `[S01](https://kubernetes.io/docs/concepts/configuration/secret/)` and `[S02](https://external-secrets.io/latest/api/externalsecret/)` point to primary sources in the bibliography. They support the behavior of Kubernetes and the tools used. This operator's API, product boundaries, proposed tests, and security decisions are **design decisions made in this book**, not an official Kubernetes specification.

## Key Corrections to the Initial Idea

`Ready=True` neither blocks deployment nor proves that the application connected to its database. A changed `resourceVersion` does not prove that a password was rotated. A rotation-time annotation is not cryptographic evidence of credential age. Prohibiting value logging does not, by itself, prevent information extraction through validation rules.

The first operator version is therefore deliberately small: it reads approved Secret objects, checks the contract, and publishes safe, clearly bounded state. Anything that changes application execution receives additional authorization, a separate RBAC profile, and specific acceptance criteria.
