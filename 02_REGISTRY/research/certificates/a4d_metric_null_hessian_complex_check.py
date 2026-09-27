#!/usr/bin/env python3
"""Exact metric-null Hessian complex for the polarized A4D star response.

Terminal: J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT

Research-only certificate. It rebuilds the exact 24x10 metric-response
symbol C from the accepted star conventions, reparameterizes character
dependence by d_r = z_r^{-1}-1, and proves:
  * C(d) vec_sym(d d^T) = 0 identically;
  * for every d != 0, rank C(d)=9 and ker C(d)=span{vec_sym(d d^T)};
  * raw character-detune visibility is exact transport of that moving null line;
  * on the nine owned L4 singular orbit representatives, all 36 FUGU raw
    detune vectors lie in im C exactly;
  * the forward-coframe metric shadow built from a=z-1 contains the backward
    null line exactly on orbit types 0 and 4.

No gauge symmetry, Einstein equation, E_eta/E_sp identification, or nonlinear
branch is claimed.
"""
from itertools import combinations
import sympy as sp

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
SYM = [(a, b) for a in range(4) for b in range(a, 4)]

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


# Rebuild the metric-response symbol directly in d_r=(z_r^-1-1).
d = sp.symbols("d0:4")
bvars = sp.symbols("b0:24")
Bc = []
for r in range(4):
    Y = sp.zeros(4)
    for j, g in enumerate(LORENTZ):
        Y += bvars[6 * r + j] * g
    Bc.append(Y)

B = sp.zeros(16, 10)
for j, (a, b) in enumerate(SYM):
    q = sp.zeros(4)
    q[a, b] = 1
    q[b, a] = 1
    Hm = sp.Rational(1, 2) * q * ETA
    for r in range(4):
        for c in range(4):
            B[4 * r + c, j] = Hm[r, c]

hvars = sp.symbols("h0:16")
h = [sp.Matrix(hvars[4 * r:4 * r + 4]) for r in range(4)]
basis = [sp.eye(4)[:, r] for r in range(4)]

cross = sp.Integer(0)
for r, s in PAIRS:
    C1 = d[r] * Bc[s] - d[s] * Bc[r]
    u, v = [i for i in range(4) if i not in (r, s)]
    B1 = wedge_vec(h[u], basis[v]) + wedge_vec(basis[u], h[v])
    cross += complement_orientation((r, s)) * (
        B1.T * G2 * STAR * bivector_of_tangent(C1)
    )[0]

HAH = sp.Matrix([
    [
        sp.diff(sp.diff(sp.expand(cross), bvars[i]), hvars[j])
        for j in range(16)
    ]
    for i in range(24)
])
C = sp.simplify(HAH * B)

check("C_SHAPE", C.shape == (24, 10))
check(
    "C_LINEAR_IN_D",
    all(sp.Poly(e, *d).total_degree() <= 1 for e in C if e != 0),
)

q = sp.Matrix([sp.expand(d[a] * d[b]) for a, b in SYM])
check(
    "GLOBAL_NULL_IDENTITY",
    all(sp.cancel(sp.together(x)) == 0 for x in C * q),
)

# Exact projective cover of d != 0.
#
# IMPORTANT: Matrix.rank() over QQ(d) only proves generic rank.  To exclude
# exceptional nonzero d, each projective chart below is covered by explicit
# 9x9 minors with no common zero.  Since C q = 0 gives rank(C) <= 9, one
# nonzero 9x9 minor is enough to force rank(C)=9 pointwise.
MINOR_COVERS = {
    # chart d0=1; variables d1,d2,d3
    0: [
        ((6, 7, 8, 9, 10, 13, 14, 15, 20),
         (1, 2, 3, 4, 5, 6, 7, 8, 9),
         -(d[3] - 1)**2 * (d[3] + 1)**2 / 256),
        ((0, 1, 2, 4, 5, 6, 7, 10, 13),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         d[3]**7 / 256),
    ],
    # chart d1=1; variables d0,d2,d3
    1: [
        ((0, 1, 2, 3, 4, 13, 15, 16, 22),
         (0, 1, 2, 3, 5, 6, 7, 8, 9),
         -(d[3]**2 + 1)**2 / 256),
        ((0, 1, 2, 3, 4, 6, 9, 10, 15),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         d[3]**4 * (d[2]**2 + d[3]**2) / 256),
        ((0, 1, 2, 3, 4, 7, 9, 10, 15),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         -d[2] * d[3]**4 / 256),
    ],
    # chart d2=1; variables d0,d1,d3
    2: [
        ((0, 1, 2, 3, 5, 6, 9, 11, 23),
         (0, 1, 2, 3, 4, 5, 6, 8, 9),
         (d[3]**2 + 1)**2 / 256),
        ((0, 1, 2, 3, 4, 7, 9, 10, 15),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         -d[1]**4 * d[3]**4 / 256),
        ((0, 1, 2, 3, 5, 9, 13, 15, 17),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         d[3]**4 * (d[1]**2 + d[3]**2) / 256),
    ],
    # chart d3=1; variables d0,d1,d2
    3: [
        ((0, 1, 2, 4, 5, 6, 10, 11, 17),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         -(d[2]**2 + 1)**2 / 256),
        ((0, 1, 2, 3, 4, 7, 9, 10, 15),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         -d[1]**4 * d[2] / 256),
        ((0, 1, 2, 3, 5, 9, 13, 15, 17),
         (0, 1, 2, 3, 4, 5, 6, 7, 8),
         d[2]**3 * (d[1]**2 + 1) / 256),
    ],
}

