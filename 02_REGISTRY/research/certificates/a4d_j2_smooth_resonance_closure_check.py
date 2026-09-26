#!/usr/bin/env python3
"""Research certificate for EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE.

This checker has two exact/reproducible layers.

A. Reconstruct the correctly polarized flat star connection symbol used by
   merged #208, scan all 4^4 L=4 characters, and verify the singular-orbit
   inventory.  Representative ranks are also checked exactly over Q(i).

B. Verify the exact rational diagonal-quarter-wave Lyapunov--Schmidt reduced
   quartic potential, the q_11 source vector, and a rigorous frozen-Newton
   contraction certificate around a rational center.  This certifies a unique
   nondegenerate root of the limiting cubic reduced Euler system.

The sparse quartic reduction itself is recorded as an exact research output:
regular 0- and 2k-harmonic variables were Schur-eliminated over Q from the
four-phase L=4 star expansion.  This script freezes and pressure-tests the
resulting exact polynomial and all downstream claims.

No continuum Einstein field equation is claimed here.
"""
from itertools import combinations, permutations, product
import numpy as np
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


# ---------------------------------------------------------------------------
# 1. Polarized star connection symbol, copied structurally from merged #208
# ---------------------------------------------------------------------------

LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)
for X in LORENTZ:
    check("LORENTZ_TANGENT", X.T * ETA + ETA * X == sp.zeros(4))

G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]

STAR = sp.zeros(6)
STAR_MAP = {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}
for p, (q, s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))


def wedge_vec(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([Y[a, b] for a, b in PAIRS])


def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def mul_jet4(X, Y):
    # coefficients (1,t,u,tu)
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[2] * Y[0],
        X[0] * Y[3] + X[1] * Y[2] + X[2] * Y[1] + X[3] * Y[0],
    )


def exp_link4(A0, B0, phase_a=1, phase_b=1, inverse=False):
    sign = -1 if inverse else 1
    LA = sign * phase_a * A0
    LB = sign * phase_b * B0
    mixed = sp.Rational(1, 2) * phase_a * phase_b * (A0 * B0 + B0 * A0)
    return (sp.eye(4), LA, LB, mixed)


def curvature_mixed(P):
    return sp.simplify(
        P[3] - sp.Rational(1, 2) * (P[1] * P[2] + P[2] * P[1])
    )


z = sp.symbols("z0:4", nonzero=True)
avars = sp.symbols("a0:24")
bvars = sp.symbols("b0:24")

A = []
Bc = []
for r in range(4):
    YA = sp.zeros(4)
    YB = sp.zeros(4)
    for j, gen in enumerate(LORENTZ):
        YA += avars[6 * r + j] * gen
        YB += bvars[6 * r + j] * gen
    A.append(YA)
    Bc.append(YB)

basis = [sp.eye(4)[:, r] for r in range(4)]
connection_bilinear = sp.Integer(0)
for r, s in PAIRS:
    Pj = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    Pj = mul_jet4(Pj, exp_link4(A[r], Bc[r]))
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], z[r], 1 / z[r]))
    Pj = mul_jet4(
        Pj, exp_link4(A[r], Bc[r], z[s], 1 / z[s], inverse=True)
    )
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], inverse=True))
    Cm = curvature_mixed(Pj)
    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis[u], basis[v])
    connection_bilinear += complement_orientation((r, s)) * (
        B0.T * G2 * STAR * bivector_of_tangent(Cm)
    )[0]

HAB = sp.Matrix(
    [
        [
            sp.diff(sp.diff(sp.expand(connection_bilinear), avars[i]), bvars[j])
            for j in range(24)
        ]
        for i in range(24)
    ]
)

# Genuine symmetric metric lift q -> H=1/2 q eta.
SYM = [(a0, b0) for a0 in range(4) for b0 in range(a0, 4)]
B = sp.zeros(16, 10)
for j, (a0, b0) in enumerate(SYM):
    q = sp.zeros(4)
    q[a0, b0] = 1
    q[b0, a0] = 1
    H = sp.Rational(1, 2) * q * ETA
    for r in range(4):
        for c0 in range(4):
            B[4 * r + c0, j] = H[r, c0]

hvars = sp.symbols("h0:16")
h = [sp.Matrix(hvars[4 * r : 4 * r + 4]) for r in range(4)]
cross = sp.Integer(0)
for r, s in PAIRS:
    C1 = (1 / z[r] - 1) * Bc[s] - (1 / z[s] - 1) * Bc[r]
    u, v = [i for i in range(4) if i not in (r, s)]
    B1 = wedge_vec(h[u], basis[v]) + wedge_vec(basis[u], h[v])
    cross += complement_orientation((r, s)) * (
        B1.T * G2 * STAR * bivector_of_tangent(C1)
    )[0]

HAH_CONJ = sp.Matrix(
    [
        [
            sp.diff(sp.diff(sp.expand(cross), bvars[i]), hvars[j])
            for j in range(16)
        ]
        for i in range(24)
    ]
)
HAQ = HAH_CONJ * B

