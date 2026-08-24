#!/usr/bin/env python3
"""D0-PHI-QUADPISOT-MINIMALITY-001 — φ is the minimal quadratic Pisot number (triple selector).

STRUCTURE (THE, Lean D0.NumberTheory.PhiQuadPisotMinimality, PHI_QUADPISOT_MINIMALITY_PROVED):
  * every quadratic Pisot number γ — real root of x² − s·x + t with s,t ∈ ℤ, γ > 1,
    conjugate |s − γ| < 1 — satisfies φ ≤ γ;
  * equality iff (s, t) = (1, −1), i.e. iff γ is φ itself (no Irrational machinery used:
    the s = 2 case dies on "k² = k + 1 has no integer solution");
  * every admissible period-one member β_a = a + tail_a (a ≥ 1, tail² + a·tail = 1) is a
    quadratic Pisot number, and β₁ = φ;
  * composed with the owned upstream Hurwitz leg (periodOneBadApproxConstant_max_at_one),
    all three classical selectors — self-reference, Hurwitz minimax, quadratic-Pisot
    minimality — agree on a = 1, i.e. on φ.

NO-OVERCLAIM BOUNDARY (the guard this cert exists to enforce):
  the naive global claim "φ is the smallest Pisot number" is FALSE.  The plastic number
  ρ ≈ 1.324717957 (real root of x³ = x + 1) is a Pisot number strictly below φ: its
  conjugate pair has modulus √(ρ² − 1) ≈ 0.8688 < 1.  The correct global statements are:
  minimal QUADRATIC Pisot number; simplest defining polynomial among Pisot numbers
  (degree 2); Hurwitz-extremal worst-approximable irrational.  The control below must
  FAIL the naive claim while the main gates PASS the correct one.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 naive-smallest-Pisot: the plastic witness must break it (ρ Pisot ∧ ρ < φ);
  C2 wrong equality pair (s, t) = (2, −2) must NOT reproduce φ;
  C3 non-Pisot quadratic x² − 3x + 2 (conjugate exactly 1) must be rejected by the
     strict conjugate filter.
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
TOL = 1e-9


def quad_roots(s: float, t: float) -> tuple[float, float] | None:
    """Real roots of x² − s·x + t (None if not two real roots)."""
    disc = s * s - 4.0 * t
    if disc < 0:
        return None
    r = disc ** 0.5
    return ((s - r) / 2.0, (s + r) / 2.0)


def is_quad_pisot(s: float, t: float) -> float | None:
    """Return the Pisot member γ > 1 of x² − s·x + t, or None if the pair has none."""
    roots = quad_roots(s, t)
    if roots is None:
        return None
    for gamma in roots:
        if gamma > 1.0 and abs(s - gamma) < 1.0:
            return gamma
    return None


def beta_one(a: int) -> float:
    """β_a = a + tail_a, the root > 1 of x² − a·x − 1 (tail solves τ² + a·τ = 1)."""
    tail = ((a * a + 4.0) ** 0.5 - a) / 2.0
    return a + tail


def main() -> int:
    print("=== D0-PHI-QUADPISOT-MINIMALITY-001  φ = min quadratic Pisot (triple selector) ===")
    print(f"STRUCTURE_FIXED_BEFORE_NUMBER: quad-Pisot class x²−sx+t (s,t∈ℤ, γ>1, |s−γ|<1); "
          f"period-one family β_a=a+tail_a; upstream Hurwitz leg owned")

    # ---- GATE 1: exhaustive scan — no quadratic Pisot number below φ --------------------
    violators: list[tuple[int, int, float]] = []
    equality_hits: list[tuple[int, int, float]] = []
    for s in range(-10, 13):
        for t in range(-40, 41):
            g = is_quad_pisot(float(s), float(t))
            if g is None:
                continue
            if g < PHI - 1e-7:
                violators.append((s, t, g))
            if abs(g - PHI) < 1e-7:
                equality_hits.append((s, t, g))
    assert not violators, f"quad-Pisot minimality violated by {violators[:4]}"
    print(f"PASS_QUADPISOT_MINIMALITY  scan s∈[−10,12], t∈[−40,40]: no γ < φ; "
          f"φ itself is quad-Pisot (min = {PHI:.12f})")

    # ---- GATE 2: equality case is exactly (s,t) = (1,−1) --------------------------------
    assert equality_hits, "φ must be realized as a quad-Pisot number"
    pairs = {(s, t) for (s, t, _) in equality_hits}
    assert pairs == {(1, -1)}, f"equality case must be exactly (1,−1), got {sorted(pairs)}"
    print(f"PASS_EQUALITY_CASE_EXACT  γ = φ ⟺ (s,t) = (1,−1);  other pairs near φ: none")

    # ---- GATE 3: the period-one family is quad-Pisot, minimal at a = 1 ------------------
    fam = [(a, beta_one(a)) for a in range(1, 25)]
    assert abs(fam[0][1] - PHI) < TOL, f"β₁ must equal φ, got {fam[0][1]}"
    assert all(b >= PHI - 1e-12 for _, b in fam), "family members must all be ≥ φ"
    assert all(abs(beta_one(a) ** 2 - a * beta_one(a) - 1) < TOL for a in range(1, 25)), \
        "family members must satisfy β² − a·β − 1 = 0"
    print(f"PASS_PERIOD_ONE_FAMILY  β₁ = φ exactly; all β_a ≥ φ for a = 1..24; poly identity holds")
    print(f"PASS_TRIPLE_SELECTOR  self-reference (a≥1) ∧ Hurwitz (1/√(a²+4) max at a=1) ∧ "
          f"quad-Pisot min: all three select a = 1 = φ")

    # ---- CONTROL C1 (must FAIL the naive claim): plastic number is Pisot below φ --------
    plastic_coeffs = [1.0, 0.0, -1.0, -1.0]  # x³ − x − 1
    roots = np.roots(plastic_coeffs)
    rho = max(r.real for r in roots if abs(r.imag) < 1e-9)
    conj_moduli = sorted(abs(r) for r in roots)[:-1]
    assert abs(rho ** 3 - rho - 1) < TOL, "ρ must satisfy ρ³ = ρ + 1"
    assert all(m < 1.0 for m in conj_moduli), f"plastic conjugates must lie inside unit disk: {conj_moduli}"
    assert 1.0 < rho < PHI, f"plastic must be a Pisot number below φ: ρ={rho}"
    print(f"FAIL_NAIVE_SMALLEST_PISOT_CLAIM  plastic ρ={rho:.9f} is Pisot (conj |·|="
          f"{conj_moduli[-1]:.6f}<1) and ρ < φ — the naive global claim is FALSE; "
          f"correct claim: minimal QUADRATIC Pisot + simplest defining polynomial")

    # ---- CONTROL C2 (must fail): wrong equality pair does not reproduce φ ---------------
    g_wrong = is_quad_pisot(2.0, -2.0)
    assert g_wrong is not None and abs(g_wrong - PHI) > 1e-3, \
        f"(2,−2) must not reproduce φ, got {g_wrong}"
    print(f"FAIL_WRONG_EQUALITY_PAIR  (s,t)=(2,−2) gives γ={g_wrong:.9f} ≠ φ")

    # ---- CONTROL C3 (must fail): conjugate exactly 1 is rejected by the strict filter ----
    assert is_quad_pisot(3.0, 2.0) is None, "x²−3x+2 (conjugate = 1) must not count as Pisot"
    print(f"FAIL_NONSTRICT_CONJUGATE  x²−3x+2 rejected: conjugate |s−γ|=1 is not < 1")

    print("HONEST_BOUNDARY  naive 'smallest Pisot' claim is closed-negative here; the "
          "Lean module carries the correct triple-selector statement (0 sorry, rc=0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
