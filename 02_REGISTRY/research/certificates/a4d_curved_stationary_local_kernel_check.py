#!/usr/bin/env python3
"""Exact local curvature/solder Euler controls for A4D star density.

Research-only. Exact rational arithmetic.

This certificate separates the solder Euler equation from the connection Euler
equation.

It proves:

1. At canonical nondegenerate solder, the local map from the six curvature
   bivectors (36 components) to the 16 solder-Euler components has rank 16 and
   a 20-dimensional kernel.

2. Restricting to the algebraic-curvature class with pair symmetry and first
   Bianchi leaves a 20-dimensional curvature space.  The solder-Euler map has
   rank 10 there, hence a 10-dimensional nonzero curvature kernel.

Therefore the solder Euler equation alone does NOT force flat curvature.

No connection-Euler solution, continuum curvature tensor, Einstein equation,
or spacetime interpretation is claimed.
"""

from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)

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


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def wedge_vec(u, v):
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])


def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1


# ---------------------------------------------------------------------------
# Full local curvature -> solder Euler map
# ---------------------------------------------------------------------------

cvars = sp.symbols("c0:36")
curvature = {
    p: sp.Matrix(cvars[6 * i:6 * (i + 1)])
    for i, p in enumerate(PAIRS)
}

z = sp.symbols("z0:16")
legs = [
    sp.Matrix(z[4 * r:4 * r + 4])
    for r in range(4)
]

density = sp.Integer(0)
for r, s in PAIRS:
    u, v = [i for i in range(4) if i not in (r, s)]
    B = wedge_vec(legs[u], legs[v])
    density += complement_orientation((r, s)) * (
        B.T * G2 * STAR * curvature[(r, s)]
    )[0]

canonical = {}
for r in range(4):
    for a in range(4):
        canonical[z[4 * r + a]] = 1 if r == a else 0

euler = sp.Matrix([
    sp.diff(density, zz).subs(canonical)
    for zz in z
])
M = euler.jacobian(cvars)

check("FULL_CURVATURE_SPACE_DIM_36", M.cols == 36)
check("SOLDER_EULER_COMPONENTS_16", M.rows == 16)
check("FULL_CURVATURE_TO_SOLDER_EULER_RANK_16", M.rank() == 16)
check("FULL_CURVATURE_SOLDER_EULER_KERNEL_DIM_20",
      len(M.nullspace()) == 20)


# ---------------------------------------------------------------------------
# Algebraic curvature subclass: pair symmetry + first Bianchi
# ---------------------------------------------------------------------------

# Arrange curvature as a symmetric 6x6 pair matrix R_[rs],[ab].
# Pair antisymmetry is already encoded by the bivector indices.
svars = []
R = sp.zeros(6)
for i in range(6):
    for j in range(i, 6):
        q = sp.symbols("s_%d_%d" % (i, j))
        svars.append(q)
        R[i, j] = q
        R[j, i] = q

i01 = PINDEX[(0, 1)]
i02 = PINDEX[(0, 2)]
i03 = PINDEX[(0, 3)]
i12 = PINDEX[(1, 2)]
i13 = PINDEX[(1, 3)]
i23 = PINDEX[(2, 3)]

# In four dimensions the remaining algebraic first-Bianchi condition is the
# vanishing totally antisymmetric component.
bianchi = R[i01, i23] - R[i02, i13] + R[i03, i12]
Brow = sp.Matrix([[
    sp.diff(bianchi, q)
    for q in svars
]])
Bnull = Brow.nullspace()
T21to20 = sp.Matrix.hstack(*Bnull)

check("PAIR_SYMMETRIC_DIM_21", len(svars) == 21)
check("BIANCHI_RANK_1", Brow.rank() == 1)
check("ALGEBRAIC_CURVATURE_DIM_20", T21to20.cols == 20)

# Map the 21 symmetric coordinates to the original 36 curvature coordinates.
Tsym = sp.zeros(36, 21)
for fi in range(6):
    for bj in range(6):
        expr = R[fi, bj]
        for k, q in enumerate(svars):
            coeff = sp.diff(expr, q)
            if coeff:
                Tsym[6 * fi + bj, k] = coeff

Talg = Tsym * T21to20
check("ALGEBRAIC_CURVATURE_EMBEDDING_RANK_20", Talg.rank() == 20)

Malg = M * Talg
check("ALGEBRAIC_CURVATURE_TO_SOLDER_EULER_RANK_10",
      Malg.rank() == 10)
check("ALGEBRAIC_CURVATURE_SOLDER_EULER_KERNEL_DIM_10",
      len(Malg.nullspace()) == 10)

# Give one explicit nonzero algebraic-curvature kernel witness.
w = Malg.nullspace()[0]
Cw = Talg * w
check("NONZERO_CURVATURE_KERNEL_WITNESS", Cw != sp.zeros(36, 1))
check("NONZERO_CURVATURE_WITNESS_KILLS_SOLDER_EULER",
      M * Cw == sp.zeros(16, 1))

print("RESULT_LOCAL: solder Euler alone does not force C=0.")
print("RESULT_ALGEBRAIC: pair symmetry + first Bianchi still leave a 10-dimensional nonzero curvature kernel.")
print("SCOPE: finite-holonomy realizability and the connection Euler equation remain separate gates.")
