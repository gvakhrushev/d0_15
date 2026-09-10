import Mathlib.Tactic

/-! An injective complete dynamics cannot reset distinguishable inputs unless
their distinction survives in another component. This is a finite information
statement, not an assumed thermodynamic law or an empirical bound. -/

namespace D0.Representation.PreparationMemoryBound

theorem reset_requires_injective_archive {S E : Type*}
    (U : S × E → S × E) (hU : Function.Injective U)
    (target : S) (initial : E) (archive : S → E)
    (h : ∀ x, U (x,initial) = (target, archive x)) :
    Function.Injective archive := by
  intro x y he
  have hu : U (x,initial) = U (y,initial) := by rw [h, h, he]
  exact congrArg Prod.fst (hU hu)

theorem archive_capacity_bound {S E : Type*} [Fintype S] [Fintype E]
    (U : S × E → S × E) (hU : Function.Injective U)
    (target : S) (initial : E) (archive : S → E)
    (h : ∀ x, U (x,initial) = (target, archive x)) :
    Fintype.card S ≤ Fintype.card E :=
  Fintype.card_le_of_injective archive
    (reset_requires_injective_archive U hU target initial archive h)

/-- Swapping supplies a reset using an ALREADY PREPARED resource, while retaining
the old state. It does not manufacture a fresh blank resource. -/
theorem swap_prepares_and_keeps_history {S : Type*} (x blank : S) :
    Equiv.prodComm S S (x,blank) = (blank,x) := rfl

/-- An independently initialized detector cannot distinguish signal inputs under
product dynamics. Distinguishability forces SOME interaction, not a unique law. -/
theorem comparison_requires_interaction {S E : Type*}
    (U : S × E → S × E) (initial : E) (s t : S)
    (hd : (U (s,initial)).2 ≠ (U (t,initial)).2) :
    ¬ ∃ f : S → S, ∃ g : E → E, ∀ x, U x = (f x.1, g x.2) := by
  rintro ⟨f,g,h⟩
  apply hd
  rw [h, h]

end D0.Representation.PreparationMemoryBound
