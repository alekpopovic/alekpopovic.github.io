# ch35-source-anchor

Read current server, agent, API, and schema compatibility ranges. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/migrations/manager.go, lines 27–46](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go#L27-L46).

```go
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
```

SHA-256: `be56007878bd6176c5688b515998ff993793e4bab24f52f5f2a55376d77820a2`. This excerpt is not an independently compilable program.
