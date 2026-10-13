	row := s.db.QueryRow(ctx, `
		UPDATE tasks
		SET node_id = $2,
			actual_status = $3,
			ports = $4,
			updated_at = timezone('utc', now()),
			row_version = row_version + 1
		WHERE id = $1 AND updated_at = $5 AND actual_status = 'pending'
		RETURNING id, namespace, service_id, node_id, container_id, desired_status, actual_status,
			image, requested_image, resolved_image_digest, image_registry, image_name, image_tag,
			version, ports, conditions, restart_count, failure_reason, created_at, updated_at, started_at, finished_at`,
		string(id),
		string(nodeID),
		string(types.TaskAssigned),
		portBytes,
		expectedUpdatedAt.UTC(),
