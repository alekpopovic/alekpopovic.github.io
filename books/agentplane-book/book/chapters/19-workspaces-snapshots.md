# 19. Preserve Workspaces Without Inventing Checkpoint Guarantees

**Part VI — State and Evidence**

Persistent storage can preserve files across runtime restarts. It does not
necessarily preserve a process, its memory, open sockets or an in-progress
transaction. These are different kinds of state and should appear as different
capabilities in the product.

## Define the workspace contract

A workspace belongs to a scope and a stable resource identity. Its policy defines
size, approved StorageClass, access mode, retention, snapshot behavior and
termination cleanup. Do not attach an arbitrary existing PVC merely because a
caller knows its name. Validate scope, ownership and intended use.

The workspace path should contain user data, not connector credentials or runtime
control binaries. Separate temporary credential delivery from persistent files.
If a program copies a secret into its own workspace, an ordinary snapshot can
capture that secret. Storage controls cannot infer every file's sensitivity.

## Distinguish consistency levels

A storage snapshot may represent crash-consistent filesystem state. An application
may require a flush, checkpoint or quiesce operation for a useful restore. A
database inside a sandbox has its own recovery semantics. Do not label every CSI
snapshot application-consistent without testing the application protocol.

Kubernetes volume snapshots depend on the snapshot APIs and a supporting CSI
implementation. They model storage snapshots, not a universal memory-checkpoint
mechanism. [S12](../references.md#s12)

Use capability labels such as `filesystem_snapshot`, `application_quiesce` and
`process_checkpoint` rather than one ambiguous `snapshot_supported` boolean.
Only advertise the capabilities actually verified for the chosen runtime and
storage combination.

## Restore into a new resource

A restore should normally create a new workspace and session, leaving the source
and original snapshot intact. This avoids silently rewinding an active workload
under the same identity. Record the source snapshot, template version, policy
version and restore operation ID.

Revalidate current security policy. A snapshot created under an old image or
credential policy does not authorize restoring those old privileges today.
Separate restoration of customer data from restoration of runtime authority.
An old workspace might contain stale credentials and must be treated accordingly.

## Hibernation and warm capacity

A restartable workspace suspension can stop compute while retaining storage.
That can be useful even when process memory is not preserved. Name the capability
honestly and explain what application work must be resumed or repeated.

Warm pools consume capacity before a customer claim. Unclaimed capacity should
have no tenant credentials or retained tenant files. Once used by a tenant,
recycling requires a proven cleanup process; creating fresh capacity is often
easier to reason about. Keep pool quotas separate from active-session quotas so
an oversized warm pool cannot starve ordinary workloads silently.

## Archive fallback is a different feature

A tar-based workspace export can be useful when CSI snapshots are unavailable,
but it is not automatically atomic. Concurrent writes may yield an inconsistent
archive. Apply path, special-file, expanded-size and credential-exclusion rules.
State where the archive is stored and who can decrypt it.

Do not silently upload an archive to SaaS-owned object storage in a BYOC product.
Make that transfer explicit in organization configuration and user-facing data
handling documentation. An export checkbox is not a reason to weaken default
workspace residency.

## Cleanup is part of correctness

A session can end while a workspace remains retained. A failed snapshot can leave
provider resources behind. Record cleanup obligations separately from the user
operation status. Run bounded reconciliation and produce a dry-run inventory for
ambiguous resources.

Storage reclaim policies and provider behavior must be tested. Deleting a
Kubernetes object may or may not delete the underlying data according to its
configuration. Do not infer secure erasure from the disappearance of a PVC row in
the dashboard.

## Exercise

Write a restore drill using synthetic files and an application-level checksum.
Change the files after the snapshot, restore into a new session and compare the
result. Repeat with a writer active during capture. Document exactly which
consistency claim the observations support and which they do not.

## Primary sources

[Kubernetes volume snapshots](../references.md#s12)
