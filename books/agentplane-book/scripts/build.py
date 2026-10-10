#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the AgentPlane Markdown, static HTML, PDF and EPUB editions.

No network requests, cluster commands or remote publishing are performed.
Python dependencies are pinned in requirements.txt; EPUB also requires Pandoc.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import mistune

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BUILD = ROOT / '.build'
META = json.loads((ROOT / 'book/book.json').read_text(encoding='utf-8'))
DOCS = ['book/preface.md'] + [c['path'] for c in META['chapters']] + META['appendices'] + ['book/references.md']
IDS = {p: ('preface' if p.endswith('/preface.md') else
           'sources' if p.endswith('/references.md') else
           'chapter-' + Path(p).name[:2] if '/chapters/' in p else
           'appendix-' + Path(p).name[0]) for p in DOCS}
LINK_RE = re.compile(r'(!?\[[^\]\n]*\])\(([^)\s]+)\)')


def title(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')


def slug(value: str) -> str:
    value = html.unescape(re.sub(r'<[^>]+>', '', value)).lower()
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'\s+', '-', value.strip()) or 'section'


class Renderer(mistune.HTMLRenderer):
    def __init__(self) -> None:
        super().__init__(escape=False)
        self.seen: dict[str, int] = {}
    def heading(self, text: str, level: int, **attrs: object) -> str:
        base = slug(text)
        count = self.seen.get(base, 0)
        self.seen[base] = count + 1
        ident = base if count == 0 else f'{base}-{count}'
        return f'<h{level} id="{ident}">{text}</h{level}>\n'


def markdown(text: str) -> str:
    return mistune.create_markdown(renderer=Renderer(), plugins=['table', 'strikethrough', 'task_lists'])(text)


def rewrite(text: str, origin: str, *, publication: bool = False, epub: bool = False) -> str:
    """Make chapter-relative paths correct in a combined reading edition."""
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(origin), unquote(parsed.path)))
        if resolved in IDS:
            dest = '#' + (parsed.fragment or IDS[resolved])
        elif resolved in {'book/index.md', 'SUMMARY.md'}:
            dest = '#contents'
        elif label.startswith('!'):
            dest = resolved
            if epub and dest.endswith('.svg') and (ROOT / dest).with_suffix('.png').exists():
                dest = str(Path(dest).with_suffix('.png'))
        elif publication:
            # Companion programs are in the repository, not missing EPUB resources.
            dest = '#companion-files'
        else:
            dest = resolved + ('#' + parsed.fragment if parsed.fragment else '')
        return f'{label}({dest})'
    return LINK_RE.sub(replace, text)


def assemble(*, publication: bool = False, epub: bool = False) -> str:
    text = '# AgentPlane\n\n**Building a Kubernetes-Native Platform for AI Agents**\n\n'
    text += '**English edition 0.1.0 · October 10, 2026**\n\n'
    text += 'AgentPlane Book contributors. Original text and diagrams: CC BY-SA 4.0. Original code: MIT. '
    text += 'This is an educational book, not a released AgentPlane application.\n\n'
    text += '<a id="contents"></a>\n\n# Contents\n\n'
    text += '\n'.join(f'- [{title(p)}](#{IDS[p]})' for p in DOCS) + '\n\n'
    for p in DOCS:
        text += f'<a id="{IDS[p]}"></a>\n\n'
        text += rewrite((ROOT / p).read_text(encoding='utf-8'), p, publication=publication, epub=epub) + '\n\n'
    return text


def build_markdown() -> None:
    (ROOT / 'AgentPlane-Book.md').write_text(assemble(), encoding='utf-8')
    shutil.copyfile(ROOT / 'AgentPlane-Book.md', DIST / 'AgentPlane-Book.md')


def site_target(origin: Path, target: str) -> str:
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith('#'):
        return target
    p = parsed.path
    if p.endswith('.md') and '/dist/' not in ('/' + p):
        p = p[:-3] + '.html'
    return p + ('#' + parsed.fragment if parsed.fragment else '')


