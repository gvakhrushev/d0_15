import Mathlib.Tactic
import D0.Cosmology.FiedlerHodgeProjection

/-!
# Fiedler tilt tautology no-go

The Fiedler projection does remove an overall multiplicative kernel weight, but
it does not by itself select a cosmological tilt.  For every nonzero one-mode
Lorentzian denominator

  P(q) = m / (q + lambda),

the logarithmic tilt is `-2 q / (q + lambda)`.  Evaluating at the matched
scale `q = lambda` gives `-1` for every nonzero `lambda`; therefore the
value `-1` does not use the special graph eigenvalue `lambda = 20`.

At fixed `lambda = 20`, changing the evaluation scale changes the tilt.  This
module records that scope boundary as an exact no-go.
-/

namespace D0.Cosmology.FiedlerTiltTautologyNoGo

open D0.Cosmology.FiedlerHodgeProjection

/-- The one-mode tilt written directly in the squared scale `q = k^2`. -/
def singleModeTilt (q lambda : ℚ) : ℚ :=
  -2 * q / (q + lambda)

/-- Matching the evaluation scale to the mode eigenvalue forces `-1` for
*every* nonzero eigenvalue.  The numerical value `20` is irrelevant. -/
theorem matched_scale_tilt_universal (lambda : ℚ) (hlambda : lambda ≠ 0) :
    singleModeTilt lambda lambda = -1 := by
  unfold singleModeTilt
  have hden : lambda + lambda ≠ 0 := by
    intro h
    apply hlambda
    linarith
  apply (div_eq_iff hden).2
  ring

/-- At the actual Fiedler eigenvalue, the existing freezeout value is an
instance of the universal matched-scale identity above. -/
theorem fiedler_minus_one_is_matched_scale_instance :
    singleModeTilt lambdaFiedler lambdaFiedler = -1 := by
  exact matched_scale_tilt_universal lambdaFiedler (by
    unfold lambdaFiedler
    norm_num)

/-- The Fiedler formula is exactly the same one-mode formula. -/
theorem fiedlerTiltSq_eq_singleModeTilt (q : ℚ) :
    fiedlerTiltSq q = singleModeTilt q lambdaFiedler := by
  rfl

/-- Fixing the Fiedler eigenvalue does not fix the evaluation scale: two
positive squared scales give different exact tilts. -/
theorem fiedler_fixed_mode_scale_dependence :
    fiedlerTiltSq 20 = -1 ∧ fiedlerTiltSq 40 = -(4 : ℚ) / 3 := by
  constructor <;> norm_num [fiedlerTiltSq, lambdaFiedler]

/-- Consequently, the projected one-mode tilt is not scale invariant even
after the spectral mode and its multiplicity have been fixed. -/
theorem fiedler_tilt_not_scale_invariant :
    fiedlerTiltSq 20 ≠ fiedlerTiltSq 40 := by
  norm_num [fiedlerTiltSq, lambdaFiedler]

/-- **D0-FIEDLER-TILT-TAUTOLOGY-NOGO-001.**
The value `-1` at `q = lambda` is universal for every nonzero one-mode
Lorentzian denominator, while at the fixed D0 value `lambda = 20` the tilt
still changes with `q`.  Thus the Fiedler projection removes an overall
weight but does not close the scale-selection residual. -/
theorem fiedler_tilt_tautology_nogo :
    (∀ lambda : ℚ, lambda ≠ 0 → singleModeTilt lambda lambda = -1) ∧
    fiedlerTiltSq 20 ≠ fiedlerTiltSq 40 := by
  constructor
  · intro lambda hlambda
    exact matched_scale_tilt_universal lambda hlambda
  · exact fiedler_tilt_not_scale_invariant

end D0.Cosmology.FiedlerTiltTautologyNoGo
