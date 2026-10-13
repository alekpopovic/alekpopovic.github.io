# ch30-source-anchor

Explain source revision provenance and deterministic manifest order. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/gitops/gitops.go, lines 198–217](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L198-L217).

```go
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
```

SHA-256: `88c50034cc084ba59ec295c77ca71107f584e87d68d124032da6e5717706b924`. This excerpt is not an independently compilable program.
