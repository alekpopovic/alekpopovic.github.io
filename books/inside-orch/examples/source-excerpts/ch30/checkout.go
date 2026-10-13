	cleanup := func() { _ = os.RemoveAll(directory) }
	args := []string{"clone", "--depth=1", "--single-branch", "--branch", source.Branch, "--", source.RepositoryURL, directory}
	command := exec.CommandContext(ctx, "git", args...)
	if output, err := command.CombinedOutput(); err != nil {
		cleanup()
		return Checkout{}, fmt.Errorf("clone repository: %w: %s", err, strings.TrimSpace(string(output)))
	}
	revisionBytes, err := exec.CommandContext(ctx, "git", "-C", directory, "rev-parse", "HEAD").Output()
	if err != nil {
		cleanup()
		return Checkout{}, fmt.Errorf("resolve checkout revision: %w", err)
	}
	return Checkout{Directory: directory, Revision: strings.TrimSpace(string(revisionBytes)), Cleanup: cleanup}, nil
