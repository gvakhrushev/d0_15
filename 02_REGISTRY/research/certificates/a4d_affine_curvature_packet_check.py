#!/usr/bin/env python3
"""Exact research regression certificate for WRK-A4D-AFFINE-CURVATURE-CERT.

Turns the finite affine/mixed plaquette packet of
MEMO_A4D_MIXED_LETTER_PLAQUETTE_CURVATURE.md (and the owned conjugacy quotient
from MEMO_A4D_AFFINE_CONJUGACY_ROLE_BIVECTOR_INSERTION_AUDIT.md) into a
deterministic exact-arithmetic checker.

No Lean. No claim-release promotion. No continuum Riemann/Cartan torsion.
No new 2-cocycle.

Default run: print STRUCTURE_FIXED_BEFORE_NUMBER: then PASS_* lines, exit 0.
Negative controls: --mutate=<name> (or env MUTATE=<name>) exits nonzero with
FAIL_*.

Mutations:
  wrong_theta_corner          -- corrupt corner/shift in affine Theta
  ordinary_dtheta_bianchi     -- replace ordered cube by illegal dTheta=0
  false_binary_removable      -- claim P!=I => every t removable
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import os
import sys


def mat(rows):
    return [[Q(x) for x in r] for r in rows]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n):
    return mat([[0] * n for _ in range(n)])


def add(A, B):
    return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]


def sub(A, B):
    return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]


def neg(A):
    return [[-v for v in r] for r in A]


def mul(A, B):
    return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]


def scale(c, A):
    return [[c * v for v in r] for r in A]


def inv(A):
    n = len(A)
    R = [r[:] + s for r, s in zip(A, eye(n))]
    for j in range(n):
        p = next(i for i in range(j, n) if R[i][j] != 0)
        R[j], R[p] = R[p], R[j]
        v = R[j][j]
        R[j] = [x / v for x in R[j]]
        for i in range(n):
            if i != j and R[i][j] != 0:
                f = R[i][j]
                R[i] = [a - f * b for a, b in zip(R[i], R[j])]
    return [r[n:] for r in R]


def chain(*xs):
    out = eye(len(xs[0]))
    for A in xs:
        out = mul(out, A)
    return out


def mv(A, v):
    return [sum(a * b for a, b in zip(r, v)) for r in A]


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def vneg(u):
    return [-a for a in u]


def veq(u, v):
    return list(u) == list(v)


def meq(A, B):
    return A == B


def transpose(A):
    return [list(c) for c in zip(*A)]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def mat_rank(A):
    """Exact rank over Q via Gaussian elimination."""
    M = [r[:] for r in A]
    nrows = len(M)
    ncols = len(M[0]) if nrows else 0
    rank = 0
    for col in range(ncols):
        piv = None
        for r in range(rank, nrows):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for r in range(nrows):
            if r != rank and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def in_image(M, t):
    """Exact: t in im(M) over Q (solve M c = t)."""
    n = len(M)
    # augmented [M | t]
    R = [M[i][:] + [t[i]] for i in range(n)]
    mcols = n
    row = 0
    pivots = []
    for col in range(mcols):
        piv = None
        for i in range(row, n):
            if R[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        R[row], R[piv] = R[piv], R[row]
        pv = R[row][col]
        R[row] = [x / pv for x in R[row]]
        for i in range(n):
            if i != row and R[i][col] != 0:
                f = R[i][col]
                R[i] = [a - f * b for a, b in zip(R[i], R[row])]
        pivots.append(col)
        row += 1
        if row == n:
            break
    for i in range(row, n):
        if R[i][mcols] != 0:
            return False
    return True


# --- homogeneous affine representation on E = R ⊕ R^2 ---------------------------

def affine(L, b):
    """T_b rho(L) = [[1,0],[b,L]] with b length-2, L 2x2."""
    return [
        [Q(1), Q(0), Q(0)],
        [Q(b[0]), L[0][0], L[0][1]],
        [Q(b[1]), L[1][0], L[1][1]],
    ]


def T_of(b):
    return affine(eye(2), b)


def rho(L):
    return affine(L, (Q(0), Q(0)))


def lin_of(P):
    return [row[1:] for row in P[1:]]


def tr_of(P):
    return [P[1][0], P[2][0]]


def pair_mul(b, L, c, M):
    """Semidirect: (b,L)(c,M) = (b + L c, L M)."""
    return (vadd(b, mv(L, c)), mul(L, M))


def pair_inv(b, L):
    """(b,L)^{-1} = (-L^{-1} b, L^{-1})."""
    Li = inv(L)
    return (vneg(mv(Li, b)), Li)


def affine_lambda_theta(u, A, v, B, w, C, z, D, mutate=None):
    """Exact ordered square formula.

    Lambda = A B C^{-1} D^{-1}
    Theta  = u + A v - A B C^{-1} w - Lambda z
    """
    if mutate == "wrong_theta_corner":
        # Illegal corner/shift: bare C^{-1} w and D z instead of
        # ABC^{-1} w and Lambda z.
        Ci = inv(C)
        Lam = mul(mul(A, B), mul(Ci, inv(D)))
        theta = vsub(vadd(u, mv(A, v)), vadd(mv(Ci, w), mv(D, z)))
        return Lam, theta
    ABC_invC = mul(mul(A, B), inv(C))
    Lam = mul(ABC_invC, inv(D))
    theta = vsub(vadd(u, mv(A, v)), vadd(mv(ABC_invC, w), mv(Lam, z)))
    return Lam, theta


def parse_mutate(argv):
    env = os.environ.get("MUTATE") or os.environ.get("AFFINE_CURVATURE_MUTATE")
    named = None
    for a in argv[1:]:
        if a.startswith("--mutate="):
            named = a.split("=", 1)[1].strip()
        elif a == "--mutate":
            named = "all"
    return named or env


def fail(code, msg):
    print(f"FAIL_{code}: {msg}")
    raise SystemExit(1)


# --- positive checks ------------------------------------------------------------

def check_semidirect_mul_inv():
    b = [Q(1), Q(-2)]
    L = mat([[Q(2), Q(1)], [Q(0), Q(3)]])
    c = [Q(4), Q(5)]
    M = mat([[Q(1), Q(-1)], [Q(2), Q(1)]])
    bc, LM = pair_mul(b, L, c, M)
    assert veq(bc, vadd(b, mv(L, c)))
    assert meq(LM, mul(L, M))
    # operator-level: affine(L,b) affine(M,c) = affine(LM, b+Lc)
    assert meq(mul(affine(L, b), affine(M, c)), affine(LM, bc))
    ib, iL = pair_inv(b, L)
    assert veq(ib, vneg(mv(inv(L), b)))
    assert meq(iL, inv(L))
    one_b, one_L = pair_mul(b, L, ib, iL)
    assert veq(one_b, [Q(0), Q(0)]) and meq(one_L, eye(2))
    one_b2, one_L2 = pair_mul(ib, iL, b, L)
    assert veq(one_b2, [Q(0), Q(0)]) and meq(one_L2, eye(2))
    assert meq(mul(affine(L, b), affine(iL, ib)), eye(3))
    print("PASS_SEMIDIRECT_MUL_INV exact (b,L)(c,M)=(b+Lc,LM) and inverse (-L^{-1}b,L^{-1})")


def check_affine_square(mutate=None):
    # Unequal rational corners so a wrong corner/shift in Theta is visible.
    A = mat([[1, 1], [0, 1]])
    B = mat([[1, 0], [1, 1]])
    C = mat([[2, 1], [0, 1]])
    D = mat([[1, 0], [2, 1]])
    u = [Q(1), Q(2)]
    v = [Q(3), Q(-1)]
    w = [Q(0), Q(4)]
    z = [Q(5), Q(1)]
    Lam, Theta = affine_lambda_theta(u, A, v, B, w, C, z, D, mutate=mutate)
    product = chain(affine(A, u), affine(B, v), inv(affine(C, w)), inv(affine(D, z)))
    expected = affine(Lam, Theta)
    if mutate == "wrong_theta_corner":
        if meq(product, expected):
            fail(
                "WRONG_THETA_CORNER_DID_NOT_BREAK",
                "corrupted Theta unexpectedly matched the ordered product",
            )
        fail(
            "WRONG_THETA_CORNER",
            "Theta used bare C^{-1}w / D z instead of ABC^{-1}w / Lambda z; "
            f"ordered product disagrees (Lambda={Lam}, bad_Theta={Theta}, "
            f"true={tr_of(product)})",
        )
    assert meq(product, expected), (product, expected)
    assert meq(product, mul(T_of(Theta), rho(Lam)))
    # Constant-link noncommuting witness kept as a second square check.
    A2 = mat([[1, 1], [0, 1]])
    B2 = mat([[1, 0], [1, 1]])
    u2, v2 = [Q(1), Q(0)], [Q(0), Q(1)]
    Lam2, Th2 = affine_lambda_theta(u2, A2, v2, B2, u2, A2, v2, B2)
    P2 = chain(affine(A2, u2), affine(B2, v2), inv(affine(A2, u2)), inv(affine(B2, v2)))
    assert meq(P2, affine(Lam2, Th2))
    print(
        "PASS_AFFINE_SQUARE P=T_Theta rho(Lambda) with "
        "Lambda=ABC^{-1}D^{-1}, Theta=u+Av-ABC^{-1}w-Lambda z"
    )


def check_pure_translation_reduction():
    # L=I everywhere, bump b from memo §8.6
    sites = list(product(range(3), repeat=2))

    def shift(x, r):
        return tuple((v + (i == r)) % 3 for i, v in enumerate(x))

    def b(x, r):
        return [Q(1), Q(0)] if (x == (0, 0) and r == 0) else [Q(0), Q(0)]

    for x in sites:
        A = eye(2)
        B = eye(2)
        C = eye(2)
        D = eye(2)
        u = b(x, 0)
        v = b(shift(x, 0), 1)
        w = b(shift(x, 1), 0)
        z = b(x, 1)
        Lam, Theta = affine_lambda_theta(u, A, v, B, w, C, z, D)
        assert meq(Lam, eye(2))
        d1 = vsub(vadd(u, v), vadd(w, z))
        assert veq(Theta, d1)
        P = chain(T_of(u), T_of(v), inv(T_of(w)), inv(T_of(z)))
        assert meq(P, T_of(Theta))
    print("PASS_PURE_TRANSLATION_REDUCTION L=I => Lambda=I, Theta=d1 b on (Z/3)^2")


def check_noncommuting_linear_witness():
    A = mat([[1, 1], [0, 1]])
    B = mat([[1, 0], [1, 1]])
    Lam = chain(A, B, inv(A), inv(B))
    assert Lam == mat([[3, -1], [1, 0]])
    assert not meq(Lam, eye(2))
    # with constant translations
    u, v = [Q(1), Q(0)], [Q(0), Q(1)]
    Lam2, Theta = affine_lambda_theta(u, A, v, B, u, A, v, B)
    assert meq(Lam2, Lam)
    assert veq(Theta, [Q(1), Q(0)])
    P = chain(affine(A, u), affine(B, v), inv(affine(A, u)), inv(affine(B, v)))
    assert meq(P, affine(Lam, Theta))
    print("PASS_NONCOMMUTING_LINEAR_WITNESS Lambda=[[3,-1],[1,0]] != I with Theta=(1,0)")


def check_shared_F_mixed(mutate=None):
    sites = list(product(range(3), repeat=2))
    I3 = eye(3)
    D = mat([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

    def F(x):
        return D if x == (0, 0) else I3

    def shift(x, r):
        return tuple((v + (i == r)) % 3 for i, v in enumerate(x))

    def kappa(x, r):
        # one-site bump memo §8.4
        return (Q(1), Q(0)) if (x == (0, 0) and r == 0) else (Q(0), Q(0))

    def omega(x):
        # Omega = kappa_r + tau_r kappa_s - tau_s kappa_r - kappa_s
        kr = kappa(x, 0)
        ks = kappa(x, 1)
        tr_ks = kappa(shift(x, 0), 1)
        ts_kr = kappa(shift(x, 1), 0)
        return (
            kr[0] + tr_ks[0] - ts_kr[0] - ks[0],
            kr[1] + tr_ks[1] - ts_kr[1] - ks[1],
        )

    def gmix(x, r):
        return chain(F(x), T_of(kappa(x, r)), inv(F(shift(x, r))))

    def plaquette(g, x, r, s):
        return chain(g(x, r), g(shift(x, r), s), inv(g(shift(x, s), r)), inv(g(x, s)))

    for x in sites:
        P = plaquette(gmix, x, 0, 1)
        Om = omega(x)
        expected = chain(F(x), T_of(Om), inv(F(x)))
        assert meq(P, expected), (x, P, expected)
    print("PASS_SHARED_F_MIXED P=F T_Omega F^{-1} with Omega=kappa_r+tau_r kappa_s-tau_s kappa_r-kappa_s")


def check_pure_shared_F_flat():
    sites = list(product(range(3), repeat=2))
    I3 = eye(3)
    D = mat([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

    def F(x):
        return D if x == (0, 0) else I3

    def shift(x, r):
        return tuple((v + (i == r)) % 3 for i, v in enumerate(x))

    def gpure(x, r):
        return mul(F(x), inv(F(shift(x, r))))

    def plaquette(g, x, r, s):
        return chain(g(x, r), g(shift(x, r), s), inv(g(shift(x, s), r)), inv(g(x, s)))

    for x in sites:
        assert meq(plaquette(gpure, x, 0, 1), I3)
    print("PASS_PURE_SHARED_F_FLAT kappa=0 => all plaquettes = I for single-valued F")


def check_frame_image_bridge():
    sites = list(product(range(3), repeat=2))
    I3 = eye(3)
    D = mat([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

    def F(x):
        return D if x == (0, 0) else I3

    def shift(x, r):
        return tuple((v + (i == r)) % 3 for i, v in enumerate(x))

    def kappa(x, r):
        return (Q(1), Q(0)) if (x == (0, 0) and r == 0) else (Q(0), Q(0))

    def Ef(x):
        return [row[1:] for row in F(x)[1:]]

    def gmix(x, r):
        return chain(F(x), T_of(kappa(x, r)), inv(F(shift(x, r))))

    def gbridge(x, r):
        E = Ef(x)
        L = mul(E, inv(Ef(shift(x, r))))
        b = mv(E, kappa(x, r))
        return affine(L, b)

    for x in sites:
        for r in range(2):
            assert meq(gbridge(x, r), gmix(x, r))
        # plaquette Lambda = I under the bridge
        A = mul(Ef(x), inv(Ef(shift(x, 0))))
        B = mul(Ef(shift(x, 0)), inv(Ef(shift(shift(x, 0), 1))))
        C = mul(Ef(shift(x, 1)), inv(Ef(shift(shift(x, 1), 0))))
        Dlin = mul(Ef(x), inv(Ef(shift(x, 1))))
        Lam, _ = affine_lambda_theta(
            mv(Ef(x), kappa(x, 0)),
            A,
            mv(Ef(shift(x, 0)), kappa(shift(x, 0), 1)),
            B,
            mv(Ef(shift(x, 1)), kappa(shift(x, 1), 0)),
            C,
            mv(Ef(x), kappa(x, 1)),
            Dlin,
        )
        assert meq(Lam, eye(2)), (x, Lam)
    print("PASS_FRAME_IMAGE_BRIDGE F=rho(E) => letters coincide and Lambda=I")


def check_ordered_cube(mutate=None):
    G1 = affine(mat([[1, 1], [0, 1]]), (Q(1), Q(0)))
    G2 = affine(mat([[1, 0], [1, 1]]), (Q(0), Q(1)))
    G3 = affine(mat([[2, 0], [0, 1]]), (Q(1), Q(-1)))
    # Memo §8 nonabelian cube uses spatially varying translations on (Z/3)^3
    bases = [
        affine(mat([[1, 1], [0, 1]]), (0, 0)),  # overwritten below with memo G's
        affine(mat([[1, 0], [1, 1]]), (0, 0)),
        affine(mat([[2, 0], [0, 1]]), (0, 0)),
    ]
    # Use the memo's exact G1,G2,G3 as the linear+translation bases
    bases = [G1, G2, G3]

    def shift(x, r):
        return tuple((v + (i == r)) % 3 for i, v in enumerate(x))

    def g3(x, r):
        base = bases[r]
        return mul(T_of((Q(x[(r + 1) % 3]), Q(x[(r + 2) % 3] - 1))), base)

    def plaquette(g, x, r, s):
        return chain(g(x, r), g(shift(x, r), s), inv(g(shift(x, s), r)), inv(g(x, s)))

    def conjug(A, B):
        return chain(A, B, inv(A))

    # Verify ordered cube on all 27 sites
    for x in product(range(3), repeat=3):
        prs = plaquette(g3, x, 0, 1)
        prt = plaquette(g3, x, 0, 2)
        pst = plaquette(g3, x, 1, 2)
        lhs = chain(prs, conjug(g3(x, 1), plaquette(g3, shift(x, 1), 0, 2)), pst)
        rhs = chain(
            conjug(g3(x, 0), plaquette(g3, shift(x, 0), 1, 2)),
            prt,
            conjug(g3(x, 2), plaquette(g3, shift(x, 2), 0, 1)),
        )
        assert meq(lhs, rhs), (x, lhs, rhs)

    # Ordinary additive dTheta is nonzero at origin (hostile control)
    def theta(x, r, s):
        P = plaquette(g3, x, r, s)
        return tr_of(P)

    x0 = (0, 0, 0)
    terms = [
        theta(shift(x0, 0), 1, 2),
        theta(x0, 1, 2),
        theta(shift(x0, 1), 0, 2),
        theta(x0, 0, 2),
        theta(shift(x0, 2), 0, 1),
        theta(x0, 0, 1),
    ]
    dtheta = [
        sum(sign * v[i] for sign, v in zip([1, -1, -1, 1, 1, -1], terms))
        for i in range(2)
    ]
    assert any(d != 0 for d in dtheta), dtheta

    if mutate == "ordinary_dtheta_bianchi":
        # Illegal: treat ordinary dTheta=0 as the Bianchi law.
        if all(d == 0 for d in dtheta):
            fail(
                "ORDINARY_DTHETA_BIANCHI_DID_NOT_BREAK",
                "ordinary dTheta vanished; hostile witness missing",
            )
        fail(
            "ORDINARY_DTHETA_BIANCHI",
            f"illegal dTheta=0 replacement rejected: ordinary additive "
            f"dTheta at origin = {dtheta} != 0 while ordered cube identity holds",
        )

    # Affine coefficient formula on all 81 squares
    for x in product(range(3), repeat=3):
        for r, s in [(0, 1), (0, 2), (1, 2)]:
            gs = [g3(x, r), g3(shift(x, r), s), g3(shift(x, s), r), g3(x, s)]
            ls = [lin_of(g) for g in gs]
            vs = [tr_of(g) for g in gs]
            AA, BB, CC, DD = ls
            uu, vv, ww, zz = vs
            Lam, Theta = affine_lambda_theta(uu, AA, vv, BB, ww, CC, zz, DD)
            assert meq(plaquette(g3, x, r, s), affine(Lam, Theta))

    print(
        "PASS_ORDERED_CUBE_BIANCHI ordered face word identity on (Z/3)^3; "
        f"ordinary dTheta={dtheta} != 0 (not a substitute)"
    )


def check_trace_blindness():
    Lam = mat([[3, -1], [1, 0]])
    Theta = [Q(1), Q(0)]
    P = mul(T_of(Theta), rho(Lam))
    assert trace(P) == trace(rho(Lam))
    assert trace(P) == Q(1) + trace(Lam)
    # Mixed plaquette: pure translation conjugacy has char poly (t-1)^3
    Om = [Q(2), Q(-1)]
    F = mat([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    Pmix = chain(F, T_of(Om), inv(F))
    assert trace(Pmix) == Q(3)
    # (Pmix - I)^2 = 0
    R = sub(Pmix, eye(3))
    assert meq(mul(R, R), zero(3))
    print("PASS_TRACE_BLINDNESS tr(T_Theta rho(Lambda))=tr rho(Lambda); mixed char poly (t-1)^dim")


def check_gauge_origin_shift():
    # Based gauge: P' = E P E^{-1}, t' = E t + (I - P') c
    P = mat([[3, -1], [1, 0]])  # from noncommuting witness linear part
    t = [Q(1), Q(0)]
    E = mat([[2, 1], [0, 1]])
    c = [Q(3), Q(-2)]
    Pp = mul(mul(E, P), inv(E))
    tp = vadd(mv(E, t), mv(sub(eye(2), Pp), c))
    # Operator-level: conjugating affine holonomy by (c,E)
    H = affine(P, t)
    g = affine(E, c)
    Hp = chain(g, H, inv(g))
    assert meq(Hp, affine(Pp, tp)), (Hp, affine(Pp, tp))
    print("PASS_GAUGE_ORIGIN_SHIFT t'=E t+(I-P')c with P'=E P E^{-1}")


def check_fixed_P_quotient():
    # Fixed-P origin shift on V=Q^3 with a singular Lorentz holonomy.
    eta = mat([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
    # Spatial half-turn: P=diag(1,-1,-1), Lorentz, I-P singular.
    P = mat([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
    assert meq(mul(mul(transpose(P), eta), P), eta)
    Imp = sub(eye(3), P)
    assert mat_rank(Imp) == 2
    t = [Q(1), Q(0), Q(0)]  # along ker / not in im
    c = [Q(2), Q(5), Q(-3)]
    t2 = vadd(t, mv(Imp, c))
    assert veq(vsub(t2, t), mv(Imp, c))
    assert in_image(Imp, mv(Imp, c))
    assert in_image(Imp, [Q(0), Q(1), Q(0)])
    assert in_image(Imp, [Q(0), Q(0), Q(1)])
    assert not in_image(Imp, t)
    assert in_image(Imp, [Q(0), Q(0), Q(0)])
    print(
        "PASS_FIXED_P_QUOTIENT t~t+(I-P)c and t~0 iff t in im(I-P) "
        "(half-turn witness: singular I-P, residual class)"
    )


def check_invertible_IP_removable():
    # Loxodromic / invertible I-P: use the noncommuting Lambda (det(I-P)=-1)
    P = mat([[3, -1], [1, 0]])
    Imp = sub(eye(2), P)
    assert det2(Imp) != 0
    # every t removable: c = -(I-P)^{-1} t
    for t in ([Q(1), Q(0)], [Q(0), Q(1)], [Q(7), Q(-3)], [Q(1, 2), Q(5, 3)]):
        c = vneg(mv(inv(Imp), t))
        t2 = vadd(t, mv(Imp, c))
        assert veq(t2, [Q(0), Q(0)])
    print("PASS_INVERTIBLE_IP_REMOVABLE every translation removable when I-P invertible")


def check_singular_lorentz_residual(mutate=None):
    # Rational boost fixing a spacelike axis: P^T eta P = eta on (1+2).
    eta = mat([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
    P = mat([[Q(5, 3), Q(4, 3), 0], [Q(4, 3), Q(5, 3), 0], [0, 0, 1]])
    assert meq(mul(mul(transpose(P), eta), P), eta)
    assert not meq(P, eye(3))
    Imp = sub(eye(3), P)
    assert mat_rank(Imp) == 2
    # Residual direction: the fixed spacelike axis e_2 is killed by I-P,
    # so e_2 is not in im(I-P) (im lives in span of boost plane).
    t = [Q(0), Q(0), Q(1)]
    removable = in_image(Imp, t)
    assert not removable

    if mutate == "false_binary_removable":
        claim_every_removable = True  # illegal mutation claim
        if claim_every_removable and (not meq(P, eye(3))) and (not removable):
            fail(
                "FALSE_BINARY_REMOVABLE",
                "P!=I does NOT imply every t removable: singular Lorentz boost "
                f"with fixed axis has I-P singular and t={t} not in im(I-P)",
            )
        fail(
            "FALSE_BINARY_REMOVABLE_DID_NOT_BREAK",
            "mutation expected a non-removable residual class",
        )

    assert not removable
    # Boost-plane vectors in im(I-P) are removable.
    assert in_image(Imp, [Imp[0][0], Imp[1][0], Imp[2][0]])
    print(
        "PASS_SINGULAR_LORENTZ_RESIDUAL boost P has singular I-P and "
        "non-removable residual translation class [t]"
    )


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    mutate = parse_mutate(argv)

    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: semidirect pair law (b,L)(c,M)=(b+Lc,LM), "
        "ordered affine square Lambda=ABC^{-1}D^{-1} / "
        "Theta=u+Av-ABC^{-1}w-Lambda z, shared-F Omega=d1 kappa, "
        "ordered cube face word, and conjugacy quotient [t] in coker(I-P) "
        "are FIXED before any numeric witness."
    )

    # If a named mutation is requested, run only the mutated check path so the
    # process exits nonzero with the corresponding FAIL_* line.
    if mutate in {None, "", "none"}:
        mutate = None

    if mutate == "wrong_theta_corner":
        check_affine_square(mutate=mutate)
        return 1
    if mutate == "ordinary_dtheta_bianchi":
        check_ordered_cube(mutate=mutate)
        return 1
    if mutate == "false_binary_removable":
        check_singular_lorentz_residual(mutate=mutate)
        return 1
    if mutate is not None and mutate != "all":
        print(f"FAIL_UNKNOWN_MUTATION: unknown --mutate={mutate}")
        return 1

    check_semidirect_mul_inv()
    check_affine_square(mutate=None)
    check_pure_translation_reduction()
    check_noncommuting_linear_witness()
    check_shared_F_mixed()
    check_pure_shared_F_flat()
    check_frame_image_bridge()
    check_ordered_cube(mutate=None)
    check_trace_blindness()
    check_gauge_origin_shift()
    check_fixed_P_quotient()
    check_invertible_IP_removable()
    check_singular_lorentz_residual(mutate=None)

    if mutate == "all":
        # Run each mutation in-process via subprocess-style recursion not needed:
        # explicitly exercise that each mutation path fails.
        for name in ("wrong_theta_corner", "ordinary_dtheta_bianchi", "false_binary_removable"):
            print(f"NOTE: re-run with --mutate={name} to fire FAIL_*")
        fail("MUTATE_ALL", "use a named --mutate=<name>; default path must stay PASS")

    print("PASS_A4D_AFFINE_CURVATURE_PACKET all required positive checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
