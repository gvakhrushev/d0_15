#!/usr/bin/env python3
"""Replay the scoped primary-family Julia-domain and actual R-source map.

The saved numerical receipt records the authoring run. Floating output
bytes are not a cross-platform invariant; replay asserts the mathematical
identities and tolerances and preserves the exact carrier/scope interface.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20"

# Literal paths participate in ordinary changed-input closure.
INPUTS = [
    "02_REGISTRY/research/A4D_PRIMARY_CONFIGURED_SOURCE_STRICT_JULIA_AND_RAYLEIGH_GATE_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/PRIMARY_DOMAIN_SOURCE.json",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/inputs/primary_recovery.md",
    "02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md",
    "02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md",
    "02_REGISTRY/research/A4D_MICROHISTORY_EINSTEIN_QUOTIENT_AND_PRICE_EULER_UNIVERSALITY_2026_10_18.md",
    "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
    "02_REGISTRY/research/A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md",
    "02_REGISTRY/research/A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md",
    "02_REGISTRY/research/A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md",
    "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py",
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
        [sys.executable, "-B", "-W", "error", str(PACKET / "check_primary_domain_source.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        sys.stderr.write(run.stderr)
        raise subprocess.CalledProcessError(run.returncode, run.args)
    if run.stderr:
        raise AssertionError(f"Unexpected checker stderr: {run.stderr}")
    actual = json.loads(run.stdout)
    saved = json.loads((PACKET / "PRIMARY_DOMAIN_SOURCE.json").read_text(encoding="utf-8"))
    if actual["status"] != "PASS":
        raise AssertionError("Scoped calculation did not pass")
    for key in ("exact_symbolic", "carrier", "density", "link_hessian", "scope"):
        if actual[key] != saved[key]:
            raise AssertionError(f"Frozen exact interface differs: {key}")
    if actual["scale"]["p_exponent"] != 3:
        raise AssertionError("Unexpected fixed chart scale")
    if [row["wave_amplitude"] for row in actual["two_primary_representatives"]] != [.125, .25]:
        raise AssertionError("Incomplete same-family source test")
    verify_inputs()
    print("PASS fixed-scale configured source transport and strict native Julia chart")
    print("PASS original CAR16/fullRIGHT128 R-link source, positive Hessian and direct price check")
    print("PASS frozen provenance unchanged; exact carrier and scope match saved receipt")
    print("SCOPE: primary-family matrix/source application; complete physical price and GR remain open.")


if __name__ == "__main__":
    main()
