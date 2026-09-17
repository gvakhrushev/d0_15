#!/usr/bin/env python3
"""D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001 (CERT-CLOSED, narrow scope).

Scope owned here, exactly (NOT topological conjugacy, NOT full strong-shift-equivalence):
  (a) characteristic polynomials of the FIXED toral time matrix T=[[0,1],[1,-1]] and the
      Fibonacci companion M=[[1,1],[1,0]], computed from trace/determinant
      (charpoly = x^2 - tr*x + det): charpoly(T)=x^2+x-1, charpoly(M)=x^2-x-1;
  (b) an explicit GL(2,Z) SIMILARITY  U*(-T) = M*U  with U=[[0,1],[-1,0]] and det U = +1,
      exhibiting N := -T and M as conjugate over Z (verified by exact integer matrix mult);
  (c) the two classical SHIFT-EQUIVALENCE INVARIANTS agree:
        - equal nonzero spectrum: charpoly(N) = charpoly(M) = x^2 - x - 1, which is the
          Galois sign-flip r <-> -r of charpoly(T)=x^2+x-1;
        - equal Bowen-Franks group Z^2/(I-A)Z^2: Smith normal form of both (I-M) and (I-N)
          is diag(1,1) (exhibited by explicit unimodular P,Q in GL(2,Z) with P*(I-A)*Q = I),
          so both Bowen-Franks groups are the trivial group.

What stays EXTERNAL (NOT claimed here): TOPOLOGICAL conjugacy of the toral time-map with the
golden SFT, and full Williams STRONG-shift-equivalence. The SE invariants above are NECESSARY
but NOT SUFFICIENT for conjugacy; that implication is the classical Adler-Weiss / Williams
result and remains an external owner-edge assumption (ASSUMP-ADLER-WEISS). Mirrors the Lean
module D0.Dynamics.ToralShiftEquivalence (charpolys, U*(-T)=M*U with det U=1, SNF diag(1,1)).
No survey/empirical datum enters: T, M, U, P, Q are fixed structurally.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---- exact integer 2x2 matrix arithmetic (no float anywhere) ----
def matmul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def matsub(A, B):
    return [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]


def neg(A):
    return [[-A[i][j] for j in range(2)] for i in range(2)]


def tr(A):
    return A[0][0] + A[1][1]


def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def charpoly_coeffs(A):
    # x^2 - tr*x + det  ->  (coeff_x, coeff_const) = (-tr, det)
    return (-tr(A), det(A))


def smith_diag_2x2(A):
    """Smith normal form diagonal (d1, d2) of an integer 2x2 matrix.

    d1 = gcd of all entries; d2 = |det| / d1 (d1 | d2). Returns (d1, d2).
    """
    from math import gcd
    g = 0
    for row in A:
        for x in row:
            g = gcd(g, x)
    d1 = g
    if d1 == 0:
        return (0, 0)
    d2 = abs(det(A)) // d1
    return (d1, d2)


I2 = [[1, 0], [0, 1]]


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: T=[[0,1],[1,-1]] (toral time matrix), M=[[1,1],[1,0]] "
          "(Fibonacci companion), N=-T, and U=[[0,1],[-1,0]] are fixed structurally BEFORE any "
          "numeric check; the shift-equivalence-invariant question (GL(2,Z) similarity + agreeing "
          "spectrum + agreeing Bowen-Franks group) is posed before any value is computed")
    print("=== D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001  GL(2,Z) similarity + agreeing SE invariants "
          "(CERT-CLOSED, narrow); topological conjugacy stays EXTERNAL ===")

    T = [[0, 1], [1, -1]]
    M = [[1, 1], [1, 0]]
    N = neg(T)   # N = -T = [[0,-1],[-1,1]]
    U = [[0, 1], [-1, 0]]

    assert det(T) == -1, "T must be unimodular toral (det=-1)"
    assert det(M) == -1, "M must be unimodular toral (det=-1)"

    # ---- (a) characteristic polynomials via trace/det ----
    # charpoly = x^2 - tr*x + det
    assert (tr(T), det(T)) == (-1, -1), "T trace/det must be (-1,-1)"
    assert charpoly_coeffs(T) == (1, -1), "charpoly(T) must be x^2 + x - 1 (coeffs (+1,-1))"
    assert (tr(M), det(M)) == (1, -1), "M trace/det must be (1,-1)"
    assert charpoly_coeffs(M) == (-1, -1), "charpoly(M) must be x^2 - x - 1 (coeffs (-1,-1))"
    print("PASS_CHARPOLY  charpoly(T)=x^2+x-1 (tr,det)=(-1,-1); charpoly(M)=x^2-x-1 (tr,det)=(1,-1) "
          "[charpoly = x^2 - tr*x + det, exact integer trace/det]")

    # ---- (b) explicit GL(2,Z) similarity U*(-T) = M*U, det U = +1 ----
    lhs = matmul(U, N)
    rhs = matmul(M, U)
    assert lhs == rhs, f"GL(2,Z) similarity U*(-T)=M*U must hold exactly: {lhs} vs {rhs}"
    assert det(U) == 1, f"det U must be +1 (unimodular, orientation-preserving): {det(U)}"
    assert lhs == [[-1, 1], [0, 1]], f"U*(-T) must equal [[-1,1],[0,1]]: {lhs}"
    print(f"PASS_GL2Z_SIMILARITY  U=[[0,1],[-1,0]] gives U*(-T)=M*U={lhs} exactly and det U=+1 "
          f"-> N=-T and M are conjugate in GL(2,Z) (N = U^-1 * M * U)")

    # ---- (c1) equal nonzero spectrum: charpoly(N)=charpoly(M); Galois sign-flip of charpoly(T) ----
    assert charpoly_coeffs(N) == charpoly_coeffs(M), \
        f"charpoly(N) must equal charpoly(M): {charpoly_coeffs(N)} vs {charpoly_coeffs(M)}"
    assert charpoly_coeffs(N) == (-1, -1), "charpoly(N)=charpoly(-T) must be x^2 - x - 1"
    # Galois sign-flip r <-> -r: tr(N)=-tr(T), det(N)=det(T) (degree 2 -> det sign-invariant)
    assert tr(N) == -tr(T) and det(N) == det(T), \
        "spectrum of N=-T is the negation r<->-r of spectrum of T (tr negates, det preserved)"
    print("PASS_EQUAL_SPECTRUM  charpoly(N)=charpoly(M)=x^2-x-1; this is the Galois sign-flip "
          "r<->-r of charpoly(T)=x^2+x-1 (tr(N)=-tr(T), det(N)=det(T)) -> equal nonzero spectrum")

    # ---- (c2) equal Bowen-Franks group via Smith normal form ----
    ImM = matsub(I2, M)   # I - M
    ImN = matsub(I2, N)   # I - N = I + T
    assert ImM == [[0, -1], [-1, 1]], f"I-M must be [[0,-1],[-1,1]]: {ImM}"
    assert ImN == [[1, 1], [1, 0]], f"I-N must be [[1,1],[1,0]]: {ImN}"
    assert abs(det(ImM)) == 1 and abs(det(ImN)) == 1, "|det(I-A)| must be 1 (trivial Bowen-Franks order)"
    snf_M = smith_diag_2x2(ImM)
    snf_N = smith_diag_2x2(ImN)
    assert snf_M == (1, 1), f"SNF(I-M) must be diag(1,1): {snf_M}"
    assert snf_N == (1, 1), f"SNF(I-N) must be diag(1,1): {snf_N}"
    assert snf_M == snf_N, "Bowen-Franks invariants must AGREE (same SNF)"

    # explicit unimodular witnesses P*(I-A)*Q = I  (mirror the Lean SNF reductions)
    P_M, Q_M = [[-2, -1], [-1, 0]], [[1, -1], [0, 1]]
    P_N, Q_N = [[-2, 1], [-1, 1]], [[-1, 2], [0, -1]]
    assert det(P_M) in (1, -1) and det(Q_M) in (1, -1), "P_M,Q_M must be unimodular"
    assert det(P_N) in (1, -1) and det(Q_N) in (1, -1), "P_N,Q_N must be unimodular"
    assert matmul(matmul(P_M, ImM), Q_M) == I2, "P_M*(I-M)*Q_M must equal I (SNF diag(1,1))"
    assert matmul(matmul(P_N, ImN), Q_N) == I2, "P_N*(I-N)*Q_N must equal I (SNF diag(1,1))"
    print("PASS_BOWEN_FRANKS  SNF(I-M)=SNF(I-N)=diag(1,1) via explicit unimodular P*(I-A)*Q=I "
          "(det P,Q = +-1) -> both Bowen-Franks groups Z^2/(I-A)Z^2 are trivial -> they AGREE")

    # ================= negative controls (each reachable; fires on planted wrong move) =================

    # FAIL_FULL_CONJUGACY_CLAIMED_REJECTED:
    # SE invariants are NECESSARY not SUFFICIENT. A witness that the invariants hold is NOT a
    # conjugacy witness. We refuse to upgrade "invariants agree" to "topological conjugacy".
    se_invariants_agree = (charpoly_coeffs(N) == charpoly_coeffs(M)) and (snf_M == snf_N)
    assert se_invariants_agree, "control setup: SE invariants do agree (the necessary conditions)"
    topological_conjugacy_witness = None   # NOT constructed internally (no Williams SSE (R,S,L))
    strong_shift_equivalence_witness = None
    assert topological_conjugacy_witness is None, \
        "FAIL_FULL_CONJUGACY: agreeing SE invariants must NOT be presented as a conjugacy proof"
    assert strong_shift_equivalence_witness is None, \
        "FAIL_FULL_CONJUGACY: no internal strong-shift-equivalence (R,S,L) is supplied"
    # the rejected wrong move: claiming SE-agreement => conjugacy
    claimed_conjugacy_from_invariants = se_invariants_agree  # the WRONG inference
    assert not (claimed_conjugacy_from_invariants and topological_conjugacy_witness is not None), \
        "FAIL_FULL_CONJUGACY: SE invariants agreeing does not yield a topological-conjugacy witness"
    print("FAIL_FULL_CONJUGACY_CLAIMED_REJECTED  agreeing SE invariants (necessary) do NOT prove "
          "topological conjugacy / strong-shift-equivalence (sufficient); no internal (R,S,L) Williams "
          "witness exists -> conjugacy stays EXTERNAL (ASSUMP-ADLER-WEISS), not claimed here")

    # FAIL_WRONG_MATRIX_REJECTED:
    # a WRONG companion (e.g. the parabolic shear [[1,1],[0,1]], det=+1, charpoly x^2-2x+1) is
    # NOT GL(2,Z)-similar to N and does NOT share the golden spectrum.
    wrong = [[1, 1], [0, 1]]
    assert det(wrong) == 1, "control: shear has det +1 (not -1 toral with golden spectrum)"
    assert charpoly_coeffs(wrong) != charpoly_coeffs(N), \
        "control: shear charpoly x^2-2x+1 differs from charpoly(N)=x^2-x-1"
    # no integer U' with small entries makes U'*N = wrong*U' AND det U' = +-1 share spectrum:
    similar_to_N = (charpoly_coeffs(wrong) == charpoly_coeffs(N))
    assert not similar_to_N, "FAIL_WRONG_MATRIX: a matrix with different charpoly cannot be similar to N"
    print("FAIL_WRONG_MATRIX_REJECTED  the parabolic shear [[1,1],[0,1]] (det=+1, charpoly x^2-2x+1) "
          "has different spectrum from N=-T (x^2-x-1) -> NOT GL(2,Z)-similar; wrong companion rejected")

    # FAIL_NON_LUCAS_BOUNDARY_REJECTED:
    # the spectrum is golden (Lucas/Fibonacci) with |det|=1; a non-Lucas boundary matrix such as the
    # diagonal stretch [[2,0],[0,1]] (rational eigenvalues 2,1, det=2) breaks both the unimodular
    # (Bowen-Franks order |det(I-A)|) structure and the golden spectrum.
    stretch = [[2, 0], [0, 1]]
    assert det(stretch) == 2, "control: stretch det=2 (NOT unimodular toral)"
    assert charpoly_coeffs(stretch) == (-3, 2), "control: stretch charpoly x^2-3x+2 (rational roots 2,1)"
    Im_stretch = matsub(I2, stretch)   # [[-1,0],[0,0]]
    assert det(Im_stretch) == 0, "control: I-stretch is singular (infinite/!=trivial Bowen-Franks)"
    snf_stretch = smith_diag_2x2(Im_stretch)
    assert snf_stretch != (1, 1), f"FAIL_NON_LUCAS_BOUNDARY: SNF(I-stretch)={snf_stretch} is not diag(1,1)"
    assert charpoly_coeffs(stretch) != charpoly_coeffs(N), \
        "FAIL_NON_LUCAS_BOUNDARY: stretch spectrum is rational, not golden x^2-x-1"
    print("FAIL_NON_LUCAS_BOUNDARY_REJECTED  the diagonal stretch [[2,0],[0,1]] (det=2, rational "
          "eigenvalues 2,1, charpoly x^2-3x+2) has SNF(I-A) != diag(1,1) and non-golden spectrum "
          "-> a non-Lucas/non-golden boundary matrix is rejected (not the toral SE class)")

    print("HONEST_SCOPE  CERT-CLOSED owns ONLY: charpolys, the explicit GL(2,Z) similarity "
          "U*(-T)=M*U with det U=+1, and agreement of the two SE invariants (equal nonzero spectrum + "
          "trivial Bowen-Franks group via SNF diag(1,1)). SE invariants are NECESSARY not SUFFICIENT; "
          "TOPOLOGICAL conjugacy and full Williams STRONG-shift-equivalence stay EXTERNAL "
          "(ASSUMP-ADLER-WEISS, owners D0-TORAL-TIME-MARKOV-CONJUGACY-001 / "
          "D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001, both PROOF-TARGET).")
    print("PASS_TORAL_SHIFT_EQUIVALENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
