import D0.Foundation.ShortlexSetoidCodes
import D0.Foundation.TheoryTransfer

/-!
# Shortlex codes for supplied future executions

A decoder induces an equivalence on words by equality of all admitted future
profiles. A supplied encoder that preserves those profiles gives codes for all
states and makes the existing actions commute with code-level transitions.
These are abstract, conditional constructions: no physical execution, finite
alphabet, admissibility, computable canonicalizer, or encoder is derived.
-/

namespace D0.Foundation.FutureShortlexAdapter

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerificationCore
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.M1ClassAdmissibility

variable {Symbol : Type} [LinearOrder Symbol] [WellFoundedLT Symbol]

/-- Two words are equivalent exactly when their decoded states have the same
complete future profile. -/
def futureWordSetoid (F : FutureExecution) (dec : List Symbol → F.State) :
    Setoid (List Symbol) := Setoid.ker (fun c => F.profile (dec c))

noncomputable def canon (F : FutureExecution) (dec : List Symbol → F.State)
    (c : List Symbol) : List Symbol :=
  (wordClassPresentation (futureWordSetoid F dec)).canon c

theorem canon_eq_iff (F : FutureExecution) (dec : List Symbol → F.State)
    (c d : List Symbol) :
    canon F dec c = canon F dec d ↔ F.profile (dec c) = F.profile (dec d) :=
  wordClass_canon_eq_iff (futureWordSetoid F dec) c d

theorem canon_profile (F : FutureExecution) (dec : List Symbol → F.State)
    (c : List Symbol) : F.profile (dec (canon F dec c)) = F.profile (dec c) :=
  wordClass_canon_related (futureWordSetoid F dec) c

theorem canon_minimal (F : FutureExecution) (dec : List Symbol → F.State)
    (c d : List Symbol) (h : F.profile (dec c) = F.profile (dec d)) :
    ShortlexLE (canon F dec c) d :=
  wordClass_canon_minimal (futureWordSetoid F dec) c d h

noncomputable def stateCode (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol) (s : F.State) : List Symbol :=
  canon F dec (enc s)

/-- A code-level transition derived from supplied encoder, decoder and action. -/
noncomputable def codeStep (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol) (a : F.Action) (c : List Symbol) : List Symbol :=
  canon F dec (enc (F.step a (dec c)))

/-- Only future-profile fidelity of the supplied round trip is required. -/
theorem stateCode_eq_iff (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s) (s t : F.State) :
    stateCode F dec enc s = stateCode F dec enc t ↔ F.profile s = F.profile t := by
  change canon F dec (enc s) = canon F dec (enc t) ↔ _
  rw [canon_eq_iff, correct s, correct t]

/-- Equivalent decoded futures have the same successor code. -/
theorem codeStep_respects_profile (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s)
    (a : F.Action) (c d : List Symbol)
    (h : F.profile (dec c) = F.profile (dec d)) :
    codeStep F dec enc a c = codeStep F dec enc a d := by
  change canon F dec (enc (F.step a (dec c))) = canon F dec (enc (F.step a (dec d)))
  apply (canon_eq_iff F dec _ _).2
  rw [correct, correct]
  exact F.profile_step_congr h a

/-- Every supplied native action commutes with its derived code transition. -/
theorem codeStep_stateCode (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s)
    (a : F.Action) (s : F.State) :
    codeStep F dec enc a (stateCode F dec enc s) = stateCode F dec enc (F.step a s) := by
  change canon F dec (enc (F.step a (dec (canon F dec (enc s))))) =
    canon F dec (enc (F.step a s))
  apply (canon_eq_iff F dec _ _).2
  rw [correct, correct]
  apply F.profile_step_congr
  exact (canon_profile F dec (enc s)).trans (correct s)

/-- With a separately supplied verification, codes identify exactly the
represented persistent records. -/
theorem stateCode_eq_iff_record (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s)
    (E : TheoryVerification F.futureEmpiricalTheory) (s t : F.State) :
    stateCode F dec enc s = stateCode F dec enc t ↔
      representedRecord E s = representedRecord E t := by
  rw [stateCode_eq_iff F dec enc correct, representedRecord_eq_iff]

/-! ## Concrete two-bit examples on existing executions -/

def pairDecode : List Bool → Bool × Bool
  | a :: b :: _ => (a, b)
  | [a] => (a, false)
  | [] => (false, false)

def pairEncode (s : Bool × Bool) : List Bool := [s.1, s.2]

theorem pairDecode_encode (s : Bool × Bool) : pairDecode (pairEncode s) = s := by
  cases s
  rfl

/-- The existing visible-bit execution identifies two distinct raw states. -/
theorem visibleBit_same_code :
    stateCode TheoryTransfer.visibleBitSystem pairDecode pairEncode (false, false) =
      stateCode TheoryTransfer.visibleBitSystem pairDecode pairEncode (false, true) := by
  apply (stateCode_eq_iff _ _ _ (fun s => congrArg _ (pairDecode_encode s)) _ _).2
  exact TheoryTransfer.visibleBit_same_all_source_futures

/-- Its two genuinely different visible outcomes remain different codes. -/
theorem visibleBit_distinct_code :
    stateCode TheoryTransfer.visibleBitSystem pairDecode pairEncode (false, false) ≠
      stateCode TheoryTransfer.visibleBitSystem pairDecode pairEncode (true, false) := by
  intro h
  have hp := (stateCode_eq_iff _ _ _ (fun s => congrArg _ (pairDecode_encode s)) _ _).1 h
  have ho := congrFun (congrFun hp []) ()
  simp [FutureExecution.profile, FutureExecution.run, TheoryTransfer.visibleBitSystem] at ho

/-- A currently hidden bit must remain distinguished when a legal future
action can expose it: a negative control against using current observation. -/
theorem hiddenBit_current_same_but_codes_different :
    hiddenBitExecution.observe (false, false) () = hiddenBitExecution.observe (false, true) () ∧
    stateCode hiddenBitExecution pairDecode pairEncode (false, false) ≠
      stateCode hiddenBitExecution pairDecode pairEncode (false, true) := by
  refine ⟨hiddenBit_same_current, ?_⟩
  intro h
  apply hiddenBit_different_future
  exact (stateCode_eq_iff _ _ _ (fun s => congrArg _ (pairDecode_encode s)) _ _).1 h

end D0.Foundation.FutureShortlexAdapter
