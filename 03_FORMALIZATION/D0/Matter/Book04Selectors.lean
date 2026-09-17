import D0.Matter.FiniteSelector

namespace D0.Matter

/--
The Book 04 physical sectors that are allowed to use the finite selector spine.
This is intentionally only a sector tag: the numerical/certified content must be
supplied by a `StrictSelected` certificate, not by the tag itself.
-/
inductive Book04PhysicalSector where
  | chargedLepton
  | proton
  | neutron
  | hadron
  | electroweak
  deriving DecidableEq, Repr

/--
A Book 04 physical selection claim is release-level finite-core material only
when it carries a strict selector certificate.  This prevents lepton, nucleon,
hadron, or EW statements from entering the core as informal chosen values.
-/
structure Book04SelectorClaim where
  sector : Book04PhysicalSector
  Candidate : Type
  selector : FiniteSelector Candidate
  selected : Candidate
  selected_strict : StrictSelected selector selected

/-- Forget the Book 04 label and keep the hard finite selector certificate. -/
def Book04SelectorClaim.toCertificate (C : Book04SelectorClaim) :
    StrictSelectorCertificate C.Candidate where
  selector := C.selector
  selected := C.selected
  selected_strict := C.selected_strict

/--
A Book 04 claim with a strict finite certificate has no alternative selected
candidate under the same selector.
-/
theorem book04_selector_claim_no_free_alternative
    (C : Book04SelectorClaim) (b : C.Candidate) (hb : b ≠ C.selected) :
    ¬ StrictSelected C.selector b := by
  exact physical_selector_no_free_alternative C.toCertificate b hb

/--
If a Book 04 claim is moved to a different selected candidate, the finite score
functional must have changed.  A cosmetic rewriting cannot do it.
-/
theorem book04_different_selected_requires_score_change
    (C : Book04SelectorClaim) (D : StrictSelectorCertificate C.Candidate)
    (hdiff : C.selected ≠ D.selected) :
    ¬ ∀ x, C.selector.score x = D.selector.score x := by
  exact different_selection_requires_score_change C.toCertificate D hdiff

end D0.Matter
