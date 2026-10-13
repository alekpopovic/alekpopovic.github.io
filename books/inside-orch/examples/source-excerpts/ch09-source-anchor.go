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
