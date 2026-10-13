# Exact source listing review

Reviewed2026-10-13 against immutable SHA `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. The six supplied seed intervals and raw excerpts are preserved. Forty additional chapter anchors use short contiguous windows from the locked bytes; none are silently repaired. A window may end before a function ends and is explicitly a window, not a full independently compilable definition. No ellipses are inserted into exact bytes.

Every entry carries stable ID, file, line range, SHA, generated SHA256, companion source URL, purpose, and (for chapter anchors) symbol/runtime scope. Source snippets are not automatically permitted standalone programs. Separate adaptations belong under teaching-extensions with attribution and tests.

| Chapter | Listing ID | File/lines | Scope |
| --- | --- | --- | --- |
| 01 | `ch01-source-anchor` | `cmd/orch-server/main.go` 146–165 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 02 | `ch02-source-anchor` | `internal/docker/docker.go` 47–66 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 03 | `ch03-source-anchor` | `internal/cli/root.go` 540–559 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 04 | `ch04-source-anchor` | `pkg/types/lifecycle.go` 136–155 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 05 | `ch05-source-anchor` | `internal/cli/deploy.go` 129–148 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 06 | `ch06-source-anchor` | `cmd/orch-server/main.go` 146–165 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 07 | `ch07-source-anchor` | `internal/apperrors/errors.go` 35–54 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 08 | `ch08-source-anchor` | `internal/config/config.go` 123–142 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 09 | `ch09-source-anchor` | `internal/store/postgres.go` 892–911 | implemented package; inspect constructor/callers before attributing to default executable |
| 10 | `ch10-source-anchor` | `internal/scheduler/scheduler.go` 270–289 | implemented package; inspect constructor/callers before attributing to default executable |
| 11 | `ch11-source-anchor` | `internal/reconciler/reconciler.go` 125–144 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 12 | `ch12-source-anchor` | `internal/docker/docker.go` 191–210 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 13 | `ch13-source-anchor` | `internal/agent/agent.go` 128–147 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 14 | `ch14-source-anchor` | `internal/health/health.go` 97–116 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 15 | `ch15-source-anchor` | `internal/events/events.go` 71–90 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 16 | `ch16-source-anchor` | `internal/agent/logs.go` 16–35 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 17 | `ch17-source-anchor` | `internal/rollout/rollout.go` 358–377 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 18 | `ch18-source-anchor` | `internal/controlplane/controlplane.go` 1436–1455 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 19 | `ch19-source-anchor` | `internal/node/monitor.go` 57–72 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 20 | `ch20-source-anchor` | `internal/discovery/discovery.go` 28–47 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 21 | `ch21-source-anchor` | `internal/traefik/config.go` 46–65 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 22 | `ch22-source-anchor` | `internal/autoscaler/autoscaler.go` 114–133 | implemented package; inspect constructor/callers before attributing to default executable |
| 23 | `ch23-source-anchor` | `internal/auth/agent.go` 36–55 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 24 | `ch24-source-anchor` | `internal/secrets/envelope.go` 47–66 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 25 | `ch25-source-anchor` | `internal/image/reference.go` 24–43 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 26 | `ch26-source-anchor` | `internal/admission/admission.go` 48–67 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 27 | `ch27-source-anchor` | `internal/namespace/context.go` 32–51 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 28 | `ch28-source-anchor` | `internal/quota/quota.go` 18–37 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 29 | `ch29-source-anchor` | `internal/policy/policy.go` 30–49 | implemented package; inspect constructor/callers before attributing to default executable |
| 30 | `ch30-source-anchor` | `internal/gitops/gitops.go` 198–217 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 31 | `ch31-source-anchor` | `internal/cronjobs/cronjobs.go` 55–74 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 32 | `ch32-source-anchor` | `pkg/types/workloads.go` 128–147 | implemented package; inspect constructor/callers before attributing to default executable |
| 33 | `ch33-source-anchor` | `internal/docker/docker.go` 47–66 | implemented package; inspect constructor/callers before attributing to default executable |
| 34 | `ch34-source-anchor` | `internal/leadership/postgres.go` 21–40 | implemented package; inspect constructor/callers before attributing to default executable |
| 35 | `ch35-source-anchor` | `internal/migrations/manager.go` 27–46 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 36 | `ch36-source-anchor` | `internal/scheduler/property_test.go` 11–30 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 37 | `ch37-source-anchor` | `internal/e2e/chaos_test.go` 19–38 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 38 | `ch38-source-anchor` | `internal/metrics/prometheus.go` 41–60 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 39 | `ch39-source-anchor` | `internal/scheduler/benchmark_test.go` 9–26 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |
| 40 | `ch40-source-anchor` | `.github/workflows/ci.yml` 11–30 | source call-path or test anchor; runtime integration must be stated in chapter, test code is not an observed run |

Validation: `python3 books/inside-orch/scripts/extract_snippets.py` derives listings and hashes; the independent review check compares every generated raw listing to its original byte slice and records `excerpt-check.json`. Claiming runtime integration remains a source-call-graph review, not an extractor result. No live credentials were introduced; excerpts are code/type/CI windows, not owner environment configuration.
