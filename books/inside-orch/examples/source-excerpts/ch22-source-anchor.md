# ch22-source-anchor

Calculate a replica recommendation from observed CPU. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/autoscaler/autoscaler.go, lines 114–133](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L114-L133).

```go
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
```

SHA-256: `fc424f33ad0c20ad5b94e1b63bea67d056d355772bc5c03b91c016bc8a33e23a`. This excerpt is not an independently compilable program.
