# ch20-source-anchor

Explain endpoint identity and health filtering. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/discovery/discovery.go, lines 28–47](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery.go#L28-L47).

```go
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
```

SHA-256: `7d494a6f5cf931e4d54d0190ed5adcc542f830654f41784db7730617ead17597`. This excerpt is not an independently compilable program.
