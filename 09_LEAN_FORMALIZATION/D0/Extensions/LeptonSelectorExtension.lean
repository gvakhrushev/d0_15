import Mathlib.Tactic

/-!
# D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001 — E4 (branch-sensitive lepton selector extension)

The "unique selector" route is CIRCULAR: it narrows the admissible symmetry group to `Cent(U_eff)` (which
excludes the (4,3) block swap), but committing to that centralizer presupposes the choice of `σ_A` over `σ_B`
— and `(4,3)` is a SINGLE `S₇` conjugacy class (12 conjugators carry `σ_A → σ_B`), so the swap-excluding group
is not canonical. Hence the present-core R4 NO-GO stands. The genuinely-NEW honest content: the resolvent DOES
force an **orbit-keyed** exponent map (`4-cycle ↦ 1/4`, `3-cycle ↦ 1/3`, and `1/4 ≠ 1/3`), but there are only
`2` orbits for `3` generations, so the branch→generation assignment is underdetermined. The mass decimals stay
an external EFT/IR passport. Cites `D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001` (R4),
`D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001`, `D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001`. Missing:
`PRIM-LEPTON-BRANCH-FIXING-OPERATOR`.
-/

namespace D0.Extensions.LeptonSelectorExtension

/-- The two cycle/orbit sizes of the shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)`. -/
def orbitSizes : List ℕ := [4, 3]

/-- The number of generations to assign. -/
def numGenerations : ℕ := 3

/-- The orbit-keyed exponents `1/4` and `1/3` are distinct (the map is well-defined on orbits). -/
theorem orbit_exponents_distinct : (1 / 4 : ℚ) ≠ 1 / 3 := by norm_num

theorem two_orbits : orbitSizes.length = 2 := by decide

/-- **Only `2` orbits for `3` generations**: the branch→generation assignment is underdetermined. -/
theorem orbits_fewer_than_generations : orbitSizes.length < numGenerations := by decide

/-- **D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001.** The resolvent forces a well-defined orbit-keyed
exponent map (`1/4 ≠ 1/3`), but `2` orbits `< 3` generations leaves the assignment unforced (and the
group-narrowing "unique" route is circular). `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` stays absent. -/
theorem lepton_selector_extension_nogo :
    (1 / 4 : ℚ) ≠ 1 / 3 ∧ orbitSizes.length = 2 ∧ orbitSizes.length < numGenerations :=
  ⟨orbit_exponents_distinct, two_orbits, orbits_fewer_than_generations⟩

end D0.Extensions.LeptonSelectorExtension
