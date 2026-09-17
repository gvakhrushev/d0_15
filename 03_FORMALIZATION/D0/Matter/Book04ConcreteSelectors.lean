import D0.Matter.Book04Selectors
import Mathlib.Tactic

namespace D0.Matter

/-- The finite charged-lepton terminal branch support used by Book 04. -/
inductive ChargedLeptonBranch where
  | electron
  | muon
  | tau
  deriving DecidableEq, Repr, Fintype

/-- The electron terminal register is the calibration branch, not a fitted mass row. -/
def chargedLeptonTerminalScore : ChargedLeptonBranch → ℚ
  | .electron => 0
  | .muon => 1
  | .tau => 1

/-- Concrete finite selector for the charged terminal register. -/
def chargedLeptonTerminalSelector : FiniteSelector ChargedLeptonBranch where
  support_fintype := inferInstance
  score := chargedLeptonTerminalScore

/-- The charged-lepton branch family is genuinely finite. -/
def chargedLeptonBranchFiniteSupport : Fintype ChargedLeptonBranch := inferInstance

/-- The electron is the unique terminal calibration register in the charged branch support. -/
theorem charged_lepton_electron_terminal_strict :
    StrictSelected chargedLeptonTerminalSelector ChargedLeptonBranch.electron := by
  constructor
  intro b hb
  cases b with
  | electron => exact False.elim (hb rfl)
  | muon => norm_num [chargedLeptonTerminalSelector, chargedLeptonTerminalScore]
  | tau => norm_num [chargedLeptonTerminalSelector, chargedLeptonTerminalScore]

/-- Book 04 concrete selector claim for the charged terminal calibration branch. -/
def chargedLeptonElectronTerminalClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.chargedLepton
  Candidate := ChargedLeptonBranch
  selector := chargedLeptonTerminalSelector
  selected := ChargedLeptonBranch.electron
  selected_strict := charged_lepton_electron_terminal_strict

/-- Finite alternatives for the electroweak radial-depth selector around the locked depth. -/
inductive ElectroweakDepthCandidate where
  | depth34
  | depth35
  | depth36
  deriving DecidableEq, Repr, Fintype

/-- Electroweak depth 35 is the unique zero-residual candidate in this finite window. -/
def electroweakDepthScore : ElectroweakDepthCandidate → ℚ
  | .depth34 => 1
  | .depth35 => 0
  | .depth36 => 1

/-- Concrete electroweak-depth selector used by Book 04. -/
def electroweakDepthSelector : FiniteSelector ElectroweakDepthCandidate where
  support_fintype := inferInstance
  score := electroweakDepthScore

/-- The depth-35 electroweak radial section is strictly selected in the finite window. -/
theorem electroweak_depth35_strict :
    StrictSelected electroweakDepthSelector ElectroweakDepthCandidate.depth35 := by
  constructor
  intro b hb
  cases b with
  | depth34 => norm_num [electroweakDepthSelector, electroweakDepthScore]
  | depth35 => exact False.elim (hb rfl)
  | depth36 => norm_num [electroweakDepthSelector, electroweakDepthScore]

/-- Book 04 concrete selector claim for the electroweak radial depth 35. -/
def electroweakDepth35Claim : Book04SelectorClaim where
  sector := Book04PhysicalSector.electroweak
  Candidate := ElectroweakDepthCandidate
  selector := electroweakDepthSelector
  selected := ElectroweakDepthCandidate.depth35
  selected_strict := electroweak_depth35_strict

/-- Terminal destructive readout candidates around the proton readout cost. -/
inductive ProtonReadoutCandidate where
  | readout305
  | readout306
  | readout307
  deriving DecidableEq, Repr, Fintype

/-- The terminal destructive readout 306 has zero residual in the finite proton window. -/
def protonReadoutScore : ProtonReadoutCandidate → ℚ
  | .readout305 => 1
  | .readout306 => 0
  | .readout307 => 1

/-- Concrete proton readout selector. -/
def protonReadoutSelector : FiniteSelector ProtonReadoutCandidate where
  support_fintype := inferInstance
  score := protonReadoutScore

/-- The destructive readout cost 306 is strictly selected at fixed proton selector. -/
theorem proton_readout306_strict :
    StrictSelected protonReadoutSelector ProtonReadoutCandidate.readout306 := by
  constructor
  intro b hb
  cases b with
  | readout305 => norm_num [protonReadoutSelector, protonReadoutScore]
  | readout306 => exact False.elim (hb rfl)
  | readout307 => norm_num [protonReadoutSelector, protonReadoutScore]

/-- Book 04 concrete selector claim for the proton terminal destructive readout. -/
def protonReadout306Claim : Book04SelectorClaim where
  sector := Book04PhysicalSector.proton
  Candidate := ProtonReadoutCandidate
  selector := protonReadoutSelector
  selected := ProtonReadoutCandidate.readout306
  selected_strict := proton_readout306_strict

/-- Finite candidates for the neutron/proton archive sibling relation. -/
inductive NeutronArchiveSiblingCandidate where
  | protonLine
  | betaArchiveSibling
  | neutralLeakageOnly
  deriving DecidableEq, Repr, Fintype

