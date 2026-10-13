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