for chart, specs in MINOR_COVERS.items():
    sub = {d[chart]: 1}
    M = C.subs(sub)
    for k, (rows, cols, expected) in enumerate(specs):
        got = sp.factor(M.extract(rows, cols).det())
        check(
            "CHART_%d_MINOR_%d_FORMULA" % (chart, k),
            sp.simplify(got - expected) == 0,
            "got %s expected %s" % (got, expected),
        )

# Exact no-common-zero proof for each explicit minor cover.
# A unit Groebner basis means the selected 9x9 minors generate the unit ideal
# on the normalized affine chart, hence they cannot vanish simultaneously.
CHART_VARS = {
    0: (d[1], d[2], d[3]),
    1: (d[0], d[2], d[3]),
    2: (d[0], d[1], d[3]),
    3: (d[0], d[1], d[2]),
}
for chart, specs in MINOR_COVERS.items():
    polys = [sp.together(expected) for _rows, _cols, expected in specs]
    gb = sp.groebner(polys, *CHART_VARS[chart], order="grevlex")
    unit = len(gb.polys) == 1 and sp.expand(gb.polys[0].as_expr()) in (1, -1)
    check("CHART_%d_MINOR_COVER_UNIT_IDEAL" % chart, unit, str(gb))

# Together the four normalized charts cover every projective class d != 0.
# C is homogeneous linear in d, so normalization by a nonzero coordinate
# preserves rank. Since q=dd^T is nonzero there and Cq=0, rank <=9; the unit
# minor covers force rank >=9. Therefore rank=9 and ker C is exactly q-line
# pointwise, with no exceptional nonzero stratum.
check(
    "PROJECTIVE_COVER_PROVES_RANK9_EVERYWHERE",
    all(
        (
            len(g.polys) == 1
            and sp.expand(g.polys[0].as_expr()) in (1, -1)
        )
        for g in (
            sp.groebner(
                [sp.together(e) for _r, _c, e in MINOR_COVERS[ch]],
                *CHART_VARS[ch],
                order="grevlex",
            )
            for ch in range(4)
        )
    ),
)

check(
    "TRIVIAL_CHARACTER_C_ZERO",
    C.subs({x: 0 for x in d}) == sp.zeros(24, 10),
)

# ---------------------------------------------------------------------------
# IR Schur-Einstein weld.
#
# Rebuild the zero-character connection Hessian A0 from the same star action.
# With z=1+t k, d=z^-1-1=-t k+O(t^2), so the leading eliminated metric
# Hessian is K_schur = -C(k)^T A0^-1 C(k).  Compare it directly with the
# already-owned E_eta symbol convention used by #201.
# ---------------------------------------------------------------------------

avars = sp.symbols("aa0:24")
cvars = sp.symbols("cc0:24")
Aconn = []
Cconn = []
for r in range(4):
    XA = sp.zeros(4)
    XC = sp.zeros(4)
    for j, g in enumerate(LORENTZ):
        XA += avars[6 * r + j] * g
        XC += cvars[6 * r + j] * g
    Aconn.append(XA)
    Cconn.append(XC)


def mul_jet4(X, Y):
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[2] * Y[0],
        X[0] * Y[3] + X[1] * Y[2] + X[2] * Y[1] + X[3] * Y[0],
    )


def exp_link4(A0, B0, inverse=False):
    sign = -1 if inverse else 1
    LA = sign * A0
    LB = sign * B0
    mixed = sp.Rational(1, 2) * (A0 * B0 + B0 * A0)
    return (sp.eye(4), LA, LB, mixed)


def curvature_mixed(P):
    return sp.simplify(
        P[3] - sp.Rational(1, 2) * (P[1] * P[2] + P[2] * P[1])
    )


