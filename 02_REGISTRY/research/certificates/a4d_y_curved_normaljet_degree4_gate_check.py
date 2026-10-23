#!/usr/bin/env python3
"""Exact highest-degree piece of the first nonlinear Y normal-jet gate.

This checks only the homogeneous degree-four part in xi of the delta^2
Euler forcing for the normalized surviving R=-kappa beta tensor beta jet.
The already-owned normal-jet certificate proves that its first connection
tangent has degree one, so this top-degree forcing comes only from the exact
second-order Gram coframe.  A common phase-independent metric source is
allowed while testing compatibility, as prescribed by the owner replay.

This is not the full O_{2,h} calculation: lower normal-coordinate degrees,
the complete second connection jet, and uniform nonlinear continuation stay
open.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_normaljet_compatibility_check as C
import a4d_y_curved_response_quotient_check as B

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree4_gate_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def rank_exact(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ).rank()


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([
        sp.expand(left[a] * right[b] - left[b] * right[a])
        for a, b in B.PAIRS
    ])


def bivector(matrix: sp.Matrix) -> sp.Matrix:
    dressed = matrix * B.ETA
    return sp.Matrix([sp.expand(dressed[a, b]) for a, b in B.PAIRS])


def pairing(area: sp.Matrix, matrix: sp.Matrix) -> sp.Expr:
    return sp.expand((area.T * B.G2 * B.STAR * bivector(matrix))[0])


def linv(matrix: sp.Matrix) -> sp.Matrix:
    return B.ETA * matrix.T * B.ETA


def plaquette_factors(phase: int, a: int, b: int):
    wave = [B.cayley_Y(sp.Integer(1)), B.I4,
            linv(B.cayley_Y(sp.Integer(1))), B.I4]
    links = [
        (phase, a, False),
        ((phase + 1) % 4, b, False),
        ((phase + 1) % 4, a, True),
        (phase, b, True),
    ]
    factors = []
    for ph, role, inverse in links:
        link = wave[ph] if role == 0 else B.I4
        factors.append(linv(link) if inverse else link)
    return factors


def odd_curvature(factors: list[sp.Matrix]) -> sp.Matrix:
    plaquette = factors[0] * factors[1] * factors[2] * factors[3]
    return (plaquette - linv(plaquette)) / 2


def odd_curvature_variation(
    factors: list[sp.Matrix], corner: int, generator_index: int
) -> sp.Matrix:
    varied_factor = (
        -B.GEN[generator_index] * factors[corner]
        if corner in (2, 3)
        else factors[corner] * B.GEN[generator_index]
    )
    dplaquette = B.I4
    for i, factor in enumerate(factors):
        dplaquette = dplaquette * (varied_factor if i == corner else factor)
    plaquette = factors[0] * factors[1] * factors[2] * factors[3]
    inverse = linv(plaquette)
    return (dplaquette + inverse * dplaquette * inverse) / 2


def run(write: bool = False) -> dict:
    # The exact normal-jet owner has already solved the full first-slow system.
    owner_result = json.loads(C.RESULT_PATH.read_text())
    check(
        "OWNER_FIRST_CONNECTION_TANGENT_IS_LINEAR",
        owner_result["normal_jet"]["surviving_first_connection_tangent_degree"] == 1,
    )

    xi = sp.symbols("xi0:4")
    n = sp.ones(3, 1)
    p_perp = sp.eye(3) - n * n.T / 3
    xi_spatial = sp.Matrix([xi[1], xi[2], xi[3]])
    x = p_perp * xi_spatial
    r2 = sp.expand((x.T * x)[0])
    T = (r2 * p_perp - x * x.T).applyfunc(sp.expand)

    # S = I + delta U + delta^2 V is the geodesic-normal Gram coframe.
    U = sp.zeros(4)
    V = sp.zeros(4)
    U[1:4, 1:4] = -T / 2
    V[1:4, 1:4] = 3 * r2 * T / 40
    q1 = sp.zeros(4)
    q2 = sp.zeros(4)
    q1[1:4, 1:4] = T
    q2[1:4, 1:4] = -sp.Rational(2, 5) * r2 * T
    check("NORMAL_GRAM_FIRST_COEFFICIENT", U.T * B.ETA + B.ETA * U == q1)
    check(
        "NORMAL_GRAM_SECOND_COEFFICIENT",
        all(sp.factor(v) == 0 for v in (V.T * B.ETA + B.ETA * V + U.T * B.ETA * U - q2)),
    )

    unit = [B.I4[:, j] for j in range(4)]

    def area_delta2(a: int, b: int) -> sp.Matrix:
        u, v = [j for j in range(4) if j not in (a, b)]
        return (
            wedge(U[:, u], U[:, v])
            + wedge(V[:, u], unit[v])
            + wedge(unit[u], V[:, v])
        )

    def area_metric_delta2(a: int, b: int, qa: int, qb: int) -> sp.Matrix:
        """Second delta coefficient of d_Q(wedge(S_u,S_v))."""
        u, v = [j for j in range(4) if j not in (a, b)]
        dq = sp.zeros(4)
        dq[qa, qb] = dq[qb, qa] = 1

        # Use the Lorentz-self-adjoint Gram section eta*dS symmetric.  If
        # A=eta*dS, then A*S + S^T*A=dQ and A is symmetric.
        a0 = dq / 2
        a1 = -(a0 * U + U * a0) / 2
        a2 = -(a1 * U + U * a1 + a0 * V + V * a0) / 2
        d0, d1, d2 = B.ETA * a0, B.ETA * a1, B.ETA * a2
        if d0 != B.metric_lift(qa, qb):
            raise AssertionError(f"wrong Gram differential at q{qa}{qb}")
        return (
            wedge(d2[:, u], unit[v]) + wedge(unit[u], d2[:, v])
            + wedge(d1[:, u], U[:, v]) + wedge(U[:, u], d1[:, v])
            + wedge(d0[:, u], V[:, v]) + wedge(V[:, u], d0[:, v])
        )

    # Verify the literal phase/role placement against stationarity of the
    # frozen z=1 vacuum before using its 136-row joint derivative below.
    area0 = lambda a, b: wedge(
        unit[[j for j in range(4) if j not in (a, b)][0]],
        unit[[j for j in range(4) if j not in (a, b)][1]],
    )
    frozen_connection_euler = []
    for phase in range(4):
        for role in range(4):
            for gen in range(6):
                value = 0
                for a, b in B.PAIRS:
                    if role == a:
                        corners = [(phase, 0), ((phase - 1) % 4, 2)]
                    elif role == b:
                        corners = [((phase - 1) % 4, 1), (phase, 3)]
                    else:
                        continue
                    for base_phase, corner in corners:
                        factors = plaquette_factors(base_phase, a, b)
                        value += B.orientation(a, b) * pairing(
                            area0(a, b),
                            odd_curvature_variation(factors, corner, gen),
                        )
                frozen_connection_euler.append(sp.factor(value))
    check("FROZEN_CONNECTION_EULER_ZERO", frozen_connection_euler == [0] * 96)

    frozen_metric_euler = []
    for phase in range(4):
        for qa, qb in B.SYM:
            dS = B.metric_lift(qa, qb)
            value = 0
            for a, b in B.PAIRS:
                factors = plaquette_factors(phase, a, b)
                u, v = [j for j in range(4) if j not in (a, b)]
                darea = wedge(dS[:, u], unit[v]) + wedge(unit[u], dS[:, v])
                value += B.orientation(a, b) * pairing(
                    darea, odd_curvature(factors)
                )
            frozen_metric_euler.append(sp.factor(value))
    check("FROZEN_METRIC_EULER_ZERO", frozen_metric_euler == [0] * 40)

    ek = [sp.Integer(0)] * 96
    eq = [sp.Integer(0)] * 40

    # At order delta^2, homogeneous degree four is independent of the
    # degree-one first connection tangent: mixed terms have degree <=3, and
    # its quadratic connection jet is exactly zero by the owner certificate.
    # Thus the following are the full degree-four forcing coefficients.
    for phase in range(4):
        for role in range(4):
            for gen in range(6):
                value = 0
                for a, b in B.PAIRS:
                    if role == a:
                        corners = [(phase, 0), ((phase - 1) % 4, 2)]
                    elif role == b:
                        corners = [((phase - 1) % 4, 1), (phase, 3)]
                    else:
                        continue
                    for base_phase, corner in corners:
                        factors = plaquette_factors(base_phase, a, b)
                        dcurv = odd_curvature_variation(factors, corner, gen)
                        value += B.orientation(a, b) * pairing(area_delta2(a, b), dcurv)
                ek[(phase * 4 + role) * 6 + gen] = sp.expand(value)

        for mi, (qa, qb) in enumerate(B.SYM):
            value = 0
            for a, b in B.PAIRS:
                factors = plaquette_factors(phase, a, b)
                curv = odd_curvature(factors)
                value += B.orientation(a, b) * pairing(
                    area_metric_delta2(a, b, qa, qb), curv
                )
            eq[phase * 10 + mi] = sp.expand(value)

    forcing_polys = [sp.Poly(expr, *xi) for expr in ek + eq]
    monomials = [exponents for exponents in itertools.product(range(5), repeat=4)
                 if sum(exponents) == 4]
    check("HOMOGENEOUS_DEGREE_FOUR_HAS_35_MONOMIALS", len(monomials) == 35)
    forcing = sp.zeros(136, len(monomials))
    for col, exponents in enumerate(monomials):
        monomial = sp.prod(xi[i] ** exponents[i] for i in range(4))
        for row, poly in enumerate(forcing_polys):
            forcing[row, col] = poly.coeff_monomial(monomial)
    forcing_nonzeros = sum(entry != 0 for entry in forcing)
    check("HOMOGENEOUS_DEGREE_FOUR_FORCING_IS_IDENTICALLY_ZERO", forcing_nonzeros == 0)

    # Check row ordering and signs against the exact frozen z=1 owner vacuum.
    H, labels, faces0 = B.action_connection_hessian(sp.Integer(1))
    faces = C.with_base_phases(faces0)
    _A1, _A2, _M0, _M1, _M2, C0, _C1, _C2, _Dphase = C.blocks_all(H, faces, labels)
    J = H.col_join(C0)
    common_source = sp.zeros(136, 10)
    for phase in range(4):
        common_source[96 + 10 * phase:96 + 10 * (phase + 1), :] = sp.eye(10)
    augmented = J.row_join(common_source)
    r_h, r_joint, r_aug = rank_exact(H), rank_exact(J), rank_exact(augmented)
    check("CONNECTION_HESSIAN_RANK_94", r_h == 94)
    check("FROZEN_JOINT_RANK_95", r_joint == 95)
    check("COMMON_SOURCE_AUGMENTED_RANK_105", r_aug == 105)
    check("FULL_JOINT_LEFT_COKERNEL_DIMENSION_31", 136 - r_aug == 31)
    check(
        "DEGREE_FOUR_FORCING_ADDS_NO_COKERNEL_CLASS",
        rank_exact(augmented.row_join(forcing)) == r_aug,
    )

    result = {
        "schema": "a4d-y-curved-normaljet-degree4-gate-v1",
        "terminal": "A4D-Y-NORMALJET-DEGREE4-COCYCLE-ABSENT",
        "scope": "only the homogeneous degree-four part of the delta^2 normal-jet Euler forcing",
        "first_connection_tangent_degree": 1,
        "metric_gram_series": {
            "S_delta": "-T/2",
            "S_delta2": "3*r^2*T/40",
            "Q_delta": "T",
            "Q_delta2": "-2*r^2*T/5",
        },
        "joint_dimensions": {
            "connection_hessian_rank": r_h,
            "fixed_metric_joint_rank": r_joint,
            "joint_rows": 136,
            "common_source_augmented_rank": r_aug,
            "left_cokernel_after_common_source": 136 - r_aug,
        },
        "degree_four": {
            "homogeneous_monomial_count": len(monomials),
            "nonzero_forcing_entries": forcing_nonzeros,
            "exact_augmented_rank_with_all_forcing_columns": rank_exact(augmented.row_join(forcing)),
            "cokernel_obstruction_rank": 0,
        },
        "nonclaims": [
            "this certificate checks only the homogeneous degree-four slice and does not itself analyze lower-degree compatibility",
            "the degree-four gate alone does not prove a nonlinear curved stationary branch or refinement-uniform remainder",
        ],
    }
    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))
    print("TERMINAL", result["terminal"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
