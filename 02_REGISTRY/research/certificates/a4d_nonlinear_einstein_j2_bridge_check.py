#!/usr/bin/env python3
"""Exact structural certificate for EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE.

Research-only, exact SymPy arithmetic.

This checker proves three bridge facts.

1. The ten-component metric lift used by merged #201 is the exact differential
   section of the nonlinear Lorentz-quotient Gram metric
       Q = Theta eta Theta^T
   at the flat solder.

2. The flat Lorentz-connection Hessian block has the exact arbitrary-phase
   determinant
       det H_AA(z)
       = 2^-16 prod_{r<s}(z_r z_s + z_r + z_s - 1)^4.
   It is therefore invertible at low momentum (det H_AA(1)=256), but has
   exact quarter-wave resonances on the unit torus.

3. At the finite L=4 character z=(i,-i,1,1), rank H_AA=20 while the
   connection source from genuine symmetric metric perturbations enlarges the
   augmented rank to 24.  An explicit left-null witness has support on
   connection coordinates 3 and 7 and pairs nontrivially with q_02:
       lambda^T H_Aq(q_02) = (1+i)/2.
   Hence there is no smooth all-mode connection section K_*(Q) through flat
   whose differential solves the connection Euler equation on the full metric
   carrier.

No continuum Einstein equation is claimed by this certificate.
"""
from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


# Lorentz tangent basis in the same ordering used by #201:
# K1,K2,K3,J12,J13,J23.
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


def mul_jet(X, Y):
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[1] * Y[1] + X[2] * Y[0],
    )


def exp_link(A, scale=1, inverse=False):
    B = scale * A
    return (sp.eye(4), -B if inverse else B, B * B / 2)


# ---------------------------------------------------------------------------
# A. Exact nonlinear metric tangent section
# ---------------------------------------------------------------------------

SYM = [(a, b) for a in range(4) for b in range(a, 4)]
qvars = sp.symbols("q0:10")
Q = sp.zeros(4)
for j, (a, b) in enumerate(SYM):
    Q[a, b] = qvars[j]
    Q[b, a] = qvars[j]

# If H stores the four solder-vector perturbations as rows, then
# d(Theta eta Theta^T)_flat = H eta + eta H^T.
# The #201 lift is H = 1/2 q eta.
H_METRIC_SECTION = sp.Rational(1, 2) * Q * ETA
check(
    "METRIC_LIFT_IS_GRAM_DIFFERENTIAL_RIGHT_INVERSE",
    sp.simplify(H_METRIC_SECTION * ETA + ETA * H_METRIC_SECTION.T - Q)
    == sp.zeros(4),
)

B = sp.zeros(16, 10)
for j, (a, b) in enumerate(SYM):
    q = sp.zeros(4)
    q[a, b] = 1
    q[b, a] = 1
    H = sp.Rational(1, 2) * q * ETA
    for r in range(4):
        for c in range(4):
            B[4 * r + c, j] = H[r, c]
check("METRIC_LIFT_RANK_10", B.rank() == 10)


# ---------------------------------------------------------------------------
# B. Arbitrary-phase flat quadratic connection block
# ---------------------------------------------------------------------------

z = sp.symbols("z0:4")
hvars = sp.symbols("h0:16")
avars = sp.symbols("a0:24")

h = [sp.Matrix(hvars[4 * r : 4 * r + 4]) for r in range(4)]
A = []
for r in range(4):
    Y = sp.zeros(4)
    for j, gen in enumerate(LORENTZ):
        Y += avars[6 * r + j] * gen
    A.append(Y)

basis = [sp.eye(4)[:, r] for r in range(4)]
total = sp.Integer(0)

