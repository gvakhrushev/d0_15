#!/usr/bin/env python3
"""Diagonal quarter-wave source-invisible joint germ.

Consumes the orbit-4 N_0 basis certified by
a4d_joint_resonance_kernel_census.json (WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL,
merged as PR #252). At q = 0 the regular connection block of H_AA is
invertible on a complement of the 8-dimensional diagonal kernel, which is the
#216 range elimination. The source-invisible coordinates are the 4-dimensional
kernel of H_QA on that kernel.

The polarized curvature_mixed scalar vanishes on that four-space. The odd
plaquette holonomy (P - P^{-1})/2 is then expanded with the regular
coordinates set to zero. That truncation is not a Lyapunov-Schmidt
elimination: a solved correction r(u)=O(u^2) can still enter E_Q at
quadratic order. The affine coframe descent is not a gauge deletion of
those regular variables.

No new action channel, torsion constraint, or Einstein equation is used.
"""

from itertools import combinations
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
CENSUS = ROOT / "02_REGISTRY/research/certificates/a4d_joint_resonance_kernel_census.json"

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
SIGMA = [1, 0, -1, 0]


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def rot(i, j):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    return X


def boost(i):
    X = sp.zeros(4)
    X[0, i] = X[i, 0] = 1
    return X


GEN = [boost(1), boost(2), boost(3), rot(1, 2), rot(1, 3), rot(2, 3)]
for X in GEN:
    check("LORENTZ_TANGENT", sp.expand(X.T * ETA + ETA * X) == sp.zeros(4))

G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE", STAR * STAR == -sp.eye(6))


def wedge_vec(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X):
    Ym = X * ETA
    return sp.Matrix([Ym[a, b] for a, b in PAIRS])


def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def mul_jet4(X, Ym):
    return (
        X[0] * Ym[0],
        X[0] * Ym[1] + X[1] * Ym[0],
        X[0] * Ym[2] + X[2] * Ym[0],
        X[0] * Ym[3] + X[1] * Ym[2] + X[2] * Ym[1] + X[3] * Ym[0],
    )


def exp_link4(A0, B0, phase_a=1, phase_b=1, inverse=False):
    sign = -1 if inverse else 1
    return (
        sp.eye(4),
        sign * phase_a * A0,
        sign * phase_b * B0,
        sp.Rational(1, 2) * phase_a * phase_b * (A0 * B0 + B0 * A0),
    )


def curvature_mixed(P):
    return P[3] - sp.Rational(1, 2) * (P[1] * P[2] + P[2] * P[1])


Z = [sp.I, sp.I, sp.I, sp.I]
avars = sp.symbols("a0:24")
bvars = sp.symbols("b0:24")
A, Bc = [], []
for r in range(4):
    YA = sp.zeros(4)
    YB = sp.zeros(4)
    for j, gen in enumerate(GEN):
        YA += avars[6 * r + j] * gen
        YB += bvars[6 * r + j] * gen
    A.append(YA)
    Bc.append(YB)
basis_cols = [sp.eye(4)[:, r] for r in range(4)]
connection_bilinear = 0
for r, s in PAIRS:
    Pj = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    Pj = mul_jet4(Pj, exp_link4(A[r], Bc[r]))
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], Z[r], 1 / Z[r]))
    Pj = mul_jet4(Pj, exp_link4(A[r], Bc[r], Z[s], 1 / Z[s], inverse=True))
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], inverse=True))
    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis_cols[u], basis_cols[v])
    connection_bilinear += complement_orientation((r, s)) * (
        B0.T * G2 * STAR * bivector_of_tangent(curvature_mixed(Pj))
    )[0]
connection_bilinear = sp.expand(connection_bilinear)
HAB = sp.zeros(24)
for i in range(24):
    di = sp.diff(connection_bilinear, avars[i])
    for j in range(24):
        HAB[i, j] = sp.diff(di, bvars[j])

hvars = sp.symbols("h0:16")
hlegs = [sp.Matrix(hvars[4 * r: 4 * r + 4]) for r in range(4)]
cross = 0
for r, s in PAIRS:
    C1 = (1 / Z[r] - 1) * Bc[s] - (1 / Z[s] - 1) * Bc[r]
    u, v = [i for i in range(4) if i not in (r, s)]
    B1 = wedge_vec(hlegs[u], basis_cols[v]) + wedge_vec(basis_cols[u], hlegs[v])
    cross += complement_orientation((r, s)) * (
        B1.T * G2 * STAR * bivector_of_tangent(C1)
    )[0]
