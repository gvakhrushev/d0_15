import D0.Representation.OrderMemoryReadout
import D0.Representation.GoldenOrderInterferometer

/-!
# Identifying a local quaternion axis with independent comparison words

A general pure unit quaternion B=x*i+y*j+z*k obeys B^2=-I. The original
j-reference word sees only y^2. Three reference words yield responses
4*p^3*(1-x^2), 4*p^3*(1-y^2), 4*p^3*(1-z^2).
These statements hold over real coefficients, not only over sampled axes.
They describe a representation class; no claim that all its members are
M1-admissible interactions is made. The source Q8 axes are explicit members.
-/

namespace D0.Representation.CouplingAxisReadout

open Matrix
abbrev M4 := Matrix (Fin 4) (Fin 4) ℝ

def axis (x y z : ℝ) : M4 :=
  !![0,-x,-y,-z; x,0,-z,y; y,z,0,-x; z,-y,x,0]
def reference : Fin 3 → M4 := ![axis 1 0 0, axis 0 1 0, axis 0 0 1]
def coordinate (x y z : ℝ) : Fin 3 → ℝ := ![x,y,z]

/-- This real-coordinate formula is exactly the earlier rational source formula. -/
theorem source_agreement (x y z : ℚ) :
    axis x y z = (D0.Representation.OrderMemoryReadout.left 0 x y z).map (Rat.castHom ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [axis, D0.Representation.OrderMemoryReadout.left]

theorem axis_skew (x y z : ℝ) : (axis x y z).transpose = -axis x y z := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [axis]

theorem axis_orthogonal (x y z : ℝ) (h : x^2+y^2+z^2=1) :
    (axis x y z).transpose * axis x y z = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [axis, Matrix.mul_apply, Fin.sum_univ_succ] <;> nlinarith

theorem reference_orthogonal (a : Fin 3) : (reference a).transpose * reference a = 1 := by
  fin_cases a <;> exact axis_orthogonal _ _ _ (by norm_num)

/-- Chronological local B, common axis, local B^-1, common axis^-1.
Since both generators are pure unit quaternions their inverse signs cancel. -/
def comparison (x y z : ℝ) (a : Fin 3) : M4 :=
  reference a * axis x y z * reference a * axis x y z

theorem comparison_orthogonal (x y z : ℝ) (h : x^2+y^2+z^2=1) (a : Fin 3) :
    (comparison x y z a).transpose * comparison x y z a = 1 := by
  have hb := axis_orthogonal x y z h
  have ha := reference_orthogonal a
  simp only [comparison, Matrix.transpose_mul, mul_assoc]
  simp only [← mul_assoc, ha, one_mul]
  simp only [mul_assoc, hb, mul_one]
  simp only [← mul_assoc, ha, one_mul, hb]

set_option maxHeartbeats 1200000 in
theorem comparison_symmetric_part (x y z : ℝ) (h : x^2+y^2+z^2=1) (a : Fin 3) :
    (comparison x y z a).transpose + comparison x y z a =
      (4*(coordinate x y z a)^2-2) • (1 : M4) := by
  fin_cases a <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [comparison, reference, coordinate, axis, Matrix.mul_apply, Fin.sum_univ_succ] <;>
    nlinarith

theorem comparison_distance (x y z : ℝ) (h : x^2+y^2+z^2=1) (a : Fin 3) :
    (comparison x y z a - 1).transpose * (comparison x y z a - 1) =
      (4*(1-(coordinate x y z a)^2)) • (1 : M4) := by
  have hc := comparison_orthogonal x y z h a
  have hs := comparison_symmetric_part x y z h a
  calc
    _ = (2 : ℝ) • (1 : M4) -
        ((comparison x y z a).transpose + comparison x y z a) := by
      simp only [Matrix.transpose_sub, Matrix.transpose_one, sub_mul, mul_sub,
        hc, mul_one, one_mul]
      module
    _ = _ := by rw [hs, ← sub_smul]; congr 1; ring

/-- The second-port map of the golden comparator is sqrt(p)*p*(C-I).
After normalized quadratic readout its coefficient is p^3 times the distance. -/
def weight (p x y z : ℝ) (a : Fin 3) : ℝ :=
  4*p^3*(1-(coordinate x y z a)^2)

theorem second_port_gram (p x y z : ℝ) (h : x^2+y^2+z^2=1) (a : Fin 3) :
    p^3 • ((comparison x y z a - 1).transpose * (comparison x y z a - 1)) =
      weight p x y z a • (1 : M4) := by
  rw [comparison_distance x y z h a, smul_smul]
  unfold weight
  congr 1
  ring

theorem three_readouts_sum (p x y z : ℝ) (h : x^2+y^2+z^2=1) :
    (∑ a : Fin 3, weight p x y z a) = 8*p^3 := by
  simp [weight, coordinate, Fin.sum_univ_succ]
  linear_combination (-4*p^3)*h

/-- The splitter can be calibrated independently: its second-port weight on
one occupied input is beta=p^2. The comparison sum is then a polynomial in beta. -/
theorem independently_calibrated_sum (p x y z : ℝ)
    (hp : p+p^2=1) (h : x^2+y^2+z^2=1) :
    (∑ a : Fin 3, weight p x y z a) = 8*(p^2)*(1-p^2) := by
  rw [three_readouts_sum p x y z h]
  linear_combination (8*p^2)*hp

theorem recover_coordinate_square (p x y z : ℝ) (hp : p ≠ 0) (a : Fin 3) :
    (coordinate x y z a)^2 = 1 - weight p x y z a / (4*p^3) := by
  unfold weight
  field_simp [hp]
  <;> ring

theorem one_reference_ambiguous (p : ℝ) : weight p 1 0 0 1 = weight p 0 0 1 1 := by
  simp [weight, coordinate]

theorem second_reference_separates (p : ℝ) (hp : p ≠ 0) :
    weight p 1 0 0 0 ≠ weight p 0 0 1 0 := by
  simp [weight, coordinate, hp]

/-- The three weights identify squared components, not their relative signs. -/
theorem sign_reversal_invisible (p x y z : ℝ) (a : Fin 3) :
    weight p (-x) (-y) (-z) a = weight p x y z a := by
  fin_cases a <;> simp [weight, coordinate]

/-- A measured residual in the i-reference channel gives exactly the squared
transverse component, so approximate agreement can be quantified. -/
theorem transverse_fraction (p x y z : ℝ) (hp : p ≠ 0) (h : x^2+y^2+z^2=1) :
    y^2+z^2 = weight p x y z 0 / (4*p^3) := by
  have hx := recover_coordinate_square p x y z hp 0
  simp only [coordinate, Matrix.cons_val_zero] at hx
  linarith

theorem zero_i_readout_forces_axis (p x y z : ℝ) (hp : p ≠ 0)
    (h : x^2+y^2+z^2=1) (hw : weight p x y z 0 = 0) :
    (x=1 ∨ x = -1) ∧ y=0 ∧ z=0 := by
  have ht := transverse_fraction p x y z hp h
  rw [hw, zero_div] at ht
  have hy : y=0 := by nlinarith [sq_nonneg z]
  have hz : z=0 := by nlinarith [sq_nonneg y]
  have hx : x^2=1 := by nlinarith
  exact ⟨(sq_eq_one_iff).mp hx, hy, hz⟩

/-! Fixed terminal actions, as opposed to an enlarged unit-quaternion class. -/

/-- Read the imaginary coordinates from the existing representation's identity
column; do not insert a desired profile as source data. -/
def sourceDirection (g : Fin 8) : Fin 3 → ℚ :=
  ![D0.Representation.OrderMemoryReadout.spin g 1 0,
    D0.Representation.OrderMemoryReadout.spin g 2 0,
    D0.Representation.OrderMemoryReadout.spin g 3 0]

def sourceProfile (g : Fin 8) (a : Fin 3) : ℚ := 1-(sourceDirection g a)^2

/-- In the fixed Q8 table, every quarter-turn has exactly one zero and two unit
responses. The profile is unique UP TO REFERENCE PERMUTATION in this class. -/
theorem fixed_terminal_profile : ∀ g : Fin 8, D0.Claims.Q8.mul g g = 1 →
    ∃ a : Fin 3, ∀ b : Fin 3, sourceProfile g b = if b=a then 0 else 1 := by
  native_decide

theorem all_three_source_axes_exist : ∀ a : Fin 3, ∃ g : Fin 8,
    D0.Claims.Q8.mul g g = 1 ∧
    ∀ b : Fin 3, sourceProfile g b = if b=a then 0 else 1 := by native_decide

theorem quarter_turn_source_is_pure : ∀ g : Fin 8, D0.Claims.Q8.mul g g = 1 →
    D0.Representation.OrderMemoryReadout.spin g =
      D0.Representation.OrderMemoryReadout.left 0
        (sourceDirection g 0) (sourceDirection g 1) (sourceDirection g 2) := by
  native_decide

/-- A concrete member of the larger representation family is NOT one of the
fixed terminal actions. It cannot silently be admitted as a rival D0 primitive. -/
theorem mixed_axis_outside_terminal : ∀ g : Fin 8,
    D0.Representation.OrderMemoryReadout.left 0 (3/5) 0 (4/5) ≠
      D0.Representation.OrderMemoryReadout.spin g := by native_decide

/-- Simultaneous relabelling i↔k, j↦-j. This moves the references too. -/
def relabel : Fin 8 → Fin 8 := ![0,1,6,7,5,4,2,3]
def relabelFrame : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1,0,0,0;0,0,0,1;0,0,-1,0;0,1,0,0]

theorem relabel_is_bijective : Function.Bijective relabel := by native_decide

theorem relabel_preserves_source_multiplication : ∀ g h,
    relabel (D0.Claims.Q8.mul g h) = D0.Claims.Q8.mul (relabel g) (relabel h) := by
  native_decide

theorem relabel_preserves_norm : relabelFrame.transpose * relabelFrame = 1 := by
  native_decide

theorem relabel_transports_all_source_actions : ∀ g,
    relabelFrame * D0.Representation.OrderMemoryReadout.spin g * relabelFrame.transpose =
      D0.Representation.OrderMemoryReadout.spin (relabel g) := by native_decide

end D0.Representation.CouplingAxisReadout
