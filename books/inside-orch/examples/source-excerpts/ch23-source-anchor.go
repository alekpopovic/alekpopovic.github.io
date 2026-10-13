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

