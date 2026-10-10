# 24. Publish a reproducible release and maintain the project


## A release is more than a tag

A product release should name the workspace commit, all child source commits, built artifacts or image digests, contracts version, database schema range, supported runner versions, migration procedure, rollback constraints, and verification evidence. A source tag is useful, but it does not identify every runtime dependency or guarantee that a build will produce the same bytes.

Publish child dependencies before a workspace references them publicly. Verify that a fresh consumer can retrieve the pinned commits with the intended access level. A private test succeeding with the maintainer's credentials is not proof that an open-source reader can reproduce the checkout.

Keep release notes factual. State features actually implemented, known limitations, upgrade requirements, and security changes. Do not replace a missing benchmark with a slogan about speed. A reliable small scope is more useful than a long checklist whose entries have no executable evidence.

## Migrate from Jenkins by proving equivalence where it matters

Inventory existing jobs, credentials, integrations, schedules, shared libraries, artifact retention, and deployment targets. Classify static supported configurations separately from dynamic or plugin-dependent behavior. An import report should identify gaps before any production switch.

Run a selected pipeline in parallel without giving both systems production mutation authority. Compare actual source revisions, test results, artifact identities, and notifications. Establish who owns the deployment schedule at each stage of migration. Keep a rollback path for the migration itself, including access to the previous job configuration and retained release artifacts.

Full Groovy or plugin compatibility is outside the first release. Document manual translations and the evidence used to approve them. Security policies are part of the migration, not something to add after the commands work.

## Maintain an open project through reviewable changes

The book repository includes contributor guidance, issue templates, a pull-request template, a licensing map, and publication scripts. The application repositories should have comparable ownership rules and release responsibilities. Contributors need to know where a schema change belongs and how to update its consumers.

Require tests or a reproducible explanation for behavioral changes. Review new dependencies for maintenance, licensing, and privilege implications. Keep secrets out of issue reports; use a private reporting path for vulnerabilities when one has been configured. Do not promise an incident-response service level the maintainers cannot provide.

A public roadmap can contain eighty implementation work items without implying that they are complete. Mark scope and evidence clearly. When a task is blocked, record the missing prerequisite rather than changing its acceptance condition until it appears green.

## Publish the book independently

The canonical manuscript is Markdown. The included builder exports a navigable static website, a print PDF, an EPUB, and a sample. The repository can be browsed directly without running the build. This keeps reading and contribution accessible even when the publication host changes.

GitHub Pages supports custom build workflows. The supplied workflow separates validation and artifact construction from the deployment job and limits deployment to the publication branch. Repository settings must enable GitHub Actions as the Pages source before deployment. A local site build is not a hosted deployment result. [S21](e-sources.md#s21) [S22](e-sources.md#s22)

Use a release tag for a reviewed book edition. Attach the PDF and EPUB to a release if desired, and keep the source history open. A reader should be able to identify which edition produced the download and submit a correction against the corresponding manuscript.

## Know what remains beyond the first platform release

Kubernetes execution, autoscaling pools, hosted control-plane billing, public hostile-code execution, additional source providers, and broader operating-system support are separate future tracks. They reuse some contracts but change operational assumptions. Add them through scoped design and evidence, not by silently broadening the original security promise.

The durable core of the system is simpler to state: immutable intent, explicit authority, bounded execution, honest uncertainty, and observable recovery. Every new feature should preserve those properties.

## Exercise

A workspace release is public, but its contracts tag exists only in a maintainer's local repository. The maintainer can build everything. What should the release gate do?

## Worked answer

Fail the consumer-resolution gate. Publish the dependency through the authorized release process, ensure the pinned commit remains reachable, and repeat the independent build from a clean environment with the access level promised to readers. A local checkout cannot establish that someone else can reproduce the release.

## Completion evidence

A fresh reader can obtain the source, understand the license, reproduce the documented checks, and distinguish implemented behavior from future work. A fresh operator can identify exact deployable outputs and follow a tested upgrade and recovery procedure.
