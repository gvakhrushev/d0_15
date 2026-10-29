#!/usr/bin/env python3
"""Read-only verification of the pinned chat-intake member files.

This verifies actual member bytes against the pinned upstream inventory. It
never imports or executes member code, reconstructs ZIP files, or verifies the
original ZIP archive byte hashes.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import sys

SOURCE_COMMIT = 'eebcb5e467742df3e9cf7fa9702042d7294aa742'
UPSTREAM_HASHES = {
    'MANIFEST.json': '53fb4d806c2cb2dbe4b044a55c8bcd0301b6967ff0e402fab2626d8bc6969c01',
    'FILES.md': 'e38079064b59a845016c620e7a39c27eb605d1982d64fefd9b1b2143483cdb51',
    'VERIFICATION.json': '3a098993270bad49a2eb5c438ff2ab9c599ba7c9e7404dd9cb17aacda1e58eba',
}
HEADER = re.compile(r'## ([A-Za-z0-9_.-]+)\.zip')
ROW = re.compile(r'\| `([^`]+)` \| ([0-9]+) \| `([0-9a-f]{64})` \|')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_relative(value: str) -> PurePosixPath:
    require(bool(value) and '\\' not in value and '\x00' not in value,
            f'Unsafe member name: {value!r}')
    require(not PureWindowsPath(value).drive, f'Windows drive path is unsafe: {value!r}')
    parts = value.split('/')
    require(all(part not in ('', '.', '..') for part in parts),
            f'Unsafe member path: {value!r}')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value,
            f'Noncanonical member path: {value!r}')
    return path


def require_real_dir(path: Path) -> None:
    st = path.lstat()
    require(stat.S_ISDIR(st.st_mode), f'Expected real directory, not a link: {path}')


def read_regular(path: Path) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f'Expected regular file, not a link: {path}')
    return path.read_bytes()


def inventory(files_text: str) -> tuple[dict[str, tuple[int, str]], dict[str, int]]:
    expected: dict[str, tuple[int, str]] = {}
    counts: dict[str, int] = {}
    package: str | None = None
    for line in files_text.splitlines():
        if line.startswith('## '):
            match = HEADER.fullmatch(line)
            require(match is not None, f'Unexpected inventory heading: {line!r}')
            package = safe_relative(match.group(1)).as_posix()
            require('/' not in package and package not in counts, f'Duplicate package: {package}')
            counts[package] = 0
        elif line.startswith('| `'):
            match = ROW.fullmatch(line)
            require(match is not None and package is not None, f'Malformed inventory row: {line!r}')
            member = safe_relative(match.group(1))
            key = f'{package}/{member.as_posix()}'
            require(key not in expected, f'Duplicate member: {key}')
            expected[key] = (int(match.group(2)), match.group(3))
            counts[package] += 1
    require(expected and counts, 'Empty inventory')
    return expected, counts


def verify(root: Path) -> dict[str, object]:
    root = Path(root)
    require_real_dir(root)
    upstream = root / 'upstream'
    packages = root / 'packages'
    require_real_dir(upstream)
    require_real_dir(packages)
    require({p.name for p in upstream.iterdir()} == set(UPSTREAM_HASHES),
            'Unexpected upstream metadata path set')
    pinned: dict[str, bytes] = {}
    for name, digest in UPSTREAM_HASHES.items():
        data = read_regular(upstream / name)
        require(hashlib.sha256(data).hexdigest() == digest, f'Upstream digest mismatch: {name}')
        pinned[name] = data
    manifest = json.loads(pinned['MANIFEST.json'].decode('utf-8'))
    historical = json.loads(pinned['VERIFICATION.json'].decode('utf-8'))
    expected, counts = inventory(pinned['FILES.md'].decode('utf-8'))
    require(manifest['file_count'] == len(expected) == historical['files'] == 74,
            'Inventory member count mismatch')
    require(manifest['file_bytes'] == sum(size for size, _ in expected.values()) ==
            historical['bytes'] == 650121, 'Inventory byte total mismatch')
    advertised: dict[str, int] = {}
    for entry in manifest['packages']:
        name = entry['archive']
        require(isinstance(name, str) and name.endswith('.zip'), 'Bad archive name')
        stem = safe_relative(name[:-4]).as_posix()
        require('/' not in stem and stem not in advertised, f'Duplicate archive: {name}')
        advertised[stem] = entry['member_count']
    require(advertised == counts, 'Manifest package/member counts differ from inventory')

    actual: dict[str, Path] = {}
    directories: set[str] = set()
    def fail_walk(error: OSError) -> None:
        raise error
    for current, dirs, names in os.walk(packages, followlinks=False, onerror=fail_walk):
        parent = Path(current)
        for name in dirs:
            p = parent / name
            require_real_dir(p)
            directories.add(p.relative_to(packages).as_posix())
        for name in names:
            p = parent / name
            key = p.relative_to(packages).as_posix()
            safe_relative(key)
            require(key not in actual, f'Duplicate actual member: {key}')
            # lstat rejects symlinks and non-regular files without following them.
            st = p.lstat()
            require(stat.S_ISREG(st.st_mode), f'Unexpected non-regular member: {key}')
            actual[key] = p
    require(set(actual) == set(expected),
            f'Member path set mismatch; missing={sorted(set(expected)-set(actual))}, '
            f'extra={sorted(set(actual)-set(expected))}')
    expected_dirs = set()
    for key in expected:
        parts = safe_relative(key).parts
        expected_dirs.update('/'.join(parts[:i]) for i in range(1, len(parts)))
    require(directories == expected_dirs,
            f'Directory path set mismatch; missing={sorted(expected_dirs-directories)}, '
            f'extra={sorted(directories-expected_dirs)}')
    total = 0
    for key, (size, digest) in expected.items():
        data = read_regular(actual[key])
        require(len(data) == size, f'Member size mismatch: {key}')
        require(hashlib.sha256(data).hexdigest() == digest, f'Member digest mismatch: {key}')
        data.decode('utf-8', errors='strict')
        total += len(data)
    require(total == 650121, 'Actual member byte total mismatch')
    return {'status': 'PASS_MEMBER_BYTES_ONLY', 'source_commit': SOURCE_COMMIT,
            'member_files': len(actual), 'member_bytes': total,
            'packages': len(counts), 'upstream_metadata_sha256': UPSTREAM_HASHES,
            'zip_archive_bytes_and_sha256': 'NOT_VERIFIED',
            'archived_code_executed': False, 'scientific_acceptance': False}


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError('Usage: verify_intake.py [intake-directory]')
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent
        print(json.dumps(verify(root), sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'FAIL_INTAKE: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
