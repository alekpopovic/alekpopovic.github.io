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
