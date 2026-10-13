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
