#!/usr/bin/env python3
"""Exact research controls for nonlinear rigidity after Cartan gauge synthesis.

Research-only. Exact SymPy arithmetic.

This certificate establishes three scoped facts for the accepted A4D star density:

1. Local solder Euler map:
   At identity solder, the coframe/solder Euler equation is a surjective
   rank-16 linear map from the 36 curvature-bivector components to 16 solder
   Euler components. Its kernel is 20-dimensional. Restricted to pair-symmetric
   algebraic curvature it has an 11-dimensional kernel; imposing the 4D first
   Bianchi relation leaves a 10-dimensional nonzero kernel.

   Therefore solder stationarity alone does NOT force curvature to vanish.

2. The exact #178 curved witness is not repairable into a nondegenerate
   stationary solder configuration at fixed links:
   at the origin its local solder Hessian has rank 8 / nullity 8, but every
   kernel solder matrix has a zero fourth internal row, hence determinant zero.

3. The six physical L=2 checkerboard quotient-null directions do not
   nonlinearly bifurcate from the flat background.
   In each of the three Lorentz-null momentum sectors there are two physical
   quotient-null modes. Exact nilpotent null-rotation exponentiation gives a
   second-order zero-momentum solder Euler source proportional to p^2+q^2.
   It projects onto a pure coframe null covector of the zero-momentum Hessian:
       E00^(2) = -32 (p^2+q^2).
   Across all three sectors:
       E00^(2) = -32 sum_j (p_j^2+q_j^2),
   so for real amplitudes no nonzero physical checkerboard tangent admits an
   analytic stationary continuation through flat space at second order.

This does not exclude finite-amplitude disconnected curved critical points,
higher L, or other carriers/actions. No Einstein/time/wave interpretation.
"""

from itertools import combinations, product
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
SITES = list(product(range(2), repeat=4))

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# Lorentz tangent basis.
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

# Degree-two metric/star.
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
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([sp.expand(Y[a, b]) for a, b in PAIRS])

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
# I. Local solder Euler map at identity solder
# ---------------------------------------------------------------------------

vvars = sp.symbols("v0:16")
vcols = [sp.Matrix(vvars[4*r:4*r+4]) for r in range(4)]
cvars = sp.symbols("c0:36")
C = {}
k = 0
for face in PAIRS:
    C[face] = sp.Matrix(cvars[k:k+6])
    k += 6

Slocal = sp.Integer(0)
for r, s in PAIRS:
    u, v = [i for i in range(4) if i not in (r, s)]
    B = wedge_vec(vcols[u], vcols[v])
    Slocal += complement_orientation((r, s)) * (
        B.T * G2 * STAR * C[(r, s)]
    )[0]
Slocal = sp.expand(Slocal)

grad = sp.Matrix([sp.diff(Slocal, z) for z in vvars])
subsI = {
    vvars[4*r+a]: (1 if r == a else 0)
    for r in range(4)
    for a in range(4)
}
gradI = sp.Matrix([sp.expand(g.subs(subsI)) for g in grad])

Ae = sp.zeros(16, 36)
for i, g in enumerate(gradI):
    for j, c in enumerate(cvars):
        Ae[i, j] = sp.diff(g, c)

check("LOCAL_SOLDER_EULER_CURVATURE_RANK_16", Ae.rank() == 16)
check("LOCAL_SOLDER_EULER_CURVATURE_KERNEL_20", len(Ae.nullspace()) == 20)

def cindex(i, j):
    return 6*i + j

# Pair-exchange symmetry on the 6x6 curvature matrix.
sym_rows = []
for i in range(6):
    for j in range(i+1, 6):
        row = [0] * 36
        row[cindex(i, j)] = 1
        row[cindex(j, i)] = -1
        sym_rows.append(row)
Sym = sp.Matrix(sym_rows)
check("PAIR_SYMMETRY_RANK_15", Sym.rank() == 15)
check("PAIR_SYMMETRIC_CURVATURE_DIM_21", 36 - Sym.rank() == 21)

