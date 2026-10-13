func (s *MemoryService) retryOrFailJobLocked(job *types.Job, previous types.Task, now time.Time) {
	if job.Attempts > job.Spec.BackoffLimit {
		job.Status = types.JobFailed
		job.CompletedAt = now
		return
	}
	job.Attempts++
	task := previous
	task.ID = types.TaskID(newUUID())
	task.NodeID = ""
	task.ContainerID = ""
	task.ActualStatus = types.TaskPending
	task.DesiredStatus = types.TaskRunning
	task.RestartCount = job.Attempts - 1
	task.ExitCode = nil
	task.FailureReason = ""
	task.CreatedAt = now
	task.UpdatedAt = now
	task.StartedAt = time.Time{}
	task.FinishedAt = time.Time{}
	s.tasks[task.ID] = task
	job.TaskIDs = append(job.TaskIDs, task.ID)
	job.Status = types.JobPending
}

