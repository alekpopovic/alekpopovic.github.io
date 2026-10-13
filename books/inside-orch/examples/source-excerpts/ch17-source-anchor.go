func rolloutStateFor(deployment types.Deployment, service types.Service, tasks []types.Task) rolloutState {
	state := rolloutState{}
	for _, task := range tasks {
		if task.Version == deployment.FromVersion {
			if isActive(task) {
				state.oldActive++
				state.oldTasks = append(state.oldTasks, task)
				if isAvailable(task) {
					state.available++
				}
			} else {
				state.oldStopped++
			}
			continue
		}
		if task.Version != deployment.ToVersion {
			continue
		}
		if task.ActualStatus == types.TaskFailed {
			state.newFailed++
