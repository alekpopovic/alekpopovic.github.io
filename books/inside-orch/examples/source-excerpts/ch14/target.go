	port, ok := healthcheckProbePort(check.Port, ports)
	if !ok {
		return health.Check{}, false
	}
	timeout := check.Timeout
	if timeout <= 0 {
		timeout = 2 * time.Second
	}
	target := "127.0.0.1:" + strconv.Itoa(port)
	switch check.Type {
	case types.HealthcheckHTTP:
		path := check.Path
		if !strings.HasPrefix(path, "/") {
			path = "/" + path
		}
		scheme := strings.ToLower(strings.TrimSpace(check.Scheme))
		if scheme == "" {
			scheme = "http"
		}
		return health.Check{Type: health.HTTPProbe, Target: scheme + "://" + target + path, Timeout: timeout}, true
	case types.HealthcheckTCP:
		return health.Check{Type: health.TCPProbe, Target: target, Timeout: timeout}, true
	default:
		return health.Check{}, false
