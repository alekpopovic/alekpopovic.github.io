# Dependency maintenance

Dependabot checks npm, Bundler, Python publishing dependencies, and GitHub
Actions weekly. Review generated output and run publication, browser, and
performance checks before merging. Updates are not merged automatically.

## Review on 2026-10-13

The Tailwind 3 globbing chain containing `braces` 3.0.3 was removed. Tailwind
4.3.3 now runs through its official PostCSS plugin in `scripts/build-css.mjs`.
The separate CLI was deliberately omitted: its file watcher still introduced
the affected chain. `scripts/watch-css.mjs` uses Node's native filesystem watcher.
The lockfile contains neither `braces` nor `micromatch` nor `@parcel/watcher`.
A registry-backed `npm audit` reports **zero known vulnerabilities** at this
review date. This is a point-in-time npm result, not a claim about every runtime
or publishing dependency.

`postcss-selector-parser` is a direct development dependency and its override
uses that same patched 7.1.6 version. The typography plugin's older major-version
constraint is overridden; retain this only while full CSS builds and browser
checks pass. Remove it when upstream uses a fixed parser itself.

Tailwind 4 requires modern browsers: Safari 16.4+, Chrome 111+, Firefox 128+.
Explicit local source paths replace automatic repository scanning. Shared
reader/AI shells and homepage card styles are generated from the same stylesheet;
per-page budgets include every linked CSS file and deferred Worker/vitals code.
Local fonts retain their licenses and builds never download fonts or browser
assets. The upstream web-vitals core is vendored from the locked npm package
with its Apache license during the ordinary asset build.

```sh
npm ci
npm audit
npm ls postcss-selector-parser braces
npm run build
bundle exec jekyll build
npm run check:site
npm run test:ui
npm run check:performance
```

Sources:
- [Tailwind 4 upgrade guide](https://tailwindcss.com/docs/upgrade-guide)
- [Source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files)
- [braces advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm)
- [selector parser advisory](https://github.com/advisories/GHSA-rj75-hqrm-r3gf)
