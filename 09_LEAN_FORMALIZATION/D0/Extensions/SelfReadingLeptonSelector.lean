import D0.Extensions.LeptonSelectorExtension
import Mathlib.Tactic

/-!
# Self-reading lepton selector (Section 2.3)

What `S₀` FORCES on the shell-torus: the orbit-keyed exponent SET `{1/4, 1/3}` is well-defined (4-cycle ↦ 1/4,
3-cycle ↦ 1/3, `1/4 ≠ 1/3`). What it does NOT fix: the branch→generation ASSIGNMENT row — there are only 2
orbits for 3 generations, and the swap `σ_A/σ_B` is a single `S₇` conjugacy class (12 conjugators), so `S` is
swap-invariant and branch uniqueness fails. The decimal/mass relation stays an external EFT/IR passport.
-/

namespace D0.Extensions.SelfReadingLeptonSelector

open D0.Extensions.LeptonSelectorExtension

/-- **2.3 forced vs disputed.** Forced: orbit exponents `1/4 ≠ 1/3`. Disputed: `2 orbits < 3 generations`
(assignment row). -/
theorem lepton_extraction_forced_vs_disputed :
    (1 / 4 : ℚ) ≠ 1 / 3 ∧ orbitSizes.length < numGenerations :=
  ⟨orbit_exponents_distinct, orbits_fewer_than_generations⟩

end D0.Extensions.SelfReadingLeptonSelector
