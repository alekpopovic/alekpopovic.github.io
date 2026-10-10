# 22. Observe reliability, capacity, and recovery


## Measure the waiting as well as the running

A platform can execute jobs quickly while users wait a long time for an eligible runner or approval. Measure request-to-queue latency, queue delay by reason, claim latency, runner start delay, execution duration, log lag, and result-commit delay separately.

Correlate logs and traces with run, job, attempt, runner, and deployment identifiers. Keep those identifiers out of unrestricted metric label sets when their cardinality would grow without bound. Metrics summarize behavior; detailed logs and traces explain a specific execution.

An uncertain-deployment count deserves more attention than a generic failure total. It represents work whose external effect is not understood. Alert on age and actionable state, with a runbook link and the relevant target identity, rather than paging on every transient retry.

## Establish service objectives from use

Do not invent a public performance claim from a developer laptop. Start with proposed internal objectives, collect measurements, then adjust capacity and architecture. State the workload: graph size, concurrent jobs, log bytes per second, artifact sizes, runner distribution, and failure injection profile.

A useful objective might distinguish “authorized run accepted into durable storage” from “run started on an eligible runner.” The first measures control-plane responsiveness; the second includes capacity and policy delays. A single average hides which experience is deteriorating.

Load tests should include noisy projects and quiet projects together. Observe starvation, backlog growth, database contention, log storage pressure, and recovery after stopping the load. A system that survives a spike but never drains its backlog has not recovered.

## Back up state and the ability to interpret it

PostgreSQL documents several backup approaches, including logical dumps and physical/continuous-archiving approaches. Choose a method around recovery-point and recovery-time objectives, then test restoration. A backup file's existence is not a restore result. [S20](e-sources.md#s20)

The recovery set also includes object storage, encryption keys, signing keys, integration configuration, source and release manifests, and the versions needed to interpret the database. Restoring rows without the keys needed to decrypt them is not a complete recovery.

Keep restored environments isolated from production side effects. Start the control plane with scheduling and dispatch paused. Reconcile old leases and external targets before enabling work. A restored database may remember an attempt as running even though the target changed after the backup point.

## Plan a controlled restart

Document the restart sequence for API, scheduler, database, and runners. Decide which component is allowed to migrate schema, which checks compatibility, and which can safely resume dispatch. Ensure health endpoints distinguish process liveness from readiness to accept work.

A runner should stop admitting new jobs when its runtime, disk, credential source, or control connection no longer meets the required conditions. Do not advertise full capacity just because the agent process is alive.

For the first deployment, keep the infrastructure understandable. A control host with separate database and dedicated runner hosts may be easier to operate than a large service fleet. Add more control instances, broker infrastructure, or Kubernetes executors when measurements show a need and the failure model is ready.

## Exercise

A database restore succeeds in a test environment. The scheduler immediately resumes jobs recorded as leased at the backup time. Why is this unsafe, and what is the first recovery action?

## Worked answer

Those records may no longer match physical execution or target state. The original runners or deployments could have continued after the backup. Keep dispatch paused, establish a new controlled recovery context, and reconcile attempts and targets before issuing new authority. Restore validation must include side-effect control, not just the ability to run SQL queries.

## Completion evidence

Record a real restore exercise with measured recovery times, key availability, object consistency checks, paused dispatch, lease reconciliation, and a controlled return to service. Publish performance numbers only with the workload and environment that produced them.
