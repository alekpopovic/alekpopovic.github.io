# ch11-source-anchor

Separate reconciliation decisions from placement and runtime side effects. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/reconciler/reconciler.go, lines 125–144](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L125-L144).

```go
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
```

SHA-256: `a9a970da055cb6821f28997d84b67767edd2093e9109afe9871a83cafc4f51a7`. This excerpt is not an independently compilable program.
