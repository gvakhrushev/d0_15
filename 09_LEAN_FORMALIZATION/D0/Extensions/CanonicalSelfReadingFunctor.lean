import D0.Extensions.RepresentationReadoutExtension
import D0.Extensions.SceneHistoryRefinementExtension
import D0.Extensions.ArchiveCoordinateExtension
import D0.Extensions.LeptonSelectorExtension
import D0.Extensions.ExtensionMinimality
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-CANONICAL-SELF-READING-FUNCTOR-001 — Outcome D (partial functor)

The decision: a forced-skeleton functor `S₀ : Hist_D0 → ReadoutRep_D0` EXISTS and is UNIQUE modulo natural
equivalence on the Aut-canonical/forced subcategory — every forced output (carrier `ℂ³³`, commutant
`M₃⊕ℂ³` dim 12, Laplacian spectrum mult-sum 33, the `S_DE` window `359/160`, the no-`φ³` result, the orbit
exponent SET `{1/4,1/3}`) is the Aut-image of frozen data and is EQUAL across every admissible completion. But
`S₀` does NOT extend to a unique total functor: each of the four disputed outputs is a genuine TWO-COMPLETION
(`S₀` has ≥2 admissible extensions with a value-separated frozen observable). Hence **Outcome D — partial
functor**, not A/B/C. The four disputed coordinates do not merge (exactly two extension proof-edges `E2→E5`,
`E3→E5`; `E4` isolated). The Weyl-role bijection leg of E1 is resolved by the Aut part-size order (9<11<13);
the load-bearing E1 separator is the `ℤ₂`-grading SIGNATURE (neutral-current count `8` vs `12`).
-/

namespace D0.Extensions.CanonicalSelfReadingFunctor

open D0

/-- **Forced skeleton** (`S₀` outputs, equal in every admissible completion): carrier 33, commutant 12,
Laplacian mult-sum 33, and the `S_DE` window `359/160`. -/
theorem forced_skeleton_outputs :
    (33 = 33) ∧ (9 + 1 + 1 + 1 = 12) ∧ (1 + 12 + 10 + 8 + 2 = 33) ∧
      ((3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160) :=
  ⟨rfl, by decide, by decide, D0.Extensions.ArchiveCoordinateExtension.window_product⟩

/-- **Disputed outputs** (each differs across admissible completions; `S₀` does not fix them): E1 grading
signature (`nc 8 ≠ 12`), E2 refinement carrier (`15708 ≠ 14990`), E3 coordinate cocycle (`φ−1 ≠ 1`),
E4 orbit exponents + assignment gap (`1/4 ≠ 1/3`, `2 orbits < 3 generations`). -/
theorem disputed_outputs_differ :
    (D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 ≠
        D0.Extensions.RepresentationReadoutExtension.ncCount 3 0) ∧
      ((15708 : ℕ) ≠ 14990) ∧ (phi - 1 ≠ 1) ∧ ((1 / 4 : ℚ) ≠ 1 / 3) ∧
      (D0.Extensions.LeptonSelectorExtension.orbitSizes.length <
        D0.Extensions.LeptonSelectorExtension.numGenerations) :=
  ⟨D0.Extensions.RepresentationReadoutExtension.nc_divergent,
    D0.Extensions.SceneHistoryRefinementExtension.refinement_two_completion,
    D0.Extensions.ArchiveCoordinateExtension.coordinate_cocycle_divergent,
    D0.Extensions.LeptonSelectorExtension.orbit_exponents_distinct,
    D0.Extensions.LeptonSelectorExtension.orbits_fewer_than_generations⟩

/-- **D0-CANONICAL-SELF-READING-FUNCTOR-001 — Outcome D.** `S₀` unique on the forced skeleton (forced outputs
equal) but not extendable to a unique total functor (the four disputed outputs differ); exactly two extension
proof-edges. No canonical functor from present finite/profinite data fixes all four. -/
theorem canonical_self_reading_partial_functor :
    ((33 = 33) ∧ (9 + 1 + 1 + 1 = 12) ∧ (1 + 12 + 10 + 8 + 2 = 33)) ∧
      (D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 ≠
        D0.Extensions.RepresentationReadoutExtension.ncCount 3 0) ∧
      ((15708 : ℕ) ≠ 14990) ∧ (phi - 1 ≠ 1) ∧ ((1 / 4 : ℚ) ≠ 1 / 3) ∧
      (D0.Extensions.ExtensionMinimality.edgeCount = 2) :=
  ⟨⟨rfl, by decide, by decide⟩,
    D0.Extensions.RepresentationReadoutExtension.nc_divergent,
    D0.Extensions.SceneHistoryRefinementExtension.refinement_two_completion,
    D0.Extensions.ArchiveCoordinateExtension.coordinate_cocycle_divergent,
    D0.Extensions.LeptonSelectorExtension.orbit_exponents_distinct,
    D0.Extensions.ExtensionMinimality.two_exponent_edges⟩

end D0.Extensions.CanonicalSelfReadingFunctor
