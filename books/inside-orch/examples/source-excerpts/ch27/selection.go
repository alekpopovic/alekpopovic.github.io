func selectedNamespace(r *http.Request) string {
	if value := strings.TrimSpace(r.Header.Get("X-Orch-Namespace")); value != "" {
		return namespace.Normalize(value)
	}
	return namespace.Normalize(r.URL.Query().Get("namespace"))
}
