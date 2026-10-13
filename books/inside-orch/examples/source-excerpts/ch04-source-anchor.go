func ValidateTaskTransition(from TaskStatus, to TaskStatus) error {
	if !ValidTaskStatus(from) || !ValidTaskStatus(to) {
		return invalidTransition("task", from, to)
	}
	if from == to {
		return nil
	}
	if IsTerminalTaskStatus(from) {
		if to == TaskRemoved && from != TaskRemoved {
			return nil
		}
		return invalidTransition("task", from, to)
	}
	switch from {
	case TaskPending:
		if to == TaskAssigned || to == TaskStopped || to == TaskRemoved || to == TaskFailed {
			return nil
		}
	case TaskAssigned:
		if to == TaskPulling || to == TaskCreated || to == TaskRunning || to == TaskHealthy || to == TaskUnhealthy || to == TaskStopping || to == TaskStopped || to == TaskRemoved || to == TaskFailed {
