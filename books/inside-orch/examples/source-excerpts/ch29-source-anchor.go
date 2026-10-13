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
