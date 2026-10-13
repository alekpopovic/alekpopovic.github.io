func managedLabels(spec ContainerSpec) map[string]string {
	labels := make(map[string]string, len(spec.Labels)+5)
	for key, value := range spec.Labels {
		labels[key] = value
	}
	labels[ManagedLabel] = "true"
	labels[ServiceIDLabel] = spec.ServiceID
	labels[TaskIDLabel] = spec.TaskID
	labels[NodeIDLabel] = spec.NodeID
	labels[VersionLabel] = strconv.FormatInt(spec.Version, 10)
	return labels
}
