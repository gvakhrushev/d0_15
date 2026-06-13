import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

namespace D0.Matter

/--
A finite physical selector is a rational score functional on a finite candidate
set.  The file is deliberately generic: charged-lepton, nucleon, hadron, and EW
selectors must instantiate this finite selector spine instead of introducing a
free phenomenological choice.
-/
structure FiniteSelector (α : Type) where
  support_fintype : Fintype α
  score : α → ℚ

/-- A finite selector really has finite support; this prevents Book 04 selectors from
being only a label over an uncontrolled candidate universe. -/
def finiteSelectorSupportFintype {α : Type} (S : FiniteSelector α) : Fintype α :=
  S.support_fintype

/--
A candidate is strictly selected when its score is strictly smaller than every
other candidate.  Strictness is the Lean-side replacement for informal phrases
such as "the selector chooses this state".
-/
structure StrictSelected {α : Type} (S : FiniteSelector α) (a : α) : Prop where
  strict_min : ∀ b, b ≠ a → S.score a < S.score b

/--
Strict finite selectors have at most one selected candidate.  This is the core
anti-numerology theorem for Book 04-style selectors: a physical state cannot be
picked twice unless the two picks are definitionally the same candidate.
-/
theorem strict_selected_unique {α : Type} (S : FiniteSelector α) {a b : α}
    (ha : StrictSelected S a) (hb : StrictSelected S b) : a = b := by
  by_contra hne_ab
  have hne_ba : b ≠ a := by
    intro hba
    exact hne_ab hba.symm
  have hab : S.score a < S.score b := ha.strict_min b hne_ba
  have hba : S.score b < S.score a := hb.strict_min a hne_ab
  exact (not_lt_of_ge (le_of_lt hba)) hab

/--
Once a candidate is strictly selected, every different candidate is ruled out as
a simultaneous strict selection for the same selector.
-/
theorem no_alternative_strict_selected {α : Type} (S : FiniteSelector α) {a b : α}
    (ha : StrictSelected S a) (hba : b ≠ a) : ¬ StrictSelected S b := by
  intro hb
  exact hba (strict_selected_unique S hb ha)

/--
A selector certificate is the minimal finite-core object needed before a Book
04 physical claim may be treated as selected rather than fitted.
-/
structure StrictSelectorCertificate (α : Type) where
  selector : FiniteSelector α
  selected : α
  selected_strict : StrictSelected selector selected

/-- The selected object of a strict selector certificate is unique. -/
theorem strict_selector_certificate_unique {α : Type}
    (C D : StrictSelectorCertificate α) (hsame : C.selector = D.selector) :
    C.selected = D.selected := by
  have hD_on_C : StrictSelected C.selector D.selected := by
    rw [hsame]
    exact D.selected_strict
  exact strict_selected_unique C.selector C.selected_strict hD_on_C

/--
Strict selection is invariant under pointwise-identical score functions.  Thus a
rewriting of notation, units, or bookkeeping cannot change the selected state
unless the score functional itself changes.
-/
theorem strict_selected_transport_of_same_scores {α : Type}
    (S T : FiniteSelector α) (hscore : ∀ x, T.score x = S.score x)
    {a : α} (ha : StrictSelected S a) : StrictSelected T a := by
  constructor
  intro b hb
  rw [hscore a, hscore b]
  exact ha.strict_min b hb

/--
Two strict selector certificates with the same pointwise scores select the same
candidate.  This is the formal no-free-retuning statement for finite physical
selectors.
-/
theorem selector_certificate_same_scores_same_selected {α : Type}
    (C D : StrictSelectorCertificate α)
    (hscore : ∀ x, C.selector.score x = D.selector.score x) :
    C.selected = D.selected := by
  have hD_on_C : StrictSelected C.selector D.selected :=
    strict_selected_transport_of_same_scores D.selector C.selector hscore D.selected_strict
  exact strict_selected_unique C.selector C.selected_strict hD_on_C

/--
A different selected candidate requires a genuine score deformation.  Cosmetic
rewriting of the same selector cannot move the selected state.
-/
theorem different_selection_requires_score_change {α : Type}
    (C D : StrictSelectorCertificate α) (hdiff : C.selected ≠ D.selected) :
    ¬ ∀ x, C.selector.score x = D.selector.score x := by
  intro hsame
  exact hdiff (selector_certificate_same_scores_same_selected C D hsame)

/--
Book-04 selector hardening: a physical selector claim is closed only by a strict
finite selector certificate, and no alternative candidate can be selected under
the same finite score functional.
-/
theorem physical_selector_no_free_alternative {α : Type}
    (C : StrictSelectorCertificate α) (b : α) (hb : b ≠ C.selected) :
    ¬ StrictSelected C.selector b := by
  exact no_alternative_strict_selected C.selector C.selected_strict hb

end D0.Matter
