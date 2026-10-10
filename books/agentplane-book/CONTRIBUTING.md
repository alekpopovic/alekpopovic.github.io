# Contributing

Use a focused pull request for one correction, exercise or build improvement.
Describe the problem, change, relevant sources, checks executed and limitations.
Edit chapter sources rather than only generated editions. Keep the book in
English; translations should be separate, clearly attributed editions.

Technical claims should cite primary documentation and identify any version
assumptions. Examples need tests proportional to their behavior. Never replace a
failing security test with a weaker assertion merely to make CI pass. Do not
submit real credentials, kubeconfigs, private logs or customer files.

Run `make verify` and rebuild affected formats. Changes to layout need visual
inspection. Changes to published security claims need a reviewer who understands
the trust boundary. CI success alone is not independent security review.

Contributions are provided under the repository's applicable text or code
license. Confirm that you have the right to contribute the material. Disclose
substantial AI assistance and verify its output; do not invent sources or test
results. Read LICENSE.md for the material-by-material allocation.
