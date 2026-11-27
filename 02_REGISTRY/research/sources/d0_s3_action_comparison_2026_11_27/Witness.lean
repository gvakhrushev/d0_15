import D0.Algebra.Sedenions

namespace ActionIdentificationWitness

open D0.Algebra.Sedenions
open D0.Algebra.Sedenions.OctonionBranch

/-- The acting permutation group is the same six-element group in both cases. -/
theorem permutation_group_card_six : Fintype.card (Equiv.Perm OctonionBranch) = 6 := by
  decide

/-- Natural and trivial actions of the same group have no injective intertwiner. -/
theorem no_injective_intertwiner_to_trivial :
    ¬ ∃ f : OctonionBranch → OctonionBranch,
      Function.Injective f ∧
      ∀ (σ : Equiv.Perm OctonionBranch) (x : OctonionBranch), f (σ x) = f x := by
  rintro ⟨f, hinjective, hequiv⟩
  have h : f O2 = f O1 := by
    simpa using hequiv (Equiv.swap O1 O2) O1
  have h01 : O2 = O1 := hinjective h
  cases h01

end ActionIdentificationWitness
