#!/usr/bin/env python3
"""Read-only replay of the frozen complete stopped quantum/source application.

Only the two new scoped calculations run. The literal full-label theorem and
the separate port-return native diagnostic retain distinct stopping languages.
Historical source bytes are consumed through declared inputs, never as suites.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22"
INPUTS = [
    "requirements.txt",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
    "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_SOURCE.md",
    "02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/PROOF.md",
    "02_REGISTRY/research/sources/d0_first_match_wald_2026-10-22/SEQUENTIAL_FULL128_BOOK_RETURN.md",
    "02_REGISTRY/research/sources/d0_first_match_wald_2026-10-22/SEQUENTIAL_STATIONARY_OCCUPATION.md",
    "02_REGISTRY/research/sources/d0_first_match_wald_2026-10-22/NATIVE_ACTIVE_LABEL_SUPPORT.md",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_STOPPED_KL_QUANTUM_MEMORY_BUDGET_2026_10_22.md",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md",
    "02_REGISTRY/research/A4D_COMPLETE_NATIVE_FIRST_MATCH_ENTROPIC_POISSON_PREPARATION_AND_HESSIAN_2026_10_22.md",
    "02_REGISTRY/research/A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/continuation_selection/STOPPED_INFORMATION_NORMALIZATION.md",
    "02_REGISTRY/research/A4D_FULL128_NORMALIZATION_AND_TRUE_BOOK_SOURCE_2026_10_21.md",
    "02_REGISTRY/research/sources/d0_full128_normalization_closure_2026-10-21/PROOF.md",
    "02_REGISTRY/research/sources/d0_native_complete_cq_source_2026-10-22/published_inputs/A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_blank_future_entropy_2026-10-22/PROOF.md",
    "02_REGISTRY/research/sources/d0_native_blank_future_entropy_2026-10-22/README.md",
    "02_REGISTRY/research/A4D_NATIVE_STOPPED_QUANTUM_PRICE_AND_SOURCE_2026_10_22.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/README.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/QUANTUM_RETURN_BALANCE.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/STATIONARY_SOURCE_CONSUMER.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/RAW_PARTITION_APPLICATION.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/check_native_quantum_return.py",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/NATIVE_QUANTUM_RETURN_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/NATIVE_IMPLEMENTATION_NOTES.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/check_finite_price_reduction.py",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/FINITE_PRICE_REDUCTION_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/PROVENANCE_CONTINUATION.md",
    "02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/SOURCE_PINS.json"
]

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_inputs():
    path = PACKET / "SOURCE_PINS.json"
    pins = json.loads(path.read_text(encoding="utf-8"))
    require(pins["GR_closed"] is False, "Physical scope changed")
    require(pins["numerical_scope"]["native_checks"] == 223, "Native inventory changed")
    require(pins["numerical_scope"]["rational_integration_checks"] == 168, "Control inventory changed")
    rows = pins["owned_inputs"] + pins["frozen_artifacts"]
    declared = [r["path"] for r in rows] + [path.relative_to(ROOT).as_posix()]
    require(len(declared) == len(set(declared)), "Duplicate manifest entry")
    require(len(INPUTS) == len(set(INPUTS)) and set(INPUTS) == set(declared),
            "Declared replay inputs do not close the frozen manifest")
    for row in rows:
        raw = (ROOT / row["path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row["sha256"],
                "Frozen input changed: " + row["path"])
        if "git_blob" in row:
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            require(blob == row["git_blob"], "Published blob changed: " + row["path"])
    return {name: sha256(ROOT / name) for name in INPUTS}

def main():
    before = verify_inputs()
    wrapper_before = sha256(Path(__file__))
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    for checker, receipt, count in [
        ("check_native_quantum_return.py", "NATIVE_QUANTUM_RETURN_RESULT.json", 223),
        ("check_finite_price_reduction.py", "FINITE_PRICE_REDUCTION_RESULT.json", 168),
    ]:
        # Default checker mode computes, validates its own immutable receipt
        # with declared tolerances, and prints JSON; never use author mode here.
        flags = ["-B"] + (["-O"] if sys.flags.optimize else [])
        run = subprocess.run([sys.executable, *flags, str(PACKET / checker)],
                             cwd=ROOT, env=env, capture_output=True, text=True,
                             timeout=180, check=False)
        if run.returncode:
            sys.stdout.write(run.stdout)
            sys.stderr.write(run.stderr)
            raise subprocess.CalledProcessError(run.returncode, run.args)
        require(not run.stderr, "Unexpected checker stderr: " + run.stderr)
        actual = json.loads(run.stdout)
        expected = json.loads((PACKET / receipt).read_text(encoding="utf-8"))
        require(type(actual["checks_passed"]) is int and actual["checks_passed"] == count,
                "Changed explicit check count: " + checker)
        require(len(actual["checks"]) == count and actual["checks"] == expected["checks"],
                "Changed explicit check inventory: " + checker)
        require(actual["scope"] == expected["scope"] and actual["scope"]["GR_closed"] is False,
                "Changed scientific scope: " + checker)
        require(actual["verification"] == expected["verification"],
                "Changed numerical controls/tolerances: " + checker)
        print("PASS " + checker + ": " + str(count) + " scoped checks", flush=True)
    require(verify_inputs() == before, "Replay mutated a source, artifact or manifest")
    require(sha256(Path(__file__)) == wrapper_before, "Replay mutated its entrypoint")
    print("PASS 391 new bounded checks; exact input provenance; immutable receipts")
    print("SCOPE: port-return native matrix test, generic full-label proof, finite-price/Poisson control; GR remains open.")

if __name__ == "__main__":
    main()
