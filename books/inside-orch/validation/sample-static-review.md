# Sample chapter and lab: static review

Reviewed file: `samples/runtime-boundary.md`.

Source snapshot: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`.

**Result:** the extracted Bash lab passes `bash -n` (exit status 0; no diagnostics). Its flags, routes, configuration behavior, and expected namespace reset are consistent with the pinned source. The Go binary, server, HTTP requests, restart sequence, and expected outputs were **not executed**. No Go executable is installed in this environment.

## Checks performed

| Check | Result | Source evidence |
| --- | --- | --- |
| Exact lab Bash syntax | Passed | Extracted the sole Bash block into `samples/runtime-boundary-lab.sh`; ran `bash -n` only |
| `--addr`, `--database-url`, `--secret-key` flags | Matched | `cmd/orch-server/main.go`, `loadConfig`, lines 67–100 |
| Loopback binding | Matched | Script passes `--addr="127.0.0.1:$book_port"`; server uses cfg.Addr in http.Server |
| Clean server environment | Matched | `env -i` retains PATH plus `ORCH_SCHEMA_CHECK=false`; no inherited ORCH configuration variables reach the server |
| No implicit configuration file | Matched | Script omits `--config`; `applyServerFile` returns without reading a file when path is empty |
| Schema check disabled | Matched | `run` invokes it only for a case-insensitive string equal to `true`; `false` skips that branch |
| Unavailable example DB URL accepted by validation | Matched | Server validation requires nonempty DatabaseURL, rather than a connection; default run constructs MemoryService |
| JWT user authentication disabled in local lab | Matched | defaultServer does not set JWTSecret; clean environment supplies none; middleware bypasses JWT enforcement when secret is empty |
| Bootstrap token limitation | Clarified | defaultServer still has `dev-bootstrap-token`; this lab never registers an agent and does not claim all authentication is disabled |
| Ready endpoint | Matched | API registers GET `/readyz`; handler returns HTTP 200 with fixed `ready` status, not a durable-state or DB health check |
| Namespace create/list API | Matched | POST `/v1/namespaces`, GET `/v1/namespaces`; request DTO contains `name`; creation responds 201 and listing 200 |
| Namespace input validity | Matched | `book-restart-lab` satisfies namespace lowercase alphanumeric/hyphen rule, maximum 63 characters |
| Initial and reset state | Matched | Constructor initializes only default namespace; CreateNamespace inserts into a process-local map; a fresh process gets fresh maps |
| Source excerpt anchors | Passed | Ten anchored source links have valid paths and in-range line numbers; three excerpt anchors point to the exact lines used |
| Historical commit links | Previously verified, unchanged | All three full SHA targets resolve to local Git commit objects |

## Corrections made

1. Added exact full-SHA line anchors to unchanged Go/SQL excerpts and key implementation references.
2. Added a local TCP port probe before each launch. An existing listening service causes the lab to stop instead of issuing namespace writes to that listener.
3. Added `book_curl` with `--noproxy '*'`, one-second connection timeout, and two-second maximum request time. This prevents inherited proxy settings from routing local lab requests elsewhere and bounds requests against a stalled listener.
4. Added INT/TERM exit traps so the existing EXIT cleanup handles interruption.
5. Rechecks owned-process liveness after readiness succeeds; startup failures print that process's captured log.
6. Keeps cleanup scoped to the child PID started by the script and the directory returned by `mktemp -d`.
7. States Bash TCP-redirection support as a prerequisite.

## Limits of this validation

- `bash -n` validates syntax; it does not execute commands or prove their runtime outcomes.
- Build dependency availability, server startup, process signals, socket behavior, HTTP response data, and restart observations remain unverified in this environment.
- The port preflight is a check, not an atomic port reservation. On a shared machine another process could claim the port between the probe and bind. Use an otherwise idle development machine and change `book_port` if occupied; the PID checks reduce mistaken readiness acceptance but do not implement socket ownership attestation.
- The no-Docker, no-agent namespace lab demonstrates control-plane map reset only. It does not establish exact container behavior or agent recovery during a real server incident.
- The sample remains 2,280 words, within the requested 2,000–2,600-word range. Exact runtime output stays explicitly labeled **expected observations, not recorded execution results**.

No files in `evidence/orch` were changed.
