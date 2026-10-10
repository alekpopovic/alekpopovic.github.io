# 28. Maintain an Open Book Like a Software Project

**Part VIII — Implementation and Publication**

An open technical book is a maintained body of claims. Its chapters, examples,
references and build scripts evolve together. GitHub provides a collaboration
surface, but the project still needs review rules, licenses, versioning and a
clear distinction between source material and generated editions.

## Keep Markdown authoritative

The files under `book/chapters` are the primary narrative source. The publication
builder assembles a complete Markdown edition, a static website, a printable PDF
and a reflowable EPUB. Fix the source rather than patching an exported PDF by hand.
Generated outputs should identify the edition and preserve their source mapping.

The assembled Markdown is convenient for searching and importing into reading
tools. Individual chapters make pull requests easier to review. The PDF has a
fixed layout and page references; the EPUB follows reader-selected text size and
screen dimensions. Do not use PDF page numbers as the only navigation mechanism.

## Separate review from publishing

Pull requests validate the sources and teaching examples. Publishing runs from a
trusted branch or an explicitly approved release workflow. Pages deployment needs
its own permissions and environment configuration. GitHub documents the custom
workflow mechanism; enabling that workflow is an account-side step, not something
a downloaded ZIP has already performed. [S16](../references.md#s16)

Keep action references immutable and review dependency changes. Do not grant a
pull-request job the ability to create a public release. A generated HTML artifact
contains contributor-controlled text, so treat it as publication content rather
than trusted executable infrastructure.

## Allocate licenses clearly

This edition assigns original narrative, diagrams and prompt prose to CC BY-SA
4.0, and original code and configuration examples to MIT. The root license file
states the boundaries. Third-party projects retain their own licenses and names.
Readers must not interpret the book's grant as permission to relicense upstream
software. [S18](../references.md#s18) [S19](../references.md#s19)

Keep attribution and change notices when adapting text. A source-repository URL
should be added when the publisher creates the actual repository; this edition
does not invent one. Following architectural ideas does not by itself place an
independently written application under the book's narrative license.

## Version claims as well as files

A book edition records its publication date, tested build tools and source review
notes. Application dependencies have separate compatibility records. A newer
upstream release does not automatically make the book obsolete, but it may
invalidate example fields or assumptions. Track the affected adapter and tests.

Corrections deserve visibility. Use an errata issue for factual mistakes and a
security-reporting route for vulnerabilities in runnable examples. Avoid posting
real credentials, customer logs or exploit details against a live installation
in a public issue. The repository security policy explains the intended route.

## Review an edition before sharing it

Check that every chapter appears in all formats, internal links resolve, diagrams
have meaningful alternatives, code remains legible and no temporary credentials
or font files are included. Validate the EPUB structure and visually inspect PDF
pages, especially tables and code. Automated build success does not prove a
pleasant reading experience.

Document checks that were not possible. A local build does not show that GitHub
Pages is enabled on a future repository, that a Kindle renders every table
perfectly, or that a Kubernetes integration has passed. Honest limits make the
next maintainer's work more efficient.

## Exercise

Make a small correction to one chapter, rebuild every format and inspect its
rendered location. Submit a pull request containing the source change and its
validation notes. Explain whether the change affects only prose, executable
examples or an advertised security property.

## Primary sources

[GitHub Pages custom workflows](../references.md#s16) · [CC BY-SA 4.0 legal code](../references.md#s18) · [MIT License](../references.md#s19) · [GitHub Actions secure use](../references.md#s24)
