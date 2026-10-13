		for _, m := range mounts {
			if m.NodeID != "" && m.NodeID != n.ID {
				ok = false
				break
			}
			if !m.ReadOnly && m.AccessMode == types.VolumeReadWriteOnce && !m.AllowConcurrentWriters {
				for _, a := range s.attachments {
					if a.VolumeID == m.VolumeID && a.DetachedAt.IsZero() {
						ok = false
						break
					}
				}
			}
		}
		if ok {
			out = append(out, n)
