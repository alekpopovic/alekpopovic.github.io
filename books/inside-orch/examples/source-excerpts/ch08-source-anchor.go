func LoadCLI(path string, overrides CLIOverrides) (CLIConfig, error) {
	cfg := CLIConfig{}
	if strings.TrimSpace(path) != "" {
		file, err := readOptionalYAMLFile[CLIConfig](path)
		if err != nil {
			return CLIConfig{}, err
		}
		cfg = file
	}
	if value := strings.TrimSpace(os.Getenv("ORCH_SERVER_URL")); value != "" {
		cfg.ServerURL = value
	}
	if value := strings.TrimSpace(os.Getenv("ORCH_TOKEN")); value != "" {
		cfg.Token = value
	}
	if value := strings.TrimSpace(os.Getenv("ORCH_NAMESPACE")); value != "" {
		cfg.Namespace = value
	}
	if strings.TrimSpace(overrides.ServerURL) != "" {
		cfg.ServerURL = strings.TrimSpace(overrides.ServerURL)
