#!/usr/bin/env python3
"""Refresh the visible video index from the two public YouTube playlists."""
import json
import re
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / '_data' / 'video_playlists.json'


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def text(value):
    if isinstance(value, str):
        return value
    return value.get('simpleText') or value.get('content') or ''.join(run.get('text', '') for run in value.get('runs', []))


def extract(html):
    marker = re.search(r'var ytInitialData\s*=\s*', html)
    if not marker:
        raise ValueError('YouTube did not return playlist metadata')
    initial, _ = json.JSONDecoder().raw_decode(html[marker.end():])
    videos = []
    for node in walk(initial.get('contents', {})):
        if 'continuationItemRenderer' in node:
            raise ValueError('Playlist needs pagination; refusing to save an incomplete index')
        if 'playlistVideoRenderer' in node:
            video = node['playlistVideoRenderer']
            if video.get('isPlayable') is False:
                continue
            videos.append(dict(id=video['videoId'], title=text(video['title']), duration=text(video.get('lengthText', {}))))
        elif 'lockupViewModel' in node:
            video = node['lockupViewModel']
            video_id = video.get('contentId', '')
            if not re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id):
                continue
            title = text(video.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}))
            badges = [item['thumbnailBadgeViewModel'].get('text', '') for item in walk(video.get('contentImage', {})) if 'thumbnailBadgeViewModel' in item]
            duration = next((badge.replace('.', ':') for badge in badges if re.fullmatch(r'\d+(?:[:.]\d{2}){1,2}', badge)), '')
            videos.append(dict(id=video_id, title=title, duration=duration))
    if not videos or any(not video['title'] for video in videos):
        raise ValueError('YouTube returned an empty or unsupported playlist; existing index retained')
    return videos


def main():
    playlists = json.loads(DATA.read_text(encoding='utf-8'))
    for playlist in playlists:
        request = urllib.request.Request(
            f'https://www.youtube.com/playlist?list={playlist["id"]}&hl=en',
            headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'})
        with urllib.request.urlopen(request, timeout=25) as response:
            playlist['videos'] = extract(response.read().decode('utf-8'))
        print(f'{playlist["youtube_title"]}: {len(playlist["videos"])} videos')
    # Write only after every playlist succeeds, retaining the last good index on failure.
    DATA.write_text(json.dumps(playlists, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(f'Video sync failed: {error}') from error
