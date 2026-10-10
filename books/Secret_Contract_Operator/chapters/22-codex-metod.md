# 22. Development with Codex and Execution Control

## 22.1 From a Large Request to a Verifiable Task

An AI coding agent is most useful with a clear scope, prior decisions, relevant files, and acceptance criteria. “Build the entire production operator” neither defines what must be checked nor prevents an agent from skipping security boundaries.

Appendix A contains 30 numbered prompts. Each has a goal, constraints, tests, and expected output. The prompts and this edition's explanations are in English. They replace the initial prompt sketch wherever the API has been consolidated.

## 22.2 Shared Context

Before every task, the agent reads `AGENTS.md`, the canonical specification, and security decisions. Keep local copies of relevant chapters in the repository instead of relying on the agent remembering an entire earlier conversation.

When code exists, begin with an inventory of the current state. The agent does not scaffold over an implementation, change the module path without an approved migration, or delete unrelated changes. Document each discrepancy between a prompt and the actual API before implementing a decision.

## 22.3 Complexity Levels, Not Implicit Model Settings

Prompts recommend `Medium` or `High`. These labels describe engineering complexity and expected review. They do not claim that Markdown front matter automatically changes the actual model or its reasoning parameter. Configure the specific client and its supported settings separately.

API, authorization, reconcile, mutation, and rotation tasks are marked High because they require concurrency and security analysis. Documentation and basic scaffolding can be Medium. Neither level replaces tests or human review.

## 22.4 Tracking Model

Each prompt moves through `pending`, `in_progress`, `blocked`, `implemented`, `verified`, and `accepted`. `implemented` means code exists. `verified` means the required checks actually ran. `accepted` requires review of results and boundaries.

```yaml
id: "008"
status: pending
depends_on: ["007"]
complexity: High
commit: null
executed_checks: []
not_run: []
reviewer: null
notes: ""
```

The accompanying `tracking/progress.csv` and `tracking/README.md` provide an initial register. All development prompts start as `pending`: creating the book does not execute those tasks. The separate local Go lab has its own test report.

## 22.5 Safe Task Execution

The agent works locally by default. Commands that modify a cluster require a dedicated test context, and release publication remains an explicit activity. Most development requires neither production kubeconfigs nor cloud credentials.

After every task, the agent reports changed files, commands actually executed, test results, remaining risks, and the next dependency. “Tests should pass” is not a test result.

## 22.6 Stopping Points

The first useful milestone is a pure validator with a status builder. The second is a functional read-only operator reacting to Secret changes. The third is a public MVP with documentation, a chart, CI, and a security audit. Mutation features begin only after that MVP is accepted.

This order prevents conveniences such as injection from hiding unresolved questions about who may read a secret or change an application. Development follows risk rather than the marketing appeal of a demonstration.

**Checkpoint.** Do not mark a prompt accepted merely because an agent finished its answer. A verifiable commit, executed tests, and review findings are required.
