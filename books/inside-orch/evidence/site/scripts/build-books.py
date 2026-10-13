#!/usr/bin/env python3
"""Generate Jekyll reading pages and complete downloads from the book manuscript."""
from __future__ import annotations
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_page(path: Path, metadata: dict, content: str = '') -> None:
    # JSON scalars are valid YAML; raw protects code examples from Liquid parsing.
    front = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}' for key, value in metadata.items())
    path.write_text(f'---\n{front}\n---\n{{% raw %}}\n{content}\n{{% endraw %}}\n', encoding='utf-8')


def build_book(source, publication, render) -> dict:
    from book_catalog import agent_publication, tracking_publication, chapter_title, local_references, section
    paths, metadata = source['paths'], source['metadata']
    output, files = source['output'], source['files']
    book_id = source['id']
    book_url = f'/books/{book_id}/'
    if book_id == 'logbranik':
        expected = '\n\n'.join(path.read_text() for path in paths)
        if expected != (source['editions'] / 'nginx-log-security.md').read_text():
            raise ValueError('LogBranik editions are out of date. Regenerate them with books/logbranik/tools/build_book.py first.')
    if book_id == 'agentplane' and agent_publication.assemble() != (source['editions'] / 'AgentPlane-Book.md').read_text():
        raise ValueError('AgentPlane editions are out of date. Rebuild the source publication first.')
    if book_id == 'universal-tracking' and tracking_publication.assemble() != (source['editions'] / (source['filename'] + '.md')).read_text():
        raise ValueError('Universal Tracking editions are out of date. Run books/universal-tracking-technical-book/scripts/build-book.sh first.')
    # This directory is exclusively generated; canonical manuscript stays separate.
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (files / 'downloads').mkdir(parents=True, exist_ok=True)
    for extension in ['pdf', 'epub']:
        name = f'{source["filename"]}.{extension}'
        shutil.copy2(source['editions'] / name, files / 'downloads' / name)
        for old_name in metadata.get('legacy_download_filenames', []):
            shutil.copy2(source['editions'] / name, files / 'downloads' / f'{old_name}.{extension}')
    for name in source['licenses']:
        (files / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source['source'] / name, files / name)
    if source.get('cover'):
        cover = files / source['cover']
        cover.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source['source'] / source['cover'], cover)
    if book_id == 'logbranik':
        shutil.copy2(source['source'] / 'branding/book-cover.png', files / 'book-cover.png')
        shutil.copy2(source['source'] / 'branding/FONT_NOTICE.txt', files / 'FONT_NOTICE.txt')
        shutil.copytree(source['source'] / 'lessons/resources', files / 'resources', dirs_exist_ok=True)

    # Publish only referenced companion documents/files, preserving their links.
    # Canonical package directories remain excluded from Jekyll's static copy.
    if book_id in {'agentplane', 'secret-contract-operator', 'universal-tracking'}:
        pending = paths + [source['source'] / 'README.md']
        if book_id == 'secret-contract-operator':
            pending.append(source['source'] / 'TEST_REPORT.md')
        if book_id == 'universal-tracking':
            pending.append(source['source'] / 'VALIDATION_REPORT.md')
        seen = set()
        while pending:
            path = pending.pop()
            if path in seen:
                continue
            seen.add(path)
            rel = path.relative_to(source['source'])
            if path.suffix == '.md' and path.name != source['filename'] + '.md':
                pending.extend(local_references(source, path))
                if path not in paths and str(rel) not in {'book/index.md', 'SUMMARY.md'}:
                    target = output / 'companion' / rel.with_suffix('.html')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    write_page(target, dict(layout='book-license', title=f'{publication.title(path)} · {metadata["title"]}',
                        description=f'Companion material for {metadata["title"]}.', book_id=book_id,
                        noindex=True, sitemap=False, permalink=f'{book_url}companion/{rel.with_suffix(".html")}'), render(source, path))
            elif path not in paths:
                destination = files / ('downloads' if path.name in {source['filename'] + '.' + ext for ext in ['pdf', 'epub', 'md']} else rel.parent) / path.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)

    chapters = []
    for i, path in enumerate(paths):
        group, label = section(source, path, i)
        words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding='utf-8')))
        chapters.append(dict(title=chapter_title(source, path), slug=path.stem,
                             url=f'{book_url}{path.stem}.html', group=group,
                             label=label, reading_minutes=max(1, round(words / 220))))
        rendered = render(source, path)
        rendered = rendered.replace('<table>', '<div class="book-table" role="region" aria-label="Scrollable table" tabindex="0"><table>').replace('</table>', '</table></div>')
        rendered = rendered.replace('<pre>', '<pre tabindex="0" aria-label="Code example">')
        write_page(output / f'{path.stem}.html', dict(
            layout='book', title=f'{chapter_title(source, path)} · {metadata["title"]}',
            description=metadata['description'], book_id=book_id, chapter_index=i,
            permalink=f'{book_url}{path.stem}.html'), rendered)

    if metadata.get('cover_image'):
        from PIL import Image
        with Image.open(ROOT / metadata['cover_image'].lstrip('/')) as cover:
            metadata = dict(metadata, cover_width=cover.width, cover_height=cover.height)
    book = dict(metadata, id=book_id, url=book_url,
                first_chapter=chapters[0]['url'], chapters=chapters,
                chapter_count=sum(c['group'] == source['chapter_group'] for c in chapters),
                chapter_unit=source['chapter_group'].lower(),
                appendix_count=sum(c['group'] == 'Appendices' for c in chapters),
                pdf=f'{source["files_url"]}/downloads/{source["filename"]}.pdf',
                epub=f'{source["files_url"]}/downloads/{source["filename"]}.epub')
    write_page(output / 'index.html', dict(layout='book-overview', title=f'{metadata["title"]}: {metadata["subtitle"]}',
                                         description=metadata['description'], book_id=book_id, permalink=book['url']))
    license_text = metadata.get('publication_notes') or (source['source'] / 'LICENSE.md').read_text(encoding='utf-8')
    if source['licenses']:
        license_text += '\n\n## License files\n\n' + '\n'.join(f'- [{name}]({source["files_url"]}/{name})' for name in source['licenses'])
    if book_id == 'logbranik':
        license_text += f'\n- [Font notices]({source["files_url"]}/FONT_NOTICE.txt)\n'
    license_tokens = publication.MD.parse(license_text)
    for token in license_tokens:
        for child in token.children or []:
            if child.type == 'link_open':
                href = child.attrGet('href')
                if href in source['licenses']:
                    child.attrSet('href', f'{source["files_url"]}/{href}')
    license_html = publication.MD.renderer.render(license_tokens, publication.MD.options, {})
    write_page(output / 'license.html', dict(layout='book-license', title=f'{metadata["title"]} · Licensing',
                                           description=f'Licensing and attribution for {metadata["title"]}.', book_id=book_id,
                                           permalink=f'{book_url}license.html'), license_html)
    print(f'{metadata["title"]}: {len(chapters)} complete sections, PDF and EPUB')
    return book


def main() -> None:
    local_python = ROOT / '.venv' / 'bin' / 'python'
    if local_python.exists() and Path(sys.prefix).resolve() != (ROOT / '.venv').resolve():
        import os
        os.execv(str(local_python), [str(local_python), str(Path(__file__).resolve())])
    from book_catalog import catalog, publication, render, secret_publication
    print('Building complete book editions and reading pages…', flush=True)
    publication.epub()
    publication.pdf()
    secret_publication.build()
    books = [build_book(source, publication, render) for source in catalog()]
    data = ROOT / '_data'
    data.mkdir(exist_ok=True)
    (data / 'books.json').write_text(json.dumps(books, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except (ImportError, OSError, ValueError, RuntimeError) as exc:
        raise SystemExit(f'Book build failed: {exc}\nInstall dependencies: python3 -m pip install -r requirements-books.txt') from exc
