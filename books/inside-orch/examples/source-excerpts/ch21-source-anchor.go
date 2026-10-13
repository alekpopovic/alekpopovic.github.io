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
