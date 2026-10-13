type AgentTask struct {
	Task            types.Task            `json:"task"`
	Healthcheck     *types.Healthcheck    `json:"healthcheck,omitempty"`
	Ports           []types.Port          `json:"ports,omitempty"`
	SecurityContext types.SecurityContext `json:"security_context,omitempty"`
	Env             map[string]string     `json:"env,omitempty"`
	ImagePullAuth   *RegistryAuth         `json:"image_pull_auth,omitempty"`
}
