#!/usr/bin/env python3
"""Verify the exact #334 source range snapshot; does not replay its mathematics."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import subprocess
import zipfile

PACKET = Path('02_REGISTRY/research/sources/d0_334_post_eeb_delta_2026-10-28')
BASE = 'eebcb5e467742df3e9cf7fa9702042d7294aa742'
HEAD = '726192353504a81a9ab2b751f9b6c7866271e75a'
MANIFEST_SHA256 = 'a48683d9079508fc0a4c3caa9d4194096ac506c1114ffb0428201d97208146ef'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_regular(root: Path, relative: Path) -> bytes:
    current = root
    for part in relative.parts[:-1]:
        require(part not in ('', '.', '..') and '\\' not in part,
                f'Unsafe path component: {part}')
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f'Expected directory: {current}')
    target = current / relative.parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode), f'Expected regular file: {target}')
    return target.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    header = b'blob ' + str(len(data)).encode('ascii') + b'\0'
    return hashlib.sha1(header + data).hexdigest()


def verify(root: Path, verify_source_objects: bool = False) -> dict[str, object]:
    manifest_bytes = read_regular(root, PACKET / 'MANIFEST.json')
    require(hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST_SHA256,
            'Manifest SHA-256 mismatch')
    manifest = json.loads(manifest_bytes)
    require(manifest['schema'] == 'd0-pr-source-range-intake-v2' and
            manifest['repository'] == 'gvakhrushev/d0_15' and
            manifest['owner_pr'] == 334, 'Unexpected source identity')
    require(manifest['source_range']['base_commit'] == BASE and
            manifest['source_range']['head_commit'] == HEAD,
            'Unexpected source range')
    rows = manifest['source_files']
    paths = [row['archive_path'] for row in rows]
    require(len(rows) == 70 and len(paths) == len(set(paths)) and paths == sorted(paths),
            'Changed-source path inventory mismatch')

    archive_meta = manifest['source_archive']
    archive = read_regular(root, PACKET / archive_meta['path'])
    require(len(archive) == archive_meta['bytes'] and
            hashlib.sha256(archive).hexdigest() == archive_meta['sha256'] and
            archive_meta['member_count'] == len(rows), 'Source archive mismatch')
    archive_names = [row['archive_path'] for row in rows]
    require(len(archive_names) == len(set(archive_names)) and
            archive_names == sorted(archive_names), 'Archive path inventory mismatch')
    for name in archive_names:
        require(not name.startswith('/') and '\\' not in name and
                all(part not in ('', '.', '..') for part in name.split('/')),
                f'Unsafe archive path: {name}')
    with zipfile.ZipFile(io.BytesIO(archive), 'r') as zf:
        infos = zf.infolist()
        require([info.filename for info in infos] == archive_names,
                'Archive member list differs from manifest')
        for row, info in zip(rows, infos):
            mode = (info.external_attr >> 16) & 0o177777
            data = zf.read(info)
            require(not info.is_dir() and mode == int(row['mode'], 8) and
                    len(data) == row['bytes'] and
                    hashlib.sha256(data).hexdigest() == row['sha256'] and
                    git_blob_sha1(data) == row['git_blob_sha1'],
                    f'Source snapshot mismatch: {row["archive_path"]}')

    patch_meta = manifest['source_patch']
    patch_storage = read_regular(root, PACKET / patch_meta['path'])
    require(len(patch_storage) == patch_meta['storage_bytes'] and
            hashlib.sha256(patch_storage).hexdigest() == patch_meta['storage_sha256'],
            'Compressed source patch mismatch')
    patch = gzip.decompress(patch_storage)
    require(len(patch) == patch_meta['bytes'] and
            hashlib.sha256(patch).hexdigest() == patch_meta['sha256'],
            'Source patch mismatch')
    commits = read_regular(root, PACKET / 'COMMITS.tsv')
    require(hashlib.sha256(commits).hexdigest() == manifest['commit_list']['sha256'] and
            len(manifest['source_commits']) == 34,
            'Commit range metadata mismatch')

    if verify_source_objects:
        def git(*args: str) -> bytes:
            return subprocess.check_output(['git', *args], cwd=root)
        require(git('rev-parse', BASE).decode().strip() == BASE and
                git('rev-parse', HEAD).decode().strip() == HEAD,
                'Pinned source commits are unavailable')
        expected_patch = git('diff', '--binary', '--full-index', BASE, HEAD)
        require(expected_patch == patch, 'Patch differs from pinned source commits')
        with zipfile.ZipFile(io.BytesIO(archive), 'r') as zf:
            for row in rows:
                upstream = git('show', f'{HEAD}:{row["archive_path"]}')
                snapshot = zf.read(row['archive_path'])
                require(upstream == snapshot,
                        f'Git tree bytes differ: {row["archive_path"]}')
        require(len(git('rev-list', '--reverse', f'{BASE}..{HEAD}').splitlines()) == 34,
                'Commit count differs from pinned source range')

    summary = manifest['change_summary']
    require(summary['changed_paths'] == 70 and summary['added_lines'] == 15782 and
            summary['deleted_lines'] == 0, 'Source diff summary mismatch')
    return {
        'status': 'PASS_SOURCE_BYTES_ONLY',
        'owner_pr': 334,
        'source_range': f'{BASE}..{HEAD}',
        'changed_paths': len(rows),
        'source_snapshot_bytes': summary['snapshot_bytes'],
        'source_archive_sha256': archive_meta['sha256'],
        'source_patch_sha256': patch_meta['sha256'],
        'source_object_check': verify_source_objects,
        'owner_checkers_replayed_by_this_verifier': False,
        'physical_admission': False,
        'scientific_acceptance': False,
        'GR_closed': False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    root = next((parent for parent in Path(__file__).resolve().parents
                 if (parent / '00_WORK' / 'manifest.json').is_file()), None)
    require(root is not None, 'Cannot locate repository root')
    print(json.dumps(verify(root, args.verify_source_objects), indent=2,
                     ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
