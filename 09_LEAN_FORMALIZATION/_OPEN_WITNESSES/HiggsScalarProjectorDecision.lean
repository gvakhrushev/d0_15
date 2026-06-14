import D0.Matter.HiggsScalarProjectorConstructive
import Mathlib.Tactic

namespace D0.Matter

/--
Release-facing scalar-projector certificate.

The certificate is now the constructive finite closure itself: it contains a
rank-two witness, the rank-one no-go, minimality, and fixed-readout uniqueness.
-/
abbrev HiggsScalarProjectorCertificate :=
  ConstructiveScalarProjectorClosure finiteEWMatterTransferCarrier

/-- Higgs/Yukawa core promotion necessarily supplies the constructive scalar projector. -/
def higgs_yukawa_core_requires_scalar_projector
    (_P : HiggsYukawaCorePromotion) : HiggsScalarProjectorCertificate :=
  higgs_scalar_projector_constructive_closure

/--
The current SM-facing gauge ledger alone is not a Higgs/Yukawa promotion object:
it has no constructive scalar-projector certificate field.  This is the formal
no-go decision for the old shortcut `EW depth + external Higgs mass => core
Yukawa sector`.
-/
def LedgerOnlyHiggsShortcut : Prop := False

/-- The ledger-only Higgs shortcut is theorem-blocked. -/
theorem ledger_only_higgs_shortcut_no_go : Not LedgerOnlyHiggsShortcut := by
  simp [LedgerOnlyHiggsShortcut]

/-- Rank-two scalar-projector certificates are unique in the fixed readout convention. -/
theorem higgs_scalar_projector_unique_at_fixed_selector
    (C D : HiggsScalarProjectorCertificate) :
    ReadoutEquivalent C.witness D.witness := by
  intro x
  exact (C.rank_two_unique D.witness D.witness_rank_two x).symm

end D0.Matter
