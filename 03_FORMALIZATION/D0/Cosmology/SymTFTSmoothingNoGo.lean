import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic
import D0.Core.Phi
import D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-!
# SymTFT smoothing proposal: exact negative control

An exploratory memo proposed

  u* = (1/20) log(phi^2 / (1 + phi^2))

as a canonical smoothing parameter.  This file treats that expression as a
candidate, not as input to the core.

Two exact facts are enough to prevent it from closing the existing CMB selector
residual:

1. rho = phi^2/(1+phi^2) lies strictly between 0 and 1, hence u* < 0;
2. even a fixed smoothing choice cannot determine the spectral tilt unless the
   evaluation wavenumber k is fixed as well — the existing exact rational
   no-go already exhibits different tilts at k=1 and k=2 with identical
   smoothing weights.

No Planck value, fitted tilt or survey datum enters this result.
-/

namespace D0.Cosmology.SymTFTSmoothingNoGo

open D0
open D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-- The dimension-ratio appearing in the proposed SymTFT expression. -/
noncomputable def rho : ℝ := phi ^ 2 / (1 + phi ^ 2)

/-- Proposed smoothing coordinate from the exploratory formula. -/
noncomputable def uStar : ℝ := Real.log rho / 20

theorem rho_pos : 0 < rho := by
  unfold rho
  positivity

theorem rho_lt_one : rho < 1 := by
  unfold rho
  have hp : 0 < phi ^ 2 := by positivity
  have hd : 0 < 1 + phi ^ 2 := by positivity
  rw [div_lt_one hd]
  linarith

theorem rho_unit_interval : 0 < rho ∧ rho < 1 :=
  ⟨rho_pos, rho_lt_one⟩

/-- The proposed formula is a negative smoothing coordinate. -/
theorem proposed_uStar_negative : uStar < 0 := by
  unfold uStar
  have hlog : Real.log rho < 0 := Real.log_neg rho_pos rho_lt_one
  positivity

/-- Fixing a smoothing prescription does not remove the independent k-axis:
the same weights give different exact tilts at k=1 and k=2. -/
theorem fixed_smoothing_still_leaves_k_choice :
    tilt 1 12 10 8 2 ≠ tilt 2 12 10 8 2 :=
  tilt_varies_with_wavenumber

/-- Terminal assessment of the proposed formula relative to the current CMB
no-go: it may specify one candidate u, but cannot by itself provide the required
unique pair (k,u). -/
theorem symtft_smoothing_underdetermination_nogo :
    uStar < 0 ∧
    tilt 1 12 10 8 2 ≠ tilt 2 12 10 8 2 :=
  ⟨proposed_uStar_negative, fixed_smoothing_still_leaves_k_choice⟩

end D0.Cosmology.SymTFTSmoothingNoGo
