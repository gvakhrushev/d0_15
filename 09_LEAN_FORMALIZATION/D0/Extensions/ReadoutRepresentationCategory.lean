import Mathlib.Tactic

/-!
# ReadoutRep_D0 — the finite response-representation target category (Section 1.2)

Objects are `(H, ρ, R = D†D, Π_term, Π_archive, Γ?, J?, C?)`: a faithful finite response representation with
the readout operator `R`, terminal and archive projectors, and OPTIONAL grading `Γ`, reality `J`, and
conditional-expectation `C` (each must be derived, not assumed). An object is admissible only if all physical
labels remain ABSENT until an invariant operator/readout identifies them.
-/

namespace D0.Extensions.ReadoutRepresentationCategory

/-- A finite response representation object. -/
structure ReadoutObject where
  carrierDim : ℕ
  hasRho : Bool        -- faithful finite representation present
  hasR : Bool          -- R = D†D present
  hasPiTerm : Bool
  hasPiArchive : Bool
  gamma : Bool         -- optional grading (derived or absent)
  jStruct : Bool       -- optional reality structure
  condExp : Bool       -- optional conditional expectation
  labelsAbsent : Bool  -- admissibility: no physical labels until identified

/-- Admissibility: faithful rep + readout present, projectors present, and physical labels absent. -/
def admissible (O : ReadoutObject) : Prop :=
  O.hasRho = true ∧ O.hasR = true ∧ O.hasPiTerm = true ∧ O.hasPiArchive = true ∧ O.labelsAbsent = true

/-- Morphism: a readout-intertwiner between admissible objects of equal carrier dimension. -/
def Hom (O P : ReadoutObject) : Prop :=
  admissible O ∧ admissible P ∧ O.carrierDim = P.carrierDim

theorem hom_id (O : ReadoutObject) (h : admissible O) : Hom O O := ⟨h, h, rfl⟩

theorem hom_comp {O P Q : ReadoutObject} (h₁ : Hom O P) (h₂ : Hom P Q) : Hom O Q :=
  ⟨h₁.1, h₂.2.1, h₁.2.2.trans h₂.2.2⟩

/-- An object that has prematurely assigned physical labels is not admissible (rejected). -/
theorem labels_present_rejected {O : ReadoutObject} (h : O.labelsAbsent = false) : ¬ admissible O := by
  rintro ⟨_, _, _, _, hl⟩; rw [h] at hl; exact Bool.noConfusion hl

/-- The optional structures `Γ, J, C` may each be present or absent — the scene carrier (`ℂ³³`) admits an object
either way (they are derived, not assumed). -/
theorem optional_structures_independent :
    ∃ O P : ReadoutObject, O.gamma = true ∧ P.gamma = false ∧ O.carrierDim = 33 ∧ P.carrierDim = 33 := by
  exact ⟨⟨33, true, true, true, true, true, true, true, true⟩,
         ⟨33, true, true, true, true, false, false, false, true⟩, rfl, rfl, rfl, rfl⟩

end D0.Extensions.ReadoutRepresentationCategory
