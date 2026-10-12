#!/usr/bin/env python3
"""Validate editorial review dates; optionally check official source links."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / '.venv/bin/python').exists() and Path(sys.prefix).resolve() != (ROOT / '.venv').resolve():
    os.execv(str(ROOT / '.venv/bin/python'), [str(ROOT / '.venv/bin/python'), __file__, *sys.argv[1:]])
import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--strict-age', action='store_true')
    parser.add_argument('--max-age', type=int, default=90)
    args = parser.parse_args()
    today = dt.date.today()
    reviews, urls, errors = [], set(), []
    for path in sorted((ROOT / '_posts').glob('*.md')):
        data = yaml.safe_load(path.read_text().split('---', 2)[1])
        if data.get('section') == 'ai':
            reviews.append((str(path.relative_to(ROOT)), str(data.get('verified_at', ''))))
            urls.update(source['url'] for source in data.get('sources', []))
    for project in json.loads((ROOT / '_data/projects.json').read_text()):
        reviews.append((project['id'], project.get('verified_at', '')))
        urls.update([project['verification_url'], project['documentation']])
        if len(project.get('source_commit', '')) != 40: errors.append(f'{project["id"]}: pin the source revision')
    report = ['# Editorial review', '', f'Checked {today}. Review interval: {args.max_age} days.', '']
    for name, value in reviews:
        try:
            date = dt.date.fromisoformat(value)
            if date > today: errors.append(f'{name}: verification date is in the future')
            age = (today - date).days
            report.append(f'- {name}: {date} ({age} days old)' + (' — review due' if age > args.max_age else ''))
            if args.strict_age and age > args.max_age: errors.append(f'{name}: editorial review is due')
        except ValueError: errors.append(f'{name}: invalid verification date')
    if args.links:
        report += ['', '## Source links', '']
        def check_link(url):
            try:
                result = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '15', '--max-redirs', '5', '--proto', '=https', '--proto-redir', '=https', '--user-agent', 'CodePop-Editorial-Check/1.0', '--output', os.devnull, '--write-out', '%{http_code}', url], capture_output=True, text=True, timeout=20)
                status = int(result.stdout) if result.returncode == 0 and result.stdout.isdigit() else 0
            except (OSError, subprocess.TimeoutExpired): status = 0
            print(f'Source {status or "manual review"}: {url}', flush=True)
            return url, status
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url, status in pool.map(check_link, sorted(urls)):
                report.append(f'- {status or "Unreachable"}: {url}' + (' — broken source' if status in (404, 410) else ' — manual verification needed' if status != 200 else ''))
                if status in (404, 410): errors.append(f'Broken editorial source: {url}')
    target = ROOT / 'reports/content-review.md'; target.parent.mkdir(exist_ok=True); target.write_text('\n'.join(report + ['', *errors]) + '\n')
    print(f'Editorial review: {len(reviews)} entries, {len(urls)} source URLs. Report: reports/content-review.md')
    for error in errors: print(error, file=sys.stderr)
    if errors: raise SystemExit(1)


if __name__ == '__main__': main()