cross = sp.expand(cross)
HAH = sp.zeros(24, 16)
for i in range(24):
    di = sp.diff(cross, bvars[i])
    for j in range(16):
        HAH[i, j] = sp.diff(di, hvars[j])
SYM = [(a0, b0) for a0 in range(4) for b0 in range(a0, 4)]
Bmet = sp.zeros(16, 10)
for j, (a0, b0) in enumerate(SYM):
    q = sp.zeros(4)
    q[a0, b0] = q[b0, a0] = 1
    H = sp.Rational(1, 2) * q * ETA
    for r in range(4):
        for c0 in range(4):
            Bmet[4 * r + c0, j] = H[r, c0]
HAQ = sp.expand(HAH * Bmet)
quarter = {avars[i]: 0 for i in range(24)}  # placeholder to keep names local
del quarter
Hq = HAB
Sq = HAQ


def kv(entries):
    vector = sp.zeros(24, 1)
    for idx, val in entries.items():
        vector[idx] = val
    return vector


KERNEL = [
    kv({0: 1, 1: 1, 2: 1}),
    kv({3: 1, 4: -1, 5: 1}),
    kv({6: 1, 9: 1, 10: 1}),
    kv({7: 1, 8: -1, 11: 1}),
    kv({12: 1, 14: -1, 16: 1}),
    kv({13: 1, 15: -1, 17: 1}),
    kv({18: 1, 19: -1, 21: 1}),
    kv({20: -1, 22: 1, 23: 1}),
]
K = sp.Matrix.hstack(*KERNEL)
check("DIAGONAL_H_RANK_16", Hq.rank() == 16)
check("DIAGONAL_KERNEL", Hq * K == sp.zeros(24, 8))
PAIR = sp.expand(Sq.T * K)
NULL = PAIR.nullspace()
check("N0_DIMENSION_4", len(NULL) == 4)
INVISIBLE_INDEX = [1, 3, 4, 6]
for vec, idx in zip(NULL, INVISIBLE_INDEX):
    target = sp.zeros(8, 1)
    target[idx] = 1
    check("N0_BASIS_%d" % idx, sp.expand(vec - target) == sp.zeros(8, 1))

census = json.loads(CENSUS.read_text(encoding="utf-8"))
orbit4 = census["n0_bases"]["4"]
check("CENSUS_ORBIT4_IDS", orbit4["ids"] == [1, 1, 1, 1])
check("CENSUS_ORBIT4_DIM", len(orbit4["basis"]) == 4)
for col, idx in zip(orbit4["basis"], INVISIBLE_INDEX):
    got = sp.Matrix([sp.sympify(x) for x in col])
    check("CENSUS_MATCHES_KERNEL_%d" % idx, sp.expand(got - KERNEL[idx]) == sp.zeros(24, 1))
    check("CENSUS_VECTOR_IN_KER_H_%d" % idx, Hq * got == sp.zeros(24, 1))
    check("CENSUS_VECTOR_IN_KER_QA_%d" % idx, sp.expand(Sq.T * got) == sp.zeros(10, 1))

# #216 range elimination at q = 0: H_AA is invertible on a complement of ker.
regular_cols = []
span = K
for i in range(24):
    trial = sp.Matrix.hstack(span, sp.eye(24)[:, i])
    if trial.rank() == span.cols + 1:
        regular_cols.append(sp.eye(24)[:, i])
        span = trial
R = sp.Matrix.hstack(*regular_cols)
check("REGULAR_COMPLEMENT_RANK_24", span.rank() == 24)
check("REGULAR_BLOCK_INJECTIVE", (Hq * R).rank() == 16)
# Visible resonant lines are outside N_0 and carry metric response.
lam0 = KERNEL[0]
w = KERNEL[2] + KERNEL[5] - KERNEL[7]
check("VISIBLE_Q11", sp.expand((lam0.T * Sq[:, SYM.index((1, 1))])[0]) == -1 - sp.I)
check("VISIBLE_W_HAS_METRIC_RESPONSE", sp.expand(Sq.T * w) != sp.zeros(10, 1))
bt = kv({0: 1, 1: 1, 2: 1, 6: 1, 7: 1, 8: 1, 12: 1, 13: 1, 14: 1})
check("TANGENT_227_NOT_IN_N0", sp.expand(Sq.T * bt) != sp.zeros(10, 1))


