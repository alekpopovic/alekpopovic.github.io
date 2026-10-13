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
