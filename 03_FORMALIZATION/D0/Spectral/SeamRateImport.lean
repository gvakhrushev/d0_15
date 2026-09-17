import D0.Spectral.SeamHolonomy
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# Seam-rate import structure — the dressing rate `h_KS = ln φ` cannot be intrinsic to the seam

The α closure-holonomy dresses `α_top⁻¹` by `1 + h_KS·sin θ_seam` (§02.13.h). The rate leg of
`D0-ALPHA-SEAM-FORM-FORCED-001` (obligation (ii)) asks whose rate `h_KS` is. This module owns
the STRUCTURAL half of the answer, machine-checked:

* the seam monodromy `U(θ) = cos θ·I + sin θ·G` is an isometry **at every power** —
  `(Uⁿ)ᵀ·Uⁿ = I` for all `n` (`seamU_pow_orthogonal`), extending `seamU_orthogonal`
  (`D0-SEAM-HOLONOMY-001`) from one turn to the iterated turn dynamics; and it is a proper
  rotation, `det U = 1` (`seamU_det_one`).

An isometric ℤ-action has zero expansion at every step, so the seam's own turn dynamics
carries **zero** Kolmogorov–Sinai rate — the reading `|λ| ≡ 1 ⇒ Lyapunov {0,0} ⇒ h_KS = 0`
is the same external Pesin/Margulis–Ruelle wrapper the corpus already registers for the toral
side (`D0-IF-KS-FORMULA-FIX-001`: `h_KS = log|λ_max|` is "the external/monotone wrapper").
Hence the dressing rate `h_KS = ln φ ≠ 0` is necessarily an IMPORT from a hyperbolic system;
the owned source is the toral time generator `T`, `|λ_max| = φ`
(`D0.Claims.FibonacciIfBridge.toral_spectral_radius_eq_phi`; its fusion counterpart is
entropy-identified at BOOK_01 §01.21.4), identified with the dressing stretch in print at
BOOK_06 §06.30a (record cert `seam_rate_import_check.py`).

The conclusion-failing control `hypCtrl_not_orthogonal` shows the pipeline distinguishes: the
hyperbolic `[[2,1],[1,1]]` (spectral radius `φ²`) fails orthogonality already at one step.

Honest scope: this module owns the matrix identities (isometry at every power, `det = 1`, the
hyperbolic control). The Lyapunov/entropy reading is the named external wrapper (same grade as
row 253's), and the identification of the imported rate with the toral `h_KS` is the in-print
sentence + record cert, not a Lean theorem — no dynamical-systems formalization is claimed.
-/

namespace D0.Spectral

open Matrix

/-- **Isometry at every power:** `(U(θ)ⁿ)ᵀ · U(θ)ⁿ = I` for all `n` — the iterated seam
monodromy never expands, so the seam's own turn dynamics carries zero rate (Pesin wrapper,
named external). -/
theorem seamU_pow_orthogonal (θ : ℝ) (n : ℕ) :
    ((seamU θ) ^ n)ᵀ * (seamU θ) ^ n = 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, Matrix.transpose_mul, mul_assoc, ← mul_assoc (((seamU θ) ^ n)ᵀ), ih,
      one_mul, seamU_orthogonal]

/-- **Proper rotation:** `det U(θ) = 1` (uses `sin²+cos²=1`) — the monodromy is orientation-
preserving, not a reflection. -/
theorem seamU_det_one (θ : ℝ) : (seamU θ).det = 1 := by
  unfold seamU seamG
  rw [Matrix.det_fin_two]
  simp [Matrix.add_apply, Matrix.smul_apply]
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- The hyperbolic control `[[2,1],[1,1]]` (spectral radius `φ²`): genuinely expanding maps
FAIL the orthogonality that `seamU` satisfies — the zero-rate verdict is a property of the
seam map, not of the method. -/
def hypCtrl : Matrix (Fin 2) (Fin 2) ℤ := !![2, 1; 1, 1]

/-- **Conclusion-failing control:** the hyperbolic matrix is not an isometry (`HᵀH ≠ I`). -/
theorem hypCtrl_not_orthogonal : hypCtrlᵀ * hypCtrl ≠ 1 := by
  decide

end D0.Spectral
