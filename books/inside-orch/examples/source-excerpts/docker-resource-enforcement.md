# docker-resource-enforcement

Adapter support for resource limits is distinct from populated agent inputs.

Unchanged, contiguous source excerpt: [internal/docker/docker.go, lines 422–440](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L422-L440).

```go
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
```

SHA-256: `416bf032c2d9ea3b4858761a56a32b094c3b6dff47cfe272487ad86e3f4d1ea1`. This excerpt is not an independently compilable program.
