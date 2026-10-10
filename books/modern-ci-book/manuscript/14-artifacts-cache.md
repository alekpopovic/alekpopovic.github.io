# 14. Preserve artifacts and keep cache trust separate


## Artifacts are outputs; caches are hints

An artifact is an identified output that another job or operator may rely on. A cache is an optimization whose absence must not invalidate correctness. Treating the two as interchangeable makes releases depend on mutable, evictable data.

An artifact manifest should record its producer attempt, project, logical name, content digest, size, content type, creation time, and retention policy. Finalize it before downstream jobs reference it. Download authorization checks ownership and current access; object-key obscurity is not access control.

A cache entry needs a namespace, key, trust level, producer information, size limit, and eviction policy. A pull-request job should not be able to overwrite a cache later consumed as trusted release input. Separate trust domains even when their dependency lockfiles happen to match.

## Transfer files deliberately

Jobs do not share a filesystem automatically. A producer declares the files it exports, and a consumer declares the artifact identity it imports. This makes it possible to schedule jobs on different hosts and understand which bytes crossed the boundary.

Before uploading, confine paths to the workspace, reject unwanted symlinks, and apply file-count and byte limits. Before extracting archives, reject absolute paths, parent traversal, unsafe links, device files, and excessive expansion. Validate the destination after path normalization, not just the original filename string. A compressed upload limit alone does not bound the uncompressed result.

Content hashes help detect corruption and identify immutable bytes, but they do not prove that the producer was authorized or the source was trustworthy. Keep the identity and policy record alongside the hash. A malicious build can produce a perfectly valid digest of malicious content.

## Reports require their own parser policy

JUnit-style XML can improve failure summaries, but report files are controlled by the job. Use a parser configuration that does not resolve external entities, and enforce depth, element count, string length, and total-size limits. Normalize paths before linking report entries back to repository files.

Do not let a malformed report erase the actual command result. Record report ingestion as a separate result: accepted, partially accepted under a documented policy, or rejected. The operator should still be able to inspect the underlying authorized artifact or log when appropriate.

Test names and failure messages are untrusted display text. Escape them in the web interface. A report containing a test named “Deployment approved by administrator” must not resemble a real approval event.

## Retention is part of the product

Define retention for ordinary runs, successful release artifacts, failed-run diagnostics, and audit records separately. A release still deployed to production may need its artifact retained even if the original build's default retention period has passed.

Garbage collection should first mark eligibility and then delete in bounded batches. Race it against new references in tests. A deletion record makes it possible to distinguish an intentional retention action from unexplained storage loss. Signed URLs should expire even when the underlying object remains.

Capacity controls belong to projects or organizations as well as the storage service. Otherwise one large test suite can exhaust a shared bucket or runner disk. Show current usage and the effect of retention policy changes before applying destructive operations.

## Exercise

A project uses one cache key, `node-modules`, for both public pull requests and production builds. A release build is fast and its tests pass. What additional property is missing from the evidence?

## Worked answer

The evidence does not establish that release inputs came from an authorized trust domain. The shared writable cache can influence a later trusted build. Use trust-aware namespaces and restricted writers, include relevant dependency and platform identities in keys, and ensure correctness can be reproduced from declared sources with an empty cache. Passing tests do not repair an undefined supply-chain boundary.

## Completion evidence

Test cross-project download denial, stale upload capabilities, archive traversal and expansion limits, report parser limits, cache poisoning boundaries, and retention racing a newly created release reference.
