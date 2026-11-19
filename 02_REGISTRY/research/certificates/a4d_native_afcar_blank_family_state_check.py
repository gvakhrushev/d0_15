#!/usr/bin/env python3
"""Exact whole-blank-family test for the owned level-three AF/CAR weld."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_afcar_blank_family_state"
PROOF = "02_REGISTRY/research/A4D_NATIVE_AFCAR_WHOLE_BLANK_STATE_BOUNDARY.md"
RECEIPT = ROOT / f"{BASE}_certificate.json"
SOURCE_PINS = {
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md":
        "36f77dea7cc868b74bb656c928b3897d5ef42bc45cfde6006070cbcfcf2b6bd9",
    "02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md":
        "040f26ba81a25959add549d01fb592c19bf102e6081e32e5b64a7102ab6fdc0c",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant.py":
        "378a4d39d5e4cb525c653d869900e1926b6fcbea9243f619513af31978098dee",
    "02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py":
        "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    "02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation.py":
        "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load_afcar_module():
    path = ROOT / "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant.py"
    spec = importlib.util.spec_from_file_location("d0_afcar_blank_family_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("AF_CAR_OWNER_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def interval_add(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return x[0] + y[0], x[1] + y[1]


def interval_mul(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    candidates = [x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1]]
    return min(candidates), max(candidates)


def interval_scale(c: F, x: tuple[F, F]) -> tuple[F, F]:
    return interval_mul((c, c), x)


def interval_expr(terms: list[tuple[F, tuple[F, F]]]) -> tuple[F, F]:
    out = (F(0), F(0))
    for coefficient, interval in terms:
        out = interval_add(out, interval_scale(coefficient, interval))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="issue the first immutable receipt")
    args = parser.parse_args()

    owner = load_afcar_module()
    CAR, FRAME, AF, JONES = owner.CAR, owner.FRAME, owner.AF, owner.JONES
    p, a = AF.p, AF.a
    x, y = sp.symbols("blank_x blank_y", real=True)
    checks: list[str] = []

    def check(name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    for path, expected in SOURCE_PINS.items():
        check(f"source_sha256:{path}", sha(path) == expected)

    # Reconstruct the exact existing same-simple level-three path weld.
    ops, adapted_frame, _ = owner.operators()
    data = AF.frame(3)
    d = data["old_dimension"]
    coordinates = data["old_coordinates"]
    index = {coordinate: i for i, coordinate in enumerate(coordinates)}
    weld = sp.zeros(4 * d, 32)
    for apparatus in range(4):
        for left_row in range(2):
            for path in range(2):
                for right_column in range(2):
                    spectator = 2 * left_row + path
                    af_row = left_row + 3 * path
                    source = (apparatus * 4 + spectator) * 2 + right_column
                    target = apparatus * d + index[(0, af_row, right_column)]
                    weld[target, source] = 1
    check("existing_level3_weld_isometry", weld.T * weld == sp.eye(32))

    blank = FRAME.mat(adapted_frame.T * CAR.blank_code() * sp.Matrix([x, y]))
    blank_with_column = sp.kronecker_product(blank, sp.eye(2)[:, 0])
    mapped_blank = weld * blank_with_column
    expected_blank = sp.zeros(4 * d, 1)
    expected_blank[index[(0, 0, 0)]] = x
    expected_blank[2 * d + index[(0, 3, 0)]] = y
    check("entire_existing_blank_family_binds_to_AF_path_pair",
          FRAME.C.zero(mapped_blank - expected_blank))
    check("blank_family_normalization_is_x2_plus_y2",
          FRAME.C.zero(blank.T * blank - sp.Matrix([[x**2 + y**2]])))

    recorded = sp.kronecker_product(ops[0], sp.eye(2)) * blank_with_column
    field_to_af = {CAR.a: AF.a, CAR.p: AF.p, FRAME.a: AF.a, FRAME.p: AF.p}
    native = AF.mat((weld * recorded).subs(field_to_af, simultaneous=True))
    row3 = sp.zeros(20, 1)
    for apparatus in range(4):
        for row in range(5):
            row3[apparatus * 5 + row] = native[apparatus * d + index[(0, row, 0)]]
    path_frame = AF.right_frames(3)[0]["V"]
    source_row = AF.mat(path_frame * row3)
    jones_frames = [
        AF.mat(frame.subs({JONES.E.a: AF.a, JONES.E.p: AF.p}, simultaneous=True))
        for frame in JONES.corner_frames(3)
    ]
    canonical_corner = AF.mat(jones_frames[0] * jones_frames[0].T)
    outside_corner = sp.eye(89) - canonical_corner
    check("source_path_frame_and_canonical_corner_have_owned_dimensions",
          path_frame.shape == (89, 20) and canonical_corner.shape == (89, 89))
    check("source_norm_is_preserved_for_all_x_y",
          AF.zero(source_row.T * source_row - sp.Matrix([[x**2 + y**2]])))

    gram = sp.Matrix([
        [AF.red((source_row.subs({x: 1, y: 0}).T * outside_corner
                 * source_row.subs({x: 1, y: 0}))[0]),
         AF.red((source_row.subs({x: 1, y: 0}).T * outside_corner
                 * source_row.subs({x: 0, y: 1}))[0])],
        [AF.red((source_row.subs({x: 0, y: 1}).T * outside_corner
                 * source_row.subs({x: 1, y: 0}))[0]),
         AF.red((source_row.subs({x: 0, y: 1}).T * outside_corner
                 * source_row.subs({x: 0, y: 1}))[0])],
    ])
    expected_gram = sp.Matrix([
        [8 * sp.sqrt(2) * a * p + 16 * a * p - 10 * a - 5 * sp.sqrt(2) * a
         - 5 * sp.sqrt(2) * p + sp.Rational(27, 2) * p - sp.Rational(15, 2)
         + 3 * sp.sqrt(2), 0],
        [0, -26 * a * p - 8 * sp.sqrt(2) * a * p + 5 * sp.sqrt(2) * a
         + 16 * a - sp.Rational(49, 2) * p + 5 * sp.sqrt(2) * p
         - 3 * sp.sqrt(2) + 16],
    ])
    check("whole_blank_off_corner_gram_exact", gram == expected_gram)
    check("whole_blank_off_corner_cross_term_vanishes", gram[0, 1] == 0 and gram[1, 0] == 0)

    p_iv = (F("0.6180339887498948"), F("0.6180339887498950"))
    a_iv = (F("0.78615137775742"), F("0.78615137775743"))
    r2_iv = (F("1.41421356237309"), F("1.41421356237310"))
    check("rational_interval_p_brackets_positive_golden_root",
          p_iv[0]**2 + p_iv[0] - 1 < 0 < p_iv[1]**2 + p_iv[1] - 1)
    check("rational_interval_a_brackets_sqrt_p",
          a_iv[0]**2 < p_iv[0] and a_iv[1]**2 > p_iv[1])
    check("rational_interval_sqrt2_is_outward",
          r2_iv[0]**2 < 2 < r2_iv[1]**2)
    ap_iv = interval_mul(a_iv, p_iv)
    sqrt2a_iv = interval_mul(r2_iv, a_iv)
    sqrt2p_iv = interval_mul(r2_iv, p_iv)
    sqrt2ap_iv = interval_mul(r2_iv, ap_iv)
    m_x_iv = interval_expr([
        (F(8), sqrt2ap_iv), (F(16), ap_iv), (F(-10), a_iv),
        (F(-5), sqrt2a_iv), (F(-5), sqrt2p_iv),
        (F(27, 2), p_iv), (F(-15, 2), (F(1), F(1))), (F(3), r2_iv),
    ])
    m_y_iv = interval_expr([
        (F(-26), ap_iv), (F(-8), sqrt2ap_iv), (F(5), sqrt2a_iv),
        (F(16), a_iv), (F(-49, 2), p_iv), (F(5), sqrt2p_iv),
        (F(-3), r2_iv), (F(16), (F(1), F(1))),
    ])
    check("first_blank_direction_off_corner_weight_in_0_5663_0_5664",
          F(5663, 10000) < m_x_iv[0] <= m_x_iv[1] < F(5664, 10000))
    check("second_blank_direction_off_corner_weight_in_0_9934_0_9936",
          F(9934, 10000) < m_y_iv[0] <= m_y_iv[1] < F(9936, 10000))

    result = {
        "schema": "d0-native-afcar-blank-family-state-boundary/1",
        "status": "PASS",
        "proof": PROOF,
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(BASE + "_check.py"),
        "source_sha256": {path: sha(path) for path in SOURCE_PINS},
        "exact_check_count": len(checks),
        "exact_checks": checks,
        "off_corner_gram": [[str(gram[i, j]) for j in range(2)] for i in range(2)],
        "off_corner_weight_bounds": {
            "x_direction": ["5663/10000", "5664/10000"],
            "y_direction": ["9934/10000", "9936/10000"],
            "all_normalized_blank_states_lower_bound": "5663/10000",
        },
        "scope": {
            "fixed_level3_same_simple_path_canonical_state_match_exists": False,
            "all_states_in_existing_real_whole_blank_family_match": False,
            "different_AF_path_identification_excluded": False,
            "other_native_preparation_families_excluded": False,
            "physical_admission_established": False,
            "metric_source_or_Ward_identity_established": False,
            "curved_solution_or_GR_established": False,
        },
    }
    if args.write:
        RECEIPT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        if json.loads(RECEIPT.read_text()) != result:
            raise AssertionError("IMMUTABLE_AFCAR_BLANK_FAMILY_RECEIPT_MISMATCH")
    print("PASS_AFCAR_WHOLE_BLANK_FAMILY", len(checks), "exact and interval checks")


if __name__ == "__main__":
    main()
