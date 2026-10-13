# ch04-source-anchor

Distinguish desired task status from observed status. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [pkg/types/lifecycle.go, lines 136–155](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L136-L155).

```go
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
```

SHA-256: `9522cf0609116b3b608f9d0de4b29882944fc855a54dbffb5dc073f73a2bcdc6`. This excerpt is not an independently compilable program.
