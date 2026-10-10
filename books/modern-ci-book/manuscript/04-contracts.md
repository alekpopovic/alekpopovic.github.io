# 4. Keep contracts and dependency resolution honest


## Three kinds of compatibility

A source commit, a library version, and a network protocol version answer different questions. The workspace pins source. A Go module declaration identifies an import dependency. A runner handshake declares which messages an installed binary understands. Pinning the first does not automatically establish the other two.

The contracts repository owns the HTTP schema, runner wire format, pipeline grammar, and generated client descriptions. The core repository owns validation semantics and the single migration tree. The server and scheduler share the core through versioned dependencies. Runner and CLI depend on wire contracts without importing the database implementation.

Model compatibility as an explicit table: server version, protocol version range, schema range, generated client revision, and tested runner versions. Reject unsupported combinations early. A helpful failure says which range is required; it does not let a worker begin a job and discover an incompatible field halfway through execution.

## Use a local workspace without hiding release defects

A Go `go.work` file can combine multiple modules during development. It is an overlay for collaborating on sibling modules, not a promise that an isolated consumer can resolve those dependencies. The Go workspace tutorial and module reference describe that distinction and module version resolution. [S05](e-sources.md#s05) [S06](e-sources.md#s06)

For this project, generate an ignored root `go.work` after the child modules exist. Check the integrated workspace, then check applications with workspace resolution disabled:

```bash
cd apps/server
GOWORK=off go test ./...
GOWORK=off go build ./cmd/server
```

These are target-application procedures, not commands provided by the book's laboratory. They should run in a fresh checkout with only the declared dependencies. Do not ship `replace` directives pointing to `../../packages/core` and call the result independent.

Before dependency repositories are published, choose a clearly labeled local verification path. One option is a verified vendor snapshot prepared from pinned source, with a receipt describing its producer commits and checksums. Another is a temporary local module proxy with valid module versions. Neither path proves that public module resolution works. The release gate must test the actual published dependency path separately.

## Generate clients with receipts

The browser can commit a generated TypeScript client into its own source tree for the first release. This avoids forcing a registry publication for each local schema iteration while keeping the web checkout self-contained. Record the full contracts commit, schema content hash, generator identity, generator version, and relevant flags.

A generated file with no provenance soon becomes hand-maintained by accident. Regenerate in integration CI and fail on drift. Do not patch generated DTOs to make a UI build pass while the server still advertises a different shape. Place presentation types outside the generated directory.

For wire evolution, prefer additive optional fields with defined defaults. An unknown enum value may need an “unsupported” presentation instead of a crash. Removing a required field or changing its meaning needs a versioned migration path. A protocol can be syntactically parseable and still semantically incompatible.

## One owner for schema change

Let the server's explicit administration command apply migrations from the core package under an exclusive migration lock. Normal API and scheduler startup check a supported range. They should not independently modify schema while accepting work.

An expansion migration can add a nullable column before code begins using it. Backfill in bounded batches. Only after the new path is proven should a later release remove the old representation. Keep both protocol and database changes reversible within a documented window, and state where downgrade ceases to be safe.

Avoid an all-purpose compatibility claim. Independently released repositories do not imply that arbitrary versions can be combined. The compatibility matrix is evidence for particular combinations, not a universal property of the architecture.

## Exercise

The web builds successfully using a sibling SDK symlink, and the server builds successfully using `go.work`. Can the workspace be released? State the missing checks.

## Worked answer

Not on those observations alone. Build the web from its own checkout with its committed lockfile and generated client receipt. Build Go consumers with `GOWORK=off` from resolvable module versions or a documented, verified vendor snapshot. Then validate the actual release resolution path and run protocol/schema compatibility tests against the built binaries. Integrated source convenience is useful, but it must not substitute for independent dependency resolution.

## Completion evidence

Every published component includes a dependency record and a tested compatibility range. A build must reveal its source and dependency inputs without requiring the author's working directory.
