#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/build"
OUT_MD="$ROOT/engineering-universal-real-time-tracking-platform.md"
OUT_PDF="$ROOT/engineering-universal-real-time-tracking-platform.pdf"
OUT_EPUB="$ROOT/engineering-universal-real-time-tracking-platform.epub"

mkdir -p "$BUILD"

python - "$ROOT" "$OUT_MD" "$BUILD/body.md" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
out_md = Path(sys.argv[2])
build_body = Path(sys.argv[3])
files = sorted((root / "chapters").glob("*.md"))
parts = [p.read_text(encoding="utf-8").rstrip() for p in files]
body = "\n\n".join(parts) + "\n"
build_body.write_text(body, encoding="utf-8")
front = (root / "metadata.yaml").read_text(encoding="utf-8").rstrip()
combined = "---\n" + front + "\n---\n\n" + body.replace("../assets/", "assets/")
out_md.write_text(combined, encoding="utf-8")
PY

(
  cd "$BUILD"
  pandoc body.md \
    --metadata-file=../metadata.yaml \
    --standalone \
    --toc \
    --toc-depth=2 \
    --section-divs \
    --highlight-style=tango \
    --template=../assets/book-template.html \
    --resource-path=..:../chapters:../assets \
    -o book.html
)

weasyprint "$BUILD/book.html" "$OUT_PDF"

(
  cd "$BUILD"
  pandoc body.md \
    --metadata-file=../metadata.yaml \
    --toc \
    --toc-depth=2 \
    --split-level=2 \
    --css=../assets/epub.css \
    --epub-cover-image=../assets/cover.png \
    --resource-path=..:../chapters:../assets \
    -o "$OUT_EPUB"
)

unzip -t "$OUT_EPUB" >/dev/null
pdfinfo "$OUT_PDF" >/dev/null
printf 'Built:\n%s\n%s\n%s\n' "$OUT_MD" "$OUT_PDF" "$OUT_EPUB"
