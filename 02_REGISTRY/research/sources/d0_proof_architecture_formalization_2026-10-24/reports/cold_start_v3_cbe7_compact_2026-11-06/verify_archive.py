#!/usr/bin/env python3
"""Verify a split gzip stream and optionally restore a new full JSON file."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zlib

P = Path(__file__).resolve().parent

def need(ok, why):
    if not ok:
        raise ValueError(why)

def verify_archive(root, manifest, target=None):
    all_gz = hashlib.sha256()
    all_raw = hashlib.sha256()
    gz_n = raw_n = 0
    z = zlib.decompressobj(wbits=31)
    parts = manifest['parts']
    need(parts and all(item['name'] == f'part-{i:03d}.gzchunk' for i, item in enumerate(parts)), 'part order')
    for item in parts:
        p = root / 'parts' / item['name']
        need(p.is_file() and not p.is_symlink() and p.stat().st_size == item['bytes'] and 0 < item['bytes'] <= manifest['part_max_bytes'], 'part metadata: ' + item['name'])
        part_h = hashlib.sha256()
        with p.open('rb') as inp:
            for chunk in iter(lambda: inp.read(1024*1024), b''):
                gz_n += len(chunk)
                all_gz.update(chunk)
                part_h.update(chunk)
                data = chunk
                while data:
                    output = z.decompress(data, 1024*1024)
                    data = z.unconsumed_tail
                    need(not z.unused_data, 'trailing data after gzip member')
                    all_raw.update(output)
                    raw_n += len(output)
                    if target is not None:
                        target.write(output)
        need(part_h.hexdigest() == item['sha256'], 'part digest: ' + item['name'])
    tail = z.flush()
    all_raw.update(tail)
    raw_n += len(tail)
    if target is not None:
        target.write(tail)
    need(z.eof and not z.unused_data, 'incomplete gzip stream')
    need(gz_n == manifest['gzip_bytes'] and all_gz.hexdigest() == manifest['gzip_sha256'], 'combined gzip')
    need(raw_n == manifest['full_bytes'] and all_raw.hexdigest() == manifest['full_sha256'], 'full JSON')
    return raw_n

def main():
    ap = argparse.ArgumentParser()
    output = ap.add_mutually_exclusive_group()
    output.add_argument('--extract', type=Path, help='exclusive new destination for full JSON')
    output.add_argument('--stdout', action='store_true', help='stream full JSON to stdout; status goes to stderr')
    args = ap.parse_args()
    root_manifest = json.loads((P / 'manifest.json').read_text())
    data = (P / 'archive.json').read_bytes()
    need(hashlib.sha256(data).hexdigest() == root_manifest['archive_manifest_sha256'], 'archive manifest digest')
    meta = json.loads(data)
    need(meta['schema'] == 'd0-v3-cbe7-split-gzip-v1' and meta['full_sha256'] == root_manifest['full_raw']['sha256'] and meta['full_bytes'] == root_manifest['full_raw']['bytes'], 'raw/summary binding')
    if args.extract:
        with args.extract.open('xb') as target:
            count = verify_archive(P, meta, target)
    elif args.stdout:
        count = verify_archive(P, meta, sys.stdout.buffer)
        sys.stdout.buffer.flush()
    else:
        count = verify_archive(P, meta)
    print(f'PASS: split gzip and restored JSON integrity, {count} bytes; no search replay', file=sys.stderr if args.stdout else sys.stdout)

if __name__ == '__main__':
    main()
