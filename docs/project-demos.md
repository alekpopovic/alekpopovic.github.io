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
