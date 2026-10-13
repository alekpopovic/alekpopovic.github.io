# ch29-source-anchor

Separate digest identity from signature authenticity. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/policy/policy.go, lines 30–49](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/policy/policy.go#L30-L49).

```go
func DefaultClusterPolicy() ClusterPolicy {
	return ClusterPolicy{AllowMutableTags: true}
}

func (policy ClusterPolicy) ValidateServiceSpec(spec types.ServiceSpec) error {
	context := spec.SecurityContext
	if context.Privileged && !policy.AllowPrivileged {
		return fmt.Errorf("security_context.privileged is not allowed by cluster policy")
	}
	if context.HostNetwork && !policy.AllowHostNetwork {
		return fmt.Errorf("security_context.host_network is not allowed by cluster policy")
	}
	if context.HostPID && !policy.AllowHostPID {
		return fmt.Errorf("security_context.host_pid is not allowed by cluster policy")
	}
	for _, capability := range context.CapAdd {
		if !policy.capabilityAllowed(capability) {
			return fmt.Errorf("security_context.cap_add %q is not allowed by cluster policy", capability)
		}
	}
```

SHA-256: `e5a25fbb52f58f41fdb88da5ce102b6ccce219d8096f4e9d62391e7fdb82d5b7`. This excerpt is not an independently compilable program.
