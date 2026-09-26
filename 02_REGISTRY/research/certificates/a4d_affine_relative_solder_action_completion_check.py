#!/usr/bin/env python3
"""Exact finite certificate for the affine relative-solder star completion.

Research-only. Exact rational arithmetic.

Candidate:
    W^(lambda)_{x,r} = Theta_{x,r} - lambda * b_{x,r}^T h_{n_x}

with the already-constructed observer-completed affine solder law

    L' = g_x L g_y^-1
    b' = g_x b + tau
    n' = g_x n
    Theta' = Theta g_x^-1 + tau^T h_{n'}

where tau = c_x - L' c_y.

The certificate checks:
  * exact observer congruence;
  * exact selector law
        W'^(lambda) = W^(lambda) g^-1 + (1-lambda) tau^T h_{n'};
  * lambda=1 gives pure linear row covariance on all 64 L=2 links;
  * the completed star density is invariant cell-by-cell under a genuinely
    site-dependent mixed Lorentz+translation gauge;
  * a curved pure-translation witness gives
        S_after(lambda)-S_before = 2/3*(lambda-1),
    so affine covariance uniquely selects lambda=1 in this family;
  * b=0 reduces exactly to the accepted star density;
  * on the flat translation-gauge chart, W^(1)=eta exactly;
  * a nonzero independent affine shift changes the completed action, so b is
    not erased;
  * one curved L=2 witness has injective covariant node-difference D_L;
  * nevertheless the completed action has a larger accidental edge-diagonal
    invariance: a one-edge matched (Theta,b) shift lies outside im(D_L) but
    leaves W and the action exactly unchanged.

No Einstein/diffeomorphism/torsion-free/time/wave interpretation is encoded.
"""

from itertools import combinations, product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
SITES = list(product(range(2), repeat=4))
SITE_INDEX = {x: i for i, x in enumerate(SITES)}

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# Lorentz / observer data
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

RCD = sp.eye(4)
RCD[2, 2] = 0
RCD[2, 3] = 1
RCD[3, 2] = -1
RCD[3, 3] = 0

for name, g in (("BOOST", BOOST), ("RBC", RBC), ("RCD", RCD)):
    check(name + "_LORENTZ", g.T * ETA * g == ETA)
    check(name + "_DET_ONE", sp.simplify(g.det()) == 1)

REST = sp.Matrix([1, 0, 0, 0])

def observer_metric(n):
    nflat = ETA * n
    return sp.simplify(-ETA + 2 * nflat * nflat.T)

check("REST_OBSERVER_METRIC_ID", observer_metric(REST) == I4)

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

def gauge_at(x):
    g = I4
    if x[0]:
        g = BOOST * g
    if x[1]:
        g = RBC * g
    if x[2]:
        g = RCD * g
    if x[3]:
        g = BOOST.inv() * g
    return sp.simplify(g)

gfield = {x: gauge_at(x) for x in SITES}
check("GAUGE_FIELD_SITE_DEPENDENT",
      len({tuple(gfield[x]) for x in SITES}) > 4)

for x in SITES:
    g = gfield[x]
    n1 = g * REST
    H1 = observer_metric(n1)
    check("OBSERVER_CONGRUENCE_" + "".join(map(str, x)),
          sp.simplify(g.T * H1 * g) == observer_metric(REST))

# ---------------------------------------------------------------------------
# Lambda^2 / star action
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
    return sp.Matrix([sp.simplify(Y[a, b]) for a, b in PAIRS])

def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

def plaquette(links, x, r, s):
    xr = site_add(x, r)
    xs = site_add(x, s)
    return sp.simplify(
        links[(x, r)]
        * links[(xr, s)]
        * links[(xs, r)].inv()
        * links[(x, s)].inv()
    )

def curvature_extract(P):
    return sp.simplify((P - P.inv()) / 2)

def relative_row(theta_row, b, n, lam):
    return sp.simplify(theta_row - lam * b.T * observer_metric(n))

def relative_rows(theta, bfield, nfield, lam):
    return {
        (x, r): relative_row(
            theta[(x, r)],
            bfield[(x, r)],
            nfield[x],
            lam,
        )
        for x in SITES
        for r in range(4)
    }

