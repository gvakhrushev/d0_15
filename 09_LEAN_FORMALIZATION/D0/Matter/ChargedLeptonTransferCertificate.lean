import D0.Matter.ChargedLeptonMassTransfer
import Mathlib.Tactic

namespace D0.Matter

/-- Explicit finite charged-lepton transfer table read from the operator-origin row. -/
structure ChargedLeptonTransferTable where
  electronRatio : ℚ
  muonRatio : ℚ
  tauRatio : ℚ
  electronExponent : ℚ
  muonExponent : ℚ
  tauExponent : ℚ

/-- Concrete charged-lepton table produced by the frozen transfer object. -/
def concreteChargedLeptonTransferTable : ChargedLeptonTransferTable where
  electronRatio := concreteChargedLeptonMassTransfer.massRatio ChargedLeptonBranch.electron
  muonRatio := concreteChargedLeptonMassTransfer.massRatio ChargedLeptonBranch.muon
  tauRatio := concreteChargedLeptonMassTransfer.massRatio ChargedLeptonBranch.tau
  electronExponent := concreteChargedLeptonMassTransfer.exponent ChargedLeptonBranch.electron
  muonExponent := concreteChargedLeptonMassTransfer.exponent ChargedLeptonBranch.muon
  tauExponent := concreteChargedLeptonMassTransfer.exponent ChargedLeptonBranch.tau

/-- Electron branch normalization is exactly one at the frozen transfer. -/
theorem charged_lepton_transfer_electron_ratio_closed :
    concreteChargedLeptonTransferTable.electronRatio = 1 := by
  norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
    chargedLeptonMassTransferRatio, chargedLeptonRatioCoefficient, chargedLeptonBridgeFactor]

/-- Muon branch ratio is the frozen rational Book 04 transfer value. -/
theorem charged_lepton_transfer_muon_ratio_closed :
    concreteChargedLeptonTransferTable.muonRatio =
      38814328681047283 / 10000000000000000 := by
  norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
    chargedLeptonMassTransferRatio, chargedLeptonRatioCoefficient, chargedLeptonBridgeFactor]

/-- Tau branch ratio is the frozen rational Book 04 transfer value. -/
theorem charged_lepton_transfer_tau_ratio_closed :
    concreteChargedLeptonTransferTable.tauRatio =
      103183483253993735 / 10000000000000000 := by
  norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
    chargedLeptonMassTransferRatio, chargedLeptonRatioCoefficient, chargedLeptonBridgeFactor]

/-- Charged-lepton exponent row is frozen together with the ratio row. -/
theorem charged_lepton_transfer_exponents_closed :
    concreteChargedLeptonTransferTable.electronExponent = 0 ∧
      concreteChargedLeptonTransferTable.muonExponent = 1 / 4 ∧
        concreteChargedLeptonTransferTable.tauExponent = 1 / 3 := by
  constructor
  · norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
      chargedLeptonDepthExponent]
  constructor
  · norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
      chargedLeptonDepthExponent]
  · norm_num [concreteChargedLeptonTransferTable, concreteChargedLeptonMassTransfer,
      chargedLeptonDepthExponent]

end D0.Matter
