import D0.Core.Phi
import D0.Foundation.Omega8Center
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

/-! ## Typed Q8-center → EXISTING Golden sign port

The original Q8 center (and its commutator [i,j]=-1) is a
SEPARATE actual formal carrier from this interferometer's real sign
port.  Here we construct an exact purely mathematical bridge using
ONLY pre-existing Q8 group multiplication and pre-existing Golden
controlledSign(s). It tests whether an ORIGINAL center bit COULD be
read by a controlled experiment if a genuine native controller supplies
the actual sign. This does NOT prove that GoldenCoherentMemory.fullStep
itself accepts Q8, nor that G0 physically realizes/charges this
controlled routing or an inverse/repeated coherent history.
-/

/-- Mathematical decoding of the ALREADY OWNED central Q8 ±1 pair.
Only intended for center inputs with q=qONE or q=qNEG. -/
def q8_center_sign (q : D0.Foundation.UQuat) : ℝ :=
  if q = D0.Foundation.qNEG then -1 else 1

theorem q8_center_sign_plus :
    q8_center_sign D0.Foundation.qONE = 1 := by
  simp [q8_center_sign, D0.Foundation.qONE, D0.Foundation.qNEG]

theorem q8_center_sign_minus :
    q8_center_sign D0.Foundation.qNEG = -1 := by
  simp [q8_center_sign]

/-- The ORIGINAL Q8 order commutator already yields the minus input
which the separately registered Golden order detector can distinguish. -/
theorem original_q8_ij_order_has_negative_golden_sign :
    q8_center_sign
      (D0.Foundation.uqmul
        (D0.Foundation.uqmul (0,1,0,0) (0,0,1,0))
        (D0.Foundation.uqmul
          (D0.Foundation.uqinv (0,1,0,0))
          (D0.Foundation.uqinv (0,0,1,0)))) = -1 := by
  rw [D0.Foundation.commutator_ij_eq_neg]
  exact q8_center_sign_minus

/-- An EXACT positive Golden order-port comparison of native Q8
center records: the +1 central class has a dark second port,
while the -1 commutator class gives probability 4*p^3 >0.
No new angle, detector, or Q8 group operation has been defined. -/
theorem q8_center_order_golden_detectable :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    (output a p (q8_center_sign D0.Foundation.qONE) 1)^2 = 0 ∧
    (output a p (q8_center_sign D0.Foundation.qNEG) 1)^2 = 4*p^3 ∧
    0 < (output a p (q8_center_sign D0.Foundation.qNEG) 1)^2 := by
  dsimp
  have ha := Real.sq_sqrt (le_of_lt primitive_positive)
  have hp := D0.primitive_root_satisfies
  rw [q8_center_sign_plus, q8_center_sign_minus]
  have hplus := plus_path_returns (Real.sqrt D0.primitiveRoot) D0.primitiveRoot ha hp
  have hminus := minus_path_weights (Real.sqrt D0.primitiveRoot) D0.primitiveRoot ha hp
  refine ⟨?_, hminus.2.1, ?_⟩
  · rw [hplus]
    norm_num
  · rw [hminus.2.1]
    exact mul_pos (by norm_num) (pow_pos primitive_positive _)


end D0.Representation.GoldenOrderInterferometer
