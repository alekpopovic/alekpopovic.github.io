# AI engineering workshops

Original practice material by Aleksandar Popovic. Requirements: Node.js 20+
and a terminal. There are no dependencies to install and no API calls.

Extract the archive, open a terminal in this directory, and choose an exercise:

| ID | Exercise | Guide |
| --- | --- | --- |
| bugfix | Numeric priority and immutable input | https://www.alekpopovic.com/posts/ai-workshop-fix-a-priority-bug/ |
| review | Review an event for data exposure | https://www.alekpopovic.com/posts/ai-workshop-review-a-logging-change/ |
| tests | Test retry timing boundaries | https://www.alekpopovic.com/posts/ai-workshop-design-retry-tests/ |
| automation | Reproducible release manifests | https://www.alekpopovic.com/posts/ai-workshop-automate-release-evidence/ |

Run `node verify.mjs bugfix` (replace the ID for other exercises). The supplied
starter is intentionally faulty. Read its tests, ask your coding assistant for
a focused explanation, edit that exercise's `app.mjs`, and run it again.

`node verify.mjs bugfix --solution` runs the separate worked solution. Compare
it after attempting the exercise. `node verify-all.mjs` checks that each
untouched starter fails assertions and each supplied solution passes. This
maintainer check expects untouched starter files; it is not a score for your edits.

AI assistance is optional. A model's answer is not test evidence. Keep the
command, exit status, changed code, and a short explanation of the boundary cases.

## Further exercises

Run `node verify.mjs gate` to reject stale deployment evidence, or
`node verify.mjs replay` to recover an ordered tenant stream. Each has eight
acceptance tests and three stages with progressive hints in the website.
The examples use synthetic data and make no Kubernetes or socket connections.
