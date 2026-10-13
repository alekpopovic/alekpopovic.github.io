func (e *LocalEnvelope) Encrypt(ctx context.Context, plaintext []byte) (Ciphertext, error) {
	if err := ctx.Err(); err != nil {
		return Ciphertext{}, err
	}
	gcm, err := e.gcm()
	if err != nil {
		return Ciphertext{}, err
	}
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return Ciphertext{}, fmt.Errorf("generate secret nonce: %w", err)
	}
	data := append([]byte(nil), nonce...)
	data = gcm.Seal(data, nonce, plaintext, []byte(e.keyID))
	return Ciphertext{KeyID: e.keyID, Data: data}, nil
}

func (e *LocalEnvelope) Decrypt(ctx context.Context, ciphertext Ciphertext) ([]byte, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
