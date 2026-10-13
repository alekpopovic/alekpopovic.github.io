# Chapter 32 - Local Volumes, Claims, and Workload Topology

Atlas API needs a disposable cache that survives a container replacement on one worker. A named local volume can preserve those bytes, but it also changes placement: moving the task to another worker does not move its data. The orchestration model must distinguish a logical claim, a physical local volume and the current authority to write it.

This chapter assumes task assignment, agent mounts and namespace scope. You will trace claim resolution into an attachment, explain the implemented ReadWriteOnce predicate, and identify which topology checks reach ordinary service placement. The safe lab uses control-plane and scheduler tests with disposable metadata; no real database contents or host volume are touched.

## Local Volumes and Claim Binding

Volume contains ID, namespace, name, driver and optional node ID. CreateVolume defaults the driver to local and rejects another driver. Names are unique within a namespace in the MemoryService inventory. This describes local volume metadata; it is not a distributed storage provisioner or an actual Engine volume-create call in that method. [Claim ch32.binding](../../validation/evidence/ch32.json).

VolumeClaim adds its own identity/name, optional VolumeID, access mode and allow_concurrent_writers. CreateVolumeClaim defaults access mode to ReadWriteOnce and checks that an explicitly referenced volume exists in the same namespace. It stores the claim under a namespaced name key. The current method replaces that map entry rather than implementing a general immutable-claim lifecycle with a duplicate-name rejection; do not assume semantics from another platform.

resolveVolumeMountsLocked takes the workload namespace and each claim reference. If the claim has no bound VolumeID, it searches for a same-name local metadata volume or creates one. It then produces ResolvedVolumeMount with claim/volume IDs, volume name, current node binding, target, read-only flag, access mode and concurrent-writer option. These resolved fields become part of the task snapshot.

[internal/controlplane/workloads.go, lines 460–477](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L460-L477) at the locked revision.

```go
		if c.VolumeID == "" {
			for id, v := range s.volumes {
				if v.Namespace == ns && v.Name == c.Name {
					c.VolumeID = id
					break
				}
			}
			if c.VolumeID == "" {
				v := types.Volume{ID: newUUID(), Namespace: ns, Name: c.Name, Driver: "local", CreatedAt: s.now()}
				s.volumes[v.ID] = v
				c.VolumeID = v.ID
				s.volumeClaims[namespacedKey(ns, c.Name)] = c
			}
		}
		v := s.volumes[c.VolumeID]
		out = append(out, types.ResolvedVolumeMount{ClaimID: c.ID, VolumeID: v.ID, VolumeName: v.Name, NodeID: v.NodeID, Target: m.Target, ReadOnly: m.ReadOnly, AccessMode: c.AccessMode, AllowConcurrentWriters: c.AllowConcurrentWriters})
	}
	return out, nil
```

The distinction between claim identity and volume identity helps describe retention. Removing one task need not delete the claim or volume metadata. A later task can resolve the same claim and find the same volume. That is useful for local replacement, provided its topology and physical naming remain correct. It does not guarantee data backup or cross-host access.

The agent converts a resolved mount into the runtime VolumeMount using VolumeName, Target and ReadOnly. The Engine adapter builds name:target:mode bind strings. It does not include the metadata volume UUID or namespace in that physical name mapping. Two logical namespaces with the same volume name on one daemon therefore require particular scrutiny: the metadata separation alone does not prove separate physical volume names. [Claim ch32.physical-name](../../validation/evidence/ch32.json).

For Atlas, choose a unique run-owned physical volume name in any live experiment. A friendly generic data name can collide with an existing host volume even if the control-plane record is new. Inspect the actual mount name and container before writing disposable data. The source-only fixture avoids this risk and cannot establish physical namespace isolation.

## Attachments and Active Writer Rules

VolumeAttachment records volume ID, task ID, node ID, read-only mode and attach/detach timestamps. attachTaskVolumesLocked creates an attachment for each resolved mount and binds an unbound volume's metadata NodeID to the chosen node. detachTaskVolumesLocked marks matching active records detached instead of erasing their history. [Claim ch32.attachments](../../validation/evidence/ch32.json).

