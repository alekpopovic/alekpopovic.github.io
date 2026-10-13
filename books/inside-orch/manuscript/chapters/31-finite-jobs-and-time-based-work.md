# Chapter 31 - Finite Jobs and Time-Based Work

Atlas needs a report that exits after counting a bounded input. A service controller would interpret exit as lost replica capacity, while a Job needs to interpret it as an outcome. Scheduling the same report every morning introduces another problem: local clock meaning, overlap and delayed controller iterations. These concerns require identities and state transitions beyond a long-running service's replica count.

This chapter assumes task reports, pending assignment and namespaces. You will follow one successful attempt and one retry, calculate five-field schedule occurrences with injected time, and distinguish Allow, Forbid and Replace. The safe lab executes real control-plane and schedule code with fake reports/clocks; it does not claim the finite workload ran on Docker.

## Finite Attempts and Exit Codes

JobSpec contains name, image, command, backoffLimit, resources, secrets, placement and volumeClaims with the source's exact YAML names. It is not a Kubernetes Job wrapper. CreateJob validates its spec, supplies resource defaults, checks the namespace and rejects an already-active same-named Job there. It creates a Job with Attempts one and one pending task carrying JobID, command and resource/placement data. [Claim ch31.attempt](../../validation/evidence/ch31.json).

The task is pending rather than directly assigned through the ordinary service path. Scheduler.Plan can construct a service-like scheduling view for Job tasks from their task fields, and MemoryService.AssignTask records the chosen node with its optimistic guard. This makes the earlier scheduler discussion relevant without assuming service and Job creation share every validation or credential feature.

Once a report arrives, updateJobForTaskLocked maps running/healthy to JobRunning. A stopped task with exit code zero produces JobSucceeded and CompletedAt. A stopped nonzero exit or failed task enters retry-or-fail handling. A missing stopped exit code defaults to zero at this method; a missing failed exit code defaults to one. This is the exact accepted-report interpretation, not proof that an arbitrary missing code is physically trustworthy.

[internal/controlplane/workloads.go, lines 190–216](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L190-L216) at the locked revision.

```go
	switch task.ActualStatus {
	case types.TaskRunning, types.TaskHealthy:
		job.Status = types.JobRunning
	case types.TaskStopped:
		code := 0
		if task.ExitCode != nil {
			code = *task.ExitCode
		}
		job.LastExitCode = &code
		if code == 0 {
			job.Status = types.JobSucceeded
			job.CompletedAt = now
		} else {
			s.retryOrFailJobLocked(&job, task, now)
		}
	case types.TaskFailed:
		code := 1
		if task.ExitCode != nil {
			code = *task.ExitCode
		}
		job.LastExitCode = &code
		s.retryOrFailJobLocked(&job, task, now)
	}
	job.UpdatedAt = now
	s.jobs[job.ID] = job
}
```

The actual focused Job test assigns a task, injects running and stopped-zero reports, and checks succeeded. It then creates a failing Job and injects nonzero failures through two attempts. The [recorded suite](../../validation/labs/ch31/focused-tests.json) passed. Because the reports are supplied directly and no Engine exists in this fixture, describe it as state-transition verification rather than successful execution of the report command.

A Docker execution experiment needs additional evidence: available image, actual command, container exit code, task identity and Job outcome. Command fields do reach the agent's ContainerSpec, but private service pull credentials and environment resolution do not automatically apply to the separate Job branch. A finite workload feature should be tested through its own DTO and agent path before claiming parity with services.

## Retry Limits and Terminal Outcomes

retryOrFailJobLocked compares current Attempts with BackoffLimit. With limit zero, the first failure is terminal because Attempts starts at one. With limit one, the first failure creates a second attempt, and the second failure is terminal. Thus the value bounds retries beyond the initial attempt. The helper does not implement a time-delay backoff merely because the field name contains backoff. [Claim ch31.retry](../../validation/evidence/ch31.json).

[internal/controlplane/workloads.go, lines 217–241](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L217-L241) at the locked revision.

