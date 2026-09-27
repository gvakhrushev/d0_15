#!/usr/bin/env python3
"""Direct flat-link metric Euler identity for the naked star density.

Owner formula: the finite density of
a4d_star_density_lorentz_nonlinear_quotient_check.py (merged #180).
Plaquette, curvature (P-P^{-1})/2, complementary wedge, G2 and star are
copied from that certificate. The Gram lift H(q)=q eta/2 is the #201/#208
map, used only to name the ten symmetric metric components. It is not the
proof that those components vanish.

At every dressed link K=I the based plaquette is exactly I for every
invertible solder. Curvature is the zero matrix, so every metric component
is the zero function of Q. A finite boost on one edge of the same evaluator
has nonzero components, so the zero result is not an empty formula.
"""
from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {pair: index for index, pair in enumerate(PAIRS)}
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]


def orient(face) -> int:
    complement = [i for i in range(4) if i not in face]
    seq = list(face) + complement
    inversions = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIRS])


def bivector(tangent: sp.Matrix) -> sp.Matrix:
    dressed = tangent * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


def gram_lift(q: sp.Matrix) -> sp.Matrix:
    return q * ETA / 2


def site_add(site, role: int):
    moved = list(site)
    moved[role] = (moved[role] + 1) % 2
    return tuple(moved)


SITES = list(product(range(2), repeat=4))


def plaquette(links, site, role_r: int, role_s: int) -> sp.Matrix:
    site_r = site_add(site, role_r)
    site_s = site_add(site, role_s)
    return (
        links[(site, role_r)]
        * links[(site_r, role_s)]
        * links[(site_s, role_r)].inv()
        * links[(site, role_s)].inv()
    )


def curvature(links, site, role_r: int, role_s: int) -> sp.Matrix:
    holonomy = plaquette(links, site, role_r, role_s)
    return (holonomy - holonomy.inv()) / 2


def metric_components(links, legs_of) -> dict:
    """Local ten-component metric partial at every site, owned Gram lift."""
    out = {}
    for site in SITES:
        values = []
        for row, col in SYM:
            direction = sp.zeros(4)
            direction[row, col] = direction[col, row] = 1
            variation = gram_lift(direction)
            total = 0
            legs = legs_of(site)
            for role_r, role_s in PAIRS:
                bend = bivector(curvature(links, site, role_r, role_s))
                u, v = [i for i in range(4) if i not in (role_r, role_s)]
                dw = wedge(variation[u, :].T, legs[v]) + wedge(legs[u], variation[v, :].T)
                total += orient((role_r, role_s)) * (dw.T * G2 * STAR * bend)[0]
            values.append(sp.factor(sp.together(total)))
        out[site] = sp.Matrix(values)
    return out


# ---------------------------------------------------------------------------
# Dressed identity: K=I implies every based plaquette is I.
# ---------------------------------------------------------------------------

corners = [sp.MatrixSymbol(name, 4, 4) for name in ("A", "B", "C", "D")]
corner_a, corner_b, corner_c, corner_d = corners
dressed = (
    corner_a.inv() * corner_b
    * corner_b.inv() * corner_d
    * corner_d.inv() * corner_c
    * corner_c.inv() * corner_a
)
check(
    "DRESSED_IDENTITY_PLAQUETTE",
    sp.simplify(dressed - sp.Identity(4)) == sp.ZeroMatrix(4, 4),
)

identity_links = {(site, role): I4 for site in SITES for role in range(4)}
for site in SITES:
    for face in PAIRS:
        check(
            "RAW_IDENTITY_CURVATURE_" + "".join(map(str, site)) + f"_{face[0]}{face[1]}",
            curvature(identity_links, site, face[0], face[1]) == sp.zeros(4),
        )


def standard_legs(_site):
    return [I4[:, i] for i in range(4)]


flat_metric = metric_components(identity_links, standard_legs)
check(
    "FLAT_STANDARD_SOLDER_ALL_SITES",
    all(value == sp.zeros(10, 1) for value in flat_metric.values()),
)

