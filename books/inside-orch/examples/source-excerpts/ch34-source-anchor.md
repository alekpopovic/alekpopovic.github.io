# ch34-source-anchor

Explain per-controller leadership versus API availability. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/leadership/postgres.go, lines 21–40](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L21-L40).

```go
func (e *PostgresElector) Acquire(ctx context.Context, name string) (Lease, error) {
	if e.pool == nil {
		return nil, fmt.Errorf("postgres pool is required")
	}
	conn, err := e.pool.Acquire(ctx)
	if err != nil {
		return nil, fmt.Errorf("acquire lock connection: %w", err)
	}
	key := advisoryLockKey(name)
	var acquired bool
	if err := conn.QueryRow(ctx, `SELECT pg_try_advisory_lock($1)`, key).Scan(&acquired); err != nil {
		conn.Release()
		return nil, fmt.Errorf("try advisory lock %s: %w", name, err)
	}
	if !acquired {
		conn.Release()
		return nil, fmt.Errorf("%w: %s", ErrLockHeld, name)
	}
	lease := &postgresLease{
		name:          name,
```

SHA-256: `b0bf391e2230ad37a500110c269a48c78dea1abed0d23e2f57c017ebdd731225`. This excerpt is not an independently compilable program.