connection_bilinear0 = sp.Integer(0)
for r, s in PAIRS:
    Pj = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    Pj = mul_jet4(Pj, exp_link4(Aconn[r], Cconn[r]))
    Pj = mul_jet4(Pj, exp_link4(Aconn[s], Cconn[s]))
    Pj = mul_jet4(Pj, exp_link4(Aconn[r], Cconn[r], inverse=True))
    Pj = mul_jet4(Pj, exp_link4(Aconn[s], Cconn[s], inverse=True))
    Cm = curvature_mixed(Pj)
    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis[u], basis[v])
    connection_bilinear0 += complement_orientation((r, s)) * (
        B0.T * G2 * STAR * bivector_of_tangent(Cm)
    )[0]

A0 = sp.Matrix([
    [
        sp.diff(
            sp.diff(sp.expand(connection_bilinear0), avars[i]),
            cvars[j],
        )
        for j in range(24)
    ]
    for i in range(24)
])
check("IR_CONNECTION_HESSIAN_DET_256", sp.factor(A0.det()) == 256)
A0_INV = A0.inv()

K_SCHUR = sp.simplify(-C.T * A0_INV * C)

# Exact E_eta quadratic symbol in the #201 convention.
qvars = sp.symbols("q0:10")
Q = sp.zeros(4)
for j, (a, b) in enumerate(SYM):
    Q[a, b] = qvars[j]
    Q[b, a] = qvars[j]

kv = sp.Matrix(d)
kup = ETA * kv
ksq = (kv.T * ETA * kv)[0]
trq = sum(ETA[a, a] * Q[a, a] for a in range(4))
vq = sp.Matrix([
    sum(kup[c] * Q[c, b] for c in range(4))
    for b in range(4)
])
qq = sum(
    kup[c] * kup[e] * Q[c, e]
    for c in range(4)
    for e in range(4)
)

EETA = sp.zeros(4)
for a in range(4):
    for b in range(4):
        EETA[a, b] = sp.expand(
            ksq * Q[a, b]
            - d[a] * vq[b]
            - d[b] * vq[a]
            + d[a] * d[b] * trq
            + ETA[a, b] * qq
            - ETA[a, b] * ksq * trq
        )
EETA_UP = ETA * EETA * ETA
S_EETA = sp.Rational(1, 2) * sum(
    Q[a, b] * EETA_UP[a, b]
    for a in range(4)
    for b in range(4)
)
K_EETA = sp.hessian(sp.expand(S_EETA), qvars)

check(
    "IR_SCHUR_EQUALS_ONE_QUARTER_E_ETA",
    sp.simplify(K_SCHUR - sp.Rational(1, 4) * K_EETA) == sp.zeros(10),
)

# Leading forward-coframe / vector-diffeomorphism lift from #264.
# q1 is O(t), x2 is O(t^2) along z=1+t k.
def lorentz_coeffs_expr(X):
    return sp.Matrix([
        X[0, 1], X[0, 2], X[0, 3],
        X[1, 2], X[1, 3], X[2, 3],
    ])


GQ1 = sp.zeros(10, 4)
GX2 = sp.zeros(24, 4)
for col in range(4):
    xi = sp.eye(4)[:, col]
    Hraw1 = sp.Matrix(d) * xi.T
    q1 = sp.expand(Hraw1 * ETA + ETA * Hraw1.T)
    Hsec1 = sp.expand(sp.Rational(1, 2) * q1 * ETA)
    Delta1 = sp.expand(Hraw1 - Hsec1)
    lam1 = sp.expand(Delta1.T)

    for j, (a, b) in enumerate(SYM):
        GQ1[j, col] = q1[a, b]

    for r in range(4):
        Xr2 = sp.expand(d[r] * lam1)
        coeff = lorentz_coeffs_expr(Xr2)
        for j in range(6):
            GX2[6 * r + j, col] = coeff[j]

# d(z)= -t k + O(t^2), hence C1=-C(k).
check(
    "IR_COFRAME_CONNECTION_ORDER2_CANCELS",
    sp.simplify(-C * GQ1 + A0 * GX2) == sp.zeros(24, 4),
)
check(
    "IR_COFRAME_METRIC_ORDER3_CANCELS",
    sp.simplify(-C.T * GX2) == sp.zeros(10, 4),
)
check(
    "IR_COFRAME_X2_IS_SCHUR_LIFT",
    sp.simplify(GX2 - A0_INV * C * GQ1) == sp.zeros(24, 4),
)
check(
    "IR_EINSTEIN_SYMBOL_KILLS_VECTOR_COFRAME_IMAGE",
    sp.simplify(K_SCHUR * GQ1) == sp.zeros(10, 4),
)

for tag, kval, rank in (
    ("TIMELIKE", (1, 0, 0, 0), 6),
    ("SPACELIKE", (0, 1, 0, 0), 6),
    ("NULL", (1, 1, 0, 0), 4),
    ("GENERIC", (1, 2, 3, 4), 6),
):
    subk = {d[j]: kval[j] for j in range(4)}
    check(
        "IR_SCHUR_RANK_" + tag,
        K_SCHUR.subs(subk).rank() == rank,
    )

