import D0.Matter.Book04CoefficientOrigin
import D0.Matter.BaryonMultipletBoundary
import D0.Matter.MesonDefectTransferAlgebra
import Mathlib.Tactic

namespace D0.Matter

/--
A finite meson transfer operator must contain the lower-Hodge support, the
typed edge-generation defect-transfer algebra, and transfer-window data.  The
lower Hodge seed alone is not a physical meson mass map.
-/
structure MesonTransferOperator where
  hasLowerHodgeSupport : Prop
  defectTransferAlgebra : Option MesonDefectTransferAlgebraClosure
  hasTransferWindow : Prop

/-- A meson operator has typed defect-transfer algebra only when it carries the closure. -/
def HasMesonDefectTransferAlgebra (O : MesonTransferOperator) : Prop :=
  ∃ C : MesonDefectTransferAlgebraClosure, O.defectTransferAlgebra = some C

/-- Meson mass promotion requires the full chiral/flavour/vector transfer
operator, not only a support eigenvalue. -/
def CanPromoteMesonMasses (O : MesonTransferOperator) : Prop :=
  O.hasLowerHodgeSupport ∧ HasMesonDefectTransferAlgebra O ∧ O.hasTransferWindow

/-- The `400` lower-Hodge seed is support-only. -/
def lowerHodge400SeedOnly : MesonTransferOperator where
  hasLowerHodgeSupport := True
  defectTransferAlgebra := none
  hasTransferWindow := False

/-- A support-only meson seed cannot promote pion/kaon/rho mass rows. -/
theorem lower_hodge_400_cannot_promote_meson_masses :
    ¬ CanPromoteMesonMasses lowerHodge400SeedOnly := by
  simp [CanPromoteMesonMasses, HasMesonDefectTransferAlgebra, lowerHodge400SeedOnly]

/-- Any admissible meson mass promotion must expose the typed defect-transfer algebra. -/
theorem meson_mass_promotion_requires_chiral_flavour_vector_operator
    (O : MesonTransferOperator) :
    CanPromoteMesonMasses O →
      HasMesonDefectTransferAlgebra O ∧ O.hasTransferWindow := by
  intro h
  exact ⟨h.2.1, h.2.2⟩

/--
A scalar/Yukawa bridge capable of promoting Higgs and Yukawa numbers to the
core must contain the constructive scalar-projector closure, a Yukawa section,
a no-second-anchor certificate, and a transfer convention.  Missing any one of
these keeps the row outside the finite core.
-/
structure HiggsYukawaProjectorBridge where
  hasScalarProjector : Prop
  hasYukawaSection : Prop
  hasNoSecondMassAnchor : Prop
  hasTransferConvention : Prop

/-- A bridge has a scalar projector only when it carries the rank-2 SU(2)-compatible projector closure
(owned by `D0.Matter.HiggsScalarProjectorConstructive`: `rank2_scalar_projector_exists`). -/
def HasConstructiveScalarProjector (B : HiggsYukawaProjectorBridge) : Prop :=
  B.hasScalarProjector

/-- Higgs/Yukawa core promotion requires all scalar-projector bridge data. -/
def CanPromoteHiggsYukawaCore (B : HiggsYukawaProjectorBridge) : Prop :=
  HasConstructiveScalarProjector B ∧ B.hasYukawaSection ∧
    B.hasNoSecondMassAnchor ∧ B.hasTransferConvention

/-- The present scalar row without a scalar projector is a comparison boundary,
not a core theorem. -/
def missingScalarProjectorBridge : HiggsYukawaProjectorBridge where
  hasScalarProjector := False
  hasYukawaSection := False
  hasNoSecondMassAnchor := False
  hasTransferConvention := False

/-- Any promoted Higgs/Yukawa row must first expose its constructive scalar closure. -/
theorem higgs_yukawa_requires_scalar_projector
    (B : HiggsYukawaProjectorBridge) :
    CanPromoteHiggsYukawaCore B → HasConstructiveScalarProjector B := by
  intro h
  exact h.1

/-- Without a scalar projector, Higgs/Yukawa comparison cannot become core. -/
theorem missing_scalar_projector_cannot_promote_higgs_yukawa_core :
    ¬ CanPromoteHiggsYukawaCore missingScalarProjectorBridge := by
  simp [CanPromoteHiggsYukawaCore, HasConstructiveScalarProjector, missingScalarProjectorBridge]

/--
A compact object collecting the Book 04 operator-boundary no-go statements.
This is the v14 replacement for leaving meson/baryon/Higgs rows as ambiguous
"future status" items.
-/
structure Book04OperatorBoundaryClosed where
  baryonBoundary : ¬ CanPromoteBaryonMultiplet nucleonLineOnlyBaryonOperator
  mesonBoundary : ¬ CanPromoteMesonMasses lowerHodge400SeedOnly
  higgsBoundary : ¬ CanPromoteHiggsYukawaCore missingScalarProjectorBridge

/-- Concrete Book 04 operator-boundary closure witness. -/
def book04OperatorBoundaryClosed : Book04OperatorBoundaryClosed where
  baryonBoundary := nucleon_line_cannot_promote_full_baryon_multiplet
  mesonBoundary := lower_hodge_400_cannot_promote_meson_masses
  higgsBoundary := missing_scalar_projector_cannot_promote_higgs_yukawa_core

/-- Final owner for the Book 04 meson/baryon/Higgs boundaries. -/
def book04_operator_boundaries_closed : Book04OperatorBoundaryClosed :=
  book04OperatorBoundaryClosed

end D0.Matter

-- BaryonMultipletOperator
-- CanPromoteBaryonMultiplet
