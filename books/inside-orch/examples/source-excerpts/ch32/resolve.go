		if c.VolumeID == "" {
			for id, v := range s.volumes {
				if v.Namespace == ns && v.Name == c.Name {
					c.VolumeID = id
					break
				}
			}
			if c.VolumeID == "" {
				v := types.Volume{ID: newUUID(), Namespace: ns, Name: c.Name, Driver: "local", CreatedAt: s.now()}
				s.volumes[v.ID] = v
				c.VolumeID = v.ID
				s.volumeClaims[namespacedKey(ns, c.Name)] = c
			}
		}
		v := s.volumes[c.VolumeID]
		out = append(out, types.ResolvedVolumeMount{ClaimID: c.ID, VolumeID: v.ID, VolumeName: v.Name, NodeID: v.NodeID, Target: m.Target, ReadOnly: m.ReadOnly, AccessMode: c.AccessMode, AllowConcurrentWriters: c.AllowConcurrentWriters})
	}
	return out, nil
