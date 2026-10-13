func (r *EngineRuntime) CreateContainer(ctx context.Context, spec ContainerSpec) (ContainerID, error) {
	if err := spec.Validate(); err != nil {
		return "", err
	}

	existing, err := r.findContainerForTask(ctx, spec.TaskID)
	if err == nil {
		return existing.ID, nil
	}
	if err != nil && !errdefs.IsNotFound(err) {
		return "", err
	}

	config, hostConfig, err := dockerContainerConfig(spec)
	if err != nil {
		return "", err
	}
	response, err := r.client.ContainerCreate(ctx, config, hostConfig, &network.NetworkingConfig{}, nil, spec.Name)
	if err != nil {
		if errdefs.IsConflict(err) {
