func NewServer() *Server {
	m := &Server{
		registry: prometheus.NewRegistry(),
		apiRequests: prometheus.NewCounterVec(prometheus.CounterOpts{
			Name: "api_requests_total",
			Help: "Total API requests by method, route, and status code.",
		}, []string{"method", "route", "status"}),
		apiRequestDuration: prometheus.NewHistogramVec(prometheus.HistogramOpts{
			Name:    "api_request_duration_seconds",
			Help:    "API request duration in seconds by method, route, and status code.",
			Buckets: prometheus.DefBuckets,
		}, []string{"method", "route", "status"}),
		schedulerRuns: prometheus.NewCounter(prometheus.CounterOpts{
			Name: "scheduler_runs_total",
			Help: "Total scheduler runs.",
		}),
		schedulerErrors: prometheus.NewCounter(prometheus.CounterOpts{
			Name: "scheduler_errors_total",
			Help: "Total scheduler run errors.",
		}),
