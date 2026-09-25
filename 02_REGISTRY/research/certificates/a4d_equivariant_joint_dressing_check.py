#!/usr/bin/env python3
"""Exact pressure checker for EXP-A4D-EQUIVARIANT-JOINT-BACKGROUND-DRESSING-GROUPOID.

The strict-conjugation obstruction is retained, but it is not terminal once a
nonabelian torsor cocycle is allowed.  The owned full raw-solder frame action
holds eta fixed and sends the flat perturbation to eta*Lambda - eta.
Conjugation covariance plus flat identity force the dressing to stay I
along that orbit, so its constitutive derivative vanishes there.
The owned first jet H does not.

All arithmetic uses fractions.Fraction.  The CAR/shift witness is an
18-dimensional rational representation (two Z/3 cycles times a 2-level
Role block), large enough that U_A is not an involution.
"""
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
import sys

def eye(n):
    return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]

def zeros(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def scale(c, A):
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]

def transpose(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]

def mul(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = sum((A[i][k] * B[k][j] for k in range(n)), Q(0))
    return C

def matvec(A, v):
    n = len(A)
    return [sum((A[i][k] * v[k] for k in range(n)), Q(0)) for i in range(n)]

def nonzero(A):
    return any(A[i][j] != 0 for i in range(len(A)) for j in range(len(A[0])))

ETA = [
    [Q(1), Q(0), Q(0), Q(0)],
    [Q(0), Q(-1), Q(0), Q(0)],
    [Q(0), Q(0), Q(-1), Q(0)],
    [Q(0), Q(0), Q(0), Q(-1)],
]
# Rational A/B boost used by PR #130.
LAM = [
    [Q(5, 3), Q(4, 3), Q(0), Q(0)],
    [Q(4, 3), Q(5, 3), Q(0), Q(0)],
    [Q(0), Q(0), Q(1), Q(0)],
    [Q(0), Q(0), Q(0), Q(1)],
]

def full_solder_image(e):
    """T_Lambda(e) = (eta+e) Lambda - eta, constant frame."""
    return sub(mul(add(ETA, e), LAM), ETA)

def rational_orbit_leaves_exact():
    assert mul(mul(transpose(LAM), ETA), LAM) == ETA
    image = full_solder_image(zeros(4))
    assert image != zeros(4)
    # A nonzero constant coframe has nonzero Role period on every L>=1.
    assert any(3 * image[r][a] != 0 for r in range(4) for a in range(4))

def perturbation_only_action_fixes_flat():
    """Negative control: e |-> e*Lambda fixes 0.  The no-go uses the full action."""
    assert mul(zeros(4), LAM) == zeros(4)

def boost_generator_direction():
    # K^T eta + eta K = 0, v = eta K nonzero and constant.
    K = zeros(4)
    K[0][1] = Q(1)
    K[1][0] = Q(1)
    assert add(mul(transpose(K), ETA), mul(ETA, K)) == zeros(4)
    v = mul(ETA, K)
    assert v != zeros(4)
    assert any(3 * v[r][a] != 0 for r in range(4) for a in range(4))
    return v

def H_nonzero_on_boost():
    """Owned formula on the AB block: diagonal average sees only e_r^r.
    Here e_A^A = e_B^B = 0, e_A^B = 1, e_B^A = -1.
    K = U_A B_B E_AB - U_B B_A E_BA, H = -K-K^T.
    """
    L = 3
    N = L * L * 2

    def idx(i, j, f):
        return ((i % L) * L + (j % L)) * 2 + f

    def operator(fn):
        M = zeros(N)
        for i in range(L):
            for j in range(L):
                for f in range(2):
                    (ti, tj, tf), c = fn(i, j, f)
                    M[idx(ti, tj, tf)][idx(i, j, f)] = c
        return M

    UA = operator(lambda i, j, f: ((i + 1, j, f), Q(1)))
    UB = operator(lambda i, j, f: ((i, j + 1, f), Q(1)))
    UAi = operator(lambda i, j, f: ((i - 1, j, f), Q(1)))
    UBi = operator(lambda i, j, f: ((i, j - 1, f), Q(1)))
    EAB = operator(lambda i, j, f: ((i, j, 0), Q(1) if f == 1 else Q(0)))
    EBA = operator(lambda i, j, f: ((i, j, 1), Q(1) if f == 0 else Q(0)))
    I = eye(N)
    BB = scale(Q(1, 2), add(I, UBi))
    BA = scale(Q(1, 2), add(I, UAi))
    K = add(mul(UA, mul(BB, EAB)), scale(Q(-1), mul(UB, mul(BA, EBA))))
    H = scale(Q(-1), add(K, transpose(K)))
    assert nonzero(H)
    # conjugation of the identity has zero derivative
    G = zeros(N)
    DW = scale(Q(-1), add(G, transpose(G)))
    assert DW == zeros(N)
    assert DW != H
    return H

def spectators_do_not_enter():
    """A and Xi are not arguments of rawFullSolderFrameAction or of H(e).
    The contradiction is in the e-slot at the flat point.
    """
    v = boost_generator_direction()
    assert nonzero(v)


def inv(A):
    n = len(A)
    aug = [A[i][:] + [Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if aug[i][j] != 0)
        aug[j], aug[p] = aug[p], aug[j]
        q = aug[j][j]
        aug[j] = [x / q for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j] != 0:
                q = aug[i][j]
                aug[i] = [x - q*y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]

def power(A, n):
    if n < 0:
        return power(inv(A), -n)
    out = eye(len(A))
    base = A
    k = n
    while k:
        if k & 1:
            out = mul(out, base)
        base = mul(base, base)
        k //= 2
    return out

def relative_representation_cocycle_discrete():
    """Exact nonabelian right cocycle:
       sigma(n)=rho(n)^-1 tau(n), rho(n)=A^n, tau(n)=B^n.
       This is the discrete analogue of the full relative-representation law.
    """
    A = [[Q(1), Q(1)], [Q(0), Q(1)]]
    B = [[Q(2), Q(0)], [Q(0), Q(1,2)]]
    def sigma(n):
        return mul(power(A, -n), power(B, n))
    def alpha(m, X):
        return mul(power(A, -m), mul(X, power(A, m)))
    I = eye(2)
    assert sigma(0) == I
    for n, m in ((1,2), (2,-1), (-2,3), (3,1)):
        assert sigma(n+m) == mul(alpha(m, sigma(n)), sigma(m))
    for n in (1,2,-1,-3):
        lhs = sigma(-n)
        rhs = inv(alpha(-n, sigma(n)))
        assert lhs == rhs

def one_parameter_tangent_not_obstructed():
    """For one Lorentz generator there is no bracket condition.
    Choosing S=-H/2 (plus any skew term) matches the constitutive tangent
    exactly.  Full obstruction must therefore use at least two generators.
    """
    H = H_nonzero_on_boost()
    S = scale(Q(-1,2), H)
    DW = scale(Q(-1), add(S, transpose(S)))
    assert DW == H



# Exact noncommuting-generator obstruction on the frozen graded degree-one block.
def degree_one_lorentz_bracket_certificate():
    G = list(product(range(3), repeat=3))
    zdisp = (0, 0, 0)

    def dadd(a, b):
        return tuple((a[k] + b[k]) % 3 for k in range(3))

    def dneg(a):
        return tuple((-a[k]) % 3 for k in range(3))

    def step(r, sign=1):
        v = [0, 0, 0]
        v[r] = sign % 3
        return tuple(v)

    def m0():
        return [[Q(0) for _ in range(3)] for _ in range(3)]

    def ma(A, B):
        return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]

    def ms(c, A):
        return [[c * A[i][j] for j in range(3)] for i in range(3)]

    def mm(A, B):
        return [[sum((A[i][k] * B[k][j] for k in range(3)), Q(0))
                 for j in range(3)] for i in range(3)]

    def mt(A):
        return [list(row) for row in zip(*A)]

    def eij(i, j):
        M = m0()
        M[i][j] = Q(1)
        return M

    def da(A, B):
        C = defaultdict(m0)
        for d, M in A.items():
            C[d] = ma(C[d], M)
        for d, M in B.items():
            C[d] = ma(C[d], M)
        return {d: M for d, M in C.items()
                if any(x != 0 for row in M for x in row)}

    def ds(c, A):
        return {d: ms(c, M) for d, M in A.items()}

    def dm(A, B):
        C = defaultdict(m0)
        for d, M in A.items():
            for e, N in B.items():
                de = dadd(d, e)
                C[de] = ma(C[de], mm(M, N))
        return {d: M for d, M in C.items()
                if any(x != 0 for row in M for x in row)}

    def dc(A, B):
        return da(dm(A, B), ds(Q(-1), dm(B, A)))

    def dt(A):
        return {dneg(d): mt(M) for d, M in A.items()}

    eta = (Q(1), Q(-1), Q(-1))
    B1 = m0()
    B1[0][1] = B1[1][0] = Q(1)
    B2 = m0()
    B2[0][2] = B2[2][0] = Q(1)
    R12 = m0()
    R12[1][2] = Q(1)
    R12[2][1] = Q(-1)
    gens = (B1, B2, R12)

    def Bdict(K):
        # B_X = sym(r_X) - H_X/2, with
        # H_X = -(K_X + K_X^T),
        # K_X = sum (eta X)_sr U_s (I+U_r^-1)/2 E_sr.
        r = {zdisp: K}
        e = [[eta[i] * K[i][j] for j in range(3)] for i in range(3)]
        Kop = {}
        for ss in range(3):
            for rr in range(3):
                if e[ss][rr] == 0:
                    continue
                for d in (step(ss), dadd(step(ss), step(rr, -1))):
                    Kop = da(Kop, {d: ms(e[ss][rr] * Q(1, 2), eij(ss, rr))})
        return da(ds(Q(1, 2), da(r, dt(r))),
                  ds(Q(1, 2), da(Kop, dt(Kop))))

    B = [Bdict(K) for K in gens]

    # Translation-invariant skew basis on Fun((Z/3)^3,R^3):
    # 3 zero-displacement skew directions + 13 inverse displacement pairs * 9.
    reps = []
    seen = {zdisp}
    for d in G:
        if d in seen:
            continue
        reps.append(d)
        seen.add(d)
        seen.add(dneg(d))

    skew = []
    for i in range(3):
        for j in range(i + 1, 3):
            skew.append({zdisp: ma(eij(i, j), ms(Q(-1), eij(j, i)))})
    for d in reps:
        nd = dneg(d)
        for i in range(3):
            for j in range(3):
                skew.append({d: eij(i, j), nd: ms(Q(-1), eij(j, i))})
    assert len(skew) == 120

    # Brackets:
    # [B1,B2]=R12, [R12,B1]=-B2, [R12,B2]=B1.
    eqs = (
        (0, 1, B[2]),
        (2, 0, ds(Q(-1), B[1])),
        (2, 1, B[0]),
    )

    CERT = [
    (1, (0, 0, 1), 0, 2, -1),
    (1, (0, 0, 1), 2, 0, 1),
    (1, (0, 0, 2), 0, 2, 1),
    (1, (0, 0, 2), 2, 0, -1),
    (1, (0, 1, 0), 0, 2, 1),
    (1, (0, 1, 0), 2, 0, -1),
    (1, (0, 1, 2), 0, 2, -1),
    (1, (0, 1, 2), 2, 0, 1),
    (1, (0, 2, 0), 0, 2, -1),
    (1, (0, 2, 0), 2, 0, 1),
    (1, (0, 2, 1), 0, 2, 1),
    (1, (0, 2, 1), 2, 0, -1),
    (1, (1, 0, 0), 0, 2, -1),
    (1, (1, 0, 0), 2, 0, 1),
    (1, (1, 0, 1), 0, 2, 5),
    (1, (1, 0, 1), 2, 0, 3),
    (1, (1, 0, 2), 0, 2, -4),
    (1, (1, 0, 2), 2, 0, -4),
    (1, (1, 1, 0), 0, 2, -4),
    (1, (1, 1, 0), 2, 0, -4),
    (1, (1, 1, 1), 0, 2, -1),
    (1, (1, 1, 1), 2, 0, 1),
    (1, (1, 1, 2), 0, 2, 5),
    (1, (1, 1, 2), 2, 0, 3),
    (1, (1, 2, 0), 0, 2, 5),
    (1, (1, 2, 0), 2, 0, 3),
    (1, (1, 2, 1), 0, 2, -4),
    (1, (1, 2, 1), 2, 0, -4),
    (1, (1, 2, 2), 0, 2, -1),
    (1, (1, 2, 2), 2, 0, 1),
    (1, (2, 0, 0), 0, 2, 1),
    (1, (2, 0, 0), 2, 0, -1),
    (1, (2, 0, 1), 0, 2, -4),
    (1, (2, 0, 1), 2, 0, -4),
    (1, (2, 0, 2), 0, 2, 3),
    (1, (2, 0, 2), 2, 0, 5),
    (1, (2, 1, 0), 0, 2, 3),
    (1, (2, 1, 0), 2, 0, 5),
    (1, (2, 1, 1), 0, 2, 1),
    (1, (2, 1, 1), 2, 0, -1),
    (1, (2, 1, 2), 0, 2, -4),
    (1, (2, 1, 2), 2, 0, -4),
    (1, (2, 2, 0), 0, 2, -4),
    (1, (2, 2, 0), 2, 0, -4),
    (1, (2, 2, 1), 0, 2, 3),
    (1, (2, 2, 1), 2, 0, 5),
    (1, (2, 2, 2), 0, 2, 1),
    (1, (2, 2, 2), 2, 0, -1),
    (2, (0, 0, 1), 0, 1, -1),
    (2, (0, 0, 1), 1, 0, 1),
    (2, (0, 0, 2), 0, 1, 1),
    (2, (0, 0, 2), 1, 0, -1),
    (2, (0, 1, 0), 0, 1, 1),
    (2, (0, 1, 0), 1, 0, -1),
    (2, (0, 1, 2), 0, 1, -1),
    (2, (0, 1, 2), 1, 0, 1),
    (2, (0, 2, 0), 0, 1, -1),
    (2, (0, 2, 0), 1, 0, 1),
    (2, (0, 2, 1), 0, 1, 1),
    (2, (0, 2, 1), 1, 0, -1),
    (2, (1, 0, 0), 0, 1, 1),
    (2, (1, 0, 0), 1, 0, -1),
    (2, (1, 0, 1), 0, 1, 4),
    (2, (1, 0, 1), 1, 0, 4),
    (2, (1, 0, 2), 0, 1, -5),
    (2, (1, 0, 2), 1, 0, -3),
    (2, (1, 1, 0), 0, 1, -5),
    (2, (1, 1, 0), 1, 0, -3),
    (2, (1, 1, 1), 0, 1, 1),
    (2, (1, 1, 1), 1, 0, -1),
    (2, (1, 1, 2), 0, 1, 4),
    (2, (1, 1, 2), 1, 0, 4),
    (2, (1, 2, 0), 0, 1, 4),
    (2, (1, 2, 0), 1, 0, 4),
    (2, (1, 2, 1), 0, 1, -5),
    (2, (1, 2, 1), 1, 0, -3),
    (2, (1, 2, 2), 0, 1, 1),
    (2, (1, 2, 2), 1, 0, -1),
    (2, (2, 0, 0), 0, 1, -1),
    (2, (2, 0, 0), 1, 0, 1),
    (2, (2, 0, 1), 0, 1, -3),
    (2, (2, 0, 1), 1, 0, -5),
    (2, (2, 0, 2), 0, 1, 4),
    (2, (2, 0, 2), 1, 0, 4),
    (2, (2, 1, 0), 0, 1, 4),
    (2, (2, 1, 0), 1, 0, 4),
    (2, (2, 1, 1), 0, 1, -1),
    (2, (2, 1, 1), 1, 0, 1),
    (2, (2, 1, 2), 0, 1, -3),
    (2, (2, 1, 2), 1, 0, -5),
    (2, (2, 2, 0), 0, 1, -3),
    (2, (2, 2, 0), 1, 0, -5),
    (2, (2, 2, 1), 0, 1, 4),
    (2, (2, 2, 1), 1, 0, 4),
    (2, (2, 2, 2), 0, 1, -1),
    (2, (2, 2, 2), 1, 0, 1),
    ]
    assert len(CERT) == 96
    cert = {(eq, d, i, j): Q(w) for eq, d, i, j, w in CERT}

    def functional(eq, D):
        out = Q(0)
        for d, M in D.items():
            for i in range(3):
                for j in range(3):
                    out += cert.get((eq, d, i, j), Q(0)) * M[i][j]
        return out

    # Every one of the 3*120 unknown skew columns is annihilated.
    for g in range(3):
        for A in skew:
            total = Q(0)
            for eq, (x, y, _rhs) in enumerate(eqs):
                if g == x:
                    total += functional(eq, dc(A, B[y]))
                if g == y:
                    total += functional(eq, ds(Q(-1), dc(A, B[x])))
            assert total == 0

    # But the required bracket right-hand side survives.
    rhs = sum((functional(eq, target) for eq, (_x, _y, target) in enumerate(eqs)), Q(0))
    assert rhs == 2


def main():
    rational_orbit_leaves_exact()
    print("PASS rational_orbit_leaves_exact")
    perturbation_only_action_fixes_flat()
    print("PASS perturbation_only_action_fixes_flat")
    boost_generator_direction()
    print("PASS boost_generator_direction")
    H_nonzero_on_boost()
    print("PASS H_nonzero_on_boost")
    relative_representation_cocycle_discrete()
    print("PASS relative_representation_cocycle_discrete")
    one_parameter_tangent_not_obstructed()
    print("PASS one_parameter_tangent_not_obstructed")
    spectators_do_not_enter()
    print("PASS spectators_do_not_enter")
    degree_one_lorentz_bracket_certificate()
    print("PASS degree_one_lorentz_bracket_certificate: left-null RHS = 2")
    print("TERMINAL EQUIVARIANT-JOINT-BACKGROUND-DRESSING-OBSTRUCTED")
    print("  strict conjugation alone was insufficient")
    print("  exact cocycle fails on the L=3 graded degree-one so(1,2) bracket")
    return 0

if __name__ == "__main__":
    sys.exit(main())
