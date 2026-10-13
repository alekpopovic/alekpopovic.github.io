func Discover(directory string) ([]Migration, error) {
	entries, err := os.ReadDir(directory)
	if err != nil {
		return nil, err
	}
	byVersion := map[string]*Migration{}
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		name := entry.Name()
		parts := strings.SplitN(name, "_", 2)
		if len(parts) != 2 {
			continue
		}
		version := parts[0]
		item := byVersion[version]
		if item == nil {
			item = &Migration{Version: version}
			byVersion[version] = item
