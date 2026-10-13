	switch task.ActualStatus {
	case types.TaskRunning, types.TaskHealthy:
		job.Status = types.JobRunning
	case types.TaskStopped:
		code := 0
		if task.ExitCode != nil {
			code = *task.ExitCode
		}
		job.LastExitCode = &code
		if code == 0 {
			job.Status = types.JobSucceeded
			job.CompletedAt = now
		} else {
			s.retryOrFailJobLocked(&job, task, now)
		}
	case types.TaskFailed:
		code := 1
		if task.ExitCode != nil {
			code = *task.ExitCode
		}
		job.LastExitCode = &code
		s.retryOrFailJobLocked(&job, task, now)
	}
	job.UpdatedAt = now
	s.jobs[job.ID] = job
}

