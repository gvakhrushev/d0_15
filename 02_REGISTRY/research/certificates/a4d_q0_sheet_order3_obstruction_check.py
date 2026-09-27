#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Order-eps^3 obstruction on the selected mode-A sheet.

The selected branch has zero first link tangent and the unique order-eps^2
repair p2 from a4d_q0_stationary_sheet_stress_check.py. This certificate
shows that the resulting order-eps^3 connection Euler lies outside the image
of the vacuum connection Hessian at character (i,i,-i,-i).

It does not rule out a different order-eps^1 kernel tangent, and it is not a
physical no-go.
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + ((" :: " + detail) if detail else ""))


PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
INC = (1, 1, -1, -1)
P2_BLOCK = (0, -4, -4, 4, 4, 0)
LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE", STAR * STAR == -sp.eye(6))


def orient(face) -> int:
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge(u, v):
    return sp.Matrix([sp.expand(u[a] * v[b] - u[b] * v[a]) for a, b in PAIRS])


def shift(phase: int, role: int) -> int:
    return (phase + INC[role]) % 4


z = (sp.I, sp.I, -sp.I, -sp.I)
dvec = sp.Matrix([sp.simplify(1 / z[r] - 1) for r in range(4)])
q = sp.expand(dvec * dvec.T)
eps, sval = sp.symbols("eps s")
Y = [sum((P2_BLOCK[g] * LORENTZ[g] for g in range(6)), sp.zeros(4)) for _ in range(4)]


def h_of(phase: int):
    chi = sp.I ** phase
    return sp.expand(q * chi + sp.conjugate(q * chi))


def frame(phase: int):
    h = h_of(phase)
    H = sp.expand(h * ETA / 2)
    S = sp.expand(-(h * ETA) ** 2 / 8)
    U = sp.expand((h * ETA) ** 3 / 16)
    return h, H, S, U


for phase in range(4):
    h, H, S, U = frame(phase)
    Theta = I4 + eps * H + eps ** 2 * S + eps ** 3 * U
    err = sp.expand(Theta * ETA * Theta.T - ETA - eps * h)
    ok = all(
        sp.Matrix([[sp.expand(err[i, j]).coeff(eps, n) for j in range(4)] for i in range(4)])
        == sp.zeros(4)
        for n in range(4)
    )
    check("GRAM_THROUGH_EPS3_PHASE_%d" % phase, ok)


def face_bivector(phase: int):
    _h, H, S, U = frame(phase)
    return H, S, U


def euler(use_p2: bool):
    result = {phase: [sp.Integer(0) for _ in range(24)] for phase in range(4)}
    for base in range(4):
        _h, H, S, U = frame(base)
        for r, sf in PAIRS:
            u, v = [i for i in range(4) if i not in (r, sf)]
            Bu = I4[:, u] + eps * H.row(u).T + eps ** 2 * S.row(u).T + eps ** 3 * U.row(u).T
            Bv = I4[:, v] + eps * H.row(v).T + eps ** 2 * S.row(v).T + eps ** 3 * U.row(v).T
            B = wedge(Bu, Bv)
            specs = [(base, r), (shift(base, r), sf), (shift(base, sf), r), (base, sf)]
            mats = []
            for ph, role in specs:
                M = I4
                if use_p2:
                    M = M + eps ** 2 * ((-1) ** ph) * Y[role]
                mats.append(M)
            P = mats[0] * mats[1] * mats[2].inv() * mats[3].inv()
            Pinv = P.inv()
            sign = orient((r, sf))
            for n, (ph, role) in enumerate(specs):
                for g, gen in enumerate(LORENTZ):
                    L1, L2, L3, L4 = mats
                    if n == 0:
                        dP = gen * L2 * L3.inv() * L4.inv()
                    elif n == 1:
                        dP = L1 * gen * L3.inv() * L4.inv()
                    elif n == 2:
                        dP = L1 * L2 * (-L3.inv() * gen * L3.inv()) * L4.inv()
                    else:
                        dP = L1 * L2 * L3.inv() * (-L4.inv() * gen * L4.inv())
                    dR = (dP + Pinv * dP * Pinv) / 2
                    bend = sp.Matrix([(dR * ETA)[a, b] for a, b in PAIRS])
                    raw = sign * (B.T * G2 * STAR * bend)[0]
                    series = sp.series(sp.expand(raw), eps, 0, 4).removeO()
                    result[ph][6 * role + g] = sp.expand(result[ph][6 * role + g] + series)
    return result


def coeff_matrix(eulers, order: int):
    return [
        sp.Matrix([sp.expand(eulers[phase][i]).coeff(eps, order) for i in range(24)])
        for phase in range(4)
    ]


def fourier(vecs, mode: int):
    acc = sp.zeros(24, 1)
    for phase, vec in enumerate(vecs):
        acc += sp.conjugate(sp.I ** mode) ** phase * vec
    return sp.simplify(acc)


