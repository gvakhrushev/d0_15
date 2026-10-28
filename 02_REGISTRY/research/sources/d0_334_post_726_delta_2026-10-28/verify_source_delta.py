#!/usr/bin/env python3
"""Verify the exact #334 post-726 source packet and pinned replay bytes."""
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

PACKET = Path('02_REGISTRY/research/sources/d0_334_post_726_delta_2026-10-28')
BASE = '726192353504a81a9ab2b751f9b6c7866271e75a'
HEAD = '8daed32d560df18837bcc69458a8fa538a9cf135'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_regular(root: Path, relative: Path) -> bytes:
    current = root
    for part in relative.parts[:-1]:
        require(part not in ('', '.', '..') and '\\' not in part,
                f'Unsafe path component: {part}')
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode),
                f'Expected directory: {current}')
    target = current / relative.parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode),
            f'Expected regular file: {target}')
    return target.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    header = b'blob ' + str(len(data)).encode('ascii') + b'\0'
    return hashlib.sha1(header + data).hexdigest()


def verify(root: Path, verify_source_objects: bool = False) -> dict[str, object]:
    manifest_bytes = read_regular(root, PACKET / 'MANIFEST.json')
    expected_manifest_sha = read_regular(root, PACKET / 'MANIFEST.sha256')
    require(expected_manifest_sha.decode().split()[0] ==
            hashlib.sha256(manifest_bytes).hexdigest(),
            'Manifest SHA-256 mismatch')
    manifest = json.loads(manifest_bytes)
    require(manifest['schema'] == 'd0-pr-source-range-intake-v1' and
            manifest['repository'] == 'gvakhrushev/d0_15' and
            manifest['owner_pr'] == 334, 'Unexpected source identity')
    require(manifest['source_range']['base_commit'] == BASE and
            manifest['source_range']['head_commit'] == HEAD and
            manifest['source_range']['commits'] == 7,
            'Unexpected source range')

    rows = manifest['source_files']
    paths = [row['archive_path'] for row in rows]
    require(len(rows) == 6 and paths == sorted(paths) and
            len(paths) == len(set(paths)), 'Changed-source path inventory mismatch')
    archive_meta = manifest['source_archive']
    archive = read_regular(root, PACKET / archive_meta['path'])
    require(len(archive) == archive_meta['bytes'] and
            hashlib.sha256(archive).hexdigest() == archive_meta['sha256'] and
            archive_meta['member_count'] == len(rows), 'Source archive mismatch')
    with zipfile.ZipFile(io.BytesIO(archive), 'r') as zf:
        infos = zf.infolist()
        file_infos = [info for info in infos if not info.is_dir()]
        require([info.filename for info in file_infos] == paths,
                'Archive member list differs from manifest')
        for row, info in zip(rows, file_infos):
            data = zf.read(info)
            require(len(data) == row['bytes'] and
                    hashlib.sha256(data).hexdigest() == row['sha256'] and
                    git_blob_sha1(data) == row['head_git_blob_sha1'],
                    f'Source snapshot mismatch: {row["archive_path"]}')
        snapshots = {info.filename: zf.read(info) for info in infos}

    patch_meta = manifest['source_patch']
    patch_storage = read_regular(root, PACKET / patch_meta['path'])
    require(len(patch_storage) == patch_meta['storage_bytes'] and
            hashlib.sha256(patch_storage).hexdigest() ==
            patch_meta['storage_sha256'], 'Compressed source patch mismatch')
    patch = gzip.decompress(patch_storage)
    require(len(patch) == patch_meta['bytes'] and
            hashlib.sha256(patch).hexdigest() == patch_meta['sha256'],
            'Source patch mismatch')
    commits = read_regular(root, PACKET / 'COMMITS.tsv')
    require(hashlib.sha256(commits).hexdigest() ==
            manifest['commit_list']['sha256'], 'Commit-list digest mismatch')
    commit_lines = commits.decode().splitlines()
    require(len(commit_lines) == 7 and
            [line.split('\t', 1)[0] for line in commit_lines] ==
            [row['sha'] for row in manifest['source_commits']],
            'Commit-list metadata mismatch')

    for row in manifest['replay_artifacts']:
        data = read_regular(root, PACKET / row['path'])
        require(len(data) == row['bytes'] and
                hashlib.sha256(data).hexdigest() == row['sha256'],
                f'Replay artifact mismatch: {row["path"]}')

    direct_normal = read_regular(root, PACKET / 'replay/direct_click_normal.json')
    direct_optimized = read_regular(root, PACKET / 'replay/direct_click_optimized.json')
    direct_owner = snapshots[
        '02_REGISTRY/research/sources/d0_mass_coordinate_equivalence_2026-10-28/result.json']
    require(direct_normal == direct_optimized == direct_owner,
            'Direct-click normal/optimized outputs differ from owner result')
    require(json.loads(direct_normal)['checks'] == 109,
            'Direct-click check count mismatch')

    retained = PACKET / 'replay/retained_past_7dd'
    retained_normal = read_regular(root, retained / 'normal.json')
    retained_optimized = read_regular(root, retained / 'optimized.json')
    retained_owner = read_regular(root, retained / 'owner.json')
    require(retained_normal == retained_optimized == retained_owner,
            'Retained-past receipts differ')
    require(len(json.loads(retained_normal)['checks']) == 22,
            'Retained-past check count mismatch')

    cauchy = PACKET / 'replay/dust_cauchy_7df'
    cauchy_normal = read_regular(root, cauchy / 'normal.json')
    cauchy_optimized = read_regular(root, cauchy / 'optimized.json')
    cauchy_owner = read_regular(root, cauchy / 'owner.json')
    require(cauchy_normal == cauchy_optimized == cauchy_owner,
            'Cauchy-transport receipts differ')
    require(json.loads(cauchy_normal)['checks'] == 28,
            'Cauchy-transport check count mismatch')

    scale = PACKET / 'replay/fixed_boundary_7de'
    low = read_regular(root, scale / 'nu_3_10.json')
    low_owner = read_regular(root, scale / 'owner_low.json')
    high = read_regular(root, scale / 'nu_3_5.json')
    high_owner = read_regular(root, scale / 'owner_high.json')
    require(low == low_owner and high == high_owner,
            'Fixed-boundary outputs differ from embedded owner receipts')
    low_claimed = '78c41acd7de771b15e2acfbffbf113024ee06d909200ae75b51760424ffa6416'
    low_actual = hashlib.sha256(low).hexdigest()
    require(low_actual != low_claimed and
            sum(a != b for a, b in zip(low_actual, low_claimed)) == 1,
            'Expected one-character low-receipt digest discrepancy changed')
    require(hashlib.sha256(high).hexdigest() ==
            '4b05b28a3edcdc452528e1ecd44d1501312f47cd0f7be7a4be2d9f718e5d1b89',
            'High endpoint receipt digest mismatch')
    low_json, high_json = json.loads(low), json.loads(high)
    require(low_json['sign_certified'] and high_json['sign_certified'] and
            low_json['full_feedback_source_enclosure'][0] > 0 and
            high_json['full_feedback_source_enclosure'][1] < 0,
            'Fixed-boundary endpoint sign enclosure mismatch')

    if verify_source_objects:
        def git(*args: str) -> bytes:
            return subprocess.check_output(['git', *args], cwd=root)
        require(git('rev-parse', BASE).decode().strip() == BASE and
                git('rev-parse', HEAD).decode().strip() == HEAD,
                'Pinned source commits are unavailable')
        require(git('diff', '--binary', '--full-index', BASE, HEAD) == patch,
                'Patch differs from pinned source commits')
        for row in rows:
            require(git('show', f'{HEAD}:{row["archive_path"]}') ==
                    snapshots[row['archive_path']],
                    f'Git tree bytes differ: {row["archive_path"]}')
        require(len(git('rev-list', '--reverse', f'{BASE}..{HEAD}').splitlines()) == 7,
                'Commit count differs from pinned source range')

    return {
        'status': 'PASS_SOURCE_AND_REPLAY_BYTES',
        'owner_pr': 334,
        'source_range': f'{BASE}..{HEAD}',
        'changed_paths': len(rows),
        'commits': len(commit_lines),
        'source_snapshot_bytes': manifest['change_summary']['snapshot_bytes'],
        'source_archive_sha256': archive_meta['sha256'],
        'source_patch_sha256': patch_meta['sha256'],
        'direct_click_checks': 109,
        'retained_past_checks': 22,
        'dust_cauchy_checks': 28,
        'fixed_boundary_endpoints': 2,
        'low_receipt_digest_note': 'embedded bytes match; owner printed digest differs by one hex digit',
        'source_object_check': verify_source_objects,
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
