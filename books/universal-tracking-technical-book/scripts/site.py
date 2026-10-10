"""Adapt the supplied Pandoc manuscript to the site's shared book reader."""
from pathlib import Path
import html
import re

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token

ROOT = Path(__file__).resolve().parents[1]
NAME = 'engineering-universal-real-time-tracking-platform'
MD = MarkdownIt('commonmark', {'html': False, 'xhtmlOut': True}).enable('table')
ATTRIBUTES = re.compile(r'\s*\{(?:[.#][\w-]+\s*)+\}$')


def meta():
    return yaml.safe_load((ROOT / 'metadata.yaml').read_text(encoding='utf-8'))


def selection():
    return sorted((ROOT / 'chapters').glob('*.md'))


def assemble():
    body = '\n\n'.join(path.read_text(encoding='utf-8').rstrip() for path in selection()) + '\n'
    front = (ROOT / 'metadata.yaml').read_text(encoding='utf-8').rstrip()
    return '---\n' + front + '\n---\n\n' + body.replace('../assets/', 'assets/')


def title(path):
    if path.name == '00-front-matter.md':
        return 'Preface'
    for token in MD.parse(path.read_text(encoding='utf-8')):
        if token.type == 'inline' and re.match(r'^(Chapter \d+|Appendix [A-Z]) - ', token.content):
            return token.content
    return next(ATTRIBUTES.sub('', line.lstrip('# ').strip())
                for line in path.read_text().splitlines() if line.startswith('#'))


def tokens(path):
    result = MD.parse(path.read_text(encoding='utf-8'))
    front_matter = path.name == '00-front-matter.md'
    first_heading = True
    for index, token in enumerate(result):
        if token.type == 'heading_open':
            inline = result[index + 1]
            inline.content = ATTRIBUTES.sub('', inline.content)
            inline.children = MD.parseInline(inline.content)[0].children
            if front_matter:
                level = 1 if first_heading else int(token.tag[1:]) + 1
            elif re.match(r'^(Chapter \d+|Appendix [A-Z]) - ', inline.content):
                level = 1
            elif token.tag == 'h1':
                # Preserve part titles as section context above the chapter heading.
                token.tag = result[index + 2].tag = 'p'
                token.attrSet('class', 'eyebrow')
                first_heading = False
                continue
            else:
                level = max(2, int(token.tag[1:]) - 1)
            token.tag = result[index + 2].tag = f'h{level}'
            first_heading = False
        children = token.children or []
        if children and children[0].type == 'text':
            task = re.match(r'^\[([ xX])\]\s+', children[0].content)
            if task:
                children[0].content = children[0].content[task.end():]
                checkbox = Token('html_inline', '', 0)
                checked = ' checked=""' if task[1].lower() == 'x' else ''
                label = html.escape(children[0].content, quote=True)
                checkbox.content = f'<input type="checkbox" disabled=""{checked} aria-label="{label}" /> '
                children.insert(0, checkbox)
        for child_index, child in enumerate(children):
            if child.type == 'image' and child_index + 1 < len(children):
                following = children[child_index + 1]
                if following.type == 'text':
                    following.content = re.sub(r'^\{width=\d+%\}', '', following.content)
    return result


def epub_sections():
    # Pandoc splits this edition at levels 1 and 2, including the front matter
    # and part headings. One online section can therefore span several files.
    sections, index = {}, 1
    for path in selection():
        headings = [token for token in MD.parse(path.read_text())
                    if token.type == 'heading_open' and token.tag in {'h1', 'h2'}]
        sections[path.stem] = [f'EPUB/text/ch{i:03}.xhtml' for i in range(index, index + len(headings))]
        index += len(headings)
    return sections