The eligibility predicate first excludes a node when a resolved mount has a different nonempty NodeID. For a writable ReadWriteOnce mount without allow_concurrent_writers, it then excludes placement when any active attachment exists for that volume. That is the actual predicate, including its conservative treatment of existing attachments. Do not replace it in prose with a more permissive abstract interpretation.

[internal/controlplane/workloads.go, lines 492–507](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L492-L507) at the locked revision.

```go
		for _, m := range mounts {
			if m.NodeID != "" && m.NodeID != n.ID {
				ok = false
				break
			}
			if !m.ReadOnly && m.AccessMode == types.VolumeReadWriteOnce && !m.AllowConcurrentWriters {
				for _, a := range s.attachments {
					if a.VolumeID == m.VolumeID && a.DetachedAt.IsZero() {
						ok = false
						break
					}
				}
			}
		}
		if ok {
			out = append(out, n)
```

A new read-only mount skips the writable-RWO conflict branch, so it does not request the writer exclusion there. However, the loop for a later writable request checks active attachments without filtering their ReadOnly flag. An existing read-only attachment can therefore block that later writer in this implementation. The storage documentation's simple statement that readers do not consume a writer lock needs this code-level qualification.

allow_concurrent_writers bypasses that writer-conflict branch; it does not add application-level serialization. ReadWriteMany likewise does not create distributed storage just because the access mode name exists. The selected Docker driver remains local. Multiple allowed writers can corrupt application data unless the application and filesystem usage are designed for it.

An attachment is a control-plane record, not a kernel lease. Marking it detached cannot prove an unreachable worker's process stopped writing. Conversely, a missing attachment after memory state loss does not mean the physical volume is unused. Logical writer exclusion is valuable within the authoritative inventory, but distributed fencing requires an external mechanism that actually revokes stale write authority.

The removal lifecycle also matters. Reported task removal and Job deletion invoke detach logic in their relevant paths. DeleteVolume rejects a metadata volume with active attachments. This prevents a particular metadata deletion while known use remains, but physical data retention and actual Engine removal are separate operations. A delete method returning nil is not proof the local filesystem bytes were securely removed.

## Topology Constraints During Placement

The standalone scheduler accounts volume topology and active writers from supplied tasks. Its focused workload test presents one running writable RWO task and one pending task sharing a volume, then expects no assignment for the second. This is a deterministic Plan constraint, not a live data migration experiment. [Claim ch32.scheduler](../../validation/evidence/ch32.json).

Ordinary service placement also has a real volume path, despite bypassing some resource/label planner filters. reconcileServiceTasksLocked resolves mounts, filters ready nodes through nodesForVolumeMountsLocked, and repeats the writer eligibility check as it creates assigned tasks. It calls attachTaskVolumesLocked immediately after storing each task. Therefore the volume constraint is not merely a disconnected planner test. [Claim ch32.live-path](../../validation/evidence/ch32.json).

The current MemoryService fixture creates a local volume explicitly bound to one ready node, a RWO claim and a service requesting two replicas. It observes only one created task and verifies its resolved VolumeID. It then injects task removal and checks attachment records for that task are detached. The [actual focused suite](../../validation/labs/ch32/focused-tests.json) passed both control-plane and scheduler volume cases.

That result is narrower than saying two-replica stateful services are supported safely. The desired replica count can remain two while only one writer is eligible. A replica deficit is an expected consequence of the storage constraint, not permission to ignore the writer rule. A UI should expose the reason rather than pretending a second ready replica exists.

| State | Placement implication | Data implication |
| --- | --- | --- |
| Unbound local volume metadata | First assignment can choose a node | No replicated bytes created |
| Bound mount with another node ID | Wrong node excluded | Data remains local |
| Active attachment and writable RWO request | Writer branch rejects another placement | No physical stale-host fencing |
| Task removed and attachment detached | Later logical use may become eligible | Volume bytes may remain |

