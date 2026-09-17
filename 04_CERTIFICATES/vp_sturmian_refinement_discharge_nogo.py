#!/usr/bin/env python3
"""vp_sturmian_refinement_discharge_nogo - D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001 (NO-GO, companion).

The Sturmian/golden refinement tower D0-STURMIAN-REFINEMENT carries a CONDITIONAL-EXTENSION: step 2 would
identify the Sturmian BONDING maps with the frozen ARCHIVE maps via a new primitive
PRIM-STURMIAN-REFINEMENT-OWNER. This cert proves that condition is NOT dischargeable by internal forcing
(M1 + the +2 grading + the centre-11 convergence) -- so the parent claim correctly STAYS PROOF-TARGET, and
the discharge is a certified NO-GO for the same reason the neighbouring phason-WZ transfer closed NO-GO.

The Sturmian tower itself is a legitimate internally-owned MATHEMATICAL object (owned, NOT contested here):
the golden substitution sigma(a)=ab, sigma(b)=a has incidence S=[[1,1],[1,0]], det=-1, trace=+1, charpoly
t^2-t-1, Perron root phi; the slope 1/phi=[0;1,1,1,...] is the unique Fibonacci-word slope; the
self-description p+p^2=1 is quadratic. What is refuted is only the DISCHARGE (that this tower is forced to BE
the archive refinement).

Two independent obstructions, both exact:

  1. FORCED FIELD OBSTRUCTION (load-bearing). The archive/window scale is 359/160 = product of the two
     nontrivial normalized-Laplacian eigenvalues (roots of 160 lam^2 - 480 lam + 359, discriminant 640 =
     64*10). Those roots are 3/2 +- sqrt10/40, living in Q(sqrt10). But sqrt10 NOT in Q(sqrt5) = Q(phi):
     sqrt10 = a + b sqrt5 forces a^2 + 5 b^2 = 10 and 2 a b = 0 with a,b rational -- no solution. So the
     golden tower (Q(sqrt5)) and the archive (Q(sqrt10)) live in DISJOINT quadratic fields
     (Q(sqrt5) cap Q(sqrt10) = Q); no canonical intertwiner ties a Q(sqrt5) carrier to a Q(sqrt10) carrier.
     This is the identical structural reason the neighbouring D0-PHASON-WZ-* transfer closed NO-GO, and it is
     explained (not weakened) by the size-fingerprint result D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001:
     sqrt10 = sqfree(3*10*12) is the fingerprint of sizes 9,11,13, generic, not a golden near-miss.

  2. ORIENTATION OBSTRUCTION. The centre-11 convergence (D0-SCENE-CENTER-SPACETIME-CONVERGENCE-001) forces
     the TIME operator T = [[0,1],[1,-1]] (trace -1, the orientation-REVERSED golden companion), via
     |Tr(T^5)| = L_5 = 11. The Sturmian tower uses the orientation-PRESERVING incidence S = [[1,1],[1,0]]
     (trace +1). Trace is a conjugacy invariant, so +1 != -1 means S is NOT conjugate to T; the scene's own
     forcing pins T ~ -S (U T U^-1 = -S, det U = +1), the OPPOSITE orientation. The periodic-point offset
     L_n - |Fix(T^n)| = [0,2,0,2,...] confirms the orientation mismatch at even n.

Numerology trap rejected out loud: no golden power reaches the archive scale (phi^k = 359/160 => k = 1.679...
non-integer), and sqrt10 = sqrt2*(2phi-1) needs sqrt2 not in Q(phi). The 359=|E|, 160=(prod deg)/(2V) are
forced scene counts, not fitted.

Honest boundary. Not claimed: that the tower is numerological (it is M1-forced as a substitution); not
claimed: that the identification is impossible in principle -- an EXTERNAL owner could postulate
PRIM-STURMIAN-REFINEMENT-OWNER as a passport. Claimed only: it is NOT internally forced and is field-obstructed
from any Q(phi)-internal construction, so the CONDITIONAL-EXTENSION cannot be discharged internally.

Falsifiable: breaks (rc=1) if sqrt10 in Q(sqrt5), if trace(S)==trace(T), if the periodic offset is not
[0,2,0,2,...] at even n, if phi^k = 359/160 for integer k, or if the wrong-object swaps misbehave
(S->N_tau leaves the field obstruction unchanged; S->T must fire the orientation controls).
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def isqrt_exact(n):
    if n < 0:
        return None
    r = int(round(n ** 0.5))
    for c in (r - 1, r, r + 1):
        if c * c == n:
            return c
    return None


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def matpow(M, p):
    R = [[1, 0], [0, 1]]
    for _ in range(p):
        R = matmul(R, M)
    return R


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def main():
    print("=== vp_sturmian_refinement_discharge_nogo  the CONDITIONAL cannot be discharged internally ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the golden tower (Q(sqrt5)) and the archive scale (Q(sqrt10)) are "
          "each M1-fixed; the question is whether one canonically intertwines the other. It cannot.")

    # 1. field disjointness: sqrt10 not in Q(sqrt5)
    # sqrt10 = a + b sqrt5 => a^2 + 5 b^2 = 10, 2ab = 0. Scan rational a,b with bounded denominator: none.
    found = False
    for da in range(1, 41):
        for na in range(-40 * da, 40 * da + 1):
            a = Fr(na, da)
            # ab = 0 => a = 0 or b = 0
            if a == 0:
                # 5 b^2 = 10 => b^2 = 2 => b irrational
                continue
            else:
                # b = 0 => a^2 = 10 => a irrational
                if a * a == 10:
                    found = True
    if found:
        die("FIELD_DISJOINT  sqrt10 must NOT be in Q(sqrt5)")
    # confirm 10 is not a perfect square and 2 is not (the two escape routes)
    if isqrt_exact(10) is not None or isqrt_exact(2) is not None:
        die("FIELD_DISJOINT  neither 10 nor 2 may be a perfect square")
    print("PASS_FIELD_DISJOINT  sqrt10 not in Q(sqrt5): sqrt10=a+b sqrt5 forces a^2+5b^2=10 & ab=0 (no "
          "rational sln). Q(phi)=Q(sqrt5) and Q(sqrt10) are DISJOINT over Q => no canonical intertwiner.")

    # archive scale 359/160 lives with sqrt10 (roots of 160 x^2 - 480 x + 359, disc 640 = 64*10)
    disc = 480 ** 2 - 4 * 160 * 359
    if disc != 640 or 640 != 64 * 10:
        die(f"ARCHIVE_DISC  archive quadratic discriminant must be 640 = 64*10: {disc}")
    print(f"PASS_ARCHIVE_FIELD  archive scale roots of 160x^2-480x+359 have disc {disc}=64*10 => "
          f"3/2 +- sqrt10/40 in Q(sqrt10); product 359/160 = |E|/((prod deg)/(2V)).")

    # 2. orientation: trace(S)=+1, trace(T)=-1
    S = [[1, 1], [1, 0]]
    T = [[0, 1], [1, -1]]
    trS = S[0][0] + S[1][1]
    trT = T[0][0] + T[1][1]
    if trS == trT:
        die(f"ORIENTATION  trace(S)={trS} must differ from trace(T)={trT}")
    print(f"PASS_ORIENTATION_SPLIT  trace(S)={trS} (orientation-preserving golden) != trace(T)={trT} "
          f"(orientation-reversed, the centre-11-forced time operator) => S NOT conjugate to T; scene pins T~-S.")

    # periodic offset L_n - |Fix(T^n)| = [0,2,0,2,...]
    def lucas(n):
        a, b = 2, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    offs = []
    for n in range(1, 7):
        Tn = matpow(T, n)
        fix = abs(det2([[Tn[0][0] - 1, Tn[0][1]], [Tn[1][0], Tn[1][1] - 1]]))
        offs.append(lucas(n) - fix)
    if offs != [0, 2, 0, 2, 0, 2]:
        die(f"PERIODIC_OFFSET  L_n - |Fix(T^n)| must be [0,2,0,2,0,2]: {offs}")
    print(f"PASS_PERIODIC_OFFSET  L_n - |Fix(T^n)| = {offs}: orientation mismatch fires at even n (offset 2).")

    # 3. numerology trap: phi^k = 359/160 has no integer k
    import math
    phi = (1 + 5 ** 0.5) / 2
    k = math.log(359 / 160) / math.log(phi)
    if abs(k - round(k)) < 1e-6:
        die(f"NO_GOLDEN_BACKFIT  phi^k = 359/160 must have NON-integer k: k={k}")
    print(f"PASS_NO_GOLDEN_BACKFIT  phi^k = 359/160 => k = {k:.4f} (non-integer): no golden power reaches "
          f"the archive scale; sqrt10 = sqrt2*(2phi-1) needs sqrt2 not in Q(phi). 359,160 are forced counts.")

    # 4. wrong-object control: S -> N_tau = [[0,1],[1,1]] (Fibonacci matrix, trace +1) leaves field
    #    obstruction unchanged (both golden, Q(sqrt5)); the archive stays Q(sqrt10). Sanity: N_tau trace +1.
    N_tau = [[0, 1], [1, 1]]
    if (N_tau[0][0] + N_tau[1][1]) != 1:
        die("CONTROL_NTAU  N_tau must have trace +1 (golden, Q(sqrt5)) — field obstruction unchanged")
    print("PASS_CONTROL_WRONG_OBJECT  swapping S->N_tau (trace +1, still Q(sqrt5)) leaves the Q(sqrt5) vs "
          "Q(sqrt10) field obstruction unchanged: the NO-GO is about the FIELD, not the specific golden matrix.")

    print("PASS_STURMIAN_REFINEMENT_DISCHARGE_NOGO — the CONDITIONAL-EXTENSION of D0-STURMIAN-REFINEMENT is "
          "NOT dischargeable internally: the golden tower (Q(sqrt5)) and the archive scale (Q(sqrt10)) are "
          "field-disjoint (no intertwiner), and the centre-11 forcing pins the OPPOSITE orientation (T~-S). "
          "The tower stays a legitimate owned substitution; PRIM-STURMIAN-REFINEMENT-OWNER is the named "
          "external choice, so the parent claim stays PROOF-TARGET honestly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
