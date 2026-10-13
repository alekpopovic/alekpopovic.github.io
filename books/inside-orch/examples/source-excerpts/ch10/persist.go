func (s *Scheduler) persistAssignment(ctx context.Context, task types.Task, assignment Assignment) (Assignment, bool, error) {
	assignment.ExpectedUpdatedAt = assignment.ExpectedUpdatedAt.UTC()
	if assignment.ExpectedUpdatedAt.IsZero() {
		assignment.ExpectedUpdatedAt = task.UpdatedAt.UTC()
	}
	transactional := false
	if _, ok := any(s.store).(store.Transactor); ok {
		transactional = true
	}
	assigned := false
	err := store.WithTx(ctx, s.store, func(txCtx context.Context, tx Store) error {
		assignedTask, err := tx.AssignTask(txCtx, assignment.TaskID, assignment.NodeID, assignment.Ports, assignment.ExpectedUpdatedAt)
		if err != nil {
			return err
		}
		assignedAt := assignedTask.UpdatedAt.UTC()
		if assignedAt.IsZero() {
			assignedAt = s.now().UTC()
