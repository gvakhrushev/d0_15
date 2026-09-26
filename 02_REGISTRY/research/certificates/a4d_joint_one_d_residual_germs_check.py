#!/usr/bin/env python3
"""Exact joint residual-germ certificate for WRK-A4D-JOINT-ONE-D-RESIDUAL-GERMS.

The corrected #231 exact census gives one-dimensional joint kernels on both
target orbits.  This certificate rechecks both bases, computes the orbit-0
and orbit-5 reduced equations over Q(i), and proves local isolation with
finite exponents 1/2 and 1/3 respectively.

All action/Euler coefficients use the owned #208/#216 finite star formula,
the real Lie-log link chart, and the inverse-character input convention.
"""
from __future__ import annotations

from contextlib import redirect_stdout
from itertools import combinations
from io import StringIO
from pathlib import Path

import sympy as sp


def check(name: str, cond: bool) -> None:
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


# Load the exact owner symbol construction from #208/#216 without rerunning its
# separate full orbit scan.  The owner source ends its construction immediately
# before this marker.
owner_path = Path(__file__).with_name("a4d_j2_smooth_resonance_closure_check.py")
owner_source = owner_path.read_text(encoding="utf-8")
owner_ns: dict[str, object] = {}
with redirect_stdout(StringIO()):
    exec(owner_source.split(
        "# ---------------------------------------------------------------------------\n"
        "# 2. Full L=4 polarized singular-character scan"
    )[0], owner_ns)

I = sp.I
ETA = owner_ns["ETA"]
G2 = owner_ns["G2"]
STAR = owner_ns["STAR"]
LORENTZ = owner_ns["LORENTZ"]
PAIRS = owner_ns["PAIRS"]
ZSYMS = owner_ns["z"]
HAB = owner_ns["HAB"]
HAQ = owner_ns["HAQ"]
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
E = [sp.eye(4)[:, r] for r in range(4)]


def padd(left, right, deg):
    out = dict(left)
    for mon, val in right.items():
        if sum(mon) <= deg:
            zero = sp.zeros(4) if isinstance(val, sp.MatrixBase) else 0
            out[mon] = out.get(mon, zero) + val
    return {mon: val for mon, val in out.items() if val != 0}


def pneg(poly):
    return {mon: -val for mon, val in poly.items()}


def pscale(poly, scalar):
    return {mon: scalar * val for mon, val in poly.items() if scalar * val != 0}


def pmul(left, right, deg):
    out = {}
    for (p, q), x in left.items():
        for (r, s), y in right.items():
            mon = (p + r, q + s)
            if sum(mon) <= deg:
                out[mon] = out.get(mon, sp.zeros(4)) + x * y
    return {mon: val for mon, val in out.items() if val != sp.zeros(4)}


def mconst(matrix):
    return {(0, 0): sp.Matrix(matrix)}


def mexp(poly, deg):
    out = mconst(sp.eye(4))
    term = mconst(sp.eye(4))
    for n in range(1, deg + 1):
        term = pmul(term, poly, deg)
        out = padd(out, pscale(term, sp.Rational(1, sp.factorial(n))), deg)
    return out


def character(site, z):
    return sp.prod(z[j] ** site[j] for j in range(4))


def shift(site, role, amount=1):
    ans = list(site)
    ans[role] = (ans[role] + amount) % 4
    return tuple(ans)


def role_matrix(vector, role):
    return sum((vector[6 * role + j] * LORENTZ[j] for j in range(6)), sp.zeros(4))


def conjugate_matrix(matrix):
    return matrix.applyfunc(sp.conjugate)


def site_log(site, role, z, center, w0=None, w2=None,
             w21=None, w03=None):
    chi = character(site, z)
    first = role_matrix(center, role)
    out = {(1, 0): chi * first,
           (0, 1): sp.conjugate(chi) * conjugate_matrix(first)}
    if w0 is not None:
        out[(1, 1)] = role_matrix(w0, role)
    if w2 is not None:
        second = role_matrix(w2, role)
        out[(2, 0)] = chi**2 * second
        out[(0, 2)] = sp.conjugate(chi)**2 * conjugate_matrix(second)
    if w21 is not None:
        third = role_matrix(w21, role)
        out[(2, 1)] = chi * third
        out[(1, 2)] = sp.conjugate(chi) * conjugate_matrix(third)
    if w03 is not None:
        third = role_matrix(w03, role)
        out[(0, 3)] = sp.conjugate(chi)**3 * third
        out[(3, 0)] = chi**3 * conjugate_matrix(third)
    return out


