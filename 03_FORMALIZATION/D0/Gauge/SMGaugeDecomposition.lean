import D0.Gauge.AnomalySums
import D0.Gauge.SMCharges

namespace D0.Gauge

/-- The finite gauge-factor labels used by the D0 SM-facing carrier ledger. -/
inductive SMGaugeFactor where
  | su3
  | su2
  | u1
  deriving DecidableEq, Repr

/-- Frozen finite gauge-factor ledger: color, weak isospin, hypercharge. -/
def frozenSMGaugeFactorLedger : List SMGaugeFactor :=
  [SMGaugeFactor.su3, SMGaugeFactor.su2, SMGaugeFactor.u1]

/--
A finite Standard-Model-facing gauge decomposition candidate.

This is intentionally still finite: a list of factor labels plus a one-generation
Weyl ledger and exact rational anomaly checks.  Smooth QFT/EFT data may only be
attached after such a finite ledger is frozen.
-/
structure FrozenSMGaugeDecomposition where
  factors : List SMGaugeFactor
  representationLedger : List D0.WeylField
  factors_frozen : factors = frozenSMGaugeFactorLedger
  representation_frozen : representationLedger = D0.generation
  grav_anomaly_zero : D0.gravU1Sum = 0
  cubic_anomaly_zero : D0.cubicU1Sum = 0
  su2_anomaly_zero : D0.su2su2u1Sum = 0
  su3_anomaly_zero : D0.su3su3u1Sum = 0

/-- Concrete frozen SM-facing finite ledger. -/
def frozenSMGaugeDecomposition : FrozenSMGaugeDecomposition where
  factors := frozenSMGaugeFactorLedger
  representationLedger := D0.generation
  factors_frozen := rfl
  representation_frozen := rfl
  grav_anomaly_zero := D0.grav_U1_anomaly_sum
  cubic_anomaly_zero := D0.U1_cubic_anomaly_sum
  su2_anomaly_zero := D0.SU2_SU2_U1_anomaly_sum
  su3_anomaly_zero := D0.SU3_SU3_U1_anomaly_sum

/-- The frozen finite carrier has exactly the SM-facing gauge-factor ledger. -/
theorem frozen_sm_gauge_factors_closed :
    frozenSMGaugeDecomposition.factors = frozenSMGaugeFactorLedger :=
  frozenSMGaugeDecomposition.factors_frozen

/-- The frozen finite matter ledger is exactly the one-generation Weyl ledger. -/
theorem frozen_sm_generation_ledger_closed :
    frozenSMGaugeDecomposition.representationLedger = D0.generation :=
  frozenSMGaugeDecomposition.representation_frozen

/-- Exact rational anomaly cancellation for the frozen one-generation ledger. -/
theorem frozen_sm_generation_anomaly_free :
    D0.gravU1Sum = 0 ∧
      D0.cubicU1Sum = 0 ∧
        D0.su2su2u1Sum = 0 ∧
          D0.su3su3u1Sum = 0 := by
  exact ⟨frozenSMGaugeDecomposition.grav_anomaly_zero,
    frozenSMGaugeDecomposition.cubic_anomaly_zero,
      frozenSMGaugeDecomposition.su2_anomaly_zero,
        frozenSMGaugeDecomposition.su3_anomaly_zero⟩

/--
At a frozen finite ledger, a different gauge-factor list is not another D0 core
solution.  It is a different carrier attempt and must be treated as a new bridge
or no-go target.
-/
theorem no_alternative_sm_factors_at_frozen_ledger
    (F : List SMGaugeFactor) (hF : F ≠ frozenSMGaugeFactorLedger) :
    ¬ ∃ C : FrozenSMGaugeDecomposition, C.factors = F := by
  intro h
  rcases h with ⟨C, hC⟩
  apply hF
  exact hC.symm.trans C.factors_frozen

/--
At a frozen finite ledger, a different one-generation representation list is not
an internal SM-facing decomposition with the same proof owner.
-/
theorem no_alternative_sm_generation_ledger_at_frozen_decomposition
    (R : List D0.WeylField) (hR : R ≠ D0.generation) :
    ¬ ∃ C : FrozenSMGaugeDecomposition, C.representationLedger = R := by
  intro h
  rcases h with ⟨C, hC⟩
  apply hR
  exact hC.symm.trans C.representation_frozen

/--
A finite SM/EFT comparison bridge is admissible only after the finite gauge and
matter ledgers are frozen.  This object deliberately contains no fitted masses,
running couplings or survey/collider data.
-/
structure SMEFTBridgeAfterFreeze where
  finiteLedger : FrozenSMGaugeDecomposition
  factors_are_frozen : finiteLedger.factors = frozenSMGaugeFactorLedger
  representation_is_frozen : finiteLedger.representationLedger = D0.generation

/-- A bridge attempt carries the frozen finite gauge/matter ledger as prerequisite. -/
theorem sm_eft_bridge_requires_frozen_decomposition
    (B : SMEFTBridgeAfterFreeze) :
    B.finiteLedger.factors = frozenSMGaugeFactorLedger ∧
      B.finiteLedger.representationLedger = D0.generation := by
  exact ⟨B.factors_are_frozen, B.representation_is_frozen⟩

/-- Concrete SM/EFT bridge boundary over the frozen finite ledger. -/
def frozenSMEFTBridgeBoundary : SMEFTBridgeAfterFreeze where
  finiteLedger := frozenSMGaugeDecomposition
  factors_are_frozen := frozen_sm_gauge_factors_closed
  representation_is_frozen := frozen_sm_generation_ledger_closed

/-- The frozen bridge boundary has no independent gauge decomposition knob. -/
theorem frozen_sm_eft_bridge_boundary_closed :
    frozenSMEFTBridgeBoundary.finiteLedger.factors = frozenSMGaugeFactorLedger ∧
      frozenSMEFTBridgeBoundary.finiteLedger.representationLedger = D0.generation :=
  sm_eft_bridge_requires_frozen_decomposition frozenSMEFTBridgeBoundary

end D0.Gauge
