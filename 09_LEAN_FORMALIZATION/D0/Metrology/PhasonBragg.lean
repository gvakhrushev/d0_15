import D0.Core.Phi
import Mathlib.Algebra.Order.Round
import Mathlib.Tactic

/-!
# D0-QUANT-MET-004 — phason Bragg line spectrum target (φ-frequency identity)

Metrology layer. Shared cert: `05_CERTS/vp_quantum_metrology_limits.py` (analog-residual block).

The analog residual `R = frac(n·φ⁻²) − 1/2` has a pure-point ("Bragg") line spectrum at the
frequencies `f_m = frac(m·φ⁻²)`. The exact φ-kernel the cert uses but never isolates: `φ⁻² = 2 − φ`
(from `φ² = φ + 1`), so `f_m = frac(m·φ⁻²) = frac(−m·φ)` for every integer `m` (the integer `2m` shifts
away under `frac`).

This module machine-checks that φ-identity and the Bragg-frequency `frac` identity. The kurtosis ≈ 9/5
and the FFT peak-enhancement targets are finite-N numerical approximations to the continuum
equidistribution limit and stay in the cert.
-/

namespace D0.Metrology

open D0

/-- The φ-kernel of the Bragg spectrum: `φ⁻² = 2 − φ` (from `φ² = φ + 1`). -/
theorem phi_inv_sq_eq_two_sub_phi : phi⁻¹ ^ 2 = 2 - phi := by
  rw [phi_inv_eq_primitiveRoot]; unfold primitiveRoot phi
  linear_combination (1 / 4 : ℝ) * sqrt_five_sq

/-- **Bragg line spectrum target:** `frac(m·φ⁻²) = frac(−m·φ)` for every integer `m`. -/
theorem phason_bragg_line_spectrum_target (m : ℤ) :
    Int.fract ((m : ℝ) * phi⁻¹ ^ 2) = Int.fract (-((m : ℝ) * phi)) := by
  have key : (m : ℝ) * phi⁻¹ ^ 2 = ((2 * m : ℤ) : ℝ) + (-((m : ℝ) * phi)) := by
    push_cast; linear_combination (m : ℝ) * phi_inv_sq_eq_two_sub_phi
  rw [key, Int.fract_intCast_add]

/-- **D0-QUANT-MET-004.** The φ-kernel `φ⁻² = 2 − φ` and the Bragg-frequency identity
`frac(m·φ⁻²) = frac(−m·φ)` for all integer `m`. -/
theorem phason_bragg_cert :
    phi⁻¹ ^ 2 = 2 - phi ∧
    (∀ m : ℤ, Int.fract ((m : ℝ) * phi⁻¹ ^ 2) = Int.fract (-((m : ℝ) * phi))) :=
  ⟨phi_inv_sq_eq_two_sub_phi, phason_bragg_line_spectrum_target⟩

end D0.Metrology
