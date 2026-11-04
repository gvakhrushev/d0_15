import D0.Foundation.TheoryTransfer

/-!
# Finite memory required for distinct complete future profiles

A correct decoder of every complete future profile needs at least one memory
value per future-equivalence class, even when raw states have identical futures.
The representative choice is classical; no quotient-respecting encoder or
computable choice is assumed. The example is an abstract execution, not a claim
that a physical D0 process supplies this memory or its cost.
-/

namespace D0.Foundation.FutureMemoryQuotientBound

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.TheoryTransfer

/-- Choose a representative only to embed future classes in sufficient memory. -/
noncomputable def memoryOfFutureClass (F : FutureExecution) {Memory : Type}
    (encode : F.State → Memory) : F.FutureClass → Memory :=
  fun q => encode (Quotient.out q)

/-- A decoder correct on every native state makes the chosen memory values
injective on future classes. The encoder need not be constant on each class. -/
theorem memoryOfFutureClass_injective (F : FutureExecution) {Memory : Type}
    (encode : F.State → Memory)
    (decode : Memory → List F.Action → F.Test → F.Outcome)
    (correct : ∀ s, decode (encode s) = F.profile s) :
    Function.Injective (memoryOfFutureClass F encode) := by
  intro q r h
  have hclass := F.sufficient_memory_reflects_future encode decode correct h
  simpa using hclass

/-- A finite memory with a correct complete-future decoder has at least as
many values as the canonical quotient of future-equivalent native states. -/
theorem futureClass_card_le_memory (F : FutureExecution) [Fintype F.FutureClass]
    {Memory : Type} [Fintype Memory] (encode : F.State → Memory)
    (decode : Memory → List F.Action → F.Test → F.Outcome)
    (correct : ∀ s, decode (encode s) = F.profile s) :
    Fintype.card F.FutureClass ≤ Fintype.card Memory :=
  Fintype.card_le_of_injective (memoryOfFutureClass F encode)
    (memoryOfFutureClass_injective F encode decode correct)

/-- Quotient of the concrete two-raw-bit system by all admitted futures. -/
noncomputable def visibleFutureEquivBool : visibleBitSystem.FutureClass ≃ Bool where
  toFun := Quotient.lift (fun s => s.1) (by
    intro s t h
    have hread := congrFun (congrFun h []) ()
    simpa [FutureExecution.profile, FutureExecution.run, visibleBitSystem] using hread)
  invFun := fun b => Quotient.mk visibleBitSystem.futureSetoid (b, false)
  left_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro s
    apply Quotient.sound
    funext w t
    change visibleBitSystem.observe (visibleBitSystem.run w (s.1, false)) t =
      visibleBitSystem.observe (visibleBitSystem.run w s) t
    rw [visibleBit_run, visibleBit_run]
    rfl
  right_inv := by intro b; rfl

noncomputable instance visibleFutureClassFintype : Fintype visibleBitSystem.FutureClass :=
  Fintype.ofEquiv Bool visibleFutureEquivBool.symm

instance visibleStateFintype : Fintype visibleBitSystem.State :=
  inferInstanceAs (Fintype (Bool × Bool))

theorem visible_raw_state_card : Fintype.card visibleBitSystem.State = 4 := by
  decide

theorem visible_future_class_card : Fintype.card visibleBitSystem.FutureClass = 2 := by
  rw [Fintype.card_congr visibleFutureEquivBool]
  decide

def visibleMemoryEncode : visibleBitSystem.State → Bool := fun s => s.1

def visibleMemoryDecode : Bool → List visibleBitSystem.Action → visibleBitSystem.Test →
    visibleBitSystem.Outcome := fun b _ _ => b

theorem visibleMemory_correct (s : visibleBitSystem.State) :
    visibleMemoryDecode (visibleMemoryEncode s) = visibleBitSystem.profile s := by
  funext w t
  change s.1 = visibleBitSystem.observe (visibleBitSystem.run w s) t
  rw [visibleBit_run]
  rfl

/-- Two memory values are necessary for any full-future decoder of this system. -/
theorem visible_memory_lower_bound {Memory : Type} [Fintype Memory]
    (encode : visibleBitSystem.State → Memory)
    (decode : Memory → List visibleBitSystem.Action → visibleBitSystem.Test →
      visibleBitSystem.Outcome)
    (correct : ∀ s, decode (encode s) = visibleBitSystem.profile s) :
    2 ≤ Fintype.card Memory := by
  simpa [visible_future_class_card] using
    futureClass_card_le_memory visibleBitSystem encode decode correct

/-- The bound is attained by the explicit one-bit memory above. -/
theorem visible_memory_bound_attained :
    (∀ s, visibleMemoryDecode (visibleMemoryEncode s) = visibleBitSystem.profile s) ∧
      Fintype.card Bool = 2 := by
  exact ⟨visibleMemory_correct, by decide⟩

end D0.Foundation.FutureMemoryQuotientBound
