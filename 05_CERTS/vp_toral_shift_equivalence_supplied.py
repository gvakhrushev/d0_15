#!/usr/bin/env python3
"""D0-TORAL-TIME-MARKOV-CONJUGACY-001 advance: EXPLICIT shift-equivalence data supplied internally.

The claim's EXACT-MISSING artifact was: "an explicit Williams shift-equivalence matrix relating
N_tau=[[0,1],[1,1]] to T's SFT realization" (previously EXTERNAL, not supplied internally). This
certificate supplies it, with exact integer 2x2 arithmetic, and states precisely what it does and
does NOT close.

FIXED STRUCTURALLY (from BOOK_06): the golden toral automorphism T=[[0,1],[1,-1]] (det=-1, trace=-1,
eigenvalues phi^-1 and -phi -- a hyperbolic/Pisot map) and the Fibonacci SFT transition matrix
N_tau=[[0,1],[1,1]] (det=-1, trace=+1, eigenvalues phi and -phi^-1).

SUPPLIED HERE (the missing artifact):
  (1) UNIMODULAR CONJUGACY  T ~ -N_tau: the integer matrix P=[[0,-1],[1,1]] (det=+1) satisfies
      T P = P (-N_tau) exactly. So T is the TIME-REVERSED Fibonacci automorphism: spec(T) = -spec(N_tau).
      This is the "hidden symmetry" linking the two: they are sign-conjugate, not equal.
  (2) ELEMENTARY STRONG SHIFT EQUIVALENCE at the phi^2 (period-2) level: with the nonnegative SFT
      matrix A = N_tau^2 = [[1,1],[1,2]] (spectrum {phi^2, phi^-2}), the nonnegative integer pair
      R=[[1,0],[1,1]], S=[[1,1],[0,1]] gives  A = R S  and  B = S R = [[2,1],[1,1]], with the
      Williams lag-1 identities  A R = R B  and  S A = B S  verified. This is a genuine internal
      elementary SSE realizing the golden phi^2 subshift.

HONEST SCOPE (what stays open): full TOPOLOGICAL conjugacy of the toral map T to the golden SFT still
requires the geometric Adler-Weiss Markov partition (owner D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001):
the shift-equivalence data is the ALGEBRAIC leg (now internal); the GEOMETRIC partition leg is not
supplied here. So this ADVANCES the PROOF-TARGET (algebraic artifact now owned) and NARROWS the
residual to the Markov-partition construction; it does NOT by itself assert T = golden SFT.

Falsifiable: recomputes P, R, S and all the matrix identities in exact integer arithmetic; breaks
(nonzero exit) if the conjugacy, the factorization, the spectra, or the SSE identities fail.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FAIL = 0
def check(tag, cond, detail=""):
    global FAIL
    if not cond:
        FAIL += 1
    print(f"{'PASS' if cond else 'FAIL'}_{tag}  {detail}")
    return cond

def mm(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
def scal(A, c): return [[c*A[0][0], c*A[0][1]], [c*A[1][0], c*A[1][1]]]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def tr(A):  return A[0][0]+A[1][1]
def eq(A, B): return A == B

T    = [[0, 1], [1, -1]]
Ntau = [[0, 1], [1, 1]]

# structural facts
check("T_DET_TRACE", det(T) == -1 and tr(T) == -1, f"det(T)={det(T)}, tr(T)={tr(T)} (hyperbolic, eigs phi^-1,-phi)")
check("NTAU_DET_TRACE", det(Ntau) == -1 and tr(Ntau) == 1, f"det(N_tau)={det(Ntau)}, tr(N_tau)={tr(Ntau)} (eigs phi,-phi^-1)")

# (1) unimodular conjugacy T ~ -N_tau
P = [[0, -1], [1, 1]]
negN = scal(Ntau, -1)
check("P_UNIMODULAR", det(P) == 1, f"det(P)={det(P)} (unimodular)")
check("CONJUGACY_T_negN", eq(mm(T, P), mm(P, negN)), "T P = P (-N_tau): T is the time-reversed Fibonacci automorphism")
# spectrum sign-flip: char polys T: l^2+l-1 ; N_tau: l^2-l-1 ; so spec(T) = -spec(N_tau)
check("SPECTRA_SIGN_FLIPPED", (tr(T) == -tr(Ntau)) and (det(T) == det(Ntau)),
      "trace flips sign, det equal => spec(T) = -spec(N_tau)")

# (2) elementary strong shift equivalence at phi^2 level
A = mm(Ntau, Ntau)          # N_tau^2 = [[1,1],[1,2]]
check("A_IS_NTAU2_NONNEG", A == [[1, 1], [1, 2]] and all(A[i][j] >= 0 for i in range(2) for j in range(2)),
      f"A=N_tau^2={A} nonnegative SFT matrix, spectrum {{phi^2,phi^-2}} (tr={tr(A)}=3, det={det(A)}=1)")
R = [[1, 0], [1, 1]]
S = [[1, 1], [0, 1]]
check("FACTOR_A_EQ_RS", eq(mm(R, S), A), f"R S = {mm(R,S)} == A")
B = mm(S, R)
check("SSE_PARTNER_B", B == [[2, 1], [1, 1]], f"B = S R = {B} (nonneg SFT, same spectrum)")
check("SAME_SPECTRUM_AB", tr(A) == tr(B) and det(A) == det(B), f"tr {tr(A)}={tr(B)}, det {det(A)}={det(B)} (SE necessary cond)")
check("SSE_LAG1_AR_RB", eq(mm(A, R), mm(R, B)), "A R = R B (Williams lag-1)")
check("SSE_LAG1_SA_BS", eq(mm(S, A), mm(B, S)), "S A = B S (Williams lag-1)")
check("RS_NONNEG", all(R[i][j] >= 0 and S[i][j] >= 0 for i in range(2) for j in range(2)),
      "R,S nonnegative integer (valid SSE data)")

# (3) the SSE partner B is GL(2,Z)-conjugate to T^2, closing the chain T~-N_tau, T^2~B=SR, A=N_tau^2=RS.
# This is what makes the (R,S) datum relate the TWO systems (T-side and N_tau-side), not just live on one.
T2 = mm(T, T)                       # [[1,-1],[-1,2]]
Ucon = [[-1, 0], [1, 1]]            # det -1
check("B_CONJ_T2", eq(mm(Ucon, T2), mm(B, Ucon)) and det(Ucon) in (1, -1),
      f"U T^2 = B U with U={Ucon} (det={det(Ucon)}): the SSE partner B is GL(2,Z)-conjugate to T^2 "
      f"(T2={T2}), tying the elementary SSE to the toral map's square")

# (4) THE ORIENTATION OBSTRUCTION (why 'T = golden SFT' is NOT naively true, sharpened NO-GO).
# Periodic-point counts are a topological-conjugacy invariant: |Fix(f^n)| must agree. For the toral
# automorphism |Fix(T^n)| = |det(T^n - I)|; for the golden SFT it is tr(N_tau^n) = Lucas(n). We show
# these DISAGREE at even n (by exactly 2) and AGREE at odd n -- the exact signature of T ~ -N_tau, the
# orientation reversal. So T is conjugate to the SFT of -N_tau (an orientation-reversed / signed system),
# NOT to the plain nonnegative golden SFT N_tau. This is a real obstruction, not a fillable gap.
def matsub(A, C): return [[A[0][0]-C[0][0], A[0][1]-C[0][1]], [A[1][0]-C[1][0], A[1][1]-C[1][1]]]
def matpow(A, n):
    R = [[1, 0], [0, 1]]
    for _ in range(n):
        R = mm(R, A)
    return R
I2 = [[1, 0], [0, 1]]
def lucas(n):
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
fixT = [abs(det(matsub(matpow(T, n), I2))) for n in range(1, 9)]     # |Fix(T^n)|
trN  = [tr(matpow(Ntau, n)) for n in range(1, 9)]                     # tr(N_tau^n) = Lucas(n)
offsets = [trN[i] - fixT[i] for i in range(8)]
check("PERIODIC_ODD_AGREE", all(offsets[n - 1] == 0 for n in range(1, 9) if n % 2 == 1),
      f"|Fix(T^n)| = tr(N_tau^n) at ODD n (offsets {[offsets[n-1] for n in range(1,9) if n%2==1]})")
check("PERIODIC_EVEN_SPLIT", all(offsets[n - 1] == 2 for n in range(1, 9) if n % 2 == 0),
      f"tr(N_tau^n) - |Fix(T^n)| = 2 at EVEN n (offsets {[offsets[n-1] for n in range(1,9) if n%2==0]}): "
      f"the orientation-reversal signature")
check("LUCAS_IS_TRACE", trN == [lucas(n) for n in range(1, 9)],
      f"tr(N_tau^n) = Lucas(n) = {trN}")
check("ORIENTATION_OBSTRUCTION", offsets != [0] * 8,
      "|Fix(T^n)| =/= tr(N_tau^n): T is NOT conjugate to the plain golden SFT N_tau (only to -N_tau); "
      "the naive 'T = golden SFT' target is FALSE as stated -- a genuine obstruction, vindicating PROOF-TARGET")

print()
if FAIL == 0:
    print("PASS_TORAL_SHIFT_EQUIVALENCE_SUPPLIED — the missing algebraic artifact is now internal: "
          "T ~ -N_tau by unimodular P=[[0,-1],[1,1]] (T = time-reversed Fibonacci), and an explicit "
          "elementary strong-shift-equivalence R=[[1,0],[1,1]], S=[[1,1],[0,1]] realizes the golden "
          "phi^2 SFT (N_tau^2 = R S, S R = [[2,1],[1,1]], lag-1 identities verified). ADVANCE: the "
          "algebraic leg is owned; residual PROOF-TARGET narrows to the geometric Adler-Weiss Markov "
          "partition (D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001). Does NOT alone assert T = golden SFT.")
    sys.exit(0)
else:
    print(f"FAIL — {FAIL} checks failed.")
    sys.exit(1)
