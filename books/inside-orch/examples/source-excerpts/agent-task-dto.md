# agent-task-dto

Trace which fields assignments carry before describing runtime enforcement.

Unchanged, contiguous source excerpt: [internal/controlplane/controlplane.go, lines 130–137](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L130-L137).

```go
type AgentTask struct {
	Task            types.Task            `json:"task"`
	Healthcheck     *types.Healthcheck    `json:"healthcheck,omitempty"`
	Ports           []types.Port          `json:"ports,omitempty"`
	SecurityContext types.SecurityContext `json:"security_context,omitempty"`
	Env             map[string]string     `json:"env,omitempty"`
	ImagePullAuth   *RegistryAuth         `json:"image_pull_auth,omitempty"`
}
```

SHA-256: `fbf033e502e67d992b45b828768b7e32da2ec62b42fe85886dc8e7fd7e982148`. This excerpt is not an independently compilable program.
