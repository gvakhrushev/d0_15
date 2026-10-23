#!/usr/bin/env python3
"""Replay the actual primary prepared-cut source with complete oldRIGHT.

Receipt bytes record provenance; replay compares the declared interface,
not floating output bytes. The exact sign proof is in the pinned RESULT.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20"
INPUTS = [
    "02_REGISTRY/research/A4D_PRIMARY_PREPARED_CUT_PAID_FEEDBACK_SOURCE_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20/check_primary_paid_feedback.py",
    "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20/PRIMARY_PAID_FEEDBACK.json",
    "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/primary_full128_helper.py",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/PRIMARY_FULL128_INFORMATION.json",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md",
    "02_REGISTRY/research/A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "02_REGISTRY/research/sources/d0_primary_paid_feedback_source_2026-10-20/inputs/CAUSAL_BOOK_SOURCE_AT_D333307D.md",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md",
]


def verify_inputs():
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


def main():
    verify_inputs()
    run = subprocess.run(
        [sys.executable, "-B", "-W", "error",
         str(PACKET / "check_primary_paid_feedback.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        sys.stderr.write(run.stderr)
        raise subprocess.CalledProcessError(run.returncode, run.args)
    if run.stderr:
        raise AssertionError(f"Unexpected checker stderr: {run.stderr}")
    actual = json.loads(run.stdout)
    saved = json.loads((PACKET / "PRIMARY_PAID_FEEDBACK.json").read_text(encoding="utf-8"))
    if actual["status"] != "PASS":
        raise AssertionError("Actual prepared-cut source check did not pass")
    for key in ("inputs", "carrier", "scope"):
        if actual[key] != saved[key]:
            raise AssertionError(f"Frozen exact interface differs: {key}")
    if actual["primary_flat"]["exact_analytic_ratio_upper_bound"] != "1/4":
        raise AssertionError("The declared analytic comparison constant changed")
    for key in ("omitted_marker_zero_complement_control_nonzero",
                "compressing_whole_DATA_feedback_control_nonzero"):
        if actual["complete_complement"][key] is not True:
            raise AssertionError(f"Hostile omission check failed: {key}")
    verify_inputs()
    print("PASS actual primary prepared cut, all128 port operator Grams and full oldRIGHT counting")
    print("PASS complete work complement, outside-E leakage and common-scale source")
    print("PASS frozen provenance and exact ratio-bound/carrier/scope interface")
    print("SCOPE: supplied echo/cut source obstruction; full physical Book price and GR remain open.")


if __name__ == "__main__":
    main()
