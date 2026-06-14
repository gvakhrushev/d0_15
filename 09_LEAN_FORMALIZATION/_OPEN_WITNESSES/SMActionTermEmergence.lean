import D0.Gauge.SMGaugeDecomposition
import D0.Matter.HiggsScalarProjectorDecision
import Mathlib.Tactic

namespace D0.Gauge

/-- Finite SM-facing action-term labels admitted before smooth EFT dressing. -/
inductive SMFiniteActionTerm where
  | gaugeKinetic
  | fermionKinetic
  | anomalyConstraint
  | scalarProjector
  | yukawaCoupling
  deriving DecidableEq, Repr

/-- Terms forced by the frozen gauge/matter/anomaly ledger before a scalar projector is supplied. -/
def frozenSMActionLedgerWithoutScalar : List SMFiniteActionTerm :=
  [SMFiniteActionTerm.gaugeKinetic,
   SMFiniteActionTerm.fermionKinetic,
   SMFiniteActionTerm.anomalyConstraint]

/-- A finite action ledger derived from the frozen SM-facing decomposition. -/
structure FrozenSMActionLedger where
  decomposition : FrozenSMGaugeDecomposition
  terms : List SMFiniteActionTerm
  terms_eq : terms = frozenSMActionLedgerWithoutScalar

/-- Concrete finite action ledger before scalar-projector promotion. -/
def frozenSMActionLedger : FrozenSMActionLedger where
  decomposition := frozenSMGaugeDecomposition
  terms := frozenSMActionLedgerWithoutScalar
  terms_eq := rfl

/-- The frozen finite action ledger contains exactly the non-scalar gauge/matter/anomaly terms. -/
theorem frozen_sm_action_terms_closed
    (A : FrozenSMActionLedger) :
    A.terms = frozenSMActionLedgerWithoutScalar :=
  A.terms_eq

/-- Scalar and Yukawa terms are not in the non-scalar frozen action ledger. -/
theorem frozen_sm_action_without_scalar_has_no_yukawa_or_scalar
    (A : FrozenSMActionLedger) :
    SMFiniteActionTerm.scalarProjector ∉ A.terms ∧
      SMFiniteActionTerm.yukawaCoupling ∉ A.terms := by
  rw [A.terms_eq]
  constructor <;> decide

/-- A scalar-completed action ledger must carry the constructive Higgs/Yukawa projector certificate. -/
structure ScalarCompletedSMActionLedger where
  base : FrozenSMActionLedger
  projector : D0.Matter.HiggsScalarProjectorCertificate
  terms : List SMFiniteActionTerm
  has_scalar : SMFiniteActionTerm.scalarProjector ∈ terms
  has_yukawa : SMFiniteActionTerm.yukawaCoupling ∈ terms

/-- Scalar/Yukawa action completion requires the constructive scalar-projector certificate. -/
def sm_scalar_yukawa_terms_require_projector
    (A : ScalarCompletedSMActionLedger) :
    D0.Matter.HiggsScalarProjectorCertificate :=
  A.projector

end D0.Gauge
