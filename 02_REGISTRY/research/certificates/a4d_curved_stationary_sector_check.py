#!/usr/bin/env python3
"""Exact interim controls for the A4D curved stationary-sector problem.

Research-only.  Exact rational arithmetic.

This checker proves only:
  * local solder Euler has a nonzero curvature kernel;
  * the #178 two-link witness forces solder degeneracy at the origin when
    E_v=0 with links fixed;
  * a one-boost curved background has exact all-site nondegenerate E_v=0
    representatives;
  * the one-boost connection-Euler map on free bivector data has rank 282;
  * after eliminating all other sites, exactly four origin constraints remain.

It does NOT prove existence or nonexistence of a nondegenerate joint
E_v=E_L=0 solution.
"""

from fractions import Fraction
from itertools import combinations, product
import random
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
SITES = list(product(range(2), repeat=4))
SITE_INDEX = {x: i for i, x in enumerate(SITES)}

G2 = sp.diag(*[
    ETA[a, a] * ETA[b, b]
    for a, b in PAIRS
])

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

ORIGIN = (0, 0, 0, 0)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

def wedge(u, v):
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])

def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([
        sp.simplify(Y[a, b])
        for a, b in PAIRS
    ])

def curvature(P):
    return sp.simplify((P - P.inv()) / 2)

def plaquette(links, x, r, s):
    xr = site_add(x, r)
    xs = site_add(x, s)
    return sp.simplify(
        links[(x, r)]
        * links[(xr, s)]
        * links[(xs, r)].inv()
        * links[(x, s)].inv()
    )

def vidx(x, r, a):
    return (SITE_INDEX[x] * 4 + r) * 4 + a

def antisym_matrix(q):
    A = sp.zeros(4)
    for value, (a, b) in zip(q, PAIRS):
        A[a, b] = value
        A[b, a] = -value
    return A

def solder_hessian(links):
    H = sp.MutableSparseMatrix(256, 256, {})
    nonzero_cells = 0
    for x in SITES:
        for r, s in PAIRS:
            C = bivector_of_tangent(
                curvature(plaquette(links, x, r, s))
            )
            if C != sp.zeros(6, 1):
                nonzero_cells += 1
            u, v = [i for i in range(4) if i not in (r, s)]
            q = orientation((r, s)) * (G2 * STAR * C)
            A = antisym_matrix(q)
            for a in range(4):
                for b in range(4):
                    if A[a, b]:
                        H[vidx(x, u, a), vidx(x, v, b)] += A[a, b]
                        H[vidx(x, v, b), vidx(x, u, a)] += A[a, b]
    return sp.SparseMatrix(H), nonzero_cells

# ------------------------------------------------------------------
# Local algebraic curvature map
# ------------------------------------------------------------------

cvars = sp.symbols("c0:36")
Cs = {
    face: sp.Matrix(cvars[6 * i:6 * (i + 1)])
    for i, face in enumerate(PAIRS)
}
xvars = sp.symbols("x0:16")
vs = [
    sp.Matrix(xvars[4 * r:4 * (r + 1)])
    for r in range(4)
]

L = sp.Integer(0)
for face in PAIRS:
    u, v = [i for i in range(4) if i not in face]
    L += orientation(face) * (
        wedge(vs[u], vs[v]).T
        * G2 * STAR * Cs[face]
    )[0]

E = [sp.diff(L, x) for x in xvars]
subs = {
    xvars[4 * r + a]: I4[a, r]
    for r in range(4)
    for a in range(4)
}
E0 = sp.Matrix([
    sp.expand(e.subs(subs))
    for e in E
])
A_local = E0.jacobian(sp.Matrix(cvars))

check("LOCAL_CURVATURE_TO_SOLDER_EULER_RANK_16",
      A_local.rank() == 16)
check("LOCAL_CURVATURE_KERNEL_DIM_20",
      len(A_local.nullspace()) == 20)

