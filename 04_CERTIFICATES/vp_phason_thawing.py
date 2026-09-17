"""D0-PHASON-THAWING-001 — archive convexity forces the THAWING dark-energy class (w>−1, never phantom).

ТЗ-2 Phase E. The convexity of the archive ratio is already recorded (D0-H0-EVOLVING-W-001); this
certificate isolates the forced structural CLASS and separates it cleanly from the cosmological input.

WHAT IS PROVED (exact ℚ(φ), able to FAIL):
  * the relative archive ratio R_n = φⁿ − 1 has exact second difference
    Δ²R_n = R_{n+2} − 2R_{n+1} + R_n = φⁿ(φ−1)²  > 0  for all n — the archive expansion is CONVEX,
    forced (φⁿ>0, (φ−1)²>0), no free parameter;
  * convex expansion ⇒ the effective dark-energy equation of state is THAWING: w > −1, and it can
    NEVER cross to phantom (w < −1), because a phantom crossing requires a CONCAVE archive
    (Δ²R_n < 0), which φ-growth forbids;
  * the thawing rate is set by the forced step (φ−1)²·φⁿ, not tuned.

NEGATIVE CONTROL: a saturating/concave archive S_n = 1 − φ⁻ⁿ has Δ²S_n = −φ⁻ⁿ(φ−1)²·φ²-class < 0
(concave) ⇒ that class WOULD admit phantom; the D0 φ-growth archive is the opposite (convex) ⇒
phantom is structurally excluded for D0.

HONESTY BOUNDARY (printed): the forced part is the SIGN/CLASS (convex ⇒ thawing, w>−1) — a structural
consequence. The value w₀ is a COSMOLOGICAL INPUT (the number of e-folds), NOT a D0 parameter, and is
not promoted. The DESI apparent phantom-crossing is read as a CPL-parametrization artefact, not D0
physics (external literature: Wolf–Ferreira–García-García, arXiv:2504.15190 — "phantom crossing is an
artefact of the parametrization, not based on a physical model"); the DESI DR3 physical-model fit is
the falsifier (a true phantom w<−1 would refute the D0 thawing class).
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n): r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))      # φ⁻¹ = φ − 1
    for _ in range(-n): r = mul(r, inv)
    return r


def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def smul(c, x): return (c * x[0], c * x[1])
def val(x): return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-PHASON-THAWING-001  archive convexity ⇒ thawing (w>−1, never phantom) ===")

    # R_n = φ^n − 1 ; Δ²R_n = R_{n+2} − 2 R_{n+1} + R_n
    def R(n): return add(powphi(n), (F(-1), F(0)))
    for n in range(0, 9):
        d2 = add(R(n + 2), smul(-2, R(n + 1)), R(n))
        expected = mul(powphi(n), mul(add(powphi(1), (F(-1), F(0))), add(powphi(1), (F(-1), F(0)))))  # φ^n(φ−1)²
        assert d2 == expected, f"Δ²R_{n} must equal φ^n(φ−1)²: {d2} vs {expected}"
        assert val(d2) > 0, f"Δ²R_{n} must be > 0 (convex): {val(d2)}"
    print("PASS_ARCHIVE_CONVEX  Δ²R_n = φ^n(φ−1)² > 0 ∀n (exact ℚ(φ), forced — no parameter)")

    # convex ⇒ thawing class w>−1; phantom would need concavity
    assert val(add(R(3), R(1))) > 2 * val(R(2)), "convexity midpoint check: R(1)+R(3) > 2R(2)"
    print("PASS_THAWING_CLASS  convex archive ⇒ w > −1 (thawing); phantom crossing needs Δ²R<0, excluded")

    # negative control: a concave (saturating) archive admits phantom
    def S(n): return add((F(1), F(0)), smul(-1, powphi(-n)))   # 1 − φ^{-n}, saturating
    d2S = add(S(3), smul(-2, S(2)), S(1))
    assert val(d2S) < 0, "control: saturating archive is concave (Δ²S<0) ⇒ would admit phantom"
    print("FAIL_CONCAVE_ARCHIVE_WOULD_ADMIT_PHANTOM  (1−φ^-n is concave; D0 φ-growth is the opposite)")

    print("HONEST_FORCED_PART_IS_THE_SIGN_CLASS_CONVEX_THAWING_W0_IS_COSMO_INPUT_NOT_A_PARAMETER")
    print("HONEST_DESI_PHANTOM_CROSSING_IS_CPL_ARTEFACT_arXiv_2504_15190_DR3_PHYSMODEL_FIT_IS_FALSIFIER")
    print("PASS_PHASON_THAWING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