```go
func (s *MemoryService) retryOrFailJobLocked(job *types.Job, previous types.Task, now time.Time) {
	if job.Attempts > job.Spec.BackoffLimit {
		job.Status = types.JobFailed
		job.CompletedAt = now
		return
	}
	job.Attempts++
	task := previous
	task.ID = types.TaskID(newUUID())
	task.NodeID = ""
	task.ContainerID = ""
	task.ActualStatus = types.TaskPending
	task.DesiredStatus = types.TaskRunning
	task.RestartCount = job.Attempts - 1
	task.ExitCode = nil
	task.FailureReason = ""
	task.CreatedAt = now
	task.UpdatedAt = now
	task.StartedAt = time.Time{}
	task.FinishedAt = time.Time{}
	s.tasks[task.ID] = task
	job.TaskIDs = append(job.TaskIDs, task.ID)
	job.Status = types.JobPending
}
```

A retry copies the previous task but assigns a new task ID, clears node/container identity, returns it to pending/running intent, resets exit/failure/timing fields and appends the new ID to Job.TaskIDs. RestartCount records attempt-related retry count. Preserving the prior task lets an operator distinguish attempts instead of overwriting one task's history as though a single process simply changed its past outcome.

The finite work itself must tolerate duplicate effects. A task can write a report externally and then lose its success acknowledgement. A later attempt may repeat that report. The Job controller's terminal-state logic does not make the external write exactly once. Use an application-level idempotency key or transactional output protocol when duplicate side effects would be harmful, and test that independently from the orchestration status.

A further source boundary concerns adoption after agent reconstruction. The create label uses a job-prefixed workload identity, while the shared matching helper compares a service-ID label against task.ServiceID. Job tasks have no ordinary service ID. That mismatch is a source-derived integration concern, not a tested guarantee of correct Job adoption. Keep it in the evidence ledger instead of borrowing the service adoption result.

DeleteJob removes Job metadata and marks its associated tasks for removal, detaching recorded task volumes in that path. Physical container stop/removal still belongs to agent convergence. Deleting the control-plane record is not proof every host side effect has ended. For a live finite-job lab, collect the actual exit and task history before cleanup, and verify only run-owned containers are removed.

## Cron Expressions and Explicit Timezones

CronJobs have schedule, timezone, concurrencyPolicy, jobTemplate, suspended and missedScheduleLimit. CreateCronJob defaults timezone to UTC and concurrency to Allow, validates supported policy values and the Job template, then stores the item. It does not parse the cron expression or load the timezone in that creation method. Those checks occur in Controller.RunOnce, so some invalid schedules/timezones fail later during controller processing.

The parser requires exactly five fields: minute, hour, day of month, month and weekday. Bounds are0–59,0–23,1–31,1–12 and 0–6. It supports comma lists, ranges, wildcard and positive step syntax implemented by parseField. Do not add a seconds field, named weekdays/months or a seventh-field extension from another cron implementation. [Claim ch31.schedule](../../validation/evidence/ch31.json).

matches requires all five fields to match. In particular, day-of-month and weekday are combined by this all-field rule; readers should not import another cron dialect's alternative-day semantics. Next truncates to a minute, starts at the following minute and searches a bounded year-sized number of minute increments. It can return zero if no occurrence is found within that horizon.

The current CronJob CLI accepts a smaller manifest surface than the full API type. A supported illustrative CLI manifest is:

```yaml
name: atlas-report-schedule
schedule: "0 9 * * 1-5"
timezone: UTC
concurrencyPolicy: Forbid
jobTemplate:
  image: busybox:1.36
  command: ["sh", "-c", "printf 'atlas report\\n'"]
  resources:
    cpu: 100m
    memory: 1Mi
```

This shows the actual intermediate CLI envelope and quantity strings; it is not an executed Docker manifest or proof the image is available. The CLI constructs a CronJobSpec from those fields, setting template name from the schedule name and identical resource requests/limits. It does not forward missedScheduleLimit or template backoffLimit from YAML in that envelope. The API/domain type supports additional fields, so use its explicit JSON contract when those are needed. The one-shot Job run envelope does support its own backoffLimit. Unknown YAML fields can be ignored by these simple unmarshalling paths; never infer acceptance of a field from a command returning without a parse error.

RunOnce loads the explicit IANA location and evaluates the schedule in that location, storing schedule timestamps in UTC. Nine in the morning under UTC and nine under Europe/Belgrade are different instants on the fixture date. The book's [actual arithmetic fixture](../../validation/labs/ch31/teaching-fixture.json) observed09:00UTC for UTC and 07:00UTC for Belgrade on2026-10-13, plus rejection of six fields. It uses injected dates, not wall-clock waiting.

