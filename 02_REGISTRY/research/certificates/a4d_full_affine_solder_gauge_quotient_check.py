#!/usr/bin/env python3
"""Exact controls for the A4D full-affine solder gauge quotient boundary.

Research-only certificate.  Exact rational arithmetic only.

It verifies four layers:

1. On the raw solder matrix alone, an affine-linear translation insertion
   d^T M composes with the Lorentz right action iff M is Lorentz invariant.
   The invariant-form system has rank 15 / nullity 1 and M is proportional to
   eta.  The owned flat translation chart instead requires M = I.

2. The already-owned observer metric h_n repairs the representation mismatch:
   h_rest = I and h_{g n} = g^{-T} h_n g^{-1}.  The observer-flattened
   translation term therefore gives an exact semidirect action on
   (linear link, observer, raw solder row).

3. The repaired action reproduces the owned flat translation chart and the
   owned pure-linear raw solder action.

4. The accepted finite star density is NOT invariant under the constructed
   observer-completed pure translations on a curved background.  An exact L=2 full-torus witness gives
   S_before = -2/3 and S_after = -4/3, while a global Lorentz control preserves
   S exactly.

No continuum, Einstein, time, wave, or torsion-free interpretation is encoded.
"""

from itertools import combinations, product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# Lorentz generators and invariant bilinear-form classification
# ---------------------------------------------------------------------------

LORENTZ_GENS = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    LORENTZ_GENS.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ_GENS.append(X)

for X in LORENTZ_GENS:
    check("LORENTZ_GENERATOR", X.T * ETA + ETA * X == sp.zeros(4))

mvars = sp.symbols("m0:16")
M = sp.Matrix(4, 4, mvars)
eqs = []
for X in LORENTZ_GENS:
    eqs.extend(list(X.T * M + M * X))
Ainv, binv = sp.linear_eq_to_matrix(eqs, mvars)
check("FIXED_INTERTWINER_RANK_15", Ainv.rank() == 15)
check("FIXED_INTERTWINER_NULLITY_1", len(Ainv.nullspace()) == 1)
basisM = sp.Matrix(4, 4, list(Ainv.nullspace()[0]))
check("FIXED_INTERTWINER_IS_ETA_LINE",
      basisM == -ETA or basisM == ETA)

# Exact rational A/B boost.
G = sp.eye(4)
G[0, 0] = sp.Rational(5, 3)
G[0, 1] = sp.Rational(4, 3)
G[1, 0] = sp.Rational(4, 3)
G[1, 1] = sp.Rational(5, 3)
LAMBDA = G.inv()
check("RATIONAL_BOOST_LORENTZ", G.T * ETA * G == ETA)

# M=I matches the flat coordinate chart but is not an intertwiner.
check("IDENTITY_CHART_NOT_LORENTZ_INTERTWINER",
      G.T * I4 * G != I4)

# M=eta composes, but flips a spacelike flat translation coordinate.
eB = sp.Matrix([0, 1, 0, 0])
check("ETA_LOWERING_SPACELIKE_SIGN",
      (eB.T * ETA) == sp.Matrix([[0, -1, 0, 0]]))
check("ETA_LOWERING_MISSES_OWNED_FLAT_CHART",
      eB.T * ETA != eB.T)

# Direct mixed-composition defect for the unlowered M=I law.
d = sp.Matrix([0, 1, 0, 0])
unlowered_seq = d.T * LAMBDA
unlowered_comp = (G * d).T
check("UNLOWERED_MIXED_COMPOSITION_FAILS",
      unlowered_seq != unlowered_comp)

# The eta-lowered law has exact mixed composition.
eta_seq = d.T * ETA * LAMBDA
eta_comp = (G * d).T * ETA
check("ETA_LOWERED_MIXED_COMPOSITION_PASSES",
      eta_seq == eta_comp)

# ---------------------------------------------------------------------------
# Observer metric as an already-owned moving intertwiner
# ---------------------------------------------------------------------------

