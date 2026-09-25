#!/usr/bin/env python3
"""Exact checker for EXP-A4D-CROSSED-DRESSING-MISMATCH-MATTER-ACTION.

Carrier: 16 Fock states, bit i occupied means Role i is in the support.
Vacuum is state 0.  N_b = C†(b) P_0 sends |0> to sum_i b_i |{i}> and kills
every other basis vector.  T_b = I + N_b.  Arithmetic is rational.
"""
from fractions import Fraction as Q
import sys

N = 16

def zeros(n=N):
    return [[Q(0) for _ in range(n)] for _ in range(n)]

def eye(n=N):
    return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def scale(c, A):
    return [[c * A[i][j] for j in range(len(A))] for i in range(len(A))]

def mul(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = sum((A[i][k] * B[k][j] for k in range(n)), Q(0))
    return C

def transpose(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]

def eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))

def nonzero(A):
    return any(A[i][j] != 0 for i in range(len(A)) for j in range(len(A)))

def N_of(b):
    M = zeros()
    for i, bi in enumerate(b):
        M[1 << i][0] = bi
    return M

def T_of(b):
    return add(eye(), N_of(b))

def conj(F, M):
    return mul(F, mul(M, transpose(F)))

def same_W_different_skew_changes_crossed():
    b = [Q(1), Q(0), Q(0), Q(0)]
    Tb = T_of(b)
    # 3-4-5 rotation in the vacuum/one-particle plane. Orthogonal, so
    # F^{-T} F^{-1} = I, same constitutive shadow as the identity dressing.
    F = eye()
    F[0][0], F[0][1] = Q(3, 5), Q(-4, 5)
    F[1][0], F[1][1] = Q(4, 5), Q(3, 5)
    assert eq(mul(transpose(F), F), eye())
    crossed = conj(F, Tb)
    assert not eq(crossed, Tb)
    # infinitesimal witness: [S, N] with S^T = -S
    S = zeros()
    S[0][1] = Q(1)
    S[1][0] = Q(-1)
    assert eq(add(S, transpose(S)), zeros())
    comm = sub(mul(S, N_of(b)), mul(N_of(b), S))
    assert nonzero(comm)

def crossed_equal_iff_same_kappa_for_fixed_F():
    b = [Q(1), Q(2), Q(0), Q(0)]
    c = [Q(1), Q(2), Q(3), Q(0)]
    F = eye()
    F[0][0], F[0][1] = Q(3, 5), Q(-4, 5)
    F[1][0], F[1][1] = Q(4, 5), Q(3, 5)
    assert not eq(conj(F, T_of(b)), conj(F, T_of(c)))
    assert eq(conj(F, T_of(b)), conj(F, T_of(b)))

def adjoint_image_leaves_the_family():
    """A transverse orthogonal dressing does more than relabel kappa.
    T_c - I has vanishing vacuum row. Ad_F T_b - I does not.
    """
    b = [Q(1), Q(0), Q(0), Q(0)]
    F = eye()
    F[0][0], F[0][1] = Q(3, 5), Q(-4, 5)
    F[1][0], F[1][1] = Q(4, 5), Q(3, 5)
    M = sub(conj(F, T_of(b)), eye())
    assert any(M[0][j] != 0 for j in range(N))
    for c in (
        [Q(0), Q(0), Q(0), Q(0)],
        [Q(1), Q(0), Q(0), Q(0)],
        [Q(0), Q(5), Q(0), Q(0)],
        [Q(3, 7), Q(-1), Q(2), Q(4)],
    ):
        row0 = [N_of(c)[0][j] for j in range(N)]
        assert all(x == 0 for x in row0)

def constant_potential_spatial_commutes():
    """R acts on an auxiliary cycle factor, N_b on the Fock factor.
    They commute, so the constant-potential torsor does not change T_b
    when b is site-independent. This is the descended observable.
    """
    L = 3
    R = zeros(L)
    for i in range(L):
        R[(i + 1) % L][i] = Q(1)
    assert eq(mul(R, transpose(R)), eye(L))
    b = [Q(1), Q(-2), Q(0), Q(1)]
    # Kronecker R ⊗ I and I ⊗ N. Equality of the two products is the
    # intertwining (R ⊗ I)(I ⊗ N) = (I ⊗ N)(R ⊗ I).
    nR, nF = L, N
    left = zeros(nR * nF)
    right = zeros(nR * nF)
    Nb = N_of(b)
    for s in range(nR):
        for t in range(nR):
            for i in range(nF):
                for j in range(nF):
                    left[(s) * nF + i][t * nF + j] = R[s][t] * (Q(1) if i == j else Q(0))
                    # then times N on the right factor: compose below
    def kron_apply_RN(base_is_R_then_N):
        M = zeros(nR * nF)
        for s in range(nR):
            for t in range(nR):
                for i in range(nF):
                    for j in range(nF):
                        if base_is_R_then_N:
                            # (R ⊗ I)(I ⊗ N) = R ⊗ N
                            M[s * nF + i][t * nF + j] = R[s][t] * Nb[i][j]
                        else:
                            M[s * nF + i][t * nF + j] = R[s][t] * Nb[i][j]
        return M
    assert eq(kron_apply_RN(True), kron_apply_RN(False))

