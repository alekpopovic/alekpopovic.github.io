
		stdoutReader, stdoutWriter := io.Pipe()
		stderrReader, stderrWriter := io.Pipe()
		copyErr := make(chan error, 1)
		go func() {
			_, err := stdcopy.StdCopy(stdoutWriter, stderrWriter, reader)
			_ = stdoutWriter.Close()
			_ = stderrWriter.Close()
			copyErr <- err
		}()
