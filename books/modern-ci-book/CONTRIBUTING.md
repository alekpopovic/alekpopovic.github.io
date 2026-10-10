# Contributing

Edit canonical prose in `manuscript/`. Keep one chapter per file and preserve the order in `manuscript/Book.txt`. The sample selection is in `manuscript/Sample.txt`. Do not edit exported HTML, PDF, or EPUB as the source of a correction.

Run `make check`, then rebuild the affected formats. A behavior change needs a test or a concrete explanation of the missing test environment. Do not claim that a SQL snippet or runtime configuration was executed unless a recorded check actually did so.

Keep the product design and the small in-memory laboratory clearly distinguished. Preserve the separate-repository ownership model and the trusted dedicated-runner scope. Add primary references for external tool behavior, with the date checked, in `sources.json` and the sources appendix.

Open an issue for a substantial scope change before reorganizing chapters. A pull request should explain the problem, the correction, its affected sections, and its verification. Keep diagrams readable in text-only form. Do not include credentials, private build logs, customer identifiers, or copied proprietary configuration.

By contributing original material, you offer it under the applicable license in `LICENSE.md`. Keep third-party notices intact and disclose any third-party material that requires attribution. Maintainers may request a smaller change or additional evidence before merging.
