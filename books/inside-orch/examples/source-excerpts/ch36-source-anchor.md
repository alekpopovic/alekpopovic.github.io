# ch36-source-anchor

Select the smallest test boundary that proves an invariant. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/scheduler/property_test.go, lines 11–30](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go#L11-L30).

```go
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
```

SHA-256: `7c3ef9ed12eb999cbc5542ecc0ba9f2f21f2a22f7b834bc195650e336d951136`. This excerpt is not an independently compilable program.
