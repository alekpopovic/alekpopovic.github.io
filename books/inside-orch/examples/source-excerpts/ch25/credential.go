func (s *MemoryService) resolveRegistryAuthLocked(ctx context.Context, namespaceName string, id string) (*RegistryAuth, error) {
	id = strings.TrimSpace(id)
	if id == "" {
		return nil, nil
	}
	credential, ok := s.registries[namespacedKey(namespaceName, id)]
	if !ok {
		return nil, fmt.Errorf("%w: registry credential %q not found", store.ErrInvalidState, id)
	}
	if s.envelope == nil {
		return nil, fmt.Errorf("%w: secret envelope is not configured", store.ErrInvalidState)
	}
	plaintext, err := s.envelope.Decrypt(ctx, secrets.Ciphertext{KeyID: credential.KeyID, Data: credential.EncryptedPassword})
	if err != nil {
		return nil, fmt.Errorf("%w: decrypt registry credential %q", store.ErrInvalidState, id)
	}
	return &RegistryAuth{
		Username:      credential.Username,
		Password:      string(plaintext),
		ServerAddress: credential.Registry,
