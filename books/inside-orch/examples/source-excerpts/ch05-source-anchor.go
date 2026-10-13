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

