#!/usr/bin/env python3
"""Verify or extract preserved handoff inputs. Never execute the preserved research code."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath
import sys

HERE = Path(__file__).resolve().parent

def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def payload() -> dict[str, str]:
    meta = json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf8'))
    encoded = ''.join((HERE/f'payload.b64.{i:02}').read_text(encoding='ascii').strip()
                      for i in range(6))
    require(len(encoded) <= 4_000_000, 'Oversized encoded input')
    packed = base64.b64decode(encoded, validate=True)
    require(hashlib.sha256(packed).hexdigest() == meta['packed_sha256'], 'Packed checksum')
    raw = lzma.decompress(packed, memlimit=128*1024*1024)
    require(len(raw) <= 8_000_000, 'Oversized decoded input')
    require(hashlib.sha256(raw).hexdigest() == meta['json_sha256'], 'JSON checksum')
    files = json.loads(raw)
    require(isinstance(files, dict) and len(files) == meta['file_count'] == 21, 'Input count')
    require(set(files) == set(meta['files']), 'Manifest file set')
    for name, text in files.items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe input path')
        require(name.startswith('02_REGISTRY/research/'), 'Wrong input prefix')
        require(isinstance(text, str), 'Non-text input')
        require(hashlib.sha256(text.encode()).hexdigest() == meta['files'][name],
                'Input checksum: '+name)
    return files


def extract(root: Path) -> None:
    root = root.resolve()
    files = payload()
    # Preflight every path and conflict before writing any file.
    for name, text in files.items():
        target = (root/name).resolve()
        require(target.is_relative_to(root), 'Symlink escape')
        if target.exists():
            require(target.is_file() and target.read_bytes() == text.encode(),
                    'Existing differing file: '+name)
    for name, text in files.items():
        target = root/name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(text.encode())
    print(f'EXTRACTED {len(files)} immutable inputs to {root}; no research execution')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--extract', type=Path)
    args = parser.parse_args()
    try:
        if args.check:
            print(f'PASS_HANDOFF_INPUT_PRESERVATION {len(payload())} files; not scientific replay')
        else:
            extract(args.extract)
    except (OSError, ValueError, KeyError, lzma.LZMAError) as exc:
        print(f'INPUT_PRESERVATION_FAILED: {exc}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
