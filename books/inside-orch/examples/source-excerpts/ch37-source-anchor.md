# ch37-source-anchor

Define an invariant before injecting a fault. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/e2e/chaos_test.go, lines 19–38](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L19-L38).

```go
func TestChaosScenarios(t *testing.T) {
	t.Run("agent restarts during task start", func(t *testing.T) {
		ctx := context.Background()
		cp, node := chaosControlPlane(t)
		service := chaosService(t, ctx, cp, "restart-during-start", 1)
		task := chaosTask(t, ctx, cp, service.ID)

		if _, err := cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: node, Status: types.TaskRunning, ContainerID: "container-1"}); err != nil {
			t.Fatalf("first running report: %v", err)
		}
		if _, err := cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: node, Status: types.TaskRunning, ContainerID: "container-1"}); err != nil {
			t.Fatalf("idempotent running report after restart: %v", err)
		}
		tasks, err := cp.ListTasks(ctx, controlplane.TaskFilter{ServiceID: service.ID})
		if err != nil {
			t.Fatalf("list tasks: %v", err)
		}
		if len(tasks) != 1 || tasks[0].ActualStatus != types.TaskRunning {
			t.Fatalf("expected one running task after restart, got %#v", tasks)
		}
```

SHA-256: `312c9d070ffb0845f6eb120e7a2c95d0d6be6f162af97dee65be21a17ca09387`. This excerpt is not an independently compilable program.
