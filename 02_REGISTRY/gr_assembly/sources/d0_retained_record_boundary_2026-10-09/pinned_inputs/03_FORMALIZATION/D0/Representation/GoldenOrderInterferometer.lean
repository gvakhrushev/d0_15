import D0.Core.Phi
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# Read the order sign with the existing golden two-port gate

Book 03 §03.26 supplies R_phi = [[sqrt(p),-p],[p,sqrt(p)]], p=phi^-1.
This module computes R_phi^T diag(1,s) R_phi on the prepared first port.
For s=+1 the second port is dark; for s=-1 its normalized squared response
is 4*p^3. Thus a balanced splitter is unnecessary. This is a real algebraic
gate calculation. Controlled routing, inverse access, preparation and the
quadratic apparatus response remain explicit implementation requirements.
-/

namespace D0.Representation.GoldenOrderInterferometer

open Matrix

def gate (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a,-p; p,a]
def controlledSign (s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1,0; 0,s]
def output (a p s : ℝ) : Fin 2 → ℝ :=
  (gate a p).transpose.mulVec ((controlledSign s).mulVec ((gate a p).mulVec ![1,0]))

theorem gate_orthogonal (a p : ℝ) (ha : a^2 = p) (hp : p + p^2 = 1) :
    (gate a p).transpose * gate a p = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [gate, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith

theorem output_formula (a p s : ℝ) :
    output a p s = ![a^2 + s*p^2, (s-1)*a*p] := by
  ext i
  fin_cases i <;>
    simp [output, gate, controlledSign, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> ring

theorem golden_cube (p : ℝ) (hp : p + p^2 = 1) : p - p^2 = p^3 := by
  linear_combination -p*hp

theorem plus_path_returns (a p : ℝ) (ha : a^2 = p) (hp : p + p^2 = 1) :
    output a p 1 = ![1,0] := by
  rw [output_formula, ha]
  simp [hp]

theorem minus_path_output (a p : ℝ) (ha : a^2 = p) (hp : p + p^2 = 1) :
    output a p (-1) = ![p^3, -2*a*p] := by
  rw [output_formula, ha]
  ext i
  fin_cases i <;> simp
  · exact golden_cube p hp
  · ring

theorem golden_response_closure (p : ℝ) (hp : p + p^2 = 1) : p^6 + 4*p^3 = 1 := by
  linear_combination (p^4-p^3+2*p^2+p+1)*hp

theorem minus_path_weights (a p : ℝ) (ha : a^2 = p) (hp : p + p^2 = 1) :
    (output a p (-1) 0)^2 = p^6 ∧
    (output a p (-1) 1)^2 = 4*p^3 ∧ p^6 + 4*p^3 = 1 := by
  rw [minus_path_output a p ha hp]
  refine ⟨?_, ?_, golden_response_closure p hp⟩
  · simp; ring
  · simp
    calc (2*a*p)^2 = 4*a^2*p^2 := by ring
      _ = 4*p^3 := by rw [ha]; ring

theorem primitive_positive : 0 < D0.primitiveRoot := by
  have h : 1 < Real.sqrt 5 := (Real.lt_sqrt (by norm_num)).2 (by norm_num)
  unfold D0.primitiveRoot
  linarith

/-- The same finite quadratic-origin argument also covers algebraic irrational
gate coordinates. This does not assume all positive responses are quadratic. -/
theorem real_quadratic_response (xx xy yy : ℝ)
    (hturn : ∀ x y : ℝ, xx*x*x + xy*x*y + yy*y*y =
      xx*(-y)*(-y) + xy*(-y)*x + yy*x*x)
    (hunit : xx = 1) :
    ∀ x y : ℝ, xx*x*x + xy*x*y + yy*y*y = x*x + y*y := by
  have hd := hturn 1 0
  have hm := hturn 1 1
  have hy : yy = 1 := by nlinarith
  have hc : xy = 0 := by nlinarith
  intro x y
  simp [hunit, hy, hc]

/-- Frozen D0 value, with no free splitter angle. -/
theorem d0_golden_order_readout :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    output a p 1 = ![1,0] ∧
    (output a p (-1) 0)^2 = p^6 ∧
    (output a p (-1) 1)^2 = 4*p^3 ∧
    p^6 + 4*p^3 = 1 ∧ 0 < 4*p^3 := by
  dsimp
  have ha := Real.sq_sqrt (le_of_lt primitive_positive)
  have hp := D0.primitive_root_satisfies
  obtain ⟨h0,h1,hn⟩ := minus_path_weights _ _ ha hp
  exact ⟨plus_path_returns _ _ ha hp, h0,h1,hn,
    mul_pos (by norm_num) (pow_pos primitive_positive _)⟩

end D0.Representation.GoldenOrderInterferometer
