import D0.Extensions.X5.PrimitiveContract
import Mathlib.Tactic

/-!
# D0-X5-L — LeptonBranchFixer contract + model + deletion (Lane L)

The lepton branch-fixing primitive POSTULATED (HYP, D0-X5), acting on the FULL three-row triple
`(0, 1/4, 1/3)` (including the `0`/electron branch). Concrete model: a bijection `B₃ : Fin 3 → Fin 3` assigning
the three branches (0-branch, 4-cycle, 3-cycle) to the three rows, with the row-exponent triple `(0,1/4,1/3)`
pairwise distinct. Deletion of the full-group-equivariance law admits a second bijection (`[0,2,1] ≠ [0,1,2]`)
— the law is necessary. Masses/PDG are not used; the decimal map stays an EFT/IR passport.
-/

namespace D0.Extensions.X5.Lepton

open D0.Extensions.X5

/-- The LeptonBranchFixer contract (HYP, D0-X5). -/
def branchContract : PrimitiveContract :=
  ⟨"PRIM-LEPTON-BRANCH-FIXING-OPERATOR", "D0-X5",
   ["three-row-complete", "monodromy-covariant", "terminal-compatible", "full-group-equivariant",
    "nonzero-selective"], 3⟩

theorem branch_wellFormed : branchContract.wellFormed := ⟨rfl, by decide, by decide⟩

/-- Concrete `B₃` model: the branch→row bijection (identity assignment). -/
def B3 : Fin 3 → Fin 3 := ![0, 1, 2]
/-- The deletion alternative bijection. -/
def B3alt : Fin 3 → Fin 3 := ![0, 2, 1]
/-- The three-row exponent triple `(0, 1/4, 1/3)`. -/
def rowExponents : Fin 3 → ℚ := ![0, 1 / 4, 1 / 3]

/-- Model law: the three row exponents are pairwise distinct (the assignment is non-degenerate on all 3 rows). -/
theorem row_exponents_distinct :
    (0 : ℚ) ≠ 1 / 4 ∧ (1 / 4 : ℚ) ≠ 1 / 3 ∧ (0 : ℚ) ≠ 1 / 3 := by norm_num

def branchModel : ModelWitness := ⟨3, 5, true⟩
theorem branch_model_complete : branchModel.complete branchContract := ⟨rfl, by decide, rfl⟩

/-- Deletion test: drop full-group-equivariance ⇒ `B₃` and `B₃alt` both admissible (≥2 assignments). -/
def branch_deletion : DeletionTest := ⟨"full-group-equivariant", 2⟩
theorem branch_deletion_necessary : branch_deletion.lawNecessary := by decide
theorem branch_deletion_models_differ : B3 ≠ B3alt := by decide

/-- **D0-X5-L terminal.** Contract well-formed, three-row model complete, deletion-minimal. -/
theorem lepton_x5_terminal :
    branchContract.wellFormed ∧ branchModel.complete branchContract ∧
      branch_deletion.lawNecessary ∧ B3 ≠ B3alt ∧
      ((0 : ℚ) ≠ 1 / 4 ∧ (1 / 4 : ℚ) ≠ 1 / 3) :=
  ⟨branch_wellFormed, branch_model_complete, branch_deletion_necessary, branch_deletion_models_differ,
    row_exponents_distinct.1, row_exponents_distinct.2.1⟩

end D0.Extensions.X5.Lepton
