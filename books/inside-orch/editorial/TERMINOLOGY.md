# Editorial terminology

This sheet applies to the English edition pinned to Orch revision `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. Preserve source symbol spelling in code and links.

| Term | Use in this edition |
| --- | --- |
| service | Desired replicated workload and its versioned specification; distinct from its tasks and containers. |
| task | One execution identity with server-owned desired state and accepted actual state. Replacement creates another identity. |
| container | A Docker runtime object. Its physical lifetime can exceed the controller's task accounting. |
| node | Registered worker identity and advertised reachability; offline is a control-plane observation. |
| deployment | Versioned rollout/rollback history record, with its own lifecycle. |
| rollout | The repeated process moving tasks toward a target version under the inspected availability predicates. |
| desired state | Server-owned intent, distinct from a worker's observation or physical completion. |
| actual state | Latest accepted task observation, which policy or node-loss logic can also transform. |
| reconciliation | Repeated comparison and bounded action toward intent; name whether the standalone package or MemoryService path is meant. |
| scheduling | Planning and claiming work; ordinary MemoryService immediate placement is a different path from scheduler.Plan. |
| admission | Validation and policy before accepting intent; acceptance does not prove runtime enforcement. |
| namespace | Logical selection and authorization scope; it does not imply kernel or network isolation. |
| task claim | Conditional assignment of a pending task; separate from reserving all node resources globally. |
| volume claim | A storage reference with its own validation/attachment rules; distinguish it from a scheduler task claim. |
| attachment | Recorded volume-to-node/task relationship; not proof of replicated data or physical exclusive access. |
| runtime | The agent's container-operation boundary; the health checker is a separate dependency. |
| requests / limits / consumption | Accounted capacity / intended runtime bounds / measured use. Preserve this distinction in units and conclusions. |
| readiness / workload health | Process endpoint response / workload-specific observation. Neither alone proves durable ownership or serving traffic. |
| fencing | Rejection of obsolete authority where effects are accepted. Heartbeat expiry alone does not fence a container. |

Use the capability labels **runtime-integrated**, **implemented package**, **partial integration**, **design only**, **teaching extension**, and **future work**. Identify the concrete constructor and consumer before changing a label. Distinguish inspected source, actually executed evidence, expected outcomes and proposed acceptance tests.

CPU uses integer millicores, Docker NanoCPUs use millicores multiplied by 1,000,000, and memory comparisons use bytes. Preserve `Mi`/`MiB` meaning and avoid relabeling binary quantities as decimal MB. Commands and symbols retain exact case. Execution timestamps identify UTC; calendar examples identify their IANA zone. Full immutable SHA destinations remain unchanged even when displayed labels are abbreviated.
