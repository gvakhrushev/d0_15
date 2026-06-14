#!/usr/bin/env python3
"""Guard: the full D0 Lean library must compile.

Runs `lake build D0.All` (the release "build all" aggregate, regenerated from
CLAIM_TO_LEAN_MAP.csv by tools/generate_lean_aggregates.py) and FAILS (non-zero
exit) if any module does not elaborate.

Why this guard exists
---------------------
CI historically scored Lean off declared `lean_status` + on-disk module existence
and never ran `lake build`. That masked 17 modules that had rotted (stale Mathlib
imports, malformed `theorem _ : Prop := ...`, references to never-defined APIs).
The discrepancy was only caught by a manual full build on 2026-06-14. This guard
closes that hole: the library is verified to actually compile on every change.

It is a real, falsifiable check: break any imported module and it exits 1.

Usage
-----
    python tools/check_lean_builds.py                 # build D0.All
    python tools/check_lean_builds.py D0.NoGo.StressTestSuite   # narrow target(s)
    LAKE=/path/to/lake python tools/check_lean_builds.py
    python tools/check_lean_builds.py --lake C:\\Users\\me\\.elan\\bin\\lake.exe

Cost note: a cold build (no Mathlib cache) is slow. In CI, set up elan from
09_LEAN_FORMALIZATION/lean-toolchain and run `lake exe cache get` first
(see .github/workflows/lean-build.yml).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = REPO_ROOT / "09_LEAN_FORMALIZATION"


def find_lake(explicit: str | None) -> str | None:
    """Locate the `lake` executable: --lake flag, $LAKE, PATH, then elan defaults."""
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("LAKE"):
        candidates.append(os.environ["LAKE"])
    on_path = shutil.which("lake")
    if on_path:
        candidates.append(on_path)
    # elan default install locations (Windows + POSIX)
    home = Path.home()
    candidates += [
        str(home / ".elan" / "bin" / ("lake.exe" if os.name == "nt" else "lake")),
    ]
    for cand in candidates:
        if cand and Path(cand).exists():
            return cand
    # last resort: bare name, let the OS resolve it (may still work under a shim)
    return on_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        default=["D0.All"],
        help="Lake build targets (default: D0.All — the whole library).",
    )
    parser.add_argument("--lake", help="Path to the lake executable.")
    args = parser.parse_args()

    if not LEAN_DIR.is_dir():
        print(f"FAIL: lean directory not found at {LEAN_DIR}")
        return 1

    lake = find_lake(args.lake)
    if not lake:
        print(
            "FAIL: could not locate `lake`. Install elan / set $LAKE or pass --lake "
            "(e.g. ~/.elan/bin/lake)."
        )
        return 1

    targets = args.targets or ["D0.All"]
    print(f"check_lean_builds: {lake} build {' '.join(targets)}  (cwd={LEAN_DIR})")
    sys.stdout.flush()

    proc = subprocess.run([lake, "build", *targets], cwd=str(LEAN_DIR))
    if proc.returncode != 0:
        print(f"FAIL: `lake build {' '.join(targets)}` exited {proc.returncode}")
        return proc.returncode or 1

    print(f"PASS: `lake build {' '.join(targets)}` is green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
