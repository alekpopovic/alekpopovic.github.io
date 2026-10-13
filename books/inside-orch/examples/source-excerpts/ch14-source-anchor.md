# ch14-source-anchor

Distinguish process running from healthy service state. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/health/health.go, lines 97–116](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go#L97-L116).

```go
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

func (c *DefaultChecker) checkTCP(ctx context.Context, target string, timeout time.Duration) (Result, error) {
	if strings.TrimSpace(target) == "" {
		return Result{}, fmt.Errorf("tcp healthcheck target is required")
	}
	var dialer net.Dialer
	ctx, cancel := context.WithTimeout(ctx, timeout)
```

SHA-256: `6b643b556061321aa3c793b690a83263e612a804c09c869240b8f9594fa19d51`. This excerpt is not an independently compilable program.
