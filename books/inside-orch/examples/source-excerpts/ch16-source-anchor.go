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
