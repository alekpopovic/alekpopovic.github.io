# Appendix A. Laboratory runbook

## Scope and prerequisites

This runbook operates only the Go examples included with the book. It does not provision application repositories, a container daemon, a database, cloud resources, or a production deployment. Work in a disposable checkout. No credential is required by the Go examples, and they do not contact external services.

Install Git for version control, a supported Go compiler, and Python 3.11 or later for book tooling. The Go module declares a language baseline; use an actively maintained release when reproducing the exercises. The website and EPUB use the packages in `requirements-site.txt`. PDF export additionally uses `requirements-print.txt` and WeasyPrint's system dependencies. The exact preparation environment is recorded in `verification/`.

## Inspect before running

From the repository root, inspect `examples/lab/go.mod` and the source files. The module contains no external dependencies and no general shell executor. Its demonstration runs the domain model only. Review the Makefile targets before using them. `make check` validates the publication sources and runs the example tests; `make site` and `make epub` write local publication outputs.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-site.txt
make check
make site
make epub
```

The virtual environment is ignored by Git. The site is written to `dist/site/`. Serve that directory locally when testing navigation:

```bash
python3 -m http.server 8000 --directory dist/site \
  --bind 127.0.0.1
```

This command binds to loopback. Open the local address printed by Python. Stop the server with the normal terminal interrupt when finished. Opening a single HTML file directly may work for navigation, but serving the directory more closely resembles a static host.

## Read the execution model

Run the demonstration directly:

```bash
cd examples/lab
go run ./cmd/demo
```

The expected sequence is a compiled `test`, `package`, and `deploy` graph; an uncertain state after expiry; refusal of a blind retry; refusal of the old attempt's stale result; success for the authorized new attempt; and recognition of an identical log retry. If the output differs, run the tests and inspect the exact commit you are using before changing expected values.

The ledger contains no persistence. Re-running the demonstration creates a fresh in-memory model. This is intentional. Use the database exercises from Chapters 9 and 23 to validate a future durable implementation instead of assuming the model survives restart.

## Reproduce the tests

```bash
cd examples/lab
go test -count=1 ./...
go test -race -count=1 ./...
go vet ./...
```

The first command disables cached success for that invocation. The race check requires a compatible compiler environment, including the platform support required by Go. A missing prerequisite should be recorded as a blocker, not relabeled as a successful check. The preparation report distinguishes tests actually run from target-system tests that remain unexecuted.

Inspect failures around the corresponding invariant. A cycle-test failure belongs to graph compilation. A stale-result failure belongs to identity and state acceptance. A signature test failing after JSON reformatting demonstrates why exact bytes matter. A log conflict is not repaired by overwriting the expected segment hash.

## Explore safely

Make a local branch and introduce one small defect. Remove a fence comparison, allow a missing dependency, or make an approval ignore the configuration digest. The relevant test should fail. Restore the invariant and commit the repair with a short explanation. Do not weaken the test to make the defect appear acceptable.

For concurrency, run the single-claim test repeatedly. It verifies process-local admission under the ledger mutex. To extend the exercise to PostgreSQL, first build a disposable database harness around the SQL examples, then use multiple real connections and crash injection. That harness is not included as an already validated service.

## SQL and runtime examples

`examples/sql/` contains a minimal schema and prepared statements explaining atomic claims and conditional completion. They are not complete production migrations. Tenant authorization, global capacity reservations, audit insertion, and external deployment safety require additional work. Do not run them against an existing application database.

Pipeline YAML files describe the proposed platform grammar. The book laboratory does not execute them. No example should be interpreted as a command to publish an image or deploy a service merely because it contains a deployment-related field.

## Collect evidence and clean up

Save command output, tool version, exit status, source commit, and relevant configuration with an experiment. Remove credentials and unrelated local paths from reports before sharing them. The repository's preparation evidence is a record for this edition, not a replacement for your environment's results.

Delete `dist/` to remove local exports, or use `make clean`. The clean target does not delete the manuscript or the laboratory source. Delete the virtual environment only when you no longer need its installed dependencies. No cloud or production cleanup is required by the included Go demonstration.
