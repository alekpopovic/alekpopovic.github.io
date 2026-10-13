# memory-service-placement

Normal service reconciliation creates assigned tasks directly; compare the separate planner path.

Unchanged, contiguous source excerpt: [internal/controlplane/controlplane.go, lines 2287–2307](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2287-L2307).

```go
	for len(active) < service.Spec.Replicas {
		eligibleNodes := s.nodesForVolumeMountsLocked(nodes, resolvedMounts)
		if len(eligibleNodes) == 0 {
			break
		}
		node := eligibleNodes[len(active)%len(eligibleNodes)]
		task := types.Task{
			ID:                  types.TaskID(newUUID()),
			Namespace:           service.Namespace,
			ServiceID:           service.ID,
			NodeID:              node.ID,
			DesiredStatus:       types.TaskRunning,
			ActualStatus:        types.TaskAssigned,
			Image:               service.Spec.EffectiveImage(),
			RequestedImage:      service.Spec.ImageMetadata.RequestedImage,
			ResolvedImageDigest: service.Spec.ImageMetadata.Digest,
			ImageRegistry:       service.Spec.ImageMetadata.Registry,
			ImageName:           service.Spec.ImageMetadata.Name,
			ImageTag:            service.Spec.ImageMetadata.Tag,
			Version:             service.DeploymentVersion,
			Ports:               s.assignPortsForNodeLocked(service.Spec.Ports, node.ID),
```

SHA-256: `44693bfa1104e662d96916541960f29cc5e06739e78f16baee4ee15bf2c0bee3`. This excerpt is not an independently compilable program.
