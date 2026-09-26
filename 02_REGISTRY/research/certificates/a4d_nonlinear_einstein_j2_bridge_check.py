#!/usr/bin/env python3
"""Exact structural certificate for EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE.

Research-only, exact SymPy arithmetic.

This checker proves three bridge facts.

1. The ten-component metric lift used by merged #201 is the exact differential
   section of the nonlinear Lorentz-quotient Gram metric
       Q = Theta eta Theta^T
   at the flat solder.

2. For a genuine complex Fourier character, the real quadratic action pairs
   mode z with the conjugate/inverse mode z^{-1}.  On the diagonal character
       z_A=z_B=z_C=z_D=t
   the correctly polarized flat Lorentz-connection block satisfies
       det H_AA^pol(t) = (t^2+1)^12 / (16 t^12).
   It is regular at low momentum (det at t=1 is 256) but singular at the
   exact L=4 quarter-wave t=i.

3. At t=i the polarized block has rank 16, while the connection source from
   genuine symmetric metric perturbations enlarges the augmented rank to 20.
   An explicit Fredholm witness lies in ker H_AA^pol and pairs nontrivially
   with the q_11 metric basis direction:
       lambda^T H_Aq(q_11) = -(1+i).
   Hence naive smooth all-mode connection elimination through flat fails on
   the full finite metric carrier at L=4.

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


# Lorentz tangent basis: K1,K2,K3,J12,J13,J23.
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
# B. Correct polarized Fourier block z <-> z^{-1}
# ---------------------------------------------------------------------------

# A real quadratic lattice action pairs a character z with z^{-1}.  We keep
# independent connection amplitudes A (mode z) and Bc (mode z^{-1}) and extract
# the mixed tu coefficient.

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


# Bivariate jet coefficients (1, t, u, tu).
def mul_jet4(X, Y):
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
    # sign^2=1 in the mixed quadratic coefficient.
    mixed = sp.Rational(1, 2) * phase_a * phase_b * (A0 * B0 + B0 * A0)
    return (sp.eye(4), LA, LB, mixed)


def curvature_mixed(P):
    # For P=I+t P10+u P01+tu P11,
    # mixed coeff of (P-P^{-1})/2 is
    # P11 - 1/2(P10 P01 + P01 P10).
    return sp.simplify(
        P[3] - sp.Rational(1, 2) * (P[1] * P[2] + P[2] * P[1])
    )


basis = [sp.eye(4)[:, r] for r in range(4)]
connection_bilinear = sp.Integer(0)

for r, s in PAIRS:
    P = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    P = mul_jet4(P, exp_link4(A[r], Bc[r]))
    P = mul_jet4(P, exp_link4(A[s], Bc[s], z[r], 1 / z[r]))
    P = mul_jet4(
        P, exp_link4(A[r], Bc[r], z[s], 1 / z[s], inverse=True)
    )
    P = mul_jet4(P, exp_link4(A[s], Bc[s], inverse=True))

    Cm = curvature_mixed(P)
    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis[u], basis[v])
    connection_bilinear += complement_orientation((r, s)) * (
        B0.T * G2 * STAR * bivector_of_tangent(Cm)
    )[0]

connection_bilinear = sp.expand(connection_bilinear)
HAB = sp.Matrix(
    [
        [
            sp.diff(sp.diff(connection_bilinear, avars[i]), bvars[j])
            for j in range(24)
        ]
        for i in range(24)
    ]
)

# Low-momentum block reproduces the #201 zero-momentum determinant.
HAB_ONE = HAB.subs({zr: 1 for zr in z})
check("POLARIZED_ZERO_MOMENTUM_RANK_24", HAB_ONE.rank() == 24)
check("POLARIZED_ZERO_MOMENTUM_DET_256", sp.factor(HAB_ONE.det()) == 256)

# Along the diagonal phase z_A=z_B=z_C=z_D=t the determinant is exactly
# one-variable and factorizes cheaply.
t = sp.symbols("t", nonzero=True)
HAB_DIAG = HAB.subs({zr: t for zr in z})
diag_det = sp.factor(HAB_DIAG.det(method="domain-ge"))
expected_diag_det = (t**2 + 1) ** 12 / (16 * t**12)
check(
    "POLARIZED_DIAGONAL_DETERMINANT",
    sp.factor(diag_det - expected_diag_det) == 0,
)


# ---------------------------------------------------------------------------
# C. Genuine metric-source incompatibility at the L=4 quarter wave
# ---------------------------------------------------------------------------

# Cross term between coframe mode z and conjugate connection mode z^{-1}.
hvars = sp.symbols("h0:16")
h = [sp.Matrix(hvars[4 * r : 4 * r + 4]) for r in range(4)]
cross = sp.Integer(0)

for r, s in PAIRS:
    # First curvature jet of the conjugate connection mode.
    C1 = (1 / z[r] - 1) * Bc[s] - (1 / z[s] - 1) * Bc[r]
    u, v = [i for i in range(4) if i not in (r, s)]
    B1 = wedge_vec(h[u], basis[v]) + wedge_vec(basis[u], h[v])
    cross += complement_orientation((r, s)) * (
        B1.T * G2 * STAR * bivector_of_tangent(C1)
    )[0]

HAH_CONJ = sp.Matrix(
    [
        [
            sp.diff(sp.diff(cross, bvars[i]), hvars[j])
            for j in range(16)
        ]
        for i in range(24)
    ]
)
HAQ = HAH_CONJ * B

quarter = {zr: sp.I for zr in z}
HAB_Q = HAB.subs(quarter)
HAQ_Q = HAQ.subs(quarter)

# Variation with respect to the conjugate-mode connection gives
# HAB^T a + HAQ q = 0.
check("QUARTER_WAVE_POLARIZED_RANK_16", HAB_Q.rank() == 16)
check("QUARTER_WAVE_METRIC_SOURCE_RANK_9", HAQ_Q.rank() == 9)
check(
    "QUARTER_WAVE_AUGMENTED_RANK_20",
    HAB_Q.T.row_join(HAQ_Q).rank() == 20,
)

# Explicit Fredholm witness: lambda is a left null vector of HAB^T, equivalently
# a right null vector of HAB.  It is supported on the three boosts of Role A.
lam = sp.zeros(24, 1)
lam[0] = 1
lam[1] = 1
lam[2] = 1
check("QUARTER_WAVE_FREDHOLM_NULL_WITNESS", HAB_Q * lam == sp.zeros(24, 1))

q11_index = SYM.index((1, 1))
pairing = sp.simplify((lam.T * HAQ_Q[:, q11_index])[0])
check("QUARTER_WAVE_METRIC_INCOMPATIBILITY", pairing == -1 - sp.I)

print("RESULT_METRIC_PROVENANCE: the #201 ten-component lift is exactly a section of dQ_flat for Q=Theta eta Theta^T.")
print("RESULT_POLARIZED_CONNECTION: along z_A=z_B=z_C=z_D=t, det H_AA^pol=(t^2+1)^12/(16 t^12).")
print("RESULT_LOW_MOMENTUM: det H_AA^pol(1)=256.")
print("RESULT_QUARTER_WAVE: at L=4, t=i, rank H_AA^pol=16 but rank[H_AA^pol|H_Aq]=20.")
print("RESULT_EXPLICIT_WITNESS: lambda on the three Role-A boosts pairs with metric q_11 as -(1+i).")
print("TERMINAL_SCOPED: ALL-MODE-FLAT-CONNECTION-ELIMINATION-FAILS-AT-L4-DIAGONAL-QUARTER-WAVE")
