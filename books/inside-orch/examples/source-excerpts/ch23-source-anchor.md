# ch23-source-anchor

Distinguish user authentication from agent bootstrap. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/auth/agent.go, lines 36–55](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go#L36-L55).

```go
func NewTokenAgentCredentialIssuer(ttl time.Duration) *TokenAgentCredentialIssuer {
	if ttl <= 0 {
		ttl = 15 * time.Minute
	}
	return &TokenAgentCredentialIssuer{ttl: func() time.Duration { return ttl }}
}

func (i *TokenAgentCredentialIssuer) Issue(_ context.Context, _ AgentIdentity) (AgentCredential, AgentCredentialRecord, error) {
	raw := make([]byte, 32)
	if _, err := rand.Read(raw); err != nil {
		return AgentCredential{}, AgentCredentialRecord{}, fmt.Errorf("generate agent credential: %w", err)
	}
	token := base64.RawURLEncoding.EncodeToString(raw)
	expiresAt := time.Now().UTC().Add(i.ttl())
	return AgentCredential{Token: token, ExpiresAt: expiresAt}, AgentCredentialRecord{
		Hash:      HashAgentToken(token),
		ExpiresAt: expiresAt,
	}, nil
}
```

SHA-256: `5190e95311139ecba70538e91f0cf355e98ab983403366eb1674270b166bae60`. This excerpt is not an independently compilable program.
