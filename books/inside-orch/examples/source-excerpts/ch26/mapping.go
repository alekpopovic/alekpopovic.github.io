	return orchdocker.SecurityContext{
		User:                   context.User,
		ReadOnlyRootFilesystem: context.ReadOnlyRootFilesystem,
		Privileged:             context.Privileged,
		CapAdd:                 append([]string(nil), context.CapAdd...),
		CapDrop:                append([]string(nil), context.CapDrop...),
		HostNetwork:            context.HostNetwork,
		HostPID:                context.HostPID,
		HostPathMounts:         mounts,
	}
}
