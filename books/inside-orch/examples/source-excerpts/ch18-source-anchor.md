# ch18-source-anchor

Explain why removal is a workflow rather than one HTTP delete. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/controlplane/controlplane.go, lines 1436–1455](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L1436-L1455).

```go
func (s *MemoryService) DeleteService(ctx context.Context, id types.ServiceID) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	s.mu.Lock()
	defer s.mu.Unlock()

	service, ok := s.services[id]
	if !ok || !namespace.Matches(ctx, service.Namespace) {
		return store.ErrNotFound
	}
	if service.Status == types.ServiceDeleted || service.Status == types.ServiceDeleting {
		return nil
	}
	if err := types.ValidateServiceTransition(service.Status, types.ServiceDeleting); err != nil {
		return fmt.Errorf("%w: %v", store.ErrInvalidState, err)
	}
	now := s.now()
	s.cancelActiveDeploymentsLocked(id, now, "service deletion requested")
	service.Status = types.ServiceDeleting
```

SHA-256: `a0cecb857a301043368e7f01c9f94951e32fe814c2b5e3eb4ea565402c85209e`. This excerpt is not an independently compilable program.