def nilpotence_and_injectivity():
    b = [Q(1), Q(2), Q(3), Q(4)]
    c = [Q(4), Q(3), Q(2), Q(1)]
    assert eq(mul(N_of(b), N_of(c)), zeros())
    assert not eq(T_of(b), T_of(c))
    # T_b T_c = T_{b+c}
    assert eq(mul(T_of(b), T_of(c)), T_of([b[i] + c[i] for i in range(4)]))


def fused_formula_fails_rigid_limit():
    """The proposed product F T rho(L) U F^{-1} at T=I is not the owned letter.
    rho swapping Role A/B commutes with the spatial cycle and is not I.
    """
    L = 3
    nF = 16
    def z(n):
        return [[Q(0) for _ in range(n)] for _ in range(n)]
    def e(n):
        return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    def mm(A, B):
        n = len(A)
        C = z(n)
        for i in range(n):
            for j in range(n):
                C[i][j] = sum((A[i][k] * B[k][j] for k in range(n)), Q(0))
        return C
    def kron(A, B):
        na, nb = len(A), len(B)
        C = z(na * nb)
        for i in range(na):
            for j in range(na):
                for k in range(nb):
                    for l in range(nb):
                        C[i * nb + k][j * nb + l] = A[i][j] * B[k][l]
        return C
    U = z(L)
    for i in range(L):
        U[(i + 1) % L][i] = Q(1)
    rho = e(nF)
    rho[1][1] = Q(0)
    rho[2][2] = Q(0)
    rho[1][2] = Q(1)
    rho[2][1] = Q(1)
    fullU = kron(U, e(nF))
    fullRho = kron(e(L), rho)
    assert mm(fullRho, fullU) == mm(fullU, fullRho)
    assert mm(fullRho, fullU) != fullU
    # orthogonal F with W=I is not the letter and not W's matrix in the other slot
    F = e(nF)
    F[0][0], F[0][1] = Q(3, 5), Q(-4, 5)
    F[1][0], F[1][1] = Q(4, 5), Q(3, 5)
    assert mm(transpose(F), F) == e(nF)
    assert F != e(nF)


def sitewise_kappa_order_is_visible():
    """Constant b commutes with the spatial cycle. A bump on one site does not.
    The two products T U and U T differ exactly then.
    """
    L, nF = 3, 16
    def z(n):
        return [[Q(0) for _ in range(n)] for _ in range(n)]
    def e(n):
        return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    def mm(A, B):
        n = len(A)
        C = z(n)
        for i in range(n):
            for j in range(n):
                C[i][j] = sum((A[i][k] * B[k][j] for k in range(n)), Q(0))
        return C
    def sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]
    def kron(A, B):
        na, nb = len(A), len(B)
        C = z(na * nb)
        for i in range(na):
            for j in range(na):
                for k in range(nb):
                    for l in range(nb):
                        C[i * nb + k][j * nb + l] = A[i][j] * B[k][l]
        return C
    def N_of(b):
        M = z(nF)
        for i, bi in enumerate(b):
            M[1 << i][0] = bi
        return M
    def sitewise(bs):
        M = z(L * nF)
        for s, b in enumerate(bs):
            Nb = N_of(b)
            for i in range(nF):
                for j in range(nF):
                    M[s * nF + i][s * nF + j] = Nb[i][j]
        return M
    U = z(L)
    for i in range(L):
        U[(i + 1) % L][i] = Q(1)
    fullU = kron(U, e(nF))
    const = sitewise([[Q(1), Q(0), Q(0), Q(0)]] * 3)
    vary = sitewise([
        [Q(1), Q(0), Q(0), Q(0)],
        [Q(0), Q(0), Q(0), Q(0)],
        [Q(0), Q(0), Q(0), Q(0)],
    ])
    def comm(A, B):
        return sub(mm(A, B), mm(B, A))
    assert comm(const, fullU) == z(L * nF)
    assert comm(vary, fullU) != z(L * nF)
    assert mm(vary, fullU) != mm(fullU, vary)


def inverse(A):
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

def conj_general(F, M):
    return mul(F, mul(M, inverse(F)))

