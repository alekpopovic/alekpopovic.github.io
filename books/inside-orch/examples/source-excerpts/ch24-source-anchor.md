# ch24-source-anchor

Trace secret encrypt/decrypt and reference resolution. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/secrets/envelope.go, lines 47–66](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L47-L66).

```go
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
```

SHA-256: `61dc36861e64925f55b6788171d1a288e632abd8f07a2b96cf4d360b69d24769`. This excerpt is not an independently compilable program.
