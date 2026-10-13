# ch39-source-anchor

Separate fake control-plane throughput from real Docker capacity. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/scheduler/benchmark_test.go, lines 9–26](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/benchmark_test.go#L9-L26).

```go
func BenchmarkSchedulerScoring(b *testing.B) {
	nodes := make([]types.Node, 100)
	for i := range nodes {
		nodes[i] = types.Node{ID: types.NodeID(fmt.Sprintf("node-%03d", i)), Status: types.NodeReady, Allocatable: types.Resources{CPU: 8000, Memory: 16 << 30}}
	}
	services := map[types.ServiceID]types.Service{}
	tasks := make([]types.Task, 1000)
	for i := range tasks {
		id := types.ServiceID(fmt.Sprintf("service-%04d", i))
		services[id] = types.Service{ID: id, Status: types.ServiceActive, Spec: types.ServiceSpec{Name: string(id), Image: "nginx", ResourceRequirements: types.ResourceRequirements{Requests: types.Resources{CPU: 100, Memory: 64 << 20}}}}
		tasks[i] = types.Task{ID: types.TaskID(fmt.Sprintf("task-%04d", i)), ServiceID: id, ActualStatus: types.TaskPending}
	}
	input := PlanInput{PendingTasks: tasks, Nodes: nodes, Services: services}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = Plan(input)
	}
}
```

SHA-256: `99c80c9aa096a0e8747b76550acdd4f55959417c7f8414a1b5bc72e9056cea78`. This excerpt is not an independently compilable program.
