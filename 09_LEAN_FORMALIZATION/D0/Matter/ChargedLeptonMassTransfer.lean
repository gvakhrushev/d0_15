import D0.Matter.Book04CoefficientOrigin
import D0.Matter.Book04FullSupportSelectors
import Mathlib.Tactic

namespace D0.Matter

/--
The charged-lepton mass-transfer readout induced by a selected coefficient row.
This is still dimensionless: SI masses and experimental uncertainties live only
in the comparison layer after the D0 transfer row is frozen.
-/
def chargedLeptonMassTransferRatio
    (row : ChargedLeptonCoefficientRow) (g : ChargedLeptonBranch) : ℚ :=
  chargedLeptonRatioCoefficient row g * chargedLeptonBridgeFactor row g

/--
A charged-lepton mass transfer is admissible only if it reads both the terminal
branch and the coefficient row already selected in Book 04.  The transfer does
not contain a new mass knob.
-/
structure ChargedLeptonMassTransfer where
  origin : ChargedLeptonCoefficientOrigin
  terminal : Book04SelectorClaim
  terminal_is_electron : terminal = chargedLeptonElectronTerminalClaim
  massRatio : ChargedLeptonBranch → ℚ
  exponent : ChargedLeptonBranch → ℚ
  massRatio_eq : massRatio = chargedLeptonMassTransferRatio origin.row
  exponent_eq : exponent = chargedLeptonDepthExponent origin.row

/-- Concrete charged-lepton mass-transfer object induced by the frozen origin row. -/
def concreteChargedLeptonMassTransfer : ChargedLeptonMassTransfer where
  origin := concreteChargedLeptonCoefficientOrigin
  terminal := chargedLeptonElectronTerminalClaim
  terminal_is_electron := rfl
  massRatio := chargedLeptonMassTransferRatio ChargedLeptonCoefficientRow.operatorOrigin
  exponent := chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin
  massRatio_eq := rfl
  exponent_eq := rfl

/--
At the fixed finite coefficient origin, the charged-lepton mass-transfer row is
forced.  This closes the gap between `r_g,p_g,B_g` as a frozen row and the
branch-wise transfer used for charged leptons.
-/
theorem charged_lepton_mass_transfer_forced
    (T : ChargedLeptonMassTransfer) :
    T.massRatio = chargedLeptonMassTransferRatio ChargedLeptonCoefficientRow.operatorOrigin ∧
      T.exponent = chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin := by
  have hrow : T.origin.row = ChargedLeptonCoefficientRow.operatorOrigin :=
    charged_lepton_coefficient_origin_row_unique T.origin
  constructor
  · simpa [hrow] using T.massRatio_eq
  · simpa [hrow] using T.exponent_eq

/-- The electron terminal register is part of every admissible charged-lepton transfer. -/
theorem charged_lepton_mass_transfer_terminal_forced
    (T : ChargedLeptonMassTransfer) :
    T.terminal = chargedLeptonElectronTerminalClaim :=
  T.terminal_is_electron

/--
No free retuning of the charged-lepton mass-transfer row is possible at the same
finite terminal branch and coefficient origin.
-/
theorem charged_lepton_mass_transfer_no_free_retuning
    (T : ChargedLeptonMassTransfer) :
    ¬ (T.massRatio ≠ chargedLeptonMassTransferRatio ChargedLeptonCoefficientRow.operatorOrigin ∨
       T.exponent ≠ chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin ∨
       T.terminal ≠ chargedLeptonElectronTerminalClaim) := by
  intro h
  rcases charged_lepton_mass_transfer_forced T with ⟨hr, hp⟩
  have ht := charged_lepton_mass_transfer_terminal_forced T
  rcases h with hratio | hexp | hterm
  · exact hratio hr
  · exact hexp hp
  · exact hterm ht

end D0.Matter
