#!/usr/bin/env python3
"""Exact cubic zero-momentum vertex of low-frequency Y center waves.

Differentiate the reduced quadratic center symbol along the boost-dual
connection-stationary family. The Y-Y entry vanishes in every shift
direction. This is a finite Taylor coefficient at z=1, not a global
continuation or response theorem.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_normaljet_compatibility_check as C
import a4d_y_curved_response_quotient_check as B
import a4d_y_slow_exact_plane_check as E

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_center_wave_cubic_vertex_results.json"
Y_SYMBOL = "a4d_y_center_envelope_symbol_results.json"
JET_SOURCE = "a4d_y_curved_normaljet_degree2_obstruction_results.json"
DUAL_SOURCE = "a4d_y_dual_center_joint_visibility_results.json"
I4 = B.I4
GEN = B.GEN
PAIRS = B.PAIRS


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ).rank()


def build_hessian(z: sp.Expr, d: sp.Expr):
    """Literal period-four connection Hessian on the exact U*Cayley(B) path."""
    Y = GEN[3] - GEN[4] + GEN[5]
    boost = GEN[0] + GEN[1] + GEN[2]
    U = E.cayley_simple(Y, 3, z)
    Cminus = E.cayley_simple(boost, -3, -d)
    Cplus = E.cayley_simple(boost, -3, d)
    waves = [U * Cminus, I4, B.linv(U) * Cplus, I4]
    labels = [(phase, role, generator)
              for phase in range(4) for role in range(4) for generator in range(6)]
    index = {label: i for i, label in enumerate(labels)}
    basis = [I4[:, j] for j in range(4)]
    H = sp.zeros(96)
    face_data = []
    for phase in range(4):
        for a, b in PAIRS:
            locs = [
                (phase, a, False),
                ((phase + 1) % 4, b, False),
                ((phase + 1) % 4, a, True),
                (phase, b, True),
            ]
            factors, first = [], []
            for q, role, inverse in locs:
                link = waves[q] if role == 0 else I4
                factor = B.linv(link) if inverse else link
                factors.append(factor)
                first.append([(-X * factor if inverse else factor * X) for X in GEN])
            local = []
            for position, (q, role, _inverse) in enumerate(locs):
                for generator in range(6):
                    local.append((position, generator, index[(q, role, generator)]))
            u, v = [j for j in range(4) if j not in (a, b)]
            area = B.wedge(basis[u], basis[v])
            Hloc = sp.zeros(24)
            for i, (pi, gi, _global_i) in enumerate(local):
                for j in range(i, 24):
                    pj, gj, _global_j = local[j]
                    if pi == pj:
                        Q = B.symxy(GEN[gi], GEN[gj])
                        Q = Q * factors[pi] if locs[pi][2] else factors[pi] * Q
                        d2P = I4
                        for n, factor in enumerate(factors):
                            d2P = d2P * (Q if n == pi else factor)
                    else:
                        d2P = I4
                        for n, factor in enumerate(factors):
                            item = first[n][gi] if n == pi else first[n][gj] if n == pj else factor
                            d2P = d2P * item
                    d2F = (d2P - B.linv(d2P)) / 2
                    value = sp.cancel(
                        B.orientation(a, b)
                        * (area.T * B.G2 * B.STAR * B.biv(d2F))[0]
                    )
                    Hloc[i, j] = Hloc[j, i] = value
            for i, (_pi, _gi, global_i) in enumerate(local):
                for j, (_pj, _gj, global_j) in enumerate(local):
                    H[global_i, global_j] += Hloc[i, j]
            face_data.append((a, b, locs, local, Hloc, factors))
    return H.applyfunc(sp.cancel), labels, face_data


def center_basis(z: sp.Expr, labels) -> sp.Matrix:
    index = {label: i for i, label in enumerate(labels)}
    y, dual = sp.zeros(96, 1), sp.zeros(96, 1)
    for phase, sign in ((0, 1), (2, -1)):
        for generator, coefficient in ((3, 1), (4, -1), (5, 1)):
            y[index[(phase, 0, generator)], 0] = (
                sign * sp.Rational(4) / (4 + 3 * z**2) * coefficient
            )
    for phase, sign in ((0, -1), (2, 1)):
        for generator in (0, 1, 2):
            dual[index[(phase, 0, generator)], 0] = sign
    return sp.Matrix.hstack(y, dual)


def reduced_symbol_derivative(H, N, A1, A2, z, d):
    M = H.row_join(N).col_join(N.T.row_join(sp.zeros(2)))
    at = {z: sp.Integer(1), d: sp.Integer(0)}
    M0 = M.subs(at).applyfunc(sp.factor)
    Md = M.diff(d).subs(at).applyfunc(sp.factor)
    N0 = N.subs(at).applyfunc(sp.factor)
    Nd = N.diff(d).subs(at).applyfunc(sp.factor)
    solutions = []
    for direction in range(4):
        rhs = sp.zeros(98, 2)
        rhs[:96, :] = -A1[direction] * N
        rhs0 = rhs.subs(at).applyfunc(sp.factor)
        rhsd = rhs.diff(d).subs(at).applyfunc(sp.factor)
        def solve(value):
            return DomainMatrix.from_Matrix(M0).convert_to(QQ).lu_solve(
                DomainMatrix.from_Matrix(value).convert_to(QQ)
            ).to_Matrix()
        sol0 = solve(rhs0)
        sold = solve((rhsd - Md * sol0).applyfunc(sp.factor))
        check(f"BORDERED_RANGE_EQUATION_{direction}", M0 * sol0 == rhs0)
        check(f"BORDERED_DERIVATIVE_EQUATION_{direction}",
              M0 * sold + Md * sol0 == rhsd)
        solutions.append((sol0[:96, :], sold[:96, :]))
    A10 = [A1[i].subs(at).applyfunc(sp.factor) for i in range(4)]
    A1d = [A1[i].diff(d).subs(at).applyfunc(sp.factor) for i in range(4)]
    A20 = {ij: A2[ij].subs(at).applyfunc(sp.factor) for ij in C.DIRPAIRS}
    A2d = {ij: A2[ij].diff(d).subs(at).applyfunc(sp.factor) for ij in C.DIRPAIRS}
    symbol0, derivative = {}, {}
    for i, j in C.DIRPAIRS:
        Yi0, Yid = solutions[i]
        Yj0, Yjd = solutions[j]
        if i == j:
            T0 = A20[(i, j)] * N0 + A10[i] * Yi0
            Td = (A2d[(i, j)] * N0 + A20[(i, j)] * Nd
                  + A1d[i] * Yi0 + A10[i] * Yid)
        else:
            T0 = A20[(i, j)] * N0 + A10[i] * Yj0 + A10[j] * Yi0
            Td = (A2d[(i, j)] * N0 + A20[(i, j)] * Nd
                  + A1d[i] * Yj0 + A10[i] * Yjd
                  + A1d[j] * Yi0 + A10[j] * Yid)
        symbol0[(i, j)] = (N0.T * T0).applyfunc(sp.factor)
        derivative[(i, j)] = (Nd.T * T0 + N0.T * Td).applyfunc(sp.factor)
    return symbol0, derivative, N0, Nd


def run(write: bool = False) -> dict:
    z, d = sp.symbols("z d", real=True)
    print("BUILDING_EXACT_TWO_PARAMETER_HESSIAN", flush=True)
    H, labels, faces = build_hessian(z, d)
    phase_faces = C.with_base_phases(faces)
    N = center_basis(z, labels)
    A1, A2, *_ = C.blocks_all(H, phase_faces, labels)
    at = {z: sp.Integer(1), d: sp.Integer(0)}
    H0 = H.subs(at).applyfunc(sp.factor)
    N0 = N.subs(at).applyfunc(sp.factor)
    H_owner, labels_owner, _ = B.action_connection_hessian(sp.Integer(1))
    check("BASE_HESSIAN_MATCHES_OWNER", labels == labels_owner and H0 == H_owner)
    check("CENTER_BASIS_MATCHES_OWNER",
          N0 == C.centers(H_owner, labels_owner, sp.Integer(1)))
    check("EXACT_CENTER_KERNEL", H0 * N0 == sp.zeros(96, 2) and N0.rank() == 2)
    check("CONNECTION_HESSIAN_RANK_94", exact_rank(H0) == 94)
    dual_owner = json.loads((HERE / DUAL_SOURCE).read_text())
    check("DUAL_PATH_IS_EXACT_CONNECTION_STATIONARY",
          dual_owner["connection_euler"] == "all 96 rows vanish identically")
    print("BUILDING_SHIFT_MOMENTS", flush=True)
    symbol0, derivative, N0, Nd = reduced_symbol_derivative(H, N, A1, A2, z, d)
    check("DUAL_CENTER_BASIS_HAS_ZERO_FIRST_DERIVATIVE", Nd == sp.zeros(96, 2))
    old = json.loads((HERE / Y_SYMBOL).read_text())
    owner_symbol = {
        tuple(map(int, key)): sp.Matrix([[sp.Rational(x) for x in row] for row in value])
        for key, value in old["quadratic_coefficients"].items()
    }
    check("REDUCED_SYMBOL_MATCHES_PINNED_Y_OWNER",
          all(symbol0[key] == value for key, value in owner_symbol.items()))
    yy_zero = all(derivative[key][0, 0] == 0 for key in C.DIRPAIRS)
    dd_zero = all(derivative[key][1, 1] == 0 for key in C.DIRPAIRS)
    mixed_nonzero = any(derivative[key][0, 1] != 0 for key in C.DIRPAIRS)
    check("DUAL_COKERNEL_YY_CUBIC_VERTEX_VANISHES", yy_zero)
    check("DUAL_COKERNEL_DD_CUBIC_VERTEX_VANISHES", dd_zero)
    check("DUAL_COKERNEL_MIXED_CUBIC_VERTEX_IS_NONZERO", mixed_nonzero)
    jet = json.loads((HERE / JET_SOURCE).read_text())
    coker = jet["connection_only_jet"]["constant_center_cokernel"]
    source = [sp.Rational(x) for x in coker["stationary_seed_projected_source"]]
    left_rows = sp.Matrix(coker["left_kernel_basis_rows"])
    check("DUAL_COKERNEL_CURVATURE_SOURCE_IS_NONZERO", source[0] > 0)
    check("LEFT_COKERNEL_ROWS_MATCH_DUAL_AND_NEGATIVE_Y",
          left_rows[0, :] == N0[:, 1].T
          and left_rows[1, :] == -sp.Rational(7, 4) * N0[:, 0].T)

    result = {
        "schema": "a4d-y-center-wave-cubic-vertex-v1",
        "base": "flat exact period-four Y vacuum, z=1, standard solder",
        "dual_direction": "exact connection-stationary Cayley(B,-d) path; B=K1+K2+K3",
        "method": "differentiate the exact bordered range solve for the quadratic reduced center symbol",
        "shift_pairs": [f"{i}{j}" for i, j in C.DIRPAIRS],
        "reduced_symbol_d_dual": {
            f"{i}{j}": [[str(derivative[(i, j)][a, b]) for b in range(2)]
                         for a in range(2)]
            for i, j in C.DIRPAIRS
        },
        "yy_entry_d_dual_all_pairs_zero": yy_zero,
        "dd_entry_d_dual_all_pairs_zero": dd_zero,
        "yd_entry_d_dual_has_nonzero_coefficients": mixed_nonzero,
        "constant_center_cokernel_basis": [
            "boost-dual tangent N_D^T", "negative Y tangent -N_Y^T"
        ],
        "curvature_squared_cokernel_source": [str(x) for x in source],
        "quadratic_low_frequency_consequence": (
            "a pair of opposite low-frequency Y-center modes has zero leading "
            "quadratic contribution to the dual constant-center cokernel; only "
            "mixed Y/dual center waves contribute at this flat cubic order"
        ),
        "scope_fence": [
            "flat-background cubic vertex only, at z=1",
            "does not include nonzero Bloch/resonance strata or aliasing",
            "does not include curved-background cubic vertices or higher interactions",
            "does not prove a nonlinear branch or a global response limit",
        ],
    }
    if OUT.exists() and not write:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    print("TERMINAL A4D-Y-DUAL-COKERNEL-LOW-FREQUENCY-YY-VERTEX-ZERO", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
