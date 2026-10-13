"""Source adapters shared by the book publisher and its completeness checks."""
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('publication', ROOT / 'books/modern-ci-book/scripts/build.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)
agent_spec = importlib.util.spec_from_file_location('agent_publication', ROOT / 'books/agentplane-book/scripts/build.py')
agent_publication = importlib.util.module_from_spec(agent_spec)
agent_spec.loader.exec_module(agent_publication)
secret_spec = importlib.util.spec_from_file_location('secret_publication', ROOT / 'books/Secret_Contract_Operator/tools/build.py')
secret_publication = importlib.util.module_from_spec(secret_spec)
secret_spec.loader.exec_module(secret_publication)
tracking_spec = importlib.util.spec_from_file_location('tracking_publication', ROOT / 'books/universal-tracking-technical-book/scripts/site.py')
tracking_publication = importlib.util.module_from_spec(tracking_spec)
tracking_spec.loader.exec_module(tracking_publication)
orch_spec = importlib.util.spec_from_file_location('orch_publication', ROOT / 'books/inside-orch/scripts/build.py')
orch_publication = importlib.util.module_from_spec(orch_spec)
orch_spec.loader.exec_module(orch_publication)


def catalog():
    log_source = ROOT / 'books/logbranik'
    log_meta = json.loads((log_source / 'publishing/book-metadata.json').read_text(encoding='utf-8'))
    paths = []
    for entry in (log_source / 'manuscript/Book.txt').read_text().splitlines():
        if not entry.strip():
            continue
        path = (log_source / 'lessons' / Path(entry).with_suffix('.md')).resolve()
        if path.parent != log_source / 'lessons' or not path.is_file():
            raise ValueError(f'Invalid LogBranik manuscript entry: {entry}')
        paths.append(path)
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('LogBranik reading order is empty or contains duplicates')
    agent_source = ROOT / 'books/agentplane-book'
    agent_meta = agent_publication.META
    secret_source = secret_publication.ROOT
    secret_meta = secret_publication.meta()
    tracking_source = tracking_publication.ROOT
    tracking_meta = tracking_publication.meta()
    books = [
        dict(id='modern-ci', source=publication.ROOT, output=ROOT / 'book-pages/modern-ci',
             files=ROOT / 'assets/books/modern-ci', files_url='/assets/books/modern-ci',
             metadata=publication.meta(), paths=publication.selection(),
             editions=publication.DIST, filename='modern-ci-book', chapter_group='Chapters',
             chapter_label='Chapter', licenses=['LICENSE.md', 'LICENSE-BOOK.md', 'LICENSE-CODE.txt']),
        dict(id='logbranik', source=log_source, output=ROOT / 'book-pages/logbranik',
             files=ROOT / 'assets/books/logbranik', files_url='/assets/books/logbranik',
             metadata={key: log_meta[key] for key in ['title', 'subtitle', 'author', 'edition', 'language', 'brand']} | dict(
                 description='A practical field guide to Nginx Open Source: local IP guards, signed policies, reliable log ingestion, and a Python laboratory with a Go/PostgreSQL production design.',
                 cover_image='/assets/books/logbranik/book-cover.png'),
             paths=paths, editions=log_source / 'output', filename='nginx-log-security',
             chapter_group='Lessons', chapter_label='Lesson',
             licenses=['LICENSE.md', 'LICENSE-CONTENT.md', 'LICENSE-CODE', 'CONTENT_RIGHTS.md']),
        dict(id='agentplane', source=agent_source, output=ROOT / 'book-pages/agentplane',
             files=ROOT / 'assets/books/agentplane', files_url='/assets/books/agentplane',
             metadata={key: agent_meta[key] for key in ['title', 'subtitle', 'author', 'edition', 'language']} | dict(
                 brand='AgentPlane', language_label='English',
                 description='Design a Kubernetes-native platform for AI agents: tenant isolation, durable commands, runtime boundaries, tool approvals, usage accounting, and recovery. Includes teaching examples and implementation exercises.',
                 cover_image='/assets/books/agentplane/book/assets/cover.png',
                 text_license='CC BY-SA 4.0', license_url='https://creativecommons.org/licenses/by-sa/4.0/',
                 license_note='Text and diagrams CC BY-SA 4.0 · Original code MIT'),
             paths=[agent_source / path for path in agent_publication.DOCS],
             editions=agent_source / 'dist', filename='AgentPlane-Book',
             chapter_group='Chapters', chapter_label='Chapter', epub_offset=2,
             cover='book/assets/cover.png',
             licenses=['LICENSE.md', 'NOTICE.md', 'licenses/MIT.txt']),
        dict(id='secret-contract-operator', source=secret_source,
             output=ROOT / 'book-pages/secret-contract-operator',
             files=ROOT / 'assets/books/secret-contract-operator', files_url='/assets/books/secret-contract-operator',
             metadata={key: secret_meta[key] for key in ['title', 'subtitle', 'author', 'brand', 'edition', 'language', 'description']} | dict(
                 schema_author={'@type': 'Organization', 'name': 'Codepop Engineering'},
                 language_label='English', edition_label='Edition',
                 cover_image='/assets/books/secret-contract-operator/assets/cover.png',
                 legacy_download_filenames=['Secret_Contract_Operator_Tehnicka_knjiga_SR'],
                 license_note='Project specification and development guide',
                 publication_notes='# Publication and attribution\n\nSecret Contract Operator — Designing a Safe Kubernetes Operator. Codepop Engineering, English edition 1.0, October 10, 2026.\n\nThe complete manuscript, companion material, cover, and diagrams have been translated into English. PDF and EPUB are generated from the same English source. Edition attribution translates the supplied credit as “Prepared for Codepop”.\n\nThe supplied package does not include a text or code license. No Creative Commons or MIT grant is added by this website.\n\nSee the [publication guide](companion/README.html) and [edition validation report](companion/TEST_REPORT.html) for scope and recorded checks.'),
             paths=sorted((secret_source / 'chapters').glob('*.md')),
             editions=secret_publication.DIST, filename=secret_publication.NAME,
             chapter_group='Chapters', chapter_label='Chapter', cover='assets/cover.png', licenses=[]),
        dict(id='universal-tracking', source=tracking_source,
             output=ROOT / 'book-pages/universal-tracking',
             files=ROOT / 'assets/books/universal-tracking', files_url='/assets/books/universal-tracking',
             metadata={key: tracking_meta[key] for key in ['title', 'subtitle', 'description']} | dict(
                 author=', '.join(tracking_meta['author']), edition='1.0', edition_label='Edition',
                 language=tracking_meta['lang'], language_label='English', brand='Universal Tracking',
                 cover_image='/assets/books/universal-tracking/assets/cover.png',
                 license_note='Copyright © 2026 Aleksandar Popovic · All rights reserved',
                 publication_notes='# Publication and attribution\n\nEngineering a Universal Real-Time Tracking Platform. Aleksandar Popovic, first edition, October 2026.\n\nCopyright (c) 2026 Aleksandar Popovic. All rights reserved. The website preserves the supplied manuscript, cover, diagrams, and complete PDF/EPUB editions. No Creative Commons or MIT grant is added.\n\nThe book describes a reference architecture and implementation guidance. Its examples are educational; the supplied publication is not a deployed tracking service.\n\nSee the [publication guide](companion/README.html) and [original validation report](companion/VALIDATION_REPORT.html) for source layout, build instructions, and recorded publication checks.'),
             paths=tracking_publication.selection(), editions=tracking_source, filename=tracking_publication.NAME,
             epub_chapters=tracking_publication.epub_sections(),
             chapter_group='Chapters', chapter_label='Chapter', cover='assets/cover.png', licenses=[]),
        dict(id='inside-orch', source=orch_publication.ROOT,
             output=ROOT / 'book-pages/inside-orch', files=ROOT / 'assets/books/inside-orch',
             files_url='/assets/books/inside-orch',
             metadata=orch_publication.meta() | dict(
                 language_label='English', edition_label='Edition',
                 cover_image='/assets/books/inside-orch/publication/cover.png',
                 license_note='Copyright © 2026 Aleksandar Popovic · All rights reserved',
                 publication_notes='# Publication and attribution\n\nInside orch: Building and Operating a Docker Orchestrator in Go. Aleksandar Popovic, edition 1.0, October 13, 2026.\n\nCopyright © 2026 Aleksandar Popovic. All rights reserved. No new public license is granted for the original manuscript. Exact source excerpts and third-party materials retain their existing rights and notices; the book does not relicense the Orch repository.\n\nThis source-based engineering edition distinguishes executable behavior, package-level experiments, teaching extensions and proposed improvements. Laboratory results describe their recorded environments, not production certification.\n\nSee the [rights statement](/assets/books/inside-orch/publication/RIGHTS.md) and [attribution notices](/assets/books/inside-orch/publication/NOTICE.md).'),
             paths=orch_publication.selection(), editions=orch_publication.DIST,
             filename=orch_publication.NAME, epub_chapters=orch_publication.epub_sections(),
             chapter_group='Chapters', chapter_label='Chapter', cover='publication/cover.png',
             licenses=['publication/RIGHTS.md', 'publication/NOTICE.md',
                       'publication/fonts/dm-sans-OFL.txt', 'publication/fonts/passion-one-OFL.txt',
                       'publication/fonts/dejavu-sans-mono-LICENSE.txt',
                       'publication/fonts/noto-color-emoji-OFL.txt'])
    ]
    for book in books:
        book['metadata'].setdefault('language_label', 'English')
        book['metadata'].setdefault('edition_label', 'Open edition')
        if book['id'] in {'modern-ci', 'logbranik'}:
            book['metadata'].update(license_note='Text CC BY 4.0 · Original code MIT',
                                    license_url='https://creativecommons.org/licenses/by/4.0/')
        if not book['paths'] or len({p.stem for p in book['paths']}) != len(book['paths']):
            raise ValueError(f'Empty or duplicate reading order: {book["id"]}')
        if any(not p.is_file() or not p.resolve().is_relative_to(book['source']) for p in book['paths']):
            raise ValueError(f'Invalid manuscript path: {book["id"]}')
    return books


def chapter_title(book, path):
    if book['id'] == 'inside-orch':
        return orch_publication.title(path)
    return tracking_publication.title(path) if book['id'] == 'universal-tracking' else publication.title(path)


def section(book, path, index):
    title = chapter_title(book, path)
    if index == 0:
        return 'Preface', 'Preface'
    appendix = re.match(r'^(?:Appendix|Dodatak) ([A-Z])(?:\.| -)', title)
    if appendix:
        return 'Appendices', f'Appendix {appendix[1]}'
    number = re.match(r'^(?:Chapter )?(\d+)(?:\.| -)', title)
    if number:
        return book['chapter_group'], f'{book["chapter_label"]} {int(number[1])}'
    return 'References', 'References'


def resolve_reference(book, origin, target):
    if book['id'] == 'inside-orch':
        path = orch_publication.source_reference(origin, target)
        if path and path not in book['paths'] and not orch_publication.permitted_companion(path):
            raise ValueError(f'Unapproved Orch companion: {path}')
        return path
    url = urlsplit(target)
    if url.scheme or url.netloc or not url.path:
        return None
    path = (origin.parent / unquote(url.path)).resolve()
    if not path.is_relative_to(book['source']) or not path.is_file():
        raise ValueError(f'Invalid local publication reference: {origin}: {target}')
    return path


def public_reference(book, origin, target):
    path = resolve_reference(book, origin, target)
    if path is None:
        return target
    url = urlsplit(target)
    suffix = ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')
    base = f'/books/{book["id"]}/'
    if path in book['paths']:
        return base + path.stem + '.html' + suffix
    rel = path.relative_to(book['source']).as_posix()
    if rel in {'book/index.md', 'SUMMARY.md'}:
        return base + '#contents'
    if path.name in {f'{book["filename"]}.{ext}' for ext in ['pdf', 'epub', 'md']}:
        return f'{book["files_url"]}/downloads/{path.name}' + suffix
    if path.suffix == '.md':
        return base + 'companion/' + str(Path(rel).with_suffix('.html')) + suffix
    return f'{book["files_url"]}/{rel}' + suffix


def local_references(book, path):
    if book['id'] == 'agentplane':
        targets = [match[1] for match in agent_publication.LINK_RE.findall(path.read_text())]
    else:
        tokens = publication.MD.parse(path.read_text())
        targets = [child.attrGet('href') if child.type == 'link_open' else child.attrGet('src')
                   for token in tokens for child in token.children or [] if child.type in {'link_open', 'image'}]
    return [p for target in targets if (p := resolve_reference(book, path, target)) is not None]


def render(book, path):
    if book['id'] == 'inside-orch':
        return orch_publication.render(path, 'site', book['paths'])
    if book['id'] == 'agentplane':
        text = agent_publication.LINK_RE.sub(
            lambda m: f'{m[1]}({public_reference(book, path, m[2])})', path.read_text(encoding='utf-8'))
        return agent_publication.markdown(text)
    if book['id'] in {'secret-contract-operator', 'universal-tracking'}:
        tokens = (tracking_publication.tokens(path) if book['id'] == 'universal-tracking'
                  else publication.MD.parse(path.read_text(encoding='utf-8')))
        used = {}
        for i, token in enumerate(tokens):
            if token.type == 'heading_open':
                base = path.stem if token.tag == 'h1' else agent_publication.slug(tokens[i + 1].content)
                count = used.get(base, 0)
                used[base] = count + 1
                token.attrSet('id', base if count == 0 else f'{base}-{count}')
            for child in token.children or []:
                attribute = 'href' if child.type == 'link_open' else 'src' if child.type == 'image' else None
                if attribute:
                    if child.type == 'image':
                        image_path = resolve_reference(book, path, child.attrGet('src'))
                        if image_path and image_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                            with Image.open(image_path) as image:
                                child.attrSet('width', str(image.width))
                                child.attrSet('height', str(image.height))
                    child.attrSet(attribute, public_reference(book, path, child.attrGet(attribute)))
        return publication.MD.renderer.render(tokens, publication.MD.options, {})
    html = publication.render(path, 'site')
    if book['id'] == 'logbranik':
        html = html.replace('src="resources/', f'src="{book["files_url"]}/resources/')
    return html
