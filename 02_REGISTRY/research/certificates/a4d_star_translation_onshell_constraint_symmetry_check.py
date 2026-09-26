#!/usr/bin/env python3
"""Exact no-go for the first Cartan-Hodge translation-symmetry class.

Research-only certificate. Exact rational arithmetic.

The accepted star action uses:
  * raw solder legs v_r(x);
  * exact based plaquette curvature R(P)=1/2(P-P^-1);
  * the Lorentz degree-two pairing G2 and internal Hodge star.

On the all-site nondegenerate solder sector, a node vector xi_x has solder
components alpha_x = V_x^-1 xi_x, V_x=[v_A v_B v_C v_D].

The first Cartan-Hodge class is the most general constant-coefficient
one-contraction / one-T-or-F ansatz using only the owned Lorentz metric and
orientation:

  dv_r =
      D_r xi
    + a0 * alpha^s T_{sr}
    + a1 * alpha^s (*_base T)_{sr}

  dL_r = Omega_r L_r

  Omega_r = alpha^s [
      b00 F_{sr}
    + b01 (*_int F)_{sr}
    + b10 (*_base F)_{sr}
    + b11 (*_int *_base F)_{sr}
  ].

Here T_{rs}=D_r v_s-D_s v_r is a solder nonparallelism two-form.  It is NOT
identified with the separately owned affine Cartan torsion.

This class:
  * is linear in xi;
  * is Lorentz covariant;
  * is one-ring / plaquette local;
  * has the exact flat limit dv=d_f xi, dL=0;
  * contains the standard Cartan-looking I/I contraction;
  * contains all base/internal Hodge companions;
  * uses no Euler/Hessian data and no new action term.

The certificate forms exact first variations dS for deterministic rational
L=2 backgrounds.  Seven homogeneous controls give rank 6 in the six correction
coefficients, hence force all corrections to zero.  One hostile curved
translation witness then has nonzero bare forward variation.  Therefore

    rank(A)=6,
    rank([A|-c])=7,

and no coefficient choice gives an off-shell Noether identity in this class.

For an on-shell identity modulo the connection Euler equation with multiplier
in the same classified connection channel space, that multiplier can be
absorbed into the four b-coefficients.  The same rank obstruction therefore
rules out that constraint completion in this class.

This is deliberately scoped: it does not classify higher-curvature,
higher-path, observer-dependent, non-polynomial or Euler-dependent laws.
"""

from itertools import combinations, product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
SITES = list(product(range(2), repeat=4))

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# Lorentz / bivector algebra
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

def wedge_vec(u, v):
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([sp.simplify(Y[a, b]) for a, b in PAIRS])

def tangent_of_bivector(c):
    Y = sp.zeros(4)
    for value, (a, b) in zip(c, PAIRS):
        Y[a, b] = value
        Y[b, a] = -value
    return sp.simplify(Y * ETA)

def internal_star_tangent(X):
    return tangent_of_bivector(STAR * bivector_of_tangent(X))

def complement_orientation(face):
    r, s = face
    comp = [i for i in range(4) if i not in face]
    seq = [r, s] + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

# ---------------------------------------------------------------------------
# L=2 torus and exact action derivative
# ---------------------------------------------------------------------------

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

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

def inverse_derivative(L, dL):
    Li = L.inv()
    return sp.simplify(-Li * dL * Li)

def plaquette_with_derivative(links, dlinks, x, r, s):
    xr = site_add(x, r)
    xs = site_add(x, s)

    keys = [
        (x, r),
        (xr, s),
        (xs, r),
        (x, s),
    ]
    mats = [
        links[keys[0]],
        links[keys[1]],
        links[keys[2]].inv(),
        links[keys[3]].inv(),
    ]
    dmats = [
        dlinks[keys[0]],
        dlinks[keys[1]],
        inverse_derivative(links[keys[2]], dlinks[keys[2]]),
        inverse_derivative(links[keys[3]], dlinks[keys[3]]),
    ]

    P = sp.eye(4)
    for M in mats:
        P = P * M

    dP = sp.zeros(4)
    for i in range(4):
        term = sp.eye(4)
        for j in range(4):
            term = term * (dmats[j] if i == j else mats[j])
        dP += term

    return sp.simplify(P), sp.simplify(dP)

