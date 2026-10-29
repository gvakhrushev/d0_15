#!/usr/bin/env python3
"""Verify the exact #334 post-523 source packet and the embedded AF replay."""
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

PACKET = Path(__file__).resolve().parent
BASE = '523d2cbcc0a9771ea40faa4a2eac84cc78704b0e'
HEAD = '15742b846f380b75e7d8f869faf7bc51623ed2a6'
PRIMARY = (
    '02_REGISTRY/research/'
    'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
)
CHECKER_BEGIN = '<!-- BEGIN 7dg GOLDEN AF FRAME CHECKER -->'
CHECKER_END = '<!-- END 7dg GOLDEN AF FRAME CHECKER -->'
RECEIPT_BEGIN = '<!-- BEGIN 7dg GOLDEN AF FRAME RECEIPT -->'
RECEIPT_END = '<!-- END 7dg GOLDEN AF FRAME RECEIPT -->'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_regular(relative: str) -> bytes:
    path = PACKET / relative
    require(not path.is_symlink() and path.is_file(),
            f'Expected regular file: {relative}')
    return path.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') +
                        b'\0' + data).hexdigest()


def verify(verify_source_objects: bool = False) -> dict[str, object]:
    manifest_bytes = read_regular('MANIFEST.json')
    recorded_manifest_sha = read_regular('MANIFEST.sha256').decode(
        'ascii').split()[0]
    require(recorded_manifest_sha == sha256(manifest_bytes),
            'Manifest SHA-256 mismatch')
    manifest = json.loads(manifest_bytes)
    require(manifest['schema'] == 'd0-pr-source-range-intake-v1' and
            manifest['repository'] == 'gvakhrushev/d0_15' and
            manifest['owner_pr'] == 334,
            'Unexpected source identity')
    source_range = manifest['source_range']
    require(source_range == {
        'base_commit': BASE,
        'head_commit': HEAD,
        'commits': 1,
    }, 'Unexpected source range')

    expected_artifacts = {row['path'] for row in manifest['artifacts']}
    actual_artifacts = {
        path.relative_to(PACKET).as_posix()
        for path in PACKET.rglob('*')
        if path.is_file() and path.name not in ('MANIFEST.json', 'MANIFEST.sha256')
    }
    require(expected_artifacts == actual_artifacts,
            'Artifact inventory differs from packet contents')
    for row in manifest['artifacts']:
        data = read_regular(row['path'])
        require(len(data) == row['bytes'] and sha256(data) == row['sha256'],
                f'Artifact digest mismatch: {row["path"]}')

    source_rows = manifest['source_files']
    source_paths = [row['archive_path'] for row in source_rows]
    require(len(source_rows) == 2 and source_paths == sorted(source_paths) and
            len(source_paths) == len(set(source_paths)),
            'Changed-source inventory mismatch')
    input_rows = manifest['source_inputs']
    require(len(input_rows) == 2 and
            all(row['commit'] == HEAD for row in input_rows),
            'Pinned checker input metadata mismatch')

    archive_meta = manifest['source_archive']
    archive = read_regular(archive_meta['path'])
    require(len(archive) == archive_meta['bytes'] and
            sha256(archive) == archive_meta['sha256'],
            'Source archive digest mismatch')
    archive_rows = {
        row['archive_path']: row for row in source_rows + input_rows
    }
    archive_names = sorted(archive_rows)
    with zipfile.ZipFile(io.BytesIO(archive), 'r') as zf:
        infos = [info for info in zf.infolist() if not info.is_dir()]
        require([info.filename for info in infos] == archive_names and
                len(infos) == archive_meta['member_count'],
                'Archive members differ from manifest')
        snapshots: dict[str, bytes] = {}
        for name, info in zip(archive_names, infos):
            row = archive_rows[name]
            data = zf.read(info)
            require(len(data) == row['bytes'] and sha256(data) == row['sha256'],
                    f'Archive member mismatch: {name}')
            if 'head_git_blob_sha1' in row:
                require(git_blob_sha1(data) == row['head_git_blob_sha1'],
                        f'Git blob mismatch: {name}')
            snapshots[name] = data
    for row in input_rows:
        replay_path = f'replay/repo/{row["repository_path"]}'
        require(read_regular(replay_path) == snapshots[row['archive_path']],
                f'Replay dependency differs from pinned archive: {replay_path}')

    primary = snapshots[PRIMARY].decode('utf-8')
    code_block = primary.split(CHECKER_BEGIN, 1)[1].split(CHECKER_END, 1)[0]
    embedded_checker = (code_block.split('```python\n', 1)[1]
                        .split('\n```', 1)[0] + '\n').encode('utf-8')
    receipt_block = primary.split(RECEIPT_BEGIN, 1)[1].split(RECEIPT_END, 1)[0]
    embedded_receipt = (receipt_block.split('```json\n', 1)[1]
                        .split('\n```', 1)[0] + '\n').encode('utf-8')
    require(read_regular('checker/check_7dg.py') == embedded_checker and
            read_regular('replay/check_7dg.py') == embedded_checker,
            'Extracted checker differs from primary artifact')
    require(read_regular('checker/owner_receipt.json') == embedded_receipt and
            read_regular('replay/owner_receipt.json') == embedded_receipt,
            'Extracted owner receipt differs from primary artifact')
    owner_receipt = json.loads(embedded_receipt)
    require(sha256(embedded_checker) == owner_receipt['checker_sha256'] and
            sha256(embedded_receipt) ==
            manifest['replay']['owner_receipt_sha256'],
            'Checker or owner receipt pin mismatch')

    patch_meta = manifest['source_patch']
    compressed_patch = read_regular(patch_meta['path'])
    require(len(compressed_patch) == patch_meta['storage_bytes'] and
            sha256(compressed_patch) == patch_meta['storage_sha256'],
            'Compressed patch digest mismatch')
    patch = gzip.decompress(compressed_patch)
    require(len(patch) == patch_meta['bytes'] and
            sha256(patch) == patch_meta['sha256'], 'Patch digest mismatch')
    commits = read_regular('COMMITS.tsv')
    require(sha256(commits) == manifest['commit_list']['sha256'] and
            len(commits.decode('utf-8').splitlines()) == 1,
            'Ordered commit list mismatch')

    replay_meta = manifest['replay']
    normal = read_regular(replay_meta['normal_output'])
    optimized = read_regular(replay_meta['optimized_output'])
    require(normal == optimized == embedded_receipt,
            'Local normal/optimized replay differs from owner receipt bytes')
    result = json.loads(normal)
    require(result['status'] == 'PASS' and result['checks'] == 101 and
            result['checker_sha256'] == owner_receipt['checker_sha256'] and
            result['frame_owner_sha256'] == owner_receipt['frame_owner_sha256'] and
            result['native_owner_sha256'] == owner_receipt['native_owner_sha256'],
            'Replay receipt fields differ')
    require(read_regular(replay_meta['normal_stderr']) == b'' and
            read_regular(replay_meta['optimized_stderr']) == b'',
            'Replay stderr is not empty')
    for key in ('physical_AF_port_addressability_proved',
                'physical_AF_growth_cost_supplied',
                'wire_execution_domain_membership_claimed', 'GR_closed'):
        require(result[key] is False, f'Scientific boundary changed: {key}')

    source_object_check = False
    if verify_source_objects:
        def git(*args: str) -> bytes:
            return subprocess.check_output(['git', *args], cwd=PACKET)

        require(git('rev-parse', BASE).decode().strip() == BASE and
                git('rev-parse', HEAD).decode().strip() == HEAD,
                'Pinned source commits are unavailable')
        require(git('diff', '--binary', '--full-index', BASE, HEAD) == patch,
                'Patch differs from pinned source commits')
        for row in source_rows:
            require(git('show', f'{HEAD}:{row["archive_path"]}') ==
                    snapshots[row['archive_path']],
                    f'Git tree bytes differ: {row["archive_path"]}')
        for row in input_rows:
            require(git('show', f'{HEAD}:{row["repository_path"]}') ==
                    snapshots[row['archive_path']],
                    f'Pinned checker input differs: {row["repository_path"]}')
        require(len(git('rev-list', '--reverse', f'{BASE}..{HEAD}').splitlines()) == 1,
                'Commit count differs from pinned range')
        source_object_check = True

    return {
        'status': 'PASS_SOURCE_AND_REPLAY_BYTES',
        'owner_pr': 334,
        'source_range': f'{BASE}..{HEAD}',
        'changed_paths': len(source_rows),
        'commits': 1,
        'source_archive_sha256': archive_meta['sha256'],
        'source_patch_sha256': patch_meta['sha256'],
        'checker_sha256': result['checker_sha256'],
        'replay_status': result['status'],
        'replay_checks': result['checks'],
        'normal_optimized_owner_bytes_identical': True,
        'physical_AF_port_addressability_proved': False,
        'physical_AF_growth_cost_supplied': False,
        'GR_closed': False,
        'source_object_check': source_object_check,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.verify_source_objects), indent=2,
                     ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
