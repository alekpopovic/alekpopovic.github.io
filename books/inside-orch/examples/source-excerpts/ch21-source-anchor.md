# ch21-source-anchor

Trace ingress to node-level published ports. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/traefik/config.go, lines 46–65](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L46-L65).

```go
func BuildConfig(services []types.Service, endpointSets []discovery.ServiceEndpoints) Config {
	config := Config{
		HTTP: HTTPConfig{
			Routers:  make(map[string]Router),
			Services: make(map[string]Service),
		},
	}
	endpointsByServiceID := endpointsByService(endpointSets)
	orderedServices := append([]types.Service(nil), services...)
	sortServices(orderedServices)

	for _, service := range orderedServices {
		if service.Status != "" && service.Status != types.ServiceActive {
			continue
		}
		endpointSet := endpointsByServiceID[service.ID]
		for routeIndex, route := range service.Spec.Routes {
			if err := route.Validate(); err != nil {
				continue
			}
```

SHA-256: `f0dcf8acc9ff3155783329db1b2f5b565c491367f5fafadcb59c6abee456840c`. This excerpt is not an independently compilable program.