def curvature_derivative(P, dP):
    Pi = P.inv()
    return sp.simplify((dP + Pi * dP * Pi) / 2)

def action_derivative(links, vfield, dlinks, dvfield):
    total = sp.Integer(0)

    for x in SITES:
        for r, s in PAIRS:
            P, dP = plaquette_with_derivative(links, dlinks, x, r, s)

            C = bivector_of_tangent(curvature_extract(P))
            dC = bivector_of_tangent(curvature_derivative(P, dP))

            u, v = [i for i in range(4) if i not in (r, s)]
            B = wedge_vec(vfield[(x, u)], vfield[(x, v)])
            dB = (
                wedge_vec(dvfield[(x, u)], vfield[(x, v)])
                + wedge_vec(vfield[(x, u)], dvfield[(x, v)])
            )

            total += complement_orientation((r, s)) * (
                (dB.T * G2 * STAR * C)[0]
                + (B.T * G2 * STAR * dC)[0]
            )

    return sp.simplify(total)

def flat_solder_vectors():
    return {
        (x, r): I4[:, r]
        for x in SITES
        for r in range(4)
    }

# ---------------------------------------------------------------------------
# First Cartan-Hodge class
# ---------------------------------------------------------------------------

def oriented_pair_value(pairdict, r, s):
    if r == s:
        exemplar = next(iter(pairdict.values()))
        return sp.zeros(*exemplar.shape)
    if r < s:
        return pairdict[(r, s)]
    return -pairdict[(s, r)]

def solder_two_form(links, vfield, x):
    """T_rs = D_r v_s - D_s v_r; not named affine Cartan torsion."""
    out = {}
    for r, s in PAIRS:
        Dr_vs = (
            links[(x, r)] * vfield[(site_add(x, r), s)]
            - vfield[(x, s)]
        )
        Ds_vr = (
            links[(x, s)] * vfield[(site_add(x, s), r)]
            - vfield[(x, r)]
        )
        out[(r, s)] = sp.simplify(Dr_vs - Ds_vr)
    return out

def base_star_vector_two_form(pairdict):
    out = {p: sp.zeros(4, 1) for p in PAIRS}
    for component in range(4):
        c = sp.Matrix([pairdict[p][component] for p in PAIRS])
        cs = STAR * c
        for i, p in enumerate(PAIRS):
            out[p][component] = sp.simplify(cs[i])
    return out

def curvature_two_form(links, x):
    return {
        (r, s): curvature_extract(plaquette(links, x, r, s))
        for r, s in PAIRS
    }

def base_star_matrix_two_form(pairdict):
    out = {p: sp.zeros(4) for p in PAIRS}
    for a in range(4):
        for b in range(4):
            c = sp.Matrix([pairdict[p][a, b] for p in PAIRS])
            cs = STAR * c
            for i, p in enumerate(PAIRS):
                out[p][a, b] = sp.simplify(cs[i])
    return out

def cartan_hodge_variation(links, vfield, xifield, pars):
    """Return dL,dv for pars=(a0,a1,b00,b01,b10,b11)."""
    a0, a1, b00, b01, b10, b11 = pars

    dvfield = {}
    dlinks = {}

    for x in SITES:
        V = sp.Matrix.hstack(*[
            vfield[(x, r)]
            for r in range(4)
        ])
        check("NONDEGENERATE_SOLDER", V.det() != 0)

        alpha = sp.simplify(V.inv() * xifield[x])

        T = solder_two_form(links, vfield, x)
        Tb = base_star_vector_two_form(T)

        F = curvature_two_form(links, x)
        Fb = base_star_matrix_two_form(F)

        for r in range(4):
            Dxi = sp.simplify(
                links[(x, r)] * xifield[site_add(x, r)]
                - xifield[x]
            )

            iT = sp.zeros(4, 1)
            iTb = sp.zeros(4, 1)

            O00 = sp.zeros(4)
            O01 = sp.zeros(4)
            O10 = sp.zeros(4)
            O11 = sp.zeros(4)

            for s in range(4):
                t = oriented_pair_value(T, s, r)
                tb = oriented_pair_value(Tb, s, r)

                f = oriented_pair_value(F, s, r)
                fb = oriented_pair_value(Fb, s, r)

                iT += alpha[s] * t
                iTb += alpha[s] * tb

                O00 += alpha[s] * f
                O01 += alpha[s] * internal_star_tangent(f)
                O10 += alpha[s] * fb
                O11 += alpha[s] * internal_star_tangent(fb)

            dvfield[(x, r)] = sp.simplify(
                Dxi + a0 * iT + a1 * iTb
            )

            Omega = sp.simplify(
                b00 * O00
                + b01 * O01
                + b10 * O10
                + b11 * O11
            )
            dlinks[(x, r)] = sp.simplify(
                Omega * links[(x, r)]
            )

    return dlinks, dvfield

