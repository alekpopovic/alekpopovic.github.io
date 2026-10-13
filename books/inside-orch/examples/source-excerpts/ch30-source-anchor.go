func (controller *Controller) Sync(ctx context.Context, id string) (types.GitOpsSource, error) {
	source, err := controller.store.GetGitOpsSource(ctx, id)
	if err != nil {
		return types.GitOpsSource{}, err
	}
	if err := ValidateSource(source); err != nil {
		return controller.fail(ctx, source, err)
	}
	checkout, err := controller.fetcher.Checkout(ctx, source)
	if err != nil {
		return controller.fail(ctx, source, err)
	}
	if checkout.Cleanup != nil {
		defer checkout.Cleanup()
	}
	files, err := manifestFiles(checkout.Directory, source.Path)
	if err != nil {
		return controller.fail(ctx, source, err)
	}

