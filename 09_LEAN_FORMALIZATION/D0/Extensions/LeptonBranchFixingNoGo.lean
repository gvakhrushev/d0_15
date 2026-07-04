import D0.Extensions.LeptonSelectorExtension
import Mathlib.Tactic

/-!
# D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001 — Lane L close (pigeonhole NO-GO)

STRENGTHENS terminal L4 (the bare inequality `2 < 3`) to a PROVEN non-constructibility. The frozen
shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)` supplies exactly `2` branch-orbits (exponents
`1/4 ≠ 1/3`), while the scene has `3` generations (`K(9,11,13)`: multiplicity of the trivial isotype
= `Tr(T²) = 3`). A branch→generation "full row" operator would have to be one of:
  (a) an injection `Gen(3) ↪ Branch(2)` (distinguish the 3 generations by branch-data), or
  (b) a surjection `Branch(2) ↠ Gen(3)` (cover the 3 generations by branches), or
  (c) a bijection `Branch(2) ≃ Gen(3)`.
All three are IMPOSSIBLE by cardinality (`decide`). Moreover the 7-point shell-torus has NO fixed point,
so there is no third "regular / unramified" (electron, index-`0`) branch inside the carrier — the third
datum is genuinely EXTERNAL (postulated HYP in `D0.Extensions.X5.Lepton`). Hence
`PRIM-LEPTON-BRANCH-FIXING-OPERATOR` is NOT constructible from the frozen 2-orbit data. NO-GO.

Cites (does not re-mint): `D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001` (R4, `σ_A/σ_B` completions),
`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` (R1, the 3 generations are rank-only with
`GL(3)`/`S₃` label-freedom), `D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001` (E4), `D0-X5-LEPTON-CONTRACT-001`
(the third row is POSTULATED HYP). Decimals stay an EFT/IR passport; no PDG mass enters.
-/

namespace D0.Extensions.LeptonBranchFixingNoGo

open D0.Extensions.LeptonSelectorExtension

/-- Number of branch-orbits the shell-torus supplies = `orbitSizes.length` = `2`. -/
def numBranches : ℕ := orbitSizes.length

theorem numBranches_eq_two : numBranches = 2 := by decide
theorem numGenerations_eq_three : numGenerations = 3 := rfl

/-- The frozen shell-torus permutation `σ = (0 1 2 3)(4 5 6)` on `Fin 7`
(matches `D0.Matter.LeptonBranchAssignmentNoGo.sigmaA`). -/
def sigmaShell : Fin 7 → Fin 7 := ![1, 2, 3, 0, 5, 6, 4]

/-- **No third branch inside the carrier.** `σ` has NO fixed point, so there is no regular/unramified
(electron index-`0`) third orbit inside the 7-point shell-torus: the third datum is external. -/
theorem shell_no_fixed_point : ∀ i, sigmaShell i ≠ i := by decide

/-- **Pigeonhole (a).** No injection `Gen(3) ↪ Branch(2)`: the 3 generations cannot be pairwise
distinguished by only 2 branch-data (≥ 2 generations must share one branch). -/
theorem no_injective_gen_into_branch :
    ¬ ∃ f : Fin 3 → Fin 2, Function.Injective f := by decide

/-- **Pigeonhole (b).** No surjection `Branch(2) ↠ Gen(3)`: any branch→generation assignment misses
≥ 1 generation (the third generation is unforced by the 2 orbits). -/
theorem no_surjective_branch_onto_gen :
    ¬ ∃ g : Fin 2 → Fin 3, Function.Surjective g := by decide

/-- **Pigeonhole (c).** No bijection `Branch(2) ≃ Gen(3)`: the full branch↔generation row is impossible. -/
theorem no_bijection_branch_gen :
    ¬ ∃ h : Fin 2 → Fin 3, Function.Bijective h := by decide

/-- **D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001 (NO-GO).** The frozen shell-torus supplies exactly
`numBranches = 2` orbit-branches for `numGenerations = 3` generations, and has no fixed point (no third
in-carrier branch). By cardinality there is no injection `Gen(3) ↪ Branch(2)`, no surjection
`Branch(2) ↠ Gen(3)`, and no bijection `Branch(2) ≃ Gen(3)`. Therefore no branch→generation full-row
operator is constructible from the frozen 2-orbit data: `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` must be an
external primitive (postulated HYP in D0-X5-L). -/
theorem lepton_branch_fixing_operator_nogo :
    numBranches = 2 ∧ numGenerations = 3 ∧ numBranches < numGenerations
      ∧ (∀ i, sigmaShell i ≠ i)
      ∧ (¬ ∃ f : Fin 3 → Fin 2, Function.Injective f)
      ∧ (¬ ∃ g : Fin 2 → Fin 3, Function.Surjective g)
      ∧ (¬ ∃ h : Fin 2 → Fin 3, Function.Bijective h) :=
  ⟨numBranches_eq_two, numGenerations_eq_three, by decide, shell_no_fixed_point,
   no_injective_gen_into_branch, no_surjective_branch_onto_gen, no_bijection_branch_gen⟩

end D0.Extensions.LeptonBranchFixingNoGo
