func (c *Controller) RunOnce(ctx context.Context) error {
	if c.controlPlane == nil {
		return fmt.Errorf("autoscaler control plane is required")
	}
	if c.provider == nil {
		return fmt.Errorf("autoscaler metrics provider is required")
	}
	services, err := c.controlPlane.ListServices(ctx)
	if err != nil {
		c.metrics.IncAutoscalerErrors()
		return fmt.Errorf("list services: %w", err)
	}
	for _, service := range services {
		if err := ctx.Err(); err != nil {
			return err
		}
		if !service.Spec.Autoscaling.Enabled || service.Status != types.ServiceActive {
			continue
		}
		if err := c.reconcileService(ctx, service); err != nil {
