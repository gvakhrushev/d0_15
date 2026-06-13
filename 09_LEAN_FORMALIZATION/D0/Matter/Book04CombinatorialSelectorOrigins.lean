import D0.Matter.Book04CenteredSupportSelectors
import D0.Combinatorics.HighGainCounts
import Mathlib.Tactic

namespace D0.Matter

/--
Electroweak selector radius read from the already-proved finite return-window
calculus, not from the Book 04 selector table.
-/
def electroweakSelectorRadius : ℕ := D0.DEW

/--
Proton terminal readout radius read from the high-gain destructive-readout
count `18*17`, not from an indicator target.
-/
def protonReadoutSelectorRadius : ℕ := 18 * 17

/--
Beta unlock selector radius read from the weak-unlock depth formula `2*10-1`,
not from a local Book 04 window.
-/
def betaUnlockSelectorRadius : ℕ := 2 * 10 - 1

/-- The electroweak centered support radius is forced by the Ω8 return-window theorem. -/
theorem electroweak_selector_radius_from_omega8 :
    electroweakSelectorRadius = 35 := by
  simpa [electroweakSelectorRadius] using D0.ew35

/-- The proton centered support radius is forced by the high-gain count `18*17`. -/
theorem proton_readout_selector_radius_from_high_gain :
    protonReadoutSelectorRadius = 306 := by
  simpa [protonReadoutSelectorRadius] using D0.readout306

/-- The beta centered support radius is forced by the weak-unlock formula `2*10-1`. -/
theorem beta_unlock_selector_radius_from_weak_unlock :
    betaUnlockSelectorRadius = 19 := by
  simpa [betaUnlockSelectorRadius] using D0.unlock19

/-- The EW full symmetric support span is therefore `0..70`. -/
theorem electroweak_centered_support_span_from_omega8 :
    2 * electroweakSelectorRadius = 70 := by
  rw [electroweak_selector_radius_from_omega8]

/-- The proton full symmetric support span is therefore `0..612`. -/
theorem proton_centered_support_span_from_high_gain :
    2 * protonReadoutSelectorRadius = 612 := by
  rw [proton_readout_selector_radius_from_high_gain]

/-- The beta full symmetric support span is therefore `0..38`. -/
theorem beta_centered_support_span_from_weak_unlock :
    2 * betaUnlockSelectorRadius = 38 := by
  rw [beta_unlock_selector_radius_from_weak_unlock]

/-- The Ω8-forced EW radius selects the same midpoint value `35`. -/
theorem electroweak_midpoint_value_from_omega8 :
    (centeredSupportMidpoint electroweakSelectorRadius).val = 35 := by
  rw [electroweak_selector_radius_from_omega8]
  rfl

/-- The high-gain proton radius selects the same midpoint value `306`. -/
theorem proton_midpoint_value_from_high_gain :
    (centeredSupportMidpoint protonReadoutSelectorRadius).val = 306 := by
  rw [proton_readout_selector_radius_from_high_gain]
  rfl

/-- The weak-unlock beta radius selects the same midpoint value `19`. -/
theorem beta_midpoint_value_from_weak_unlock :
    (centeredSupportMidpoint betaUnlockSelectorRadius).val = 19 := by
  rw [beta_unlock_selector_radius_from_weak_unlock]
  rfl

/--
Derived EW selector: the support radius is imported from the Ω8 return-window
calculus before the centered selector is applied.
-/
def electroweakDepthDerivedCenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.electroweak
  Candidate := Fin (2 * electroweakSelectorRadius + 1)
  selector := centeredSupportSelector (R := electroweakSelectorRadius)
  selected := centeredSupportMidpoint electroweakSelectorRadius
  selected_strict := centered_support_midpoint_strict electroweakSelectorRadius

/-- Derived proton selector: the support radius is imported from `18*17`. -/
def protonReadoutDerivedCenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.proton
  Candidate := Fin (2 * protonReadoutSelectorRadius + 1)
  selector := centeredSupportSelector (R := protonReadoutSelectorRadius)
  selected := centeredSupportMidpoint protonReadoutSelectorRadius
  selected_strict := centered_support_midpoint_strict protonReadoutSelectorRadius

