# ch31-source-anchor

Trace Job exit status to success, failure, or retry. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/cronjobs/cronjobs.go, lines 55–74](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go#L55-L74).

```go
func (c *Controller) RunOnce(ctx context.Context) error {
	items, err := c.store.ListCronJobs(ctx)
	if err != nil {
		return err
	}
	now := c.clock.Now().UTC()
	for _, item := range items {
		loc, err := time.LoadLocation(item.Spec.Timezone)
		if err != nil {
			return fmt.Errorf("cronjob %s timezone: %w", item.ID, err)
		}
		schedule, err := Parse(item.Spec.Schedule)
		if err != nil {
			return fmt.Errorf("cronjob %s schedule: %w", item.ID, err)
		}
		base := item.LastScheduleAt
		if base.IsZero() {
			base = item.CreatedAt
		}
		due := schedule.Between(base.In(loc), now.In(loc), item.Spec.MissedScheduleLimit)
```

SHA-256: `d7ca1f0b7a5e4963ef0aa36402921ed62d13fdb566b8d369e1f7ed303bfb7cd5`. This excerpt is not an independently compilable program.
