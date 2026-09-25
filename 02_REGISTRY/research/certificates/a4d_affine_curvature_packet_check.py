#!/usr/bin/env python3
"""Exact 4D Role-native affine curvature regression certificate.

WRK-A4D-AFFINE-CURVATURE-CERT

One carrier throughout:
  RoleSpace = Q^4, Role order A,B,C,D,
  eta = diag(1,-1,-1,-1),
  affine homogeneous representation on Q ⊕ RoleSpace.

This is a finite research certificate only.  It does not identify continuum
Riemann curvature or Cartan torsion and does not promote claim status.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import os
import sys


# ---------------------------------------------------------------------------
# Exact linear algebra
# ---------------------------------------------------------------------------

def mat(rows):
    return [[Q(x) for x in row] for row in rows]


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def zero(n, m=None):
    m = n if m is None else m
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def add(A, B):
    return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]


def sub(A, B):
    return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]


def mul(A, B):
    return [
        [sum((a * b for a, b in zip(r, c)), Q(0)) for c in zip(*B)]
        for r in A
    ]


def transpose(A):
    return [list(c) for c in zip(*A)]


def mv(A, v):
    return [sum((a * b for a, b in zip(r, v)), Q(0)) for r in A]


def vadd(a, b):
    return [x + y for x, y in zip(a, b)]


def vsub(a, b):
    return [x - y for x, y in zip(a, b)]


def vneg(a):
    return [-x for x in a]


def scale(c, A):
    return [[Q(c) * x for x in row] for row in A]


def inv(A):
    n = len(A)
    R = [row[:] + e for row, e in zip(A, eye(n))]
    for c in range(n):
        p = next(i for i in range(c, n) if R[i][c] != 0)
        R[c], R[p] = R[p], R[c]
        pv = R[c][c]
        R[c] = [x / pv for x in R[c]]
        for i in range(n):
            if i != c and R[i][c] != 0:
                f = R[i][c]
                R[i] = [x - f * y for x, y in zip(R[i], R[c])]
    return [row[n:] for row in R]


def chain(*As):
    out = eye(len(As[0]))
    for A in As:
        out = mul(out, A)
    return out


def trace(A):
    return sum((A[i][i] for i in range(len(A))), Q(0))


def rank(A):
    M = [row[:] for row in A]
    if not M:
        return 0
    nrows, ncols = len(M), len(M[0])
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, nrows) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nrows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == nrows:
            break
    return r


def in_image(M, t):
    return rank(M) == rank([row[:] + [t[i]] for i, row in enumerate(M)])


# ---------------------------------------------------------------------------
# Fixed four-Role Lorentz carrier
# ---------------------------------------------------------------------------

ETA = mat([
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1],
])

I4 = eye(4)
Z4 = [Q(0)] * 4


def is_lorentz(L):
    return mul(mul(transpose(L), ETA), L) == ETA


# Rational boost in the A-B plane: cosh=5/3, sinh=4/3.
BOOST_AB = mat([
    [Q(5, 3), Q(4, 3), 0, 0],
    [Q(4, 3), Q(5, 3), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

# Rational spatial rotations.
ROT_BC = mat([
    [1, 0, 0, 0],
    [0, Q(3, 5), Q(-4, 5), 0],
    [0, Q(4, 5), Q(3, 5), 0],
    [0, 0, 0, 1],
])

ROT_CD = mat([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, Q(3, 5), Q(-4, 5)],
    [0, 0, Q(4, 5), Q(3, 5)],
])

for _L in (BOOST_AB, ROT_BC, ROT_CD):
    assert is_lorentz(_L)


# ---------------------------------------------------------------------------
# Affine semidirect representation on Q ⊕ RoleSpace
# ---------------------------------------------------------------------------

def affine(L, b):
    return [[Q(1)] + [Q(0)] * 4] + [[Q(b[i])] + L[i][:] for i in range(4)]


def T(b):
    return affine(I4, b)


def rho(L):
    return affine(L, Z4)


def lin_of(H):
    return [row[1:] for row in H[1:]]


def tr_of(H):
    return [H[i + 1][0] for i in range(4)]


def pair_mul(b, L, c, M):
    return vadd(b, mv(L, c)), mul(L, M)


def pair_inv(b, L):
    Li = inv(L)
    return vneg(mv(Li, b)), Li


def affine_square_formula(u, A, v, B, w, C, z, D, wrong=False):
    Ci = inv(C)
    Lam = chain(A, B, Ci, inv(D))
    if wrong:
        # Deliberately wrong: drops the A B transport on w and Lambda on z.
        Theta = vsub(vadd(u, mv(A, v)), vadd(mv(Ci, w), mv(D, z)))
    else:
        ABCi = chain(A, B, Ci)
        Theta = vsub(vadd(u, mv(A, v)), vadd(mv(ABCi, w), mv(Lam, z)))
    return Lam, Theta


def conjug(A, B):
    return chain(A, B, inv(A))


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_semidirect():
    b = [Q(1), Q(-2), Q(3), Q(0)]
    c = [Q(0), Q(1), Q(-1), Q(2)]
    bc, LM = pair_mul(b, BOOST_AB, c, ROT_BC)
    assert affine(LM, bc) == mul(affine(BOOST_AB, b), affine(ROT_BC, c))
    ib, iL = pair_inv(b, BOOST_AB)
    assert affine(iL, ib) == inv(affine(BOOST_AB, b))
    assert pair_mul(b, BOOST_AB, ib, iL) == (Z4, I4)
    print("PASS_SEMIDIRECT exact 4D Role affine multiplication/inverse")


def square_witness(wrong=False):
    A, B, C, D = BOOST_AB, ROT_BC, ROT_CD, I4
    u = [Q(1), Q(2), Q(-1), Q(0)]
    v = [Q(0), Q(1), Q(3), Q(-2)]
    w = [Q(2), Q(-1), Q(0), Q(1)]
    z = [Q(-1), Q(0), Q(2), Q(1)]
    Lam, Theta = affine_square_formula(u, A, v, B, w, C, z, D, wrong=wrong)
    actual = chain(affine(A, u), affine(B, v), inv(affine(C, w)), inv(affine(D, z)))
    return actual, affine(Lam, Theta), Lam, Theta


def check_affine_square():
    actual, expected, Lam, _ = square_witness()
    assert actual == expected
    assert is_lorentz(Lam)
    print("PASS_AFFINE_SQUARE P=T_Theta rho(Lambda) on one 4D Role carrier")


def check_noncommuting_linear():
    Lam = chain(BOOST_AB, ROT_BC, inv(BOOST_AB), inv(ROT_BC))
    assert is_lorentz(Lam)
    assert Lam != I4
    print("PASS_NONCOMMUTING_LINEAR exact Lorentz commutator Lambda != I")


def shift2(x, r):
    return tuple((a + (1 if i == r else 0)) % 3 for i, a in enumerate(x))


def kappa(x, r):
    if x == (0, 0) and r == 0:
        return [Q(1), Q(-1), Q(2), Q(0)]
    return Z4[:]


def frame_E(x):
    return BOOST_AB if x == (0, 0) else I4


def mixed_link(x, r):
    xp = shift2(x, r)
    return chain(rho(frame_E(x)), T(kappa(x, r)), inv(rho(frame_E(xp))))


def plaquette2(g, x, r, s):
    return chain(g(x, r), g(shift2(x, r), s), inv(g(shift2(x, s), r)), inv(g(x, s)))


def omega(x):
    kr = kappa(x, 0)
    ks = kappa(x, 1)
    trks = kappa(shift2(x, 0), 1)
    tskr = kappa(shift2(x, 1), 0)
    return vsub(vadd(kr, trks), vadd(tskr, ks))


def check_mixed_and_pure_frame():
    for x in product(range(3), repeat=2):
        P = plaquette2(mixed_link, x, 0, 1)
        expected = chain(rho(frame_E(x)), T(omega(x)), inv(rho(frame_E(x))))
        assert P == expected

    def pure_frame_link(x, r):
        return chain(rho(frame_E(x)), inv(rho(frame_E(shift2(x, r)))))

    for x in product(range(3), repeat=2):
        assert plaquette2(pure_frame_link, x, 0, 1) == eye(5)

    print("PASS_SHARED_F_MIXED exact P=F T_Omega F^-1 and kappa=0 even flatness")


def check_pure_translation():
    def b(x, r):
        if x == (0, 0) and r == 0:
            return [Q(1), Q(2), Q(0), Q(-1)]
        return Z4[:]

    def glink(x, r):
        return T(b(x, r))

    for x in product(range(3), repeat=2):
        P = plaquette2(glink, x, 0, 1)
        d1 = vsub(vadd(b(x, 0), b(shift2(x, 0), 1)),
                  vadd(b(shift2(x, 1), 0), b(x, 1)))
        assert lin_of(P) == I4
        assert tr_of(P) == d1
    print("PASS_PURE_TRANSLATION L=I => Lambda=I, Theta=d1 b")


def check_frame_image_bridge():
    for x in product(range(3), repeat=2):
        for r in range(2):
            xp = shift2(x, r)
            E = frame_E(x)
            L = mul(E, inv(frame_E(xp)))
            b = mv(E, kappa(x, r))
            assert mixed_link(x, r) == affine(L, b)

    for x in product(range(3), repeat=2):
        P = plaquette2(mixed_link, x, 0, 1)
        assert lin_of(P) == I4
    print("PASS_FRAME_IMAGE_BRIDGE F=rho(E) gives affine link and Lambda=I")


# Three-dimensional base archive, still one four-Role internal carrier.
def shift3(x, r):
    return tuple((a + (1 if i == r else 0)) % 3 for i, a in enumerate(x))


BASES = [
    affine(BOOST_AB, [Q(1), Q(0), Q(0), Q(0)]),
    affine(ROT_BC, [Q(0), Q(1), Q(0), Q(0)]),
    affine(ROT_CD, [Q(0), Q(0), Q(1), Q(0)]),
]


def cube_link(x, r):
    site_t = [
        Q(x[(r + 1) % 3]),
        Q(x[(r + 2) % 3] - 1),
        Q((x[0] + x[1] + x[2] + r) % 2),
        Q(r - 1),
    ]
    return mul(T(site_t), BASES[r])


def plaquette3(x, r, s):
    return chain(
        cube_link(x, r),
        cube_link(shift3(x, r), s),
        inv(cube_link(shift3(x, s), r)),
        inv(cube_link(x, s)),
    )


def ordinary_dtheta(x):
    terms = [
        tr_of(plaquette3(shift3(x, 0), 1, 2)),
        tr_of(plaquette3(x, 1, 2)),
        tr_of(plaquette3(shift3(x, 1), 0, 2)),
        tr_of(plaquette3(x, 0, 2)),
        tr_of(plaquette3(shift3(x, 2), 0, 1)),
        tr_of(plaquette3(x, 0, 1)),
    ]
    signs = [1, -1, -1, 1, 1, -1]
    return [
        sum((Q(s) * v[i] for s, v in zip(signs, terms)), Q(0))
        for i in range(4)
    ]


def check_ordered_cube():
    for x in product(range(3), repeat=3):
        lhs = chain(
            plaquette3(x, 0, 1),
            conjug(cube_link(x, 1), plaquette3(shift3(x, 1), 0, 2)),
            plaquette3(x, 1, 2),
        )
        rhs = chain(
            conjug(cube_link(x, 0), plaquette3(shift3(x, 0), 1, 2)),
            plaquette3(x, 0, 2),
            conjug(cube_link(x, 2), plaquette3(shift3(x, 2), 0, 1)),
        )
        assert lhs == rhs

    dt = ordinary_dtheta((0, 0, 0))
    assert any(dt)
    print(f"PASS_ORDERED_CUBE exact nonabelian word identity; ordinary dTheta={dt} != 0")


def check_trace_blindness():
    P = chain(BOOST_AB, ROT_BC, inv(BOOST_AB), inv(ROT_BC))
    t = [Q(2), Q(-1), Q(3), Q(4)]
    H = affine(P, t)
    assert trace(H) == Q(1) + trace(P)
    assert trace(H) == trace(affine(P, Z4))
    R = sub(T(t), eye(5))
    assert mul(R, R) == zero(5)
    print("PASS_TRACE_BLINDNESS affine translation block is invisible to ordinary trace")


def check_gauge_origin_shift():
    P = chain(BOOST_AB, ROT_BC, inv(BOOST_AB), inv(ROT_BC))
    t = [Q(1), Q(0), Q(-2), Q(3)]
    E = ROT_CD
    c = [Q(2), Q(-1), Q(1), Q(4)]

    Pp = chain(E, P, inv(E))
    tp = vadd(mv(E, t), mv(sub(I4, Pp), c))

    H = affine(P, t)
    g = affine(E, c)
    assert chain(g, H, inv(g)) == affine(Pp, tp)
    print("PASS_GAUGE_ORIGIN_SHIFT t'=Et+(I-P')c exactly")


def check_fixed_P_quotient_and_singular_residual():
    P = BOOST_AB
    IP = sub(I4, P)
    assert P != I4 and is_lorentz(P)
    assert rank(IP) == 2

    residual = [Q(0), Q(0), Q(1), Q(0)]  # fixed C direction
    assert not in_image(IP, residual)

    removable = mv(IP, [Q(2), Q(-3), Q(5), Q(7)])
    assert in_image(IP, removable)

    # The equivalence is exact by construction of the orbit t -> t+(I-P)c.
    assert in_image(IP, Z4)
    print("PASS_FIXED_P_QUOTIENT [t] in coker(I-P); singular Lorentz P has residual class")


def check_invertible_IP():
    # Boost in A-B and nontrivial spatial rotation in C-D: no unit eigenvalue.
    P = mul(BOOST_AB, ROT_CD)
    assert is_lorentz(P)
    IP = sub(I4, P)
    assert rank(IP) == 4

    for t in (
        [Q(1), Q(0), Q(0), Q(0)],
        [Q(0), Q(1), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
        [Q(1, 2), Q(-3, 5), Q(7, 3), Q(2)],
    ):
        c = vneg(mv(inv(IP), t))
        assert vadd(t, mv(IP, c)) == Z4
    print("PASS_INVERTIBLE_IP all translations removable for exact 4D loxodromic witness")


# ---------------------------------------------------------------------------
# Reachable negative mutations
# ---------------------------------------------------------------------------

def fail(code, msg):
    print(f"FAIL_{code}: {msg}")
    return 1


def run_mutation(name):
    if name == "wrong_theta_corner":
        actual, bad, _, _ = square_witness(wrong=True)
        if actual == bad:
            return fail("WRONG_THETA_CORNER_DID_NOT_BREAK", "bad formula accidentally matched")
        return fail("WRONG_THETA_CORNER", "dropped transported corner factors")

    if name == "ordinary_dtheta_bianchi":
        dt = ordinary_dtheta((0, 0, 0))
        if not any(dt):
            return fail("ORDINARY_DTHETA_BIANCHI_DID_NOT_BREAK", "hostile witness vanished")
        return fail("ORDINARY_DTHETA_BIANCHI", f"ordered cube holds but dTheta={dt} != 0")

    if name == "false_binary_removable":
        P = BOOST_AB
        IP = sub(I4, P)
        t = [Q(0), Q(0), Q(1), Q(0)]
        if P == I4 or in_image(IP, t):
            return fail("FALSE_BINARY_REMOVABLE_DID_NOT_BREAK", "residual witness missing")
        return fail("FALSE_BINARY_REMOVABLE", "P!=I but t is not in im(I-P)")

    return fail("UNKNOWN_MUTATION", name)


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    mutation = os.environ.get("MUTATE") or os.environ.get("AFFINE_CURVATURE_MUTATE")
    for arg in argv[1:]:
        if arg.startswith("--mutate="):
            mutation = arg.split("=", 1)[1]

    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: RoleSpace=Q^4 with eta=diag(1,-1,-1,-1); "
        "all affine, plaquette, cube, and conjugacy witnesses use this same internal carrier."
    )

    if mutation:
        return run_mutation(mutation)

    check_semidirect()
    check_affine_square()
    check_pure_translation()
    check_noncommuting_linear()
    check_mixed_and_pure_frame()
    check_frame_image_bridge()
    check_ordered_cube()
    check_trace_blindness()
    check_gauge_origin_shift()
    check_fixed_P_quotient_and_singular_residual()
    check_invertible_IP()

    print("TERMINAL A4D-AFFINE-CURVATURE-CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
