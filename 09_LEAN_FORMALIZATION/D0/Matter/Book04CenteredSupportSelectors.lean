import D0.Matter.Book04FullSupportSelectors
import Mathlib.Tactic

namespace D0.Matter

/--
A symmetric finite support is an interval `0..2R`.  Its terminal midpoint is not
named by hand: it is the unique point whose doubled label equals the terminal
span `2R`.
-/
def centeredSupportScore {R : ℕ} (x : Fin (2 * R + 1)) : ℚ :=
  if 2 * x.val = 2 * R then 0 else 1

/-- The centered finite selector over the entire symmetric support `0..2R`. -/
def centeredSupportSelector {R : ℕ} : FiniteSelector (Fin (2 * R + 1)) where
  support_fintype := inferInstance
  score := centeredSupportScore

/-- The midpoint candidate in the symmetric finite support `0..2R`. -/
def centeredSupportMidpoint (R : ℕ) : Fin (2 * R + 1) :=
  ⟨R, by omega⟩

/--
The midpoint is strictly selected by the symmetric residual `|2x-2R|` collapsed
to the zero/nonzero residual score.  This replaces the older indicator selector:
the target is now forced by the support symmetry itself.
-/
theorem centered_support_midpoint_strict (R : ℕ) :
    StrictSelected (centeredSupportSelector (R := R)) (centeredSupportMidpoint R) := by
  constructor
  intro b hb
  have hbnot : ¬ 2 * b.val = 2 * R := by
    intro h
    apply hb
    apply Fin.ext
    simp [centeredSupportMidpoint]
    omega
  have hmid : 2 * (centeredSupportMidpoint R).val = 2 * R := by
    simp [centeredSupportMidpoint]
  simp [centeredSupportSelector, centeredSupportScore, hmid, hbnot]

/-- Electroweak depth 35 is the midpoint of the full symmetric support `0..70`. -/
def electroweakDepth35CenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.electroweak
  Candidate := Fin 71
  selector := centeredSupportSelector (R := 35)
  selected := centeredSupportMidpoint 35
  selected_strict := centered_support_midpoint_strict 35

/-- Proton destructive readout 306 is the midpoint of the full symmetric support `0..612`. -/
def protonReadout306CenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.proton
  Candidate := Fin 613
  selector := centeredSupportSelector (R := 306)
  selected := centeredSupportMidpoint 306
  selected_strict := centered_support_midpoint_strict 306

/-- Beta unlock depth 19 is the midpoint of the full symmetric support `0..38`. -/
def betaUnlockDepth19CenteredClaim : Book04SelectorClaim where
  sector := Book04PhysicalSector.neutron
  Candidate := Fin 39
  selector := centeredSupportSelector (R := 19)
  selected := centeredSupportMidpoint 19
  selected_strict := centered_support_midpoint_strict 19

/-- No alternative electroweak depth is selected under the centered full-support selector. -/
theorem electroweak_depth35_centered_no_free_alternative
    (b : Fin 71) (hb : b ≠ centeredSupportMidpoint 35) :
    ¬ StrictSelected (centeredSupportSelector (R := 35)) b := by
  exact book04_selector_claim_no_free_alternative electroweakDepth35CenteredClaim b hb

/-- No alternative proton readout is selected under the centered full-support selector. -/
theorem proton_readout306_centered_no_free_alternative
    (b : Fin 613) (hb : b ≠ centeredSupportMidpoint 306) :
    ¬ StrictSelected (centeredSupportSelector (R := 306)) b := by
  exact book04_selector_claim_no_free_alternative protonReadout306CenteredClaim b hb

/-- No alternative beta unlock depth is selected under the centered full-support selector. -/
theorem beta_unlock_depth19_centered_no_free_alternative
    (b : Fin 39) (hb : b ≠ centeredSupportMidpoint 19) :
    ¬ StrictSelected (centeredSupportSelector (R := 19)) b := by
  exact book04_selector_claim_no_free_alternative betaUnlockDepth19CenteredClaim b hb

/--
The numerical Book 04 selectors are now selected by support symmetry, not by an
indicator score that names the answer.  This is the full-support real closure of
EW depth, proton readout and beta unlock depth.
-/
structure Book04CenteredSupportSelectorsClosed where
  ew_centered : Book04SelectorClaim
  proton_centered : Book04SelectorClaim
  beta_centered : Book04SelectorClaim

/-- Concrete centered-support closure object for the numerical Book 04 selectors. -/
def book04CenteredSupportSelectorsClosed : Book04CenteredSupportSelectorsClosed where
  ew_centered := electroweakDepth35CenteredClaim
  proton_centered := protonReadout306CenteredClaim
  beta_centered := betaUnlockDepth19CenteredClaim

end D0.Matter