# Pair-symmetric 6x6 curvature matrix + first Bianchi.
svars = sp.symbols("s0:21")
R6 = sp.zeros(6)
k = 0
for i in range(6):
    for j in range(i, 6):
        R6[i, j] = svars[k]
        R6[j, i] = svars[k]
        k += 1

subc = {}
for i in range(6):
    for j in range(6):
        subc[cvars[6 * i + j]] = R6[i, j]

E_sym = sp.Matrix([
    sp.expand(e.subs(subc))
    for e in E0
])
A_sym = E_sym.jacobian(sp.Matrix(svars))

bianchi = (
    R6[PINDEX[(0, 1)], PINDEX[(2, 3)]]
    - R6[PINDEX[(0, 2)], PINDEX[(1, 3)]]
    + R6[PINDEX[(0, 3)], PINDEX[(1, 2)]]
)
Brow = sp.Matrix([[
    sp.diff(bianchi, s)
    for s in svars
]])
N_bianchi = sp.Matrix.hstack(*Brow.nullspace())
A_bianchi = A_sym * N_bianchi

check("PAIR_SYMMETRIC_BIANCHI_SPACE_DIM_20",
      N_bianchi.shape[1] == 20)
check("Bianchi_RESTRICTED_SOLDER_EULER_RANK_10",
      A_bianchi.rank() == 10)
check("Bianchi_RESTRICTED_CURVATURE_KERNEL_DIM_10",
      len(A_bianchi.nullspace()) == 10)

# ------------------------------------------------------------------
# Two-link #178 witness: exact degeneracy obstruction
# ------------------------------------------------------------------

links_two = {
    (x, r): I4
    for x in SITES
    for r in range(4)
}
links_two[(ORIGIN, 0)] = BOOST
links_two[(ORIGIN, 1)] = RBC

H_two, nz_two = solder_hessian(links_two)
check("TWO_LINK_NONZERO_CURVED_CELLS_11", nz_two == 11)
check("TWO_LINK_SOLDER_HESSIAN_RANK_28", H_two.rank() == 28)

N_two = sp.Matrix.hstack(*H_two.nullspace())
for r in range(4):
    row = N_two[vidx(ORIGIN, r, 3), :]
    check(
        "TWO_LINK_ORIGIN_D_COMPONENT_FORCED_ZERO_ROLE_" + str(r),
        all(value == 0 for value in row),
    )

# ------------------------------------------------------------------
# One-boost positive solder-Euler control
# ------------------------------------------------------------------

links_one = {
    (x, r): I4
    for x in SITES
    for r in range(4)
}
links_one[(ORIGIN, 0)] = BOOST

H_one, nz_one = solder_hessian(links_one)
check("ONE_BOOST_NONZERO_CURVED_CELLS_6", nz_one == 6)
check("ONE_BOOST_SOLDER_HESSIAN_RANK_16", H_one.rank() == 16)
check("ONE_BOOST_SOLDER_HESSIAN_NULLITY_240",
      len(H_one.nullspace()) == 240)

N_one = sp.Matrix.hstack(*H_one.nullspace())
rng = random.Random(991)
found = None
for trial in range(100):
    coeff = sp.Matrix([
        rng.randint(-3, 3)
        for _ in range(N_one.cols)
    ])
    candidate = N_one * coeff
    dets = []
    for x in SITES:
        M = sp.Matrix(
            4, 4,
            lambda a, r: candidate[vidx(x, r, a)]
        )
        dets.append(sp.factor(M.det()))
    if all(d != 0 for d in dets):
        found = (trial, candidate, dets)
        break

check("ONE_BOOST_NONDEGENERATE_EV_ZERO_WITNESS_FOUND",
      found is not None)
check("ONE_BOOST_NONDEGENERATE_WITNESS_IS_EV_ZERO",
      H_one * found[1] == sp.zeros(256, 1))
