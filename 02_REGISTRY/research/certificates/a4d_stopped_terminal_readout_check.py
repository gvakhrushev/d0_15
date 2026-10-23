#!/usr/bin/env python3
"""Replay the scoped stopped-terminal CAR16 source application without mutation.

The saved receipt is immutable evidence of the authoring run. Numerical
identities and bounds are asserted by the checker on the actual replay;
floating output bytes are not required to match across BLAS implementations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_stopped_terminal_readout_2026-10-20"

# Literal paths are consumed by the ordinary changed-input closure.
INPUTS = [
    "02_REGISTRY/research/A4D_STOPPED_TERMINAL_READOUT_COMPLETE_SOURCE_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_stopped_terminal_readout_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_stopped_terminal_readout_2026-10-20/check_terminal_readout.py",
    "02_REGISTRY/research/sources/d0_stopped_terminal_readout_2026-10-20/TERMINAL_READOUT.json",
    "02_REGISTRY/research/sources/d0_stopped_terminal_readout_2026-10-20/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/flag_source.md",
    "02_REGISTRY/research/sources/d0_relational_coherent_synthesis_2026-10-20/fixed_readout.md",
    "02_REGISTRY/research/sources/d0_relational_coherent_synthesis_2026-10-20/coherent_execution.md",
]


def verify_inputs() -> None:
    pins = json.loads((PACKET / "SOURCE_PINS.json").read_text(encoding="utf-8"))
    entries = pins["owned_inputs"] + pins["frozen_artifacts"]
    declared = {row["path"] for row in entries}
    declared.add((PACKET / "SOURCE_PINS.json").relative_to(ROOT).as_posix())
    if declared != set(INPUTS):
        raise AssertionError("Declared input closure differs from frozen pins")
    for row in entries:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            raise AssertionError(f"Frozen input changed: {row['path']}")


def main() -> None:
    verify_inputs()
    run = subprocess.run(
        [sys.executable, "-B", "-W", "error", str(PACKET / "check_terminal_readout.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        sys.stderr.write(run.stderr)
        raise subprocess.CalledProcessError(run.returncode, run.args)
    if run.stderr:
        raise AssertionError(f"Unexpected checker stderr: {run.stderr}")
    actual = json.loads(run.stdout)
    saved = json.loads((PACKET / "TERMINAL_READOUT.json").read_text(encoding="utf-8"))
    if actual["status"] != "PASS":
        raise AssertionError("Scoped calculation did not pass")
    for key in ("exact", "carrier", "tolerances", "scope"):
        if actual[key] != saved[key]:
            raise AssertionError(f"Frozen exact interface differs: {key}")
    if [row["cap"] for row in actual["full_leaf_checks"]] != [3, 4, 7]:
        raise AssertionError("Incomplete chronological-tree replay")
    if [row["cap"] for row in actual["cap_source_checks"]] != [7, 20, 40, 60]:
        raise AssertionError("Incomplete terminal-source replay")
    verify_inputs()
    print("PASS full stopped CAR16 terminal-readout laws, sources, code and dark/rank-birth controls")
    print("PASS supplied moving-instrument jets and retained successful-source control")
    print("PASS frozen provenance unchanged; exact interface matches saved receipt")
    print("SCOPE: compact terminal cap-error component; physical Book price/admission and GR remain open.")


if __name__ == "__main__":
    main()
