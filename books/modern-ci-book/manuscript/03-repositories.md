# 3. Make every application an independent repository


## Eight repositories compose one system

The application's source topology is intentionally explicit:

| Repository | Workspace path | Responsibility |
|---|---|---|
| `modern-ci-workspace` | root | Integration, pins, operational composition |
| `modern-ci-server` | `apps/server` | HTTP API and identity |
| `modern-ci-scheduler` | `apps/scheduler` | Scheduling and reconciliation |
| `modern-ci-runner` | `apps/runner` | Execution and runner protocol |
| `modern-ci-web` | `apps/web` | Angular operator interface |
| `modern-ci-cli` | `apps/cli` | Command-line client |
| `modern-ci-core` | `packages/core` | Public domain/store/compiler libraries |
| `modern-ci-contracts` | `packages/contracts` | Wire schemas and client generation |

The book you are reading belongs in a separate `modern-ci-book` repository. It does not pretend to contain these application histories. The companion module is a teaching fixture, not an eighth application hidden inside the book.

A Git submodule is a separate repository referenced by a gitlink in a superproject. The gitlink selects a commit; `.gitmodules` records configuration such as its path and URL. Copying a folder into a ZIP does not create that relationship. [S03](e-sources.md#s03)

## Bootstrap in the right order

Create an initial commit in each child repository and make it reachable in a repository you control. Then register the children from the workspace. The following is an operator example after the child repository exists; replace the owner deliberately:

```bash
OWNER=your-github-owner
git submodule add \
  "https://github.com/$OWNER/modern-ci-server.git" \
  apps/server
git add .gitmodules apps/server
git commit -m "Register the server repository"
```

Repeat the pattern for the other components. Do not insert invented commit hashes into a lock file. Before publishing the parent, ensure readers have access to the child commits it references. A publicly readable workspace pointing to inaccessible private children is not a reproducible public release.

Cloning an existing workspace normally requires recursive initialization:

```bash
git clone --recurse-submodules REPOSITORY_URL
git submodule status --recursive
```

The checkout selected by the parent may be detached. Before editing inside a child, create or switch to an appropriate branch. Commit inside the child, then stage the updated gitlink in the parent. Git's submodule documentation explains the separate histories and update behavior. [S04](e-sources.md#s04)

## Source separation is not build independence

A runner repository that imports a sibling directory through a relative replacement is not independently buildable. A Dockerfile in `apps/server` cannot rely on undeclared files above its build context. A web repository that needs a local symlink to another repository is not a complete source checkout.

Make each child own its dependency declarations, tests, Dockerfile where applicable, and release procedure. The root owns the tested combination, not a hidden source overlay. Root integration tests are necessary, but they cannot replace a standalone build of every application.

The shared core package must expose intentional public APIs. An `internal` package in one Go repository is not a convenient cross-repository import surface. Keep low-level internals private and publish narrowly named packages for the compiler, queue transactions, domain types, and store. The contracts repository should remain independent of persistence implementation.

## Coordinate a change without losing history

Suppose a new job field requires schema and UI changes. Start with the contracts and compatibility fixtures. Update the core validation. Update server and scheduler consumers. Regenerate the web client with a receipt naming the schema digest and generator. Test each changed repository independently, then test the combined workspace.

Commit the children first. Update the workspace gitlinks second. Record a source lock from those exact commits. A release manifest later adds built image digests and schema/protocol compatibility. The source lock and release manifest are different records: one identifies code, the other identifies deployable outputs.

Do not force-rewrite commits already used by a release or evidence record. Use forward changes and a new workspace snapshot. Rewriting a child history can invalidate references preserved in several other repositories.

## Exercise

A developer changes the runner, commits only the workspace, and sends the workspace commit for review. The reviewer gets the old runner. Why, and how should the change be repaired without inventing a new history?

## Worked answer

The parent cannot store uncommitted source inside a submodule as an ordinary directory patch. Commit the runner changes inside its repository, publish that child commit through the normal review path, then commit the new gitlink in the workspace. Verify the resulting workspace from a fresh recursive clone. The important evidence is not that the author's working tree looked correct, but that another checkout can retrieve the same child commit.

## Completion evidence

A clean consumer environment can clone the workspace recursively, identify all seven child commits, and build each application without relying on untracked sibling files.
