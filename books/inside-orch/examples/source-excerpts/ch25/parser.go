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
	if lastColon > lastSlash {
		tag = nameAndTag[lastColon+1:]
		namePart = nameAndTag[:lastColon]
		if tag == "" {
			return types.ImageMetadata{}, fmt.Errorf("image tag is empty")
		}
	}
