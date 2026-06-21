import D0.Extensions.LeptonSelectorExtension
import Mathlib.Tactic

/-!
# D0-LEPTON-BRANCH-FIXING-001 — Lane L terminal (L4)

The orbit sizes `{4,3}` are intrinsically distinct, so the orbit-keyed exponent selector (`4-cycle ↦ 1/4`,
`3-cycle ↦ 1/3`, `1/4 ≠ 1/3`) is branch-sensitive WITHOUT any post-hoc group narrowing. But there are only `2`
orbits for `3` generations — terminal **L4**: a branch-sensitive response exists, yet the full
branch→generation row needs one exact new operator (`PRIM-LEPTON-BRANCH-FIXING-OPERATOR`). The decimal/mass
map stays an EFT/IR passport.
-/

namespace D0.Extensions.LeptonBranchSelectorConstruction

open D0.Extensions.LeptonSelectorExtension

/-- **Terminal L4.** Orbit-keyed selector exists (`1/4 ≠ 1/3`, intrinsic — no narrowing) but `2 orbits < 3
generations`, so the full row needs one new operator. -/
theorem lepton_branch_selector_L4 :
    (1 / 4 : ℚ) ≠ 1 / 3 ∧ orbitSizes = [4, 3] ∧ orbitSizes.length < numGenerations :=
  ⟨orbit_exponents_distinct, rfl, orbits_fewer_than_generations⟩

end D0.Extensions.LeptonBranchSelectorConstruction