SymEL = Sym.col_join(Ae)
check("PAIR_SYMMETRIC_SOLDER_EL_RANK_10",
      SymEL.rank() - Sym.rank() == 10)
check("PAIR_SYMMETRIC_SOLDER_EL_KERNEL_11",
      36 - SymEL.rank() == 11)

# One 4D algebraic first-Bianchi relation:
# R_01,23 - R_02,13 + R_03,12 = 0.
brow = [0] * 36
brow[cindex(PINDEX[(0,1)], PINDEX[(2,3)])] = 1
brow[cindex(PINDEX[(0,2)], PINDEX[(1,3)])] = -1
brow[cindex(PINDEX[(0,3)], PINDEX[(1,2)])] = 1
Alg = Sym.col_join(sp.Matrix([brow]))
check("ALGEBRAIC_CURVATURE_CONSTRAINT_RANK_16", Alg.rank() == 16)
check("ALGEBRAIC_CURVATURE_DIM_20", 36 - Alg.rank() == 20)

AlgEL = Alg.col_join(Ae)
check("ALGEBRAIC_CURVATURE_SOLDER_EL_RANK_10",
      AlgEL.rank() - Alg.rank() == 10)
check("ALGEBRAIC_CURVATURE_SOLDER_EL_KERNEL_10",
      36 - AlgEL.rank() == 10)

# Explicit nonzero diagonal algebraic-curvature kernel witness:
# (01|01)=+1, (03|03)=-1, (12|12)=-1, (23|23)=+1.
cw = sp.zeros(36, 1)
for face, val in {
    (0,1): 1,
    (0,3): -1,
    (1,2): -1,
    (2,3): 1,
}.items():
    i = PINDEX[face]
    cw[cindex(i, i)] = val
check("ALGEBRAIC_CURVATURE_WITNESS_NONZERO", cw != sp.zeros(36, 1))
check("ALGEBRAIC_CURVATURE_WITNESS_PAIR_BIANCHI",
      Alg * cw == sp.zeros(Alg.rows, 1))
check("ALGEBRAIC_CURVATURE_WITNESS_SOLDER_EL_ZERO",
      Ae * cw == sp.zeros(16, 1))

# ---------------------------------------------------------------------------
# II. Exact #178 witness: fixed links force degenerate stationary solder
# ---------------------------------------------------------------------------

BOOST = sp.eye(4)
BOOST[0, 0] = sp.Rational(5, 3)
BOOST[0, 1] = sp.Rational(4, 3)
BOOST[1, 0] = sp.Rational(4, 3)
BOOST[1, 1] = sp.Rational(5, 3)

RBC = sp.eye(4)
RBC[1, 1] = 0
RBC[1, 2] = 1
RBC[2, 1] = -1
RBC[2, 2] = 0

check("BOOST_LORENTZ", BOOST.T * ETA * BOOST == ETA)
check("RBC_LORENTZ", RBC.T * ETA * RBC == ETA)

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

def plaquette(links, x, r, s):
    xr = site_add(x, r)
    xs = site_add(x, s)
    return (
        links[(x, r)]
        * links[(xr, s)]
        * links[(xs, r)].inv()
        * links[(x, s)].inv()
    )

def curvature_extract(P):
    return sp.expand((P - P.inv()) / 2)

origin = (0, 0, 0, 0)
links = {(x, r): I4 for x in SITES for r in range(4)}
links[(origin, 0)] = BOOST
links[(origin, 1)] = RBC

C0 = {
    face: bivector_of_tangent(curvature_extract(plaquette(links, origin, *face)))
    for face in PAIRS
}
S0 = sp.Integer(0)
for r, s in PAIRS:
    u, v = [i for i in range(4) if i not in (r, s)]
    S0 += complement_orientation((r, s)) * (
        wedge_vec(vcols[u], vcols[v]).T
        * G2 * STAR * C0[(r, s)]
    )[0]
H=¸ß^Ü…ªì¶»§q«^