# ch12-source-anchor

Identify idempotency keys and managed-container labels. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/docker/docker.go, lines 191–210](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L191-L210).

```go
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
```

SHA-256: `097b7a4fdc38f813109292018b5db92667201013ac3634fcd1626db22645b0e0`. This excerpt is not an independently compilable program.
