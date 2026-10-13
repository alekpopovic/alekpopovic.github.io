func (r *Reconciler) stopTask(ctx context.Context, task types.Task, reason string) (bool, error) {
	if task.DesiredStatus == types.TaskStopped || task.DesiredStatus == types.TaskRemoved {
		return false, nil
	}
	transactional := r.transactional()
	stopped := false
	err := store.WithTx(ctx, r.store, func(txCtx context.Context, tx Store) error {
		stoppedTask, err := tx.StopTask(txCtx, task.ID, task.UpdatedAt)
		if err != nil {
			return err
		}
		if err := events.Emit(txCtx, tx, types.Event{
