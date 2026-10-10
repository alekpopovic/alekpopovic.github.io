# Runtime and Network Boundary

## Prerequisites

Disposable cluster, enforced NetworkPolicy, reviewed image and installed runtime.

## Procedure

Render the Kubernetes example with explicit arguments. Review every resource and namespace. Manually test admission and traffic in the isolated cluster, then add one narrowly scoped test destination.

## Acceptance criteria

Verify denied traffic using actual packets, not manifest presence. Verify the runtime handler and the absence of service-account token mounting. Record what the CNI cannot enforce. Remove only lab-owned resources.

## Evidence record

Record date, source revision, environment, exact commands, expected result, actual result, limitations and teardown status. Never attach secrets or customer payloads. A written procedure is not an executed result.
