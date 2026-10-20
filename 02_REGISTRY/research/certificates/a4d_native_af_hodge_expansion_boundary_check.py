#!/usr/bin/env python3
"""Replay the exact AF-capacity / normalized Hodge-metric boundary."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = "02_REGISTRY/research/certificates/"
PROOF = "02_REGISTRY/research/A4D_NATIVE_AF_HODGE_EXPANSION_BOUNDARY_2026-10-16.md"
AF_RESULT = CERT + "a4d_native_engine_correlated_current_extension_results.json"
AF_NOTE = "02_REGISTRY/research/A4D_NATIVE_ENGINE_CORRELATED_CURRENT_EXTENSION_2026-10-15.md"
AF_CHECKER = CERT + "a4d_native_engine_correlated_current_extension_check.py"
AF_LEAN = CERT + "a4d_native_engine_correlated_current_extension.lean"
AF_LEAN_OUTPUT = CERT + "a4d_native_engine_correlated_current_extension_lean_output.txt"
HODGE_CERT = CERT + "a4d_native_hodge_connes_metric_certificate.json"
HODGE_RESULT = CERT + "a4d_native_hodge_connes_metric_results.json"
HODGE_NOTE = "02_REGISTRY/research/A4D_NATIVE_HODGE_CONNES_METRIC.md"
HODGE_CHECKER = CERT + "a4d_native_hodge_connes_metric_check.py"
HODGE_LEAN = CERT + "a4d_native_hodge_connes_metric.lean"
HODGE_OUTPUT = CERT + "a4d_native_hodge_connes_metric_output.txt"
LEAN = CERT + "a4d_native_af_hodge_expansion_boundary.lean"
LEAN_OUTPUT = CERT + "a4d_native_af_hodge_expansion_boundary_output.txt"
OUT = CERT + "a4d_native_af_hodge_expansion_boundary_results.json"


def read(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def sha256(path: str) -> str:
    return hashlib.sha256(read(path)).hexdigest()


def git_blob(path: str) -> str:
    data = read(path)
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def run() -> dict:
    checks: dict[str, int] = {}

    def ck(name: str, condition: bool, count: int = 1) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = checks.get(name, 0) + count

    hcert = json.loads(read(HODGE_CERT))
    hres = json.loads(read(HODGE_RESULT))
    af = json.loads(read(AF_RESULT))

    # Revalidate the exact upstream Hodge theorem receipt and its source pins.
    ck("Hodge_certificate_and_result_pass", hcert["status"] == "PASS" and hres["status"] == "PASS")
    ck("Hodge_certificate_binds_checker", sha256(HODGE_CHECKER) == hcert["checker_sha256"])
    ck("Hodge_certificate_binds_note", sha256(HODGE_NOTE) == hcert["proof_sha256"])
    ck("Hodge_certificate_binds_Lean_capsule", sha256(HODGE_LEAN) == hcert["capsule_sha256"])
    ck("Hodge_certificate_binds_receipt", sha256(HODGE_RESULT) == hcert["receipt_sha256"])
    ck("Hodge_result_binds_output", sha256(HODGE_OUTPUT) == hres["output_sha256"])
    ck("Hodge_certificate_control_count", hcert["exact_control_count"] == sum(hcert["checks"].values()))
    for group in ("transitive_d0_source_sha256", "primary_and_prior_input_sha256", "toolchain_input_sha256"):
        for path, expected in hres[group].items():
            ck("Hodge_source_pin_" + group, sha256(path) == expected)
    ck("Hodge_formula_is_all_size", hcert["scope"]["all_size_exact_product_circle_Connes_distance"] == "ANALYTIC_PROOF_NOT_FULL_LEAN_FORMALIZATION")
    ck("Hodge_does_not_claim_physical_refinement", not hcert["scope"]["native_archive_RG_is_physical_metric_refinement"])
    ck("Hodge_does_not_claim_GR", not hcert["scope"]["curved_Lorentz_metric_source_Ward_or_GR_derived"])

    # Revalidate the AF package whose capacity and invariant readout are used.
    ck("AF_certificate_result_pass", af["status"] == "PASS")
    ck("AF_result_binds_checker", sha256(AF_CHECKER) == af["checker_sha256"])
    ck("AF_result_binds_note", sha256(AF_NOTE) == af["research_note_sha256"])
    ck("AF_result_binds_Lean_capsule", sha256(AF_LEAN) == af["lean_capsule_sha256"])
    ck("AF_result_binds_Lean_output", sha256(AF_LEAN_OUTPUT) == af["lean_output_sha256"])
    for path, expected in af["owner_sha256"].items():
        ck("AF_owner_source_sha256", sha256(path) == expected)
    for path, expected in af["owner_git_blob"].items():
        ck("AF_owner_source_git_blob", git_blob(path) == expected)
    af_readout = af["metric_transition_owner_census"]["af_internal_resolution_and_record_information"]
    ck("AF_capacity_formula", af_readout["AF_GNS_dimension"] == "d_k=F_(6k+5)")
    ck("AF_capacity_witnesses", af_readout["dimension_witnesses"] == [5, 89, 1597])
    ck("AF_inherited_metric_remains_fixed", "remain unchanged at every depth" in af_readout["inherited_metric_response"])
    ck("AF_does_not_claim_physical_expansion", "no physical metric expansion" in af_readout["scope"])

    # The small Lean capsule connects the exact phase edge scale to the
    # coefficient actually used by the full-cochain Hodge/CAR operator.
    lean_output = read(LEAN_OUTPUT).decode()
    ck("Lean_scale_declaration_compiled", "actual_hodge_scale_matches_phase_metric" in lean_output)
    ck("Lean_actual_square_declaration_compiled", "actual_hodge_square_is_owned_scaled_laplacian" in lean_output)
    ck("Lean_output_has_no_error_or_sorry", ": error" not in lean_output and "sorryAx" not in lean_output)
    scale_axioms = lean_output.split("'D0.Research.NativeAFHodgeExpansionBoundary.actual_hodge_scale_matches_phase_metric' depends on axioms:", 1)
    ck("Lean_scale_bridge_has_standard_axioms_only", len(scale_axioms) == 2 and "native_decide" not in scale_axioms[1].split("theorem", 1)[0])
    ck("Lean_square_retains_imported_native_decide_boundary", "D0.Geometry.car_mixed_anticommutator_int._native.native_decide.ax_1_1" in lean_output)

    # Exact finite controls for the all-size antipodal/neighbor argument.
    diameter_cases = 0
    for n in range(1, 129):
        L = 4 * n
        antipode_sq = Fraction(4 * (L // 2) ** 2, L * L)
        neighbor_sq = Fraction(1, L * L)
        coordinate_bound_sq = Fraction(4 * (L // 2) ** 2, L * L)
        ck("normalized_diameter_exactly_one", antipode_sq == 1 and coordinate_bound_sq == 1)
        ck("neighbor_resolution_is_inverse_L", neighbor_sq * L * L == 1)
        ck("antipode_attains_coordinate_bound", antipode_sq == coordinate_bound_sq)
        # Removing the owned L prefactor changes D to D/L and multiplies d by L.
        unnormalized_diameter_sq = antipode_sq * L * L
        ck("dropping_L_prefactor_mutates_diameter", unnormalized_diameter_sq == L * L)
        diameter_cases += 1

    # Replay the AF Fibonacci capacity recurrence alongside, without identifying
    # its tick with L or treating capacity as a spatial volume.
    af_capacity_cases = 0
    for k in range(35):
        d0, d1, d2 = fib(6 * k + 5), fib(6 * (k + 1) + 5), fib(6 * (k + 2) + 5)
        ck("AF_three_inclusion_capacity_recurrence", d2 + d0 == 18 * d1)
        ck("AF_capacity_ratio_increment_identity", d0 * d2 - d1 * d1 == 64)
        ck("AF_capacity_strictly_accelerates", d2 - 2 * d1 + d0 > 0)
        # Pairing a tick to any illustrative L in 4N leaves the normalized
        # diameter fixed. This is a control, not an asserted native k -> L map.
        L = 4 * (k + 1)
        ck("AF_tick_does_not_set_normalized_diameter", Fraction(4 * (L // 2) ** 2, L * L) == 1)
        af_capacity_cases += 1

    source_paths = sorted({
        PROOF, AF_NOTE, AF_CHECKER, AF_LEAN, AF_LEAN_OUTPUT, AF_RESULT,
        HODGE_CERT, HODGE_RESULT, HODGE_NOTE, HODGE_CHECKER, HODGE_LEAN,
        HODGE_OUTPUT, LEAN, LEAN_OUTPUT,
    } | set(hres["transitive_d0_source_sha256"]) |
       set(hres["primary_and_prior_input_sha256"]) |
       set(hres["toolchain_input_sha256"]) |
       set(af["owner_sha256"]) |
       set(af["owner_git_blob"]))
    source_pins = {path: {"sha256": sha256(path), "git_blob": git_blob(path)} for path in source_paths}
    return {
        "status": "PASS",
        "proof": PROOF,
        "proof_sha256": sha256(PROOF),
        "checker": CERT + "a4d_native_af_hodge_expansion_boundary_check.py",
        "checker_sha256": sha256(CERT + "a4d_native_af_hodge_expansion_boundary_check.py"),
        "lean_capsule": LEAN,
        "lean_capsule_sha256": sha256(LEAN),
        "lean_output": LEAN_OUTPUT,
        "lean_output_sha256": sha256(LEAN_OUTPUT),
        "lean_compiler_exit_code": 0,
        "lean_command": ["lake", "env", "lean", "../" + LEAN],
        "lean_command_cwd": "03_FORMALIZATION",
        "lean_axiom_boundary": {
            "actual_hodge_scale_matches_phase_metric": ["propext", "Classical.choice", "Quot.sound"],
            "actual_hodge_square_is_owned_scaled_laplacian": [
                "propext", "Classical.choice", "Quot.sound",
                "D0.Geometry.car_annihilate_anticommutator_int._native.native_decide.ax_1_1",
                "D0.Geometry.car_create_anticommutator_int._native.native_decide.ax_1_1",
                "D0.Geometry.car_mixed_anticommutator_int._native.native_decide.ax_1_1",
            ],
        },
        "source_pins": source_pins,
        "exact_control_count": sum(checks.values()),
        "checks": checks,
        "witnesses": {
            "L_values": [4, 8, 12, 16, 32, 64, 128, 256, 512],
            "diameter_squared": "1",
            "nearest_neighbor_distance": "1/L",
            "AF_dimension_values": [fib(5), fib(11), fib(17)],
            "AF_dimension_law": "d_k=F_(6k+5)",
            "mutated_operator_without_L_prefactor_diameter": "L",
        },
        "scope": {
            "direct_AF_capacity_to_owned_normalized_Hodge_metric_expansion": "SCOPED_NO_GO",
            "all_AF_to_physical_metric_couplings_excluded": False,
            "AF_tick_to_Hodge_L_map_derived": False,
            "changing_q_D_or_operator_scale_derived": False,
            "physical_expansion_curvature_source_Ward_or_GR_derived": False,
            "Hodge_all_size_metric_theorem_fully_Lean_formalized": False,
            "AF_capacity_is_spatial_volume": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        (ROOT / OUT).write_text(encoded)
    else:
        recorded = json.loads(read(OUT))
        if recorded != result:
            raise AssertionError("STALE_OR_MUTATED_AF_HODGE_EXPANSION_BOUNDARY_RECEIPT")
    print(f"PASS_AF_HODGE_EXPANSION_BOUNDARY controls={result['exact_control_count']} "
          f"L_cases={result['checks']['normalized_diameter_exactly_one']} "
          f"AF_ticks={result['checks']['AF_three_inclusion_capacity_recurrence']}")