Timezone arithmetic alone does not settle every daylight-saving policy. Minute stepping and local-time matching can encounter absent or repeated wall-clock times. The exact date/location must be part of a DST test; do not infer a universal skipped/repeated-hour guarantee from the ordinary October13 case. The dedicated workload lab adds explicit transition cases with recorded outcomes.

## Allow, Forbid, Replace, and Missed Runs

RunOnce chooses its base from LastScheduleAt, or CreatedAt if none exists. Between returns occurrences after that base through now, up to the configured missed limit, defaulting to100 when nonpositive. It takes the earliest due occurrences in that window. A delayed iteration can therefore leave a backlog rather than silently selecting only the latest minute. [Claim ch31.concurrency](../../validation/evidence/ch31.json).

Active jobs are those referenced by ActiveJobIDs whose current status is pending or running. Allow retains them and creates due jobs. Forbid makes due nil when an active job exists. Replace deletes active jobs before creating the due set. Replace requests removal; it does not establish that every old host process stopped before new work starts. This matters when old and new attempts write to the same external resource.

| Policy | Existing active Job | Controller action | Physical guarantee absent |
| --- | --- | --- | --- |
| Allow | Retained | Creates due Jobs | Unique external effect |
| Forbid | Retained | Suppresses this pass's creation | Permanent skipping of backlog |
| Replace | Deleted through store method | Creates due Jobs afterward | Verified old-process fencing |

Forbid does not advance LastScheduleAt when it suppresses all due occurrences in the inspected loop. Later, after the active job finishes, those earlier occurrences can still be due, subject to the limit. Also, when no active job exists at the start, a backlog's several due entries can be created in one Forbid pass; the controller does not recalculate overlap between each newly created Job in that loop. Name the tested behavior rather than importing a stronger non-overlap promise.

Job names include the UTC occurrence timestamp. That provides a useful deterministic label, but CreateJob only rejects same-name Jobs while active. Consider a failure after CreateJob succeeds but before UpdateCronJob records LastScheduleAt. The next iteration can revisit that occurrence. An active duplicate may reject, while later lifecycle changes can permit reuse. There is no transactional create-and-schedule checkpoint or exactly-once external execution guarantee in this method.

The default server constructs the Cron controller, so this is not wholly disconnected design. Its authoritative state is still MemoryService, and fresh process state loss can remove schedule/job inventory. A durable scheduling claim needs persistent composition, atomic checkpoint semantics and restart/partition tests beyond the current fake-clock suite.

History is the batch [4d641bbe8913da568d6d9f4697a0144314e10b87](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87), which adds jobs, cron, local storage, DNS and notifications. The design includes broader stateful/time-based ideas; the code and executed tests define which pieces are present. Do not invent a separate implementation commit for each original workload prompt.

For the safe lab, use the disposable module and Go 1.25. Run the focused tests, then copy examples/teaching-extensions/ch31/main.go to book-cron and run the arithmetic fixture. No Docker, database, server listener or external service is required.

```sh
go test ./internal/cronjobs ./internal/controlplane \
  -run 'TestParseAndRunWithFakeClock|TestConcurrencyForbidAndReplace|TestJobSuccessFailureRetryAndDelete' \
  -count=1 -v
go run ./book-cron
```

Expected observations are one successful injected attempt, bounded retry terminal failure, two earliest missed minutes under a limit of two, and distinct explicit-timezone instants. The linked runs passed those assertions. Cleanup is process exit and optional removal of copied teaching directories; no persistent report data was produced.

A useful schedule incident bundle includes the original five-field expression, IANA location, UTC base/now, computed due list, active Job IDs and the last accepted checkpoint. Preserve these before deleting generated work. A local-time string without its location or UTC offset cannot explain a repeated-hour decision, and a Job count alone cannot reveal whether the controller replayed backlog or generated a new occurrence.

## Exercises

1. Calculate maximum total attempts for backoffLimit zero and one. Why does the helper not prove delayed retry?
2. Explain why an accepted stopped report without an exit code and a failed report without an exit code take different defaults.
3. For a three-minute delay and missed limit two, which occurrences are created first? What can Forbid do when several are due and none was active at the start?
4. Identify the create-before-checkpoint failure window and design evidence needed for a stronger scheduling guarantee, including a concrete DST transition case.

[Worked answers](../solutions/ch31.md) retain attempt identity, exact cron syntax and time scope. Finite outcomes and deterministic scheduling are implemented, while external exactly-once effects, physical replacement fencing and durable process recovery remain separate requirements.