def density_terms(links, rows):
    out = {}
    for x in SITES:
        legs = [
            ETA * rows[(x, r)].T
            for r in range(4)
        ]
        for r, s in PAIRS:
            C = bivector_of_tangent(
                curvature_extract(plaquette(links, x, r, s))
            )
            u, v = [i for i in range(4) if i not in (r, s)]
            B = wedge_vec(legs[u], legs[v])
            out[(x, r, s)] = sp.simplify(
                complement_orientation((r, s))
                * (B.T * G2 * STAR * C)[0]
            )
    return out

def star_action(links, rows):
    return sp.simplify(sum(density_terms(links, rows).values(), sp.Integer(0)))

# ---------------------------------------------------------------------------
# Base curved affine configuration
# ---------------------------------------------------------------------------

origin = (0, 0, 0, 0)

links = {(x, r): I4 for x in SITES for r in range(4)}
links[(origin, 0)] = BOOST
links[(origin, 1)] = RBC
links[((1, 0, 0, 0), 2)] = RCD

# Raw solder rows: flat plus two small rational perturbations.
theta = {
    (x, r): sp.Matrix([[ETA[r, a] for a in range(4)]])
    for x in SITES
    for r in range(4)
}
theta[(origin, 2)] += sp.Matrix([[0, sp.Rational(1, 3), 0, 0]])
theta[((1, 0, 0, 0), 3)] += sp.Matrix([[0, 0, sp.Rational(-2, 5), 0]])

# Independent affine shifts.
bfield = {
    (x, r): sp.zeros(4, 1)
    for x in SITES
    for r in range(4)
}
bfield[(origin, 3)] = sp.Matrix([sp.Rational(1, 5), 0, sp.Rational(-1, 4), 0])
bfield[((1, 1, 0, 0), 1)] = sp.Matrix([0, sp.Rational(2, 7), 0, sp.Rational(1, 6)])

nfield = {x: REST for x in SITES}

# Nonconstant node translations.
cfield = {
    x: sp.Matrix([
        sp.Rational(x[0] - x[1], 3),
        sp.Rational(x[1] + x[2], 5),
        sp.Rational(x[2] - x[3], 7),
        sp.Rational(x[3] + x[0], 11),
    ])
    for x in SITES
}

# ---------------------------------------------------------------------------
# Full affine transformation
# ---------------------------------------------------------------------------

links_g = {}
b_g = {}
theta_g = {}
n_g = {}

for x in SITES:
    gx = gfield[x]
    n_g[x] = sp.simplify(gx * nfield[x])

for x in SITES:
    gx = gfield[x]
    for r in range(4):
        y = site_add(x, r)
        gy = gfield[y]

        Lp = sp.simplify(gx * links[(x, r)] * gy.inv())
        tau = sp.simplify(cfield[x] - Lp * cfield[y])

        links_g[(x, r)] = Lp
        b_g[(x, r)] = sp.simplify(gx * bfield[(x, r)] + tau)

        Hp = observer_metric(n_g[x])
        theta_g[(x, r)] = sp.simplify(
            theta[(x, r)] * gx.inv()
            + tau.T * Hp
        )

# Exact symbolic lambda transformation law.
lam = sp.symbols("lam")
for x in SITES:
    gx = gfield[x]
    Hp = observer_metric(n_g[x])
    for r in range(4):
        y = site_add(x, r)
        tau = sp.simplify(cfield[x] - links_g[(x, r)] * cfield[y])

        W_before = relative_row(
            theta[(x, r)], bfield[(x, r)], nfield[x], lam
        )
        W_after = relative_row(
            theta_g[(x, r)], b_g[(x, r)], n_g[x], lam
        )
        rhs = sp.simplify(
            W_before * gx.inv()
            + (1 - lam) * tau.T * Hp
        )
        check(
            "LAMBDA_TRANSFORM_LAW_" + "".join(map(str, x)) + "_" + str(r),
            sp.simplify(W_after - rhs) == sp.zeros(1, 4),
        )

