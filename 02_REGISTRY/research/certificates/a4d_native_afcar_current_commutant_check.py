#!/usr/bin/env python3
"""Portable freshness and scope checker for the AF-CAR commutant result."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant"
PROOF = "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md"
SOURCE_COMMIT = "3e512e599f3cf69571b1cacb63972e5c315d9a2c"
LEAN = "02_REGISTRY/research/certificates/a4d_native_afcar_right_action_no_scalar.lean"
LEAN_OUTPUT = "02_REGISTRY/research/certificates/a4d_native_afcar_right_action_no_scalar_output.txt"
LEAN_RESULTS = "02_REGISTRY/research/certificates/a4d_native_afcar_right_action_no_scalar_results.json"
OUTPUT = BASE + "_output.txt"
INPUTS = [
    PROOF,
    OUTPUT,
    "02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md",
    "02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md",
    "02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json",
    "02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant.py",
    "02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py",
    "02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_check.py",
    "02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_certificate.json",
    "02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation.py",
    "02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation_check.py",
    "02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation_certificate.json",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_check.py",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport_check.py",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport_certificate.json",
    LEAN,
    LEAN_OUTPUT,
    LEAN_RESULTS,
    "03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean",
    "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean",
]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load_program():
    path = ROOT / (BASE + ".py")
    spec = importlib.util.spec_from_file_location("afcar_commutant", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controls():
    source = subprocess.run(
        ["git", "cat-file", "-e", SOURCE_COMMIT + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert source.returncode == 0, "PINNED_SOURCE_COMMIT_MISSING"
    program = load_program()
    result = program.certificate_data()
    assert result["status"] == "PASS", "AF_CAR_COMMUTANT_PROGRAM_FAILED"
    assert result["source_commit"] == SOURCE_COMMIT, "SOURCE_COMMIT_MISMATCH"
    assert result["field"]["polynomial_residue"] == 0, "BAD_MODULAR_ROOT"
    assert result["commutant"]["modular_rank"] == 255, "BAD_MODULAR_RANK"
    assert result["commutant"]["minor_determinant_mod11"] == 6, "BAD_PIVOT_MINOR"
    assert result["commutant"]["complex_dimension"] == 1, "BAD_COMPLEX_COMMUTANT_DIM"
    assert result["controls"]["current_only_commutant_dimension"] == 32
    assert result["controls"]["record_only_commutant_dimension"] == 16
    assert result["controls"]["without_record_step_commutant_dimension"] == 2
    assert result["two_copy_abstract_right_M2_extension_realized"] is True
    assert result["two_copy_commutant_dimension_by_block_argument"] == 4
    assert result["two_copy_AF_path_binding_established"] is False
    af_capacity = result["AF_right_module_capacity"]
    assert af_capacity["old_right_multiplicities"] == [34, 21]
    assert af_capacity["two_copy_slots_required"] == 16
    assert af_capacity["M2_branch_has_capacity"] is True
    assert af_capacity["path_specific_carrier_established"] is False

    lean = json.loads((ROOT / LEAN_RESULTS).read_text())
    assert lean["status"] == "PASS" and lean["compiler_exit_code"] == 0
    assert lean["capsule_sha256"] == sha(LEAN), "LEAN_CAPSULE_STALE"
    assert lean["output_sha256"] == sha(LEAN_OUTPUT), "LEAN_OUTPUT_STALE"
    theorem = "D0.Research.AFCarRightAction.no_unital_matrix_two_ring_hom_to_complex"
    assert theorem in (ROOT / LEAN_OUTPUT).read_text()
    assert set(lean["axioms"][theorem]) <= {"propext", "Classical.choice", "Quot.sound"}
    expected_output = (
        "PASS_A4D_NATIVE_AFCAR_CURRENT_COMMUTANT "
        f"controls={result['exact_controls']} commutant_dim=1 "
        "single_copy=NO_GO two_copy=RIGHT_M2 AF_path_binding=OPEN\n"
    )
    assert (ROOT / OUTPUT).read_text() == expected_output, "OUTPUT_TRANSCRIPT_MISMATCH"

    certificate = {
        **result,
        "program_sha256": sha(BASE + ".py"),
        "checker_sha256": sha(BASE + "_check.py"),
        "input_sha256": {path: sha(path) for path in INPUTS},
        "lean_axioms": lean["axioms"],
        "lean_capsule_sha256": lean["capsule_sha256"],
        "lean_output_sha256": lean["output_sha256"],
    }
    return certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = controls()
    target = ROOT / (BASE + "_certificate.json")
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        stored = json.loads(target.read_text())
        assert stored == result, "AF_CAR_COMMUTANT_CERTIFICATE_STALE"
    print(
        "PASS_A4D_NATIVE_AFCAR_CURRENT_COMMUTANT "
        f"controls={result['exact_controls']} commutant_dim=1 "
        "single_copy=NO_GO two_copy=RIGHT_M2 AF_path_binding=OPEN"
    )


if __name__ == "__main__":
    main()
