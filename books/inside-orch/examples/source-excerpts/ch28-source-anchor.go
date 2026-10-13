func (e *Error) Error() string {
	return fmt.Sprintf("namespace %q quota exceeded for %s: limit %d, used %d, requested %d", e.Namespace, e.Resource, e.Limit, e.Used, e.Requested)
}

func Validate(value types.ResourceQuota) error {
	if strings.TrimSpace(value.Namespace) == "" {
		return fmt.Errorf("namespace is required")
	}
	if value.MaxServices < 0 || value.MaxReplicas < 0 || value.MaxCPUMillicores < 0 || value.MaxMemoryBytes < 0 || value.MaxPublicPorts < 0 || value.MaxSecrets < 0 || value.MaxRegistryCredentials < 0 {
		return fmt.Errorf("quota limits cannot be negative")
	}
	return nil
}

func Check(value types.ResourceQuota, usage types.ResourceUsage) error {
	checks := []struct {
		name  string
		limit int64
		used  int64
	}{
