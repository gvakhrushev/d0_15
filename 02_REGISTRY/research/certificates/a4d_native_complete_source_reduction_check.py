#!/usr/bin/env python3
"""Read-only replay of the frozen actual-cut / marginal / full-history packet.

Only three new bounded calculations run. Existing native constructors are
consumed by the history checker's pinned AST slice, never as an old suite.
Receipt bytes are provenance; floating diagnostics have explicit tolerances.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22"
INPUTS = [
    "requirements.txt",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
    "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py",
    "02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/PROOF.md",
    "02_REGISTRY/research/sources/d0_generated_thermal_source_2026-10-22/ACTUAL_CUT_APPLICATION.md",
    "02_REGISTRY/research/sources/d0_generated_thermal_source_2026-10-22/PRICE_AND_CAUSAL_PULLBACK.md",
    "02_REGISTRY/research/sources/d0_generated_thermal_source_2026-10-22/NATIVE_TANGENT_APPLICATION.md",
    "02_REGISTRY/research/A4D_ORIGINAL_GOLDEN_READY_COHERENT_BOOK_FULL42_BRIDGE_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_original_golden_ready_coherent_book_2026-10-22/check_native_palindrome_compilation.mjs",
    "02_REGISTRY/research/A4D_ORIGINAL_FULL128_BOOK_THERMAL_WARD_OBSTRUCTION_2026_10_22.md",
    "02_REGISTRY/research/A4D_NATIVE_CORRELATED_RETURN_MODULAR_HEAT_COMPATIBILITY_2026_10_22.md",
    "02_REGISTRY/research/A4D_ORIGINAL_FULL128_STATIONARY_PORT_CORRELATION_SOURCE_2026_10_22.md",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md",
    "02_REGISTRY/research/A4D_PRIMARY_FULL128_COMMON_RECORD_INFORMATION_SOURCE_2026_10_20.md",
    "02_REGISTRY/research/A4D_BOOK03_FINITE_ALGEBRAIC_FULL_SOURCE_PUISEUX_GATE_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/published_inputs/A4D_EXACT_FULL42_OPEN_PF_COLLAR_BRANCH_AND_CONTINUOUS_BOOK_RESIDUAL_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/published_inputs/A4D_BOOK03_STAGE_CLOCK_INTERNAL_CUT_NECESSITY_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/published_inputs/check_native_entropy_poisson.mjs",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/published_inputs/A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/README.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/CONCURRENT_INTAKE.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/CUT_SOURCE_EQUIVALENCE.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/check_cut_source_equivalence.py",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/CUT_SOURCE_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/CUT_SOURCE_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/MAXIMUM_ENTROPY_PREPARATION.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/check_maximum_entropy_preparation.py",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/MAXIMUM_ENTROPY_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/MAXIMUM_ENTROPY_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_SOURCE.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/SOURCE_PINS.json",
]

EXACT_FLOAT_KEYS = {
    "eta", "eta_check", "regularization_eta", "smaller_eta_check",
    "independent_value_source_tolerance",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs():
    pin_path = PACKET / "SOURCE_PINS.json"
    pins = json.loads(pin_path.read_text(encoding="utf-8"))
    require(pins["GR_closed"] is False, "Source scope changed")
    rows = pins["owned_inputs"] + pins["frozen_artifacts"]
    declared = [row["path"] for row in rows]
    declared.append(pin_path.relative_to(ROOT).as_posix())
    require(len(declared) == len(set(declared)), "Duplicate frozen input")
    require(len(INPUTS) == len(set(INPUTS)), "Duplicate INPUTS entry")
    require(set(declared) == set(INPUTS), "Frozen manifest and input closure differ")
    for row in rows:
        raw = (ROOT / row["path"]).read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        require(actual == row["sha256"], "Frozen SHA256 changed: " + row["path"])
        if "git_blob" in row:
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            require(blob == row["git_blob"], "Frozen Git blob changed: " + row["path"])
    return {name: sha256(ROOT / name) for name in INPUTS}


def compare(actual, expected, path="receipt"):
    """Compare exact interfaces and explicitly tolerated floating diagnostics."""
    if isinstance(expected, bool) or expected is None or isinstance(expected, str):
        require(type(actual) is type(expected) and actual == expected,
                "Exact value differs: " + path)
    elif isinstance(expected, int):
        require(type(actual) is int and actual == expected,
                "Exact count differs: " + path)
    elif isinstance(expected, float):
        require(type(actual) in (int, float) and math.isfinite(actual),
                "Nonfinite or nonnumeric diagnostic: " + path)
        require(math.isfinite(expected), "Nonfinite expected diagnostic: " + path)
        key = path.rsplit(".", 1)[-1]
        if key in EXACT_FLOAT_KEYS:
            require(actual == expected, "Exact numerical control differs: " + path)
        else:
            atol = 1e-18 if key.endswith("error_bound") else 2e-9
            require(math.isclose(actual, expected, abs_tol=atol, rel_tol=2e-8),
                    "Numerical diagnostic differs: " + path)
    elif isinstance(expected, list):
        require(type(actual) is list and len(actual) == len(expected),
                "List interface differs: " + path)
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, path + "[" + str(index) + "]")
    elif isinstance(expected, dict):
        require(type(actual) is dict and set(actual) == set(expected),
                "Object interface differs: " + path)
        for key in expected:
            compare(actual[key], expected[key], path + "." + key)
    else:
        raise TypeError("Unsupported receipt field: " + path)


def main():
    before = verify_inputs()
    wrapper_before = sha256(Path(__file__))
    jobs = [
        ("check_cut_source_equivalence.py", "CUT_SOURCE_RESULT.json", "checks", 100),
        ("check_maximum_entropy_preparation.py", "MAXIMUM_ENTROPY_RESULT.json", "check_count", 23),
        ("check_complete_history_source.py", "COMPLETE_HISTORY_RESULT.json", "checks_passed", 50),
    ]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # These tiny fixed matrices do not benefit from a large BLAS thread pool.
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    for checker, receipt, count_key, count in jobs:
        flags = ["-B"] + (["-O"] if sys.flags.optimize else [])
        run = subprocess.run(
            [sys.executable, *flags, str(PACKET / checker)],
            cwd=ROOT, env=env, capture_output=True, text=True,
            timeout=180, check=False,
        )
        if run.returncode:
            sys.stdout.write(run.stdout)
            sys.stderr.write(run.stderr)
            raise subprocess.CalledProcessError(run.returncode, run.args)
        require(not run.stderr, "Unexpected checker stderr: " + run.stderr)
        actual = json.loads(run.stdout)
        expected = json.loads((PACKET / receipt).read_text(encoding="utf-8"))
        compare(actual, expected, receipt)
        require(actual[count_key] == count, "Bounded check inventory changed")
        require(actual["GR_closed"] is False, "Physical closure was silently promoted")
        print("PASS " + checker + ": " + str(count) + " scoped checks", flush=True)
    require(verify_inputs() == before, "Replay mutated a frozen input or manifest")
    require(sha256(Path(__file__)) == wrapper_before, "Replay mutated the entrypoint")
    print("PASS 173 bounded checks; exact input provenance; immutable receipts")
    print("SCOPE: actual cut / marginal / complete history; physical Book03 selection and GR remain open.")


if __name__ == "__main__":
    main()
