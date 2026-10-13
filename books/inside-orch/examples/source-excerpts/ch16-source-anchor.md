# ch16-source-anchor

Locate actual log stream boundaries and response formats. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/agent/logs.go, lines 16–35](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/logs.go#L16-L35).

```go
func WithMetricsHandler(handler http.Handler) LogHandlerOption {
	return func(server *logServer) {
		server.metricsHandler = handler
	}
}

func NewLogHandler(runtime orchdocker.Runtime, token string, logger *slog.Logger, opts ...LogHandlerOption) http.Handler {
	if logger == nil {
		logger = slog.Default()
	}
	server := &logServer{runtime: runtime, token: token, logger: logger}
	for _, opt := range opts {
		opt(server)
	}
	mux := http.NewServeMux()
	if server.metricsHandler != nil {
		mux.Handle("GET /metrics", server.metricsHandler)
	}
	mux.HandleFunc("GET /v1/agent/logs", server.streamLogs)
	return mux
```

SHA-256: `39618a4143b1d3b547b9f1074d006388623d17c0036677857c6bd0bad6db69f4`. This excerpt is not an independently compilable program.
