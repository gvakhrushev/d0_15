import D0.Foundation.FutureShortlexAdapter

/-!
# Boolean comparison of codes without Boolean outcomes

The supplied theory verification compares records with a Boolean verdict. It
agrees exactly with inequality of the shortlex codes of the complete future
profile. The execution's outcome type is arbitrary. A concrete three-outcome
execution below constructs its own verification witness and encoding.

This is not a physical admissibility or computability claim, and it does not
derive any probability threshold or a unique code ontology.
-/

namespace D0.Foundation.FutureCodeVerdict

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.VerificationCore
open D0.Foundation.FutureShortlexAdapter

variable {Symbol : Type} [LinearOrder Symbol] [WellFoundedLT Symbol]

/-- For a supplied verification and profile-correct code round trip, the
actual record comparison returns true exactly for unequal canonical codes. -/
theorem comparison_true_iff_codes_ne (F : FutureExecution)
    (dec : List Symbol → F.State) (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s)
    (E : TheoryVerification F.futureEmpiricalTheory)
    (l : E.protocol.Line) (cat : E.protocol.Catalogue) (s t : F.State) :
    E.protocol.compare l cat (representedRecord E s) (representedRecord E t) = true ↔
      stateCode F dec enc s ≠ stateCode F dec enc t := by
  rw [representedComparison_iff]
  exact not_congr (stateCode_eq_iff F dec enc correct s t).symm

/-! ## A complete three-outcome realization -/

/-- A finite execution with three actual readout values. -/
def ternaryExecution : FutureExecution where
  State := Fin 3
  Action := Unit
  Test := Unit
  Outcome := Fin 3
  step := fun _ s => s
  observe := fun s _ => s

theorem ternary_run (w : List ternaryExecution.Action) (s : ternaryExecution.State) :
    ternaryExecution.run w s = s := by
  induction w with
  | nil => rfl
  | cons a w ih => exact ih

theorem ternary_profile_eq_iff (s t : ternaryExecution.State) :
    ternaryExecution.profile s = ternaryExecution.profile t ↔ s = t := by
  constructor
  · intro h
    have hread := congrFun (congrFun h []) ()
    simpa [FutureExecution.profile, FutureExecution.run, ternaryExecution] using hread
  · intro h
    cases h
    rfl

private theorem ternary_encoding_sound (s t : ternaryExecution.State)
    (h : signature ternaryExecution.futureEmpiricalTheory s =
      signature ternaryExecution.futureEmpiricalTheory t) : s = t := by
  have hread := congrFun (congrFun h ()) (([], ()) : List ternaryExecution.Action ×
    ternaryExecution.Test)
  change ternaryExecution.profile s [] () = ternaryExecution.profile t [] () at hread
  simpa [FutureExecution.profile, FutureExecution.run, ternaryExecution] using hread

private theorem ternary_encoding_faithful (s t : ternaryExecution.State) (h : s = t) :
    signature ternaryExecution.futureEmpiricalTheory s =
      signature ternaryExecution.futureEmpiricalTheory t := by
  cases h
  rfl

private noncomputable def ternaryEmpiricalRepresentation :
    Fin 3 ≃ EmpiricalState ternaryExecution.futureEmpiricalTheory :=
  (minimalPresentationEquiv ternaryExecution.futureEmpiricalTheory id
    ternary_encoding_sound ternary_encoding_faithful (fun x => ⟨x, rfl⟩)).symm

/-- A real verification witness, including two distinct verification lines. -/
noncomputable def ternaryVerification :
    TheoryVerification ternaryExecution.futureEmpiricalTheory where
  protocol := {
    State := Fin 3
    Record := Fin 3
    Line := Bool
    Catalogue := Unit
    record := id
    compare := fun _ _ x y => decide (x ≠ y)
  }
  contract := {
    state_nontrivial := ⟨0, 1, by decide⟩
    line_nontrivial := ⟨false, true, by decide⟩
    catalogue_nonempty := ⟨()⟩
    correct := by intro line catalogue x y; rfl
  }
  represents := ternaryEmpiricalRepresentation

def ternaryDecode : List (Fin 3) → Fin 3
  | [] => 0
  | a :: _ => a

def ternaryEncode (s : Fin 3) : List (Fin 3) := [s]

theorem ternary_roundtrip (s : ternaryExecution.State) :
    ternaryExecution.profile (ternaryDecode (ternaryEncode s)) = ternaryExecution.profile s := rfl

/-- The concrete comparator and the canonical codes agree for all three
states, both verification lines and the existing catalogue. -/
theorem ternary_comparison_iff_codes_ne (l : ternaryVerification.protocol.Line)
    (cat : ternaryVerification.protocol.Catalogue) (s t : ternaryExecution.State) :
    ternaryVerification.protocol.compare l cat (representedRecord ternaryVerification s)
      (representedRecord ternaryVerification t) = true ↔
      stateCode ternaryExecution ternaryDecode ternaryEncode s ≠
        stateCode ternaryExecution ternaryDecode ternaryEncode t :=
  comparison_true_iff_codes_ne _ _ _ ternary_roundtrip ternaryVerification l cat s t

/-- Each of the three outcomes determines a different complete-future code. -/
theorem ternary_codes_injective :
    Function.Injective (stateCode ternaryExecution ternaryDecode ternaryEncode) := by
  intro s t h
  apply (ternary_profile_eq_iff s t).1
  exact (stateCode_eq_iff _ _ _ ternary_roundtrip s t).1 h

/-- Both truth values occur for the same actual comparator. -/
theorem ternary_comparison_nontrivial :
    ternaryVerification.protocol.compare false () (representedRecord ternaryVerification (0 : Fin 3))
      (representedRecord ternaryVerification (1 : Fin 3)) = true ∧
    ternaryVerification.protocol.compare false () (representedRecord ternaryVerification (0 : Fin 3))
      (representedRecord ternaryVerification (0 : Fin 3)) = false := by
  constructor
  · apply (representedComparison_iff ternaryVerification false () (0 : Fin 3) (1 : Fin 3)).2
    intro h
    have := (ternary_profile_eq_iff (0 : Fin 3) (1 : Fin 3)).1 h
    exact (by decide : (0 : Fin 3) ≠ 1) this
  · have hnot : ¬ ternaryVerification.protocol.compare false ()
        (representedRecord ternaryVerification (0 : Fin 3)) (representedRecord ternaryVerification (0 : Fin 3)) = true := by
      intro h
      exact ((representedComparison_iff ternaryVerification false () (0 : Fin 3) (0 : Fin 3)).1 h) rfl
    cases hcmp : ternaryVerification.protocol.compare false ()
        (representedRecord ternaryVerification (0 : Fin 3)) (representedRecord ternaryVerification (0 : Fin 3)) <;>
      simp_all

end D0.Foundation.FutureCodeVerdict
