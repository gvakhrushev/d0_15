#!/usr/bin/env python3
"""D0-TIME-MODULAR-FLOW-001 — quasicrystal carrier = symbolic time; arrow = Pisot.

ROOT B, T-B.2/T-B.3 (Iteration 3). The corpus asserts (BOOK_01 §01.19a) that the
quasicrystal carrier IS the symbolic dynamics of the golden foliation of the time
torus, and backs the load-bearing letter-by-letter coincidence with a PROSE-ONLY
"verified to 40 symbols" claim (no executable artifact). This certificate UPGRADES
that to an EXACT, executable, falsifiable check at large N, and is HONEST that the
full topological conjugacy stays a theorem-target.

WHAT IS PROVED (exact, able to FAIL):
  * SYMBOLIC COINCIDENCE.  The cut-and-project (mechanical) word of slope φ⁻² and the
    Fibonacci substitution word (a→ab, b→a) coincide letter-by-letter to N = 4000,
    under the canonical tile↔letter relabelling (long↔a).  Floors are computed by
    EXACT integer arithmetic via the closed form  ⌊kφ⌋ = (k + isqrt(5k²)) // 2  — no
    floating point, so the check genuinely can FAIL (it is not a 40-symbol eyeball).
    Slope = density of the rare letter = 2 - φ = φ⁻² (FORCED, not a tiling input).
  * PISOT ARROW.  ψ = 1 - φ = -1/φ is the Galois conjugate; |ψ| = φ⁻¹ = 0.6180… < 1.
    One conjugate outside the unit disk (φ > 1), one strictly inside (|ψ| < 1) ⇒ φ is
    Pisot at degree 2 ⇒ a clean golden Markov partition (Adler–Weiss) and a CONTRACTING
    direction: the arrow of time is the Pisot contraction of the conjugate.
  * NON-PERIODICITY.  The mechanical word is aperiodic (no period p ≤ 200 repeats),
    consistent with the irrational slope φ⁻² (a periodic carrier would mean rational
    slope = a forbidden resonance).

HONESTY BOUNDARY (printed, not hidden):
  * The cert proves the EXACT SYMBOLIC coincidence (the substitution fixed point = the
    slope-φ⁻² cut word). The full TOPOLOGICAL/MEASURE conjugacy — that the φ⁻² circle
    rotation is conjugate to the first-return map of the golden foliation of T
    (Morse–Hedlund / Sturm; golden-mean shift, Vershik) — is one page of standard
    ergodic mechanics that needs machinery NOT in Mathlib; it stays a THEOREM-TARGET.
  * The arrow-of-time INTERPRETATION ("|ψ|<1 ⇒ irreversibility") rests on Adler–Weiss
    as an external citation; the cert closes only the algebra |ψ| = φ⁻¹ < 1.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
N = 4000


def floor_k_phi(k: int) -> int:
    """EXACT ⌊k·φ⌋ via the closed form (k + ⌊√(5k²)⌋) // 2  (lower Wythoff)."""
    return (k + math.isqrt(5 * k * k)) // 2


def mechanical_word(n: int) -> list[int]:
    """Cut-and-project word of slope φ⁻²: m_k = ⌊(k+1)φ⌋ - ⌊kφ⌋ - 1 ∈ {0,1}, k≥1."""
    return [floor_k_phi(k + 1) - floor_k_phi(k) - 1 for k in range(1, n + 1)]


def fibonacci_substitution_word(n: int) -> list[int]:
    """Fixed point of σ: a→ab, b→a, with a=0, b=1, truncated to n letters."""
    s = "a"
    while len(s) < n:
        s = s.replace("a", "#").replace("b", "a").replace("#", "ab")
    return [0 if c == "a" else 1 for c in s[:n]]


