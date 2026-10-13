func (s *postgresStore) AssignTask(ctx context.Context, id types.TaskID, nodeID types.NodeID, ports []types.Port, expectedUpdatedAt time.Time) (types.Task, error) {
	current, err := s.getTask(ctx, id, s.begin == nil)
	if err != nil {
		if errors.Is(err, ErrNotFound) && s.begin == nil {
			if _, getErr := s.getTask(ctx, id, false); errors.Is(getErr, ErrNotFound) {
				return types.Task{}, ErrNotFound
			} else if getErr != nil {
				return types.Task{}, getErr
			}
			return types.Task{}, ErrConflict
		}
		return types.Task{}, err
	}
	if err := types.ValidateTaskTransition(current.ActualStatus, types.TaskAssigned); err != nil {
		return types.Task{}, fmt.Errorf("%w: %v", ErrInvalidState, err)
	}
	portBytes, err := jsonBytes(defaultSlice(ports))
	if err != nil {
		return types.Task{}, err
	}
	row := s.db.QueryRow(ctx, `
		UPDATE tasks
		SET node_id = $2,
			actual_status = $3,
			ports = $4,
			updated_at = timezone('utc', now()),
			row_version = row_version + 1
		WHERE id = $1 AND updated_at = $5 AND actual_status = 'pending'
		RETURNING id, namespace, service_id, node_id, container_id, desired_status, actual_status,