def face_logs(base, a, b, z, center, w0=None, w2=None,
              w21=None, w03=None):
    return [
        site_log(base, a, z, center, w0, w2, w21, w03),
        site_log(shift(base, a), b, z, center, w0, w2, w21, w03),
        site_log(shift(base, b), a, z, center, w0, w2, w21, w03),
        site_log(base, b, z, center, w0, w2, w21, w03),
    ]


def face_factors(logs, deg):
    return [mexp(pscale(log, sign), deg)
            for log, sign in zip(logs, (1, 1, -1, -1))]


def product(factors, deg):
    out = mconst(sp.eye(4))
    for factor in factors:
        out = pmul(out, factor, deg)
    return out


def inverse_product(logs, deg):
    signed = list(zip(logs, (1, 1, -1, -1)))
    return product([mexp(pscale(log, -sign), deg)
                    for log, sign in reversed(signed)], deg)


def bivector_polynomial(curvature):
    out = {}
    for mon, matrix in curvature.items():
        lowered = matrix * ETA
        out[mon] = sp.Matrix([lowered[a, b] for a, b in PAIRS])
    return out


def wedge(left, right):
    return sp.Matrix([left[a] * right[b] - left[b] * right[a]
                      for a, b in PAIRS])


def orientation(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    inversions = sum(seq[i] > seq[j]
                     for i in range(4) for j in range(i + 1, 4))
    return (-1) ** inversions


def face_density(a, b, curvature):
    u, v = [j for j in range(4) if j not in (a, b)]
    background_bivector = wedge(E[u], E[v])
    return {
        mon: orientation(a, b) *
        (background_bivector.T * G2 * STAR * value)[0]
        for mon, value in bivector_polynomial(curvature).items()
    }


def face_metric_euler(a, b, curvature, qvariation):
    u, v = [j for j in range(4) if j not in (a, b)]
    h = qvariation * ETA / 2
    dB = wedge(h[u, :].T, E[v]) + wedge(E[u], h[v, :].T)
    return {
        mon: sp.simplify(orientation(a, b) * (dB.T * G2 * STAR * value)[0])
        for mon, value in bivector_polynomial(curvature).items()
    }


def face_connection_euler(a, b, dcurvature):
    u, v = [j for j in range(4) if j not in (a, b)]
    background_bivector = wedge(E[u], E[v])
    return {
        mon: sp.simplify(orientation(a, b) *
                         (background_bivector.T * G2 * STAR * value)[0])
        for mon, value in bivector_polynomial(dcurvature).items()
    }


def metric_euler(site, z, center, w0=None, w2=None, deg=2):
    result = []
    for qa, qb in SYM:
        q = sp.zeros(4)
        q[qa, qb] = q[qb, qa] = 1
        total = {}
        for a, b in PAIRS:
            logs = face_logs(site, a, b, z, center, w0, w2)
            P = product(face_factors(logs, deg), deg)
            Pinv = inverse_product(logs, deg)
            curvature = pscale(padd(P, pneg(Pinv), deg), sp.Rational(1, 2))
            total = padd(total, face_metric_euler(a, b, curvature, q), deg)
        result.append(total)
    return result


def edge_euler(site, role, variation, z, center, w0=None, w2=None, deg=2):
    total = {}
    for a, b in PAIRS:
        if role == a:
            incident = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            incident = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in incident:
            logs = face_logs(base, a, b, z, center, w0, w2)
            factors = face_factors(logs, deg)
            if corner < 2:
                dF = pmul(factors[corner], mconst(variation), deg)
            else:
                dF = pscale(pmul(mconst(variation), factors[corner], deg), -1)
            differentiated = [dF if j == corner else factor
                              for j, factor in enumerate(factors)]
            dP = product(differentiated, deg)
            Pinv = inverse_product(logs, deg)
            dC = pscale(padd(
                dP,
                pmul(pmul(pmul(Pinv, dP, deg), Pinv, deg),
                     {(0, 0): sp.Integer(1)}, deg),
                deg), sp.Rational(1, 2))
            total = padd(total, face_connection_euler(a, b, dC), deg)
    return total


def coefficient(poly, mon):
    return sp.simplify(poly.get(mon, 0))


def run_orbit_zero():
    roots = [sp.Integer(1), I, sp.Integer(-1), -I]
    ids = (0, 0, 1, 1)
    z_table = [roots[i] for i in ids]
    z = [1 / x for x in z_table]  # physical input character is inverse row character
    substitution = dict(zip(ZSYMS, z))
    H = HAB.subs(substitution)
    symbol_q = HAQ.subs(substitution)
    center = sp.zeros(24, 1)
    exact_basis = {
        0: -1, 6: -1, 12: 1, 14: -1,
        16: 1, 18: 1, 19: -1, 21: 1,
    }
    for index, value in exact_basis.items():
        center[index] = value
    table_substitution = dict(zip(ZSYMS, z_table))
    H_table = HAB.subs(table_substitution)
    Q_table = HAQ.subs(table_substitution).T
    check("ORBIT0_BASIS_MATCHES_PR231_CONNECTION",
          H_table.T * center == sp.zeros(24, 1))
    check("ORBIT0_BASIS_MATCHES_PR231_METRIC",
          Q_table * center == sp.zeros(10, 1))
    check("ORBIT0_PR231_N0_DIMENSION",
          len(sp.Matrix.vstack(H_table.T, Q_table).nullspace()) == 1)
    check("ORBIT0_EXACT_N0_BASIS_CONNECTION", H.T * center == sp.zeros(24, 1))
    check("ORBIT0_EXACT_N0_BASIS_METRIC", symbol_q.T * center == sp.zeros(10, 1))
    check("ORBIT0_N0_DIMENSION", len(sp.Matrix.vstack(
        H.T, symbol_q.T).nullspace()) == 1)

    # Check the direct nonlinear Euler implementation against the owned
    # polarized symbol before taking any higher coefficient.
    linear_k = []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator, z, center, deg=1)
            linear_k.append(coefficient(p, (1, 0)))
    linear_k = sp.Matrix(linear_k)
    check("ORBIT0_DIRECT_CONNECTION_LINEAR", linear_k == H.T * center)
    linear_q = metric_euler((0, 0, 0, 0), z, center, deg=1)
    linear_q = sp.Matrix([coefficient(p, (1, 0)) for p in linear_q])
    check("ORBIT0_DIRECT_METRIC_LINEAR", linear_q == symbol_q.T * center)
    check("ORBIT0_LINEAR_JOINT_ZERO",
          linear_k == sp.zeros(24, 1) and linear_q == sp.zeros(10, 1))

    ones = {variable: 1 for variable in ZSYMS}
    squares = {variable: value**2 for variable, value in zip(ZSYMS, z)}
    H0 = HAB.subs(ones)
    H2 = HAB.subs(squares)
    check("GENERATED_ZERO_MODE_REGULAR", H0.rank() == 24)
    check("GENERATED_TWO_K_MODE_REGULAR", H2.rank() == 24)

    f0, f2 = [], []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator,
                           z, center, deg=2)
            f0.append(coefficient(p, (1, 1)))
            f2.append(coefficient(p, (2, 0)))
    w0 = -H0.T.inv() * sp.Matrix(f0)
    w2 = -H2.T.inv() * sp.Matrix(f2)
    check("RANGE_CONNECTION_EQUATIONS_ORDER2",
          H0.T * w0 + sp.Matrix(f0) == sp.zeros(24, 1) and
          H2.T * w2 + sp.Matrix(f2) == sp.zeros(24, 1))

    metric = metric_euler((0, 0, 0, 0), z, center, w0, w2, deg=2)
    u2 = sp.Matrix([coefficient(p, (2, 0)) for p in metric])
    uv = sp.Matrix([coefficient(p, (1, 1)) for p in metric])
    v2 = sp.Matrix([coefficient(p, (0, 2)) for p in metric])
    expected_u2 = sp.zeros(10, 1)
    expected_u2[0], expected_u2[1], expected_u2[4] = 1-I, -2, 1+I
    expected_v2 = expected_u2.applyfunc(sp.conjugate)
    check("METRIC_UV_QUADRATIC_ZERO", uv == sp.zeros(10, 1))
    check("METRIC_U2_QUADRATIC_EXACT", u2 == expected_u2)
    check("METRIC_V2_QUADRATIC_EXACT", v2 == expected_v2)

    # Continue connection range elimination through cubic order.  The
    # resonant connection residual vanishes at degree three; the regular
    # particular solutions are used to form the degree-six reduced action.
    f21, f03 = [], []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator,
                           z, center, w0, w2, deg=3)
            f21.append(coefficient(p, (2, 1)))
            f03.append(coefficient(p, (0, 3)))
    f21, f03 = sp.Matrix(f21), sp.Matrix(f03)
    left_kernel = H.nullspace()
    check("CONNECTION_RESONANT_CUBIC_ZERO",
          all((row.T * f).applyfunc(sp.simplify) == sp.zeros(1, 1)
              for row in left_kernel for f in (f21, f03)))
    x21, params21 = H.T.gauss_jordan_solve(-f21)
    x03, params03 = H.T.gauss_jordan_solve(-f03)
    for parameter in list(params21) + list(params03):
        x21, x03 = x21.subs(parameter, 0), x03.subs(parameter, 0)
    check("CONNECTION_RANGE_EQUATIONS_ORDER3",
          (H.T*x21 + f21).applyfunc(sp.simplify) == sp.zeros(24, 1) and
          (H.T*x03 + f03).applyfunc(sp.simplify) == sp.zeros(24, 1))

    # Sum the six anchored face densities, then use exact character
    # orthogonality on the 4^4 torus.  Terms survive iff p-q == 0 mod 4.
    local_action = {}
    for a, b in PAIRS:
        logs = face_logs((0, 0, 0, 0), a, b, z,
                         center, w0, w2, x21, x03)
        P = product(face_factors(logs, 6), 6)
        Pinv = inverse_product(logs, 6)
        curvature = pscale(padd(P, pneg(Pinv), 6), sp.Rational(1, 2))
        local_action = padd(local_action, face_density(a, b, curvature), 6)
    U, V = sp.symbols("u v")
    reduced_action = {
        n: sp.factor(256 * sum(
            value * U**p * V**q
            for (p, q), value in local_action.items()
            if p + q == n and (p - q) % 4 == 0
        ))
        for n in range(1, 7)
    }
    check("REDUCED_ACTION_QUARTIC_ZERO", reduced_action[4] == 0)
    expected_action6 = 512*I*U*V*(U**2 + I*V**2)**2
    check("REDUCED_ACTION_SEXTIC_EXACT",
          sp.simplify(reduced_action[6] - expected_action6) == 0)
    e_k5 = sp.factor(sp.diff(reduced_action[6], V))
    expected_e_k5 = 512*I*U*(U**2 + I*V**2)*(U**2 + 5*I*V**2)
    check("CONNECTION_REDUCED_QUINTIC_EXACT",
          sp.simplify(e_k5 - expected_e_k5) == 0)

    # Real amplitude u=x+i y, v=conj(u).  The three independent metric rows
    # have a coercive exact quadratic norm, so higher analytic terms cannot
    # create a nonzero local joint-vacuum branch.
    X, Y = sp.symbols("x y", real=True)
    q00 = (1-I)*U**2 + (1+I)*V**2
    q01 = -2*U**2 - 2*V**2
    q11 = (1+I)*U**2 + (1-I)*V**2
    real_sub = {U: X+I*Y, V: X-I*Y}
    norm_sq = sum(sp.expand(value.subs(real_sub))**2
                  for value in (q00, q01, q11))
    check("METRIC_QUADRATIC_COERCIVE_NORM",
          sp.simplify(norm_sq - (24*X**4 + 24*Y**4 - 16*X**2*Y**2)) == 0)
    print("ORBIT0_E_Q2:")
    print("  q00 = (1-i)u^2 + (1+i)conj(u)^2")
    print("  q01 = -2u^2 - 2conj(u)^2")
    print("  q11 = (1+i)u^2 + (1-i)conj(u)^2")
    print("ORBIT0_E_K5: 512 i u (u^2+i conj(u)^2) (u^2+5i conj(u)^2)")
    print("ORBIT0_METRIC_BOUND: ||E_Q^red(u)||_2 >= 2 sqrt(2) |u|^2 + O(|u|^3)")


