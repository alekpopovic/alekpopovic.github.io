		Env:          env,
		Labels:       labels,
		ExposedPorts: exposedPorts,
		Cmd:          spec.Command,
		Healthcheck:  dockerHealthcheck(spec.Healthcheck),
		User:         spec.Security.User,
	}
	hostConfig := &container.HostConfig{
		PortBindings: portBindings,
		RestartPolicy: container.RestartPolicy{
			Name: "no",
		},
		Resources: container.Resources{
			Memory:   spec.Resources.Memory,
			NanoCPUs: spec.Resources.CPUMilli * 1_000_000,
		},
		Privileged:     spec.Security.Privileged,
		ReadonlyRootfs: spec.Security.ReadOnlyRootFilesystem,
		CapAdd:         append([]string(nil), spec.Security.CapAdd...),
