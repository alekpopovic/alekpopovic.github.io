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
