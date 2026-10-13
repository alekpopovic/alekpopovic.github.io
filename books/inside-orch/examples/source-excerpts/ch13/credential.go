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

func (i *TokenAgentCredentialIssuer) Validate(_ context.Context, token string, record AgentCredentialRecord, now time.Time) error {
	if record.Revoked {