# Character form and exact transport identity.
z = sp.symbols("z0:4", nonzero=True)
subz = {d[j]: 1 / z[j] - 1 for j in range(4)}
Cz = sp.simplify(C.subs(subz))
qz = sp.simplify(q.subs(subz))

for j in range(4):
    DjC = sp.simplify(z[j] * Cz.diff(z[j]))
    Djq = sp.simplify(z[j] * qz.diff(z[j]))
    residual = sp.simplify(DjC * qz + Cz * Djq)
    check(
        "DETUNE_%d_TRANSPORT_IDENTITY" % j,
        all(sp.cancel(sp.together(x)) == 0 for x in residual),
    )

# Nine owned L4 singular orbit representatives.
ROOT = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
ORBITS = [
    (0, 0, 1, 1),
    (0, 0, 1, 3),
    (0, 1, 1, 2),
    (1, 0, 1, 2),
    (1, 1, 1, 1),
    (1, 1, 3, 3),
    (2, 0, 1, 1),
    (2, 1, 1, 2),
    (2, 1, 2, 3),
]

aligned = []
for n, ids in enumerate(ORBITS):
    sub = {z[j]: ROOT[ids[j]] for j in range(4)}
    Ce = Cz.subs(sub)
    qe = qz.subs(sub)
    check("ORBIT_%d_RANK9" % n, Ce.rank() == 9)

    for j in range(4):
        w = sp.simplify((z[j] * Cz.diff(z[j])).subs(sub) * qe)
        check(
            "ORBIT_%d_D%d_RAW_IN_IM_C" % (n, j),
            Ce.row_join(w).rank() == Ce.rank(),
        )

    # Forward-coframe metric shadow: q = a y^T + y a^T, a=z-1.
    zv = sp.Matrix([ROOT[k] for k in ids])
    a = zv - sp.ones(4, 1)
    cols = []
    for col in range(4):
        y = sp.eye(4)[:, col]
        Q = sp.expand(a * y.T + y * a.T)
        cols.append(sp.Matrix([Q[r, s] for r, s in SYM]))
    G = sp.Matrix.hstack(*cols)
    if G.row_join(qe).rank() == G.rank():
        aligned.append(n)

check(
    "AFFINE_NULL_ALIGNMENT_EXACTLY_0_4",
    aligned == [0, 4],
    str(aligned),
)

# Exact forward/backward relation.
a = sp.Matrix([z[j] - 1 for j in range(4)])
Z = sp.diag(*[1 / z[j] for j in range(4)])
d_from_a = sp.Matrix([1 / z[j] - 1 for j in range(4)])

check(
    "FORWARD_BACKWARD_VECTOR_IDENTITY",
    sp.simplify(d_from_a + Z * a) == sp.zeros(4, 1),
)
check(
    "FORWARD_BACKWARD_HESSIAN_IDENTITY",
    sp.simplify(
        d_from_a * d_from_a.T - Z * (a * a.T) * Z
    ) == sp.zeros(4),
)

print(
    "IR_IDENTITY: q_backward-q_forward = "
    "(Z-I)q_f + q_f(Z-I) + (Z-I)q_f(Z-I)"
)
print(
    "IR_ORDER: for z=exp(i h k), q_f=O(h^2), Z-I=O(h), "
    "hence mismatch=O(h^3), h^-2 mismatch=O(h)"
)

if FAILS:
    print("J2-METRIC-NULL-HESSIAN-COMPLEX: FAIL", FAILS)
    raise SystemExit(1)

print("J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT")
print(
    "KERNEL: for every nonzero d=z^-1-1, rank C=9 and "
    "ker C=span{vec_sym(d d^T)}"
)
print(
    "DETUNE: raw (D_j C)q is exactly -C(D_j q), so fixed-q "
    "FUGU visibility is null-line transport"
)
print("L4: all 36 raw detune vectors lie in im C exactly")
print(
    "AFFINE: forward-coframe metric shadow contains the backward "
    "null line exactly on owned orbits 0 and 4"
)
print(
    "IR_WELD: -C(k)^T A0^-1 C(k) = (1/4) K_E_eta exactly; "
    "with owned E_eta=-2G this is the designated -1/2 G seed"
)
print(
    "IR_GAUGE: the four leading forward-coframe metric directions are "
    "killed by K_SCHUR after their canonical O(h^2) connection lift"
)
print(
    "SCOPE: exact polarized metric-response symbol plus leading IR Schur weld; "
    "no finite full diffeomorphism gauge or nonlinear Einstein claim"
)