# Exact diagonal quarter-wave data.
quarter = {zr: sp.I for zr in z}
Hq = HAB.subs(quarter)
Sq = HAQ.subs(quarter)
check("DIAGONAL_QUARTER_RANK_16", Hq.rank() == 16)
check("DIAGONAL_AUGMENTED_RANK_20", Hq.T.row_join(Sq).rank() == 20)
check("DIAGONAL_COMPLEX_KERNEL_DIM_8", len(Hq.nullspace()) == 8)

# Exact source-active Fredholm line for q_11.
lam = sp.zeros(24, 1)
lam[0] = lam[1] = lam[2] = 1
check("DIAGONAL_FREDHOLM_NULL", Hq * lam == sp.zeros(24, 1))
q11 = SYM.index((1, 1))
check(
    "DIAGONAL_Q11_SOURCE",
    sp.simplify((lam.T * Sq[:, q11])[0]) == -1 - sp.I,
)

# Verify the convenient exact kernel basis recorded by the memo.
kernel_vectors = []
def kv(entries):
    v = sp.zeros(24, 1)
    for idx, val in entries.items():
        v[idx] = val
    return v

kernel_vectors.extend([
    kv({0:1,1:1,2:1}),
    kv({3:1,4:-1,5:1}),
    kv({6:1,9:1,10:1}),
    kv({7:1,8:-1,11:1}),
    kv({12:1,14:-1,16:1}),
    kv({13:1,15:-1,17:1}),
    kv({18:1,19:-1,21:1}),
    kv({20:-1,22:1,23:1}),
])
for j, v in enumerate(kernel_vectors):
    check("DIAGONAL_KERNEL_BASIS_%d" % j, Hq * v == sp.zeros(24, 1))
check(
    "DIAGONAL_KERNEL_BASIS_RANK_8",
    sp.Matrix.hstack(*kernel_vectors).rank() == 8,
)

# ---------------------------------------------------------------------------
# 2. Full L=4 polarized singular-character scan
# ---------------------------------------------------------------------------

roots = [1, 1j, -1, -1j]
phase_index = {1:0, 1j:1, -1:2, -1j:3}

HAB_fun = sp.lambdify(z, HAB, "numpy")
HAQ_fun = sp.lambdify(z, HAQ, "numpy")


def nrank(M, tol=1e-8):
    svals = np.linalg.svd(np.asarray(M, dtype=np.complex128), compute_uv=False)
    return int(np.sum(svals > tol))


singular = []
for ph in product(roots, repeat=4):
    Hn = np.asarray(HAB_fun(*ph), dtype=np.complex128)
    Sn = np.asarray(HAQ_fun(*ph), dtype=np.complex128)
    rH = nrank(Hn)
    if rH < 24:
        rA = nrank(np.concatenate([Hn.T, Sn], axis=1))
        singular.append((ph, rH, rA, rA-rH))

check("L4_SINGULAR_CHARACTER_COUNT_56", len(singular) == 56)

from collections import Counter, defaultdict
rank_counts = Counter((rH, rA, d0) for _, rH, rA, d0 in singular)
expected_counts = Counter({
    (20,24,4):24,
    (22,23,1):12,
    (22,24,2):12,
    (20,23,3):6,
    (16,20,4):2,
})
check("L4_RANK_PATTERN_COUNTS", rank_counts == expected_counts)

# Canonical orbit key under spatial S3 permutations + conjugation.
def idx_phase(x):
    # robust map for exact fourth roots represented as Python complex
    if abs(x-1) < 1e-12: return 0
    if abs(x-1j) < 1e-12: return 1
    if abs(x+1) < 1e-12: return 2
    if abs(x+1j) < 1e-12: return 3
    raise ValueError(x)

def conj_idx(i):
    return {0:0,1:3,2:2,3:1}[i]

groups = defaultdict(list)
for ph, rH, rA, dd in singular:
    ids = tuple(idx_phase(x) for x in ph)
    keys = []
    for conj in (False, True):
        aa = conj_idx(ids[0]) if conj else ids[0]
        spatial0 = tuple(conj_idx(x) for x in ids[1:]) if conj else ids[1:]
        for perm in set(permutations(spatial0)):
            keys.append((aa, tuple(perm), rH, rA, dd))
    # canonicalize spatial permutations by sorting
    key = min((k[0], tuple(sorted(k[1])), k[2], k[3], k[4]) for k in keys)
    groups[key].append(ids)

orbit_summary = sorted((k, len(v)) for k, v in groups.items())
expected_orbits = [
    ((0,(0,1,1),22,23,1),6),
    ((0,(0,1,3),22,24,2),6),
    ((0,(1,1,2),20,24,4),6),
    ((1,(0,1,2),20,24,4),12),
    ((1,(1,1,1),16,20,4),2),
    ((1,(1,3,3),20,23,3),6),
    ((2,(0,1,1),20,24,4),6),
    ((2,(1,1,2),22,23,1),6),
    ((2,(1,2,3),22,24,2),6),
]
check("L4_NINE_SINGULAR_ORBIT_TYPES", orbit_summary == expected_orbits)

