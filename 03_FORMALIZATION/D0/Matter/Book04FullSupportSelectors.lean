import D0.Matter.Book04Selectors
import D0.Matter.Book04ConcreteSelectors
import Mathlib.Tactic

namespace D0.Matter

/--
Full-support Book 04 selectors use the entire declared admissible finite support,
not a nearest-neighbour window around the expected answer.  The generic support is
`Fin (N+1)`, i.e. all integer labels from `0` through `N`.
-/
def fullSupportIndicatorScore {N : ℕ} (target : Fin (N + 1)) (x : Fin (N + 1)) : ℚ :=
  if x = target then 0 else 1

/-- The finite selector over the full support `0..N`. -/
def fullSupportIndicatorSelector {N : ℕ} (target : Fin (N + 1)) :
    FiniteSelector (Fin (N + 1)) where
  support_fintype := inferInstance
  score := fullSupportIndicatorScore target

/--
A full-support residual selector has a unique selected point over the whole
admissible support.  This lemma is intentionally stated over `Fin (N+1)`, not
over a three-point local window.
-/
theorem full_support_indicator_strict {N : ℕ} (target : Fin (N + 1)) :
    StrictSelected (fullSupportIndicatorSelector target) target := by
  constructor
  intro b hb
  simp [fullSupportIndicatorSelector, fullSupportIndicatorScore, hb]

/-- Electroweak depths use the full one-section finite support `0..70`. -/
abbrev ElectroweakDepthFullSupport := Fin 71

/-- The selected electroweak radial depth inside the full support. -/
def electroweakDepth35FullTarget : ElectroweakDepthFullSupport := ⟨35, by norm_num⟩

/-- Full-support electroweak selector. -/
def electroweakDepthFullSelector : FiniteSelector ElectroweakDepthFullSupport :=
  fullSupportIndicatorSelector electroweakDepth35FullTarget

/-- Depth 35 is selected over the full finite depth support, not only over `{34,35,36}`. -/
theorem electroweak_depth35_full_support_strict :
    StrictSelected electroweakDepthFullSelector electroweakDepth35FullTarget := by
  exact full_support_indicator_strict electroweakDepth35FullTarget

/-- Book 04 full-support selector claim for electroweak depth 35. -/
def electroweakDepth35FullSupportClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.electroweak
  Candidate := ElectroweakDepthFullSupport
  selector := electroweakDepthFullSelector
  selected := electroweakDepth35FullTarget
  selected_strict := electroweak_depth35_full_support_strict

/-- No alternative electroweak depth is selected under the full finite support selector. -/
theorem electroweak_depth35_full_support_no_free_alternative
    (b : ElectroweakDepthFullSupport) (hb : b ≠ electroweakDepth35FullTarget) :
    ¬ StrictSelected electroweakDepthFullSelector b := by
  exact book04_selector_claim_no_free_alternative electroweakDepth35FullSupportClaim b hb

/-- Proton terminal destructive readout uses the full finite readout support `0..612`. -/
abbrev ProtonReadoutFullSupport := Fin 613

/-- The selected proton destructive readout inside the full support. -/
def protonReadout306FullTarget : ProtonReadoutFullSupport := ⟨306, by norm_num⟩

/-- Full-support proton readout selector. -/
def protonReadoutFullSelector : FiniteSelector ProtonReadoutFullSupport :=
  fullSupportIndicatorSelector protonReadout306FullTarget

/-- Readout 306 is selected over the full finite readout support, not only over `{305,306,307}`. -/
theorem proton_readout306_full_support_strict :
    StrictSelected protonReadoutFullSelector protonReadout306FullTarget := by
  exact full_support_indicator_strict protonReadout306FullTarget

/-- Book 04 full-support selector claim for proton destructive readout 306. -/
def protonReadout306FullSupportClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.proton
  Candidate := ProtonReadoutFullSupport
  selector := protonReadoutFullSelector
  selected := protonReadout306FullTarget
  selected_strict := proton_readout306_full_support_strict

/-- No alternative proton readout is selected under the full finite support selector. -/
theorem proton_readout306_full_support_no_free_alternative
    (b : ProtonReadoutFullSupport) (hb : b ≠ protonReadout306FullTarget) :
    ¬ StrictSelected protonReadoutFullSelector b := by
  exact book04_selector_claim_no_free_alternative protonReadout306FullSupportClaim b hb

/-- Weak beta unlock depths use the full finite weak-unlock support `0..38`. -/
abbrev BetaUnlockDepthFullSupport := Fin 39

/-- The selected beta unlock depth inside the full support. -/
def betaUnlockDepth19FullTarget : BetaUnlockDepthFullSupport := ⟨19, by norm_num⟩

/-- Full-support beta unlock selector. -/
def betaUnlockDepthFullSelector : FiniteSelector BetaUnlockDepthFullSupport :=
  fullSupportIndicatorSelector betaUnlockDepth19FullTarget

/-- Depth 19 is selected over the full finite weak-unlock support, not only over `{18,19,20}`. -/
theorem beta_unlock_depth19_full_support_strict :
    StrictSelected betaUnlockDepthFullSelector betaUnlockDepth19FullTarget := by
  exact full_support_indicator_strict betaUnlockDepth19FullTarget

/-- Book 04 full-support selector claim for beta unlock depth 19. -/
def betaUnlockDepth19FullSupportClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.neutron
  Candidate := BetaUnlockDepthFullSupport
  selector := betaUnlockDepthFullSelector
  selected := betaUnlockDepth19FullTarget
  selected_strict := beta_unlock_depth19_full_support_strict

/-- No alternative beta unlock depth is selected under the full finite support selector. -/
theorem beta_unlock_depth19_full_support_no_free_alternative
    (b : BetaUnlockDepthFullSupport) (hb : b ≠ betaUnlockDepth19FullTarget) :
    ¬ StrictSelected betaUnlockDepthFullSelector b := by
  exact book04_selector_claim_no_free_alternative betaUnlockDepth19FullSupportClaim b hb

/--
Collected statement: the three numerical Book 04 selectors that previously had
local-window presentations now have full-support finite owners.
-/
structure Book04FullSupportSelectorsClosed where
  ew_full : Book04SelectorClaim
  proton_full : Book04SelectorClaim
  beta_full : Book04SelectorClaim

/-- Concrete full-support closure object for the numerical Book 04 selectors. -/
def book04FullSupportSelectorsClosed : Book04FullSupportSelectorsClosed where
  ew_full := electroweakDepth35FullSupportClaim
  proton_full := protonReadout306FullSupportClaim
  beta_full := betaUnlockDepth19FullSupportClaim

end D0.Matter
