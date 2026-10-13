# ch17-source-anchor

Compute rollout availability and surge limits. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/rollout/rollout.go, lines 358–377](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go#L358-L377).

```go
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
```

SHA-256: `9459109426133e4923c1ce53cdee4701437e9af076d977ad426d0946bd3c3410`. This excerpt is not an independently compilable program.
