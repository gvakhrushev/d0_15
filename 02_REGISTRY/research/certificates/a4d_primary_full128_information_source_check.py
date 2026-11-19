#!/usr/bin/env python3
"""Replay the original one-round full128 source on the primary preparation.

Numerical receipt bytes are provenance, not cross-platform expected output.
Exact interfaces and scoped mathematical checks must reproduce.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20"
INPUTS = [
    "02_REGISTRY/research/A4D_PRIMARY_FULL128_COMMON_RECORD_INFORMATION_SOURCE_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/primary_full128_helper.py",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/check_primary_full128_information_source.py",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/PRIMARY_FULL128_INFORMATION.json",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/PRIMARY_DOMAIN_SOURCE.json",
    "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md",
    "02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_two_round_complete_shannon_order_source.py",
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
         str(PACKET / "check_primary_full128_information_source.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        sys.stderr.write(run.stderr)
        raise subprocess.CalledProcessError(run.returncode, run.args)
    if run.stderr:
        raise AssertionError(f"Unexpected checker stderr: {run.stderr}")
    actual = json.loads(run.stdout)
    saved = json.loads((PACKET / "PRIMARY_FULL128_INFORMATION.json").read_text(encoding="utf-8"))
    if actual["status"] != "PASS":
        raise AssertionError("Scoped full128 source calculation did not pass")
    for key in ("carrier", "regularization", "scope", "finite_difference_step",
                "primary_checker_source_sha256"):
        if actual[key] != saved[key]:
            raise AssertionError(f"Frozen exact interface differs: {key}")
    if [(c["wave_amplitude"], c["variation"]) for c in actual["cases"]] != [
        (c["wave_amplitude"], c["variation"]) for c in saved["cases"]
    ]:
        raise AssertionError("The declared primary source tangents changed")
    verify_inputs()
    print("PASS original full128 record, fixed33-vector isometry and actual primary preparation")
    print("PASS true-adjoint Julia jets, paid-port source and explicit regularized entropy jets")
    print("PASS frozen input provenance and carrier/scope interface")
    print("SCOPE: one-round information-source candidates; full physical price and GR remain open.")


if __name__ == "__main__":
    main()
