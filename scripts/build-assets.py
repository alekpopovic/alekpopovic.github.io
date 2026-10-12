#!/usr/bin/env python3
"""Build deterministic social cards, icons and responsive covers without a network."""
import json
import math
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parents[1]
venv = ROOT / '.venv'
if (venv / 'bin/python').exists() and Path(sys.prefix).resolve() != venv.resolve():
    os.execv(str(venv / 'bin/python'), [str(venv / 'bin/python'), __file__])

import yaml
from PIL import Image, ImageDraw, ImageFont
from fontTools import subset
from fontTools.varLib.instancer import instantiateVariableFont
import shutil

# Keep the complete local font as a language fallback; the English interface
# preloads a smaller deterministic subset from the same licensed source.
font_options = subset.Options()
font_options.flavor = 'woff2'
font_options.recalc_timestamp = False
font = subset.load_font(str(ROOT / 'assets/fonts/dm-sans.ttf'), font_options)
subsetter = subset.Subsetter(options=font_options)
subsetter.populate(unicodes=list(range(0x100)) + list(range(0x2000, 0x2800)) + [0x131, 0x152, 0x153, 0x2BB, 0x2BC, 0x2C6, 0x2DA, 0x2DC, 0x304, 0x308, 0x329, 0xFEFF, 0xFFFD])
subsetter.subset(font)
if 'fvar' in font and any(axis.axisTag == 'opsz' for axis in font['fvar'].axes):
    font = instantiateVariableFont(font, {'opsz': 14}, inplace=True)
subset.save_font(font, str(ROOT / 'assets/fonts/dm-sans-latin.woff2'), font_options)
vendor = ROOT / 'assets/vendor'
vendor.mkdir(exist_ok=True)
shutil.copyfile(ROOT / 'node_modules/web-vitals/dist/web-vitals.js', vendor / 'web-vitals.js')
shutil.copyfile(ROOT / 'node_modules/web-vitals/LICENSE', vendor / 'web-vitals-LICENSE.txt')


def save_image(image, destination, image_format, **options):
    """Publish complete images so Jekyll's watcher cannot copy a partial encode."""
    temporary = None
    try:
        # Hidden temporary files are ignored by Jekyll; rename stays on one filesystem.
        with NamedTemporaryFile(dir=destination.parent, prefix=f'.{destination.name}.', suffix='.tmp', delete=False) as output:
            temporary = Path(output.name)
            image.save(output, format=image_format, **options)
        temporary.chmod(0o644)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def flower(draw, x, y, radius, color):
    points = []
    for n in range(240):
        angle = n * math.tau / 240
        r = radius * (0.84 + 0.16 * math.cos(8 * angle))
        points.append((x + math.cos(angle) * r, y + math.sin(angle) * r))
    draw.polygon(points, fill=color)
    draw.ellipse((x-radius*.3, y-radius*.3, x+radius*.3, y+radius*.3), fill='#ffd33d')


def card(name, title, label, purple=False, ai=False):
    image = Image.new('RGB', (1200, 630), '#0b0d14' if ai else '#fff3b8')
    draw = ImageDraw.Draw(image)
    color = '#c4b5fd' if ai else ('#5941d9' if purple else '#2153d8')
    font_path = str(ROOT / ('assets/fonts/dm-sans.ttf' if ai else 'assets/fonts/passion-one-bold.ttf'))
    regular = ImageFont.truetype(str(ROOT / 'assets/fonts/dm-sans.ttf'), 23)
    draw.rounded_rectangle((55, 48, 1145, 105), 28, fill=color)
    draw.text((80, 62), label.upper(), font=regular, fill='#171126' if ai else 'white')
    for size in range(92, 47, -2):
        display = ImageFont.truetype(font_path, size)
        lines, line = [], ''
        for word in (title if ai else title.upper()).split():
            candidate = f'{line} {word}'.strip()
            if draw.textlength(candidate, font=display) > 900 and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
        if len(lines) * size * 1.05 <= 330:
            break
    draw.multiline_text((55, 148), '\n'.join(lines), font=display, fill=color, spacing=4)
    flower(draw, 1067, 425, 88, '#8d75bf' if ai else '#fd4401')
    draw.line((55, 535, 1145, 535), fill=color, width=2)
    draw.text((55, 559), 'Aleksandar Popovic', font=regular, fill='#d9d5e7' if ai else '#20201e')
    hostname = urlsplit(yaml.safe_load((ROOT / '_config.yml').read_text())['url']).netloc
    draw.text((785, 559), hostname, font=regular, fill='#d9d5e7' if ai else '#20201e')
    save_image(image, ROOT / f'assets/social/{name}.png', 'PNG', optimize=True)


def main():
    (ROOT / 'assets/social').mkdir(parents=True, exist_ok=True)
    card('site', 'Small ideas. Better systems.', 'Engineering · Books · Open source')
    card('codepop', 'CodePop. From idea to production.', 'My company · Product engineering · Cloud')
    card('ai', 'Less friction. More possibility.', 'AI Lab · Commands · Tools · Workflows', ai=True)
    books = json.loads((ROOT / '_data/books.json').read_text())
    for book in books:
        card(f'book-{book["id"]}', f'{book["title"]}: {book["subtitle"]}', f'The complete engineering book · {book["language_label"]}', book['id'] == 'logbranik')
        if book.get('cover_image'):
            cover = Image.open(ROOT / book['cover_image'].lstrip('/')).convert('RGB')
            for width in [320, 640, 960]:
                small = cover.copy()
                small.thumbnail((width, round(width * cover.height / cover.width)), Image.Resampling.LANCZOS)
                save_image(small, ROOT / f'assets/books/{book["id"]}/cover-{width}.webp', 'WEBP', quality=86, method=6)
    for path in sorted((ROOT / '_posts').glob('*.md')):
        metadata = yaml.safe_load(path.read_text().split('---', 2)[1])
        slug = metadata.get('slug') or path.stem[11:]
        ai = metadata.get('section') == 'ai'
        card(f'post-{slug}', metadata['title'], f'{"AI Lab" if ai else "Field notes"} · {metadata["category"]}', metadata.get('book_id') == 'logbranik', ai=ai)
    for project in json.loads((ROOT / '_data/projects.json').read_text()):
        card(f'project-{project["id"]}', project['name'], project['category'])
    for name, size in [('favicon-32', 32), ('apple-touch-icon', 180), ('icon-192', 192), ('icon-512', 512)]:
        icon = Image.new('RGB', (size * 3, size * 3), '#ffd33d')
        flower(ImageDraw.Draw(icon), size * 1.5, size * 1.5, size * 1.25, '#5941d9')
        save_image(icon.resize((size, size), Image.Resampling.LANCZOS), ROOT / f'assets/brand/{name}.png', 'PNG')
    print('Built social cards, icons, and responsive WebP covers.')


if __name__ == '__main__':
    main()
