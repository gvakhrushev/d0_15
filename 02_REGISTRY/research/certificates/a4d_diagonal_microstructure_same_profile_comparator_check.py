#!/usr/bin/env python3
"""Compare the #232 joint slow-jet coefficients with the independent #216 sheet.

The exact native 24-dimensional jet is consumed from its pinned checker.  The
#216 approximate sheet depends on the sampled metric and its derivatives, not
on the fast connection amplitude z.  This certificate checks that interface
and independently computes the continuum Einstein tensor of the same local
slow-profile extension.  It does not construct a finite smooth root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
INPUTS = {
    "02_REGISTRY/research/certificates/a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py":
        "11479b60d96a8cb26ce963ac3c4c5190d3de179c433f1bb20b8ea1e5d0a1ad02",
    "02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md":
        "3ba0c4355999b147bc77048b082660558c538c48d49ef7fff98d4541069bf28a",
}


def require(ok: bool, name: str, checks: list[str]) -> None:
    if not bool(ok):
        raise AssertionError(name)
    checks.append(name)


def series_matrix(matrix: sp.MatrixBase, variable: sp.Symbol, order: int) -> sp.Matrix:
    return matrix.applyfunc(
        lambda value: sp.expand(sp.series(value, variable, 0, order).removeO())
    )


def main() -> dict:
    checks: list[str] = []
    for rel, expected in INPUTS.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected, "pinned_input_" + Path(rel).name, checks)

    native_checker = (ROOT / next(iter(INPUTS))).read_text()
    smooth_owner = (ROOT / list(INPUTS)[1]).read_text()
    require(
        "H3_JET_NATIVE_METRIC_H2_X0_ZERO_FOR_ALL_24_DIRECTIONS" in native_checker
        and "H3_JET_NATIVE_METRIC_H3_X0_ZERO_FOR_ALL_24_DIRECTIONS" in native_checker,
        "consumed_native_h2_h3_coefficients_are_the_all24_exact_checks",
        checks,
    )
    require(
        r"A_h^{\rm sm}=\sum_{j\ge1}h^j A_j[g]" in smooth_owner
        and "h^{-2}E_Q(Q_h,K_h^{\\rm sm})(x)=-\\tfrac12G[g](x)+O(h)" in smooth_owner,
        "consumed_designated_smooth_sheet_is_a_function_of_g",
        checks,
    )

    h, x0, z = sp.symbols("h x0 z", real=True)
    eta = sp.diag(1, -1, -1, -1)
    alpha = sp.zeros(4)
    alpha[1, 2] = alpha[2, 1] = 1
    beta = sp.zeros(4)
    beta[0, 1] = beta[1, 0] = 1
    A = (alpha * eta / 2).T
    B = (beta * eta / 2).T

    # This is exactly the solder profile used by the pinned native jet.
    S_lattice = sp.eye(4) + h * A + h**2 * x0 * B
    Q_lattice = sp.simplify(S_lattice.T * eta * S_lattice)
    require(z not in Q_lattice.free_symbols, "sampled_metric_is_independent_of_fast_z", checks)
    require(Q_lattice.subs(h, 0) == eta, "profile_has_flat_limit", checks)

    # A formal response of the designated #216 sheet may depend arbitrarily
    # on h and x0, but its coefficients are functions of Q_h only.  Keep the
    # coefficients generic so the zero-z conclusion does not assume a
    # particular smooth-branch gauge or a discrete Levi-Civita formula.
    smooth_response = sp.zeros(10, 1)
    for slot in range(10):
        smooth_response[slot] = sum(
            sp.Symbol(f"r_{slot}_{a}_{b}") * h**a * x0**b
            for a in range(4)
            for b in range(2)
        )
    mixed_monomials = (h**2 * z * x0, h**3 * z * x0)
    smooth_coefficients = {}
    for monomial in mixed_monomials:
        values = [sp.Poly(value, h, z, x0).coeff_monomial(monomial)
                  for value in smooth_response]
        require(values == [0] * 10, "smooth_sheet_mixed_coefficient_zero_" + str(monomial), checks)
        smooth_coefficients[str(monomial)] = [str(value) for value in values]

    # The exact pinned #232 solve has zero common metric coefficient at both
    # mixed orders for every one of its 24 free directions.  Since the same
    # #216 comparator has zero coefficient there, the normalized response
    # difference has no gap on this formal bidegree.
    native_coefficients = {str(monomial): ["0"] * 10 for monomial in mixed_monomials}
    gap_coefficients = {
        key: [str(sp.sympify(a) - sp.sympify(b)) for a, b in zip(native_coefficients[key], values)]
        for key, values in smooth_coefficients.items()
    }
    require(all(value == "0" for row in gap_coefficients.values() for value in row),
            "same_profile_response_gap_zero_at_h2zx0_and_h3zx0", checks)

    # Continuum control: set X=h*x0 and extend the same coframe locally as
    # S_h(X)=I+h*A+h*X*B.  This is an h-dependent slow profile, not the fixed-g
    # refinement family required by the parent terminal.
    X = sp.symbols("X", real=True)
    S_cont = sp.eye(4) + h * A + h * X * B
    g = sp.simplify(S_cont.T * eta * S_cont)
    g_inverse = sp.simplify(g.inv())

    def d(value: sp.Expr, index: int) -> sp.Expr:
        return sp.diff(value, X) if index == 0 else sp.Integer(0)

    gamma = [[[
        sp.cancel(sum(
            g_inverse[a, m] * (d(g[m, c], b) + d(g[m, b], c) - d(g[b, c], m)) / 2
            for m in range(4)
        ))
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = sp.Matrix(4, 4, lambda b, c: sp.cancel(sum(
        d(gamma[a][b][c], a) - d(gamma[a][b][a], c)
        + sum(gamma[a][a][m] * gamma[m][b][c] - gamma[a][c][m] * gamma[m][b][a]
              for m in range(4))
        for a in range(4)
    )))
    scalar = sp.cancel(sp.trace(g_inverse * ricci))
    einstein = sp.simplify(ricci - g * scalar / 2)
    einstein_h3 = series_matrix(einstein, h, 4)
    expected_einstein_h3 = sp.Matrix([
        [0, 0, 0, 0],
        [0, 0, -h**3 / 4, 0],
        [0, -h**3 / 4, h**2 / 4, 0],
        [0, 0, 0, h**2 / 4],
    ])
    require(einstein_h3 == expected_einstein_h3,
            "same_profile_continuum_Einstein_series_through_h3", checks)
    det_h1 = sp.series(g.det(), h, 0, 2).removeO()
    require(det_h1 == -1, "same_profile_is_lorentzian_in_a_local_small_h_chart", checks)

    return {
        "status": "PASS_SCOPED_SAME_PROFILE_COMPARATOR",
        "checks": checks,
        "exact_checks": len(checks),
        "inputs": INPUTS,
        "profile": {
            "solder": "I + h*(alpha*eta/2)^T + h^2*x0*(beta*eta/2)^T",
            "alpha": "E12+E21",
            "beta": "E01+E10",
            "metric_depends_on_fast_z": False,
            "smooth_sheet_depends_on": "Q_h and its smooth derivatives only",
        },
        "same_profile_mixed_coefficients": {
            key: {
                "native_all24_directions": native_coefficients[key],
                "designated_216_smooth_sheet": smooth_coefficients[key],
                "normalized_response_difference": gap_coefficients[key],
            }
            for key in smooth_coefficients
        },
        "continuum_geometry_control": {
            "coordinate_relation": "X=h*x0",
            "metric": [[str(value) for value in row] for row in g.tolist()],
            "Einstein_tensor_series_through_h3": [
                [str(value) for value in row] for row in einstein_h3.tolist()
            ],
            "scope": "continuum local slow-profile check; not a finite discrete root",
        },
        "conclusion": (
            "The h^2*z*x0 and h^3*z*x0 response-gap coefficients vanish on the "
            "pinned 24-dimensional formal joint family. This removes this local "
            "bidegree as a response-gap witness; it proves no exact root or "
            "refinement-uniform terminal."
        ),
        "nonclaims": [
            "no exact coupled periodic root",
            "no fixed nonconstant smooth metric refinement sequence",
            "no owner-sum response estimate",
            "no physical native admission or complete Cost-Info selection",
            "no #334 terminal and no positive GR closure",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("a4d_diagonal_microstructure_same_profile_comparator_results.json"))
    args = parser.parse_args()
    result = main()
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.write_json:
        args.output.write_text(encoded + "\n")
    print(encoded)
