# ch19-source-anchor

Interpret stale heartbeat transitions. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/node/monitor.go, lines 57–72](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/monitor.go#L57-L72).

```go
func (m *Monitor) CheckOnce(ctx context.Context) ([]types.Node, error) {
	if m.controlPlane == nil {
		return nil, fmt.Errorf("node monitor control plane is required")
	}
	if m.timeout <= 0 {
		return nil, fmt.Errorf("node heartbeat timeout must be positive")
	}
	offline, err := m.controlPlane.MarkStaleNodesOffline(ctx, m.timeout)
	if err != nil {
		return nil, err
	}
	for _, node := range offline {
		m.logger.Warn("node marked offline after stale heartbeat", "node_id", node.ID, "last_heartbeat_at", node.LastHeartbeatAt)
	}
	return offline, nil
}
```

SHA-256: `f0b4ac85bcc719b2782ea7b337b7ab67cc030187a8140db55db6d7f230ecf221`. This excerpt is not an independently compilable program.
