# ch15-source-anchor

Differentiate domain events, diagnostic logs, and audits. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/events/events.go, lines 71–90](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/events/events.go#L71-L90).

```go
func Strict() EmitOption {
	return func(cfg *emitConfig) {
		cfg.strict = true
	}
}

func WithLogger(logger *slog.Logger) EmitOption {
	return func(cfg *emitConfig) {
		cfg.logger = logger
	}
}

func Emit(ctx context.Context, store Store, event types.Event, opts ...EmitOption) error {
	if store == nil {
		return nil
	}
	cfg := emitConfig{logger: slog.Default()}
	for _, opt := range opts {
		opt(&cfg)
	}
```

SHA-256: `fdd7c24ede8b244f6d46fdb6255ebd777f9e0b8a70aa9014ceb64f4eb97efe7c`. This excerpt is not an independently compilable program.
