func (s *postgresStore) withTx(ctx context.Context, fn func(*postgresStore) error) error {
	if s.begin == nil {
		return fn(s)
	}
	tx, err := s.begin(ctx)
	if err != nil {
		return mapPostgresError(err)
	}
	txStore := &postgresStore{db: tx}
	defer rollback(ctx, tx)
	if err := fn(txStore); err != nil {
		return err
	}
	return mapPostgresError(tx.Commit(ctx))
}
