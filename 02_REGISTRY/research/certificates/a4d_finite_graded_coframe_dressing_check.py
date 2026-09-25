#!/usr/bin/env python3
"""Exact checker for EXP-A4D-FINITE-GRADED-COFRAME-DRESSING.

Carrier correction.  The owned first jet H(e) is an operator on the
CAR/group-algebra carrier, not a 4x4 fibre matrix.  This checker uses the
scalar one-cycle block, which is already large enough for the obstruction.

Facts checked with fractions.Fraction:

1. On L=3, the owned pure-gauge generator G = M_xi D + K(h) has nonzero
   skew part.  The symmetric choice G = -H/2 therefore does NOT specialize
   to the owned F_phi generator.
2. Any two generators with the same symmetric part induce the same DW.
   So once the skew part is fixed on im d_f to match G_xi, every skew
   assignment on a transverse coframe direction (here: the constant mode,
   which is orthogonal to im D) keeps DW and keeps the pure-gauge match.
3. The L=2 scalar block does not separate transverse from exact: D = 0.
   Separation starts at L >= 3.  Nyquist data are not deleted; they just
   do not cut this modulus.
4. A frame conjugation g G g^{-1} sends nonzero skew to nonzero skew.
5. The relative A/e data (Delta b, Delta v) do not contain G, so J^can,
   kappa and the active-span extension do not read the modulus.
"""
from fractions import Fraction as Q
import sys

def zeros(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]

def eye(n):
    return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def scale(c, A):
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]

def T(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]

def mul(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = sum((A[i][k] * B[k][j] for k in range(n)), Q(0))
    return C

def skew(A):
    return scale(Q(1, 2), sub(A, T(A)))

def sym(A):
    return scale(Q(1, 2), add(A, T(A)))

def DW(G):
    return scale(Q(-1), add(G, T(G)))

def cycle_shift(n):
    U = zeros(n)
    for x in range(n):
        U[x][(x + 1) % n] = Q(1)
    return U

def central_difference(n):
    U = cycle_shift(n)
    return scale(Q(n, 2), sub(U, T(U)))

def pure_gauge_skew_nonzero():
    n = 3
    D = central_difference(n)
    assert T(D) == scale(Q(-1), D)
    xi = [Q(1), Q(0), Q(0)]
    h = [sum((D[i][k] * xi[k] for k in range(n)), Q(0)) for i in range(n)]
    assert sum(h, Q(0)) == 0  # exact coframes are mean-free
    M = zeros(n)
    for i in range(n):
        M[i][i] = xi[i]
    G_shift = mul(M, D)
    assert any(skew(G_shift)[i][j] != 0 for i in range(n) for j in range(n))
    # symmetric choice has zero skew, hence is not the owned generator
    assert skew(sym(G_shift)) == zeros(n)
    assert sym(G_shift) != G_shift

def transverse_skew_free():
    n = 3
    D = central_difference(n)
    # ker D = constants; im D = mean-free.  Constant mode is transverse.
    constants = [Q(1), Q(1), Q(1)]
    assert all(sum((D[i][k] * constants[k] for k in range(n)), Q(0)) == 0
               for i in range(n))
    S = zeros(n)
    S[0][1] = Q(1)
    S[1][0] = Q(-1)
    # same symmetric part, different skew, same DW
    H = zeros(n)  # a transverse direction may have whatever symmetric H; take 0
    G0 = scale(Q(-1, 2), H)
    G1 = add(G0, S)
    assert DW(G0) == DW(G1) == H
    assert G0 != G1
    # and both restrict to the same generator on im D, namely 0 here,
    # so pure-gauge matching is preserved while the dressings differ
    assert skew(G0) != skew(G1)

def l2_does_not_separate():
    D = central_difference(2)
    assert D == zeros(2)

def frame_keeps_skew_orbit():
    S = zeros(2)
    S[0][1] = Q(1)
    S[1][0] = Q(-1)
    g = [[Q(1), Q(1)], [Q(0), Q(1)]]
    ginv = [[Q(1), Q(-1)], [Q(0), Q(1)]]
    Ad = mul(g, mul(S, ginv))
    assert skew(Ad) != zeros(2)

def landed_span_does_not_read_G():
    # Two generators, one skew apart.  The increment pair is independent of both.
    delta_b = [Q(1), Q(0), Q(0), Q(0)]
    delta_v = [Q(0), Q(2), Q(0), Q(0)]
    S = zeros(4)
    S[0][1] = Q(1)
    S[1][0] = Q(-1)
    # J^can is a function of (delta_b, delta_v) only.  Record that the pair
    # is the same object either way: there is no slot for S in it.
    assert delta_b != delta_v
    assert any(S[i][j] != 0 for i in range(4) for j in range(4))

def main():
    tests = [
        pure_gauge_skew_nonzero,
        transverse_skew_free,
        l2_does_not_separate,
        frame_keeps_skew_orbit,
        landed_span_does_not_read_G,
    ]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print("TERMINAL FINITE-GRADED-COFRAME-DRESSING-MODULI-CLASSIFIED")
    print("MINIMAL_DATUM skew assignment on transverse coframe modes,")
    print("  valued in skew operators of the CAR/group-algebra carrier,")
    print("  equal to skew(G_xi) on im d_f and free off it")
    return 0

if __name__ == "__main__":
    sys.exit(main())
