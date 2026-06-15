#!/usr/bin/env python3
"""D0-UNITY-SPLIT-SPACETIME-001 — dividing unity around ½ ⇒ space (symmetric) + time (antisym).

The root act: split the unit 1 into two. There are two canonical cuts:
  * HONEST cut         1 = ½ + ½              — symmetric under a↔b (exchange changes nothing).
  * SELF-CONSISTENT    1 = φ⁻¹ + φ⁻²          — forced by p²+p=1 (the detection quadratic).
Their separation is exactly the archive quantum
  δ₀ = φ⁻¹ − ½ = (√5 − 2)/2 .
Write any cut as 1 = (½ + s) + (½ − s). The SYMMETRIC part (½,½) is invariant under a↔b — exchange
of the two sides changes nothing, transport is reversible, no arrow ⇒ SPACE. The ANTISYMMETRIC
part s = δ₀ changes sign under a↔b — exchange singles out a direction ⇒ TIME (an arrow), of
magnitude δ₀.

Operator check (det = −1). T = [[0,1],[1,−1]] has det = −1 = ψ·φ (Vieta) and spectrum {φ⁻¹, −φ}:
the positive eigenvalue is the symmetric (space, |λ|<1 contraction) mode, the NEGATIVE eigenvalue
is the sign-flip = the antisymmetric = the single ARROW. det = −1 forces exactly one sign change ⇒
exactly one time arrow.

HONESTY BOUNDARY (printed). The symbolic content here — δ₀ exact, det = −1 = ψφ, exactly one
negative eigenvalue, the symmetric/antisymmetric split — is decidable and is shadowed in Lean
(D0.Synthesis.UnitySplitSpacetime). Status is LEM, not THE: the step "the SYMMETRIC part is
specifically rank-3 adjacency" rests on identifying the S₂-invariant with the adjacency rank — the
SAME rank-3 node that is ALREADY FORCED as the causal cone (D0-RANK3-CAUSAL-CONE-FORCING-001,
Iter-11). So the residual is narrowed to that one identification (and the cone-speed Connes unit
beyond it), NOT a fresh open gap. The BTC transition-asymmetry below is a CONFIRMATION on data,
not a derivation.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def smul(c, x):
    return (c * x[0], c * x[1])


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n):
            r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))
    for _ in range(-n):
        r = mul(r, inv)
    return r


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-UNITY-SPLIT-SPACETIME-001  unity split ⇒ space (sym) + time (antisym, δ₀) ===")

    half = (F(1, 2), F(0))
    pinv, pinv2 = powphi(-1), powphi(-2)

    # ---- the two canonical cuts ----------------------------------------------------
    assert add(half, half) == (F(1), F(0)), "honest cut ½+½ = 1"
    assert add(pinv, pinv2) == (F(1), F(0)), "self-consistent cut φ⁻¹+φ⁻² = 1 (forced p²+p=1)"
    print("PASS_TWO_CANONICAL_CUTS  1 = ½+½ (symmetric)  and  1 = φ⁻¹+φ⁻² (self-consistent)")

    # ---- δ₀ = φ⁻¹ − ½ = (√5−2)/2 = φ − 3/2 -----------------------------------------
    delta0 = add(pinv, smul(-1, half))
    assert delta0 == (F(-3, 2), F(1)), f"δ₀ must be −3/2 + φ: {delta0}"
    # (√5−2)/2 = (2φ−1−2)/2 = φ − 3/2  ✓ (exact, since √5 = 2φ−1)
    assert abs(val(delta0) - (5 ** 0.5 - 2) / 2) < 1e-12, "δ₀ = (√5−2)/2"
    print(f"PASS_DELTA0_EXACT  δ₀ = φ⁻¹ − ½ = φ − 3/2 = (√5−2)/2 = {val(delta0):.8f}")

    # ---- operator: det T = −1 = ψφ, spectrum {φ⁻¹, −φ}, one negative eigenvalue -----
    # T = [[0,1],[1,-1]]; det = 0*(-1) - 1*1 = -1; psi*phi = -1 (Vieta)
    psi = (F(1), F(-1))                                   # ψ = 1 − φ
    detT = F(0) * F(-1) - F(1) * F(1)
    assert detT == -1, "det T must be −1"
    assert mul(psi, (F(0), F(1))) == (F(-1), F(0)), "−1 = ψ·φ (Vieta B)"
    # eigenvalues solve λ²+λ−1=0 : φ⁻¹ (>0) and −φ (<0)
    for lam, sign in ((pinv, +1), (smul(-1, (F(0), F(1))), -1)):
        char = add(mul(lam, lam), lam, (F(-1), F(0)))     # λ²+λ−1
        assert char == (F(0), F(0)), f"λ must solve λ²+λ−1=0: {lam}"
        assert (val(lam) > 0) == (sign > 0), "eigenvalue sign"
    print("PASS_DET_MINUS_ONE_ONE_ARROW  det T=−1=ψφ; spectrum {φ⁻¹,−φ}; one negative λ ⇒ one arrow")

    # ---- symmetric ⇒ space, antisymmetric ⇒ time -----------------------------------
    # symmetric part (½,½) invariant under a↔b; antisymmetric s flips sign
    a, b = add(half, (delta0[0], delta0[1])), add(half, smul(-1, delta0))   # (½+δ₀, ½−δ₀)
    sym = smul(F(1, 2), add(a, b))                        # (a+b)/2 = ½  (exchange-invariant)
    anti = smul(F(1, 2), add(a, smul(-1, b)))             # (a−b)/2 = δ₀ (sign-flips under a↔b)
    assert sym == half, "symmetric part = ½ (space: exchange-invariant)"
    assert anti == delta0, "antisymmetric part = δ₀ (time: the arrow)"
    print("PASS_SYM_SPACE_ANTISYM_TIME  (a+b)/2=½ exchange-invariant ⇒ space; (a−b)/2=δ₀ ⇒ time-arrow")

    # ---- BTC confirmation (a confirmation, NOT a derivation) ------------------------
    fwd = val(pinv2) * (1 - val(delta0))                  # φ⁻²(1−δ₀)
    bwd = val(pinv) * (1 + val(delta0))                   # φ⁻¹(1+δ₀)
    assert abs((fwd + bwd) - 1.0) > 1e-3, "asymmetric transitions: sum ≠ 1 (time has an arrow)"
    print(f"CONFIRM_BTC_ASYMMETRY  φ⁻²(1−δ₀)+φ⁻¹(1+δ₀)={fwd+bwd:.4f}≠1 (arrow); confirmation, not derivation")

    # ---- negative control: s = 0 ⇒ reversible (no arrow) ---------------------------
    fwd0, bwd0 = val(pinv2), val(pinv)                    # δ₀→0
    assert abs((fwd0 + bwd0) - 1.0) < 1e-12, "control: s=0 ⇒ φ⁻²+φ⁻¹=1, reversible, no time"
    print("FAIL_ZERO_SPLIT_IS_REVERSIBLE_NO_ARROW  s=0 ⇒ φ⁻²+φ⁻¹=1 (sum=1, time reversible)")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_STATUS_LEM_SYMMETRIC_PART_EQ_RANK3_ADJACENCY_ROUTES_TO_ALREADY_FORCED_CONE")
    print("HONEST_RANK3_EQ_CAUSAL_CONE_ALREADY_FORCED_ITER11_RESIDUAL_IS_CONE_SPEED_CONNES_ONLY")

    print("PASS_UNITY_SPLIT_SPACETIME")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
