# ch02-source-anchor

Navigate the actual package tree. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/docker/docker.go, lines 47–66](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L47-L66).

```go
type Runtime interface {
	PullImage(ctx context.Context, image string, auth *RegistryAuth) error
	CreateContainer(ctx context.Context, spec ContainerSpec) (ContainerID, error)
	StartContainer(ctx context.Context, id ContainerID) error
	StopContainer(ctx context.Context, id ContainerID, timeout time.Duration) error
	RemoveContainer(ctx context.Context, id ContainerID, force bool) error
	InspectContainer(ctx context.Context, id ContainerID) (ContainerStatus, error)
	ListManagedContainers(ctx context.Context, labels map[string]string) ([]ContainerStatus, error)
	StreamLogs(ctx context.Context, id ContainerID, opts LogOptions) (<-chan LogLine, <-chan error)
}

type ContainerSpec struct {
	Name        string
	Image       string
	ServiceID   string
	TaskID      string
	NodeID      string
	Version     int64
	Env         map[string]string
	Ports       []PortBinding
```

SHA-256: `a41c8dffac6e3852b207f82e3a8fe32edb4d1124603fc9c561945578418aaf25`. This excerpt is not an independently compilable program.
