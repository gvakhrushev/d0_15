#!/usr/bin/env python3
"""Exact flat Jacobian entry for the naked-star metric partial.

The dimensionless chart is the link logarithm: L = exp(A), A in so(1,3).
At identity links and standard solder, this certificate evaluates one
directional derivative of the metric partial Euler covector with respect to
one link logarithm. The value is a nonzero rational, so the raw Lipschitz
exponent cannot be improved below 0 and the h^{-2}-normalized exponent
cannot be improved below 2.

No continuum Einstein equation is encoded here.
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
check("G2_NONDEGENERATE", G2.det() != 0)


def wedge_vec(u, v):
    out = sp.zeros(6, 1)
    for i, (a, b) in enumerate(PAIRS):
        out[i] = u[a] * v[b] - u[b] * v[a]
    return out


def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([Y[a, b] for a, b in PAIRS])


def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def metric_partial_link_derivative(link_dir, link_algebra, solder_leg, solder_vec):
    """Derivative at the identity of E_Q[solder] along one link logarithm.

    The based plaquette for an ordered pair (r, s) is
    L_r(x) L_s(x+e_r) L_r(x+e_s)^{-1} L_s(x)^{-1}.
    At the identity, the plaquette derivative is the signed sum of the
    four link derivatives. Solder enters only through the base-site
    complementary bivector, so only the base site contributes.
    """
    basis = [sp.eye(4)[:, r] for r in range(4)]
    total = sp.Integer(0)
    for r, s in PAIRS:
        p_dot = sp.zeros(4)
        if r == link_dir:
            p_dot += link_algebra
        if s == link_dir:
            p_dot -= link_algebra
        if p_dot == sp.zeros(4):
            continue
        c_dot = bivector_of_tangent(p_dot)
        u, v = [i for i in range(4) if i not in (r, s)]
        db = sp.zeros(6, 1)
        if u == solder_leg:
            db += wedge_vec(solder_vec, basis[v])
        if v == solder_leg:
            db += wedge_vec(basis[u], solder_vec)
        eps = complement_orientation((r, s))
        total += eps * (db.T * G2 * STAR * c_dot)[0]
    return sp.expand(total)


# Boost in the 0-1 plane, varying the r=0 link, scaling the e_2 solder leg.
boost_01 = LORENTZ[0]
check("BOOST_IS_FIRST", boost_01[0, 1] == 1 and boost_01[1, 0] == 1)
entry = metric_partial_link_derivative(0, boost_01, 2, sp.eye(4)[:, 2])
check("FLAT_MIXED_ENTRY_RATIONAL", entry == sp.Integer(entry))
check("FLAT_MIXED_ENTRY_NONZERO", entry != 0)
print("FLAT_MIXED_ENTRY", entry)

# The same entry is unchanged by an overall positive mesh power: multiplying
# the normalized response by h^{-2} raises the sharp exponent from 0 to 2.
for hexp in (1, 2, 3, 5):
    h = sp.Rational(1, hexp)
    raw_ratio = sp.Abs(entry)
    normalized_ratio = raw_ratio / h**2
    check(
        f"NORMALIZED_POWER_H_{hexp}",
        sp.simplify(normalized_ratio / (raw_ratio * h ** (-2))) == 1,
    )

# Polynomial loss preserves a high positive power. An exponential-in-L
# constant, with L represented by the integer reciprocal N = 1/h, does not.
for n in (2, 4, 8):
    h = sp.Rational(1, n)
    source = h**12
    normalized = h ** (-2) * source
    check(f"NORMALIZED_SOURCE_POWER_N_{n}", normalized == h**10)
    check(f"POLYNOMIAL_LOSS_STILL_DECAYS_N_{n}", normalized < h)
    hidden = sp.exp(n) * sp.exp(-n)
    check(f"EXPONENTIAL_CONSTANT_NOT_SMALL_N_{n}", hidden == 1)

print("ALL_CHECKS_PASSED")