# Nonstandard rational solder, still raw identity links. Curvature does not
# read the solder, so the metric partial remains zero.
displaced = {
    (0, 0, 0, 0): sp.Matrix([[0, 0, 0, 0], [0, 0, sp.Rational(1, 3), 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    (1, 0, 0, 0): sp.Matrix([[0, sp.Rational(-2, 5), 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
}


def displaced_legs(site):
    delta = displaced.get(site, sp.zeros(4))
    return [I4[:, i] + delta[:, i] for i in range(4)]


check(
    "FLAT_DISPLACED_SOLDER_ALL_SITES",
    all(value == sp.zeros(10, 1) for value in metric_components(identity_links, displaced_legs).values()),
)

# Explicit K=I reconstruction on four rational invertible frames.
frames = {
    (0, 0, 0, 0): sp.Matrix([[1, 0, 0, 0], [0, 1, sp.Rational(1, 5), 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    (1, 0, 0, 0): sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, sp.Rational(1, 7), 1, 0], [0, 0, 0, 1]]),
    (0, 1, 0, 0): sp.Matrix([[1, sp.Rational(1, 4), 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    (1, 1, 0, 0): I4,
}
for frame in frames.values():
    check("FRAME_INVERTIBLE", frame.det() != 0)
# One face inside the frame patch: (0,1) at the origin. The four links are
# the dressed-identity reconstruction L = Theta_x^{-1} Theta_y.
origin = (0, 0, 0, 0)
face_links = {
    (origin, 0): frames[origin].inv() * frames[(1, 0, 0, 0)],
    ((1, 0, 0, 0), 1): frames[(1, 0, 0, 0)].inv() * frames[(1, 1, 0, 0)],
    ((0, 1, 0, 0), 0): frames[(0, 1, 0, 0)].inv() * frames[(1, 1, 0, 0)],
    (origin, 1): frames[origin].inv() * frames[(0, 1, 0, 0)],
}
holonomy = (
    face_links[(origin, 0)]
    * face_links[((1, 0, 0, 0), 1)]
    * face_links[((0, 1, 0, 0), 0)].inv()
    * face_links[(origin, 1)].inv()
)
check("EXPLICIT_K_IDENTITY_HOLONOMY", sp.simplify(holonomy - I4) == sp.zeros(4))

# ---------------------------------------------------------------------------
# Hostile control: one owned finite boost, same partial.
# ---------------------------------------------------------------------------

BOOST = sp.eye(4)
BOOST[0, 0] = sp.Rational(5, 3)
BOOST[0, 1] = sp.Rational(4, 3)
BOOST[1, 0] = sp.Rational(4, 3)
BOOST[1, 1] = sp.Rational(5, 3)
check("BOOST_LORENTZ", BOOST.T * ETA * BOOST == ETA)
boost_links = dict(identity_links)
boost_links[(origin, 0)] = BOOST
boost_curvature = curvature(boost_links, origin, 0, 1)
check("BOOST_CURVATURE_NONZERO", boost_curvature != sp.zeros(4))
boost_metric = metric_components(boost_links, standard_legs)[origin]
expected_boost = {
    (0, 0): 0,
    (0, 1): 0,
    (0, 2): 0,
    (0, 3): 0,
    (1, 1): 0,
    (1, 2): sp.Rational(2, 3),
    (1, 3): sp.Rational(2, 3),
    (2, 2): sp.Rational(-2, 3),
    (2, 3): 0,
    (3, 3): sp.Rational(-2, 3),
}
for index, pair in enumerate(SYM):
    check(f"BOOST_COMPONENT_{pair[0]}{pair[1]}", boost_metric[index] == expected_boost[pair])
check("BOOST_CONTROL_NONZERO", any(value != 0 for value in boost_metric))

# Analytic curve through the identity. The constant term is absent and the
# linear coefficient is nonzero, so the valuation statement is sharp on this
# curve without classifying other germs.
curve = sp.symbols("t")
generator = sp.zeros(4)
generator[0, 1] = generator[1, 0] = 1
link = sp.simplify((I4 - curve * generator / 2).inv() * (I4 + curve * generator / 2))
curve_links = dict(identity_links)
curve_links[(origin, 0)] = link
component = metric_components(curve_links, standard_legs)[origin][SYM.index((1, 2))]
component = sp.together(sp.simplify(component))
check("CURVE_EXACT_COMPONENT", component == -2 * curve / (curve**2 - 4))
check("CURVE_CONSTANT_TERM_ABSENT", sp.series(component, curve, 0, 1).removeO() == 0)
linear = sp.series(component, curve, 0, 2).coeff(curve, 1)
check("CURVE_LINEAR_COEFFICIENT", linear == sp.Rational(1, 2))

print("TERMINAL", "J2-FLAT-LINK-METRIC-EULER-IDENTITY-CERTIFIED")
