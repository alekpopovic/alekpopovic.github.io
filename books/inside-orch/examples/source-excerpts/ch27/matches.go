func Selected(ctx context.Context) (string, bool) {
	if ctx == nil {
		return Default, false
	}
	name, ok := ctx.Value(contextKey{}).(string)
	return Normalize(name), ok
}

func Matches(ctx context.Context, objectNamespace string) bool {
	selected, explicit := Selected(ctx)
	return !explicit || selected == Normalize(objectNamespace)
}
