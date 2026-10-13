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
