#!/usr/bin/env python3
"""One-shot APFS clone of a D0 Lake cache into an owned detached worktree.

Every regular file uses clonefile(2); no full-copy fallback, replacement, or
source write. Any failure leaves the partial destination in place for review.
"""
from __future__ import annotations
import ctypes
import ctypes.util
import fcntl
import hashlib
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import time

SOURCE = pathlib.Path('/Users/grigorijvahrusev/.codex/worktrees/d0-proof-architecture-followup/d0-main-assembly-audit/03_FORMALIZATION/.lake')
TARGET = pathlib.Path('/private/tmp/d0-2bc-lean-receipt-worktree/03_FORMALIZATION/.lake')
SOURCE_REPO = SOURCE.parent.parent
TARGET_REPO = TARGET.parent.parent
SOURCE_HEAD = 'b30862d47a5972c346d6f6fe9b4cc985d2a86dc7'
TARGET_HEAD = '1eabcccbf7e115c667e9bb8c445ef300107b1493'
TEN_GIB = 10 * 1024 ** 3
NINE_GIB = 9 * 1024 ** 3
MIN_INODES = 500_000
SKIP = {'d0-task-build.lock', 'd0-final-build-receipt.json', 'd0-final-build-receipt.json.tmp'}
PROGRESS = pathlib.Path('/tmp/d0-clone-lake-progress.json')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def resources():
    s = os.statvfs(str(TARGET.parent))
    return s.f_bavail * s.f_frsize, s.f_favail


def check_resources(threshold):
    available, inodes = resources()
    if available < threshold or inodes < MIN_INODES:
        raise RuntimeError(f'resource threshold: free={available}, inodes={inodes}')
    return available, inodes


def main():
    start = time.monotonic()
    counts = {'files': 0, 'directories': 0, 'symlinks': 0, 'logical_bytes': 0, 'sample_hashes': 0}
    state = {'status': 'preflight', 'source': str(SOURCE), 'target': str(TARGET),
             'source_head': SOURCE_HEAD, 'target_head': TARGET_HEAD, 'counts': counts,
             'clonefile_fallback': False, 'source_cache_writes': False}
    def report(status):
        state.update(status=status, elapsed_seconds=round(time.monotonic()-start, 2),
                     available_bytes=resources()[0], available_inodes=resources()[1])
        print(json.dumps(state, ensure_ascii=False), flush=True)
        PROGRESS.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    if TARGET.exists() or TARGET.is_symlink():
        raise RuntimeError('destination already exists; will not overwrite or clean')
    if not SOURCE.is_dir() or SOURCE.is_symlink() or not TARGET.parent.is_dir():
        raise RuntimeError('unexpected source or destination root')
    if SOURCE.stat().st_dev != TARGET.parent.stat().st_dev:
        raise RuntimeError('source and destination are on different devices')
    if git(SOURCE_REPO, 'rev-parse', 'HEAD') != SOURCE_HEAD or git(TARGET_REPO, 'rev-parse', 'HEAD') != TARGET_HEAD:
        raise RuntimeError('source or target HEAD moved')
    if git(SOURCE_REPO, 'status', '--porcelain=v1') or git(TARGET_REPO, 'status', '--porcelain=v1'):
        raise RuntimeError('source or target worktree is dirty')
    if git(TARGET_REPO, 'rev-parse', '--show-toplevel') != str(TARGET_REPO):
        raise RuntimeError('target Git worktree binding is wrong')
    check_resources(TEN_GIB)
    lib = ctypes.CDLL(ctypes.util.find_library('System'), use_errno=True)
    clone = lib.clonefile
    clone.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    clone.restype = ctypes.c_int
    src_lock = os.open(SOURCE / 'd0-task-build.lock', os.O_RDONLY)
    try:
        fcntl.flock(src_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.mkdir(TARGET, stat.S_IMODE(SOURCE.stat().st_mode))
        dirs_to_restore = []
        report('cloning')
        for current, dirs, files in os.walk(SOURCE, topdown=True, followlinks=False):
            source_dir = pathlib.Path(current)
            relative = source_dir.relative_to(SOURCE)
            target_dir = TARGET / relative
            source_dir_info = source_dir.lstat()
            dirs_to_restore.append((target_dir, source_dir_info))
            for name in list(dirs):
                source_item = source_dir / name
                target_item = target_dir / name
                info = source_item.lstat()
                if stat.S_ISLNK(info.st_mode):
                    os.symlink(os.readlink(source_item), target_item)
                    dirs.remove(name)
                    counts['symlinks'] += 1
                elif stat.S_ISDIR(info.st_mode):
                    os.mkdir(target_item, stat.S_IMODE(info.st_mode))
                    os.chmod(target_item, stat.S_IMODE(info.st_mode))
                    counts['directories'] += 1
                else:
                    raise RuntimeError(f'non-directory in directory walk: {source_item}')
            for name in files:
                if relative == pathlib.Path('.') and name in SKIP:
                    continue
                source_item = source_dir / name
                target_item = target_dir / name
                info = source_item.lstat()
                if stat.S_ISLNK(info.st_mode):
                    os.symlink(os.readlink(source_item), target_item)
                    counts['symlinks'] += 1
                    continue
                if not stat.S_ISREG(info.st_mode):
                    raise RuntimeError(f'special file refused: {source_item}')
                if clone(os.fsencode(source_item), os.fsencode(target_item), 0):
                    e = ctypes.get_errno()
                    raise OSError(e, f'clonefile failed, no fallback: {source_item}: {os.strerror(e)}')
                cloned = target_item.lstat()
                fingerprint = lambda s: (s.st_dev, s.st_size, s.st_mtime_ns, stat.S_IMODE(s.st_mode))
                if (not stat.S_ISREG(cloned.st_mode) or cloned.st_ino == info.st_ino or
                        fingerprint(source_item.lstat()) != fingerprint(info) or
                        cloned.st_size != info.st_size):
                    raise RuntimeError(f'source changed or clone metadata invalid: {source_item}')
                os.chmod(target_item, stat.S_IMODE(info.st_mode))
                os.utime(target_item, ns=(info.st_atime_ns, info.st_mtime_ns), follow_symlinks=False)
                counts['files'] += 1
                counts['logical_bytes'] += info.st_size
                if counts['files'] <= 5 or (counts['files'] % 4096 == 0 and info.st_size <= 8 * 1024 * 1024):
                    if hashlib.sha256(source_item.read_bytes()).digest() != hashlib.sha256(target_item.read_bytes()).digest():
                        raise RuntimeError(f'sampled clone hash mismatch: {source_item}')
                    counts['sample_hashes'] += 1
                if counts['files'] % 64 == 0:
                    check_resources(NINE_GIB)
                if counts['files'] % 2048 == 0:
                    report('cloning')
        for path, info in reversed(dirs_to_restore):
            os.chmod(path, stat.S_IMODE(info.st_mode))
            os.utime(path, ns=(info.st_atime_ns, info.st_mtime_ns), follow_symlinks=False)
        check_resources(NINE_GIB)
        if git(SOURCE_REPO, 'rev-parse', 'HEAD') != SOURCE_HEAD or git(TARGET_REPO, 'rev-parse', 'HEAD') != TARGET_HEAD:
            raise RuntimeError('source or target HEAD moved during clone')
        report('cloned_pending_verification')
    except BaseException:
        report('failed_partial_destination_retained')
        raise
    finally:
        os.close(src_lock)


if __name__ == '__main__':
    main()