def observer_metric(n):
    nflat = ETA * n
    return -ETA + 2 * nflat * nflat.T

REST = sp.Matrix([1, 0, 0, 0])
H0 = observer_metric(REST)
check("OBSERVER_REST_METRIC_IS_ID", H0 == I4)
n1 = G * REST
H1 = observer_metric(n1)
check("OBSERVER_METRIC_BOOST_CONGRUENCE",
      G.T * H1 * G == H0)
check("OBSERVER_METRIC_MOVES_NONTRIVIALLY", H1 != H0)

# Exact edge-level semidirect composition.
# Link is y -> x.  Raw solder row lives at x and acts on the right.
RBC = sp.eye(4)
RBC[1, 1] = 0
RBC[1, 2] = 1
RBC[2, 1] = -1
RBC[2, 2] = 0
check("SPATIAL_ROTATION_LORENTZ", RBC.T * ETA * RBC == ETA)

gx = G
gy = RBC
px = RBC
py = G
cx = sp.Matrix([1, 2, 0, 0])
cy = sp.Matrix([0, 1, 1, 0])
dx = sp.Matrix([0, 0, 1, 0])
dy = sp.Matrix([1, 0, 0, 0])
L0 = RBC
n0 = REST
theta0 = sp.Matrix([[1, 2, 3, 4]])

def edge_step(theta, L, n, gx, gy, cx, cy):
    Lp = gx * L * gy.inv()
    np = gx * n
    Hp = observer_metric(np)
    tau = cx - Lp * cy
    thetap = theta * gx.inv() + tau.T * Hp
    return thetap, Lp, np, tau

theta1, L1, n_1, tau1 = edge_step(theta0, L0, n0, gx, gy, cx, cy)
theta2, L2, n_2, tau2 = edge_step(theta1, L1, n_1, px, py, dx, dy)

gxc = px * gx
gyc = py * gy
cxc = px * cx + dx
cyc = py * cy + dy
thetac, Lc, nc, tauc = edge_step(theta0, L0, n0, gxc, gyc, cxc, cyc)

check("OBSERVER_COMPLETED_LINK_COMPOSITION", L2 == Lc)
check("OBSERVER_COMPLETED_OBSERVER_COMPOSITION", n_2 == nc)
check("OBSERVER_COMPLETED_TAU_COCYCLE",
      tauc == px * tau1 + tau2)
check("OBSERVER_COMPLETED_SOLDER_COMPOSITION",
      sp.simplify(theta2 - thetac) == sp.zeros(1, 4))

# Pure-linear restriction is exactly right multiplication by g^{-1}.
zero = sp.zeros(4, 1)
theta_lin, _, n_lin, tau_lin = edge_step(theta0, L0, n0, gx, gy, zero, zero)
check("PURE_LINEAR_TAU_ZERO", tau_lin == zero)
check("PURE_LINEAR_RAW_SOLDER_RIGHT_ACTION",
      theta_lin == theta0 * gx.inv())

# Flat pure translation at rest reproduces the unlowered coordinate chart:
# tau = c_x - c_y and h_rest = I.
theta_flat_row = sp.Matrix([[1, 0, 0, 0]])
cx_t = sp.Matrix([0, 1, 0, 0])
cy_t = sp.Matrix([0, 0, 0, 0])
theta_t, Lt, nt, taut = edge_step(
    theta_flat_row, I4, REST, I4, I4, cx_t, cy_t)
check("FLAT_TRANSLATION_LINEAR_LINK_UNCHANGED", Lt == I4)
check("FLAT_TRANSLATION_OBSERVER_UNCHANGED", nt == REST)
check("FLAT_TRANSLATION_TAU_IS_EDGE_DIFFERENCE", taut == cx_t - cy_t)
check("FLAT_TRANSLATION_RAW_ROW_EQUALS_OWNED_CHART",
      theta_t - theta_flat_row == taut.T)

