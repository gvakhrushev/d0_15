#!/usr/bin/env python3
"""Compare the Lean and Python four-mode CAR matrices entry by entry.

Run from any directory after preparing the repository's Lean dependencies:
    python 02_REGISTRY/research/sources/d0_archive_car_comparison_2026_11_27/check.py

The default uses lake env lean in 03_FORMALIZATION. An explicit --lean
binary uses the caller's LEAN_PATH, useful with an already compiled cache.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
CERTIFICATE = ROOT / "04_CERTIFICATES" / "vp_archive_car_relations.py"
LEAN_SOURCE = Path(__file__).with_name("Compare.lean")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", help="Lean binary to use with the caller's LEAN_PATH")
    args = parser.parse_args()

    command = [args.lean] if args.lean else ["lake", "env", "lean"]
    result = subprocess.run(
        [*command, str(LEAN_SOURCE)],
        cwd=ROOT / "03_FORMALIZATION",
        check=True,
        capture_output=True,
        text=True,
    )
    lean_matrices = ast.literal_eval(result.stdout)
    spec = importlib.util.spec_from_file_location("archive_car_relations", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the CAR certificate")
    certificate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(certificate)
    python_matrices = [
        certificate.construct_annihilation_matrix(role) for role in certificate.ROLES
    ]
    if lean_matrices != python_matrices:
        raise ValueError("Lean and Python annihilation matrices differ")
    if certificate.check_car_system() != (True, True, True):
        raise ValueError("The canonical CAR system failed")
    if all(certificate.check_car_system(mutate=True)):
        raise ValueError("The mutated sign convention passed the CAR checks")
    print("PASS: 4 x 16 x 16 Lean and Python matrix entries agree")
    print("PASS: canonical CAR and mutated-sign negative control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
