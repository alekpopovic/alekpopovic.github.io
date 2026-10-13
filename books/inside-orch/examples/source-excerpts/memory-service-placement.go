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
