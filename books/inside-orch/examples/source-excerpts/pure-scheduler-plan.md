# pure-scheduler-plan

Standalone planner entrypoint: inspect its callers before transferring invariants to the binary.

Unchanged, contiguous source excerpt: [internal/scheduler/scheduler.go, lines 270–298](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L270-L298).

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
		}
		assignments = append(assignments, Assignment{
			TaskID:            task.ID,
			NodeID:            node.ID,
			Ports:             ports,
			ExpectedUpdatedAt: task.UpdatedAt.UTC(),
		})
		state.addPlanned(node.ID, task, service.Spec.ResourceRequirements.Requests, ports)
	}
```

SHA-256: `b7b5ad28ebad58aff63854fc85a4603e539ae413d925ae1ac6e2bcc0ad5759b5`. This excerpt is not an independently compilable program.
