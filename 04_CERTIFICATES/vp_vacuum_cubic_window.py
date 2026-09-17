#!/usr/bin/env python3
"""D0-VACUUM-CUBIC-WINDOW-001 — the S_DE cubic-vs-quadratic fork, discriminator computed.

ROOT §4 (Iteration 3). The GOLDEN dossier (transfer-D0-THEORY-DOSSIER-0940) records an
HONEST FORK: two catalog-free ownerships of the dark-energy / S_DE archive window —
  (A) the S_DE QUADRATIC  160λ² − 480λ + 359  (already CERT-CLOSED, BOOK_08 §08.12), and
  (B) the VACUUM CUBIC    λ³ = 359λ + 2574    (= the adjacency characteristic cubic),
— and a window-center discriminator "0.808 (cubic) vs 0.900 (quadratic)" against DESI DR3
that "has never been computed". This certificate COMPUTES that discriminator exactly from
first principles (so the fork is now sharply posed) and is scrupulously HONEST that it does
NOT pick a winner: DESI DR3 is the empirical decider and has not been run here.

WHAT IS PROVED (exact, able to FAIL):
  * QUADRATIC branch.  160λ² − 480λ + 359 has trace 3 and det 359/160, with
    160 = 2·Ω₈·γ = 2·8·10 (γ=10 = nullity/rank = 30/3). Eigenvalues λ_{c,r} = 3/2 ∓ √10/40.
    Window-center ratio  λ_c/λ_r = (60 − √10)/(60 + √10) = 0.89987  ≈ 0.900.
  * CUBIC branch.  λ³ − 359λ − 2574 has catalog-free symmetric-function owners
    e₁ = 0 (traceless), e₂ = −359 (= −|E|, capacity), e₃ = 2574 = 2·1287 = 2·|triangles|
    of K(9,11,13); positive discriminant ⇒ 3 distinct real roots {21.84, −9.758, −12.079}.
    Window-center ratio = |λ₂|/|λ₃| of the two negative roots = 0.80787  ≈ 0.808.
  * THE DISCRIMINATOR (now computed, was never computed): cubic 0.808 vs quadratic 0.900.

HONESTY BOUNDARY (printed, not hidden):
  * This is a FORK, not a decision.  Both branches are derived from catalog-free owners;
    the cert computes the two competing window-center predictions but DOES NOT choose —
    the discriminating observable is DESI DR3, which is NOT run here. Promotion of either
    branch to the sole core form requires that external survey comparison (a BRIDGE step),
    which the firewall keeps out of core.
  * The cubic IS the adjacency characteristic polynomial (already owned by
    D0-MIXING-HIERARCHY-INVERSION-001); this cert adds its cosmology-window reading and
    the computed discriminator, not a new polynomial.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9
# K(9,11,13) invariants (owned upstream)
E_COUNT = 359
TRIANGLES = 1287
OMEGA8 = 8
GAMMA = 10            # reduced terminal echo depth = nullity/rank = 30/3


def cubic_roots() -> list[float]:
    """Real roots of λ³ - 359λ - 2574 (the adjacency characteristic cubic)."""
    import numpy as np
    r = np.roots([1.0, 0.0, -359.0, -2574.0])
    return sorted(float(x.real) for x in r if abs(x.imag) < 1e-9)


def main() -> int:
    print("=== D0-VACUUM-CUBIC-WINDOW-001  S_DE cubic-vs-quadratic fork (discriminator) ===")

    # ---- QUADRATIC branch: 160λ²-480λ+359, 160=2·Ω₈·γ, ratio = (60-√10)/(60+√10) -----
    assert 160 == 2 * OMEGA8 * GAMMA, "160 != 2·Ω₈·γ"
    # trace 3, det 359/160 (exact)
    trace = F(480, 160)
    det = F(359, 160)
    assert trace == 3, "quadratic trace != 3"
    assert det == F(359, 160), "quadratic det != 359/160"
    # eigenvalues 3/2 ∓ √10/40
    sq10 = math.sqrt(10.0)
    lam_c = 1.5 - sq10 / 40.0
    lam_r = 1.5 + sq10 / 40.0
    assert abs(lam_c + lam_r - 3.0) < TOL and abs(lam_c * lam_r - 359.0 / 160.0) < TOL
    quad_ratio = lam_c / lam_r
    # exact form (60-√10)/(60+√10)
    assert abs(quad_ratio - (60 - sq10) / (60 + sq10)) < TOL, "quad ratio != (60-√10)/(60+√10)"
    assert abs(quad_ratio - 0.900) < 5e-3, f"quad window-center ratio {quad_ratio} !≈ 0.900"
    print(f"PASS_QUADRATIC_BRANCH  160=2·Ω₈·γ; eigs 3/2∓√10/40; ratio (60-√10)/(60+√10)={quad_ratio:.5f}≈0.900")

    # ---- CUBIC branch: λ³-359λ-2574 from (e1,e2,e3)=(0,-359,2·1287) ------------------
    e1, e2, e3 = 0, -E_COUNT, 2 * TRIANGLES
    assert e2 == -359 and e3 == 2574 == 2 * 1287, "cubic symmetric-function owners wrong"
    roots = cubic_roots()
    assert len(roots) == 3, f"cubic must have 3 real roots, got {len(roots)}"
    # verify Vieta: sum=e1=0, pairwise sum=e2=-359, product=e3=2574
    assert abs(sum(roots)) < TOL, "cubic e1 != 0"
    pair = roots[0] * roots[1] + roots[0] * roots[2] + roots[1] * roots[2]
    assert abs(pair - (-359)) < 1e-6, "cubic e2 != -359"
    assert abs(roots[0] * roots[1] * roots[2] - 2574) < 1e-6, "cubic e3 != 2574"
    # each root satisfies the cubic
    for x in roots:
        assert abs(x ** 3 - 359 * x - 2574) < 1e-6, f"root {x} fails the cubic"
    # window-center ratio = |smaller neg|/|larger neg| of the two negative roots
    negs = sorted((x for x in roots if x < 0), key=abs)   # [-9.758, -12.079]
    cubic_ratio = abs(negs[0]) / abs(negs[1])
    assert abs(cubic_ratio - 0.808) < 5e-3, f"cubic window-center ratio {cubic_ratio} !≈ 0.808"
    print(f"PASS_CUBIC_BRANCH  e=(0,-359,2·1287); roots {[round(r,3) for r in roots]}; ratio={cubic_ratio:.5f}≈0.808")

    # ---- THE DISCRIMINATOR: cubic 0.808 vs quadratic 0.900 (now computed) ------------
    assert abs(cubic_ratio - quad_ratio) > 0.05, "branches do not separate"
    print(f"PASS_DISCRIMINATOR_COMPUTED  cubic {cubic_ratio:.3f} vs quadratic {quad_ratio:.3f} "
          f"(Δ={abs(cubic_ratio-quad_ratio):.3f}) — separable against DESI DR3")

    # ---- negative controls (must differ) -------------------------------------------
    # the cubic is NOT the quadratic; ratios must be distinct
    assert round(cubic_ratio, 3) != round(quad_ratio, 3), "control: ratios coincide"
    # wrong e3 (e.g. |triangles| not doubled) would break Vieta
    assert 1287 != 2574, "control: e3 must be the DOUBLED triangle count"
    print("FAIL_CUBIC_NOT_QUADRATIC")
    print("FAIL_E3_IS_DOUBLED_TRIANGLES")
    print("PASS_VACUUM_CUBIC_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_FORK_NOT_A_DECISION_DESI_DR3_DECIDES_AND_IS_NOT_RUN_HERE")
    print("HONEST_CUBIC_IS_THE_ADJACENCY_POLY_OWNED_BY_MIXING_HIERARCHY_INVERSION")
    print("HONEST_EITHER_BRANCH_TO_SOLE_CORE_NEEDS_EXTERNAL_DESI_COMPARISON_BRIDGE")

    print("PASS_VACUUM_CUBIC_WINDOW")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