for r, s in PAIRS:
    P = (sp.eye(4), sp.zeros(4), sp.zeros(4))
    P = mul_jet(P, exp_link(A[r]))
    P = mul_jet(P, exp_link(A[s], z[r]))
    P = mul_jet(P, exp_link(A[r], z[s], inverse=True))
    P = mul_jet(P, exp_link(A[s], inverse=True))

    P1, P2 = P[1], P[2]
    C1 = bivector_of_tangent(P1)
    C2 = bivector_of_tangent(P2 - P1 * P1 / 2)

    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis[u], basis[v])
    B1 = wedge_vec(h[u], basis[v]) + wedge_vec(basis[u], h[v])

    total += complement_orientation((r, s)) * (
        (B0.T * G2 * STAR * C2)[0] + (B1.T * G2 * STAR * C1)[0]
    )

total = sp.expand(total)
HESS = sp.hessian(total, list(hvars) + list(avars))
HAA = HESS[16:, 16:]
HAH = HESS[16:, :16]

expected_det = sp.Rational(1, 2**16)
for r, s in PAIRS:
    expected_det *= (z[r] * z[s] + z[r] + z[s] - 1) ** 4

actual_det = sp.factor(HAA.det(method="domain-ge"))
check("CONNECTION_DETERMINANT_FACTORIZATION", sp.factor(actual_det - expected_det) == 0)
check("ZERO_MOMENTUM_CONNECTION_DET_256", sp.simplify(actual_det.subs({x: 1 for x in z})) == 256)
check("ZERO_MOMENTUM_CONNECTION_RANK_24", HAA.subs({x: 1 for x in z}).rank() == 24)


# ---------------------------------------------------------------------------
# C. Exact L=4 quarter-wave obstruction on genuine metric directions
# ---------------------------------------------------------------------------

quarter = {z[0]: sp.I, z[1]: -sp.I, z[2]: 1, z[3]: 1}
HAA_Q = HAA.subs(quarter)
HAQ_Q = (HAH * B).subs(quarter)

check("QUARTER_WAVE_CONNECTION_RANK_20", HAA_Q.rank() == 20)
check("QUARTER_WAVE_METRIC_SOURCE_RANK_9", HAQ_Q.rank() == 9)
check("QUARTER_WAVE_AUGMENTED_RANK_24", HAA_Q.row_join(HAQ_Q).rank() == 24)

# Explicit left-null witness. Coordinates 3 and 7 correspond to
# (Role A,J12) and (Role B,K2) in the basis ordering above.
lam = sp.zeros(24, 1)
lam[3] = 1
lam[7] = 1
check("QUARTER_WAVE_LEFT_NULL_WITNESS", (lam.T * HAA_Q) == sp.zeros(1, 24))

q02_index = SYM.index((0, 2))
pairing = sp.simplify((lam.T * HAQ_Q[:, q02_index])[0])
check("QUARTER_WAVE_METRIC_INCOMPATIBILITY", pairing == (1 + sp.I) / 2)

# The resonant determinant factor itself vanishes exactly.
resonant_factor = z[0] * z[1] + z[0] + z[1] - 1
check("QUARTER_WAVE_FACTOR_ZERO", sp.simplify(resonant_factor.subs(quarter)) == 0)

print("RESULT_METRIC_PROVENANCE: the #201 ten-component lift is exactly a section of dQ_flat for Q=Theta eta Theta^T.")
print("RESULT_CONNECTION_SYMBOL: det H_AA(z)=2^-16 prod_{r<s}(z_r z_s+z_r+z_s-1)^4.")
print("RESULT_LOW_MOMENTUM: det H_AA(1,1,1,1)=256.")
print("RESULT_QUARTER_WAVE: at z=(i,-i,1,1), rank H_AA=20 but rank[H_AA|H_Aq]=24.")
print("RESULT_EXPLICIT_WITNESS: lambda_(A,J12)+lambda_(B,K2) pairs with metric q_02 as (1+i)/2.")
print("TERMINAL_SCOPED: ALL-MODE-FLAT-CONNECTION-ELIMINATION-FAILS-AT-L4-QUARTER-WAVE-RESONANCE")
