# ch13-source-anchor

Follow agent bootstrap and credential use. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/agent/agent.go, lines 128–147](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L128-L147).

```go
func (r *Runner) Run(ctx context.Context) error {
	if err := r.cfg.Validate(); err != nil {
		return err
	}
	if r.client == nil {
		client, err := NewHTTPClient(r.cfg.ServerURL, r.cfg.BootstrapToken)
		if err != nil {
			return err
		}
		r.client = client
	}
	if r.runtime == nil {
		runtime, err := orchdocker.NewEngineRuntimeFromEnv()
		if err != nil {
			return err
		}
		r.runtime = runtime
	}

	capacity := DetectCapacity()
```

SHA-256: `422d6bb8515b841abc7aeb8f25e90f56488eace76d32243128da963d71e1c7d6`. This excerpt is not an independently compilable program.
