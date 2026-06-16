import D0.Core.Phi
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Data.Real.StarOrdered
import Mathlib.Tactic

/-!
# D0-QUANT-MET-003 — conditional φ⁻² purification flux bound

Metrology layer. Shared cert: `05_CERTS/vp_quantum_metrology_limits.py` (conditional-bound block).

The cert is explicit that `λ_* = φ⁻²` is a **sector hypothesis / prediction target**, NOT a consequence
of the PSD lemma alone (section 3 is a negative control showing the algebra does not force it). So only
the CONDITIONAL bound is internalizable: if the sector operator `F − λ·P` is positive semidefinite and
`Π` is Hermitian, then the purification flux `Tr(Π (F − λ·P) Π) ≥ 0`, i.e. `Tr(Π F Π) ≥ λ·Tr(Π P Π)`.

This module machine-checks that conditional trace bound (with `λ` generic) and the sector value
`φ⁻² > 0`. The physical claim "the flux IS `φ⁻²`" stays a PROOF-TARGET / cert.
-/

namespace D0.Metrology

open Matrix

/-- The sector flux value `λ_* = φ⁻²` is strictly positive. -/
theorem phi_inv_sq_pos : (0 : ℝ) < phi⁻¹ ^ 2 := by
  have hphi : (0 : ℝ) < phi := by unfold phi; positivity
  exact pow_pos (inv_pos.mpr hphi) 2

/-- **D0-QUANT-MET-003 (conditional).** If the sector operator `F − λ·P` is PSD and `Π` is Hermitian,
the purification flux `Tr(Π (F − λ·P) Π) ≥ 0`. The sector value `λ = φ⁻²` is the D0 hypothesis
(CONDITIONAL-THEOREM-TARGET), not derived here. -/
theorem phi2_purification_flux_target {n : ℕ} (F P Pi : Matrix (Fin n) (Fin n) ℝ) (lam : ℝ)
    (hPih : Piᴴ = Pi) (hsector : (F - lam • P).PosSemidef) :
    0 ≤ (Pi * (F - lam • P) * Pi).trace := by
  have hpsd : (Pi * (F - lam • P) * Pi).PosSemidef := by
    have h := hsector.conjTranspose_mul_mul_same Pi
    rwa [hPih] at h
  exact hpsd.trace_nonneg

end D0.Metrology