def variation_row(links, vfield, xifield):
    """dS = bare + row.dot(pars)."""
    dL0, dv0 = cartan_hodge_variation(
        links, vfield, xifield, [0] * 6
    )
    bare = action_derivative(
        links, vfield, dL0, dv0
    )

    row = []
    for i in range(6):
        pars = [0] * 6
        pars[i] = 1
        dL, dv = cartan_hodge_variation(
            links, vfield, xifield, pars
        )
        value = action_derivative(
            links, vfield, dL, dv
        )
        row.append(sp.simplify(value - bare))

    return sp.simplify(bare), row

# ---------------------------------------------------------------------------
# Flat-limit control
# ---------------------------------------------------------------------------

flat_links = {
    (x, r): I4
    for x in SITES
    for r in range(4)
}
flat_v = flat_solder_vectors()
flat_xi = {
    x: sp.Matrix([
        x[0] - x[1],
        x[1] - x[2],
        x[2] - x[3],
        x[3] - x[0],
    ])
    for x in SITES
}
flat_bare, flat_row = variation_row(
    flat_links, flat_v, flat_xi
)
check("FLAT_LIMIT_BARE_VARIATION_ZERO", flat_bare == 0)
check("FLAT_LIMIT_CORRECTIONS_VANISH",
      all(value == 0 for value in flat_row))

# ---------------------------------------------------------------------------
# Seven homogeneous rank controls
# ---------------------------------------------------------------------------

def homogeneous_witness(k):
    links = {
        (x, r): I4
        for x in SITES
        for r in range(4)
    }

    placements = [
        SITES[(3 * k + 0) % 16],
        SITES[(5 * k + 1) % 16],
        SITES[(7 * k + 2) % 16],
    ]
    roles = [
        k % 4,
        (k + 1) % 4,
        (k + 2) % 4,
    ]
    for x, r, M in zip(
        placements,
        roles,
        (BOOST, RBC, RCD),
    ):
        links[(x, r)] = M

    links[(
        SITES[(11 * k + 3) % 16],
        (k + 3) % 4,
    )] = BOOST.inv()

    vfield = flat_solder_vectors()
    modifications = [
        (
            SITES[(2 * k + 1) % 16],
            (k + 1) % 4,
            sp.Matrix([
                sp.Rational(1, 5 + k), 0, 0, 0
            ]),
        ),
        (
            SITES[(4 * k + 2) % 16],
            (k + 2) % 4,
            sp.Matrix([
                0,
                sp.Rational((-1) ** k, 3 + k),
                0,
                0,
            ]),
        ),
        (
            SITES[(6 * k + 3) % 16],
            (k + 3) % 4,
            sp.Matrix([
                0, 0, sp.Rational(1, 4 + k), 0
            ]),
        ),
    ]
    for x, r, delta in modifications:
        vfield[(x, r)] = (
            vfield[(x, r)] + delta
        )

    xifield = {
        x: sp.zeros(4, 1)
        for x in SITES
    }
    xifield[SITES[(k + 1) % 16]] = sp.Matrix([
        1, k + 1, -1, 0
    ])
    xifield[SITES[(3 * k + 5) % 16]] = sp.Matrix([
        0, 1, -k - 1, 1
    ])
    xifield[SITES[(9 * k + 7) % 16]] = sp.Matrix([
        sp.Rational(1, 2), 0, 1, -1
    ])

    return links, vfield, xifield