print("computing corrected Euler")
corrected = euler(True)
bare = euler(False)
bare2 = coeff_matrix(bare, 2)
real_fa = bare2[0]
check("BARE_ORDER2_PHASE0_NONZERO", real_fa != sp.zeros(24, 1))
for phase in range(4):
    check(
        "BARE_ORDER2_PHASE_%d" % phase,
        sp.simplify(bare2[phase] - ((-1) ** phase) * real_fa) == sp.zeros(24, 1),
    )
for order in (0, 1, 2):
    mats = coeff_matrix(corrected, order)
    check(
        "CORRECTED_ORDER_%d_ZERO" % order,
        all(vec == sp.zeros(24, 1) for vec in mats),
    )
order3 = coeff_matrix(corrected, 3)
mode_coeffs = [fourier(order3, mode) for mode in range(4)]
check("ORDER3_MODES_0_AND_2_ZERO", mode_coeffs[0] == sp.zeros(24, 1) and mode_coeffs[2] == sp.zeros(24, 1))
check(
    "ORDER3_MODE1_AMPLITUDE",
    sp.simplify(mode_coeffs[1] - 4 * (-2 + 2 * sp.I) * real_fa) == sp.zeros(24, 1),
)
check(
    "ORDER3_MODE3_IS_CONJUGATE",
    sp.simplify(mode_coeffs[3] - sp.conjugate(mode_coeffs[1])) == sp.zeros(24, 1),
)


def B_of(r, s):
    u, v = [i for i in range(4) if i not in (r, s)]
    B = sp.zeros(6, 1)
    if u < v:
        B[PINDEX[(u, v)]] = 1
    else:
        B[PINDEX[(v, u)]] = -1
    return B


def fourier_column(active_role: int, active_gen: int, chi):
    local = {phase: sp.zeros(24, 1) for phase in range(4)}
    for base in range(4):
        for r, sf in PAIRS:
            specs = [(base, r), (shift(base, r), sf), (shift(base, sf), r), (base, sf)]
            mats = []
            for ph, role in specs:
                M = I4
                if role == active_role:
                    M = M + sval * chi(ph) * LORENTZ[active_gen]
                mats.append(M)
            holonomy = mats[0] * mats[1] * mats[2].inv() * mats[3].inv()
            holonomy_inv = holonomy.inv()
            sign = orient((r, sf))
            B = B_of(r, sf)
            for n, (ph, role) in enumerate(specs):
                for g, gen in enumerate(LORENTZ):
                    L1, L2, L3, L4 = mats
                    if n == 0:
                        dP = gen * L2 * L3.inv() * L4.inv()
                    elif n == 1:
                        dP = L1 * gen * L3.inv() * L4.inv()
                    elif n == 2:
                        dP = L1 * L2 * (-L3.inv() * gen * L3.inv()) * L4.inv()
                    else:
                        dP = L1 * L2 * L3.inv() * (-L4.inv() * gen * L4.inv())
                    dR = (dP + holonomy_inv * dP * holonomy_inv) / 2
                    bend = sp.Matrix([(dR * ETA)[a, b] for a, b in PAIRS])
                    raw = sign * (B.T * G2 * STAR * bend)[0]
                    lin = sp.series(sp.expand(raw), sval, 0, 2).removeO().coeff(sval, 1)
                    if lin != 0:
                        local[ph][6 * role + g] += sp.expand(lin)
    acc = sp.zeros(24, 1)
    for phase in range(4):
        acc += sp.conjugate(chi(phase)) * local[phase]
    return sp.simplify(acc)


def hessian(chi):
    return sp.Matrix.hstack(*[
        fourier_column(role, gen, chi) for role in range(4) for gen in range(6)
    ])


print("building character -1 control")
H_minus = hessian(lambda phase: (-1) ** phase)
p2 = sp.Matrix(list(P2_BLOCK) * 4)
check("CHAR_MINUS_RANK_24", H_minus.rank() == 24)
check(
    "P2_CANCELS_IN_HESSIAN_NORMALIZATION",
    sp.simplify(H_minus * p2 + 4 * real_fa) == sp.zeros(24, 1),
)

print("building character i")
H_i = hessian(lambda phase: sp.I ** phase)
force = mode_coeffs[1]
check("CHAR_I_RANK_20", H_i.rank() == 20)
check("ORDER3_FORCE_NOT_IN_IMAGE", H_i.row_join(force).rank() == 21)
left = H_i.T.nullspace()
check("LEFT_KERNEL_NONEMPTY", len(left) == 4)
pairings = [sp.simplify((v.T * force)[0]) for v in left]
check("LEFT_KERNEL_SEES_FORCE", any(value != 0 for value in pairings))
print("OBSTRUCTION_PAIRINGS", pairings)

if FAILS:
    print("A4D-Q0-SELECTED-BRANCH-ORDER3-OBSTRUCTION: FAIL (%d)" % len(FAILS))
    for name in FAILS:
        print("  - " + name)
    raise SystemExit(1)

print("A4D-Q0-SELECTED-BRANCH-ORDER3-OBSTRUCTION")
print("SELECTED_BRANCH: zero order-eps link tangent, then p2 at order eps^2.")
print("ORDER3: forcing on (i,i,-i,-i) is outside the rank-20 connection Hessian.")
print("SCOPE: other order-eps kernel tangents are not excluded; not a physical no-go.")
