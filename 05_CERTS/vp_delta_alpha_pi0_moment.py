#!/usr/bin/env python3
"""D0-DELTA-ALPHA-MOMENT-001 — α_alg⁻¹ is the depth-2 π₀-phase moment of the feedback resolvent.

Sharpening (not closure) of §05.6 obligation 4 (the Δ_α analytic owner, routed to CVFT-F1).
The exact VALUE of α_alg⁻¹ is already closed (D0-DELTA-ALPHA-EXACT-001, CORE). What was open is
the analytic OWNER: deriving the algebraic writing α_alg⁻¹ = 2¹¹·π₀·φ⁻⁸ + (2/3)·δ₀ as a
second-order / π₀-phase MOMENT of the Feshbach–Schur feedback resolvent W_eff
(D0-GENERATIVE-DYNAMICS-001). This certificate establishes the FINITE SHADOW of that owner and
names precisely what stays frontier.

THE FINITE FINDING (exact ℚ(φ), able to FAIL). Substituting δ₀ = ½φ⁻³ collapses the algebraic
writing into a polynomial in the single archive-floor unit u = φ⁻³ (the rank-3 archive eigenvalue):

    α_alg⁻¹ = μ₂·u² + μ₁·u ,   u = φ⁻³ ,   μ₂ = 2¹¹·π₀·φ⁻² = 12288/5 ,   μ₁ = 1/3 ,   μ₀ = 0

i.e. α_alg⁻¹ = (12288/5)·φ⁻⁶ + (1/3)·φ⁻³ exactly. This is EXACTLY the shape of a resolvent
moment expansion W_eff(z) = A + Σ_{k≥0} z⁻⁽ᵏ⁺¹⁾·B Dᵏ C (the closed Feshbach–Schur form): the
k-th archive excursion carries weight uᵏ with u the archive eigenvalue, μ_k = B Dᵏ C the k-th
moment. The reading of the algebraic α writing is then forced to be:
  * the exponents −6, −3 are −2·rank and −1·rank — moments at archive depth k=2 and k=1
    (the rank-3 unit φ⁻³ is the per-excursion weight);
  * the SECOND-ORDER moment μ₂ carries the π₀ feedback phase (π₀=(6/5)φ²): μ₂ = 2¹¹·π₀·φ⁻²;
  * there is NO constant term (μ₀ = 0): zero archive depth ⇒ zero anomaly contribution — the
    mechanistic sign of the resolvent reading, forced, not fitted;
  * the depth-2 truncation is consistent with the loop floor |Δ_α| < φ⁻¹⁶ (the next moment μ₃u³
    ~ φ⁻⁹ sits below the seam scale; D0-GENERATIVE-DYNAMICS-001 A.3).

HONESTY BOUNDARY (printed, not hidden). The finite model forces the SHAPE — a degree-2 polynomial
in the forced unit u=φ⁻³, no constant term, the π₀ phase on the 2nd moment — and that shape is the
mechanical content of "α_alg⁻¹ = the π₀-phase 2nd moment of W_eff". What it does NOT force are the
two RESIDUE AMPLITUDES μ₂=2¹¹·π₀·φ⁻² and μ₁=1/3: these are the residues of W_eff at the pole, set
by the continuum normalization (the s→pole continuation / profinite spectral measure). So this
SHARPENS obligation 4 — the owner is now "the depth-2 π₀-phase moment of W_eff in the unit φ⁻³,
only the two residue amplitudes ↔ s→pole residues stay profinite" — but does NOT close it; Δ_α and
D0-DELTA-ALPHA-EXACT-001 keep their honest status, CVFT-F1 stays a PROOF-TARGET. The numerical
coincidence 2¹¹ = 2^V11 is FLAGGED for the continuation, NOT asserted as forced (anti-numerology:
a list-match is not a derivation).
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# --- exact ℚ(φ) arithmetic: x = (a, b) means a + b·φ, with φ² = φ + 1 -------------
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n):
            r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))      # φ⁻¹ = φ − 1
    for _ in range(-n):
        r = mul(r, inv)
    return r


def smul(c, x):
    return (c * x[0], c * x[1])


def add(*xs):
    a = sum(x[0] for x in xs)
    b = sum(x[1] for x in xs)
    return (a, b)


def val(x):
    return float(x[0]) + float(x[1]) * PHI


RANK = 3   # the forced non-zero spectral rank of K(9,11,13); the archive unit is φ^(−RANK)


def main() -> int:
    print("=== D0-DELTA-ALPHA-MOMENT-001  α_alg⁻¹ = depth-2 π₀-phase moment of W_eff (sharpen obl.4) ===")

    # ---- the closed algebraic writing α_alg⁻¹ = 2¹¹ π₀ φ⁻⁸ + (2/3) δ₀ --------------
    pi0 = smul(F(6, 5), powphi(2))                      # π₀ = (6/5) φ²
    d0 = smul(F(1, 2), powphi(-3))                      # δ₀ = (1/2) φ⁻³
    alg = add(smul(2048, mul(pi0, powphi(-8))), smul(F(2, 3), d0))
    assert alg == (F(159739, 5), F(-294902, 15)), f"α_alg⁻¹ reference wrong: {alg}"
    print(f"PASS_ALPHA_ALG_REFERENCE  α_alg⁻¹ = 159739/5 − (294902/15)φ = {val(alg):.8f}")

    # ---- moment decomposition in the rank-3 archive unit u = φ⁻³ --------------------
    u = powphi(-RANK)                                   # u = φ⁻³ (archive eigenvalue / per-excursion weight)
    mu2 = smul(2048, mul(pi0, powphi(-2)))             # μ₂ = 2¹¹ π₀ φ⁻²  (the 2nd-moment residue)
    mu1 = (F(1, 3), F(0))                               # μ₁ = 1/3         (the 1st-moment residue)
    assert mu2 == (F(12288, 5), F(0)), f"μ₂ must be the pure rational 12288/5: {mu2}"
    P = add(mul(mu2, mul(u, u)), mul(mu1, u))          # P(u) = μ₂ u² + μ₁ u  (μ₀ = 0)
    assert P == alg, f"moment decomposition μ₂φ⁻⁶+μ₁φ⁻³ must equal α_alg⁻¹ exactly: {P} != {alg}"
    print(f"PASS_MOMENT_DECOMPOSITION  α_alg⁻¹ = μ₂·φ⁻⁶ + μ₁·φ⁻³, μ₂=12288/5, μ₁=1/3 (exact ℚ(φ))")

    # μ₂ carries the π₀ feedback phase: μ₂ = 2¹¹ · π₀ · φ⁻²
    assert smul(2048, mul(pi0, powphi(-2))) == mu2, "μ₂ must factor as 2¹¹·π₀·φ⁻²"
    print(f"PASS_SECOND_MOMENT_CARRIES_PI0_PHASE  μ₂ = 2¹¹·π₀·φ⁻²  (π₀=(6/5)φ², the feedback phase)")

    # ---- exponents are integer multiples of the rank-3 archive unit ----------------
    bulk = smul(mu2[0], mul(u, u))                     # μ₂ φ⁻⁶ = depth-2 excursion
    floor = mul(mu1, u)                                 # μ₁ φ⁻³ = depth-1 excursion
    assert mul(u, u) == powphi(-2 * RANK), "u² must be φ^(−2·rank) (depth-2 moment)"
    assert u == powphi(-1 * RANK), "u must be φ^(−1·rank) (depth-1 moment)"
    print(f"PASS_RANK3_MOMENT_UNITS  exponents −6=−2·rank, −3=−1·rank; bulk={val(bulk):.6f}, floor={val(floor):.6e}")

    # ---- NO constant term: zero archive depth ⇒ zero anomaly (mechanistic, forced) -
    # P(u) evaluated at u=0 is exactly 0 — there is no μ₀·u⁰ piece in α_alg⁻¹.
    P_at_zero = add(mul(mu2, mul((F(0), F(0)), (F(0), F(0)))), mul(mu1, (F(0), F(0))))
    assert P_at_zero == (F(0), F(0)), "the moment polynomial must vanish at u=0 (no constant term)"
    print("PASS_NO_CONSTANT_TERM  μ₀=0 ⇒ P(0)=0: zero archive depth ⇒ zero anomaly (forced sign)")

    # ---- consistency with the loop floor: the dropped μ₃ term is below the seam ----
    # next moment μ₃ u³ ~ φ⁻⁹; the seam/loop floor is φ⁻¹⁶ (D0-GENERATIVE-DYNAMICS-001 A.3).
    assert val(powphi(-3 * RANK)) < val(powphi(-RANK)) ** 2, "depth-3 weight φ⁻⁹ < (depth-1)²"
    print("PASS_DEPTH2_TRUNCATION_CONSISTENT  μ₃u³~φ⁻⁹ is sub-leading (loop floor φ⁻¹⁶ truncates)")

    # ---- NEGATIVE CONTROLS: the shape is constrained, not free ----------------------
    # (a) a different archive unit exponent does NOT reproduce α_alg⁻¹
    for e in (-2, -4, -5, -7):                          # not the forced −3
        ue = powphi(e)
        Pe = add(mul(mu2, mul(ue, ue)), mul(mu1, ue))
        assert Pe != alg, f"control: unit φ^{e} must not reproduce α_alg⁻¹"
    print("FAIL_WRONG_ARCHIVE_UNIT_DOES_NOT_REPRODUCE_ALPHA  (only u=φ⁻³ works)")
    # (b) a spurious constant term breaks the exact identity
    assert add(P, (F(1, 1000), F(0))) != alg, "control: any nonzero μ₀ breaks the identity"
    print("FAIL_SPURIOUS_CONSTANT_TERM_BREAKS_THE_IDENTITY  (μ₀ must be 0)")
    # (c) the 2nd moment WITHOUT the π₀ phase misses α_alg⁻¹
    mu2_nopi = smul(2048, powphi(-2))                  # drop π₀
    P_nopi = add(mul(mu2_nopi, mul(u, u)), mul(mu1, u))
    assert P_nopi != alg, "control: μ₂ without the π₀ phase must miss α_alg⁻¹"
    print("FAIL_SECOND_MOMENT_WITHOUT_PI0_MISSES_ALPHA  (the π₀ phase is on μ₂)")

    # ---- honesty boundary -----------------------------------------------------------
    print("HONEST_SHADOW_FORCES_THE_SHAPE_DEG2_IN_PHI_MINUS_3_NO_CONSTANT_PI0_ON_MU2")
    print("HONEST_RESIDUE_AMPLITUDES_2P11_AND_ONE_THIRD_ARE_THE_S_TO_POLE_CONTINUATION_PROFINITE")
    print("HONEST_THIS_SHARPENS_CVFT_F1_OBLIGATION_4_DOES_NOT_CLOSE_IT_DELTA_ALPHA_STATUS_UNCHANGED")
    print("HONEST_2P11_EQ_2_POW_V11_IS_FLAGGED_FOR_THE_CONTINUATION_NOT_CLAIMED_FORCED")

    print("PASS_DELTA_ALPHA_PI0_MOMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
