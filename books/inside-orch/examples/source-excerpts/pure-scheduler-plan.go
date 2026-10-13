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
