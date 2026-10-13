# ch28-source-anchor

Calculate namespace requested CPU/memory and port usage. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/quota/quota.go, lines 18–37](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/quota/quota.go#L18-L37).

```go
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
```

SHA-256: `5154d664c39c0dcc473d679498a57c2276f8a5609c2155f6671bac07e52a0106`. This excerpt is not an independently compilable program.
