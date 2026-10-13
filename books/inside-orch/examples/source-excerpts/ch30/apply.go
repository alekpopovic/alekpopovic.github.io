	syncCtx := namespace.WithContext(ctx, source.Namespace)
	managed := make([]string, 0, len(files))
	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("read manifest %q: %w", file, err))
		}
		spec, err := controller.parser(data)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("validate manifest %q: %w", file, err))
		}
		service, err := controller.store.ApplyService(syncCtx, spec)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("apply service %q: %w", spec.Name, err))
		}
		if marker, ok := controller.store.(managedStore); ok {
			relative, _ := filepath.Rel(checkout.Directory, file)
			policy := source.DriftPolicy
