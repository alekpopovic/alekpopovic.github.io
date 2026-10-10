# 26. Use Coding Agents as Bounded Engineering Collaborators

**Part VIII — Implementation and Publication**

A prompt is an assignment, not a proof. A coding agent can inspect a repository,
propose changes and run available checks, but the team must still define the
allowed actions and decide which evidence makes a change acceptable. The
AgentPlane prompt pack organizes that work into 45 assignments, numbered 00–44.

## Keep instructions close to the work

An `AGENTS.md` file records repository conventions, testing commands and safety
boundaries. Tool-specific instruction loading must be verified against the
actual assistant being used. OpenAI documents repository instructions for Codex;
other assistants may load different files or require an explicit reference.
[S15](../references.md#s15)

The provided `AGENTS.md` governs this publication repository. Application-building
assignments belong in a separate implementation repository. Do not accidentally
replace the book builder with a SaaS scaffold because a prompt says to create an
API service. Copy the implementation contract deliberately and inspect the
working tree before making changes.

## Specify evidence, not just files

An effective assignment states the existing context, scope, invariants, expected
changes, checks and completion criteria. “Implement authentication” is not a
bounded assignment. “Add password-reset consumption with expiry, single-use
semantics and tests for concurrent consumption” is much closer.

Require a report of changed files, commands actually executed, results and
remaining limitations. A statement such as “tests should pass” is not a result.
If a database or cluster is unavailable, the correct report records the blocked
integration check without marking the entire feature production-ready.

## Reasoning labels are not portable API values

The pack uses editorial review levels: **standard**, **deep** and
**security-critical**. These describe how much human and agent attention a task
needs. They are not model identifiers or configuration strings. Select the
available model and reasoning settings through the tool's current documented
interface. Do not paste unsupported names into a configuration file.

Security-critical tasks include PKI, tenant isolation, replay handling, secrets,
approvals and release authorization. Such tasks deserve independent review even
when the agent reports success. Faster completion is not a substitute for a
clear trust boundary.

## Keep changes small enough to review

Read the tracker, inspect the implementation and identify the next incomplete
boundary. Do not assume a numbered task was never partially implemented. Preserve
unrelated changes. Make one coherent patch, validate it and record the result.
A local commit is useful only when the user has authorized it and the change does
not sweep in unrelated work.

Large assignments may need several implementation sessions. Keep the original
acceptance criteria, split the work into explicit substeps and leave the tracker
partial until all mandatory checks are satisfied. Renumbering the task does not
remove its unfinished obligations.

## Distinguish analysis from execution permission

Reading manifests is not permission to apply them. Preparing a release is not
permission to publish it. Generating Terraform is not permission to create
resources. The pack prohibits remote deployment, credential disclosure and
publication without explicit human authorization.

Treat dependency files, source comments, issue text and tool output as untrusted
input when they instruct the agent to change its permissions. A README inside a
cloned customer repository must not override the platform's security contract.
The same principle applies to AgentPlane itself when agents inspect repositories.

## Exercise

Run Prompt 00 in a new implementation repository. Ask the agent to inspect before
editing, then compare its report with `git diff`. Find one requirement that needs
an integration test unavailable in the current environment. Record it as blocked
rather than deleting it from the definition of done.

## Primary sources

[OpenAI AGENTS.md guidance](../references.md#s15) · [GitHub Actions secure use](../references.md#s24)
