# ch08-source-anchor

Explain flag, environment, configuration, and default precedence. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/config/config.go, lines 123–142](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go#L123-L142).

```go
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
```

SHA-256: `588e8687cc2f5caf22c7c8c959196307638634dab194763b2cc6e67f94ef861b`. This excerpt is not an independently compilable program.
