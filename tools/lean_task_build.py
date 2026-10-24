#!/usr/bin/env python3
"""Serialized Lean task build helper.

Use narrow builds while iterating and exactly one final D0.All build per unchanged
source tree. The helper rejects concurrent builds sharing the same .lake cache and
invalidates a result if Lean sources changed while the build was running.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import subprocess
import sys
import time
from contextlib import contextmanager

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMAL = ROOT / "03_FORMALIZATION"
LAKE = FORMAL / ".lake"
LOCK = LAKE / "d0-task-build.lock"
STAMP = LAKE / "d0-final-build.sha256"


class BuildLockBusy(Exception):
    """Raised when another process owns the shared Lake build cache."""


@contextmanager
def build_lock(path: pathlib.Path):
    """Lock one byte without truncating the persistent lock file.

    POSIX uses flock; Windows uses the CRT byte-range lock. Both are
    non-blocking so concurrent build attempts fail before starting Lake.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as lock:
        lock.seek(0, os.SEEK_END)
        if lock.tell() == 0:
            lock.write(b"\0")
            lock.flush()
        lock.seek(0)

        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                if exc.errno in {13, 36} or getattr(exc, "winerror", None) in {33, 36}:
                    raise BuildLockBusy from exc
                raise
            try:
                yield
            finally:
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise BuildLockBusy from exc
            try:
                yield
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def source_digest() -> str:
    h = hashlib.sha256()
    # Lake dependencies are inputs to the imported environment, but they are
    # pinned independently by lake-manifest.json. Hashing their checked-out
    # sources here both makes every build needlessly expensive and includes
    # files that are not project-owned Lean sources.
    files = sorted(
        p for p in FORMAL.rglob("*.lean")
        if ".lake" not in p.relative_to(FORMAL).parts
    )
    for extra in ("lakefile.lean", "lake-manifest.json", "lean-toolchain"):
        p = FORMAL / extra
        if p.exists():
            files.append(p)
    for p in sorted(set(files)):
        h.update(p.relative_to(FORMAL).as_posix().encode())
        h.update(b"\0")
        h.update(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
        h.update(b"\0")
    return h.hexdigest()


def run_locked(command: list[str], target: str) -> int:
    LAKE.mkdir(parents=True, exist_ok=True)
    try:
        with build_lock(LOCK):
            before = source_digest()
            started = time.monotonic()
            proc = subprocess.run(command, cwd=FORMAL)
            elapsed = time.monotonic() - started
            after = source_digest()
            print(f"D0_BUILD target={target} seconds={elapsed:.1f} returncode={proc.returncode}")
            if before != after:
                print(
                    "INVALID_BUILD: Lean sources changed while lake was running. "
                    "The build may have compiled an obsolete file; rerun after edits stop.",
                    file=sys.stderr,
                )
                return 3
            return proc.returncode
    except BuildLockBusy:
        print(
            "REFUSE: another D0 Lean build already owns the shared .lake cache; "
            "do not start a second lake process.",
            file=sys.stderr,
        )
        return 2


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    narrow = sub.add_parser("narrow")
    narrow.add_argument("target")

    cache = sub.add_parser("cache")
    cache.add_argument("targets", nargs="*", help="Lean modules/files whose Mathlib cache is needed")

    final = sub.add_parser("final")
    final.add_argument("--force", action="store_true")

    args = ap.parse_args()

    if args.mode == "narrow":
        if args.target in {"D0", "D0.All"}:
            print("REFUSE: use 'final' for D0.All; iterate on one narrow module target.", file=sys.stderr)
            return 2
        return run_locked(["lake", "build", args.target], args.target)

    if args.mode == "cache":
        return run_locked(["lake", "exe", "cache", "get", *args.targets], "mathlib-cache-get")

    digest = source_digest()
    if STAMP.exists() and STAMP.read_text(encoding="utf-8").strip() == digest and not args.force:
        print("SKIP: this exact Lean source tree already passed final D0.All.")
        return 0

    rc = run_locked(["lake", "build", "D0.All"], "D0.All")
    if rc == 0:
        STAMP.write_text(digest + "\n", encoding="utf-8")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
