#!/usr/bin/env python3
"""Verify frozen native full-history jet inputs and focused calibration.

The all-depth and common marked-limit theorems are the pinned analytic
proof. Floating receipt bytes record provenance, not expected replay bytes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20"
INPUTS = [
    "02_REGISTRY/research/A4D_NATIVE_RELATIVE_HISTORY_FIRST_JET_AND_MARKED_LIMIT_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/check_relative_history_first_jet.py",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RELATIVE_HISTORY_FIRST_JET.json",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_native_relative_transfer_2026-10-17/check_native_relative_transfer.py",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md",
    "02_REGISTRY/research/A4D_VARIABLE_RECORD_FIRST_SOURCE_LIMIT.md",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/inputs/SMOOTH_BULK_FULL128_C1_HEAT_HISTORY_TRANSFER_AT_BE5E5BD0.md",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/inputs/MINIMAL_GOLDEN_COMPLETE_SOURCE_AT_C16531E3.md",
]


def verify_inputs():
    pins = json.loads((PACKET / "SOURCE_PINS.json").read_text(encoding="utf-8"))
    entries = pins["owned_inputs"] + pins["frozen_artifacts"]
    declared = {row["path"] for row in entries}
    declared.add((PACKET / "SOURCE_PINS.json").relative_to(ROOT).as_posix())
    if declared != set(INPUTS):
        raise AssertionError("Declared input closure differs from frozen pins")
    for row in entries:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError(f"Frozen input changed: {row['path']}")


def main():
    verify_inputs()
    run = subprocess.run(
        [sys.executable, "-B", "-W", "error",
         str(PACKET / "check_relative_history_first_jet.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        sys.stderr.write(run.stderr)
        raise subprocess.CalledProcessError(run.returncode, run.args)
    if run.stderr:
        raise AssertionError(f"Unexpected checker stderr: {run.stderr}")
    actual = json.loads(run.stdout)
    saved = json.loads((PACKET / "RELATIVE_HISTORY_FIRST_JET.json").read_text(encoding="utf-8"))
    if actual["status"] != "PASS":
        raise AssertionError("Native complete-history first-jet calibration failed")
    for key in ("carrier", "scope", "original_fixture_source_sha256",
                "exact_general_cross_differentiation"):
        if actual[key] != saved[key]:
            raise AssertionError(f"Frozen exact interface differs: {key}")
    physical_key = "separate_physical_coframe_scaling"
    numerical_key = "literal_positive_first_role_controls_at_existing_mesh"
    if {k: v for k, v in actual[physical_key].items() if k != numerical_key} != {
        k: v for k, v in saved[physical_key].items() if k != numerical_key
    }:
        raise AssertionError("Frozen physical scale and clock interface differs")
    cases = actual["literal_matrix_verification"]["cases"]
    if [(c["nu"], c["momentum_role"], c["momentum_sign"]) for c in cases] != [
        (c["nu"], c["momentum_role"], c["momentum_sign"])
        for c in saved["literal_matrix_verification"]["cases"]
    ]:
        raise AssertionError("The declared original shell/parameter checks changed")
    verify_inputs()
    print("PASS exact native connection, full-history derivative norm and hostile phase control")
    print("PASS all128 original matrix jets and complete ordered-sector normalization")
    print("PASS separate physical coframe scaling, sharp longer clock and all128 a-jets")
    print("PASS frozen proof/calibration inputs and declared carrier/scope")
    print("SCOPE: fixed-shell marked C1 carrier including the prospective physical h^-4 clock; actual clock/Book selection and raw spatial source remain open.")


if __name__ == "__main__":
    main()