hom_rows = []
hom_bare = []

# k=5 is a zero row and is intentionally omitted.
for k in (0, 1, 2, 3, 4, 6, 7):
    links, vfield, xifield = homogeneous_witness(k)
    bare, row = variation_row(
        links, vfield, xifield
    )
    check("HOMOGENEOUS_BARE_ZERO_" + str(k),
          bare == 0)
    hom_bare.append(bare)
    hom_rows.append(row)

A_hom = sp.Matrix(hom_rows)
check("HOMOGENEOUS_COEFFICIENT_RANK_6",
      A_hom.rank() == 6)

# Thus all six corrections are forced to zero on the homogeneous controls.
null_hom = A_hom.nullspace()
check("HOMOGENEOUS_NULLITY_ZERO",
      len(null_hom) == 0)

# ---------------------------------------------------------------------------
# Hostile inhomogeneous translation witness
# ---------------------------------------------------------------------------

origin = (0, 0, 0, 0)
links = {
    (x, r): I4
    for x in SITES
    for r in range(4)
}
links[(origin, 0)] = BOOST
links[(origin, 1)] = RBC
links[((1, 0, 0, 0), 2)] = RCD

vfield = flat_solder_vectors()
vfield[(origin, 2)] = (
    vfield[(origin, 2)]
    + sp.Matrix([0, sp.Rational(1, 3), 0, 0])
)
vfield[((1, 0, 0, 0), 3)] = (
    vfield[((1, 0, 0, 0), 3)]
    + sp.Matrix([0, 0, sp.Rational(-2, 5), 0])
)

xifield = {
    x: sp.zeros(4, 1)
    for x in SITES
}
xifield[origin] = sp.Matrix([1, 2, -1, 0])
xifield[(1, 1, 0, 0)] = sp.Matrix([0, 1, 1, -1])

hostile_bare, hostile_row = variation_row(
    links, vfield, xifield
)

check("HOSTILE_BARE_FORWARD_VARIATION",
      hostile_bare == sp.Rational(-5, 3))

expected_hostile_row = [
    sp.Rational(-68, 27),
    sp.Rational(64, 45),
    sp.Rational(70, 81),
    sp.Rational(-109, 45),
    sp.Rational(-10, 9),
    sp.Rational(293, 135),
]
check("HOSTILE_CORRECTION_ROW",
      hostile_row == expected_hostile_row)

# The standard I/I Cartan-looking choice a0=b00=1 fails too.
standard_value = sp.simplify(
    hostile_bare
    + hostile_row[0]
    + hostile_row[2]
)
check("STANDARD_CARTAN_I_I_FAILS",
      standard_value == sp.Rational(-269, 81))

# ---------------------------------------------------------------------------
# Terminal exact rank obstruction
# ---------------------------------------------------------------------------

A = sp.Matrix(hom_rows + [hostile_row])
rhs = sp.Matrix(
    [0] * len(hom_rows)
    + [-hostile_bare]
)

check("FULL_COEFFICIENT_RANK_6",
      A.rank() == 6)
check("AUGMENTED_RANK_7",
      A.row_join(rhs).rank() == 7)
check("NO_COEFFICIENT_SOLUTION",
      sp.linsolve((A, rhs)) == sp.EmptySet)

print("HOMOGENEOUS_ROWS")
for row in hom_rows:
    print(row)

print("HOSTILE_BARE", hostile_bare)
print("HOSTILE_ROW", hostile_row)
print("STANDARD_CARTAN_I_I", standard_value)

print("RESULT: no first Cartan-Hodge coefficient choice yields an exact Noether symmetry.")
print("RESULT: the same rank obstruction excludes an on-shell connection-constraint completion whose multiplier lies in the same four curvature channels.")
print("SCOPE: higher-curvature/path, observer-dependent, non-polynomial and Euler-dependent laws are not classified.")
