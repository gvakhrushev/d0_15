import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Data.Real.StarOrdered
import Mathlib.Tactic

/-!
# D0-GRAV-006 / D0-HORIZON-JET-001 — horizon emission operator (positive semidefinite)

BOOK_07. Python certificate: `05_CERTS/vp_horizon_jet_axis_observable.py`.

The Horizon Emission Law: the conjugate archive→retained emission operator `F = Q Uᴴ P U Q` (with the
measurement projector `P`, complement `Q = 1 − P`, and any orthogonal `U`) is **positive semidefinite**.
This is exact, structural, and `U`-generic: `F = (P U Q)ᴴ (P U Q)` is a Gram matrix. The cert's toy
collimation inequality `J_axis > J_trans` depends on the specific float QR matrix and stays cert; the
axis/transverse seam projectors are exactly orthogonal (`Π_axis · Π_trans = 0`).

This module machine-checks the PSD law (the cert-closed core) and the projector orthogonality.
-/

namespace D0.Gravity

open Matrix

/-- **D0-GRAV-006.** The conjugate emission operator `F = Q Uᴴ P U Q` (`Q = 1 − P`) is positive
semidefinite for any matrix `U` and any Hermitian idempotent projector `P`. -/
theorem horizon_jet_baryon_pole_layer_cert {n : ℕ} (P U : Matrix (Fin n) (Fin n) ℝ)
    (hPh : Pᴴ = P) (hPP : P * P = P) :
    ((1 - P) * Uᴴ * P * U * (1 - P)).PosSemidef := by
  have hP : P.PosSemidef := by
    have hPeq : Pᴴ * P = P := by rw [hPh, hPP]
    rw [← hPeq]; exact posSemidef_conjTranspose_mul_self P
  have hQh : ((1 : Matrix (Fin n) (Fin n) ℝ) - P)ᴴ = 1 - P := by
    rw [conjTranspose_sub, conjTranspose_one, hPh]
  have h1 : (Uᴴ * P * U).PosSemidef := hP.conjTranspose_mul_mul_same U
  have h2 := h1.mul_mul_conjTranspose_same (1 - P)
  rw [hQh] at h2
  have heq : (1 - P) * Uᴴ * P * U * (1 - P) = (1 - P) * (Uᴴ * P * U) * (1 - P) := by
    simp only [mul_assoc]
  rw [heq]; exact h2

/-- Axis seam projector `Π_axis = diag(0,0,1,0)`. -/
def piAxis : Matrix (Fin 4) (Fin 4) ℚ := Matrix.diagonal ![0, 0, 1, 0]

/-- Transverse seam projector `Π_trans = diag(0,0,0,1)`. -/
def piTrans : Matrix (Fin 4) (Fin 4) ℚ := Matrix.diagonal ![0, 0, 0, 1]

/-- **D0-HORIZON-JET-001.** The horizon emission operator is PSD (any orthogonal `U`, any projector
`P`) and the axis/transverse seam projectors are orthogonal (`Π_axis · Π_trans = 0`). -/
theorem horizon_jet_observable_cert :
    (∀ {n : ℕ} (P U : Matrix (Fin n) (Fin n) ℝ), Pᴴ = P → P * P = P →
      ((1 - P) * Uᴴ * P * U * (1 - P)).PosSemidef) ∧
    piAxis * piTrans = 0 := by
  refine ⟨fun P U hPh hPP => horizon_jet_baryon_pole_layer_cert P U hPh hPP, ?_⟩
  native_decide

end D0.Gravity