print("ONE_BOOST_WITNESS_TRIAL", found[0])
print("ONE_BOOST_SITE_DETERMINANTS", found[2])

# ------------------------------------------------------------------
# Connection Euler as a linear operator on free B data
# ------------------------------------------------------------------

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

cells = []
incidence = {
    key: []
    for key in links_one
}

for x in SITES:
    for r, s in PAIRS:
        xr = site_add(x, r)
        xs = site_add(x, s)
        keys = [
            (x, r),
            (xr, s),
            (xs, r),
            (x, s),
        ]
        invflags = [False, False, True, True]
        mats = [
            links_one[keys[i]].inv()
            if invflags[i]
            else links_one[keys[i]]
            for i in range(4)
        ]
        P = sp.eye(4)
        for M in mats:
            P = P * M
        cell = {
            "x": x,
            "face": (r, s),
            "keys": keys,
            "inv": invflags,
            "mats": mats,
            "P": sp.simplify(P),
        }
        ci = len(cells)
        cells.append(cell)
        for pos, key in enumerate(keys):
            incidence[key].append((ci, pos))

def dmat(L, dL, inverse):
    if not inverse:
        return dL
    Li = L.inv()
    return sp.simplify(-Li * dL * Li)

def cell_dP(cell, pos, dL):
    dm = dmat(
        links_one[cell["keys"][pos]],
        dL,
        cell["inv"][pos],
    )
    out = sp.eye(4)
    for j, M in enumerate(cell["mats"]):
        out = out * (dm if j == pos else M)
    return sp.simplify(out)

def dcurvature(P, dP):
    Pi = P.inv()
    return sp.simplify(
        (dP + Pi * dP * Pi) / 2
    )

rows = []
for x in SITES:
    for r in range(4):
        key = (x, r)
        for X in LORENTZ:
            dL = sp.simplify(X * links_one[key])
            row = {}
            for ci, pos in incidence[key]:
                cell = cells[ci]
                dP = cell_dP(cell, pos, dL)
                dC = bivector_of_tangent(
                    dcurvature(cell["P"], dP)
                )
                q = (
                    orientation(cell["face"])
                    * G2 * STAR * dC
                )
                for k, value in enumerate(q):
                    if value:
                        col = ci * 6 + k
                        row[col] = sp.simplify(
                            row.get(col, 0) + value
                        )
            rows.append({
                c: v
                for c, v in row.items()
                if v != 0
            })

def to_fraction(q):
    q = sp.Rational(q)
    return Fraction(int(q.p), int(q.q))

def sparse_rank_Q(rows):
    pivots = {}
    rank = 0
    for data in rows:
        row = {
            c: to_fraction(v)
            for c, v in data.items()
            if v != 0
        }
        while row:
            c = min(row)
            if c not in pivots:
                f = row[c]
                row = {
                    j: v / f
                    for j, v in row.items()
                }
                pivots[c] = row
                rank += 1
                break
            prow = pivots[c]
            factor = row[c]
            for j, value in prow.items():
                new = row.get(j, Fraction(0)) - factor * value
                if new:
                    row[j] = new
                elif j in row:
                    del row[j]
    return rank, pivots

rank_B, piv_B = sparse_rank_Q(rows)
check("CONNECTION_EULER_FREE_B_RANK_282", rank_B == 282)
check("CONNECTION_EULER_FREE_B_NULLITY_294",
      576 - rank_B == 294)

# Independent modular rank controls.
def mod_value(q, p):
    q = sp.Rational(q)
    return (
        int(q.p) % p
        * pow(int(q.q) % p, -1, p)
    ) % p

def sparse_rank_mod(rows, p):
    pivots = {}
    rank = 0
    for data in rows:
        row = {
            c: mod_value(v, p)
            for c, v in data.items()
            if mod_value(v, p)
        }
        while row:
            c = min(row)
            if c not in pivots:
                inv = pow(row[c], -1, p)
                row = {
                    j: (v * inv) % p
                    for j, v in row.items()
                }
                pivots[c] = row
                rank += 1
                break
            prow = pivots[c]
            factor = row[c]
            for j, value in prow.items():
                new = (
                    row.get(j, 0)
                    - factor * value
                ) % p
                if new:
                    row[j] = new
                elif j in row:
                    del row[j]
    return rank

