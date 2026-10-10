# Engineering a Universal Real-Time Tracking Platform

**Author:** Aleksandar Popovic  
**Edition:** First Edition, October 2026  
**Language:** English

This source package contains the technical book in combined Markdown, individual chapter files, PDF, and EPUB formats.

## Final architecture

- Go modular monolith with `api`, `worker`, `scheduler`, `gps-gateway`, `migrate`, and `simulator` roles.
- PostgreSQL with PostGIS as the only mandatory infrastructure service.
- PostgreSQL transactional outbox, leased jobs, advisory locks, and `LISTEN/NOTIFY` wake-up signals.
- Angular dashboard and public tracking application.
- Angular, Ionic, and Capacitor mobile shell.
- Native Kotlin Android and Swift iOS background location engines.
- Docker, Docker Compose, and Nginx provider-neutral deployment.

## Source layout

```text
chapters/         Individual Markdown chapters
assets/           Cover, diagrams, and styles
metadata.yaml     Book metadata
README.md         This file
```

## Build

The generated editions were built with Pandoc and WeasyPrint. A local build requires Pandoc, WeasyPrint, Graphviz, and the fonts referenced by the style sheets.

```bash
./scripts/build-book.sh
```

The build script creates a combined Markdown file, an EPUB, and a print PDF, then runs basic archive and PDF checks.
