# ch25-source-anchor

Parse tags and digests through actual image-reference code. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/image/reference.go, lines 24–43](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go#L24-L43).

```go
func Parse(reference string) (types.ImageMetadata, error) {
	requested := strings.TrimSpace(reference)
	if requested == "" {
		return types.ImageMetadata{}, fmt.Errorf("image reference is required")
	}

	nameAndTag := requested
	digest := ""
	if before, after, found := strings.Cut(requested, "@"); found {
		if strings.Contains(after, "@") || !digestPattern.MatchString(after) {
			return types.ImageMetadata{}, fmt.Errorf("image digest is invalid")
		}
		nameAndTag = before
		digest = strings.ToLower(after)
	}

	lastSlash := strings.LastIndexByte(nameAndTag, '/')
	lastColon := strings.LastIndexByte(nameAndTag, ':')
	tag := ""
	namePart := nameAndTag
```

SHA-256: `bc16308c42dd51e54bcf7cdc88c79896aa796a0b8ac55331bc1be5f9e20e58d4`. This excerpt is not an independently compilable program.