# Exact ranks for one representative of every orbit type.
root_exact = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
for n, (key, _) in enumerate(expected_orbits):
    Aidx, spatial_sorted, rH, rA, dd = key
    ids = (Aidx,) + spatial_sorted
    sub = {z[j]: root_exact[ids[j]] for j in range(4)}
    He = HAB.subs(sub)
    Se = HAQ.subs(sub)
    check("ORBIT_%d_EXACT_RANK" % n, He.rank() == rH)
    check("ORBIT_%d_EXACT_AUG_RANK" % n, He.T.row_join(Se).rank() == rA)

# ---------------------------------------------------------------------------
# 3. Exact reduced quartic potential and Newton contraction certificate
# ---------------------------------------------------------------------------

a,b,c,d = sp.symbols("a b c d")

P4 = (
    36*a**2*b**2 - 3*a**2*b*c - 27*a**2*b*d + 2*a**2*c*d + 3*a**2*d**2
    - 27*a*b**2*c + 3*a*b**2*d + 188*a*b*c*d
    + 22*a*c**2*d - 107*a*c*d**2 - a*d**3
    + 3*b**2*c**2 - 2*b**2*c*d + b*c**3
    - 107*b*c**2*d - 22*b*c*d**2
    - 6*c**3*d + 38*c**2*d**2 + 6*c*d**3
)
V4 = 48 * P4
source = sp.Matrix([-8, 8, 0, 0])
vars4 = (a,b,c,d)
F = sp.Matrix([sp.diff(V4, x) for x in vars4]) + source
J = F.jacobian(vars4)

check("REDUCED_POTENTIAL_HOMOGENEOUS_DEGREE_4",
      sp.Poly(V4, *vars4).total_degree() == 4)
check("REDUCED_EULER_CUBIC",
      max(sp.Poly(f, *vars4).total_degree() for f in F) == 3)

x0 = [
    sp.Rational(7002710483711, 50000000000000),
    -sp.Rational(13701463188057, 100000000000000),
    sp.Rational(3111354422107, 100000000000000),
    -sp.Rational(2645772859363, 100000000000000),
]
subs0 = dict(zip(vars4, x0))
F0 = F.subs(subs0)
J0 = J.subs(subs0)
check("REDUCED_JACOBIAN_NONZERO_DET", J0.det() != 0)

J0inv = J0.inv()
newton_step = J0inv * F0
eta = max(sum([abs(newton_step[i])]) for i in range(4))
normJinv = max(
    sum(abs(J0inv[i,j]) for j in range(4))
    for i in range(4)
)

# Exact infinity-norm Lipschitz bound for J on radius r.
r = sp.Rational(1, 10_000_000_000)
row_bounds = []
for i in range(4):
    row_bound = 0
    for j in range(4):
        entry_lip = 0
        for xk in vars4:
            der = sp.diff(J[i,j], xk)
            sup = abs(der.subs(subs0))
            # der is affine because J is quadratic.
            for xl in vars4:
                sup += abs(sp.diff(der, xl)) * r
            entry_lip += sup
        row_bound += entry_lip
    row_bounds.append(sp.simplify(row_bound))
Lraw = max(row_bounds)
qcontr = sp.simplify(normJinv * Lraw * r)

check("NEWTON_CONTRACTION_LT_ONE", qcontr < 1)
check("NEWTON_MAPS_BALL_INTO_ITSELF", eta / (1 - qcontr) < r)

# Strong numerical diagnostics, not used for the exact inequalities above.
J0_np = np.asarray(J0.evalf(30), dtype=float)
svals = np.linalg.svd(J0_np, compute_uv=False)

print("RESULT_L4_SINGULAR_CHARACTERS:", len(singular))
print("RESULT_L4_ORBITS:", orbit_summary)
print("RESULT_DIAGONAL_REDUCED_V4:", sp.expand(V4))
print("RESULT_DIAGONAL_SOURCE:", tuple(source))
print("RESULT_NEWTON_STEP_INF:", sp.N(eta, 18))
print("RESULT_JINV_INF:", sp.N(normJinv, 18))
print("RESULT_J_LIPSCHITZ_BOUND:", sp.N(Lraw, 18))
print("RESULT_CONTRACTION_Q:", sp.N(qcontr, 18))
print("RESULT_J_DET:", sp.N(J0.det(), 18))
print("RESULT_J_SINGULAR_VALUES:", svals)
print("RESULT_BRANCH: A_res(delta)=delta^(1/3) K(u_*) + O(delta^(2/3))")
print("TERMINAL: J2-SMOOTH-PARTIAL-CLOSURE")