# ---------------------------------------------------------------- joint quadrics
Ms = [
    GEN[3] - GEN[4] + GEN[5],
    GEN[1] - GEN[2] + GEN[5],
    GEN[0] - GEN[2] + GEN[4],
    GEN[0] - GEN[1] + GEN[3],
]
for slot, (idx, M) in enumerate(zip(INVISIBLE_INDEX, Ms)):
    role = [1, 3, 4, 6][slot]  # kernel index; role is slot
    role = slot
    rebuilt = sp.zeros(4)
    for j in range(6):
        rebuilt += KERNEL[idx][6 * role + j] * GEN[j]
    check("GENERATOR_MATCH_%d" % idx, sp.expand(rebuilt - M) == sp.zeros(4))

# Owned polarized curvature_mixed scalar on the invisible coordinates.
def mul_jet4(X, Ym):
    return (
        X[0] * Ym[0],
        X[0] * Ym[1] + X[1] * Ym[0],
        X[0] * Ym[2] + X[2] * Ym[0],
        X[0] * Ym[3] + X[1] * Ym[2] + X[2] * Ym[1] + X[3] * Ym[0],
    )

def exp_link_cubic(A0, phase=1, inverse=False):
    sign = -1 if inverse else 1
    A0 = sign * phase * A0
    return (sp.eye(4), A0, sp.Rational(1, 2) * A0 * A0, sp.Rational(1, 6) * A0 * A0 * A0)

u = sp.symbols("u0:4")
mixed = 0
for p, q in PAIRS:
    Ap = u[p] * Ms[p]
    Aq = u[q] * Ms[q]
    Pj = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    Pj = mul_jet4(Pj, exp_link_cubic(Ap, 1, False))
    Pj = mul_jet4(Pj, exp_link_cubic(Aq, sp.I, False))
    Pj = mul_jet4(Pj, exp_link_cubic(Ap, sp.I, True))
    Pj = mul_jet4(Pj, exp_link_cubic(Aq, 1, True))
    R = sp.expand(Pj[3] - sp.Rational(1, 2) * (Pj[1] * Pj[2] + Pj[2] * Pj[1]))
    uu, vv = [i for i in range(4) if i not in (p, q)]
    mixed += complement_orientation((p, q)) * (
        wedge_vec(basis_cols[uu], basis_cols[vv]).T * G2 * STAR * bivector_of_tangent(R)
    )[0]
check("POLARIZED_CURVATURE_MIXED_VANISHES_ON_N0", sp.expand(mixed) == 0)
Kinv = sp.Matrix.hstack(*[KERNEL[i] for i in INVISIBLE_INDEX])
check("POLARIZED_SYMMETRIZED_QUADRATIC_FORM_VANISHES",
      sp.expand(Kinv.T * (Hq + Hq.T) * Kinv) == sp.zeros(4))

# Odd holonomy (P - P^{-1})/2 through degree 2. Its linear term is the
# census factor (1 - i) on a single role; the quadratic term is the first
# joint response.
NDEG = 2

def exp_series(X):
    out = [sp.zeros(4) for _ in range(NDEG + 1)]
    out[0] = sp.eye(4)
    power = sp.eye(4)
    fact = 1
    for k in range(1, NDEG + 1):
        power = sp.expand(power * X)
        fact *= k
        out[k] = sp.expand(power / fact)
    return out

def mul_series(A, B):
    out = [sp.zeros(4) for _ in range(NDEG + 1)]
    for i in range(NDEG + 1):
        for j in range(NDEG + 1 - i):
            out[i + j] = sp.expand(out[i + j] + A[i] * B[j])
    return out

def inv_series(P):
    higher = [sp.zeros(4) for _ in range(NDEG + 1)]
    for k in range(1, NDEG + 1):
        higher[k] = P[k]
    acc = [sp.zeros(4) for _ in range(NDEG + 1)]
    acc[0] = sp.eye(4)
    power = [sp.zeros(4) for _ in range(NDEG + 1)]
    power[0] = sp.eye(4)
    sign = -1
    for _ in range(NDEG):
        power = mul_series(power, higher)
        acc = [sp.expand(acc[k] + sign * power[k]) for k in range(NDEG + 1)]
        sign = -sign
    return acc

def dressed(role, phase, inverse):
    coef = -phase if inverse else phase
    return exp_series(coef * u[role] * Ms[role])

flat = [0, 0, 0]
odd2 = {}
for p, q in PAIRS:
    P = dressed(p, 1, False)
    P = mul_series(P, dressed(q, sp.I, False))
    P = mul_series(P, dressed(p, sp.I, True))
    P = mul_series(P, dressed(q, 1, True))
    Pinv = inv_series(P)
    odd = [sp.expand(sp.Rational(1, 2) * (P[k] - Pinv[k])) for k in range(3)]
    odd2[(p, q)] = odd[2]
    uu, vv = [i for i in range(4) if i not in (p, q)]
    area = wedge_vec(basis_cols[uu], basis_cols[vv])
    sgn = complement_orientation((p, q))
    for k in range(3):
        flat[k] += sp.expand(sgn * (area.T * G2 * STAR * bivector_of_tangent(odd[k]))[0])
