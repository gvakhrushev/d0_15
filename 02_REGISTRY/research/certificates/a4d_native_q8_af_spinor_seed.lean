import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# Q8/AF spinor seed: the exact Hermitian 2x2 determinant form

This research module formalizes only the finite kinematic statement: the
Hermitian Pauli coordinates on the first M₂ block have determinant of
signature (1,3). It does not identify this cone with a physical metric or
derive a Lorentz link, source, or Einstein dynamics.
-/

namespace D0.Research.Q8AFSpinorSeed

open Matrix

/-- Hermitian 2x2 matrix in real Pauli coordinates (t,x,y,z). -/
def hermitianPauli (t x y z : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![ Complex.ofReal (t + z), Complex.ofReal x - Complex.I * Complex.ofReal y;
      Complex.ofReal x + Complex.I * Complex.ofReal y, Complex.ofReal (t - z) ]

/-- Its determinant is exactly the Lorentz quadratic form. -/
theorem hermitianPauli_det (t x y z : ℝ) :
    (hermitianPauli t x y z).det =
      Complex.ofReal (t^2 - x^2 - y^2 - z^2) := by
  unfold hermitianPauli
  rw [Matrix.det_fin_two_of]
  apply Complex.ext <;>
    simp [Complex.ofReal, Complex.I] <;>
    ring

/-- The time axis has positive square. -/
theorem lorentz_time_axis (t : ℝ) :
    t^2 - 0^2 - 0^2 - 0^2 = t^2 := by ring

/-- Each of the three traceless Pauli axes has negative square. -/
theorem lorentz_spatial_axes (x y z : ℝ) :
    (0 : ℝ)^2 - x^2 - 0^2 - 0^2 = -x^2 ∧
    (0 : ℝ)^2 - 0^2 - y^2 - 0^2 = -y^2 ∧
    (0 : ℝ)^2 - 0^2 - 0^2 - z^2 = -z^2 := by
  constructor
  · ring
  constructor
  · ring
  · ring

/-- The golden half-gap equals p^3/2 from the Fibonacci trace equation. -/
theorem golden_half_gap (p : ℝ) (hp : p + p^2 = 1) :
    (p - p^2) / 2 = p^3 / 2 := by
  have hp2 : p^2 = 1 - p := by linarith
  have hgap : p - p^2 = p^3 := by
    calc
      p - p^2 = p * (1 - p) := by ring
      _ = p * p^2 := by rw [← hp2]
      _ = p^3 := by ring
  rw [hgap]

/-- The two existing feedback weights are complementary. -/
theorem golden_feedback_corner_complement (p : ℝ) (hp : p + p^2 = 1) :
    4 * p^3 + p^6 = 1 := by
  have hp2 : p^2 = 1 - p := by linarith
  have hp3 : p^3 = 2 * p - 1 := by
    calc
      p^3 = p * p^2 := by ring
      _ = p * (1 - p) := by rw [hp2]
      _ = p - p^2 := by ring
      _ = 2 * p - 1 := by rw [hp2]; ring
  have hp6 : p^6 = 5 - 8 * p := by
    calc
      p^6 = (p^3)^2 := by ring
      _ = (2 * p - 1)^2 := by rw [hp3]
      _ = 4 * p^2 - 4 * p + 1 := by ring
      _ = 5 - 8 * p := by rw [hp2]; ring
  rw [hp3, hp6]
  ring

end D0.Research.Q8AFSpinorSeed
