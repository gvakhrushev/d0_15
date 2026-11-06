import D0.Foundation.InterpretedFutureMemoryBound

/-!
# Native and common future memory for the extra-bit execution

The native execution has a Boolean test for each of its two retained bits.
All native future profiles separate the four raw states, while the interpreted
common test only sees the first bit. The finite bounds below concern complete
profile decoding in these explicit abstract systems. They say nothing about
physical admission, computational cost, clock, work, or quantum memory.
-/

namespace D0.Foundation.ExtraBitNativeMemory

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.TheoryTransfer
open D0.Foundation.FutureMemoryQuotientBound
open D0.Foundation.InterpretedFutureMemoryBound

/-- Testing both Boolean test values at the empty word distinguishes every
native raw state. -/
theorem extraBit_profile_injective : Function.Injective extraBitTestSystem.profile := by
  intro s t h
  have h₀ := congrFun (congrFun h []) false
  have h₁ := congrFun (congrFun h []) true
  apply Prod.ext
  · simpa [FutureExecution.profile, FutureExecution.run, extraBitTestSystem] using h₀
  · simpa [FutureExecution.profile, FutureExecution.run, extraBitTestSystem] using h₁

/-- The full native future quotient is exactly the pair of raw bits. -/
noncomputable def extraBitFutureEquivPair : extraBitTestSystem.FutureClass ≃ Bool × Bool :=
  (Equiv.ofBijective
    (fun s : extraBitTestSystem.State =>
      (Quotient.mk extraBitTestSystem.futureSetoid s : extraBitTestSystem.FutureClass))
    ⟨by
      intro s t h
      exact extraBit_profile_injective (Quotient.exact h),
     by
      intro q
      exact Quotient.inductionOn q (fun s => ⟨s, rfl⟩)⟩).symm

noncomputable instance extraBitFutureClassFintype : Fintype extraBitTestSystem.FutureClass :=
  Fintype.ofEquiv (Bool × Bool) extraBitFutureEquivPair.symm

theorem extraBit_native_future_card : Fintype.card extraBitTestSystem.FutureClass = 4 := by
  rw [Fintype.card_congr extraBitFutureEquivPair]
  decide

/-- Every finite memory that recovers all native profiles has at least four
values. This applies the generic quotient-level bound to the full native tests. -/
theorem extraBit_native_memory_lower_bound {Memory : Type} [Fintype Memory]
    (encode : extraBitTestSystem.State → Memory)
    (decode : Memory → List extraBitTestSystem.Action → extraBitTestSystem.Test →
      extraBitTestSystem.Outcome)
    (correct : ∀ s, decode (encode s) = extraBitTestSystem.profile s) :
    4 ≤ Fintype.card Memory := by
  simpa [extraBit_native_future_card] using
    futureClass_card_le_memory extraBitTestSystem encode decode correct

/-- No admitted action changes either retained bit. -/
theorem extraBit_run (w : List extraBitTestSystem.Action) (s : extraBitTestSystem.State) :
    extraBitTestSystem.run w s = s := by
  induction w with
  | nil => rfl
  | cons a w ih => exact ih

def extraBit_pair_encode : extraBitTestSystem.State → Bool × Bool := fun s => s

def extraBit_pair_decode : Bool × Bool → List extraBitTestSystem.Action →
    extraBitTestSystem.Test → extraBitTestSystem.Outcome :=
  fun s _ test => if (show Bool from test) then s.2 else s.1

theorem extraBit_pair_correct (s : extraBitTestSystem.State) :
    extraBit_pair_decode (extraBit_pair_encode s) = extraBitTestSystem.profile s := by
  funext w test
  change (if (show Bool from test) then s.2 else s.1) =
    extraBitTestSystem.observe (extraBitTestSystem.run w s) test
  rw [extraBit_run]
  rfl

/-- The full-native lower bound is attained by retaining the pair. -/
theorem extraBit_native_bound_attained :
    (∀ s, extraBit_pair_decode (extraBit_pair_encode s) = extraBitTestSystem.profile s) ∧
      Fintype.card (Bool × Bool) = 4 :=
  ⟨extraBit_pair_correct, by decide⟩

/-- The established common-interface bit decoder attains two values, while
native decoding of the same native carrier attains its bound at four. -/
theorem common_vs_native_bounds_attained :
    (∀ s, commonVisibleDecode (commonVisibleEncode s) =
      visibleBitInterpretation.commonExecution.profile s) ∧
    Fintype.card Bool = 2 ∧
    (∀ s, extraBit_pair_decode (extraBit_pair_encode s) = extraBitTestSystem.profile s) ∧
    Fintype.card (Bool × Bool) = 4 := by
  exact ⟨commonVisible_bound_attained.1, commonVisible_bound_attained.2,
    extraBit_native_bound_attained.1, extraBit_native_bound_attained.2⟩

end D0.Foundation.ExtraBitNativeMemory
