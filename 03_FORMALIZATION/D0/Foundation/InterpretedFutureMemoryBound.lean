import D0.Foundation.FutureMemoryQuotientBound

/-!
# Interpreted future classes impose a memory bound

The common execution exposes only interpreted source operations and tests on
native states. Its correct future decoder must retain all source future classes.
This does not assert coverage of extra native contexts or any physical resource
selection, effective coding procedure, time, work, or cost.
-/

namespace D0.Foundation.InterpretedFutureMemoryBound

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.TheoryTransfer
open D0.Foundation.FutureMemoryQuotientBound

/-- Compose the proved map of source classes with the existing selected memory
representatives of the common execution. -/
noncomputable def interpretedClassMemory {F G : FutureExecution}
    (I : Interpretation F G) {Memory : Type} (encode : G.State → Memory) :
    F.FutureClass → Memory :=
  memoryOfFutureClass I.commonExecution encode ∘ I.futureMap

/-- Memory which decodes every common-execution profile separates every source
future class, without demanding a raw-state injection or native coverage. -/
theorem interpretedClassMemory_injective {F G : FutureExecution}
    (I : Interpretation F G) {Memory : Type} (encode : G.State → Memory)
    (decode : Memory → List F.Action → F.Test → G.Outcome)
    (correct : ∀ s : G.State, decode (encode s) = I.commonExecution.profile s) :
    Function.Injective (interpretedClassMemory I encode) :=
  (memoryOfFutureClass_injective I.commonExecution encode decode correct).comp
    I.futureMap_injective

/-- Finite memory which decodes the common execution has at least as many
values as there are source future classes. The common quotient itself need not
be finite. -/
theorem sourceFutureClass_card_le_commonMemory {F G : FutureExecution}
    (I : Interpretation F G) [Fintype F.FutureClass] {Memory : Type}
    [Fintype Memory] (encode : G.State → Memory)
    (decode : Memory → List F.Action → F.Test → G.Outcome)
    (correct : ∀ s : G.State, decode (encode s) = I.commonExecution.profile s) :
    Fintype.card F.FutureClass ≤ Fintype.card Memory :=
  Fintype.card_le_of_injective (interpretedClassMemory I encode)
    (interpretedClassMemory_injective I encode decode correct)

/-! ## The visible-bit interpretation and its extra native test -/

def commonVisibleEncode : extraBitTestSystem.State → Bool := fun s => s.1

def commonVisibleDecode : Bool → List visibleBitSystem.Action → visibleBitSystem.Test →
    extraBitTestSystem.Outcome := fun b _ _ => b

/-- This one-bit memory recovers all profiles of the common source interface. -/
theorem commonVisible_correct (s : extraBitTestSystem.State) :
    commonVisibleDecode (commonVisibleEncode s) =
      visibleBitInterpretation.commonExecution.profile s := by
  funext w t
  have h := congrFun (congrFun (visibleMemory_correct s) w) t
  have hcomm := visibleBitInterpretation.common_profile_commutes s w t
  change visibleBitInterpretation.commonExecution.profile s w t =
    visibleBitSystem.profile s w t at hcomm
  exact h.trans hcomm.symm

/-- Every finite memory recovering this common interface needs two values. -/
theorem commonVisible_memory_lower_bound {Memory : Type} [Fintype Memory]
    (encode : extraBitTestSystem.State → Memory)
    (decode : Memory → List visibleBitSystem.Action → visibleBitSystem.Test →
      extraBitTestSystem.Outcome)
    (correct : ∀ s : extraBitTestSystem.State,
      decode (encode s) = visibleBitInterpretation.commonExecution.profile s) :
    2 ≤ Fintype.card Memory := by
  simpa [visible_future_class_card] using
    sourceFutureClass_card_le_commonMemory visibleBitInterpretation encode decode correct

/-- The lower bound for the common interface is achieved by the explicit bit. -/
theorem commonVisible_bound_attained :
    (∀ s, commonVisibleDecode (commonVisibleEncode s) =
      visibleBitInterpretation.commonExecution.profile s) ∧ Fintype.card Bool = 2 :=
  ⟨commonVisible_correct, by decide⟩

/-- No decoder of the retained first bit can recover every *native* profile:
the extra native test distinguishes a pair collapsed by this encoding. -/
theorem commonVisible_encode_not_native_sufficient
    (decode : Bool → List extraBitTestSystem.Action → extraBitTestSystem.Test →
      extraBitTestSystem.Outcome) :
    ¬ ∀ s : extraBitTestSystem.State,
      decode (commonVisibleEncode s) = extraBitTestSystem.profile s := by
  intro correct
  apply extraBit_different_native_futures
  exact (correct (false, false)).symm.trans (correct (false, true))

/-- This interpretation really lacks the stronger full-native coverage. -/
theorem commonVisible_not_native_coverage :
    ¬ Nonempty (NativeContextCoverage visibleBitInterpretation) :=
  extra_native_test_prevents_coverage

end D0.Foundation.InterpretedFutureMemoryBound
