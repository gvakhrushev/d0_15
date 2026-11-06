#!/usr/bin/env python3
"""Verify the exact #334 post-8da source packet and replay receipts."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import stat
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parent
BASE = '8daed32d560df18837bcc69458a8fa538a9cf135'
HEAD = '523d2cbcc0a9771ea40faa4a2eac84cc78704b0e'
INPUT_COMMIT = '1e6420f319d714be53363a77823f76ec620a6473'
INPUT_PATH = (
    '02_REGISTRY/research/sources/'
    'd0_original_retained_history_source_2026-10-28/check_history_source.py'
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_regular(relative: str) -> bytes:
    path = PACKET / relative
    require(not path.is_symlink() and path.is_file(),
            f'Expected regular file: {relative}')
    return path.read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = b'blob ' + str(len(data)).encode('ascii') + b'\0'
    return hashlib.sha1(header + data).hexdigest()


def compare_values(owner: object, replay: object, path: str = '') -> list[tuple[str, float]]:
    differences: list[tuple[str, float]] = []
    if isinstance(owner, dict) and isinstance(replay, dict):
        require(set(owner) == set(replay), f'Result keys differ at {path or "/"}')
        for key in sorted(owner):
            if path == '/environment' and key in ('python', 'numpy'):
                continue
            differences.extend(compare_values(owner[key], replay[key], f'{path}/{key}'))
    elif isinstance(owner, list) and isinstance(replay, list):
        require(len(owner) == len(replay), f'Result list length differs at {path}')
        for index, (left, right) in enumerate(zip(owner, replay)):
            differences.extend(compare_values(left, right, f'{path}/{index}'))
    elif isinstance(owner, float) or isinstance(replay, float):
        require(isinstance(owner, (int, float)) and isinstance(replay, (int, float)),
                f'Result numeric type differs at {path}')
        delta = abs(float(owner) - float(replay))
        require(math.isfinite(delta) and delta <= 2e-15,
                f'Replay numerical drift exceeds 2e-15 at {path}: {delta}')
        if delta:
            differences.append((path, delta))
    else:
        require(owner == replay, f'Result value differs at {path}')
    return differences


def verify(verify_source_objects: bool = False) -> dict[str, object]:
    manifest_bytes = read_regular('MANIFEST.json')
    manifest_sha = read_regular('MANIFEST.sha256').decode('ascii').split()[0]
    require(manifest_sha == sha256(manifest_bytes), 'Manifest SHA-256 mismatch')
    manifest = json.loads(manifest_bytes)
    require(manifest['schema'] == 'd0-pr-source-range-intake-v1' and
            manifest['repository'] == 'gvakhrushev/d0_15' and
            manifest['owner_pr'] == 334,
            'Unexpected source identity')
    source_range = manifest['source_range']
    require(source_range['base_commit'] == BASE and
            source_range['head_commit'] == HEAD and
            source_range['commits'] == 7,
            'Unexpected source range')

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
    require(len(source_rows) == 7 and source_paths == sorted(source_paths) and
            len(source_paths) == len(set(source_paths)),
            'Changed-source path inventory mismatch')
    input_rows = manifest['source_inputs']
    require(len(input_rows) == 1 and
            input_rows[0]['commit'] == INPUT_COMMIT and
            input_rows[0]['repository_path'] == INPUT_PATH,
            'Pinned source input metadata mismatch')

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
                'Archive member list differs from manifest')
        snapshots: dict[str, bytes] = {}
        for name, info in zip(archive_names, infos):
            row = archive_rows[name]
            data = zf.read(info)
            require(len(data) == row['bytes'] and
                    sha256(data) == row['sha256'],
                    f'Archive member mismatch: {row["archive_path"]}')
            if 'head_git_blob_sha1' in row:
                require(git_blob_sha1(data) == row['head_git_blob_sha1'],
                        f'Git blob mismatch: {row["archive_path"]}')
            snapshots[row['archive_path']] = data
            raw_path = (f'upstream/{row["archive_path"]}'
                        if row in source_rows else 'upstream/inputs/check_history_source.py')
            require(read_regular(raw_path) == data,
                    f'Readable source differs from archive: {raw_path}')

    patch_meta = manifest['source_patch']
    compressed_patch = read_regular(patch_meta['path'])
    require(len(compressed_patch) == patch_meta['storage_bytes'] and
            sha256(compressed_patch) == patch_meta['storage_sha256'],
            'Compressed patch digest mismatch')
    patch = gzip.decompress(compressed_patch)
    require(len(patch) == patch_meta['bytes'] and
            sha256(patch) == patch_meta['sha256'], 'Patch digest mismatch')

    commits = read_regular('COMMITS.tsv')
    require(sha256(commits) == manifest['commit_list']['sha256'],
            'Commit-list digest mismatch')
    commit_lines = commits.decode('utf-8').splitlines()
    require(len(commit_lines) == 7 and
            [line.split('\t', 1)[0] for line in commit_lines] ==
            [row['sha'] for row in manifest['source_commits']],
            'Ordered commit list mismatch')

    replay_meta = manifest['replay']
    normal = read_regular(replay_meta['normal_output'])
    optimized = read_regular(replay_meta['optimized_output'])
    require(normal == optimized, 'Normal and python -O outputs differ byte-for-byte')
    owner = read_regular(replay_meta['owner_output'])
    local_result = json.loads(normal)
    owner_result = json.loads(owner)
    require(local_result['status'] == 'PASS_COMPLETE_FIXED_PREFIX_COVECTOR_RECOVERY' and
            owner_result['status'] == local_result['status'] and
            local_result['checks'] == owner_result['checks'] == 69,
            'Replay status or control count mismatch')
    for key in ('original_admission_derived', 'exact_finite_stationary_root_proved',
                'uncontrolled_new_apparatus_rows_eliminated',
                'full_GR_native_program_executed', 'GR_closed'):
        require(local_result[key] is False and owner_result[key] is False,
                f'Scientific boundary changed: {key}')
    numerical_differences = compare_values(owner_result, local_result)

    normal_stderr = read_regular(replay_meta['normal_stderr'])
    optimized_stderr = read_regular(replay_meta['optimized_stderr'])
    require(normal_stderr == optimized_stderr,
            'Normal and python -O diagnostic logs differ')
    stderr_text = normal_stderr.decode('utf-8')
    warning_lines = [line for line in stderr_text.splitlines()
                     if 'RuntimeWarning:' in line]
    require(len(warning_lines) == 120,
            'RuntimeWarning count differs from the recorded local replay')
    require(all(any(message in line for message in (
        'divide by zero encountered in matmul',
        'overflow encountered in matmul',
        'invalid value encountered in matmul')) for line in warning_lines),
        'Unexpected warning class in replay log')

    failed_solve = json.loads(read_regular(replay_meta['failed_full_solve']))
    require(failed_solve['success'] is False and
            failed_solve['accepted_as_stationary'] is False and
            failed_solve['positive_orientation_kept'] is False and
            failed_solve['GR_closed'] is False,
            'Failed unrestricted exploration was promoted')

    source_object_check = False
    if verify_source_objects:
        def git(*args: str) -> bytes:
            return subprocess.check_output(['git', *args], cwd=PACKET)

        require(git('rev-parse', BASE).decode().strip() == BASE and
                git('rev-parse', HEAD).decode().strip() == HEAD and
                git('rev-parse', INPUT_COMMIT).decode().strip() == INPUT_COMMIT,
                'Pinned Git commits are unavailable')
        require(git('diff', '--binary', '--full-index', BASE, HEAD) == patch,
                'Patch differs from pinned source commits')
        for row in source_rows:
            require(git('show', f'{HEAD}:{row["archive_path"]}') ==
                    snapshots[row['archive_path']],
                    f'Git tree bytes differ: {row["archive_path"]}')
        require(git('show', f'{INPUT_COMMIT}:{INPUT_PATH}') ==
                snapshots['inputs/check_history_source.py'],
                'Pinned original constructor bytes differ')
        require(len(git('rev-list', '--reverse', f'{BASE}..{HEAD}').splitlines()) == 7,
                'Commit count differs from pinned range')
        source_object_check = True

    return {
        'status': 'PASS_SOURCE_AND_REPLAY_BYTES',
        'owner_pr': 334,
        'source_range': f'{BASE}..{HEAD}',
        'changed_paths': len(source_rows),
        'commits': len(commit_lines),
        'source_archive_sha256': archive_meta['sha256'],
        'source_patch_sha256': patch_meta['sha256'],
        'replay_status': local_result['status'],
        'replay_checks': local_result['checks'],
        'normal_optimized_output_identical': True,
        'owner_local_numeric_fields_with_drift': len(numerical_differences),
        'owner_local_max_absolute_float_drift': max(
            (delta for _, delta in numerical_differences), default=0.0),
        'runtime_warning_records_each_run': len(warning_lines),
        'physical_admission': False,
        'scientific_acceptance': False,
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
