import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Representation.GoldenCoherentMemory

/-!
# Q8/AF spinor seed: exact cone and retained gate state

This research module formalizes the finite Hermitian Pauli determinant and
the actual retained blank-record gate's two exact qubit marginals. It does not
identify the cone or this apparatus readout with the physical metric, or derive
a Lorentz link, source, or Einstein dynamics.
-/

namespace D0.Research.Q8AFSpinorSeed

open Matrix

/-- Hermitian 2x2 matrix in real Pauli coordinates (t,x,y,z). -/
def hermitianPauli (t x y z : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![ Complex.ofReal (t + z), Complex.ofReal x - Complex.I * Complex.ofReal y;
      Complex.ofReal x + Complex.I * Complex.ofReal y, Complex.ofReal (t - z) ]

/-- The literal retained blank-record output of the owned four-coordinate gate. -/
def blankRecordOutput (a p : ℝ) : Fin 4 → ℝ :=
  (D0.Representation.GoldenCoherentMemory.fullStep a p).mulVec ![1, 0, 0, 0]

/-- Partial trace over the record bit in apparatus order 00, 01, 10, 11. -/
def systemMarginal (v : Fin 4 → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![v 0 ^ 2 + v 1 ^ 2, v 0 * v 2 + v 1 * v 3;
     v 2 * v 0 + v 3 * v 1, v 2 ^ 2 + v 3 ^ 2]

/-- Partial trace over the system bit in apparatus order 00, 01, 10, 11. -/
def recordMarginal (v : Fin 4 → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![v 0 ^ 2 + v 2 ^ 2, v 0 * v 1 + v 2 * v 3;
     v 1 * v 0 + v 3 * v 2, v 1 ^ 2 + v 3 ^ 2]

/-- The AF-record gate prepares both qubit marginals from its retained pure output. -/
theorem blankRecordOutput_eq (a p : ℝ) :
    blankRecordOutput a p = ![a, 0, 0, p] := by
  have h := D0.Representation.GoldenCoherentMemory.blank_record_evolution a p 1 0
  simpa [blankRecordOutput, D0.Representation.GoldenCoherentMemory.fullStep] using h

/-- The actual blank output has the golden system and record densities. -/
theorem blankRecordOutput_golden_marginals (a p : ℝ)
    (ha : a ^ 2 = p) :
    systemMarginal (blankRecordOutput a p) = !![p, 0; 0, p ^ 2] ∧
    recordMarginal (blankRecordOutput a p) = !![p, 0; 0, p ^ 2] := by
  rw [blankRecordOutput_eq]
  constructor <;> simp [systemMarginal, recordMarginal, ha]

/-- This state is normalized and its Q8 spinor determinant is the owned p^3 weight. -/
theorem blankRecordOutput_golden_trace_det (a p : ℝ)
    (ha : a ^ 2 = p) (hp : p + p ^ 2 = 1) :
    (systemMarginal (blankRecordOutput a p)).trace = 1 ∧
    (systemMarginal (blankRecordOutput a p)).det = p ^ 3 := by
  have hm := (blankRecordOutput_golden_marginals a p ha).1
  rw [hm]
  constructor
  · simpa using hp
  · simp [Matrix.det_fin_two_of]
    ring

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

#print axioms D0.Research.Q8AFSpinorSeed.hermitianPauli_det
#print axioms D0.Research.Q8AFSpinorSeed.blankRecordOutput_eq
#print axioms D0.Research.Q8AFSpinorSeed.blankRecordOutput_golden_marginals
#print axioms D0.Research.Q8AFSpinorSeed.blankRecordOutput_golden_trace_det
#print axioms D0.Research.Q8AFSpinorSeed.golden_half_gap
#print axioms D0.Research.Q8AFSpinorSeed.golden_feedback_corner_complement
