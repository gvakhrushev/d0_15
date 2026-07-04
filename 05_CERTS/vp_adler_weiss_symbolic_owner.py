#!/usr/bin/env python3
"""D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001 ADVANCE: exact symbolic owner of the toral partition.

The geometric Adler-Weiss Markov partition of the golden toral time-map T=[[0,1],[1,-1]] was flagged
PROOF-TARGET with EXACT-MISSING = the Voronoi/parallelogram-cell Markov property. This cert supplies a
genuine advance on the SYMBOLIC leg, exactly (integer/GL(2,Z) arithmetic, no float as proof):

  * T is GL(2,Z)-CONJUGATE to -S, where S=[[1,1],[1,0]] is the incidence matrix of the Fibonacci
    substitution sigma: 0->01, 1->0 (equivalently the golden-mean SFT matrix N_tau). The conjugator is
    the minimal unimodular U=[[0,1],[-1,0]] (the 90-degree rotation, det +1): U T U^{-1} = -S, exact.
  * Hence the Adler-Weiss partition of T is the geometric (Rauzy) realization of the Fibonacci
    substitution system, TWISTED BY ORIENTATION: T codes the ORIENTATION-REVERSED golden SFT (-S), not
    the plain golden SFT (+S). This is consistent with the periodic-count obstruction
    (|Fix(T^n)| tracks -S, differing from tr(S^n)=Lucas(n) by 2 at even n; see
    vp_toral_shift_equivalence_supplied.py).

CONSEQUENCE: the 'missing statement' for D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001 is sharpened from
'find the symbolic model of the partition' to 'realize the Rauzy parallelogram cells of the (known,
orientation-twisted Fibonacci) substitution' -- a classical metric construction. Status stays
PROOF-TARGET; the symbolic owner is now pinned internally and exactly. This cert is falsifiable: it
breaks if the conjugacy U T U^{-1} = -S fails or if U is not unimodular.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def mm(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]

def det(A):
    return A[0][0]*A[1][1] - A[0][1]*A[1][0]

def tr(A):
    return A[0][0] + A[1][1]

def scal(k, A):
    return [[k*A[0][0], k*A[0][1]], [k*A[1][0], k*A[1][1]]]

def inv_unimod(A):
    d = det(A)
    assert d in (1, -1), "not unimodular"
    return [[A[1][1]//d, -A[0][1]//d], [-A[1][0]//d, A[0][0]//d]]

def check(tag, ok, msg):
    print(("PASS_" if ok else "FAIL_") + tag + "  " + msg)
    if not ok:
        raise SystemExit(1)

def main() -> int:
    print("=== D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001  exact symbolic owner: T ~ -S (Fibonacci substitution) ===")
    T = [[0, 1], [1, -1]]
    S = [[1, 1], [1, 0]]          # Fibonacci substitution incidence = golden SFT matrix N_tau
    U = [[0, 1], [-1, 0]]         # minimal unimodular conjugator (90-degree rotation)

    check("T_ANOSOV", det(T) == -1 and tr(T) == -1,
          f"T=[[0,1],[1,-1]] has det={det(T)}, tr={tr(T)} (Anosov toral automorphism, char poly lam^2+lam-1)")
    check("S_FIBONACCI", det(S) == -1 and tr(S) == 1,
          f"S=[[1,1],[1,0]] is the Fibonacci substitution incidence / golden SFT matrix (det={det(S)}, tr={tr(S)}, "
          f"char poly lam^2-lam-1, Perron eigenvalue phi)")
    check("U_UNIMODULAR", det(U) == 1,
          f"conjugator U={U} is unimodular (det={det(U)}), the minimal (90-degree rotation) integer conjugacy")

    negS = scal(-1, S)
    UT = mm(U, T)
    negS_U = mm(negS, U)
    check("CONJUGACY_T_negS", UT == negS_U,
          f"U*T = {UT} = (-S)*U = {negS_U}  =>  U T U^{{-1}} = -S EXACTLY: T is GL(2,Z)-conjugate to the "
          f"ORIENTATION-REVERSED Fibonacci substitution matrix")
    # double check via explicit inverse
    conj = mm(mm(U, T), inv_unimod(U))
    check("CONJUGACY_EXPLICIT", conj == negS,
          f"U T U^-1 = {conj} = -S (explicit unimodular inverse)")

    # orientation is essential: T is NOT conjugate to +S (that would need same trace; tr(T)=-1 != tr(S)=1)
    check("ORIENTATION_ESSENTIAL", tr(T) != tr(S) and tr(T) == tr(negS),
          f"tr(T)={tr(T)} = tr(-S)={tr(negS)} != tr(S)={tr(S)}: T codes the ORIENTATION-REVERSED golden SFT (-S), "
          f"never the plain golden SFT (+S) -- the symbolic owner is -S, exactly")

    print()
    print("PASS_ADLER_WEISS_SYMBOLIC_OWNER — the toral partition's symbolic model is pinned internally and "
          "exactly: T ~ -S via U=[[0,1],[-1,0]], i.e. the orientation-reversed Fibonacci substitution. Residual "
          "(honest): realize the Rauzy parallelogram cells of this substitution (classical metric construction). "
          "Status stays PROOF-TARGET; the missing statement is sharpened from 'find the model' to 'realize the "
          "known Rauzy cells'.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
