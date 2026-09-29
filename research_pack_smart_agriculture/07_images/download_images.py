#!/usr/bin/env python3
"""Download the verified image URLs; preserve originals and update the CSV.
Run locally: python download_images.py [--timeout 30]
Network access is required. Copyright permissions are not granted by this script.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MAX_BYTES = 15 * 1024 * 1024

def image_signature(data: bytes) -> bool:
    return (data.startswith(b'\xff\xd8\xff') or
            data.startswith(b'\x89PNG\r\n\x1a\n') or
            (data[:4] == b'RIFF' and data[8:12] == b'WEBP'))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout', type=float, default=30.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    base = Path(__file__).resolve().parent
    manifest = base / 'image_credits.csv'
    try:
        with manifest.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            fields = list(reader.fieldnames or [])
            rows = list(reader)
        required = {'filename', 'direct_url', 'downloaded', 'file_size_bytes'}
        if not required.issubset(fields):
            raise ValueError('Manifest is missing required columns')
    except (OSError, ValueError, csv.Error) as exc:
        print(f'Cannot read manifest: {exc}', file=sys.stderr)
        return 2
    failures = 0
    for row in rows:
        filename = row['filename']
        url = row['direct_url']
        target = base / filename
        if (Path(filename).name != filename or
                urllib.parse.urlparse(url).scheme != 'https'):
            print(f'REJECT unsafe filename or URL: {filename}', file=sys.stderr)
            failures += 1
            continue
        try:
            if target.exists():
                payload = target.read_bytes()
                if not image_signature(payload):
                    raise ValueError('Existing file is not a supported image; remove it manually')
                print(f'KEEP {filename}')
            else:
                request = urllib.request.Request(url, headers={'User-Agent': 'ResearchAssetDownloader/1.0'})
                with urllib.request.urlopen(request, timeout=args.timeout) as response:
                    payload = response.read(MAX_BYTES + 1)
                if len(payload) > MAX_BYTES:
                    raise ValueError('Image exceeds the 15 MB safety limit')
                if not image_signature(payload):
                    raise ValueError('Response is not a JPEG, PNG, or WebP image')
                temporary = target.with_suffix(target.suffix + '.part')
                temporary.write_bytes(payload)
                temporary.replace(target)
                print(f'OK   {filename}  {len(payload)} bytes')
            row['downloaded'] = 'yes'
            row['file_size_bytes'] = str(len(payload))
            if len(payload) > 1_500_000:
                print(f'NOTE {filename}: over 1.5 MB; review size without violating its license')
        except (OSError, ValueError, urllib.error.URLError) as exc:
            row['downloaded'] = 'no'
            row['file_size_bytes'] = ''
            failures += 1
            print(f'FAIL {filename}: {exc}', file=sys.stderr)
    temporary_manifest = manifest.with_suffix('.csv.part')
    with temporary_manifest.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary_manifest.replace(manifest)
    print(f'Finished: {len(rows)-failures} ready, {failures} failed. Review image_credits.csv.')
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
