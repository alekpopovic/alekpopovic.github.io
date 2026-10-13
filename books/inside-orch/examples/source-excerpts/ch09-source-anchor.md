# ch09-source-anchor

Identify transaction boundaries and optimistic conflict checks. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/store/postgres.go, lines 892–911](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L892-L911).

```go
func (s *postgresStore) AssignTask(ctx context.Context, id types.TaskID, nodeID types.NodeID, ports []types.Port, expectedUpdatedAt time.Time) (types.Task, error) {
	current, err := s.getTask(ctx, id, s.begin == nil)
	if err != nil {
		if errors.Is(err, ErrNotFound) && s.begin == nil {
			if _, getErr := s.getTask(ctx, id, false); errors.Is(getErr, ErrNotFound) {
				return types.Task{}, ErrNotFound
			} else if getErr != nil {
				return types.Task{}, getErr
			}
			return types.Task{}, ErrConflict
		}
		return types.Task{}, err
	}
	if err := types.ValidateTaskTransition(current.ActualStatus, types.TaskAssigned); err != nil {
		return types.Task{}, fmt.Errorf("%w: %v", ErrInvalidState, err)
	}
	portBytes, err := jsonBytes(defaultSlice(ports))
	if err != nil {
		return types.Task{}, err
	}
```

SHA-256: `95fdc88cf5e7a872aa277153b2efc11a6c27b3acd0393ee074deb182e63e8254`. This excerpt is not an independently compilable program.
