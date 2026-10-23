#!/usr/bin/env python3
"""Exact rational TT continuation of the original full-40 Schur operator.

Rebuilds the original six-based-plaquette L/B/C Taylor blocks through cubic
order, eliminates the 24 Lorentz links, and checks both TT polarisations on
the real null cone 2*u*v=x^2+y^2 with u != 0.  Correctors are constructed
over rational-function fields; y=0 and the null-axis chart are checked
separately so the chosen generic corrector denominators do not hide a real
direction.  The result is a quartic Taylor-jet identity, not an all-order
dispersion theorem or native-action selection.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from itertools import combinations
from math import factorial
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import QQ


ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = Path("02_REGISTRY/research/sources/d0_two_null_crossing_2026-10-19")
BASE_JS = SOURCE_DIR / "check_full40_schur_rank_modular.cjs"
TAYLOR_JS = SOURCE_DIR / "check_oblique_tt_directional_dispersion.cjs"

u, v, x, y = sp.symbols("u v x y")
MOMENTUM = (u, v, x, y)
Q = x**2 + y**2
NULL_SUBSTITUTION = {v: Q / (2 * u)}
PAIRS = list(combinations(range(4), 2))
ETA = sp.Matrix(
    [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ]
)
IDENTITY = sp.eye(4)
ZERO4 = sp.zeros(4)
GENERATORS: list[sp.Matrix] = []
for _i, _j in PAIRS:
    _forward = sp.zeros(4)
    _forward[_i, _j] = 1
    _backward = sp.zeros(4)
    _backward[_j, _i] = 1
    GENERATORS.append((_forward - _backward) * ETA)


def permutation_sign(a: int, b: int, c: int, d: int) -> int:
    values = (a, b, c, d)
    if len(set(values)) != 4:
        return 0
    inversions = sum(
        values[i] > values[j] for i in range(4) for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def binomial_polynomial(value: sp.Expr, order: int) -> sp.Expr:
    result: sp.Expr = sp.Integer(1)
    for j in range(order):
        result *= value - j
    return sp.expand(result / factorial(order))


def plaquette_pair(
    coframe: sp.Matrix, first: int, second: int, curvature: sp.Matrix
) -> sp.Expr:
    curvature_eta = curvature * ETA
    total: sp.Expr = sp.Integer(0)
    for a, b in PAIRS:
        c, d = [index for index in range(4) if index not in (a, b)]
        area = (
            coframe[a, first] * coframe[b, second]
            - coframe[b, first] * coframe[a, second]
        )
        total += permutation_sign(a, b, c, d) * area * curvature_eta[c, d]
    return sp.expand(total)


def coframe_pair(
    row: int, column: int, first: int, second: int, curvature: sp.Matrix
) -> sp.Expr:
    if column not in (first, second):
        return sp.Integer(0)
    varied = IDENTITY.copy()
    for index in range(4):
        varied[index, column] = int(row == index)
    return plaquette_pair(varied, first, second, curvature)


def shifted(site: tuple[int, ...], axis: int, amount: int = 1) -> tuple[int, ...]:
    return tuple(value + amount if index == axis else value for index, value in enumerate(site))


def link_column(
    momentum: tuple[sp.Expr, ...], varied_axis: int, varied_generator: int, order: int
) -> list[sp.Expr]:
    """One column of the original 24-link Euler Jacobian at Taylor order."""
    output: list[sp.Expr] = [sp.Integer(0)] * 24
    origin = (0, 0, 0, 0)

    for equation_axis in range(4):
        for equation_generator in range(6):
            total: sp.Expr = sp.Integer(0)
            generator = GENERATORS[equation_generator]
            for r, t in PAIRS:
                if equation_axis not in (r, t):
                    continue
                other = t if equation_axis == r else r
                first, second = [index for index in range(4) if index not in (r, t)]
                bases = (origin, shifted(origin, other, -1))
                for base in bases:
                    edges = (
                        (base, r, 1),
                        (shifted(base, r), t, 1),
                        (shifted(base, t), r, -1),
                        (base, t, -1),
                    )
                    edge_jets = []
                    for site, axis, orientation in edges:
                        if axis == varied_axis:
                            order_value = binomial_polynomial(
                                sum(momentum[i] * site[i] for i in range(4)), order
                            )
                            edge_jets.append(
                                orientation * GENERATORS[varied_generator] * order_value
                            )
                        else:
                            edge_jets.append(ZERO4)
                    first_plaquette_jet = sum(edge_jets, sp.zeros(4))
                    d_curvature_zero = sp.zeros(4)
                    d_curvature_first = sp.zeros(4)

                    for edge_index, (site, axis, orientation) in enumerate(edges):
                        if axis != equation_axis or site != origin:
                            continue
                        d0 = orientation * generator
                        field = (
                            GENERATORS[varied_generator]
                            * binomial_polynomial(
                                sum(momentum[i] * site[i] for i in range(4)), order
                            )
                            if axis == varied_axis
                            else ZERO4
                        )
                        d1 = generator * field if orientation == 1 else field * generator
                        d_curvature_zero += d0
                        term = d1
                        for previous in range(edge_index):
                            term += edge_jets[previous] * d0
                        for following in range(edge_index + 1, 4):
                            term += d0 * edge_jets[following]
                        d_curvature_first += term

                    corrected = d_curvature_first - (
                        first_plaquette_jet * d_curvature_zero
                        + d_curvature_zero * first_plaquette_jet
                    ) / 2
                    total += permutation_sign(r, t, first, second) * plaquette_pair(
                        IDENTITY, first, second, corrected
                    )
            output[6 * equation_axis + equation_generator] = sp.expand(total)
    return output


def taylor_blocks(
    momentum: tuple[sp.Expr, ...], order: int, *, need_link_block: bool = True
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Original six-face L/B/C coefficient at one Taylor order."""
    link_block = sp.zeros(24, 24)
    if need_link_block:
        for column in range(24):
            values = link_column(momentum, column // 6, column % 6, order)
            for row, value in enumerate(values):
                link_block[row, column] = value

    coframe_from_link = sp.zeros(24, 16)
    coframe_block = sp.zeros(16, 24)
    if order:
        for direction in range(4):
            for generator_index in range(6):
                for r, t in PAIRS:
                    if direction not in (r, t):
                        continue
                    other = t if direction == r else r
                    first, second = [index for index in range(4) if index not in (r, t)]
                    factor = (
                        permutation_sign(r, t, first, second)
                        * (1 if direction == r else -1)
                        * (-binomial_polynomial(-momentum[other], order))
                    )
                    for row in range(4):
                        for column in range(4):
                            pair_value = coframe_pair(
                                row, column, first, second, GENERATORS[generator_index]
                            )
                            if pair_value:
                                coframe_from_link[
                                    6 * direction + generator_index, 4 * row + column
                                ] += sp.expand(factor * pair_value)

        # This block is outside the direction loop: each original face is
        # counted once, with its two link directions.
        for r, t in PAIRS:
            first, second = [index for index in range(4) if index not in (r, t)]
            for direction in (r, t):
                factor = permutation_sign(r, t, first, second) * (
                    -binomial_polynomial(momentum[t], order)
                    if direction == r
                    else binomial_polynomial(momentum[r], order)
                )
                for generator_index in range(6):
                    for row in range(4):
                        for column in range(4):
                            pair_value = coframe_pair(
                                row,
                                column,
                                first,
                                second,
                                GENERATORS[generator_index],
                            )
                            if pair_value:
                                coframe_block[
                                    4 * row + column, 6 * direction + generator_index
                                ] += sp.expand(factor * pair_value)
    return link_block, coframe_from_link, coframe_block


def expanded(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(sp.expand)


def substitute_matrix(matrix: sp.Matrix, substitution: dict[sp.Symbol, sp.Expr]) -> sp.Matrix:
    return matrix.applyfunc(lambda value: sp.expand(value.subs(substitution)))


def solve_in_fraction_field(
    matrix: sp.Matrix, rhs: sp.Matrix, field: Any
) -> tuple[sp.Matrix, int, int, tuple[int, ...]]:
    """Construct a sparse particular solution and verify it in the exact field."""
    domain_matrix = DomainMatrix.from_Matrix(matrix).convert_to(field)
    augmented = DomainMatrix.from_Matrix(matrix.row_join(rhs)).convert_to(field)
    reduced, pivots = augmented.rref()
    if matrix.cols in pivots:
        raise AssertionError("source is outside the Schur image")

    reduced_matrix = reduced.to_Matrix()
    solution = sp.zeros(matrix.cols, 1)
    for row, pivot in enumerate(pivots):
        if pivot >= matrix.cols:
            raise AssertionError("right-hand side became a pivot")
        solution[pivot] = reduced_matrix[row, matrix.cols]

    solution_domain = DomainMatrix.from_Matrix(solution).convert_to(field)
    rhs_domain = DomainMatrix.from_Matrix(-rhs).convert_to(field)
    residual = domain_matrix.matmul(solution_domain).add(rhs_domain).to_Matrix()
    if any(value != 0 for row in residual.tolist() for value in row):
        raise AssertionError("constructed corrector does not satisfy its exact equation")
    return solution, domain_matrix.rank(), len(pivots), tuple(pivots)


def zero_in_field(matrix: sp.Matrix, field: Any) -> bool:
    exact = DomainMatrix.from_Matrix(matrix).convert_to(field).to_Matrix()
    return all(value == 0 for row in exact.tolist() for value in row)


def denominator_factors(vector: sp.Matrix) -> list[str]:
    factors = {
        str(sp.factor(sp.denom(sp.cancel(value))))
        for value in vector
        if value != 0
    }
    return sorted(factors)


def polarization_vectors() -> dict[str, sp.Matrix]:
    transverse_u = sp.Matrix([0, x / u, 1, 0])
    transverse_v = sp.Matrix([0, y / u, 0, 1])
    plus = sp.zeros(4, 4)
    cross = sp.zeros(4, 4)
    for row in range(4):
        for column in range(4):
            plus[row, column] = sp.expand(
                sum(
                    ETA[row, index]
                    * (
                        transverse_u[index] * transverse_u[column]
                        - transverse_v[index] * transverse_v[column]
                    )
                    for index in range(4)
                )
                / 2
            )
            cross[row, column] = sp.expand(
                sum(
                    ETA[row, index]
                    * (
                        transverse_u[index] * transverse_v[column]
                        + transverse_v[index] * transverse_u[column]
                    )
                    for index in range(4)
                )
                / 2
            )
    return {"plus": sp.Matrix(list(plus)), "cross": sp.Matrix(list(cross))}


def continue_one_polarization(
    name: str,
    e0: sp.Matrix,
    s2: sp.Matrix,
    s3: sp.Matrix,
    s4: sp.Matrix,
    dv_s2: sp.Matrix,
    gamma: sp.Expr,
    field: Any,
) -> dict[str, Any]:
    if not zero_in_field(s2 * e0, field):
        raise AssertionError(f"{name}: not a principal null TT polarization")

    e1, rank_s2, rank_cubic, pivots_e1 = solve_in_fraction_field(
        s2, -s3 * e0, field
    )
    if rank_s2 != 4 or rank_cubic != 4:
        raise AssertionError(f"{name}: unexpected cubic Schur rank")

    quartic_residual = expanded(s4 * e0 + s3 * e1 + gamma * dv_s2 * e0)
    e2, rank_s2_again, rank_quartic, pivots_e2 = solve_in_fraction_field(
        s2, -quartic_residual, field
    )
    if rank_s2_again != 4 or rank_quartic != 4:
        raise AssertionError(f"{name}: unexpected quartic Schur rank")

    return {
        "principal_null": True,
        "rank_S2": rank_s2,
        "rank_cubic_augmented": rank_cubic,
        "rank_quartic_augmented": rank_quartic,
        "e1_pivot_columns": list(pivots_e1),
        "e2_pivot_columns": list(pivots_e2),
        "e1_nonzero_columns": [i for i, value in enumerate(e1) if value != 0],
        "e2_nonzero_columns": [i for i, value in enumerate(e2) if value != 0],
        "e1_denominators": denominator_factors(e1),
        "e2_denominators": denominator_factors(e2),
        "exact_corrector_identities": True,
    }


def modular_value(value: sp.Expr, prime: int) -> int:
    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_value = int(numerator) % prime
    denominator_value = int(denominator) % prime
    if denominator_value == 0:
        raise ZeroDivisionError("sample denominator is zero in the reference field")
    return numerator_value * pow(denominator_value, prime - 2, prime) % prime


def node_executable() -> str:
    configured = os.environ.get("D0_NODE")
    executable = configured or shutil.which("node")
    if not executable:
        raise RuntimeError("set D0_NODE or make Node.js available on PATH for source replay")
    return executable


def compare_reference_implementation(
    root: Path,
    l0: sp.Matrix,
    jets: dict[int, tuple[sp.Matrix, sp.Matrix, sp.Matrix]],
    schur: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    gamma_u: sp.Expr,
    gamma_v: sp.Expr,
) -> dict[str, Any]:
    node = node_executable()
    prime = 1009
    block_ray = [1, 2, 2, 0]
    base_module = "./" + str(BASE_JS)
    base_program = (
        f'const m=require("{base_module}");'
        "console.log(JSON.stringify([0,1,2,3].map(d=>"
        f'm.flatTaylorBlocks({json.dumps(block_ray)},d))))'
    )
    env = dict(os.environ)
    env["D0_SCHUR_PRIME"] = str(prime)
    actual_blocks = json.loads(
        subprocess.check_output(
            [node, "-e", base_program], cwd=root, env=env, text=True
        )
    )
    source_blocks = {0: (l0, sp.zeros(24, 16), sp.zeros(16, 24)), **jets}
    block_substitution = {
        u: 1,
        v: 2,
        x: 2,
        y: 0,
    }
    for order in range(4):
        for label, index in (("L", 0), ("B", 1), ("C", 2)):
            matrix = source_blocks[order][index]
            computed = [
                [
                    modular_value(matrix[row, column].subs(block_substitution), prime)
                    for column in range(matrix.cols)
                ]
                for row in range(matrix.rows)
            ]
            if computed != actual_blocks[order][label]:
                raise AssertionError(f"symbolic {label}_{order} disagrees with original source")

    schur_rays = ([1, 2, 2, 0], [1, 5, 1, -3], [2, 1, 2, 0], [2, 2, 2, 2])
    taylor_module = "./" + str(TAYLOR_JS)
    for ray in schur_rays:
        if 2 * ray[0] * ray[1] != ray[2] ** 2 + ray[3] ** 2:
            raise AssertionError("reference ray must be Minkowski null")
        program = (
            f'const m=require("{taylor_module}");'
            f"console.log(JSON.stringify(m.schurTaylor({json.dumps(ray)})))"
        )
        actual_schur = json.loads(
            subprocess.check_output([node, "-e", program], cwd=root, env=env, text=True)
        )
        substitution = {u: ray[0], x: ray[2], y: ray[3]}
        computed_schur = [
            [
                [
                    modular_value(matrix[row, column].subs(substitution), prime)
                    for column in range(16)
                ]
                for row in range(16)
            ]
            for matrix in schur
        ]
        if computed_schur != actual_schur:
            raise AssertionError(f"symbolic Schur jets disagree at {ray}")

        branch_program = (
            f'const m=require("{taylor_module}");'
            f"console.log(JSON.stringify([m.oneRay({json.dumps(ray)},0),"
            f"m.oneRay({json.dumps(ray)},1)]))"
        )
        actual_branches = json.loads(
            subprocess.check_output(
                [node, "-e", branch_program], cwd=root, env=env, text=True
            )
        )
        branch_gammas = (gamma_u, gamma_v)
        for branch_index, candidate in enumerate(branch_gammas):
            expected_gamma = modular_value(candidate.subs(substitution), prime)
            for polarization in ("plus", "cross"):
                if actual_branches[branch_index][polarization]["gamma_mod_p"] != expected_gamma:
                    raise AssertionError(
                        f"symbolic null-branch correction disagrees at {ray}"
                    )

    node_version = subprocess.check_output([node, "--version"], text=True).strip()
    return {
        "status": "PASS",
        "prime": prime,
        "L_B_C_orders": [0, 1, 2, 3],
        "L_B_C_ray": block_ray,
        "Schur_orders": [2, 3, 4],
        "Schur_rays": [list(ray) for ray in schur_rays],
        "null_branch_corrections": ["k_u", "k_v"],
        "node_version": node_version,
    }


def main() -> None:
    l0, _, _ = taylor_blocks(MOMENTUM, 0)
    determinant = l0.det()
    if determinant != 256:
        raise AssertionError(f"original flat Cartan determinant changed: {determinant}")
    inverse_l0 = l0.inv()
    jets = {order: taylor_blocks(MOMENTUM, order) for order in (1, 2, 3)}
    l1, b1, c1 = jets[1]
    l2, b2, c2 = jets[2]
    l3, b3, c3 = jets[3]

    x1 = expanded(inverse_l0 * b1)
    x2 = expanded(inverse_l0 * (b2 - l1 * x1))
    x3 = expanded(inverse_l0 * (b3 - l1 * x2 - l2 * x1))
    s2_raw = expanded(-c1 * x1)
    s3_raw = expanded(-(c1 * x2 + c2 * x1))
    s4_raw = expanded(-(c1 * x3 + c2 * x2 + c3 * x1))

    _, b_ev_u, c_ev_u = taylor_blocks((1, 0, 0, 0), 1, need_link_block=False)
    _, b_ev_v, c_ev_v = taylor_blocks((0, 1, 0, 0), 1, need_link_block=False)
    derivative_u_from_first_jets = expanded(
        -c_ev_u * inverse_l0 * b1 - c1 * inverse_l0 * b_ev_u
    )
    derivative_v_from_first_jets = expanded(
        -c_ev_v * inverse_l0 * b1 - c1 * inverse_l0 * b_ev_v
    )
    derivative_u_identity = expanded(
        derivative_u_from_first_jets
        - s2_raw.applyfunc(lambda value: sp.expand(sp.diff(value, u)))
    )
    derivative_v_identity = expanded(
        derivative_v_from_first_jets
        - s2_raw.applyfunc(lambda value: sp.expand(sp.diff(value, v)))
    )
    if any(value != 0 for value in derivative_u_identity):
        raise AssertionError("direct S2 u-momentum derivative identity failed")
    if any(value != 0 for value in derivative_v_identity):
        raise AssertionError("direct S2 v-momentum derivative identity failed")

    s2 = substitute_matrix(s2_raw, NULL_SUBSTITUTION)
    s3 = substitute_matrix(s3_raw, NULL_SUBSTITUTION)
    s4 = substitute_matrix(s4_raw, NULL_SUBSTITUTION)
    du_s2 = substitute_matrix(derivative_u_from_first_jets, NULL_SUBSTITUTION)
    dv_s2 = substitute_matrix(derivative_v_from_first_jets, NULL_SUBSTITUTION)
    gamma_numerator = (
        5 * Q**2
        + 12 * x * y * Q
        - 4 * (x * y) ** 2
        - 6 * (u + Q / (2 * u)) * (x + y) * Q
        + 2 * (u**2 + (Q / (2 * u)) ** 2) * Q
    )
    gamma_v = sp.cancel(gamma_numerator / (48 * u))
    gamma_u = sp.cancel(gamma_numerator / (48 * (Q / (2 * u))))

    field = QQ.frac_field(u, x, y)
    vectors = polarization_vectors()
    generic_results = {
        "shift_k_v": {
            name: continue_one_polarization(
                name, vector, s2, s3, s4, dv_s2, gamma_v, field
            )
            for name, vector in vectors.items()
        },
        "shift_k_u": {
            name: continue_one_polarization(
                name, vector, s2, s3, s4, du_s2, gamma_u, field
            )
            for name, vector in vectors.items()
        },
    }

    strata: dict[str, dict[str, Any]] = {}
    for label, substitution, stratum_field in (
        ("y=0", {y: sp.Integer(0)}, QQ.frac_field(u, x)),
        (
            "x=y=0",
            {x: sp.Integer(0), y: sp.Integer(0)},
            QQ.frac_field(u),
        ),
    ):
        restricted = {
            "S2": substitute_matrix(s2, substitution),
            "S3": substitute_matrix(s3, substitution),
            "S4": substitute_matrix(s4, substitution),
            "duS2": substitute_matrix(du_s2, substitution),
            "dvS2": substitute_matrix(dv_s2, substitution),
        }
        vectors = {
            name: substitute_matrix(vector, substitution)
            for name, vector in polarization_vectors().items()
        }
        branch_results = {
            "shift_k_v": {
                name: continue_one_polarization(
                    name,
                    vector,
                    restricted["S2"],
                    restricted["S3"],
                    restricted["S4"],
                    restricted["dvS2"],
                    sp.cancel(gamma_v.subs(substitution)),
                    stratum_field,
                )
                for name, vector in vectors.items()
            }
        }
        if label == "y=0":
            # Here x is generic and nonzero, hence v=Q/(2u) is nonzero.
            branch_results["shift_k_u"] = {
                name: continue_one_polarization(
                    name,
                    vector,
                    restricted["S2"],
                    restricted["S3"],
                    restricted["S4"],
                    restricted["duS2"],
                    sp.cancel(gamma_u.subs(substitution)),
                    stratum_field,
                )
                for name, vector in vectors.items()
            }
        strata[label] = branch_results

    source_hashes = {
        str(path): hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in (BASE_JS, TAYLOR_JS)
    }
    checker_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    node_replay = compare_reference_implementation(
        ROOT, l0, jets, (s2, s3, s4), gamma_u, gamma_v
    )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()

    result = {
        "status": "PASS_EXACT_RATIONAL_IDENTITY",
        "schema": "d0-oblique-tt-quartic-symbolic/1",
        "command": (
            "D0_NODE=<node> python3 "
            "02_REGISTRY/research/sources/d0_two_null_crossing_2026-10-19/"
            "check_oblique_tt_quartic_symbolic.py"
        ),
        "git_head": head,
        "checker_sha256": checker_hash,
        "environment": {
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
        },
        "carrier": "original six-based-plaquette full-40 Lorentz/coframe action",
        "flat_cartan_determinant": int(determinant),
        "null_chart": "2*u*v=x^2+y^2, u!=0; v=(x^2+y^2)/(2*u)",
        "fraction_field": "QQ(u,x,y)",
        "schur_coefficients": ["S2", "S3", "S4"],
        "gamma_formulas": {
            "shift_k_v": "(5Q^2+12PQ-4P^2-6(u+v)(x+y)Q+2(u^2+v^2)Q)/(48u)",
            "shift_k_u": "(5Q^2+12PQ-4P^2-6(u+v)(x+y)Q+2(u^2+v^2)Q)/(48v), v!=0",
            "Q": "x^2+y^2",
            "P": "xy",
        },
        "direct_momentum_derivatives": {"u": "PASS_EXACT", "v": "PASS_EXACT"},
        "generic_polarizations": generic_results,
        "real_denominator_strata": strata,
        "reference_implementation_replay": node_replay,
        "input_sha256": source_hashes,
        "scope": [
            "constructive exact rational e1 and e2 correctors solve both TT Schur equations through order h^4 on the k_v branch for every real null direction in the u!=0 chart",
            "the k_u branch is also exact when v!=0; the k_v branch covers the axis x=y=0",
            "generic identities are over QQ(u,x,y); y=0 and x=y=0 strata are checked separately",
            "does not prove an all-order finite-h characteristic pole or residue",
            "does not prove uniform refinement or a nonlinear periodic root",
            "does not select the same-run native Book/Cost-Info action; GR_closed=false",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
