#!/usr/bin/env python3
"""D0-PACKING-LIMIT-001 — probe: is gamma_Choptuik = C_max = 3/8 one packing limit? (HYP)

Self-calibrated status: HYP with a NAMED GAP, NOT a forcing and NOT a declared bridge. The
deep-research claim "gamma_Choptuik <-> C=3/8 are one packing limit" was downgraded by the
LIMITS filter: a coincidence at a single point (D=4) is NOT an identity. This probe RUNS the
test honestly and records the verdict; both possible outcomes are results, not failures.

THE TEST. In D0, mass = winding = packing and geometry = packing, so IF gamma and C were one
packing limit there should be a function F(D) projecting to both. We check whether C_max=3/8
is a LIMIT of the critical exponent gamma(D), or only numerically close at D=4.

NUMBERS (one table):
  * gamma_Choptuik(D=4) = 0.373961, gamma(D=5) = 0.41322   (Ecker-Ecker-Grumiller PRL 136
    191401 (2026) + arXiv:2602.10185; massless-scalar critical collapse).
  * C_max = 3/8 = 0.375 (caustic/causal compactness ceiling; Jampolski-Rezzolla PRD 113
    L121502 (2026); D0: 3/8 = rank/|Omega8|).
  * Bekenstein S = A/4 (coefficient 1/4; Bekenstein 1981) -- supports "capacity is finite",
    a separate (weaker) statement, not a packing-limit identity.

VERDICT (computed, able to FAIL):
  * gamma(D=4) matches 3/8 to 0.28% (the coincidence is real and worth recording).
  * BUT gamma(D=5) is >10% from 3/8 and gamma INCREASES with D (gamma(5)>gamma(4)>3/8), i.e.
    gamma moves AWAY from 3/8 as D grows -- so 3/8 is NOT lim_{D->inf} gamma. The two are
    distinct quantities that happen to nearly coincide at D=4.
  * Therefore the "single packing limit" bridge is NOT established. Honest status: HYP. The
    named gap: derive a common mechanism F(D) projecting to both gamma(D=4) and C_max (e.g.
    two different slices of one archive-capacity function rank/|Omega8|), or accept the D=4
    coincidence and reject the unified-limit reading. NOT declared a bridge without that
    derivation.

HONESTY BOUNDARY (printed): coincidence at one point != identity; this is the same discipline
applied to 710/113. The D=4 match is real and interesting; the unified limit is unproven.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GAMMA = {4: 0.373961, 5: 0.41322}     # Choptuik critical exponents (Ecker et al.)
C_MAX = 3.0 / 8.0                      # 0.375, exact rational 3/8
C_MAX_EXACT = F(3, 8)
BEKENSTEIN_COEFF = F(1, 4)            # S = A/4


def rel(a, b):
    return abs(a - b) / abs(b)


def main() -> int:
    print("=== D0-PACKING-LIMIT-001  packing-limit probe: gamma vs 3/8 (HYP) ===")

    # exact 3/8 anchor (already owned by D0-COMPACTNESS-DEF-FORCING-001)
    assert C_MAX_EXACT == F(3, 8) and abs(float(C_MAX_EXACT) - C_MAX) < 1e-15, "3/8 anchor"
    print(f"PASS_CMAX_EXACT  C_max = 3/8 = {C_MAX:.6f} (rank/|Omega8|, exact rational)")

    # the D=4 coincidence is REAL (within 1%)
    d4 = rel(GAMMA[4], C_MAX)
    assert d4 < 0.01, f"gamma(4) should be within 1% of 3/8: {d4:.4%}"
    print(f"PASS_D4_COINCIDENCE_REAL  |gamma(4)-3/8|/(3/8) = {d4:.4%} (~0.28%, genuine near-hit)")

    # but gamma DIVERGES from 3/8 at D=5 (>5%) and INCREASES with D -> 3/8 is NOT a limit:
    # gamma(D) is monotone-increasing and CROSSES 3/8 between D=4 and D=5 (gamma(4)<3/8<gamma(5)),
    # so 3/8 is a crossing point near D=4, not lim_{D->inf} gamma.
    d5 = rel(GAMMA[5], C_MAX)
    assert d5 > 0.05, f"gamma(5) must be far (>5%) from 3/8 to show divergence: {d5:.4%}"
    assert GAMMA[5] > GAMMA[4], "gamma increases with D (monotone)"
    assert GAMMA[4] < C_MAX < GAMMA[5], "3/8 is CROSSED between D=4 and D=5, not approached as a limit"
    print(f"FAIL_3_8_IS_NOT_A_LIMIT_OF_GAMMA  |gamma(5)-3/8|/(3/8) = {d5:.4%}; gamma(4)<3/8<gamma(5) (crossing, not limit)")

    # no common F(D) is derived here: the two are distinct quantities (one a critical exponent,
    # one a geometric ceiling) -- the unified-limit bridge is NOT established
    unified_limit_derived = False
    assert not unified_limit_derived, "must NOT declare a unified packing limit without derivation"
    print("FAIL_UNIFIED_PACKING_LIMIT_NOT_DERIVED  (D=4 coincidence, not a shared limit)")

    # Bekenstein 1/4 is a separate (capacity-finite) statement, not the packing-limit identity
    assert BEKENSTEIN_COEFF == F(1, 4) and BEKENSTEIN_COEFF != C_MAX_EXACT, "1/4 != 3/8"
    print("PASS_BEKENSTEIN_SEPARATE  S=A/4 supports 'capacity finite', not the 3/8 packing limit")

    # honest verdict
    print("HONEST_COINCIDENCE_AT_D4_IS_NOT_IDENTITY_STATUS_HYP_NOT_BRIDGE")
    print("HONEST_NAMED_GAP_DERIVE_COMMON_F_OF_D_OR_ACCEPT_D4_COINCIDENCE")
    print("HONEST_SAME_DISCIPLINE_AS_710_113_DO_NOT_PASS_COINCIDENCE_AS_DERIVATION")

    print("PASS_PACKING_LIMIT_PROBE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
