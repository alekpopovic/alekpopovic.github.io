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
