func scanLogStream(ctx context.Context, reader io.Reader, stream string, out chan<- LogLine, done chan<- error) {
	scanner := bufio.NewScanner(reader)
	for scanner.Scan() {
		select {
		case <-ctx.Done():
			done <- ctx.Err()
			return
		case out <- LogLine{Stream: stream, Line: scanner.Text(), Timestamp: time.Now().UTC()}:
		}
	}
	done <- scanner.Err()
}
