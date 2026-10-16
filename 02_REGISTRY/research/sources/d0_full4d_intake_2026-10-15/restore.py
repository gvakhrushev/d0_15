#!/usr/bin/env python3
"""Restore the unchanged 25-file full-4D intake and replay it without network."""
from __future__ import annotations
import argparse, hashlib, json, lzma, os, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
HERE = Path(__file__).resolve().parent
PART_HASHES = [
    'faafbd0043100961fd3d8cdfae6a591c988bab7c1edee757a09416515da6fb8e',
    'eb5ba66ad85cf27a998618dbefbda6daf4aba463c360e32cac8ce154a2ab18ba',
    '2251d86b5e79476fdb755b219a52630f5c9c387daf605cb759bc2d70599ee46e',
    '47d2f824815764bc4e0a6672b8e8eaa704be8278217897c25a220ec95b61bc8c',
    '3cfad399ac8fe849f779d3d911d42d28e0419cd88de9e6742ed7adfd8c502ae3',
]
PACK_SHA = '3f71d2cfdc56ef5569bd54f6d84fc06f66e3e168ccfe2078a8bfc24d707cf2d0'
JSON_SHA = 'fa6bf3cf390f2d39a3d21c4e2a0598077d8b0cefc5ea8cce410688f7e1fd87b5'
SOURCE = '02_REGISTRY/research/sources/d0_full_four_dimensional_sheet_2026-10-15'

def require(value: bool, message: str) -> None:
    if not value: raise RuntimeError(message)

def payload() -> dict[str, str]:
    parts = []
    for i, wanted in enumerate(PART_HASHES):
        data = (HERE / f'payload.xz.{i:02}').read_bytes()
        require(hashlib.sha256(data).hexdigest() == wanted, f'PART_HASH_{i}')
        parts.append(data)
    packed = b''.join(parts)
    require(hashlib.sha256(packed).hexdigest() == PACK_SHA, 'PACK_HASH')
    raw = lzma.decompress(packed, memlimit=128*1024*1024)
    require(hashlib.sha256(raw).hexdigest() == JSON_SHA, 'JSON_HASH')
    files = json.loads(raw)
    require(isinstance(files, dict) and len(files) == 25, 'FILE_COUNT')
    for name, text in files.items():
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts, 'UNSAFE_PATH')
        require(name.startswith('02_REGISTRY/research/') and isinstance(text, str), 'FILE_TYPE')
    return files

def restore(root: Path) -> Path:
    root = root.resolve()
    files = payload()
    # Validate all conflicts before writing anything.
    for name, text in files.items():
        out = (root/name).resolve()
        require(out.is_relative_to(root), 'SYMLINK_ESCAPE')
        if out.exists(): require(out.is_file() and out.read_bytes() == text.encode(), 'EXISTING_FILE_DIFFERS: '+name)
    for name, text in files.items():
        out = root/name
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists(): out.write_bytes(text.encode())
        require(out.read_bytes() == text.encode(), 'RESTORE_BYTES: '+name)
    return root/SOURCE

def replay(root: Path, full: bool) -> None:
    source = restore(root)
    env = {**os.environ, 'OPENBLAS_NUM_THREADS':'1', 'OMP_NUM_THREADS':'1', 'PYTHONDONTWRITEBYTECODE':'1'}
    groups = [['verify.py'], ['-O', 'verify.py', '--kernel-only'], ['hostile.py']]
    if full: groups[1] = ['-O', 'verify.py']
    for group in groups:
        subprocess.run([sys.executable, *group], cwd=source, env=env, check=True, timeout=240)
    print('PASS_FULL_4D_INTAKE_25_FILES_NOT_ALL_MESH_GR', flush=True)

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--extract', type=Path)
    ap.add_argument('--full', action='store_true', help='also rerun the full interval computation under Python -O')
    args = ap.parse_args()
    if args.extract:
        print(restore(args.extract))
    else:
        with tempfile.TemporaryDirectory(prefix='d0-full4d-') as directory:
            replay(Path(directory), args.full)
if __name__ == '__main__': main()
