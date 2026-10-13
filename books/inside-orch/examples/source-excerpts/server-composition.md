# server-composition

The concrete MemoryService constructor controls live state ownership.

Unchanged, contiguous source excerpt: [cmd/orch-server/main.go, lines 142–158](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L142-L158).

```go
	envelope, err := secrets.NewLocalEnvelope(cfg.SecretKey)
	if err != nil {
		return err
	}
	controlPlane := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope), controlplane.WithClusterPolicy(cfg.ClusterPolicy), controlplane.WithRetentionConfig(cfg.Retention))
	controlPlane.SetNotificationDispatcher(notifications.NewDispatcher(controlPlane, nil))
	serverMetrics := metrics.NewServer()
	if dnsAddress := os.Getenv("ORCH_DNS_ADDR"); dnsAddress != "" {
		dnsTTL := 30 * time.Second
		if raw := os.Getenv("ORCH_DNS_TTL"); raw != "" {
			parsed, parseErr := time.ParseDuration(raw)
			if parseErr != nil || parsed <= 0 {
				return fmt.Errorf("ORCH_DNS_TTL must be a positive duration")
			}
			dnsTTL = parsed
		}
		dnsServer := orchdns.New(controlPlane, dnsTTL, "default", serverMetrics)
```

SHA-256: `0bbd79dd7489b8800dfad63b9a0b6f5aa9379299834f1b41a97bc2706e433e37`. This excerpt is not an independently compilable program.
