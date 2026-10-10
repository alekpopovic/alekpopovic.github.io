# Building reading editions

The canonical sources are UTF-8 Markdown files listed in
`manuscript/Book.txt`. There is no remote publishing step in the local builder.
It writes only `dist/`. Building the website replaces `dist/site/`.

## Prerequisites

Use Python 3.11+ in a virtual environment. Website and EPUB export need only
`requirements-site.txt`. The Go laboratory has no third-party modules; the race
detector additionally requires a C toolchain on a supported host.

PDF export uses `requirements-print.txt`, WeasyPrint, Pango, HarfBuzz and locally
installed fonts. Consult the [official WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
for your operating system. The GitHub workflow targets Ubuntu 24.04 and installs
these dependencies explicitly. A typical Ubuntu preparation is:

```bash
sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 \
  libharfbuzz-subset0 fonts-dejavu-core
python -m pip install -r requirements-print.txt
```

The styles request DejaVu Serif, Sans and Sans Mono. Font files are not included
in the repository. A different installed font set or renderer version can
change pagination. Record your dependency versions for a release; the listed
Python requirements are top-level pins, not a complete transitive lock file.

## Commands

```bash
python scripts/check.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/build.py site
python scripts/build.py epub
python scripts/build.py pdf
python scripts/build.py sample
```

`python scripts/build.py all` exports EPUB, both PDFs and the website. Website
exports copy any available PDF/EPUB files from `dist/` into their downloads
folder. Run the PDF and EPUB steps before the site step to include reading
editions in the site.

`make check` runs publication checks and Go unit, race and vet checks. `make all`
runs that gate before building all editions. No PostgreSQL, Docker, Angular or
cloud integration is tested by these targets.

## Review a release

Read the generated contents page and follow internal links. Inspect PDF covers,
tables, code blocks, source references and page boundaries. Validate EPUB XML
and links; use an external EPUBCheck installation for a formal conformance gate.
The included structural tests are not a substitute for EPUBCheck or a device
compatibility test.

The builder accepts the local trusted manuscript, not arbitrary customer HTML.
Raw Markdown HTML is disabled. No network images, scripts, external fonts or
analytics are included. Do not convert this utility into a public upload service
without a separate resource and network-isolation design.

## Manuscript platforms

`Book.txt` and `Sample.txt` also provide a simple manuscript order for external
publishing workflows. A platform may support a different Markdown dialect.
Review relative links and formatting in that platform's own preview. This
edition does not claim a tested Leanpub upload or store publication.
