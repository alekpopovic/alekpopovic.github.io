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
