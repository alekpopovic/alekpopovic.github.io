# ch32-source-anchor

Explain why a local claim binds future placement to a node. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [pkg/types/workloads.go, lines 128–147](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/workloads.go#L128-L147).

```go
type VolumeClaim struct {
	ID                     string           `json:"id"`
	Namespace              string           `json:"namespace"`
	Name                   string           `json:"name"`
	VolumeID               string           `json:"volume_id,omitempty"`
	AccessMode             VolumeAccessMode `json:"access_mode"`
	AllowConcurrentWriters bool             `json:"allow_concurrent_writers,omitempty"`
	CreatedAt              time.Time        `json:"created_at"`
}

type VolumeClaimMount struct {
	Claim    string `json:"claim" yaml:"claim"`
	Target   string `json:"target" yaml:"target"`
	ReadOnly bool   `json:"read_only,omitempty" yaml:"readOnly,omitempty"`
}

type ResolvedVolumeMount struct {
	ClaimID                string           `json:"claim_id"`
	VolumeID               string           `json:"volume_id"`
	VolumeName             string           `json:"volume_name"`
```

SHA-256: `8e91e07a9db752beab64b52e473881d0b23a3eda4db649be04717afc131656ee`. This excerpt is not an independently compilable program.