# Lambda=1: exact pure row covariance on every link.
W1 = relative_rows(theta, bfield, nfield, sp.Integer(1))
W1_g = relative_rows(theta_g, b_g, n_g, sp.Integer(1))
for x in SITES:
    gx = gfield[x]
    for r in range(4):
        check(
            "RELATIVE_SOLDER_ROW_COVARIANCE_" + "".join(map(str, x)) + "_" + str(r),
            sp.simplify(W1_g[(x, r)] - W1[(x, r)] * gx.inv())
            == sp.zeros(1, 4),
        )

# Complete density is invariant cell-by-cell.
before_terms = density_terms(links, W1)
after_terms = density_terms(links_g, W1_g)
check(
    "ALL_96_COMPLETED_DENSITIES_AFFINE_INVARIANT",
    all(
        sp.simplify(after_terms[k] - before_terms[k]) == 0
        for k in before_terms
    ),
)
check(
    "COMPLETED_ACTION_FULL_AFFINE_INVARIANT",
    sp.simplify(star_action(links_g, W1_g) - star_action(links, W1)) == 0,
)

# ---------------------------------------------------------------------------
# Lambda selector: curved pure translation
# ---------------------------------------------------------------------------

selector_links = {(x, r): I4 for x in SITES for r in range(4)}
selector_links[(origin, 0)] = BOOST
selector_links[(origin, 1)] = RBC

theta0 = {
    (x, r): sp.Matrix([[ETA[r, a] for a in range(4)]])
    for x in SITES
    for r in range(4)
}
zero_b = {
    (x, r): sp.zeros(4, 1)
    for x in SITES
    for r in range(4)
}
rest_n = {x: REST for x in SITES}

S_before = star_action(
    selector_links,
    relative_rows(theta0, zero_b, rest_n, lam),
)
check("SELECTOR_ACTION_BEFORE", S_before == sp.Rational(-2, 3))

selector_c = {x: sp.zeros(4, 1) for x in SITES}
selector_c[origin] = sp.Matrix([0, 1, 0, 0])

theta_t = {}
b_t = {}
for x in SITES:
    for r in range(4):
        y = site_add(x, r)
        tau = sp.simplify(
            selector_c[x] - selector_links[(x, r)] * selector_c[y]
        )
        theta_t[(x, r)] = sp.simplify(theta0[(x, r)] + tau.T)
        b_t[(x, r)] = tau

S_after = sp.factor(
    star_action(
        selector_links,
        relative_rows(theta_t, b_t, rest_n, lam),
    )
)
delta_selector = sp.factor(S_after - S_before)

check(
    "LAMBDA_SELECTOR_POLYNOMIAL",
    delta_selector == sp.Rational(2, 3) * (lam - 1),
)
check(
    "LAMBDA_ONE_UNIQUE_SELECTOR",
    sp.solve(sp.Eq(delta_selector, 0), lam) == [1],
)
check(
    "LAMBDA_ZERO_REPRODUCES_OLD_FAILURE",
    sp.simplify(S_after.subs(lam, 0)) == sp.Rational(-4, 3),
)

# ---------------------------------------------------------------------------
# Flat gauge diagonal
# ---------------------------------------------------------------------------

flat_links = {(x, r): I4 for x in SITES for r in range(4)}
flat_c = {
    x: sp.Matrix([x[0], -x[1], x[2], -x[3]])
    for x in SITES
}
flat_theta = {}
flat_b = {}

for x in SITES:
    for r in range(4):
        y = site_add(x, r)
        tau = flat_c[x] - flat_c[y]
        flat_theta[(x, r)] = sp.simplify(theta0[(x, r)] + tau.T)
        flat_b[(x, r)] = tau

flat_W = relative_rows(flat_theta, flat_b, rest_n, sp.Integer(1))
check(
    "FLAT_TRANSLATION_GAUGE_RELATIVE_SOLDER_UNCHANGED",
    all(flat_W[(x, r)] == theta0[(x, r)] for x in SITES for r in range(4)),
)
check(
    "FLAT_TRANSLATION_GAUGE_COMPLETED_ACTION_ZERO",
    star_action(flat_links, flat_W) == 0,
)

# ---------------------------------------------------------------------------
# b=0 reduction and independent pure-shift visibility
# ---------------------------------------------------------------------------

