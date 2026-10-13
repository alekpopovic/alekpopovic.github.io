# ch10-source-anchor

Explain deterministic ordering and tie-breaking. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/scheduler/scheduler.go, lines 270–289](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L270-L289).

```go
func Plan(input PlanInput) []Assignment {
	pending := sortedTasks(input.PendingTasks)
	nodes := sortedNodes(input.Nodes)
	state := newClusterState(nodes, input.RunningTasks, input.Services)

	assignments := make([]Assignment, 0, len(pending))
	for _, task := range pending {
		if task.ActualStatus != types.TaskPending {
			continue
		}
		service, ok := input.Services[task.ServiceID]
		if !ok && task.JobID != "" {
			service, ok = jobTaskService(task)
		}
		if !ok {
			continue
		}
		node, ports, ok := bestNode(task, service, nodes, state)
		if !ok {
			continue
```

SHA-256: `0bd286216c8bdafd5c4d9bbecf4e573878f7e65e8eb91f163036a0b330b89c4c`. This excerpt is not an independently compilable program.
