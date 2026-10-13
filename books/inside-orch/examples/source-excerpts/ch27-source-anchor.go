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

