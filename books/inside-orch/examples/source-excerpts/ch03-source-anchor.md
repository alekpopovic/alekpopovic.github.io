# ch03-source-anchor

Build or install the pinned CLI reproducibly. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/cli/root.go, lines 540–559](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go#L540-L559).

```go
func (a *app) deployCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "deploy <file.yaml>",
		Short: "Deploy a service from YAML",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			spec, err := ParseDeployFile(args[0])
			if err != nil {
				return err
			}
			client, err := a.client()
			if err != nil {
				return err
			}
			service, err := client.CreateService(cmd.Context(), spec)
			if err != nil {
				return err
			}
			return writeServices(a.out, a.output, []types.Service{service})
		},
```

SHA-256: `0d184a38a1b0700f64b6686588c480daeb83e5df33bdc779046a26eedb42235f`. This excerpt is not an independently compilable program.
