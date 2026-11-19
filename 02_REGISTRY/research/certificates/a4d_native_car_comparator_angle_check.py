#!/usr/bin/env python3
"""KILL-FIRST exact test of the direct CAR/v10 projector-pair identification.

This only rejects a common isometric intertwiner of the two existing
two-projector records. It does not reject a non-isometric instrument map,
compression with auxiliary history, or the full D0 core.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_car_comparator_angle"
PROOF = "02_REGISTRY/research/A4D_NATIVE_CAR_COMPARATOR_ANGLE_BOUNDARY.md"
RECEIPT = ROOT / f"{BASE}_certificate.json"
SOURCE_PINS = {
    "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean":
        "6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7",
    "02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md":
        "d85e57979a61972e641eae24442a776133c429c8696d0948590f6d290a60b045",
    "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md":
        "601e5bb9203789a66ad2a945aad30da92b6233ac40417d54c6b47c95dc43536b",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/RESULT.md":
        "92fecc34d44a6bb22a63d09073d861ef0f5accdb866b33d658c80eaa0944832b",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/verify.py":
        "d5660e27d0fe2a6f46472084de30ef197fb7a187ff27c269574032a1dd189491",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def make_record_basis() -> sp.Matrix:
    masks = [
        [0, 2, 4, 8], [1, 3, 5, 9],
        [14, 12, 10, 6], [15, 13, 11, 7],
    ]
    basis = sp.zeros(16)
    for row in range(4):
        for column in range(4):
            sign = -1 if row in (2, 3) and column == 2 else 1
            basis[masks[row][column], 4 * row + column] = sign
    return basis


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="issue the first immutable receipt")
    args = parser.parse_args()

    a, p = sp.symbols("a p", real=True)
    ideal = sp.groebner([a**2 - p, p**2 + p - 1], a, p, domain=sp.QQ)

    def red(value: sp.Expr) -> sp.Expr:
        numerator, denominator = sp.cancel(value).as_numer_denom()
        numerator = ideal.reduce(sp.expand(numerator))[1]
        denominator = ideal.reduce(sp.expand(denominator))[1]
        if denominator == 0:
            raise ZeroDivisionError("golden denominator")
        return sp.cancel(numerator / denominator)

    def zero(matrix: sp.MatrixBase) -> bool:
        return all(red(value) == 0 for value in matrix)

    checks: list[str] = []

    def check(name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    for path, expected in SOURCE_PINS.items():
        check(f"source_sha256:{path}", sha(path) == expected)

    # Actual golden coherent record in the full 16-state CAR/exterior fibre.
    identity4, identity16 = sp.eye(4), sp.eye(16)
    local_gate = sp.Matrix([
        [a, -p, 0, 0], [p, a, 0, 0],
        [0, 0, a, -p], [0, 0, -p, -a],
    ])
    local_cut = sp.diag(1, 0, 1, 0)
    basis = make_record_basis()
    car_gate = basis * sp.kronecker_product(local_gate, identity4) * basis.T
    car_cut = basis * sp.kronecker_product(local_cut, identity4) * basis.T
    car_return_cut = car_gate.T * car_cut * car_gate
    car_pair_invariant = (car_cut + car_return_cut - identity16) ** 2
    check("CAR_fullstep_uses_owned_golden_relations", zero(local_gate.T * local_gate - identity4))
    check("CAR_record_basis_is_signed_orthogonal", basis.T * basis == identity16)
    check("CAR_cut_is_projection", car_cut * car_cut == car_cut)
    check("CAR_transported_cut_is_projection", zero(car_return_cut**2 - car_return_cut))
    check("CAR_two_projector_angle_operator_is_p_identity",
          zero(car_pair_invariant - p * identity16))
    check("CAR_compressed_pair_relation_PQP_equals_pP",
          zero(car_cut * car_return_cut * car_cut - p * car_cut))
    complement_cut = identity16 - car_cut
    check("CAR_same_outcome_repeats_with_probability_p_on_both_cuts",
          zero(car_cut * car_gate.T * car_cut * car_gate * car_cut - p * car_cut)
          and zero(complement_cut * car_gate.T * complement_cut * car_gate * complement_cut
                   - p * complement_cut))

    # Existing v10 comparator projectors and its exact loop-energy operator.
    rotation = sp.diag(
        sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]]),
        sp.Matrix([[sp.Rational(5, 13), -sp.Rational(12, 13)],
                   [sp.Rational(12, 13), sp.Rational(5, 13)]]),
        sp.eye(2),
    )
    identity6 = sp.eye(6)
    comparator_cut = sp.diag(1, 0, 1, 0, 0, 0)
    comparator_return_cut = rotation.T * comparator_cut * rotation
    comparator_pair_invariant = sp.simplify(
        (comparator_cut + comparator_return_cut - identity6) ** 2
    )
    expected_spectrum_matrix = sp.diag(
        sp.Rational(9, 25), sp.Rational(9, 25),
        sp.Rational(25, 169), sp.Rational(25, 169), 1, 1,
    )
    check("v10_projectors_are_exactly_the_pinned_pair",
          comparator_cut**2 == comparator_cut and
          comparator_return_cut**2 == comparator_return_cut)
    check("v10_pair_invariant_exact_diagonal", comparator_pair_invariant == expected_spectrum_matrix)
    expected_compressed_pair = sp.diag(
        sp.Rational(9, 25), 0, sp.Rational(25, 169), 0, 0, 0,
    )
    check("v10_compressed_pair_exact_diagonal",
          comparator_cut * comparator_return_cut * comparator_cut == expected_compressed_pair)
    check("sharp_to_sharp_UCP_pair_map_is_impossible",
          not zero(expected_compressed_pair - p * comparator_cut))

    # Test the induced repeated-direct histories, beyond sharp projector-pair
    # equivalence. The actual v10 direct Kraus operator is C0.
    loop = -(2 * comparator_cut - identity6) * (2 * comparator_return_cut - identity6)
    comparator_direct = p * identity6 + p**2 * loop
    comparator_direct_effect = (comparator_direct.T * comparator_direct).applyfunc(red)
    expected_direct_effect = sp.diag(
        1 - 4 * p**3 * sp.Rational(9, 25),
        1 - 4 * p**3 * sp.Rational(9, 25),
        1 - 4 * p**3 * sp.Rational(25, 169),
        1 - 4 * p**3 * sp.Rational(25, 169),
        1 - 4 * p**3, 1 - 4 * p**3,
    ).applyfunc(red)
    check("v10_direct_effect_exact_spectrum", comparator_direct_effect == expected_direct_effect)
    check("v10_direct_kraus_is_normal",
          zero(comparator_direct.T * comparator_direct
               - comparator_direct * comparator_direct.T))
    candidate_p = [sp.Rational(61, 97), sp.Rational(269, 369), sp.Rational(5, 9)]
    candidate_residuals = [sp.factor(x**2 + x - 1) for x in candidate_p]
    check("v10_direct_effect_has_no_eigenvalue_p",
          all(value != 0 for value in candidate_residuals)
          and all(red(lam - p) != 0 for lam in expected_direct_effect.diagonal()))
    check("v10_pair_invariant_has_three_distinct_eigenvalues",
          comparator_pair_invariant.eigenvals() == {
              sp.Rational(9, 25): 2, sp.Rational(25, 169): 2, sp.Integer(1): 2,
          })
    check("v10_pair_is_not_a_projection",
          comparator_pair_invariant**2 != comparator_pair_invariant)

    # A common unitary/isometric intertwiner must preserve the spectrum of
    # (P+Q-I)^2. The v10 rational eigenvalues cannot equal the golden p.
    rational_eigenvalues = [sp.Rational(9, 25), sp.Rational(25, 169), sp.Integer(1)]
    residuals = [sp.factor(value**2 + value - 1) for value in rational_eigenvalues]
    check("no_v10_angle_is_a_golden_root", all(value != 0 for value in residuals))
    check("CAR_and_v10_pair_characteristic_polynomials_differ",
          sp.expand((sp.Symbol("x") - p)**16) != sp.expand(
              (sp.Symbol("x") - sp.Rational(9, 25))**2
              * (sp.Symbol("x") - sp.Rational(25, 169))**2
              * (sp.Symbol("x") - 1)**2
          ))

    result = {
        "schema": "d0-native-car-comparator-angle-boundary/1",
        "status": "PASS",
        "proof": PROOF,
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(BASE + "_check.py"),
        "source_sha256": {path: sha(path) for path in SOURCE_PINS},
        "exact_checks": checks,
        "exact_check_count": len(checks),
        "car_pair_invariant_spectrum": {"p": 16},
        "v10_pair_invariant_spectrum": {"9/25": 2, "25/169": 2, "1": 2},
        "car_PQP_relation": "PQP=pP",
        "v10_PcPrPc_diagonal": ["9/25", "0", "25/169", "0", "0", "0"],
        "sharp_to_sharp_unital_CP_pair_map": "IMPOSSIBLE_BY_MULTIPLICATIVE_DOMAIN",
        "v10_direct_effect_spectrum": {
            "1-36*p^3/25": 2,
            "1-100*p^3/169": 2,
            "1-4*p^3": 2,
        },
        "rational_candidates_if_direct_effect_eigenvalue_equals_p": [str(x) for x in candidate_p],
        "minimal_polynomial_residuals": [str(x) for x in candidate_residuals],
        "history_intertwiner_preserving_repeated_direct_words": "IMPOSSIBLE",
        "v10_golden_polynomial_residuals": {
            "9/25": str(residuals[0]),
            "25/169": str(residuals[1]),
            "1": str(residuals[2]),
        },
        "scope": {
            "direct_common_isometric_pair_intertwiner_exists": False,
            "nonisometric_instrument_map_excluded": False,
            "history_auxiliary_compression_excluded": False,
            "all_native_preparations_excluded": False,
            "new_physical_action_or_selector": False,
            "physical_Cost_minus_Info_binding_proved": False,
            "source_or_Ward_identity_proved": False,
            "Einstein_or_GR_closure": False,
        },
    }

    if args.write:
        RECEIPT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        expected = json.loads(RECEIPT.read_text())
        if expected != result:
            raise AssertionError("IMMUTABLE_CAR_COMPARATOR_ANGLE_RECEIPT_MISMATCH")
    print("PASS_CAR_COMPARATOR_ANGLE_BOUNDARY", len(checks), "exact checks")


if __name__ == "__main__":
    main()