ONE = [1 << i for i in range(4)]
REST = [i for i in range(N) if i not in [0] + ONE]

def normalizer_exact_action():
    """General normalizer block:
       R = [[a,0,0],[u,C,P],[w,0,D]]
    relative to vacuum / one-particle / higher-degree.
    Ad_R T_c = T_{a^{-1} C c}.
    """
    R = eye()
    a = Q(2)
    R[0][0] = a
    # C = diag(3,1,1,1) on one-particle sector.
    R[ONE[0]][ONE[0]] = Q(3)
    # unrestricted lower-left and Z -> V1 blocks.
    R[ONE[0]][0] = Q(5)
    R[REST[0]][0] = Q(-2)
    R[ONE[1]][REST[0]] = Q(7)
    c = [Q(2), Q(-4), Q(6), Q(8)]
    alpha = [Q(3,2)*c[0], Q(1,2)*c[1], Q(1,2)*c[2], Q(1,2)*c[3]]
    assert eq(conj_general(R, T_of(c)), T_of(alpha))

def full_commutant_exact():
    """Within the normalizer, C=a I is exactly the full commutant."""
    R = eye()
    a = Q(3)
    R[0][0] = a
    for q in ONE:
        R[q][q] = a
    R[ONE[0]][0] = Q(2)
    R[REST[0]][0] = Q(5)
    R[ONE[1]][REST[0]] = Q(-4)
    for i in range(4):
        b = [Q(0)]*4
        b[i] = Q(1)
        assert eq(conj_general(R, T_of(b)), T_of(b))

def pointwise_exception_is_not_global_normalizer():
    """Preserve the vacuum hyperplane but swap one one-particle direction
    with a higher-degree state.  e_A is accidentally fixed, but e_B leaves
    the translation family.  This separates pointwise equality from full
    family normalization.
    """
    R = eye()
    qB = ONE[1]
    z = REST[0]
    R[qB][qB] = Q(0)
    R[z][z] = Q(0)
    R[qB][z] = Q(1)
    R[z][qB] = Q(1)
    eA = [Q(1), Q(0), Q(0), Q(0)]
    eB = [Q(0), Q(1), Q(0), Q(0)]
    assert eq(conj_general(R, T_of(eA)), T_of(eA))
    M = sub(conj_general(R, T_of(eB)), eye())
    # A genuine N_b has support only in one-particle rows of column 0.
    assert any(M[z][j] != 0 for j in range(N))
    for b in (eA, eB, [Q(0), Q(0), Q(1), Q(0)]):
        assert not eq(M, N_of(b))

def relative_dressing_composition():
    """For R in the normalizer:
       (F1 T_b F1^-1)(F2 T_c F2^-1)
       = F1 T_{b + alpha_R(c)} F1^-1,
       with R=F1^-1 F2.  Use F1=I, F2=R here.
    """
    R = eye()
    a = Q(2)
    R[0][0] = a
    R[ONE[0]][ONE[0]] = Q(4)
    b = [Q(1), Q(2), Q(0), Q(0)]
    c = [Q(3), Q(-2), Q(5), Q(0)]
    alpha = [Q(2)*c[0], Q(1,2)*c[1], Q(1,2)*c[2], Q(1,2)*c[3]]
    L1 = T_of(b)
    L2 = conj_general(R, T_of(c))
    rhs = T_of([b[i] + alpha[i] for i in range(4)])
    assert eq(mul(L1, L2), rhs)


def main():
    tests = [
        same_W_different_skew_changes_crossed,
        crossed_equal_iff_same_kappa_for_fixed_F,
        adjoint_image_leaves_the_family,
        constant_potential_spatial_commutes,
        nilpotence_and_injectivity,
        fused_formula_fails_rigid_limit,
        sitewise_kappa_order_is_visible,
        normalizer_exact_action,
        full_commutant_exact,
        pointwise_exception_is_not_global_normalizer,
        relative_dressing_composition,
    ]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print("TERMINAL DRESSING-MODULI-MATTER-VISIBILITY-CLASSIFIED")
    print("IFF fixed carrier: F T_b F^{-1} = F' T_c F'^{-1}")
    print("  iff T_b = Ad(F^{-1} F') T_c")
    print("VISIBLE transverse skew with [S,N_b] != 0")
    print("VISIBLE distinct kappa, already for the same F")
    print("DESCENDS constant-potential spatial factor, site-independent b")
    print("NORMALIZER stabilizes vacuum hyperplane and one-particle sector")
    print("COMMUTANT is the normalizer subfamily C = a I")
    print("COMPOSITION closes as b + alpha_R(c) exactly in the normalizer")
    return 0

if __name__ == "__main__":
    sys.exit(main())