/-- Derived beta selector: the support radius is imported from `2*10-1`. -/
def betaUnlockDerivedCenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.neutron
  Candidate := Fin (2 * betaUnlockSelectorRadius + 1)
  selector := centeredSupportSelector (R := betaUnlockSelectorRadius)
  selected := centeredSupportMidpoint betaUnlockSelectorRadius
  selected_strict := centered_support_midpoint_strict betaUnlockSelectorRadius

/-- No alternative EW depth survives once the Ω8-derived support is fixed. -/
theorem electroweak_depth_derived_centered_no_free_alternative
    (b : Fin (2 * electroweakSelectorRadius + 1))
    (hb : b ≠ centeredSupportMidpoint electroweakSelectorRadius) :
    ¬ StrictSelected (centeredSupportSelector (R := electroweakSelectorRadius)) b := by
  exact book04_selector_claim_no_free_alternative electroweakDepthDerivedCenteredClaim b hb

/-- No alternative proton readout survives once the high-gain-derived support is fixed. -/
theorem proton_readout_derived_centered_no_free_alternative
    (b : Fin (2 * protonReadoutSelectorRadius + 1))
    (hb : b ≠ centeredSupportMidpoint protonReadoutSelectorRadius) :
    ¬ StrictSelected (centeredSupportSelector (R := protonReadoutSelectorRadius)) b := by
  exact book04_selector_claim_no_free_alternative protonReadoutDerivedCenteredClaim b hb

/-- No alternative beta unlock depth survives once the weak-unlock-derived support is fixed. -/
theorem beta_unlock_derived_centered_no_free_alternative
    (b : Fin (2 * betaUnlockSelectorRadius + 1))
    (hb : b ≠ centeredSupportMidpoint betaUnlockSelectorRadius) :
    ¬ StrictSelected (centeredSupportSelector (R := betaUnlockSelectorRadius)) b := by
  exact book04_selector_claim_no_free_alternative betaUnlockDerivedCenteredClaim b hb

/--
Book 04 numerical selectors with combinatorial origins.  This closes the
remaining weakness of centered selectors: the radii `35`, `306`, and `19` are
not named by the selector layer, but imported from prior D0 combinatorics.
-/
structure Book04CombinatorialSelectorOriginsClosed where
  ew_radius_forced : electroweakSelectorRadius = 35
  ew_span_forced : 2 * electroweakSelectorRadius = 70
  ew_midpoint_forced : (centeredSupportMidpoint electroweakSelectorRadius).val = 35
  proton_radius_forced : protonReadoutSelectorRadius = 306
  proton_span_forced : 2 * protonReadoutSelectorRadius = 612
  proton_midpoint_forced : (centeredSupportMidpoint protonReadoutSelectorRadius).val = 306
  beta_radius_forced : betaUnlockSelectorRadius = 19
  beta_span_forced : 2 * betaUnlockSelectorRadius = 38
  beta_midpoint_forced : (centeredSupportMidpoint betaUnlockSelectorRadius).val = 19

/-- Concrete closure object for Book 04 derived centered selector origins. -/
def book04CombinatorialSelectorOriginsClosed : Book04CombinatorialSelectorOriginsClosed where
  ew_radius_forced := electroweak_selector_radius_from_omega8
  ew_span_forced := electroweak_centered_support_span_from_omega8
  ew_midpoint_forced := electroweak_midpoint_value_from_omega8
  proton_radius_forced := proton_readout_selector_radius_from_high_gain
  proton_span_forced := proton_centered_support_span_from_high_gain
  proton_midpoint_forced := proton_midpoint_value_from_high_gain
  beta_radius_forced := beta_unlock_selector_radius_from_weak_unlock
  beta_span_forced := beta_centered_support_span_from_weak_unlock
  beta_midpoint_forced := beta_midpoint_value_from_weak_unlock

end D0.Matter
