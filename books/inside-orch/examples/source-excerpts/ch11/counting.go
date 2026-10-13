	for _, task := range tasks {
		if task.Version != service.DeploymentVersion {
			if isNonTerminal(task) {
				outdated = append(outdated, task)
			}
			continue
		}
		if isNonTerminal(task) {
			current = append(current, task)
			continue
		}
		if task.ActualStatus == types.TaskFailed && !restartAllowed(service.Spec.RestartPolicy) {
			nonRestartableFailed++
		}
	}

	for _, task := range stopOrder(outdated) {
		if err := ctx.Err(); err != nil {
			return result, err
