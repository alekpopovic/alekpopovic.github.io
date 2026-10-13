# Atlas schedule arithmetic fixture

Copy `main.go` into `book-cron/main.go` under the disposable locked module. Go1.25 and timezone data are required; no network, database, daemon or wall-clock waiting. It verifies nine local hours under UTC versus Europe/Belgrade on2026-10-13, earliest two missed minute occurrences, and rejection of six-field cron syntax. This complements upstream fake-store controller tests but does not execute jobs, test every DST transition, or establish exactly-once scheduling.
