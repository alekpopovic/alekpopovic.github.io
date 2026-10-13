# ch05-source-anchor

Parse CPU and memory quantities without ambiguity. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/cli/deploy.go, lines 129–148](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go#L129-L148).

```go
func ParseDeploy(data []byte) (types.ServiceSpec, error) {
	var deploy DeployFile
	decoder := yaml.NewDecoder(bytes.NewReader(data))
	decoder.KnownFields(true)
	if err := decoder.Decode(&deploy); err != nil {
		return types.ServiceSpec{}, fmt.Errorf("parse deploy YAML: %w", err)
	}
	if err := deploy.Validate(); err != nil {
		return types.ServiceSpec{}, fmt.Errorf("invalid deploy file: %w", err)
	}

	requests, err := deploy.Resources.toRequests()
	if err != nil {
		return types.ServiceSpec{}, err
	}
	autoscaling, err := deploy.Autoscaling.toDomain()
	if err != nil {
		return types.ServiceSpec{}, err
	}
```

SHA-256: `f8b78e4b111d8d0e29f8ad2571d1988d5de6bc1ec3c0974f643b0e223aa2a85b`. This excerpt is not an independently compilable program.
