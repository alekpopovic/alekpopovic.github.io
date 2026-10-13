# Preface

An orchestration system is most revealing when something interrupts its plans. A container starts but its status report disappears. A worker stops answering while its application remains reachable. An operator restarts a server and discovers that the running containers remember more than the new control plane. These moments expose the difference between a useful algorithm, an implemented package, and a working recovery protocol. This book studies that difference through one inspectable Go and Docker system: orch.

I wrote this edition for readers who want to understand the machinery behind an orchestration interface. Developers need to follow types and interfaces until a request becomes a runtime effect. DevOps engineers need to distinguish an accepted deployment from available application replicas and know what to inspect after a failure. Architects need to identify where authority lives, which invariants are local, and which guarantees require coordination across processes. Those interests overlap. An operator's unexplained failure often points to a developer's missing boundary, while an architectural promise becomes credible only when someone can test its recovery conditions.

## One source edition, with an honest boundary

The source edition is orch commit `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. References use that full revision so readers can inspect the same files even as the application changes. The accompanying history contains ninety-one development prompts and 105 reachable commits. Prompts describe requested work; implementation and tests show what was built. Several early prompts were added retrospectively, and later work landed in batches. A completed development tracker is useful navigation, but it is not a transcript establishing that a laboratory ran or that a distributed guarantee holds.

The most important fact appears before the sophisticated features: the default server constructs an in-memory control plane. Its service, node, task and deployment records belong to the running process. PostgreSQL storage code, migrations and backup scripts exist, but their presence does not make the default API state durable. Leadership, autoscaling and reconciliation packages also need to be read with their callers in view. A package can provide a sound building block without being the implementation selected by the executable.

This boundary is an opportunity to learn rather than a detail to hide. We can examine deterministic planning without claiming every service uses that planner. We can study optimistic database assignment without pretending it reserves every resource globally. We can inspect Docker limit support while tracing whether the agent supplies the required fields. Every chapter asks both what a component does and how its behavior reaches the running system.

## Three ways through the book

Everyone should read the opening chapters on scope, the laboratory, models and the request path. They establish the vocabulary of desired state, reported state, identity and process ownership. Later chapters repeatedly use those definitions instead of quietly changing what “running,” “available” or “recovered” means.

The developer path follows API contracts, the CLI, persistence interfaces, scheduling, reconciliation, Docker operations and agent reports. Read it with the source open. Pay particular attention to the smallest function that decides a state transition and the caller that gives it authority. Exercises ask you to reason about stale snapshots, idempotency, concurrency and test boundaries before proposing changes.

The DevOps path follows deployment flow, probes, events, logs, rollouts, node loss, secrets, upgrades and observability. Its recurring question is what an operator can actually observe. Keep a worksheet with service, task, node, deployment and container identifiers. A successful application request, a healthy agent heartbeat and a control-plane record are separate pieces of evidence; none should silently stand in for the others.

The architect path follows composition, state ownership, admission, tenancy, jobs, local storage and leadership. It emphasizes failure windows and tradeoffs rather than product checklists. Use the worked scenarios to decide where a stronger guarantee would need durable identity, atomic mutation, fencing or a different topology. Design-only topics remain useful when the missing implementation is stated precisely.

## A laboratory that respects its neighbors

The running example is Atlas, a small application used to connect chapters. Its services, jobs and operational decisions become more interesting as the book progresses. The laboratory is disposable. Go commands run against a separate copy of the pinned application source, not against the website repository or the immutable research snapshot. Containers, temporary repositories, ports and databases belong to that laboratory and must have an explicit cleanup owner.

Start with deterministic package tests and local fixtures. They provide focused evidence without demanding an entire cluster. Docker and PostgreSQL experiments are additional boundaries, not decorative prerequisites. Some upstream tests reset database schemas, so only a database created for the experiment is acceptable. A shared development daemon also deserves care: never replace scoped cleanup with a command that deletes every container or volume on the host.

Each experiment states prerequisites, commands, observations, abort conditions and cleanup. An expected result describes what source inspection predicts; an observed result requires a recorded run. Missing tools or unavailable external services remain visible gaps. Reading can continue while a laboratory is blocked, but a release cannot claim that the blocked integration was verified.

## How to read the evidence

Short source listings are unchanged excerpts with pinned file and line references. Adapted examples are labeled teaching extensions and live separately from the application baseline. Diagrams explain ownership and state changes; they are not permission to invent a connection absent from startup code. Tests inspected in source establish intended assertions. Only command records with scope, timestamps, exit status and logs establish execution.

Performance results require measurement context. Security findings distinguish source-derived concerns from demonstrated behavior. A fake runtime is valuable for deterministic faults, but it does not prove Docker, network or database behavior. Likewise, a controller reconstructed over the same memory object has not demonstrated a new server process recovering its state.

Exercises have worked answers, yet their purpose is to sharpen judgment rather than reward recall. Ask where identity survives, who can repeat a side effect, what happens between a write and its report, and which observation would falsify your explanation. By the final chapter, you should be able to describe both the system's useful mechanisms and its unresolved boundaries with equal precision. That is the foundation for evolving an orchestrator responsibly—and for operating the version that actually exists.
