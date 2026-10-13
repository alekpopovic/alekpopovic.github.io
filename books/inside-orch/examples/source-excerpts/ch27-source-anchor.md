# ch27-source-anchor

Resolve namespaces consistently across API and CLI. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/namespace/context.go, lines 32–51](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go#L32-L51).

```go
func WithContext(ctx context.Context, name string) context.Context {
	return context.WithValue(ctx, contextKey{}, Normalize(name))
}

func FromContext(ctx context.Context) string {
	if ctx == nil {
		return Default
	}
	name, _ := ctx.Value(contextKey{}).(string)
	return Normalize(name)
}

func Selected(ctx context.Context) (string, bool) {
	if ctx == nil {
		return Default, false
	}
	name, ok := ctx.Value(contextKey{}).(string)
	return Normalize(name), ok
}
```

SHA-256: `76800139f7f87b0bbf0b045d3184aa31461624c974a07a02f12c329a32cd8585`. This excerpt is not an independently compilable program.