check("ODD_HOLONOMY_DEGREE0", sp.expand(flat[0]) == 0)
check("ODD_HOLONOMY_DEGREE1", sp.expand(flat[1]) == 0)
V2 = sp.expand(flat[2])
expected_V2 = sp.expand(2 * (-1 + sp.I) * u[0] * u[1] + 2 * (1 - sp.I) * u[0] * u[2] + 2 * (-1 + sp.I) * u[0] * u[3])
check("EK_POTENTIAL_DEGREE2", V2 - expected_V2 == 0)
EK = [sp.expand(sp.diff(V2, ui)) for ui in u]
scale = 2 * (1 - sp.I)
check("EK0", sp.expand(EK[0] - scale * (-u[1] + u[2] - u[3])) == 0)
check("EK1", sp.expand(EK[1] - scale * (-u[0])) == 0)
check("EK2", sp.expand(EK[2] - scale * u[0]) == 0)
check("EK3", sp.expand(EK[3] - scale * (-u[0])) == 0)
check("EK_JACOBIAN_RANK_2", sp.Matrix([[sp.diff(comp, var) for var in u] for comp in EK]).rank() == 2)

EQ = []
for role in range(4):
    for comp in range(4):
        total = 0
        for p, q in PAIRS:
            uu, vv = [i for i in range(4) if i not in (p, q)]
            Bvar = sp.zeros(6, 1)
            if role == uu:
                Bvar += wedge_vec(basis_cols[comp], basis_cols[vv])
            if role == vv:
                Bvar += wedge_vec(basis_cols[uu], basis_cols[comp])
            total += complement_orientation((p, q)) * (
                Bvar.T * G2 * STAR * bivector_of_tangent(odd2[(p, q)])
            )[0]
        EQ.append(sp.expand(total))
check("EQ_SIXTEEN_COMPONENTS", len(EQ) == 16)
check("EQ_NOT_ALL_ZERO", any(comp != 0 for comp in EQ))

# Elimination: EK forces u0 = 0 and u2 = u1 + u3. Two metric quadrics then
# force u1 = u3 = 0. The same identities are checked by direct substitution.
u0, u1, u2, u3 = u
subs = {u0: 0, u2: u1 + u3}
check("EK_HOLDS_ON_CANDIDATE_PLANE", all(sp.expand(comp.subs(subs)) == 0 for comp in EK))
eq01 = sp.expand(EQ[1].subs(subs))  # role 0, component 1
eq02 = sp.expand(EQ[2].subs(subs))
check("EQ01_REDUCES_TO_U1_SQUARE", sp.expand(eq01 + (1 - sp.I) * u1**2) == 0)
check("EQ02_AFTER_U1", sp.expand(eq02.subs({u1: 0}) - (-1 + sp.I) * u3**2) == 0)
# Therefore every common zero has u1 = 0, then u3 = 0, then u2 = 0, u0 = 0.
for comp in EQ:
    check_value = sp.expand(comp.subs({u0: 0, u1: 0, u2: 0, u3: 0}))
    if check_value != 0:
        raise AssertionError("origin fails E_Q")
check("ORIGIN_IS_A_JOINT_ZERO", True)
# No other complex solution of the four connection equations and these two
# metric quadrics: the factors (1 - i) and the squares are non-zero.
solutions = sp.solve([EK[0], EK[1], EK[2], EK[3], EQ[1], EQ[2]], list(u), dict=True)
if solutions != [{u0: 0, u1: 0, u2: 0, u3: 0}]:
    print("SOLUTIONS", solutions)
    print("EQ1", EQ[1])
    print("EQ2", EQ[2])
check(
    "ONLY_ZERO_SOLVES_EK_AND_TWO_EQ",
    solutions == [{u0: 0, u1: 0, u2: 0, u3: 0}],
)

print("INVISIBLE_COORDINATES", list(INVISIBLE_INDEX))
print("EK_RED_DEGREE", 1)
print("EQ_RED_DEGREE", 2)
print("JOINT_JACOBIAN_RANK", 2)
print("BLOCKED: J2-DIAGONAL-INVISIBLE-LYAPUNOV-SCHMIDT-CORRECTION-MISSING")
print("MISSING: solved regular correction r(u)=O(u^2) substituted into E_Q")
print("CLOSED_BYPASS: J2-AFFINE-COFRAME-L4-KINEMATIC-DESCENT-NOT-GAUGE-NULL")
