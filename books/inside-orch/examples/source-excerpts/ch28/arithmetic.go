func addServiceUsage(usage *types.ResourceUsage, spec types.ServiceSpec) {
	usage.Services++
	usage.Replicas += spec.Replicas
	usage.CPUMillicores += spec.ResourceRequirements.Requests.CPU * int64(spec.Replicas)
	usage.MemoryBytes += spec.ResourceRequirements.Requests.Memory * int64(spec.Replicas)
	for _, port := range spec.Ports {
		if port.PublishedPort > 0 {
			usage.PublicPorts++
		}
	}
}
