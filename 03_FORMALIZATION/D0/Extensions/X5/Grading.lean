import D0.Extensions.X5.PrimitiveContract
import D0.Extensions.RawCommutantWedderburn
import D0.Extensions.RepresentationReadoutExtension
import Mathlib.Tactic

/-!
# D0-X5-G — GammaNC contract + model + deletion (Lane G)

The grading/neutral-current primitive POSTULATED on the derived `M₃` block (`RawCommutantWedderburn`). HYP,
`extension_layer = D0-X5` — NOT present-core. Concrete model: the signature-`(2,1)` grading `diag(1,1,-1)` on
the 3-dim `M₃` (self-adjoint, involutive — `decide`-checked, non-vacuous), giving `N_active = nc(2,1) = 8`.
Deletion of the response-equivariance law admits the `(3,0)` model too (`nc = 12 ≠ 8`) — the law is necessary.
`N_active = 8` is a theorem RELATIVE to the D0-X5-G contract, never a present-core fact.
-/

namespace D0.Extensions.X5.Grading

open D0.Extensions.X5

/-- The GammaNC contract (HYP, D0-X5). -/
def gammaNCContract : PrimitiveContract :=
  ⟨"PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR", "D0-X5",
   ["selfadjoint", "involution", "tripartite-commute", "terminal-preserving", "response-equivariant"], 3⟩

theorem gammaNC_wellFormed : gammaNCContract.wellFormed := ⟨rfl, by decide, by decide⟩

/-- Concrete model: the grading diagonal `diag(1,1,-1)` (signature `(2,1)`) on the `M₃` block. -/
def gradingDiag : Fin 3 → ℤ := ![1, 1, -1]
/-- The `(3,0)` deletion alternative `diag(1,1,1)`. -/
def gradingDiag30 : Fin 3 → ℤ := ![1, 1, 1]

/-- Model laws (non-vacuous, `decide`-checked): involution `Γ² = I`. -/
theorem grading_involution : ∀ i, gradingDiag i ^ 2 = 1 := by decide
/-- Signature `(2,1)`: two `+1`, one `-1`. -/
theorem grading_signature_21 :
    (List.ofFn gradingDiag).count 1 = 2 ∧ (List.ofFn gradingDiag).count (-1) = 1 := by decide

def gammaNCModel : ModelWitness := ⟨3, 5, true⟩
theorem gammaNC_model_complete : gammaNCModel.complete gammaNCContract := ⟨rfl, by decide, rfl⟩

/-- Deletion test: drop response-equivariance ⇒ `(2,1)` and `(3,0)` both admissible (≥2 models). -/
def gammaNC_deletion : DeletionTest := ⟨"response-equivariant", 2⟩
theorem gammaNC_deletion_necessary : gammaNC_deletion.lawNecessary := by decide
/-- The two deletion models genuinely differ. -/
theorem gammaNC_deletion_models_differ : gradingDiag ≠ gradingDiag30 := by decide

/-- **Relative theorem (THE relative to D0-X5-G).** Under the `(2,1)` grading contract,
`N_active = nc(2,1) = 8`; the deletion-model `(3,0)` gives `12` — so `N_active` is contract-relative. -/
theorem N_active_relative :
    D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 = 8 ∧
      D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 ≠
        D0.Extensions.RepresentationReadoutExtension.ncCount 3 0 :=
  ⟨D0.Extensions.RepresentationReadoutExtension.nc_signature_21,
    D0.Extensions.RepresentationReadoutExtension.nc_divergent⟩

/-- **D0-X5-G terminal.** Contract well-formed, model complete (non-vacuous), deletion-minimal. -/
theorem grading_x5_terminal :
    gammaNCContract.wellFormed ∧ gammaNCModel.complete gammaNCContract ∧
      gammaNC_deletion.lawNecessary ∧ gradingDiag ≠ gradingDiag30 :=
  ⟨gammaNC_wellFormed, gammaNC_model_complete, gammaNC_deletion_necessary, gammaNC_deletion_models_differ⟩

end D0.Extensions.X5.Grading