for prime in (1000003, 1000033, 1000037):
    check(
        "CONNECTION_EULER_MOD_RANK_282_" + str(prime),
        sparse_rank_mod(rows, prime) == 282,
    )

# ------------------------------------------------------------------
# Eliminate all non-origin B variables
# ------------------------------------------------------------------

origin_cell_ids = [
    i
    for i, cell in enumerate(cells)
    if cell["x"] == ORIGIN
]
origin_cols = set()
for ci in origin_cell_ids:
    origin_cols.update(
        range(ci * 6, ci * 6 + 6)
    )

other_cols = [
    c
    for c in range(576)
    if c not in origin_cols
]
origin_cols_sorted = sorted(origin_cols)
new_order = other_cols + origin_cols_sorted
newpos = {
    c: i
    for i, c in enumerate(new_order)
}
rows_reordered = [
    {
        newpos[c]: v
        for c, v in row.items()
    }
    for row in rows
]
rank_reordered, piv_reordered = sparse_rank_Q(
    rows_reordered
)
check("REORDERED_CONNECTION_RANK_STILL_282",
      rank_reordered == 282)

pure_origin_rows = []
for pivot, row in piv_reordered.items():
    if pivot >= len(other_cols):
        pure_origin_rows.append((pivot, row))

check("ORIGIN_REDUCED_CONSTRAINT_COUNT_4",
      len(pure_origin_rows) == 4)

def label(global_col):
    ci, k = divmod(global_col, 6)
    return (
        cells[ci]["face"],
        PAIRS[k],
    )

constraints = []
for pivot, row in pure_origin_rows:
    terms = []
    for newcol, value in sorted(row.items()):
        check("PURE_ORIGIN_REDUCED_ROW",
              newcol >= len(other_cols))
        global_col = new_order[newcol]
        terms.append((label(global_col), value))
    constraints.append(terms)

expected = {
    frozenset([
        (((0, 1), (0, 3)), Fraction(1)),
        (((0, 2), (0, 3)), Fraction(-1)),
        (((0, 3), (0, 3)), Fraction(1)),
    ]),
    frozenset([
        (((0, 1), (0, 2)), Fraction(1)),
        (((0, 2), (0, 2)), Fraction(-1)),
        (((0, 3), (0, 2)), Fraction(1)),
    ]),
    frozenset([
        (((0, 1), (1, 3)), Fraction(1)),
        (((0, 2), (1, 3)), Fraction(-1)),
        (((0, 3), (1, 3)), Fraction(1)),
    ]),
    frozenset([
        (((0, 1), (1, 2)), Fraction(1)),
        (((0, 2), (1, 2)), Fraction(-1)),
        (((0, 3), (1, 2)), Fraction(1)),
    ]),
}

actual = {
    frozenset(terms)
    for terms in constraints
}
check("ORIGIN_REDUCED_CONSTRAINTS_MATCH",
      actual == expected)

print("ORIGIN_REDUCED_CONSTRAINTS")
for terms in constraints:
    print(terms)

print("RESULT_LOCAL: solder Euler has nonzero algebraic curvature kernels.")
print("RESULT_TWO_LINK: the exact #178 two-link background forces origin solder degeneracy at E_v=0.")
print("RESULT_ONE_BOOST: a different exact curved background has all-site nondegenerate E_v=0 representatives.")
print("RESULT_CONNECTION: free-B connection Euler has rank 282/nullity 294; four reduced origin constraints remain after eliminating other sites.")
print("SCOPE: no joint nondegenerate E_v=E_L=0 solution or no-go is claimed yet.")
