import D0.Representation.PreparationMemoryBound

/-!
# Information accounting for a general retained/archived update

Global injectivity is equivalent to archive injectivity on each fiber of the visible map.
Closedness of the carrier alone is not injectivity: a constant self-map supplies a control.
These are classical distinguishable-state statements; quantum correlations require the
full joint density operator rather than a pair of reduced density operators.
-/
namespace D0.Representation.ArchiveFiberConservation

def completeUpdate {S V A : Type*} (visible : S → V) (archive : S → A) : S → V × A :=
  fun s => (visible s,archive s)

theorem conservation_iff_fiber_separation {S V A : Type*}
    (visible : S → V) (archive : S → A) :
    Function.Injective (completeUpdate visible archive) ↔
      ∀ s t, visible s = visible t → archive s = archive t → s = t := by
  constructor
  · intro h s t hv ha
    exact h (Prod.ext hv ha)
  · intro h s t he
    exact h s t (congrArg Prod.fst he) (congrArg Prod.snd he)

/-- Every distinction erased by the retained map must remain in the archive. -/
theorem visible_collision_requires_archive_distinction {S V A : Type*}
    (visible : S → V) (archive : S → A)
    (h : Function.Injective (completeUpdate visible archive))
    {s t : S} (hne : s ≠ t) (hv : visible s = visible t) :
    archive s ≠ archive t := by
  intro ha
  exact hne ((conservation_iff_fiber_separation visible archive).mp h s t hv ha)

/-- The archive must fit every class of inputs with the same visible output. -/
theorem archive_fiber_capacity {S V A : Type*} [Fintype S] [Fintype A]
    (visible : S → V) (archive : S → A)
    (h : Function.Injective (completeUpdate visible archive)) (v : V)
    [DecidablePred (fun s => visible s = v)] :
    Fintype.card {s : S // visible s = v} ≤ Fintype.card A := by
  apply Fintype.card_le_of_injective (fun s : {s : S // visible s = v} => archive s.1)
  intro s t ha
  apply Subtype.ext
  exact (conservation_iff_fiber_separation visible archive).mp h s.1 t.1
    (s.2.trans t.2.symm) ha

/-- Exact sufficient archive as a dependent residual: store the input's position in its fiber.
This is a mathematical reversible encoding, not a minimal physical preparation construction. -/
def fiberEncoding {S V : Type*} (visible : S → V) :
    S ≃ (Σ v : V, {s : S // visible s = v}) where
  toFun s := ⟨visible s,s,rfl⟩
  invFun pair := pair.2.1
  left_inv := fun _ => rfl
  right_inv := by
    rintro ⟨v,s,h⟩
    subst v
    rfl

/-- Loss relative to the visible response can be total while complete evolution is reversible. -/
theorem complete_reset_example :
    Function.Injective (fun b : Bool => (false,b)) ∧
    ¬ Function.Injective (fun _ : Bool => false) := by
  constructor
  · intro s t h
    exact congrArg Prod.snd h
  · intro h
    have he : false = true := @h false true rfl
    cases he

/-- A self-map has no external output but can still merge inputs. Thus absence of an outside
does not, by itself, prove an information-preserving dynamical law. -/
theorem closed_carrier_not_sufficient :
    ∃ update : Bool → Bool, ¬ Function.Injective update :=
  ⟨fun _ => false, complete_reset_example.2⟩

end D0.Representation.ArchiveFiberConservation
