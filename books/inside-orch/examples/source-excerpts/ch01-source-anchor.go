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