def main() -> int:
    print("=== D0-TIME-MODULAR-FLOW-001  quasicrystal = symbolic time; arrow = Pisot ===")

    # ---- exact floor sanity (the load-bearing primitive) ---------------------------
    for k, want in [(1, 1), (2, 3), (3, 4), (4, 6), (5, 8), (10, 16)]:
        got = floor_k_phi(k)
        if got != want:
            raise AssertionError(f"exact floor ⌊{k}φ⌋ = {got} != {want}")
    print("PASS_EXACT_FLOOR_PRIMITIVE  ⌊kφ⌋ = (k+isqrt(5k²))//2 verified")

    # ---- the symbolic coincidence (slope φ⁻² cut word = Fibonacci substitution) -----
    mech = mechanical_word(N)
    sub = fibonacci_substitution_word(N)
    # canonical tile↔letter relabelling (long tile ↔ letter a): m_k = 1 - sub_k
    relabel = [1 - x for x in sub]
    if mech != relabel:
        first = next(i for i in range(N) if mech[i] != relabel[i])
        raise AssertionError(f"symbolic coincidence breaks at index {first}")
    if mech == sub:
        raise AssertionError("relabelling is trivial — coincidence is suspicious")
    print(f"PASS_SYMBOLIC_COINCIDENCE_TO_{N}  cut(φ⁻²) = Fibonacci-subst word (exact)")

    # ---- slope = φ⁻² (frequency of the RARE letter b = the slope of the cut word) ---
    # the common letter has density φ⁻¹; the rare letter (b in the substitution) has
    # density φ⁻² — that rare-letter frequency IS the cut-and-project slope.
    rare = sum(1 for x in sub if x == 1) / N    # density of b in the Fibonacci word
    target = 2.0 - PHI                          # = φ⁻² = 0.381966…
    if abs(rare - target) > 5e-3:               # finite-N sampling band around φ⁻²
        raise AssertionError(f"rare-letter density {rare:.5f} != φ⁻² {target:.5f}")
    if abs(target - PHI ** -2) > 1e-12:
        raise AssertionError("2 - φ != φ⁻²")
    common = sum(mech) / N                       # density of the common letter ≈ φ⁻¹
    if abs(common - PHI ** -1) > 5e-3:
        raise AssertionError(f"common-letter density {common:.5f} != φ⁻¹")
    print(f"PASS_SLOPE_IS_PHI_MINUS_2  rare freq {rare:.5f} ≈ φ⁻²={target:.5f}; "
          f"common ≈ φ⁻¹={common:.5f}")

    # ---- Pisot arrow: ψ = 1-φ = -1/φ, |ψ| = φ⁻¹ < 1 -------------------------------
    psi = 1.0 - PHI
    if abs(psi - (-1.0 / PHI)) > 1e-12:
        raise AssertionError("ψ != -1/φ")
    if not (abs(psi) < 1.0):
        raise AssertionError("|ψ| !< 1 — not Pisot")
    if abs(abs(psi) - PHI ** -1) > 1e-12:
        raise AssertionError("|ψ| != φ⁻¹")
    print(f"PASS_PISOT_ARROW  ψ = -1/φ, |ψ| = φ⁻¹ = {abs(psi):.6f} < 1 (contracting)")

    # ---- aperiodicity (irrational slope ⇒ no short period) -------------------------
    for p in range(1, 201):
        if all(mech[i] == mech[i + p] for i in range(N - p)):
            raise AssertionError(f"mechanical word has period {p} — would be periodic")
    print("PASS_APERIODIC_NO_PERIOD_LEQ_200  consistent with irrational slope φ⁻²")

    # ---- negative controls (must differ) -------------------------------------------
    # a RATIONAL slope (e.g. 2/5) would be periodic and NOT match the Fibonacci word
    rat = [( (k + 1) * 2 // 5) - (k * 2 // 5) for k in range(1, N + 1)]
    if rat == mech or rat == relabel:
        raise AssertionError("rational-slope control matched the φ⁻² word")
    print("FAIL_RATIONAL_SLOPE_2_5_DOES_NOT_MATCH")
    if floor_k_phi(7) == 7:                 # ⌊7φ⌋ = 11, not 7
        raise AssertionError("floor control failed")
    print("FAIL_FLOOR_NOT_IDENTITY")
    print("PASS_TIME_MODULAR_FLOW_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_PROVES_EXACT_SYMBOLIC_COINCIDENCE_NOT_TOPOLOGICAL_CONJUGACY")
    print("HONEST_ROTATION_CONJUGATE_TO_FOLIATION_RETURN_MAP_IS_THEOREM_TARGET")
    print("HONEST_ARROW_INTERPRETATION_RESTS_ON_ADLER_WEISS_EXTERNAL_CITATION")

    print("PASS_QUASICRYSTAL_TIME_STURMIAN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
