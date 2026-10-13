func redactMetadataValue(key string, value string) string {
	if isSensitiveMetadataKey(key) {
		return "[REDACTED]"
	}
	if strings.Contains(strings.ToLower(key), "url") {
		parsed, err := url.Parse(value)
		if err == nil && parsed.Scheme != "" && parsed.Host != "" && parsed.User != nil {
			parsed.User = url.User("[REDACTED]")
			return parsed.String()
		}
	}
	return value
}

func isSensitiveMetadataKey(key string) bool {
	normalized := strings.ToLower(strings.ReplaceAll(strings.TrimSpace(key), "-", "_"))
