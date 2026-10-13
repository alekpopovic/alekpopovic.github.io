# ch01-source-anchor

Trace a service from API request to Docker container. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [cmd/orch-server/main.go, lines 146–165](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L165).

```go
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
		go func() {
			if err := dnsServer.ServeUDP(ctx, dnsAddress); err != nil && !errors.Is(err, context.Canceled) {
				logger.Warn("internal DNS stopped", "error", err)
			}
		}()
	}
	gitopsController := gitops.NewController(controlPlane, nil, cli.ParseDeploy, logger)
```

SHA-256: `86d6f1461361cfd02ab904e1bb29c6e4c9365e7c4f609e33432c4053cfadca73`. This excerpt is not an independently compilable program.
