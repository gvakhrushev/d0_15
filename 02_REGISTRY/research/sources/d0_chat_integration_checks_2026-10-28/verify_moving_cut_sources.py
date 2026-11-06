#!/usr/bin/env python3
"""Verify six literal moving-cut source files, without requiring Git.

SHA-256 and Git blob IDs below are pinned to the published PR #334 commit.
This validates working-tree bytes, not the presence of the upstream Git object
or scientific correctness; no checked source code is imported or executed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import sys

SOURCE_COMMIT = 'eebcb5e467742df3e9cf7fa9702042d7294aa742'
EXPECTED = {
    '02_REGISTRY/research/A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md':
        ('88522b7ef53104d9798aa2337ccb11f2ef2cb878f851b9a53f97d1e9e58efb87',
         'a2e0d3ed877985c98b5fe7f1ef29bbe95d9422f4'),
    '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/MANIFEST.json':
        ('63d3817249bc9f470d18e97be2bcd2f911aca993f8f354f62fe2f912fda979cc',
         '5b6846eacad58a99b3c0ffdb560389d06de98bc5'),
    '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/PROOF_RU.md':
        ('fd2210be3ff120390be9359d877b957b845de27705d7c896fd1f44e5795677a0',
         'eeff19caa071dae92961f5aa8f0ff16087ca2de1'),
    '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/check_root_moving_cut.py':
        ('da4df4d9c075b9b6cc01a4c74503ea1bb379d062bdbb74e5ddb02703f2f85d2c',
         '4ae220f71339dc82ddffc0771f4bd91e5f19646c'),
    '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/result.json':
        ('b361bcba014c0a68f545a0167ae1a4be20ccc1386fe754bd389c472bd361dc8b',
         '39cedbaf8d6891bd1711ce1f13f49af37ce2b3d3'),
    '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/result_optimized.json':
        ('b361bcba014c0a68f545a0167ae1a4be20ccc1386fe754bd389c472bd361dc8b',
         '39cedbaf8d6891bd1711ce1f13f49af37ce2b3d3'),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_pinned_file(root: Path, relative: str) -> bytes:
    """Reject symbolic links at the root, each child directory and file."""
    require(stat.S_ISDIR(root.lstat().st_mode), f'Expected real repository directory: {root}')
    parts = relative.split('/')
    require(parts and all(part not in ('', '.', '..') and '\\' not in part for part in parts),
            f'Unsafe source path: {relative}')
    current = root
    for part in parts[:-1]:
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f'Expected real directory: {current}')
    file = current / parts[-1]
    require(stat.S_ISREG(file.lstat().st_mode), f'Expected regular file: {file}')
    return file.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def verify(root: Path) -> dict[str, object]:
    files = []
    for path, (expected_sha256, expected_blob) in EXPECTED.items():
        data = read_pinned_file(Path(root), path)
        sha256 = hashlib.sha256(data).hexdigest()
        blob = git_blob_sha1(data)
        require(sha256 == expected_sha256, f'SHA-256 mismatch: {path}')
        require(blob == expected_blob, f'Git blob ID mismatch: {path}')
        files.append({'path': path, 'bytes': len(data), 'sha256': sha256, 'git_blob': blob})
    return {'status': 'PASS_PINNED_MOVING_CUT_BYTES', 'source_commit': SOURCE_COMMIT,
            'files': files, 'file_count': len(files),
            'actual_git_object_store_checked': False, 'source_code_executed': False,
            'scientific_acceptance': False}


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError('Usage: verify_moving_cut_sources.py [repository-root]')
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[4]
        print(json.dumps(verify(root), sort_keys=True, indent=2))
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(f'FAIL_MOVING_CUT_SOURCE: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
