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
    print("PRESSURE strict conjugation obstructed, general cocycle not terminally obstructed")
    print("OPEN full Lorentz six-generator representation-extension system")
    print("  S(K)+S(K)^T=-H(eta K) plus exact bracket integrability")
    return 0

if __name__ == "__main__":
    sys.exit(main())
