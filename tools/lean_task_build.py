#!/usr/bin/env python3
"""Serialized Lean task build helper.

Use narrow builds while iterating and exactly one final D0.All build per unchanged
source tree. The helper rejects concurrent builds sharing the same .lake cache and
invalidates a result if Lean sources changed while the build was running.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMAL = ROOT / "03_FORMALIZATION"
LAKE = FORMAL / ".lake"
LOCK = LAKE / "d0-task-build.lock"
STAMP = LAKE / "d0-final-build.sha256"


def source_digest() -> str:
    h = hashlib.sha256()
    files = sorted(FORMAL.rglob("*.lean"))
    for extra in ("lakefile.lean", "lake-manifest.json", "lean-toolchain"):
        p = FORMAL / extra
        if p.exists():
            files.append(p)
    for p in sorted(set(files)):
        h.update(p.relative_to(FORMAL).as_posix().encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def run_locked(target: str) -> int:
    LAKE.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(
                "REFUSE: another D0 Lean build already owns the shared .lake cache; "
                "do not start a second lake process.",
                file=sys.stderr,
            )
            return 2

        before = source_digest()
        started = time.monotonic()
        proc = subprocess.run(["lake", "build", target], cwd=FORMAL)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    narrow = sub.add_parser("narrow")
    narrow.add_argument("target")

    final = sub.add_parser("final")
    final.add_argument("--force", action="store_true")

    args = ap.parse_args()

    if args.mode == "narrow":
        if args.target in {"D0", "D0.All"}:
            print("REFUSE: use 'final' for D0.All; iterate on one narrow module target.", file=sys.stderr)
            return 2
        return run_locked(args.target)

    digest = source_digest()
    if STAMP.exists() and STAMP.read_text(encoding="utf-8").strip() == digest and not args.force:
        print("SKIP: this exact Lean source tree already passed final D0.All.")
        return 0

    rc = run_locked("D0.All")
    if rc == 0:
        STAMP.write_text(digest + "\n", encoding="utf-8")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
