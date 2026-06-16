import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Data.Real.StarOrdered
import Mathlib.Tactic

/-!
# D0-QUANT-MET-002 — purification operator inequality (PSD)

Metrology layer. Shared cert: `05_CERTS/vp_quantum_metrology_limits.py` (purification block).

The admitted operator lemma `F_lab ≽ Π F_N Π`. When the lab projector `Π` sits inside the system
projector `P_N` (`Π·P_N = Π`), the difference collapses to `F_lab − Π F_N Π = Π Uᴴ (P_N − Π) U Π`, which
is positive semidefinite because `R := P_N − Π` is itself a Hermitian projector (hence PSD) and
`Π Uᴴ R U Π` is a double conjugation of a PSD matrix. The cert's "random unitaries" are a Monte-Carlo
witness of this `U`-generic exact fact.

This module machine-checks the operator positivity: `R PSD ⇒ Π Uᴴ R U Π PSD` (the lemma) and
`P_N, Π Hermitian idempotent with Π·P_N = Π ⇒ (P_N − Π) PSD`.
-/

namespace D0.Metrology

open Matrix

/-- **D0-QUANT-MET-002.** Purification operator lemma: for any `U`, any Hermitian `Π`, and any PSD `R`,
the conjugated operator `Π Uᴴ R U Π` is positive semidefinite. (With `R = P_N − Π` this is
`F_lab − Π F_N Π ≽ 0`.) -/
theorem psd_purification_inequality {n : ℕ} (U Pi R : Matrix (Fin n) (Fin n) ℝ)
    (hPih : Piᴴ = Pi) (hR : R.PosSemidef) :
    (Pi * Uᴴ * R * U * Pi).PosSemidef := by
  have h1 : (Uᴴ * R * U).PosSemidef := hR.conjTranspose_mul_mul_same U
  have h2 := h1.mul_mul_conjTranspose_same Pi
  rw [hPih] at h2
  have heq : Pi * Uᴴ * R * U * Pi = Pi * (Uᴴ * R * U) * Pi := by simp only [mul_assoc]
  rw [heq]; exact h2

/-- The projector difference `P_N − Π` is positive semidefinite when `Π ≤ P_N`
(`Π·P_N = Π`, both Hermitian idempotents) — it is itself a Hermitian projector. -/
theorem proj_diff_posSemidef {n : ℕ} (PN Pi : Matrix (Fin n) (Fin n) ℝ)
    (hPNh : PNᴴ = PN) (hPNi : PN * PN = PN) (hPih : Piᴴ = Pi) (hPii : Pi * Pi = Pi)
    (hsub : Pi * PN = Pi) : (PN - Pi).PosSemidef := by
  have hPNPi : PN * Pi = Pi := by
    have h := congrArg conjTranspose hsub
    rw [conjTranspose_mul, hPNh, hPih] at h; exact h
  have hRh : (PN - Pi)ᴴ = PN - Pi := by rw [conjTranspose_sub, hPNh, hPih]
  have hRR : (PN - Pi) * (PN - Pi) = PN - Pi := by
    have hexp : (PN - Pi) * (PN - Pi) = PN * PN - PN * Pi - Pi * PN + Pi * Pi := by
      noncomm_ring
    rw [hexp, hPNi, hPNPi, hsub, hPii]; abel
  have hReq : (PN - Pi)ᴴ * (PN - Pi) = PN - Pi := by rw [hRh, hRR]
  rw [← hReq]; exact posSemidef_conjTranspose_mul_self _

end D0.Metrology
