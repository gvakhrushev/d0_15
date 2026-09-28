#!/usr/bin/env python3
"""Replay the supplied A4D closure packet with exact arithmetic.

The packet's original scripts and result files are retained byte-for-byte in
``research/sources/a4d_closure_packet_2026-09-28``.  This checker reruns them in
temporary directories, strengthens the degree-three witness serialization,
and constructs explicit exact ``q_2`` witnesses for the two D2 orbits and both
carriers.  The checked scope is finite and named in the companion memo.

Run normally to verify the committed result, or pass ``--write-results`` only
when intentionally regenerating that result during review.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "02_REGISTRY/research/sources/a4d_closure_packet_2026-09-28"
CERT_DIR = ROOT / "02_REGISTRY/research/certificates"
RESULT_PATH = CERT_DIR / "a4d_closure_packet_integration_results.json"
COEFFICIENTS = CERT_DIR / "a4d_haq_coefficientwise_identity_coefficients.json"

INPUT_SHA256 = {
    "d0_a4d_closure_certificate.py": "cf87dcd06951c9923de06ed52621f9d93034612b5b4b6253e6a9bec0e9597fde",
    "d0_a4d_closure_results.json": "8758fdd5ea96ffdad9220178342b25eb980b288a83ba7975acd2dfb90e552666",
    "a4d_slow_lift_reconstruction_check.py": "2a7ef4720ec6645efd18bd84052be3ba7c8f6bc49af007903208da2e91317198",
    "d0_a4d_slow_lift_result.json": "ebe9a53f88fc82a450f9287330fa0ed71a495e5134d29b87dae6b6ef5731887a",
}
COEFFICIENTS_SHA256 = "e106d8937fad966eefd1838ce69e0bb32d7e34100e452b9a9c1f78ec78e454f5"
CLOSURE_TERMINAL = "TERMINAL D0-A4D-CLOSURE-CERTIFICATE-PASS"
SLOW_TERMINAL = "TERMINAL J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS"


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def complex_text(value) -> list[str]:
    return [fraction_text(value[0]), fraction_text(value[1])]


def run_closure_source(namespace_out: dict) -> tuple[dict, str]:
    """Run the verbatim closure script and return its globals and stdout."""
    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="a4d-closure-packet-") as tmp_name:
        work = Path(tmp_name)
        shutil.copy2(SOURCE_DIR / "d0_a4d_closure_certificate.py", work)
        shutil.copy2(COEFFICIENTS, work / "haq_coefficients.json")
        os.chdir(work)
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                namespace = runpy.run_path(str(work / "d0_a4d_closure_certificate.py"))
        finally:
            os.chdir(old_cwd)
        generated = json.loads((work / "d0_a4d_closure_results.json").read_text())
    namespace_out.update(namespace)
    return generated, output.getvalue()


def solve_exact(matrix, rhs, ns):
    """Return one exact Gaussian-rational solution of matrix*q=rhs."""
    F = ns["F"]
    add, mul, cd, sc = ns["add"], ns["mul"], ns["cd"], ns["sc"]
    zero = (F(0), F(0))
    augmented = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        found = next(
            (i for i in range(pivot_row, len(augmented)) if augmented[i][column] != zero),
            None,
        )
        if found is None:
            continue
        augmented[pivot_row], augmented[found] = augmented[found], augmented[pivot_row]
        pivot = augmented[pivot_row][column]
        augmented[pivot_row] = [cd(value, pivot) for value in augmented[pivot_row]]
        for i in range(len(augmented)):
            if i == pivot_row:
                continue
            coefficient = augmented[i][column]
            if coefficient != zero:
                augmented[i] = [
                    add(value, sc(-1, mul(coefficient, base)))
                    for value, base in zip(augmented[i], augmented[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(augmented):
            break

    require("D2_WITNESS_SYSTEM_CONSISTENT", all(
        any(value != zero for value in row[:-1]) or row[-1] == zero
        for row in augmented
    ))
    solution = [zero for _ in matrix[0]]
    for row, column in enumerate(pivot_columns):
        solution[column] = augmented[row][-1]
    exact_rows = True
    for i, row in enumerate(matrix):
        value = zero
        for coefficient, component in zip(row, solution):
            value = add(value, mul(coefficient, component))
        exact_rows = exact_rows and value == rhs[i]
    require("D2_WITNESS_CQ2_EQ_M2_EXACT", exact_rows)
    return solution


def build_results(ns: dict, closure_source_result: dict, slow_stdout: str) -> dict:
    F = ns["F"]
    zero = (F(0), F(0))

    # The supplied A calculation uses an exact Fraction Hessian.  Recompute
    # its four Fourier ranks and verify the named left witness explicitly.
    degree3 = {}
    ell = [F(1), F(1), F(1)] + [F(0)] * 21
    for name, dress, probe, sign in [
        ("COS", [1, 0, -1, 0], [0, 1, 0, -1], 1),
        ("SIN", [0, 1, 0, -1], [1, 0, -1, 0], -1),
    ]:
        blocks = [
            ns["hessian_block"](probe, weight)
            for weight in ([1] * 4, [1, -1, 1, -1], dress, probe)
        ]
        ranks = [len(ns["rref"](block)[1]) for block in blocks]
        joint = [sum((block[i] for block in blocks), []) for i in range(24)]
        f3 = [F(sign * value) for value in ns["COS_f3"]]
        augmented = [row + [f3[i]] for i, row in enumerate(joint)]
        joint_rank = len(ns["rref"](joint)[1])
        augmented_rank = len(ns["rref"](augmented)[1])
        left_products = [sum(ell[i] * joint[i][j] for i in range(24)) for j in range(96)]
        pairing = sum(ell[i] * f3[i] for i in range(24))
        require(f"A260_{name}_FOURIER_RANKS", ranks == [0, 0, 16, 0])
        require(f"A260_{name}_JOINT_RANK", joint_rank == 16)
        require(f"A260_{name}_AUGMENTED_RANK", augmented_rank == 17)
        require(f"A260_{name}_EXPLICIT_LEFT_WITNESS", left_products == [F(0)] * 96)
        require(f"A260_{name}_PAIRING", pairing == F(64 * sign))
        degree3[name] = {
            "fourier_ranks": ranks,
            "joint_rank": joint_rank,
            "augmented_rank": augmented_rank,
            "ell": [int(value) for value in ell],
            "ell_dot_f3": int(pairing),
        }

    # The supplied D2 checker scans k=1..12.  The closed formula uses the
    # proven two-value support and M1=0; this replay exports an exact q2 and
    # checks qk = ratio(k)*q2 through k=12 for both orbits and carriers.
    orbit_results = []
    all_checks = 0
    for orbit, raw_x in [
        (5, [(-1, -1), (-1, -1), (-1, 1), (-1, 1)]),
        (7, [(-2, 0), (-1, -1), (-1, -1), (-2, 0)]),
    ]:
        x = [(F(real), F(imag)) for real, imag in raw_x]
        distinct = []
        for value in x:
            if value not in distinct:
                distinct.append(value)
        a, b = distinct
        m1 = ns["Mkx"](x, 1)
        require(f"D2_ORBIT_{orbit}_M1_ZERO", all(value == zero for value in m1))
        for carrier, d_values in (("C(x)", x), ("C(conj x)", [ns["cj"](v) for v in x])):
            matrix = ns["Cm"](d_values)
            m2 = ns["Mkx"](x, 2)
            rank_c = ns["rank"](ns["realify"](matrix)) // 2
            require(f"D2_ORBIT_{orbit}_{carrier}_RANK_C9", rank_c == 9)
            q2 = solve_exact(matrix, m2, ns)
            per_k = []
            formula_checks = []
            witness_checks = []
            augmented_checks = []
            for k in range(1, 13):
                mk = ns["Mkx"](x, k)
                ratio = ns["cd"](
                    ns["add"](ns["pw"](a, k - 1), ns["sc"](-1, ns["pw"](b, k - 1))),
                    ns["add"](a, ns["sc"](-1, b)),
                )
                formula = [ns["mul"](ratio, value) for value in m2]
                qk = [ns["mul"](ratio, value) for value in q2]
                image = [
                    sum_complex(
                        (ns["mul"](coefficient, component) for coefficient, component in zip(row, qk)),
                        ns,
                    )
                    for row in matrix
                ]
                augmented_rank = ns["rank"](
                    ns["realify"]([row + [mk[i]] for i, row in enumerate(matrix)])
                ) // 2
                formula_checks.append(mk == formula)
                witness_checks.append(image == mk)
                augmented_checks.append(augmented_rank == rank_c)
                per_k.append({"k": k, "ratio": complex_text(ratio), "augmented_rank": augmented_rank})
                all_checks += 1
            require(f"D2_ORBIT_{orbit}_{carrier}_ALL_12_IDENTITIES", all(formula_checks))
            require(f"D2_ORBIT_{orbit}_{carrier}_ALL_12_WITNESSES", all(witness_checks))
            require(f"D2_ORBIT_{orbit}_{carrier}_ALL_12_AUGMENTED_RANKS", all(augmented_checks))
            orbit_results.append({
                "orbit": orbit,
                "carrier": carrier,
                "rank_C": rank_c,
                "q2": [complex_text(value) for value in q2],
                "qk_rule": "q_k = ((a^(k-1)-b^(k-1))/(a-b)) * q_2",
                "checked_k": per_k,
            })

    # The slow-lift script is a separate exact SymPy reconstruction.  Its own
    # assertions are fatal; verify the expected terminal and all 96 flat rows.
    require("C275_SLOW_TERMINAL", SLOW_TERMINAL in slow_stdout)
    require("C275_SLOW_ORDER_H_FORCING", "PASS_ORDER_H_FORCING_SUPPORT" in slow_stdout)
    require("C275_SLOW_LIFT_SOLUTION", "PASS_LIFT_SOLUTION" in slow_stdout)
    require("C275_SLOW_LIFT_RESIDUAL", "PASS_LIFT_RESIDUAL" in slow_stdout)
    require("C275_SLOW_ALL_PHASE_ORDER_H", sum(
        f"PASS_PHASE_{phase}_ORDER_H_CANCELLED" in slow_stdout for phase in range(4)
    ) == 4)
    require("C275_SLOW_ALL_PHASE_ORDER_H2", sum(
        f"PASS_PHASE_{phase}_ORDER_H2" in slow_stdout for phase in range(4)
    ) == 4)
    require("C275_SLOW_NORMALIZED_H_AND_H2", all(
        token in slow_stdout for token in ("PASS_NORMALIZED_LIMIT_h", "PASS_NORMALIZED_LIMIT_h**2")
    ))
    flat_rows = sum(1 for line in slow_stdout.splitlines() if line.startswith("PASS_FLAT_LIMIT_EK_"))
    require("C275_SLOW_96_FLAT_COMPONENTS", flat_rows == 96)

    supplied_closure = json.loads((SOURCE_DIR / "d0_a4d_closure_results.json").read_text())
    supplied_slow = json.loads((SOURCE_DIR / "d0_a4d_slow_lift_result.json").read_text())
    slow_claims = supplied_slow["C_275_slow_lift"]
    slow_checks = slow_claims["checks"]
    require("SUPPLIED_CLOSURE_RESULT_REPLAYED", closure_source_result == supplied_closure)
    require("SUPPLIED_SLOW_RESULT_SCOPE", "not the full #240 class" in slow_claims["scope"])
    require("SUPPLIED_SLOW_RESULT_TERMINAL", slow_claims["terminal"] == SLOW_TERMINAL.removeprefix("TERMINAL "))
    require("SUPPLIED_SLOW_RESULT_FORCING", "support" in slow_checks["order_h_forcing"])
    require("SUPPLIED_SLOW_RESULT_LIFT", slow_checks["lift_solution"] == [
        "-z(z+2)/D", "-2z^2/D", "z(z+2)/D", "-2z^2/D"
    ] and slow_checks["lift_residual"] == "zero")
    require("SUPPLIED_SLOW_RESULT_METRIC", slow_checks["order_h_metric_cancelled"] == "all four phases")
    require("SUPPLIED_SLOW_RESULT_NORMALIZED_LIMIT", slow_checks["normalized_limit"] == "0 under z=h and z=h^2")

    return {
        "schema": "a4d-closure-packet-integration/1",
        "source_sha256": INPUT_SHA256,
        "coefficient_input": {
            "path": "02_REGISTRY/research/certificates/a4d_haq_coefficientwise_identity_coefficients.json",
            "sha256": COEFFICIENTS_SHA256,
        },
        "A_260_degree3": {
            "fourier_order": ["zero", "minus", "resonant", "orthogonal"],
            "COS": degree3["COS"],
            "SIN": degree3["SIN"],
            "scope": "two selected real dressings only; not a classification of the full complex N0 support",
            "uploaded_json_note": "The supplied result stores ell as scalar 1; this result records and checks the full 24-entry witness.",
        },
        "B_D2_imC_all_k": {
            "identity": "M_k = ((a^(k-1)-b^(k-1))/(a-b)) * M_2",
            "all_k_witness": "q_k = ((a^(k-1)-b^(k-1))/(a-b)) * q_2",
            "orbit_carrier_count": len(orbit_results),
            "finite_replays": all_checks,
            "nonconforming": 0,
            "witnesses": orbit_results,
            "scope": "orbits 5 and 7, with C(x) and C(conj x), and the pinned coefficient table",
        },
        "C_275_reconstructed_slow_lift": {
            "terminal": SLOW_TERMINAL.removeprefix("TERMINAL "),
            "checks": {
                "flat_components": flat_rows,
                "lift_solution": ["-z(z+2)/D", "-2z^2/D", "z(z+2)/D", "-2z^2/D"],
                "D": "3z^2+4",
                "order_h_metric_cancelled": "all four phases",
                "normalized_limit": "0 under z=h and z=h^2",
            },
            "scope": "independent reconstruction on selected #232 Y carrier; does not extend to full #240 class",
        },
    }


def sum_complex(values, ns):
    result = (ns["F"](0), ns["F"](0))
    for value in values:
        result = ns["add"](result, value)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true", help="regenerate the committed JSON result")
    args = parser.parse_args()

    for name, expected in INPUT_SHA256.items():
        require(f"SOURCE_SHA256_{name}", sha256(SOURCE_DIR / name) == expected)
    require("COEFFICIENT_INPUT_SHA256", sha256(COEFFICIENTS) == COEFFICIENTS_SHA256)

    namespace_out: dict = {}
    closure_result, closure_stdout = run_closure_source(namespace_out)
    require("CLOSURE_SOURCE_TERMINAL", CLOSURE_TERMINAL in closure_stdout)
    slow_run = __import__("subprocess").run(
        [__import__("sys").executable, str(SOURCE_DIR / "a4d_slow_lift_reconstruction_check.py")],
        cwd=SOURCE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if slow_run.returncode != 0:
        raise AssertionError("slow-lift source failed:\n" + slow_run.stdout + "\n" + slow_run.stderr)
    results = build_results(namespace_out, closure_result, slow_run.stdout)

    rendered = json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    if args.write_results:
        RESULT_PATH.write_text(rendered)
        print("WROTE " + str(RESULT_PATH.relative_to(ROOT)))
    else:
        require("INTEGRATION_RESULT_MATCHES", RESULT_PATH.read_text() == rendered)
    print("TERMINAL A4D-CLOSURE-PACKET-INDEPENDENT-REPLAY-PASS")


if __name__ == "__main__":
    main()