Binding snapshots need care. Resolved mounts carry the node value copied at resolution time. attachTaskVolumesLocked can subsequently set the volume record's NodeID. A task retry copying an old resolved mount or a multi-task loop retaining an earlier snapshot requires inspection to ensure the latest binding is represented. The current helper checks mount.NodeID rather than reloading the volume record for every predicate. This is a source-derived stale-snapshot edge, not a guarantee that every rescheduling history is already covered.

The Atlas failure window is node loss while a writer may remain alive. Starting a replacement on another worker would not bring over the local bytes and could create a second independent dataset. A correct operational response needs knowledge of the old process and actual data location. An offline heartbeat is not sufficient evidence for force-detach, migration or safe failover.

## The Storage Guarantees That Are Absent

The repository's stateful-workload design proposes stable ordinals, ordered startup/shutdown, claim templates, snapshots, backup hooks and controlled replacement. Those are architectural ideas, not features to infer from the simpler VolumeClaim type. The current MVP does not implement a replicated stateful-service abstraction, distributed storage driver, automatic data migration or application-aware backup. [Claim ch32.design-boundary](../../validation/evidence/ch32.json).

A local cache and a database have different recovery needs. Losing a cache may be acceptable when it can be rebuilt; losing database bytes may not. The same RWO metadata predicate does not establish a backup strategy for either. Define the data's value, retention, rebuild process and acceptable downtime before choosing a replacement procedure.

Cleanup must state its retention choice. The deterministic chapter fixture creates only memory metadata, so process exit removes the test state and leaves no host volume. A live extension should default to retaining the exact named volume after removing its run-owned task, verify the data through an explicitly authorized subsequent mount if desired, and delete the exact owned volume only when disposable data removal is intended. Never use a broad volume prune to complete a chapter exercise.

The Engine adapter's container removal requests volume removal for associated anonymous volumes, while named-volume behavior has its own Engine semantics. Do not infer that every claim's named volume disappears with the container. Record the actual container mounts and volume inventory in a live retention test rather than relying on an unrelated metadata method.

The default server's attachment and volume maps are memory-owned. Restarting it can lose the logical inventory while physical named volumes remain on the daemon. This is another reason that memory-state recovery and storage-data recovery must be designed together. A fresh process can neither prove a volume is unused nor reconstruct all writer authority from an empty map.

History is the batched implementation [4d641bbe8913da568d6d9f4697a0144314e10b87](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87). Its changed workload types, agent mounts, control-plane attachment logic and scheduler tests establish the MVP. The accompanying stateful design's broader promises remain design only. No separate implementation is invented for each original storage prompt.

For the safe Atlas lab, use the disposable source module and pinned Go 1.25 toolchain. Predict one writer for desired two, a refused conflicting scheduler assignment and detached metadata after the injected removal. Run:

```sh
go test ./internal/controlplane ./internal/scheduler \
  -run 'TestLocalVolumeSchedulingConflictAndCleanup|Test.*Volume' -count=1 -v
```

The linked record contains the real selected tests and pass results. No PostgreSQL, Docker daemon, filesystem data write or network listener is needed. Cleanup is process exit. A wrong-node extension can present two fake nodes and a mount explicitly bound to one, then assert the other is ineligible; keep that result separate from the actually recorded baseline cases.

For a live storage experiment, use a unique owned named volume and harmless sentinel text, record the selected node and actual mount source, then distinguish container replacement from relocation. An observed sentinel surviving replacement on one node supports that one retention scenario. It would still not prove replication, backup, distributed fencing or isolation between equal names in different namespaces.

## Exercises

1. Trace claim name, metadata VolumeID and physical Docker VolumeName. Which one reaches the bind string, and what namespace assumption can fail?
2. Explain the exact writable-RWO predicate when an active read-only attachment already exists. How does this qualify the documentation?
3. Why does the passing one-writer fixture not prove safe automatic failover after node loss?
4. Design a retention test with explicit cleanup, then identify the stale resolved-node snapshot case and the additional assertion needed before claiming all later placement stays pinned.

[Worked answers](../solutions/ch32.md) preserve identity, topology and physical-effect distinctions. Local volume metadata and writer checks are implemented; replication, safe stale-host revocation and complete stateful recovery remain separate engineering work.
