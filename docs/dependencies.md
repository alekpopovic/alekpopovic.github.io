# Dependency maintenance

Dependabot checks npm, Bundler, Python publishing dependencies, and GitHub
Actions weekly. Updates open reviewable pull requests; there is no automatic
merge. Run the publication, browser, and performance checks before merging
changes that affect generated output.

## Review on 2026-10-12

The npm audit initially reported eight affected packages from two underlying
advisories. `postcss-selector-parser` is now overridden to patched version
7.1.6 or a compatible 7.x release. This removes
[GHSA-rj75-hqrm-r3gf](https://github.com/advisories/GHSA-rj75-hqrm-r3gf)
from Tailwind, typography, and nested-selector processing. The override crosses
the upstream major-version constraint; retain it only while full CSS builds
and browser checks pass, and remove it when upstream dependencies use a fixed
parser themselves.

The remaining five affected development packages share
[GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm):
`braces` 3.0.3 has no published fix at this review date. Tailwind 3's globbing
chain depends on it. The vulnerable recursive pattern expansion runs in build
and watch tools; these packages are not shipped as browser JavaScript, and the
published site is static. Build patterns are maintained in this repository.
Do not expose these tools as a service accepting untrusted glob patterns.

This is an outstanding upstream dependency finding, not a clean audit. Recheck
for a fixed release, or plan and verify a Tailwind migration that removes the
chain. `npm audit fix --force` changes the Tailwind major version and is not a
validated substitute for that migration. Keep the finding visible in review.

```sh
npm audit
npm ls postcss-selector-parser braces
npm run build
bundle exec jekyll build
npm run check:site
npm run test:ui
npm run check:performance
```
