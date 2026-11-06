import D0.Foundation.FutureShortlexAdapter
import Mathlib.Data.Set.Countable
import Mathlib.Analysis.Real.Cardinality

/-!
# A cardinality boundary for future-profile codes

When the supplied alphabet is countable, the profile-correct encoder/decoder
assumptions of `FutureShortlexAdapter` imply that the set of distinct complete
future profiles is countable. We explicitly inject the profile range into the
canonical words provided by that adapter. This is a cardinality theorem, not
an algorithm for deciding profile equality or computing canonical codes.

The direct range argument below does not require any ordering on the alphabet.
The real-valued example is an abstract execution with no physical admission
claim. Its complete future profiles distinguish every real state, so it cannot
have such an encoder and decoder over a countable alphabet.
-/

namespace D0.Foundation.FutureProfileCountability

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.FutureShortlexAdapter

variable {Symbol : Type}

/-- Every realized profile occurs in the image of the supplied word decoder;
no ordering or canonical code is needed for this countability conclusion. -/
theorem future_profiles_countable_of_roundtrip [Countable Symbol] (F : FutureExecution)
    (dec : List Symbol → F.State) (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s) :
    (Set.range F.profile).Countable := by
  apply (Set.countable_range (fun c : List Symbol => F.profile (dec c))).mono
  rintro _ ⟨s, rfl⟩
  exact ⟨enc s, correct s⟩

section Shortlex

variable [LinearOrder Symbol] [WellFoundedLT Symbol]

/-- Select one state realizing a profile and take its canonical state code.
The selected representative and the canonical code are both classical. -/
noncomputable def profileCode (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol) (p : Set.range F.profile) : List Symbol :=
  stateCode F dec enc (Classical.choose p.property)

/-- Different realized future profiles cannot have the same canonical word. -/
theorem profileCode_injective (F : FutureExecution) (dec : List Symbol → F.State)
    (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s) :
    Function.Injective (profileCode F dec enc) := by
  rintro ⟨p, hp⟩ ⟨q, hq⟩ hcode
  apply Subtype.ext
  have hprofiles : F.profile (Classical.choose hp) = F.profile (Classical.choose hq) :=
    (stateCode_eq_iff F dec enc correct _ _).1 hcode
  exact (Classical.choose_spec hp).symm.trans (hprofiles.trans (Classical.choose_spec hq))

/-- Countable words therefore support at most countably many distinct realized
future profiles when the stipulated round-trip condition holds. -/
theorem future_profiles_countable [Countable Symbol] (F : FutureExecution)
    (dec : List Symbol → F.State) (enc : F.State → List Symbol)
    (correct : ∀ s, F.profile (dec (enc s)) = F.profile s) :
    (Set.range F.profile).Countable :=
  (profileCode_injective F dec enc correct).countable

end Shortlex

/-! ## A concrete abstract execution with uncountably many profiles -/

def realReadExecution : FutureExecution where
  State := ℝ
  Action := Unit
  Test := Unit
  Outcome := ℝ
  step := fun _ s => s
  observe := fun s _ => s

theorem realRead_profile_injective : Function.Injective realReadExecution.profile := by
  intro s t h
  have hread := congrFun (congrFun h []) ()
  simpa [FutureExecution.profile, FutureExecution.run, realReadExecution] using hread

theorem realRead_profiles_uncountable : ¬ (Set.range realReadExecution.profile).Countable := by
  intro hcount
  letI : Countable (Set.range realReadExecution.profile) := hcount
  have hreal : Countable ℝ :=
    (Set.rangeFactorization_injective.mpr realRead_profile_injective).countable
  exact not_countable hreal

/-- In particular, no total profile-correct encoding/decoding pair over any
countable alphabet can represent this abstract execution. -/
theorem realRead_no_countable_profile_codes [Countable Symbol] :
    ¬ ∃ (dec : List Symbol → realReadExecution.State)
        (enc : realReadExecution.State → List Symbol),
        ∀ s, realReadExecution.profile (dec (enc s)) = realReadExecution.profile s := by
  rintro ⟨dec, enc, correct⟩
  exact realRead_profiles_uncountable
    (future_profiles_countable_of_roundtrip realReadExecution dec enc correct)

end D0.Foundation.FutureProfileCountability
