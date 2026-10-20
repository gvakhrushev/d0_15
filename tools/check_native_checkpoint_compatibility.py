#!/usr/bin/env python3
"""Compile the ten #322 capsules against maintained sources, without overlays."""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import subprocess

import native_checkpoint_inputs as historical

ROOT = Path(__file__).resolve().parents[1]
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interface-only", action="store_true",
                        help="check preserved declarations only; this does not compile Lean")
    args = parser.parse_args()
    manifest, _, preserved = historical.validate(ROOT)
    maintained_sha = historical.sha(historical.read(ROOT, historical.TARGET))
    if args.interface_only:
        print(json.dumps({"scope": "TEXT_INTERFACE_ONLY_NOT_LEAN_COMPILATION",
                          "maintained_sha256": maintained_sha,
                          "preserved_declarations": preserved}, indent=2))
        return 0

    formal = ROOT / "03_FORMALIZATION"
    lake_dir = formal / ".lake"
    lake_dir.mkdir(exist_ok=True)
    capsules = sorted(manifest["compatibility_capsules"])
    imports = sorted({name for path in capsules
                      for name in re.findall(r"(?m)^import\s+(D0\.[\w.]+)",
                                             historical.read(ROOT, path).decode())})
    with (lake_dir / "d0-task-build.lock").open("w") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit("Another Lean build owns this .lake cache")
        subprocess.run(["lake", "build", *imports], cwd=formal, check=True)
        records = []
        for path in capsules:
            result = subprocess.run(["lake", "env", "lean", "../" + path],
                                    cwd=formal, capture_output=True, text=True)
            output = result.stdout + result.stderr
            print("CURRENT_SOURCE_CAPSULE " + path, flush=True)
            print(output, end="" if output.endswith("\n") else "\n", flush=True)
            if result.returncode or "sorryAx" in output or "Lean.trustCompiler" in output:
                raise SystemExit("Current-source capsule compilation failed: " + path)
            axioms = {name.strip()
                      for group in re.findall(r"depends on axioms:\s*\[([^\]]*)\]", output, re.S)
                      for name in group.split(",") if name.strip()}
            if not axioms <= STANDARD_AXIOMS:
                raise SystemExit("Unexpected current-source axiom dependency: " + path)
            records.append({"capsule": path, "compiler_exit_code": 0, "axioms": sorted(axioms)})
        # Neither source evolution during execution nor a capsule edit may reuse this result.
        historical.validate(ROOT)
        if historical.sha(historical.read(ROOT, historical.TARGET)) != maintained_sha:
            raise SystemExit("Maintained source changed during compatibility compilation")
    print(json.dumps({"scope": "CURRENT_SOURCE_LEAN_COMPATIBILITY_NO_PHYSICAL_PROMOTION",
                      "maintained_sha256": maintained_sha, "historical_overlay_used": False,
                      "preserved_declarations": preserved, "compiled_capsules": records}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