check(
    "B_ZERO_REDUCES_TO_ACCEPTED_STAR",
    star_action(selector_links, relative_rows(theta0, zero_b, rest_n, 1))
    == star_action(selector_links, theta0),
)

pure_b = dict(zero_b)
pure_b[(origin, 0)] = sp.Matrix([1, 0, 0, 0])
S_pure_shift = star_action(
    selector_links,
    relative_rows(theta0, pure_b, rest_n, 1),
)
check(
    "PURE_AFFINE_SHIFT_VISIBLE",
    S_pure_shift == sp.Rational(-5, 3)
    and S_pure_shift != S_before,
)

# ---------------------------------------------------------------------------
# Translation stabilizer / principal-sector witness
# ---------------------------------------------------------------------------

def covariant_node_difference_matrix(links):
    # c -> tau_{x,r}=c_x-L_{x,r}c_{x+r}
    M = sp.zeros(len(SITES) * 4 * 4, len(SITES) * 4)
    row = 0
    for x in SITES:
        for r in range(4):
            y = site_add(x, r)
            for a in range(4):
                M[row, SITE_INDEX[x] * 4 + a] = 1
                for b in range(4):
                    M[row, SITE_INDEX[y] * 4 + b] -= links[(x, r)][a, b]
                row += 1
    return M

DL = covariant_node_difference_matrix(links)
check("CURVED_TRANSLATION_STABILIZER_TRIVIAL", DL.rank() == 64)

# ---------------------------------------------------------------------------
# Fatal overquotient control: matched edge shift outside node-gauge image
# ---------------------------------------------------------------------------

# u is supported on one edge/component.  If it were a pure node translation,
# it would lie in the image of D_L.  Exact augmented rank says it does not.
u = sp.zeros(len(SITES) * 4 * 4, 1)
row = 0
for x in SITES:
    for r in range(4):
        for a in range(4):
            if x == origin and r == 0 and a == 0:
                u[row] = 1
            row += 1

check("ONE_EDGE_MATCHED_SHIFT_NOT_NODE_GAUGE",
      DL.row_join(u).rank() == 65)

theta_match = {
    key: sp.Matrix(value)
    for key, value in theta0.items()
}
b_match = {
    key: sp.Matrix(value)
    for key, value in zero_b.items()
}
edge_u = sp.Matrix([1, 0, 0, 0])
theta_match[(origin, 0)] = theta_match[(origin, 0)] + edge_u.T
b_match[(origin, 0)] = b_match[(origin, 0)] + edge_u

W_match = relative_rows(theta_match, b_match, rest_n, 1)
W_base = relative_rows(theta0, zero_b, rest_n, 1)

check("MATCHED_NONGAUGE_SHIFT_LEAVES_RELATIVE_SOLDER",
      all(W_match[key] == W_base[key] for key in W_base))

S_base_principal = star_action(links, W_base)
S_match_principal = star_action(links, W_match)
check("MATCHED_NONGAUGE_SHIFT_LEAVES_ACTION",
      S_match_principal == S_base_principal)

# Since W is nondegenerate, any full-affine gauge relating these two
# configurations while leaving W fixed must have g_x=I.  The remaining
# translation equation is exactly D_L c=u, already excluded above.
check("RELATIVE_SOLDER_BASE_NONDEGENERATE",
      all(sp.Matrix.vstack(*[W_base[(x, r)] for r in range(4)]).det() != 0
          for x in SITES))

print("RESULT_SELECTOR: full-affine covariance uniquely forces lambda=1 in the relative-solder family.")
print("RESULT_COVARIANCE: all 96 completed finite cell densities are invariant under a mixed site-dependent affine gauge.")
print("RESULT_FLAT: b=0 recovers the accepted star density and the flat translation-gauge chart leaves relative solder exactly eta.")
print("RESULT_SHIFT: independent affine shift remains visible.")
print("RESULT_PRINCIPAL_WITNESS: one curved L=2 background has no nonzero covariantly constant node translation.")
print("RESULT_OVERQUOTIENT: a nongauge one-edge matched shift leaves relative solder and the completed action unchanged.")
print("RESULT: AFFINE-RELATIVE-SOLDER-COMPLETION-OVERQUOTIENTS-EDGE-DIAGONAL")
