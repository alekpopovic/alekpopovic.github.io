	for {
		err := operation()
		if err == nil {
			return nil
		}
		delay := backoff + time.Duration(rng.Int63n(int64(backoff)))
		timer := time.NewTimer(delay)
		select {
		case <-ctx.Done():
			timer.Stop()
			return ctx.Err()
		case <-timer.C:
		}
		if backoff < 5*time.Second {
			backoff *= 2
		}
	}
}

func DetectCapacity() types.Resources {
	return types.Resources{
