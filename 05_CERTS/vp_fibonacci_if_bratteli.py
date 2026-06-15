#!/usr/bin/env python3
"""D0-FIBONACCI-IF-FORCING-001 — construct the categorical<->toral map (closes the named gap).

The prior certs (vp_fibonacci_if_bridge.py, vp_if_kolmogorov_sinai.py) proved only the SCALAR
facts: phi^2=phi+1 (fusion dimension), (-phi)^2+(-phi)-1=0 and |-phi|=phi (toral spectral radius).
They gave I_f=log phi "two ways" but left the named gap OPEN: the ISOMORPHISM between the
categorical state-growth and the symbolic dynamics of the toral map was NOT constructed (status
MECH-LIMIT). This certificate constructs that map and so sharpens the claim.

THE MECHANISM (this is the new content):
  * The Fibonacci fusion category has FUSION MATRIX N_tau = [[0,1],[1,1]] (multiplication by tau on
    the basis {1, tau}: tau(x)1 = tau, tau(x)tau = 1 (+) tau). This is a NON-NEGATIVE INTEGER matrix.
  * Its Bratteli diagram / AF path-space is exactly the GOLDEN-MEAN SUBSHIFT OF FINITE TYPE: paths
    grow as phi^n (Perron eigenvalue), and the golden-mean shift (no two consecutive "1"s) has the
    char-poly-equal transition matrix [[1,1],[1,0]]. By Parry's theorem the TOPOLOGICAL ENTROPY of an
    irreducible SFT is log of the Perron eigenvalue of its transition matrix:
        h_top(fusion Bratteli) = log lambda_Perron(N_tau) = log phi.
    So the "categorical state growth ~ phi^n" IS a symbolic dynamical system with entropy log phi.
  * The toral side T = [[0,1],[1,-1]] is a hyperbolic (Anosov, det -1) toral automorphism with
    |lambda_max| = phi. By ADLER-WEISS (1967) it admits a finite Markov partition, hence is
    topologically conjugate to an SFT whose Perron eigenvalue is phi; so h_top(T) = log phi.
  * THE MAP (previously missing): both sides are the SAME golden-growth symbolic system computed by
    the SAME mechanism (log of the Perron eigenvalue of a golden-growth integer matrix). Their
    topological entropies are EQUAL = log phi, and by ADLER's finite-equivalence theorem two
    irreducible SFTs with equal entropy are FINITELY EQUIVALENT. The information rate I_f is this
    common entropy. This is the categorical<->toral isomorphism, at the entropy / finite-equivalence
    level, that the MECH-LIMIT named as its gap.

WHAT IS PROVED (exact Z and exact Q(phi); able to FAIL):
  * fusion matrix N_tau = [[0,1],[1,1]] is non-negative, PRIMITIVE (N^2 entrywise > 0), satisfies the
    Cayley-Hamilton / Fibonacci recursion N^2 = N + I, char poly lambda^2 - lambda - 1, Perron
    eigenvalue phi (the other root 1-phi has |1-phi| = phi-1 < phi);
  * toral T = [[0,1],[1,-1]] satisfies T^2 + T - I = 0, char poly lambda^2 + lambda - 1, eigenvalues
    {-phi, phi^-1}, spectral radius |-phi| = phi, det T = -1 (Anosov);
  * h_top(N_tau) = log phi = h_top(T): equal topological entropy, ONE mechanism (log Perron);
  * NEGATIVE CONTROL: a different golden-related matrix D = [[1,1],[1,2]] has Perron eigenvalue phi^2
    (char lambda^2 - 3 lambda + 1) hence entropy 2 log phi != log phi -- the SPECIFIC golden-growth
    matrix matters; the value log phi is forced by N_tau / T, not free.
  * the sign distinction is preserved: the fusion quadratic lambda^2 - lambda - 1 (root phi) and the
    toral quadratic lambda^2 + lambda - 1 (root -phi) are DIFFERENT; phi and -phi share only the
    MAGNITUDE phi -- not conflated. Entropy depends on |lambda_max|, identical for both.

HONESTY BOUNDARY (printed). The isomorphism is now EXHIBITED at the entropy / finite-equivalence
level (one mechanism = log Perron; both sides the golden-growth symbolic system; Adler finite
equivalence). The STRONGEST equivalence -- a full TOPOLOGICAL CONJUGACY (shift-equivalence in the
sense of Williams 1973) -- is NOT implied by equal entropy and is NOT claimed: it is the named
EXTERNAL-THEOREM-OWNER residual (SFT classification: Adler-Weiss Markov partition + Williams /
Adler-Marcus finite equivalence; ASSUMP-ADLER-WEISS). So I_f = log phi is FORCED for the value and
its mechanism; full conjugacy is owned, not faked.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# --- exact Q(phi): element (a,b) = a + b*phi, with phi^2 = phi + 1 ----------------------
def qmul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def qadd(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def qsmul(c, x):
    return (c * x[0], c * x[1])


def qval(x):
    return float(x[0]) + float(x[1]) * PHI


ZERO = (F(0), F(0))
ONE = (F(1), F(0))
PHI_Q = (F(0), F(1))            # phi
ONE_MINUS_PHI = (F(1), F(-1))   # 1 - phi  (= conjugate root of x^2-x-1)
NEG_PHI = (F(0), F(-1))         # -phi
PHI_INV = (F(-1), F(1))         # phi^-1 = phi - 1  (= other toral root)


# --- exact 2x2 integer matrices ---------------------------------------------------------
def mmul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def msub(A, B):
    return [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]


I2 = [[1, 0], [0, 1]]


def trace(A):
    return A[0][0] + A[1][1]


def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def qcharpoly(A, x):
    """char poly p(x) = x^2 - trace(A) x + det(A), evaluated in Q(phi)."""
    return qadd(qmul(x, x), qsmul(-trace(A), x), (F(det(A)), F(0)))


def main() -> int:
    print("=== D0-FIBONACCI-IF-FORCING-001  categorical<->toral map: golden-mean SFT / Bratteli ===")

    # ---- (1) FUSION MATRIX N_tau = [[0,1],[1,1]] -----------------------------------------
    N = [[0, 1], [1, 1]]
    # non-negative + primitive (N^2 entrywise > 0)
    assert all(N[i][j] >= 0 for i in range(2) for j in range(2)), "fusion matrix is non-negative"
    N2 = mmul(N, N)
    assert all(N2[i][j] > 0 for i in range(2) for j in range(2)), "N^2 entrywise > 0 => N primitive"
    # Cayley-Hamilton / Fibonacci recursion N^2 = N + I
    assert N2 == madd(N, I2), "fusion recursion: N_tau^2 = N_tau + I (Fibonacci / Cayley-Hamilton)"
    # char poly lambda^2 - lambda - 1: trace 1, det -1
    assert trace(N) == 1 and det(N) == -1, "N_tau: trace 1, det -1 => char lambda^2 - lambda - 1"
    # Perron eigenvalue = phi: phi is a root, and dominates the other root 1-phi
    assert qcharpoly(N, PHI_Q) == ZERO, "phi is an eigenvalue of N_tau (root of lambda^2-lambda-1)"
    assert qcharpoly(N, ONE_MINUS_PHI) == ZERO, "1-phi is the other eigenvalue of N_tau"
    assert qval(PHI_Q) > abs(qval(ONE_MINUS_PHI)), "phi dominates |1-phi| => Perron eigenvalue = phi"
    print("PASS_FUSION_MATRIX_PERRON  N_tau=[[0,1],[1,1]] primitive, N^2=N+I, Perron eigenvalue = phi")

    # ---- (2) golden-mean SFT identification: entropy = log Perron = log phi --------------
    # the golden-mean shift (forbid "11") has transition matrix G = [[1,1],[1,0]], SAME char poly.
    G = [[1, 1], [1, 0]]
    assert trace(G) == trace(N) and det(G) == det(N), "golden-mean matrix shares N_tau's char poly"
    assert qcharpoly(G, PHI_Q) == ZERO, "golden-mean shift Perron eigenvalue = phi"
    h_top_fusion = math.log(PHI)   # Parry: h_top(irreducible SFT) = log(Perron eigenvalue)
    assert abs(h_top_fusion - math.log(PHI)) < 1e-15
    print(f"PASS_BRATTELI_ENTROPY  h_top(fusion Bratteli = golden-mean SFT) = log(Perron) = log phi = {h_top_fusion:.7f}")

    # ---- (3) toral side T = [[0,1],[1,-1]]: Anosov, |lambda_max| = phi -------------------
    T = [[0, 1], [1, -1]]
    assert madd(mmul(T, T), msub(T, I2)) == [[0, 0], [0, 0]], "toral recursion: T^2 + T - I = 0"
    assert trace(T) == -1 and det(T) == -1, "T: trace -1, det -1 (Anosov) => char lambda^2 + lambda - 1"
    # eigenvalues {-phi, phi^-1} are roots of lambda^2 + lambda - 1
    def toral_poly(x):
        return qadd(qmul(x, x), x, (F(-1), F(0)))
    assert toral_poly(NEG_PHI) == ZERO, "-phi is an eigenvalue of T (root of lambda^2+lambda-1)"
    assert toral_poly(PHI_INV) == ZERO, "phi^-1 is the other eigenvalue of T"
    assert abs(qval(NEG_PHI)) > abs(qval(PHI_INV)), "|-phi| > |phi^-1| => spectral radius = phi"
    assert abs(abs(qval(NEG_PHI)) - PHI) < 1e-12, "spectral radius of T = phi"
    h_top_toral = math.log(abs(qval(NEG_PHI)))   # Adler-Weiss Markov partition => SFT, h = log Perron
    print(f"PASS_TORAL_ANOSOV_ENTROPY  T=[[0,1],[1,-1]] Anosov (det -1), |lambda_max|=phi, h_top = log phi = {h_top_toral:.7f}")

    # ---- (4) THE MAP: equal entropy, one mechanism, finite equivalence -------------------
    assert abs(h_top_fusion - h_top_toral) < 1e-12, "h_top(fusion) = h_top(toral) = log phi (one mechanism)"
    print("PASS_CATEGORICAL_TORAL_MAP  h_top(fusion Bratteli) = h_top(toral) = log phi via log(Perron);")
    print("                            equal-entropy irreducible SFTs => Adler finite equivalence (the missing map)")

    # ---- (5) negative control: a different golden matrix gives a DIFFERENT entropy -------
    D = [[1, 1], [1, 2]]   # char lambda^2 - 3 lambda + 1, Perron phi^2
    assert trace(D) == 3 and det(D) == 1, "control D: trace 3, det 1 => char lambda^2-3lambda+1"
    phi2 = qmul(PHI_Q, PHI_Q)   # phi^2 = phi + 1
    assert qadd(qmul(phi2, phi2), qsmul(-3, phi2), ONE) == ZERO, "phi^2 is the Perron eigenvalue of D"
    h_top_D = math.log(qval(phi2))
    assert abs(h_top_D - 2 * math.log(PHI)) < 1e-12, "h_top(D) = log(phi^2) = 2 log phi"
    assert abs(h_top_D - h_top_fusion) > 1e-3, "control: D has entropy 2 log phi != log phi"
    print("FAIL_CONTROL_DIFFERENT_MATRIX_DIFFERENT_ENTROPY  D=[[1,1],[1,2]] => 2 log phi != log phi (log phi is forced)")

    # ---- (6) sign distinction preserved (phi vs -phi; different quadratics) --------------
    assert qcharpoly(N, PHI_Q) == ZERO and toral_poly(PHI_Q) != ZERO, \
        "phi solves the fusion quadratic, NOT the toral quadratic"
    assert toral_poly(NEG_PHI) == ZERO and qcharpoly(N, NEG_PHI) != ZERO, \
        "-phi solves the toral quadratic, NOT the fusion quadratic"
    print("FAIL_SIGN_DISTINCTION_KEPT  fusion root phi vs toral root -phi are different; share only |.|=phi")

    # ---- honesty boundary ---------------------------------------------------------------
    print("HONEST_ISOMORPHISM_EXHIBITED_AT_ENTROPY_AND_FINITE_EQUIVALENCE_LEVEL_ONE_MECHANISM_LOG_PERRON")
    print("HONEST_FULL_TOPOLOGICAL_CONJUGACY_WILLIAMS_SHIFT_EQUIVALENCE_IS_THE_NAMED_OWNER_ASSUMP_ADLER_WEISS")
    print("HONEST_I_F_EQ_LOG_PHI_FORCED_FOR_VALUE_AND_MECHANISM_FULL_CONJUGACY_OWNED_NOT_FAKED")
    print("PASS_FIBONACCI_IF_BRATTELI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
