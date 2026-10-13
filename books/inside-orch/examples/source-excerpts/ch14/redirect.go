func sameOriginRedirect(origin *url.URL) func(*http.Request, []*http.Request) error {
	originScheme := strings.ToLower(origin.Scheme)
	originHost := strings.ToLower(origin.Host)
	return func(req *http.Request, via []*http.Request) error {
		if len(via) >= 10 {
			return fmt.Errorf("stopped after 10 redirects")
		}
		if strings.ToLower(req.URL.Scheme) != originScheme || strings.ToLower(req.URL.Host) != originHost {
			return fmt.Errorf("healthcheck redirect blocked: %s", req.URL.Redacted())
		}
		return nil
	}
}