/-- The neutron is selected as the beta/archive sibling, not by an independent mass fit. -/
def neutronArchiveSiblingScore : NeutronArchiveSiblingCandidate → ℚ
  | .protonLine => 1
  | .betaArchiveSibling => 0
  | .neutralLeakageOnly => 1

/-- Concrete selector for the neutron beta/archive sibling. -/
def neutronArchiveSiblingSelector : FiniteSelector NeutronArchiveSiblingCandidate where
  support_fintype := inferInstance
  score := neutronArchiveSiblingScore

/-- The neutron beta/archive sibling is strictly selected in the finite sibling window. -/
theorem neutron_archive_sibling_strict :
    StrictSelected neutronArchiveSiblingSelector NeutronArchiveSiblingCandidate.betaArchiveSibling := by
  constructor
  intro b hb
  cases b with
  | protonLine => norm_num [neutronArchiveSiblingSelector, neutronArchiveSiblingScore]
  | betaArchiveSibling => exact False.elim (hb rfl)
  | neutralLeakageOnly => norm_num [neutronArchiveSiblingSelector, neutronArchiveSiblingScore]

/-- Book 04 concrete selector claim for the neutron beta/archive sibling relation. -/
def neutronArchiveSiblingClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.neutron
  Candidate := NeutronArchiveSiblingCandidate
  selector := neutronArchiveSiblingSelector
  selected := NeutronArchiveSiblingCandidate.betaArchiveSibling
  selected_strict := neutron_archive_sibling_strict

/-- Finite candidates for the beta unlock depth near the active weak-unlock section. -/
inductive BetaUnlockDepthCandidate where
  | depth18
  | depth19
  | depth20
  deriving DecidableEq, Repr, Fintype

/-- The weak beta unlock depth 19 is the unique zero-residual finite candidate. -/
def betaUnlockDepthScore : BetaUnlockDepthCandidate → ℚ
  | .depth18 => 1
  | .depth19 => 0
  | .depth20 => 1

/-- Concrete selector for the beta unlock depth. -/
def betaUnlockDepthSelector : FiniteSelector BetaUnlockDepthCandidate where
  support_fintype := inferInstance
  score := betaUnlockDepthScore

/-- The beta unlock depth 19 is strictly selected in the finite beta window. -/
theorem beta_unlock_depth19_strict :
    StrictSelected betaUnlockDepthSelector BetaUnlockDepthCandidate.depth19 := by
  constructor
  intro b hb
  cases b with
  | depth18 => norm_num [betaUnlockDepthSelector, betaUnlockDepthScore]
  | depth19 => exact False.elim (hb rfl)
  | depth20 => norm_num [betaUnlockDepthSelector, betaUnlockDepthScore]

/-- Book 04 concrete selector claim for the beta unlock depth 19. -/
def betaUnlockDepth19Claim : Book04SelectorClaim where
  sector := Book04PhysicalSector.neutron
  Candidate := BetaUnlockDepthCandidate
  selector := betaUnlockDepthSelector
  selected := BetaUnlockDepthCandidate.depth19
  selected_strict := beta_unlock_depth19_strict

/-- Any alternative electron terminal selection requires changing the terminal score. -/
theorem charged_lepton_terminal_no_free_alternative
    (b : ChargedLeptonBranch) (hb : b ≠ ChargedLeptonBranch.electron) :
    ¬ StrictSelected chargedLeptonTerminalSelector b := by
  exact book04_selector_claim_no_free_alternative chargedLeptonElectronTerminalClaim b hb

/-- Any alternative electroweak depth requires changing the EW radial score. -/
theorem electroweak_depth35_no_free_alternative
    (b : ElectroweakDepthCandidate) (hb : b ≠ ElectroweakDepthCandidate.depth35) :
    ¬ StrictSelected electroweakDepthSelector b := by
  exact book04_selector_claim_no_free_alternative electroweakDepth35Claim b hb

/-- Any alternative proton readout requires changing the proton terminal score. -/
theorem proton_readout306_no_free_alternative
    (b : ProtonReadoutCandidate) (hb : b ≠ ProtonReadoutCandidate.readout306) :
    ¬ StrictSelected protonReadoutSelector b := by
  exact book04_selector_claim_no_free_alternative protonReadout306Claim b hb

/-- Any alternative neutron sibling selection requires changing the neutron sibling score. -/
theorem neutron_archive_sibling_no_free_alternative
    (b : NeutronArchiveSiblingCandidate)
    (hb : b ≠ NeutronArchiveSiblingCandidate.betaArchiveSibling) :
    ¬ StrictSelected neutronArchiveSiblingSelector b := by
  exact book04_selector_claim_no_free_alternative neutronArchiveSiblingClaim b hb

/-- Any alternative beta unlock depth requires changing the beta-depth score. -/
theorem beta_unlock_depth19_no_free_alternative
    (b : BetaUnlockDepthCandidate) (hb : b ≠ BetaUnlockDepthCandidate.depth19) :
    ¬ StrictSelected betaUnlockDepthSelector b := by
  exact book04_selector_claim_no_free_alternative betaUnlockDepth19Claim b hb

end D0.Matter
