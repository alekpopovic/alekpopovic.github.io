func lockQuota(ctx context.Context, db postgresDB, namespaceName string) error {
	_, err := db.Exec(ctx, `SELECT pg_advisory_xact_lock(hashtextextended($1, 0))`, namespaceName)
	return mapPostgresError(err)
}

func lockAndCheckQuota(ctx context.Context, db postgresDB, namespaceName string, replaceID types.ServiceID, replacement *types.ServiceSpec, addSecrets int, addRegistries int) error {
	if err := lockQuota(ctx, db, namespaceName); err != nil {
		return err
	}
	value, usage, err := loadQuotaAndUsage(ctx, db, namespaceName, replaceID, replacement, false)
	if err != nil {
		return err
	}
	usage.Secrets += addSecrets
	usage.RegistryCredentials += addRegistries
	return quota.Check(value, usage)
}
