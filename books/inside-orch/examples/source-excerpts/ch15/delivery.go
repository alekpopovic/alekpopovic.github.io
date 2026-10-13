	var last error
	for attempt := 0; attempt < s.attempts; attempt++ {
		req, err := http.NewRequestWithContext(ctx, http.MethodPost, sink.URL, bytes.NewReader(payload))
		if err != nil {
			return err
		}
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("User-Agent", "orch-notifier/1")
		if sink.SigningSecret != "" {
			mac := hmac.New(sha256.New, []byte(sink.SigningSecret))
			_, _ = mac.Write(payload)
			req.Header.Set("X-Orch-Signature", "sha256="+hex.EncodeToString(mac.Sum(nil)))
		}
		resp, err := s.client.Do(req)
		if err == nil {
			_, _ = io.Copy(io.Discard, resp.Body)
			_ = resp.Body.Close()
			if resp.StatusCode >= 200 && resp.StatusCode < 300 {
				return nil
			}
