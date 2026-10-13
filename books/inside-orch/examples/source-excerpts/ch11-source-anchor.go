func (r *Reconciler) ReconcileOnce(ctx context.Context) error {
	r.metrics.IncReconciliationRuns()
	if r.store == nil {
		r.metrics.IncReconciliationErrors()
		return fmt.Errorf("reconciler store is required")
	}
	if err := ctx.Err(); err != nil {
		r.metrics.IncReconciliationErrors()
		return err
	}

	started := r.now()
	lease, err := r.lock.Acquire(ctx)
	if err != nil {
		r.metrics.IncReconciliationErrors()
		return fmt.Errorf("acquire leader lock: %w", err)
	}
	defer func() {
		if lease != nil {
			if err := lease.Release(context.Background()); err != nil {
