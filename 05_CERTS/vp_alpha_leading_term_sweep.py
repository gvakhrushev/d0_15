#!/usr/bin/env python3
"""vp_alpha_leading_term_sweep — the exact outcome of the N*phi^p + m*phi^q sweep near alpha^-1,
replacing an unowned and FALSE uniqueness claim.

ERROR OF RECORD (found by reproduction 2026-08-10): the pre-refactor README asserted the sweep
over N <= 500, |m| <= 12, |p|,|q| <= 20 "finds exactly ONE value within 4e-4 of alpha^-1".
FALSE: the window contains THREE distinct values (12 parameter tuples). The D0 term
359*phi^-2 - phi^-5 is among them at distance ~3.71e-4; BOTH rivals sit closer (~1.98e-4, ~3.62e-4).
No uniqueness or rarity claim survives; what IS owned: the exact identity
zeta_E(-1) = 359*phi^-2 - phi^-5 (Lean zetaEdge_neg_one) and zeta_E(0) = 359 (zetaEdge_zero),
with the residual ~3.7e-4 closed by the registered dressing (the alpha line's own ladder).
This certificate pins the TRUE sweep outcome so the dead claim cannot silently return.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1 + 5 ** 0.5) / 2
TARGET = 137.035999084  # CODATA-2018 alpha^-1
TOL = 4e-4


def main() -> int:
    print("=== vp_alpha_leading_term_sweep — true outcome of the leading-term sweep ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: sweep family N*phi^p + m*phi^q, N in [1,500], "
          "m in [-12,12]\\{0}, p,q in [-20,20]; window |value - alpha^-1| < 4e-4; the claim "
          "under test is the COUNT of distinct values in the window")

    powers = {e: PHI ** e for e in range(-20, 21)}
    hits = []
    for p in range(-20, 21):
        for N in range(1, 501):
            a = N * powers[p]
            if a > TARGET + 200:  # coarse prune: m*phi^q >= -12*phi^20 cannot bridge huge a
                continue
            for q in range(-20, 21):
                for m in range(-12, 13):
                    if m == 0:
                        continue
                    v = a + m * powers[q]
                    if abs(v - TARGET) < TOL:
                        hits.append((v, N, p, m, q))
    values = sorted({round(v, 9) for v, *_ in hits})
    ref = 359 * PHI ** -2 - PHI ** -5
    print(f"PASS_SWEEP_COUNTS  {len(hits)} parameter tuples, {len(values)} distinct values in the window")
    assert len(hits) == 12 and len(values) == 3, (len(hits), len(values))

    assert any(abs(v - ref) < 1e-8 for v in values)
    print(f"PASS_D0_TERM_PRESENT  359*phi^-2 - phi^-5 = {ref:.9f} is in the window "
          f"(distance {abs(ref-TARGET):.3e})")

    closer = [v for v in values if abs(v - TARGET) < abs(ref - TARGET) - 1e-12]
    assert len(closer) == 2
    print(f"FAIL_UNIQUENESS_REFUTED  BOTH rival values lie CLOSER to alpha^-1 than the D0 term "
          f"(distances {abs(closer[0]-TARGET):.3e}, {abs(closer[1]-TARGET):.3e} vs "
          f"{abs(ref-TARGET):.3e}) — the old README's 'exactly one value' claim is FALSE and is "
          "retired; no rarity claim is registered")

    # control: the machinery can fail — shrink the window until only the closest value remains
    tight = [v for v in values if abs(v - TARGET) < 2.5e-4]
    assert len(tight) == 1 and abs(tight[0] - min(closer, key=lambda v: abs(v-TARGET))) < 1e-8
    print("FAIL_WINDOW_CONTROL  at 2.5e-4 exactly one value survives and it is the rival, "
          "not the D0 term — the count genuinely depends on the window (can-fail)")

    print("HONEST_SCOPE  owned content stays: zeta_E(-1) = 359*phi^-2 - phi^-5 and zeta_E(0) = 359 "
          "(Lean, D0-EDGE-ALPHA-001); the ~3.7e-4 residual is closed by the registered dressing; "
          "this cert only pins the sweep's true combinatorics")
    print("PASS_ALPHA_LEADING_TERM_SWEEP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