def build_html() -> None:
    site = ROOT / '_site'
    if site.exists():
        shutil.rmtree(site)
    site.mkdir()
    ignored = {'.build', '_site', '.venv', '.git', '__pycache__'}
    docs = [p for p in ROOT.rglob('*.md') if not any(part in ignored for part in p.relative_to(ROOT).parts)
            and 'dist' not in p.relative_to(ROOT).parts and p.name != 'AgentPlane-Book.md']
    sidebar = ['<a href="{base}README.html" class="brand">AgentPlane</a>',
               '<a href="{base}book/index.html">Contents</a>']
    for c in META['chapters']:
        dest = c['path'][:-3] + '.html'
        sidebar.append(f'<a href="{{base}}{dest}">{c["number"]:02d} · {html.escape(c["title"])}</a>')
    sidebar.extend(['<a href="{base}labs/README.html">Teaching labs</a>',
                    '<a href="{base}prompts/README.html">Implementation prompts</a>',
                    '<a href="{base}reports/VALIDATION.html">Validation</a>'])
    for source in docs:
        rel = source.relative_to(ROOT)
        target = site / rel.with_suffix('.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        base = '../' * (len(rel.parts) - 1)
        raw = source.read_text(encoding='utf-8')
        raw = LINK_RE.sub(lambda m: f'{m[1]}({site_target(rel, m[2])})', raw)
        body = markdown(raw)
        heading = html.escape(raw.splitlines()[0].lstrip('# '))
        nav = '\n'.join(sidebar).replace('{base}', base)
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{heading} — AgentPlane</title>
<link rel="stylesheet" href="{base}assets/site.css"></head><body>
<a class="skip" href="#main">Skip to content</a><aside><nav aria-label="Book navigation">{nav}</nav></aside>
<main id="main"><header class="edition-label">OPEN ENGINEERING BOOK / ENGLISH 0.1.0</header>{body}
<footer>AgentPlane Book contributors · Text CC BY-SA 4.0 · Code MIT · Educational reference</footer></main></body></html>'''
        target.write_text(page, encoding='utf-8')
    for folder in ['book/assets', 'assets']:
        if (ROOT / folder).exists():
            shutil.copytree(ROOT / folder, site / folder, dirs_exist_ok=True)
    # Source and binary companion downloads stay available alongside rendered pages.
    for folder in ['examples', 'prompts', 'labs', 'scripts', 'licenses', 'dist']:
        if (ROOT / folder).exists():
            shutil.copytree(ROOT / folder, site / folder, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    if (ROOT / 'AgentPlane-Book.md').exists():
        shutil.copyfile(ROOT / 'AgentPlane-Book.md', site / 'AgentPlane-Book.md')
        combined = markdown(assemble(publication=True))
        (site / 'AgentPlane-Book.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AgentPlane — Complete Book</title><link rel="stylesheet" href="assets/site.css"></head><body><main id="main">'+combined+'</main></body></html>')
    shutil.copyfile(site / 'README.html', site / 'index.html')
    (site / '.nojekyll').write_text('')


def build_pdf() -> None:
    from weasyprint import HTML, CSS
    toc = ['<nav class="toc" id="contents"><h1>Contents</h1>']
    part = None
    for p in DOCS:
        record = next((c for c in META['chapters'] if c['path'] == p), None)
        current = record['part'] if record else ('Opening' if p.endswith('preface.md') else 'Appendices and Sources')
        if current != part:
            toc.append(f'<p class="part">{html.escape(current)}</p>');part=current
        toc.append(f'<a href="#{IDS[p]}">{html.escape(title(p))}</a>')
    toc.append('</nav>')
    pieces = []
    for p in DOCS:
        raw = rewrite((ROOT / p).read_text(encoding='utf-8'), p, publication=True)
        pieces.append(f'<section class="chapter" id="{IDS[p]}">{markdown(raw)}</section>')
    cover = '''<div class="cover"><img src="book/assets/cover.svg" alt="AgentPlane: Building a Kubernetes-Native Platform for AI Agents"></div>'''
    colophon = '''<section class="colophon"><p class="eyebrow">OPEN ENGINEERING BOOK / 0.1.0</p><h1>AgentPlane</h1>
<h2>Building a Kubernetes-Native<br>Platform for AI Agents</h2><p class="author">AgentPlane Book contributors</p>
<p>English edition · October 10, 2026</p><hr><p>Original narrative, diagrams and prompt prose are licensed under Creative Commons Attribution-ShareAlike 4.0 International. Original program code and configuration examples are licensed under MIT. See the repository license files for scope and attribution.</p>
<p>This independent educational book develops a proposed reference architecture. It is not a released AgentPlane service, an independent security audit, a compliance certification or official upstream documentation.</p>
<p>Teaching examples and actual checks are identified in the companion repository. Database, cluster and cloud exercises need separate execution in authorized disposable environments. No customer or benchmark results are invented.</p>
<p>Source Markdown, diagrams, code, labs, implementation assignments and build scripts accompany this edition. No public repository address is assumed.</p>
<p class="colophon-note">Read the boundary. Test the invariant. Record the evidence.</p></section>'''
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AgentPlane — Building a Kubernetes-Native Platform for AI Agents</title><meta name="author" content="AgentPlane Book contributors"><meta name="description" content="An open engineering book about secure, reliable agent execution on Kubernetes."></head><body>' + cover + colophon + ''.join(toc) + ''.join(pieces) + '</body></html>'
    (BUILD / 'print.html').write_text(page, encoding='utf-8')
    HTML(string=page, base_url=str(ROOT)).write_pdf(DIST / 'AgentPlane-Book.pdf',
        stylesheets=[CSS(filename=str(ROOT / 'assets/print.css'))])


def build_epub() -> None:
    if not shutil.which('pandoc'):
        raise RuntimeError('Pandoc is required for EPUB. See BUILDING.md.')
    source = BUILD / 'epub-source.md'
    source.write_text(assemble(publication=True, epub=True), encoding='utf-8')
    metadata = BUILD / 'epub-metadata.yaml'
    metadata.write_text('''title: AgentPlane
subtitle: Building a Kubernetes-Native Platform for AI Agents
author: AgentPlane Book contributors
lang: en
date: 2026-10-10
identifier: urn:uuid:8a6a3f66-a950-4d36-864d-e316c0243ea9
rights: "Original text and diagrams: CC BY-SA 4.0. Original code: MIT. See license scope in the companion repository."
description: "An open engineering book on tenant isolation, secure agent execution, tool governance, evidence and recovery in Kubernetes."
''')
    command = ['pandoc', str(source), '--from=markdown', '--to=epub3', '--standalone',
        '--toc', '--toc-depth=1', '--split-level=1', '--epub-title-page=false',
        '--metadata-file', str(metadata), '--resource-path', str(ROOT),
        '--epub-cover-image', str(ROOT / 'book/assets/cover.png'),
        '--css', str(ROOT / 'assets/epub.css'), '--output', str(DIST / 'AgentPlane-Book.epub')]
    subprocess.run(command, check=True, cwd=ROOT)


def checksums() -> None:
    lines = []
    for p in sorted(DIST.glob('AgentPlane-Book.*')):
        lines.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}')
    (DIST / 'SHA256SUMS').write_text('\n'.join(lines) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--format', choices=['all', 'md', 'html', 'pdf', 'epub'], default='all')
    args = parser.parse_args()
    DIST.mkdir(exist_ok=True);BUILD.mkdir(exist_ok=True)
    build_markdown()
    if args.format in ('all','pdf'): build_pdf()
    if args.format in ('all','epub'): build_epub()
    checksums()
    if args.format in ('all','html'): build_html()
    print(f'Built {args.format}: {DIST}; Markdown: {ROOT / "AgentPlane-Book.md"}')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f'Build failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
