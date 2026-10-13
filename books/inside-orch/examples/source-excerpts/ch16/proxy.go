	baseURL := normalizeAgentURL(req.AgentURL)
	values := url.Values{}
	values.Set("task_id", req.TaskID)
	if req.Follow {
		values.Set("follow", "true")
	}
	if strings.TrimSpace(req.Tail) != "" {
		values.Set("tail", strings.TrimSpace(req.Tail))
	}
	httpReq, err := http.NewRequestWithContext(ctx, http.MethodGet, baseURL+"/v1/agent/logs?"+values.Encode(), nil)
	if err != nil {
		return fmt.Errorf("create agent logs request: %w", err)
	}
	if req.Token != "" {
		httpReq.Header.Set("Authorization", "Bearer "+req.Token)
	}
	resp, err := client.Do(httpReq)
	if err != nil {
		return fmt.Errorf("request agent logs: %w", err)
