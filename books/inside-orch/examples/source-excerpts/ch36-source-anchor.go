func TestSchedulerRandomizedInvariants(t *testing.T) {
	for _, seed := range []int64{1, 7, 42, 99, 20260821} {
		t.Run(fmt.Sprintf("seed_%d", seed), func(t *testing.T) {
			rng := rand.New(rand.NewSource(seed))
			nodes := make([]types.Node, 5+rng.Intn(10))
			for i := range nodes {
				status := types.NodeReady
				if rng.Intn(4) == 0 {
					status = []types.NodeStatus{types.NodeDraining, types.NodeOffline}[rng.Intn(2)]
				}
				nodes[i] = types.Node{ID: types.NodeID(fmt.Sprintf("n-%02d", i)), Status: status, Labels: map[string]string{"zone": []string{"a", "b"}[rng.Intn(2)]}, Allocatable: types.Resources{CPU: int64(1000 + rng.Intn(4000)), Memory: int64(1+rng.Intn(8)) << 30}}
			}
			services := map[types.ServiceID]types.Service{}
			tasks := []types.Task{}
			for i := 0; i < 100; i++ {
				id := types.ServiceID(fmt.Sprintf("s-%03d", i))
				cpu := int64(50 + rng.Intn(500))
				memory := int64(32+rng.Intn(512)) << 20
				constraints := []types.PlacementConstraint{}
				if rng.Intn(2) == 0 {
