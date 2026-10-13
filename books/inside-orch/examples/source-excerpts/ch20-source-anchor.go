func BuildServiceEndpoints(service types.Service, tasks []types.Task, nodes []types.Node, includeUnhealthy bool) ServiceEndpoints {
	nodesByID := make(map[types.NodeID]types.Node, len(nodes))
	for _, node := range nodes {
		nodesByID[node.ID] = node
	}
	endpoints := make([]Endpoint, 0)
	for _, task := range tasks {
		if task.ServiceID != service.ID || task.NodeID == "" {
			continue
		}
		if !includeTask(task, includeUnhealthy) {
			continue
		}
		node, ok := nodesByID[task.NodeID]
		if !ok {
			continue
		}
		for _, port := range taskPorts(task, service) {
			if port.ContainerPort == 0 {
				continue