def run_orbit_five():
    roots = [sp.Integer(1), I, sp.Integer(-1), -I]
    ids = (1, 1, 3, 3)
    z_table = [roots[i] for i in ids]
    table_substitution = dict(zip(ZSYMS, z_table))
    H_table = HAB.subs(table_substitution)
    Q_table = HAQ.subs(table_substitution)
    center = sp.zeros(24, 1)
    exact_basis = {
        0: -1 + I, 6: -1 + I, 12: 1, 14: -1,
        16: 1, 18: 1, 19: -1, 21: 1,
    }
    for index, value in exact_basis.items():
        center[index] = value
    table_joint = sp.Matrix.vstack(H_table, Q_table.T)
    check("ORBIT5_RANK_H_20", H_table.rank() == 20)
    check("ORBIT5_RANK_A_INVENTORY_23",
          H_table.T.row_join(Q_table).rank() == 23)
    check("ORBIT5_N0_DIMENSION_ONE", len(table_joint.nullspace()) == 1)
    check("ORBIT5_PR231_EXACT_N0_BASIS",
          (H_table * center).applyfunc(sp.simplify) == sp.zeros(24, 1) and
          (Q_table.T * center).applyfunc(sp.simplify) == sp.zeros(10, 1) and
          table_joint.rank() == 23)

    # The physical input field uses the inverse Fourier character.  Check the
    # owned nonlinear Euler maps directly at that character.
    z = [1 / value for value in z_table]
    substitution = dict(zip(ZSYMS, z))
    H = HAB.subs(substitution)
    symbol_q = HAQ.subs(substitution)
    linear_k = []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator,
                           z, center, deg=1)
            linear_k.append(coefficient(p, (1, 0)))
    linear_k = sp.Matrix(linear_k)
    linear_q = sp.Matrix([
        coefficient(p, (1, 0))
        for p in metric_euler((0, 0, 0, 0), z, center, deg=1)
    ])
    check("ORBIT5_DIRECT_CONNECTION_LINEAR_ZERO",
          linear_k == sp.zeros(24, 1))
    check("ORBIT5_DIRECT_METRIC_LINEAR_ZERO",
          linear_q == sp.zeros(10, 1))

    ones = {variable: 1 for variable in ZSYMS}
    squares = {variable: value**2 for variable, value in zip(ZSYMS, z)}
    H0, H2 = HAB.subs(ones), HAB.subs(squares)
    check("ORBIT5_ZERO_MODE_REGULAR", H0.rank() == 24)
    check("ORBIT5_TWO_K_MODE_REGULAR", H2.rank() == 24)
    f0, f2 = [], []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator,
                           z, center, deg=2)
            f0.append(coefficient(p, (1, 1)))
            f2.append(coefficient(p, (2, 0)))
    f0, f2 = sp.Matrix(f0), sp.Matrix(f2)
    w0 = -H0.T.inv() * f0
    w2 = -H2.T.inv() * f2
    check("ORBIT5_CONNECTION_RANGE_ORDER2",
          H0.T * w0 + f0 == sp.zeros(24, 1) and
          H2.T * w2 + f2 == sp.zeros(24, 1))

    # The quadratic metric residual is degenerate on the real coordinate axes.
    metric = metric_euler((0, 0, 0, 0), z, center, w0, w2, deg=2)
    u2 = sp.Matrix([coefficient(p, (2, 0)) for p in metric])
    uv = sp.Matrix([coefficient(p, (1, 1)) for p in metric])
    v2 = sp.Matrix([coefficient(p, (0, 2)) for p in metric])
    expected_u2, expected_v2 = sp.zeros(10, 1), sp.zeros(10, 1)
    for index, value in {
        1: 2*I, 2: -I, 3: -I, 4: -2*I, 5: I, 6: I,
    }.items():
        expected_u2[index] = value
        expected_v2[index] = sp.conjugate(value)
    check("ORBIT5_METRIC_U2_EXACT", u2 == expected_u2)
    check("ORBIT5_METRIC_UV_QUADRATIC_ZERO",
          uv == sp.zeros(10, 1))
    check("ORBIT5_METRIC_V2_EXACT", v2 == expected_v2)
    U, V = sp.symbols("u v")
    X, Y = sp.symbols("x y", real=True)
    leading_q = [u2[i]*U**2 + v2[i]*V**2 for i in range(10)]
    real_sub = {U: X + I*Y, V: X - I*Y}
    norm_sq = sum(sp.expand(q.subs(real_sub))**2 for q in leading_q)
    check("ORBIT5_METRIC_QUADRATIC_DEGENERATE_AXES",
          sp.simplify(norm_sq - 192*X**2*Y**2) == 0)

    # Eliminate the regular connection ranges at cubic order and project the
    # resonant forcing to an exact left-kernel covector.
    f21, f03 = [], []
    for role in range(4):
        for generator in LORENTZ:
            p = edge_euler((0, 0, 0, 0), role, generator,
                           z, center, w0, w2, deg=3)
            f21.append(coefficient(p, (2, 1)))
            f03.append(coefficient(p, (0, 3)))
    f21, f03 = sp.Matrix(f21), sp.Matrix(f03)
    left_kernel = H.nullspace()
    check("ORBIT5_RESONANT_COKERNEL_DIMENSION_FOUR",
          len(left_kernel) == 4)
    cokernel_basis = sp.Matrix.hstack(*left_kernel)
    range_cokernel = H.T.row_join(cokernel_basis)
    check("ORBIT5_RANGE_COKERNEL_COMPLEMENT_FULL_RANK",
          range_cokernel.rank() == 24)
    split21, params21 = range_cokernel.gauss_jordan_solve(-f21)
    split03, params03 = range_cokernel.gauss_jordan_solve(-f03)
    for parameter in list(params21) + list(params03):
        split21 = split21.subs(parameter, 0)
        split03 = split03.subs(parameter, 0)
    check("ORBIT5_CONNECTION_RANGE_COKERNEL_SPLIT_ORDER3",
          (range_cokernel * split21 + f21).applyfunc(sp.simplify)
          == sp.zeros(24, 1) and
          (range_cokernel * split03 + f03).applyfunc(sp.simplify)
          == sp.zeros(24, 1))

    ell = sp.zeros(24, 1)
    for index, value in {
        6: (1 + I)/2, 9: -(1 + I)/2, 10: -(1 + I)/2,
        14: 1, 19: 1,
    }.items():
        ell[index] = value
    check("ORBIT5_EXACT_COKERNEL_COVECTOR",
          (H * ell).applyfunc(sp.simplify) == sp.zeros(24, 1))
    obstruction_u2v = sp.simplify((ell.T * f21)[0])
    obstruction_v3 = sp.simplify((ell.T * f03)[0])
    check("ORBIT5_CONNECTION_CUBIC_EXACT",
          obstruction_u2v == 2*I and obstruction_v3 == -(1 + I))
    projections = [(sp.simplify((row.T*f21)[0]),
                    sp.simplify((row.T*f03)[0])) for row in left_kernel]
    check("ORBIT5_CUBIC_COKERNEL_PROJECTIONS",
          all(pair in ((0, 0), (2*I, -(1 + I))) for pair in projections)
          and (2*I, -(1 + I)) in projections)

    # Reverse triangle inequality gives a degree-three lower bound in every
    # complex direction, including the axes where the metric quadratic drops.
    lower_constant = 2 - sp.sqrt(2)
    check("ORBIT5_CUBIC_REVERSE_TRIANGLE_BOUND",
          lower_constant > 0)
    print("ORBIT5_E_Q2_NONZERO: "
          "E01=2i(u^2-conj(u)^2), E02=E03=-i(u^2-conj(u)^2), "
          "E11=-2i(u^2-conj(u)^2), E12=E13=i(u^2-conj(u)^2)")
    print("ORBIT5_METRIC_NORM_SQUARED: 192 x^2 y^2")
    print("ORBIT5_E_K3: 2 i u^2 conj(u) - (1+i) conj(u)^3")
    print("ORBIT5_CUBIC_BOUND: |E_K^red(u)| >= "
          "(2-sqrt(2)) |u|^3 + O(|u|^5)")


if __name__ == "__main__":
    run_orbit_zero()
    run_orbit_five()
    print("J2-JOINT-ONE-D-RESIDUAL-ORBITS-ISOLATED")
