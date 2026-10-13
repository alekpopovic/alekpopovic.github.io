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
