# Project recording evidence

`_data/project_demos.json` records the scope, pinned source revision, capture
date, and actual successful command output used by each featured project page.
The WebM recordings and WebP posters are editorial assets under
`assets/projects/demos/`. Ordinary builds use local assets and never execute
these external projects or fetch their dependencies.

The 2026-10-12 captures use the revisions in `_data/projects.json`:

| Project | What actually ran | Limits |
| --- | --- | --- |
| Orch | Local server and agent; validate, deploy one nginx container, inspect actual running state, inspect events, delete the service | Temporary in-memory local server; no availability or production claims |
| ClusterForge | `cf --no-plugins --non-interactive wizard --defaults`, `cf --no-plugins generate dev`, `cf --no-plugins env list` | Existing-Kubernetes scaffold only; no Terraform plan/apply or cluster provisioning |
| Cloudivision | `go test -p 2 ./internal/webhook ./internal/redact ./internal/policy -v` | Unit fixtures for three packages; no live Kubernetes controller |
| ContainerDesk | Build the pinned browser UI with Node 24.21.0 and npm 11.19.0; open its built-in demo and inspect containers, Compose, images, settings | Synthetic fixtures, no SSH and no native desktop bridge |

The CLI videos replay captured output in a readable terminal frame. Their
captions say this explicitly; the page provides the full transcript. The
ContainerDesk video records the actual browser demo. Its visible demo banner
and page caption identify the synthetic data. Videos have no audio and do not
autoplay; equivalent text is available beside each recording.

For a new capture, check out the exact public revision into an isolated
temporary directory. Review its instructions and prerequisites, run only the
documented local scenario, retain unmodified successful output, and review it
for credentials before updating the data file. Any Docker scenario must use
the local Unix socket explicitly, a unique temporary node/service identity,
and cleanup restricted to that identity. Do not prune other resources. Save
both desired and actual task states; desired `running` alone is insufficient.

To render terminal replays from the reviewed evidence, run:

```sh
node scripts/record-project-demos.mjs
```

To record ContainerDesk after building and serving that pinned project locally:

```sh
node scripts/record-project-demos.mjs --preview=http://127.0.0.1:4318 --only=container-desk
```

These authoring commands require an installed Playwright Chromium browser.
They do not advance verification dates or generate purported command evidence.
Update source pins, dates, captions, and transcripts deliberately after actual
review. `npm run check:site` checks that pins agree, recording and poster files
are present, and recorded commands succeeded.

## Deeper captures on 2026-10-13

The ClusterForge recording now captures the pinned Kubernetes workload module
on the owned `codepop-site-20261013` kind cluster with a separate kubeconfig.
Terraform 1.16.1 initialized, validated, planned, applied, and destroyed four
resources. The configuration explicitly creates its ServiceAccount and uses a
locally loaded nginx:1.27-alpine image with pull policy Never. Rollout, resource
status, and an HTTP request inside the actual pod passed. The local older
OpenTofu could not handle cross-variable validation; no module code was changed
to conceal that limitation. This does not establish broad Terraform/OpenTofu
version compatibility, cloud provisioning, or ingress behavior.

Cloudivision ran its pinned API on 127.0.0.1:4320 with real CRDs in that same
disposable cluster. Synthetic resources and a synthetic webhook secret produced
HTTP 401 for an invalid signature, 201 for a signed push, and 200 for a duplicate.
A separate kubectl read confirmed one BuildRun. The recording does not claim
controller reconciliation, a runner Job, artifact publication, or deployment.
The HTTP error is an expected assertion in a successful capture script.

ContainerDesk retains the explicitly synthetic browser video and adds a separate
terminal replay of `python3 tests/lab/ssh_auth.py --engine --listing --inventory`.
The native Rust backend verified direct and ProxyJump SSH, a fresh real Docker
Engine 28.3.3, exact inventory IDs for two metadata-only containers, stale-session
rejection, and cancellation. This is backend integration evidence, not a video
of a connected desktop window. The complete capture includes a separately
labelled synthetic fault matrix. Temporary SSH keys, agent, containers, and
network were removed by the harness.

Complete reviewed captures are in `assets/projects/evidence/`, with SHA-256
checksums in the demo catalogue. The site check verifies their bytes, source
pins, and media. The temporary API was stopped and the owned kind cluster
deleted after both Kubernetes captures. No existing contexts or workloads
were used. Record dates are editorial values, never advanced by builds.