# ---------------------------------------------------------------------------
# Accepted star density on the exact period-two four-Role torus
# ---------------------------------------------------------------------------

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
    return sp.Matrix([Y[a, b] for a, b in PAIRS])

def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

SITES = list(product(range(2), repeat=4))
BASIS = [I4[:, r] for r in range(4)]

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
    return (P - P.inv()) / 2

def solder_legs(e, x):
    out = []
    for r in range(4):
        row = sp.Matrix([
            ETA[r, a] + e.get((x, r, a), 0)
            for a in range(4)
        ])
        out.append(ETA * row)
    return out

def star_action(links, e):
    total = sp.Integer(0)
    for x in SITES:
        vs = solder_legs(e, x)
        for r, s in PAIRS:
            P = plaquette(links, x, r, s)
            C = bivector_of_tangent(curvature_extract(P))
            u, v = [i for i in range(4) if i not in (r, s)]
            B = wedge_vec(vs[u], vs[v])
            total += complement_orientation((r, s)) * (
                B.T * G2 * STAR * C
            )[0]
    return sp.simplify(total)

# Curved exact witness:
# one A-link carries the rational A/B boost,
# one B-link at the same origin carries a B/C quarter-turn.
origin = (0, 0, 0, 0)
links = {(x, r): I4 for x in SITES for r in range(4)}
links[(origin, 0)] = G
links[(origin, 1)] = RBC

S_before = star_action(links, {})
check("CURVED_CONTROL_ACTION_BEFORE", S_before == sp.Rational(-2, 3))

# Positive control: a global proper Lorentz frame leaves the action unchanged.
links_g = {
    key: sp.simplify(G * L * G.inv())
    for key, L in links.items()
}
# Raw flat solder transforms by right multiplication with G^{-1}.
Theta_g = ETA * G.inv()
e_g = {}
for x in SITES:
    for r in range(4):
        for a in range(4):
            e_g[(x, r, a)] = sp.simplify(Theta_g[r, a] - ETA[r, a])
S_lorentz = star_action(links_g, e_g)
check("STAR_ACTION_GLOBAL_LORENTZ_INVARIANT", S_lorentz == S_before)

# Pure node translation with rest observer.  Since g=I, h_n=I and
# tau_{x,r}=c_x-L_{x,r}c_{x+r}, the observer-completed action gives e'=tau.
cfield = {x: sp.zeros(4, 1) for x in SITES}
cfield[origin] = eB
e_trans = {}
for x in SITES:
    for r in range(4):
        y = site_add(x, r)
        tau = cfield[x] - links[(x, r)] * cfield[y]
        for a in range(4):
            e_trans[(x, r, a)] = sp.simplify(tau[a])

S_after = star_action(links, e_trans)
check("CURVED_CONTROL_ACTION_AFTER_TRANSLATION",
      S_after == sp.Rational(-4, 3))
check("STAR_ACTION_PURE_TRANSLATION_NOT_INVARIANT",
      S_after - S_before == sp.Rational(-2, 3))

# Flat connection remains a harmless control because every curvature vanishes.
flat_links = {(x, r): I4 for x in SITES for r in range(4)}
check("FLAT_ACTION_ZERO", star_action(flat_links, {}) == 0)
check("FLAT_TRANSLATED_ACTION_ZERO",
      star_action(flat_links, e_trans) == 0)

print("RESULT_FIXED_INTERTWINER: unique affine-linear Lorentz-compatible lowering is R*eta; M=I chart is incompatible.")
print("RESULT_OBSERVER_COMPLETION: owned h_n gives an exact semidirect solder action and reproduces the flat translation chart.")
print("RESULT_DENSITY: accepted star density is Lorentz invariant but fails the constructed observer-completed off-shell translation law on a curved background.")
print("RESULT_QUOTIENT: this observer-completed law cannot define the full affine quotient; alternative nonlinear solder gauge laws remain unclassified.")
