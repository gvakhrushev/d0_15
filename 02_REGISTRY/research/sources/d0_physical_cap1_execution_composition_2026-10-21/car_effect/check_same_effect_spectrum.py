#!/usr/bin/env python3
"""Exact full-angle same-z effect-spectrum test for cap-one versus two-step CAR."""
import hashlib
import argparse
import json
from math import comb
from pathlib import Path
import subprocess
import sys

import sympy as s

ROOT = Path(__file__).resolve().parents[5]
PKG = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
INPUT = "92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be"
checks = []


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)
    checks.append(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(
        ["git", f"--work-tree={ROOT}", *args], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout


def main():
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    require(pins["input_commit"] == INPUT, "same_source_snapshot")
    for row in pins["sources"]:
        source = git("show", f"{INPUT}:{row['path']}")
        require(sha(source) == row["sha256"], "source_sha:" + row["path"])
        blob = git("rev-parse", f"{INPUT}:{row['path']}").decode().strip()
        require(blob == row["git_blob"], "source_blob:" + row["path"])
        require((ROOT / row["path"]).read_bytes() == source,
                "working_source_matches_pin:" + row["path"])

    chronology_path = ROOT / "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md"
    chronology = chronology_path.read_bytes()
    chronology_receipt = json.loads((ROOT / (
        "02_REGISTRY/research/certificates/"
        "a4d_native_record_metric_chronology_certificate.json"
    )).read_text())
    require(chronology_receipt["status"] == "PASS", "consumed_car_receipt_status")
    require(chronology_receipt["exact_controls"] == 469, "consumed_car_receipt_control_count")
    require(chronology_receipt["proof_sha256"] == sha(chronology),
            "consumed_car_receipt_proof_hash")
    chronology_checker = ROOT / (
        "02_REGISTRY/research/certificates/"
        "a4d_native_record_metric_chronology_check.py"
    )
    require(chronology_receipt["checker_sha256"] == sha(chronology_checker.read_bytes()),
            "consumed_car_receipt_checker_hash")
    require(chronology_receipt["scope"]["price_readout"] == "ORIGINAL_P_ON_BOTH_SIDES",
            "consumed_car_original_readout_scope")
    require(chronology_receipt["full_native_fibre"] == 16,
            "consumed_car_full16_scope")

    query_script = PKG / "moving_query/check_native_query_value_and_jet.py"
    query_proc = subprocess.run(
        [sys.executable, str(query_script)], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    query = json.loads(query_proc.stdout)
    require(query["status"] == "PASS", "cap_one_query_checker_status")
    require("actual retained plus/minus feedback eigenvalues" in query["checks"],
            "cap_one_query_eigenvalue_control_present")

    a = s.symbols("a", positive=True)
    p = a**2
    reduce = lambda x: s.rem(
        s.Poly(s.expand(x), a), s.Poly(a**4 + a**2 - 1, a)
    ).as_expr().expand()
    z = s.Rational(1, 2**20)
    zvar = s.symbols("zvar", real=True)
    c = s.Integer(1)
    L = 4 * p**3
    M = L * (1 + p**6)

    # Check the aligned c=1 determinant anchor from equation (8).
    ell = p**2 * (1 + c) * (1 + p**3 * c)
    tr = 2 * (p**2 + p**5 * c**2)
    det = p**4 * (1 - c**2) ** 2
    tr0 = 2 * (1 - c) * (
        2 * p**4 * c**3 + 2 * p * c**2 + (3 * p - 1) * c + p**2
    )
    det0 = (1 - c) ** 2 * (5 * p**4 * c**2 + (14 * p - 8) * c + p**4)
    Avar = 1 - zvar * ell
    Bvar = 1 - zvar * tr + zvar**2 * det
    Cvar = 1 - zvar * tr0 + zvar**2 * det0
    car_determinant = Avar**2 * Bvar**2 * Cvar
    require(reduce(car_determinant - (1 - zvar * L) ** 4) == 0,
            "car_aligned_full16_pencil")
    require(reduce(ell - L) == 0 and reduce(tr - L) == 0,
            "car_aligned_active_blocks_have_value_L")
    require(reduce(det) == 0 and reduce(tr0) == 0 and reduce(det0) == 0,
            "car_aligned_remaining_blocks_are_zero")

    # Uniform spectral bound over the full native observer-angle domain.
    p0 = (s.sqrt(5) - 1) / 2
    L0 = 4 * p0**3
    c0, x0 = s.symbols("c0 x0", real=True)
    ell0 = p0**2 * (1 + c0) * (1 + p0**3 * c0)
    t_all = 2 * (p0**2 + p0**5 * c0**2)
    d_all = p0**4 * (1 - c0**2) ** 2
    t0_all = 2 * (1 - c0) * (
        2 * p0**4 * c0**3 + 2 * p0 * c0**2 + (3 * p0 - 1) * c0 + p0**2
    )
    d0_all = (1 - c0) ** 2 * (
        5 * p0**4 * c0**2 + (14 * p0 - 8) * c0 + p0**4
    )
    require(s.simplify(
        L0 - ell0 - p0**2 * (1 - c0) * (1 + p0**3 * (2 + c0))
    ) == 0, "all_angle_ell_lies_below_L")
    require(s.simplify(
        L0 - t_all - 2 * p0**5 * (1 - c0**2)
    ) == 0, "all_angle_repeated_block_trace_below_L")
    require(s.simplify(t_all.subs(c0, 1) - L0) == 0,
            "repeated_block_trace_endpoint_normalization")

    qpoly = s.Poly(s.expand((2 * L0 - t0_all).subs(c0, 2 * x0 - 1)), x0)
    require(qpoly.degree() == 4, "observer_trace_gap_degree_four")
    power_coefficients = [qpoly.nth(i) for i in range(5)]
    bernstein = [s.simplify(sum(
        power_coefficients[i] * s.Rational(comb(k, i), comb(4, i))
        for i in range(k + 1)
    )) for k in range(5)]
    expected_bernstein = [
        s.Integer(0), -45 + 21 * s.sqrt(5), -4 + s.Rational(8, 3) * s.sqrt(5),
        -21 + 9 * s.sqrt(5), -16 + 8 * s.sqrt(5),
    ]
    require(all(s.simplify(a0 - b0) == 0
                for a0, b0 in zip(bernstein, expected_bernstein)),
            "observer_trace_gap_exact_bernstein_coefficients")
    require(bool(s.simplify(bernstein[3] < 0)),
            "observer_trace_unsplit_negative_control_requires_split")
    levels = [bernstein]
    while len(levels[-1]) > 1:
        prior = levels[-1]
        levels.append([s.simplify((prior[i] + prior[i + 1]) / 2)
                       for i in range(len(prior) - 1)])
    left_controls = [levels[j][0] for j in range(5)]
    right_controls = [levels[4 - j][j] for j in range(5)]
    expected_left = [
        s.Integer(0), (-45 + 21 * s.sqrt(5)) / 2,
        (-141 + 67 * s.sqrt(5)) / 6, -21 + 10 * s.sqrt(5),
        -19 + 9 * s.sqrt(5),
    ]
    expected_right = [
        -19 + 9 * s.sqrt(5), -17 + 8 * s.sqrt(5),
        (-93 + 43 * s.sqrt(5)) / 6, (-37 + 17 * s.sqrt(5)) / 2,
        -16 + 8 * s.sqrt(5),
    ]
    require(all(s.simplify(a0 - b0) == 0
                for a0, b0 in zip(left_controls, expected_left)),
            "observer_trace_gap_left_half_controls")
    require(all(s.simplify(a0 - b0) == 0
                for a0, b0 in zip(right_controls, expected_right)),
            "observer_trace_gap_right_half_controls")
    require(left_controls[0] == 0, "observer_trace_gap_only_endpoint_zero")
    for index, coefficient in enumerate(left_controls[1:], start=1):
        require(bool(s.simplify(coefficient > 0)),
                f"observer_trace_gap_left_positive_{index}")
    for index, coefficient in enumerate(right_controls):
        require(bool(s.simplify(coefficient > 0)),
                f"observer_trace_gap_right_positive_{index}")
    require(s.simplify(t0_all.subs(c0, -1) - 2 * L0) == 0 and
            s.simplify(d0_all.subs(c0, -1) - L0**2) == 0 and
            s.simplify(t0_all.subs(c0, 1)) == 0 and
            s.simplify(d0_all.subs(c0, 1)) == 0,
            "observer_trace_endpoint_blocks")

    # Rebuild the cap-one F_query matrix and check both actual eigenvectors.
    I2 = s.eye(2)
    G = s.Matrix([[a, -a**2], [a**2, a]])
    CX = s.eye(4)
    CX[2, 2] = CX[3, 3] = 0
    CX[2, 3] = CX[3, 2] = 1
    T = CX * s.kronecker_product(G, I2)
    U = s.kronecker_product(T * T, G * G)
    P = s.zeros(8, 2)
    P[0, 0] = P[2, 1] = 1
    W = P.T * U * P
    F_query = I2 - W.T * W
    plus = s.Matrix([1, 1])
    minus = s.Matrix([1, -1])
    require(all(reduce(x) == 0 for x in (F_query * plus - M * plus)),
            "query_plus_effect_eigenvalue_M")
    require(all(reduce(x) == 0 for x in (F_query * minus - L * minus)),
            "query_minus_effect_eigenvalue_L")
    require(reduce(M - L - 4 * p**9) == 0 and a.is_positive,
            "strict_effect_spectral_gap")

    # At c=1, the full CAR maximum is L; bound the aligned determinant gap.
    p_exact = (s.sqrt(5) - 1) / 2
    L_exact = 4 * p_exact**3
    require(bool(s.simplify(p_exact - s.Rational(1, 2) > 0)),
            "golden_probability_lower_bound")
    require(bool(s.simplify(s.Rational(5, 8) - p_exact > 0)),
            "golden_probability_upper_bound")
    require(bool(s.simplify(L_exact - s.Rational(1, 2) > 0)),
            "L_lower_bound_for_compression")
    require(bool(s.simplify(s.Rational(125, 128) - L_exact > 0)),
            "L_upper_bound_for_compression")
    det_gap = s.simplify((1 - z * M) - (1 - z * L) ** 3)
    brace = L * (2 - p**6) - 3 * z * L**2 + z**2 * L**3
    require(reduce(det_gap - z * brace) == 0,
            "determinant_gap_exact_factorization")
    require(s.Rational(1, 2) - 3 * z > 0 and p_exact**6 < 1,
            "determinant_gap_rational_lower_bound")
    require(reduce((1 - z * M) * (1 - z * L) - (1 - z * L) ** 4 -
                   (1 - z * L) * det_gap) == 0,
            "raw_two_band_and_car_determinants_relation")

    result = {
        "status": "PASS",
        "input_commit": INPUT,
        "checks": checks,
        "check_count": len(checks),
        "target_effect_spectrum": ["L=4*p^3", "M=4*p^3*(1+p^6)"],
        "car_effect_spectrum": ["ell(c) multiplicity 2", "roots(x^2-t(c)x+d(c)) multiplicity 2", "roots(x^2-t0(c)x+d0(c))", "eight zeros"],
        "strict_gap": "M-L=4*p^9>0",
        "aligned_c1_raw_determinant_relation": "det_query-det_CAR=(1-z*L)*z*(L*(2-p^6)-3*z*L^2+z^2*L^3)>0",
        "observer_angle_result": "no direct two-dimensional same-event isometric compression for any c in [-1,1]",
        "scope": "same-z direct isometric effect compression only; no Book03 price identity, physical admission, or GR closure",
    }
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        (HERE / "VERIFICATION.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
