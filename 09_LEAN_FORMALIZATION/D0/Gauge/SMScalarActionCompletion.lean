import D0.Gauge.SMActionTermEmergence
import D0.Matter.HiggsScalarProjectorPositive
import Mathlib.Tactic

namespace D0.Gauge

/-- Scalar/Yukawa-completed finite SM-facing action ledger after the positive projector closure. -/
def frozenSMActionLedgerWithMinimalScalar : List SMFiniteActionTerm :=
  [SMFiniteActionTerm.gaugeKinetic,
   SMFiniteActionTerm.fermionKinetic,
   SMFiniteActionTerm.anomalyConstraint,
   SMFiniteActionTerm.scalarProjector,
   SMFiniteActionTerm.yukawaCoupling]

/-- Concrete scalar-completed action ledger using the constructive rank-two Higgs projector. -/
def minimalScalarCompletedSMActionLedger : ScalarCompletedSMActionLedger where
  base := frozenSMActionLedger
  projector := D0.Matter.minimalPositiveHiggsScalarProjectorCertificate
  terms := frozenSMActionLedgerWithMinimalScalar
  has_scalar := by
    simp [frozenSMActionLedgerWithMinimalScalar]
  has_yukawa := by
    simp [frozenSMActionLedgerWithMinimalScalar]

/-- The constructive scalar projector closes the scalar/Yukawa action-term admission. -/
theorem sm_minimal_scalar_action_terms_closed :
    SMFiniteActionTerm.scalarProjector ∈ minimalScalarCompletedSMActionLedger.terms ∧
      SMFiniteActionTerm.yukawaCoupling ∈ minimalScalarCompletedSMActionLedger.terms := by
  constructor
  · exact minimalScalarCompletedSMActionLedger.has_scalar
  · exact minimalScalarCompletedSMActionLedger.has_yukawa

/-- The scalar-completed action ledger still reads the frozen non-scalar base ledger. -/
theorem sm_scalar_completion_preserves_frozen_base :
    minimalScalarCompletedSMActionLedger.base.terms = frozenSMActionLedgerWithoutScalar := by
  exact minimalScalarCompletedSMActionLedger.base.terms_eq

/-- The scalar/Yukawa completion is not an external mass insertion; it carries the finite projector closure. -/
theorem sm_scalar_completion_uses_minimal_projector :
    minimalScalarCompletedSMActionLedger.projector =
      D0.Matter.minimalPositiveHiggsScalarProjectorCertificate := rfl

/-- The scalar/Yukawa completion carries a rank-two matter-transfer projector. -/
theorem sm_scalar_completion_projector_rank_two :
    minimalScalarCompletedSMActionLedger.projector.witness.rank = 2 := by
  exact minimalScalarCompletedSMActionLedger.projector.witness_rank_two

end D0.Gauge
