# Reproduce and inspect the local Inside orch edition

This is a local, reviewable engineering edition by Aleksandar Popovic. It grants no new public license to the manuscript or the application. Read `RIGHTS.md`, `NOTICE.md` and the bundled font notices. Packaging or a passing local check does not publish the website, establish production readiness or replace the remaining editorial release gates.

## Open the reader package

Extract `inside-orch-offline.zip`, then open `inside-orch/reader/index.html` in a browser. The edition contains all 47 reading sections, worked answers, selected companions, local styles/fonts/images, and the PDF/EPUB under `reader/downloads/`. Navigation, contents, previous/next and answer links require no JavaScript. No local server, search module, account, analytics or service worker is required. Source and commit links remain external references and need an internet connection when followed.

Actual Chromium validation used both file URLs and a disposable server bound only to 127.0.0.1, with JavaScript disabled and external requests denied. All 100 generated HTML documents were visited under each transport; all local target files/fragments,47-section contents, images and representative local fonts passed. Preface/Chapter 4/Appendices A–B fit 390px and 1280px viewports. Eight real navigation assertions passed. The owned server closed after the test. Browser evidence is `validation/publication/offline-reader.json`. Other browser/file-security policies are outside that measured scope. If a browser restricts file access, this optional command serves only the extracted reader directory:

```bash
cd inside-orch/reader
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`, then stop this owned process with Ctrl+C. Do not run the command from your home directory or a directory containing private files.

## Inspect the distinct source package

Extract `inside-orch-sources.zip` into a disposable directory. Paths begin `books/inside-orch/`, preserving the website workspace binding without including unrelated website files. It includes canonical Markdown, 40 answer files, exact source excerpts, original teaching examples, eight lab guides/fixtures, publishing scripts, selected build styles/configuration, asset sources, font notices, source/history indexes, and validation metadata/reviews. `PACKAGE-MANIFEST.json` records every archived input's SHA256 and size.

The complete application/site snapshots, original development prompts, dependency caches, environment/authentication files, application executables and database dumps are excluded. Raw stdout/stderr/transcripts are excluded except four already-published, scoped synthetic lab records needed by chapter references: rollout, security probes, fixed-seed fake load and the owned Docker flow. Validation JSON retains original command/timestamp/outcome metadata; records can point to deliberately omitted raw logs or temporary paths. Retrieve the full website checkout for the original unabridged evidence corpus. Neither archive silently claims those missing transcripts were rerun during packaging.

## Retrieve the exact application source separately

The inspected application is `https://github.com/alekpopovic/orch` at:

```text
cbfc94ade5b57e449d6b73bf1485b1c5b1647022
```

Use a disposable clone, outside the canonical website source/evidence directories:

```bash
git clone https://github.com/alekpopovic/orch.git /tmp/inside-orch-reproduction-app
git -C /tmp/inside-orch-reproduction-app checkout --detach cbfc94ade5b57e449d6b73bf1485b1c5b1647022
git -C /tmp/inside-orch-reproduction-app rev-parse HEAD
```

Compare tracked file hashes with `evidence/source-lock.json` before experiments. `examples/teaching-extensions/` contains book additions; those files are not part of the application commit. Copy only the lab-specific extension into the disposable module as its guide directs. Never patch `evidence/orch/` to make a claim true. `evidence/COMMIT_INDEX.md`, `commits.json`, `prompt-commit-map.json` and `releases.json` distinguish historical associations from current behavior and actual execution. Retrieving a commit does not execute its tests.

## Actual tools and commands

The local publisher/packager ran with Python 3.14.4, markdown-it-py 4.2.0, WeasyPrint 68.0, pypdf 6.20.0, Pillow 12.3.0 and zlib 1.3.1. Browser validation used Node 26.4.0 with the repository's installed Playwright and `/opt/google/chrome/chrome`; the exact browser version is recorded by the validator. Application checks used Go 1.25.0. Docker/PostgreSQL prerequisites, actual engine versions, owned resource labels and laboratory scopes are recorded in `labs/ENVIRONMENT.md`, `validation/labs/summary.json` and the per-lab JSON. Missing external tools must remain blocked rather than be replaced by invented output.

From the website root, the actual publication workflow used:

```bash
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
npm run check:site
```

These site commands require the complete website checkout and its lockfiles; the source ZIP is not a standalone Jekyll website. Its publisher can be inspected and used from the extracted parent containing `books/` after providing the recorded Python dependencies:

```bash
.venv/bin/python books/inside-orch/scripts/build.py pdf
.venv/bin/python books/inside-orch/scripts/build.py epub
```

Install dependencies in a disposable environment using their recorded versions. PDF generation additionally depends on the platform libraries required by WeasyPrint; the installed build platform is recorded by the publication evidence. Do not rerun PDF generation merely to verify the shipped checksum. PDF/EPUB validation and page-by-page typesetting review are distinct gates. Native site acceptance must pass before creating a new offline edition.

After accepted native exports, the commands actually used for prompt 095 were:

```bash
.venv/bin/python books/inside-orch/scripts/build.py offline
node books/inside-orch/scripts/validate_offline_reader.cjs
.venv/bin/python books/inside-orch/scripts/package_release.py
cd books/inside-orch/dist
sha256sum -c SHA256SUMS.txt
```

The packager requires existing passed native-site/quality/offline-browser records and the exact final audited NOTICE. It does not run labs, fetch the application, install tools or publish. In a fresh reproduction, old validation metadata is historical evidence; run the appropriate checks again before accepting new exports. Archive input manifests allow inspection without installing any toolchain.

## Reproducibility limits

ZIP entries use sorted names, fixed UTC timestamp 2026-10-13T00:00:00Z, regular-file 0644 permissions and deflate level 9. The packager creates each archive twice from the same frozen input bytes and requires byte equality, then verifies CRCs and every member hash. Independent `sha256sum -c` checks the final PDF, EPUB and two ZIPs after they exist. Exact compression bytes can depend on Python/zlib versions. `SHA256SUMS.txt` is outside its own checksum set.

Archive determinism does not promise that rebuilding every upstream artifact on another host produces identical bytes. Lab timestamps, generated identities, observed durations and external-engine behavior change between executions. PDF internals and font producer metadata can differ between builds even where page content is visually equal; fonts, platform libraries and rendering versions matter. This was actually observed locally: the final routine build changed the PDF checksum despite unchanged content inputs. All546 decoded page text/content streams and all546 rendered PNG byte sequences matched the previously reviewed PDF; the equivalence evidence is `validation/publication/pdf-rebuild-equivalence.json`. The accepted final download is bound to the new checksum, rather than claiming byte-reproducible PDF generation. Preserve the exact accepted PDF/EPUB and verify their hashes for this edition. New export bytes require the corresponding validation/review gates again. Later release-gate reports and archives are separate snapshots and are not retroactively inserted into this source package.

All checks described here have their scope in actual command records. The first sandboxed loopback attempt was refused by the environment, and an authorized owned-loopback retry succeeded. An initial browser validator queried lazy font readiness too early; its failed record is preserved, and the corrected validator explicitly awaited the local FontFaceSet before the passing rerun. Neither event required a reader CSS/content change.
