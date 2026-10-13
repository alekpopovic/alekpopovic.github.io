# ch38-source-anchor

Map an emitted metric to a subsystem and failure mode. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/metrics/prometheus.go, lines 41–60](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go#L41-L60).

```go
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
```

SHA-256: `cc35884092df6c73b8cbb6c4ea38b732795957a53cb53971170f7c301d42e545`. This excerpt is not an independently compilable program.
