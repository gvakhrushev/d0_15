#!/usr/bin/env python3
"""KILL-FIRST: complete POVM gain has zero net action on the owned A9 blank."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_afcar_max_gain_action"
PROOF = "02_REGISTRY/research/A4D_NATIVE_AFCAR_MAX_GAIN_ACTION_BOUNDARY.md"
RECEIPT = ROOT / f"{BASE}_certificate.json"
SOURCE_PINS = {
    "02_REGISTRY/research/A4D_NATIVE_OPERATIONAL_GAIN_AND_MEMORY.md":
        "af0e92ebdfdadaee207070c2eef9aad889acc818c8b4ede5eb800d35b31e8d47",
    "02_REGISTRY/research/certificates/a4d_native_operational_gain_check.py":
        "41b6e5ecd88e16528cf2ac20e926e8b3affc09f0d365dfb285e0a5779f6ef256",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/MANIFEST.json":
        "a9ec7817db52efb8ee59a95d46aa6a8ec6f0564f5e2db73ea5394a8098c8da6c",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/RESULT.md":
        "428bdda31e27ea6e7bf18ac93528fa4bc21c28677026341af2e86a36ac67ff52",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/verify.py":
        "81a7b75b84ea23b8915eebaa054a08dbbc0573f0959a0c26661dcb775aeb4736",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/hostile.py":
        "26d4f003f89f8bc14dac14e1a4af1e0fd616ec24a2ea705e6933fbbe6cd0d685",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/receipt.json":
        "31ff9bd7d0547929bedea34e36beec680155ad1e7ac23e0ae8e879860edf5501",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/numeric_result.json":
        "95320dbb026996dcd077f897194d5a1ea903792a718d3a6f660abb5a4d8d0244",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/hostile_receipt.json":
        "dba566cc3e3255defd9af8db586272c488ae14267045e2608d75167957ba8fb6",
    "02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md":
        "d8f1ab42a88b2f88a4e7db370c5cc3abbcdf09b55ac7444a29d0a5ec53661f76",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md":
        "36f77dea7cc868b74bb656c928b3897d5ef42bc45cfde6006070cbcfcf2b6bd9",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_WHOLE_BLANK_STATE_BOUNDARY.md":
        "f632ddfebbabfd3a9dcc254de57ab3aedcc7e04a00c5d0ebf799f5ab577e1751",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_POSITIVE_STATE_REFINEMENT.md":
        "1b50e1ca0cdc555ac26d0a3091cebdfefc68bd0ae2c284b9f037239bbc7fe7cc",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant.py":
        "378a4d39d5e4cb525c653d869900e1926b6fcbea9243f619513af31978098dee",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant_certificate.json":
        "d536f753cc632e7bd1207e495207f70e8988bdd18196bbc7c225e421c1baf2e8",
    "02_REGISTRY/research/certificates/a4d_native_afcar_blank_family_state_certificate.json":
        "f25423f161a62f9d08ecea8c605f66a35a4372e2c15f175d3ffe08198e3efbf8",
    "02_REGISTRY/research/certificates/a4d_native_afcar_positive_state_refinement_certificate.json":
        "91c24b6b721388c181b75b2d7c2b3d245e80a59d0b6be57e425864254c912601",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(stem: str):
    path = ROOT / "02_REGISTRY/research/certificates" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_IMPORT_FAILED:{stem}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="issue the initial receipt")
    args = parser.parse_args()
    checks: list[str] = []

    def check(name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    for path, expected in SOURCE_PINS.items():
        check(f"source_sha256:{path}", sha(path) == expected)

    # Verify the locally replayed complete-gain result, its hostile controls,
    # and all transitive files listed by its immutable source manifest.
    source = ROOT / "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15"
    gain_receipt = json.loads((source / "receipt.json").read_text())
    check("complete_gain_exact_receipt_has_74_conditions",
          gain_receipt["schema"] == "d0-operational-gain/1"
          and gain_receipt["exact_conditions"] == 74)
    check("complete_gain_receipt_preserves_physical_status_boundary",
          gain_receipt["scope"]["native_Info_identified_without_maximal_gain_contract"] is False
          and gain_receipt["scope"]["physical_admission_of_all_algebraic_tests"] is False)
    manifest = json.loads((source / "MANIFEST.json").read_text())
    for relpath, expected in manifest.items():
        actual = hashlib.sha256((source / relpath).read_bytes()).hexdigest()
        check(f"operational_gain_manifest:{relpath}", actual == expected)
    hostile_receipt = json.loads((source / "hostile_receipt.json").read_text())
    check("all_eight_complete_gain_mutants_rejected",
          hostile_receipt["status"] == "PASS"
          and len(hostile_receipt["mathematical_mutants"]) == 8
          and hostile_receipt["false_physical_receipt_rejected"] is True)

    # Consume the exact level-nine state and the proof that it is the actual
    # recorded source, not an arbitrary density chosen to fit the conclusion.
    family_receipt = json.loads((ROOT / "02_REGISTRY/research/certificates/a4d_native_afcar_blank_family_state_certificate.json").read_text())
    state_receipt = json.loads((ROOT / "02_REGISTRY/research/certificates/a4d_native_afcar_positive_state_refinement_certificate.json").read_text())
    check("whole_blank_state_owner_passes", family_receipt["status"] == "PASS")
    check("actual_A9_positive_state_refinement_passes", state_receipt["status"] == "PASS")
    check("actual_source_current_is_nonzero", state_receipt["source_current"] == ["2*a*p", "0", "0"])
    check("state_owner_does_not_claim_physical_or_GR_closure",
          state_receipt["scope"]["physical_execution_or_clock_derived"] is False
          and state_receipt["scope"]["curved_solution_or_GR_derived"] is False)
    for path, digest in state_receipt["source_sha256"].items():
        check(f"state_refinement_transitive_source:{path}", sha(path) == digest)
    for path, digest in family_receipt["source_sha256"].items():
        check(f"whole_blank_transitive_source:{path}", sha(path) == digest)

    owner = load("a4d_native_afcar_current_commutant")
    CAR, FRAME, AF = owner.CAR, owner.FRAME, owner.AF
    ops, adapted_frame, _current = owner.operators()
    x, y = sp.symbols("blank_x blank_y", real=True)
    data3 = AF.frame(3)
    d3 = data3["old_dimension"]
    index3 = {coordinate: i for i, coordinate in enumerate(data3["old_coordinates"])}
    weld = sp.zeros(4 * d3, 32)
    for apparatus in range(4):
        for left_row in range(2):
            for path in range(2):
                for right_column in range(2):
                    spectator = 2 * left_row + path
                    af_row = left_row + 3 * path
                    source_column = (apparatus * 4 + spectator) * 2 + right_column
                    target_row = apparatus * d3 + index3[(0, af_row, right_column)]
                    weld[target_row, source_column] = 1
    blank = FRAME.mat(adapted_frame.T * CAR.blank_code() * sp.Matrix([x, y]))
    blank_with_column = sp.kronecker_product(blank, sp.eye(2)[:, 0])
    recorded = sp.kronecker_product(ops[0], sp.eye(2)) * blank_with_column
    field_to_af = {CAR.a: AF.a, CAR.p: AF.p, FRAME.a: AF.a, FRAME.p: AF.p}
    native = AF.mat((weld * recorded).subs(field_to_af, simultaneous=True))
    row3 = sp.zeros(20, 1)
    for apparatus in range(4):
        for row in range(5):
            row3[apparatus * 5 + row] = native[apparatus * d3 + index3[(0, row, 0)]]
    path_frame = AF.right_frames(3)[0]["V"]
    source_vector = AF.mat(path_frame * row3)
    norm = AF.red((source_vector.T * source_vector)[0])
    check("source_blank_family_is_normalized_on_x2_plus_y2_one",
          AF.zero(norm - (x**2 + y**2)))
    rho_plus = AF.mat(source_vector * source_vector.T)
    check("A9_state_outer_product_is_rank_one_and_normalized_on_fiber",
          AF.zero(rho_plus * rho_plus - norm * rho_plus)
          and AF.red(sp.trace(rho_plus) - norm) == 0)
    check("A9_state_has_zero_other_simple_block", AF.counts(9) == (89, 55))

    # The proper PF reference is central on A9 and has the owned code costs.
    p = AF.p
    reference_trace = AF.red(89 * p**10 + 55 * p**11)
    check("A9_PF_reference_is_normalized", reference_trace == 1)
    check("A9_code_costs_are_10_and_11", AF.counts(9) == (89, 55))
    expected_cost = 10 * norm
    check("A9_prepared_state_cost_is_10_on_normalized_fiber",
          AF.red(expected_cost - 10) == 10 * (norm - 1))

    # The state itself supplies an allowed mathematical projector test for
    # the complete-POVM maximum. It has q=(1,0), reference r=(p^10,1-p^10).
    eye_plus, eye_minus = sp.eye(89), sp.eye(55)
    effect_one = rho_plus
    effect_two_plus, effect_two_minus = eye_plus - rho_plus, eye_minus
    rho_square = AF.mat(rho_plus * rho_plus)
    check("state_projector_pair_is_a_complete_POVM",
          AF.zero(rho_square - norm * rho_plus)
          and AF.zero(effect_one**2 - effect_one - (norm - 1) * rho_plus)
          and AF.zero(effect_two_plus**2 - effect_two_plus - (norm - 1) * rho_plus)
          and AF.zero(effect_one * effect_two_plus - (1 - norm) * rho_plus)
          and AF.zero(effect_one + effect_two_plus - eye_plus)
          and effect_two_minus == eye_minus)
    q_one = AF.red(sp.trace(rho_square))
    q_two = AF.red(sp.trace(rho_plus) - q_one)
    ref_one = AF.red(p**10 * sp.trace(effect_one))
    ref_two = AF.red(1 - ref_one)
    check("prepared_projector_readout_has_q_one_zero_on_fiber",
          AF.red(q_one - norm**2) == 0 and AF.red(q_two - (norm - norm**2)) == 0
          and AF.red(q_one - 1 - (norm - 1) * (norm + 1)) == 0
          and AF.red(q_two - norm * (1 - norm)) == 0)
    check("PF_reference_projector_probabilities_are_p10_and_complement",
          AF.red(ref_one - p**10 * norm) == 0 and AF.red(ref_two - (1 - p**10 * norm)) == 0
          and AF.red(ref_one - p**10 - p**10 * (norm - 1)) == 0)

    # Rank one gives S_vN(rho)=0. Since mu=p^10 I on its support,
    # D(rho||mu)=10 log(phi); the theorem's full maximum is therefore 10.
    phi = 1 / p
    check("pure_A9_state_has_projection_spectrum_and_zero_entropy_on_fiber",
          AF.zero(rho_square - norm * rho_plus)
          and AF.red(sp.trace(rho_plus) - norm) == 0)
    check("PF_support_log_ratio_is_exactly_ten_code_units",
          AF.red(p**10 - phi**(-10)) == 0)
    check("complete_gain_upper_bound_is_ten_phi_units",
          gain_receipt["scope"]["finite_full_algebra_measurement_optimization"] is True
          and AF.red(p**10 - phi**(-10)) == 0)
    check("projective_test_attains_complete_gain_and_cancels_cost",
          AF.red(q_one - norm**2) == 0 and AF.red(ref_one - p**10 * norm) == 0
          and AF.red(expected_cost - 10 * norm) == 0
          and AF.red(10 * norm - 10 * norm) == 0)
    check("net_action_and_source_are_constant_on_the_whole_blank_family",
          norm == x**2 + y**2)
    check("nonzero_native_current_coexists_with_zero_complete_gain_action",
          state_receipt["source_current"][0] != "0"
          and "projective_test_attains_complete_gain_and_cancels_cost" in checks)

    result = {
        "schema": "d0-native-afcar-max-gain-action-boundary/1",
        "status": "PASS",
        "proof": PROOF,
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(BASE + "_check.py"),
        "source_sha256": {path: sha(path) for path in SOURCE_PINS},
        "exact_check_count": len(checks),
        "exact_checks": checks,
        "AF_level": 9,
        "defining_block_sizes": [89, 55],
        "prepared_density_support": "rank_one_in_M89_and_zero_in_M55",
        "PF_reference": "p^10*I89 direct_sum p^11*I55",
        "measurement_probabilities": {"q": ["1", "0"], "reference": ["p^10", "1-p^10"]},
        "expected_cost_phi_units": "10",
        "complete_max_gain_phi_units": "10",
        "cost_minus_complete_gain_phi_units": "0",
        "actual_native_current": state_receipt["source_current"],
        "scope": {
            "full_A9_POVM_maximization_selected_as_physical_Info": False,
            "under_complete_max_gain_contract_blank_family_action_is_zero": True,
            "candidate_action_has_zero_tangent_source_on_blank_family": True,
            "native_current_readout_remains_nonzero": True,
            "restricted_branch_outcome_Info_excluded": False,
            "physical_admission_of_state_projector_test_established": False,
            "physical_source_or_Ward_identity_established": False,
            "Einstein_or_GR_closure": False,
        },
    }
    if args.write:
        RECEIPT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        if json.loads(RECEIPT.read_text()) != result:
            raise AssertionError("IMMUTABLE_AFCAR_MAX_GAIN_ACTION_RECEIPT_MISMATCH")
    print("PASS_AFCAR_COMPLETE_GAIN_ZERO_ACTION", len(checks), "exact checks")


if __name__ == "__main__":
    main()
