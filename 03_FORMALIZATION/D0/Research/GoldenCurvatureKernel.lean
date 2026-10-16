import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Algebra.Ring.Parity

/-!
# Four-cylinder moments and a degree-four coefficient filter

Scalar algebra on the existing cylinder weight `D0.CondensedAnchor.cylWeight`.
The four words are the length-two readout cylinders. The reading
`FF/RR ↦ 0`, `FR ↦ 1`, `RF ↦ -1` is an assigned integer, not a curvature
hypothesis. The three-point filter extracts the quadratic coefficient of
`b + a t² + c t⁴`. The golden ratio enters only as a specialization of that
parameter. Nothing here is a metric variation, a Gauss identity, or an
action principle.
-/

namespace D0.Research.GoldenCurvatureKernel

open Real D0.CondensedAnchor
open scoped goldenRatio

/-- The four length-two cylinders. `true` is the direct letter and `false` is the return letter,
as in `cylWeight`. -/
inductive FourCylinder
  | FF | FR | RF | RR

def word : FourCylinder → List Bool
  | .FF => [true, true]
  | .FR => [true, false]
  | .RF => [false, true]
  | .RR => [false, false]

/-- Assigned two-letter reading: `FF/RR ↦ 0`, `FR ↦ 1`, `RF ↦ -1`. -/
def epsilon : FourCylinder → ℤ
  | .FF => 0
  | .FR => 1
  | .RF => -1
  | .RR => 0

lemma weightExp_FF : weightExp (word .FF) = 2 := by simp [word, weightExp]
lemma weightExp_FR : weightExp (word .FR) = 3 := by simp [word, weightExp]
lemma weightExp_RF : weightExp (word .RF) = 3 := by simp [word, weightExp]
lemma weightExp_RR : weightExp (word .RR) = 4 := by simp [word, weightExp]

lemma cylWeight_FF : cylWeight (word .FF) = (φ⁻¹) ^ 2 := by
  rw [cylWeight_eq_pow, weightExp_FF]

lemma cylWeight_FR : cylWeight (word .FR) = (φ⁻¹) ^ 3 := by
  rw [cylWeight_eq_pow, weightExp_FR]

lemma cylWeight_RF : cylWeight (word .RF) = (φ⁻¹) ^ 3 := by
  rw [cylWeight_eq_pow, weightExp_RF]

lemma cylWeight_RR : cylWeight (word .RR) = (φ⁻¹) ^ 4 := by
  rw [cylWeight_eq_pow, weightExp_RR]

noncomputable section

/-- Sum of `cylWeight` over the four cylinders. This is the owner measure, not a second weight. -/
def cylinderExpect (f : FourCylinder → ℝ) : ℝ :=
  cylWeight (word .FF) * f .FF + cylWeight (word .FR) * f .FR
    + cylWeight (word .RF) * f .RF + cylWeight (word .RR) * f .RR

def cylinderMoment (k : ℕ) : ℝ :=
  cylinderExpect (fun c => (epsilon c : ℝ) ^ k)

theorem fourCylinderMass :
    cylWeight (word .FF) + cylWeight (word .FR)
      + cylWeight (word .RF) + cylWeight (word .RR) = 1 := by
  rw [cylWeight_FF, cylWeight_FR, cylWeight_RF, cylWeight_RR]
  have hone : (1 : ℝ) + φ⁻¹ = φ := by
    have hinv : φ⁻¹ = φ - 1 := by
      rw [inv_goldenRatio, ← one_sub_goldenConj]
      ring
    linear_combination hinv
  calc
    (φ⁻¹) ^ 2 + (φ⁻¹) ^ 3 + (φ⁻¹) ^ 3 + (φ⁻¹) ^ 4
        = (φ⁻¹) ^ 2 * (1 + φ⁻¹) ^ 2 := by ring
    _ = (φ⁻¹) ^ 2 * φ ^ 2 := by rw [hone]
    _ = (φ⁻¹ * φ) ^ 2 := by ring
    _ = 1 := by rw [inv_mul_cancel₀ goldenRatio_ne_zero, one_pow]

theorem cylinderExpect_const (r : ℝ) : cylinderExpect (fun _ => r) = r := by
  simp only [cylinderExpect]
  calc
    cylWeight (word .FF) * r + cylWeight (word .FR) * r
        + cylWeight (word .RF) * r + cylWeight (word .RR) * r
        = (cylWeight (word .FF) + cylWeight (word .FR)
            + cylWeight (word .RF) + cylWeight (word .RR)) * r := by ring
    _ = 1 * r := by rw [fourCylinderMass]
    _ = r := by ring

theorem cylinderMoment_odd {k : ℕ} (hk : Odd k) : cylinderMoment k = 0 := by
  have hk0 : k ≠ 0 := hk.pos.ne'
  have hFF : (epsilon .FF : ℝ) ^ k = 0 := by
    simp only [epsilon, Int.cast_zero, zero_pow hk0]
  have hRR : (epsilon .RR : ℝ) ^ k = 0 := by
    simp only [epsilon, Int.cast_zero, zero_pow hk0]
  have hFR : (epsilon .FR : ℝ) ^ k = 1 := by
    simp only [epsilon, Int.cast_one, one_pow]
  have hRF : (epsilon .RF : ℝ) ^ k = -1 := by
    simp only [epsilon, Int.cast_neg, Int.cast_one]
    exact hk.neg_one_pow
  have hw : cylWeight (word .FR) = cylWeight (word .RF) := by
    rw [cylWeight_FR, cylWeight_RF]
  simp only [cylinderMoment, cylinderExpect, hFF, hRR, hFR, hRF, mul_zero, mul_one, mul_neg,
    zero_add, add_zero, hw]
  ring

theorem cylinderMoment_one : cylinderMoment 1 = 0 :=
  cylinderMoment_odd ⟨0, rfl⟩

theorem cylinderMoment_three : cylinderMoment 3 = 0 :=
  cylinderMoment_odd ⟨1, rfl⟩

theorem cylinderMoment_two : cylinderMoment 2 = 2 * (φ⁻¹) ^ 3 := by
  have hFF : (epsilon .FF : ℝ) ^ 2 = 0 := by norm_num [epsilon]
  have hFR : (epsilon .FR : ℝ) ^ 2 = 1 := by norm_num [epsilon]
  have hRF : (epsilon .RF : ℝ) ^ 2 = 1 := by norm_num [epsilon]
  have hRR : (epsilon .RR : ℝ) ^ 2 = 0 := by norm_num [epsilon]
  simp only [cylinderMoment, cylinderExpect, hFF, hFR, hRF, hRR, mul_zero, mul_one, zero_add,
    add_zero]
  rw [cylWeight_FR, cylWeight_RF]
  ring

theorem epsilon_pow_four_eq_two (c : FourCylinder) :
    (epsilon c : ℝ) ^ 4 = (epsilon c : ℝ) ^ 2 := by
  cases c <;> norm_num [epsilon]

theorem cylinderMoment_four : cylinderMoment 4 = 2 * (φ⁻¹) ^ 3 := by
  have h (c : FourCylinder) : (epsilon c : ℝ) ^ 4 = (epsilon c : ℝ) ^ 2 :=
    epsilon_pow_four_eq_two c
  calc
    cylinderMoment 4
        = cylWeight (word .FF) * (epsilon .FF : ℝ) ^ 2
          + cylWeight (word .FR) * (epsilon .FR : ℝ) ^ 2
          + cylWeight (word .RF) * (epsilon .RF : ℝ) ^ 2
          + cylWeight (word .RR) * (epsilon .RR : ℝ) ^ 2 := by
            simp only [cylinderMoment, cylinderExpect]
            rw [h .FF, h .FR, h .RF, h .RR]
    _ = cylinderMoment 2 := by simp only [cylinderMoment, cylinderExpect]
    _ = 2 * (φ⁻¹) ^ 3 := cylinderMoment_two

/-- Expectation of `b₀ + α ε² t² + γ ε⁴ t⁴` under `cylWeight`. -/
theorem cylinderExpect_degreeFour_shape (b0 alpha gamma t : ℝ) :
    cylinderExpect (fun c =>
        b0 + alpha * (epsilon c : ℝ) ^ 2 * t ^ 2 + gamma * (epsilon c : ℝ) ^ 4 * t ^ 4)
      = b0 + (alpha * cylinderMoment 2) * t ^ 2 + (gamma * cylinderMoment 4) * t ^ 4 := by
  have hconst := cylinderExpect_const b0
  calc
    cylinderExpect (fun c =>
        b0 + alpha * (epsilon c : ℝ) ^ 2 * t ^ 2 + gamma * (epsilon c : ℝ) ^ 4 * t ^ 4)
        = cylinderExpect (fun _ => b0)
          + t ^ 2 * alpha * cylinderExpect (fun c => (epsilon c : ℝ) ^ 2)
          + t ^ 4 * gamma * cylinderExpect (fun c => (epsilon c : ℝ) ^ 4) := by
            simp only [cylinderExpect]
            ring
    _ = b0 + (alpha * cylinderMoment 2) * t ^ 2 + (gamma * cylinderMoment 4) * t ^ 4 := by
          simp only [cylinderMoment, hconst]
          ring

/-- Polynomial whose quadratic and degree-four coefficients are the ones the filter sees. -/
def degreeFour (b a c t : ℝ) : ℝ :=
  b + a * t ^ 2 + c * t ^ 4

/-- Dimensionless weights that kill the constant and the degree-four term and normalize `t²`. -/
def coeffC0 (lam : ℝ) : ℝ := -(lam ^ 2 + 1) / lam ^ 2

def coeffC1 (lam : ℝ) : ℝ := lam ^ 2 / (lam ^ 2 - 1)

def coeffC2 (lam : ℝ) : ℝ := -1 / (lam ^ 2 * (lam ^ 2 - 1))

def threePointFilter (lam t b a c : ℝ) : ℝ :=
  coeffC0 lam * degreeFour b a c 0
    + coeffC1 lam * degreeFour b a c t
    + coeffC2 lam * degreeFour b a c (lam * t)

theorem coeff_system {lam : ℝ} (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1) :
    coeffC0 lam + coeffC1 lam + coeffC2 lam = 0
      ∧ coeffC1 lam + coeffC2 lam * lam ^ 2 = 1
      ∧ coeffC1 lam + coeffC2 lam * lam ^ 4 = 0 := by
  have hden2 : lam ^ 2 ≠ 0 := pow_ne_zero 2 h0
  have hden : lam ^ 2 - 1 ≠ 0 := sub_ne_zero.mpr h1
  unfold coeffC0 coeffC1 coeffC2
  refine ⟨?_, ?_, ?_⟩
  · field_simp [hden2, hden]
    ring_nf
  · field_simp [hden2, hden]
    ring_nf
  · field_simp [hden2, hden]
    ring_nf

theorem coeff_unique {lam x0 x1 x2 : ℝ} (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1)
    (hc : x0 + x1 + x2 = 0) (hq : x1 + x2 * lam ^ 2 = 1) (hqu : x1 + x2 * lam ^ 4 = 0) :
    x0 = coeffC0 lam ∧ x1 = coeffC1 lam ∧ x2 = coeffC2 lam := by
  have hden2 : lam ^ 2 ≠ 0 := pow_ne_zero 2 h0
  have hden : lam ^ 2 - 1 ≠ 0 := sub_ne_zero.mpr h1
  have hx2 : x2 = coeffC2 lam := by
    have hsub : x2 * (lam ^ 4 - lam ^ 2) = -1 := by
      linear_combination hqu - hq
    have hdiff : lam ^ 4 - lam ^ 2 = lam ^ 2 * (lam ^ 2 - 1) := by ring
    have hmul : x2 * (lam ^ 2 * (lam ^ 2 - 1)) = -1 := by
      rw [← hdiff]
      exact hsub
    have : x2 = -1 / (lam ^ 2 * (lam ^ 2 - 1)) := by
      rw [eq_div_iff (mul_ne_zero hden2 hden)]
      simpa [mul_assoc] using hmul
    simpa [coeffC2] using this
  have hx1 : x1 = coeffC1 lam := by
    have hx1' : x1 = 1 - x2 * lam ^ 2 := by linear_combination hq
    rw [hx1', hx2]
    unfold coeffC1 coeffC2
    field_simp [hden2, hden]
    ring_nf
  have hx0 : x0 = coeffC0 lam := by
    have hx0' : x0 = -(x1 + x2) := by linear_combination hc
    rw [hx0', hx1, hx2]
    unfold coeffC0 coeffC1 coeffC2
    field_simp [hden2, hden]
    ring_nf
  exact ⟨hx0, hx1, hx2⟩

/-- For admissible `lam` (`lam ≠ 0` and `lam² ≠ 1`), the filter cancels `b` and `c` and returns `a t²`. -/
theorem threePointFilter_eq_quadratic {lam t b a c : ℝ} (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1) :
    threePointFilter lam t b a c = a * t ^ 2 := by
  obtain ⟨hc, hq, hqu⟩ := coeff_system h0 h1
  have hpoly :
      threePointFilter lam t b a c
        = (coeffC0 lam + coeffC1 lam + coeffC2 lam) * b
          + (coeffC1 lam + coeffC2 lam * lam ^ 2) * (a * t ^ 2)
          + (coeffC1 lam + coeffC2 lam * lam ^ 4) * (c * t ^ 4) := by
    unfold threePointFilter degreeFour
    ring
  rw [hpoly, hc, hq, hqu]
  ring

theorem threePointFilter_of_cylinder_shape {lam t b0 alpha gamma : ℝ}
    (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1) :
    threePointFilter lam t b0 (alpha * cylinderMoment 2) (gamma * cylinderMoment 4)
      = alpha * cylinderMoment 2 * t ^ 2 :=
  threePointFilter_eq_quadratic h0 h1

/-- The same additive constant on all three samples does not change the reading. -/
theorem joint_spectator_on_samples {lam f0 ft fl r : ℝ} (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1) :
    coeffC0 lam * (f0 + r) + coeffC1 lam * (ft + r) + coeffC2 lam * (fl + r)
      = coeffC0 lam * f0 + coeffC1 lam * ft + coeffC2 lam * fl := by
  have hsum := (coeff_system h0 h1).1
  linear_combination r * hsum

theorem joint_spectator_blank_preserves_filter {lam t b a c r : ℝ}
    (h0 : lam ≠ 0) (h1 : lam ^ 2 ≠ 1) :
    threePointFilter lam t (b + r) a c = threePointFilter lam t b a c := by
  rw [threePointFilter_eq_quadratic h0 h1, threePointFilter_eq_quadratic h0 h1]

def goldenContrast (t b a c : ℝ) : ℝ :=
  φ ^ 4 * (degreeFour b a c t - degreeFour b a c 0)
    - (degreeFour b a c (φ * t) - degreeFour b a c 0)

theorem golden_lambda_admissible : φ ≠ 0 ∧ φ ^ 2 ≠ 1 := by
  refine ⟨goldenRatio_ne_zero, ?_⟩
  intro h
  have hsq : φ ^ 2 = φ + 1 := goldenRatio_sq
  have hsum : φ + 1 = 1 := by rw [← hsq, h]
  have hφ : φ = 0 := by simpa using congrArg (fun x : ℝ => x - 1) hsum
  exact goldenRatio_ne_zero hφ

theorem goldenContrast_scale (t b a c : ℝ) :
    goldenContrast t b a c = a * (φ ^ 4 - φ ^ 2) * t ^ 2 := by
  unfold goldenContrast degreeFour
  ring

theorem golden_pair_weight_calibration : (φ⁻¹) ^ 3 * (φ ^ 4 - φ ^ 2) = 1 := by
  have hsq : φ ^ 2 = φ + 1 := goldenRatio_sq
  have hstep : φ ^ 2 - 1 = φ := by linear_combination hsq
  have hpow : φ ^ 4 - φ ^ 2 = φ ^ 3 := by
    calc
      φ ^ 4 - φ ^ 2 = φ ^ 2 * (φ ^ 2 - 1) := by ring
      _ = φ ^ 2 * φ := by rw [hstep]
      _ = φ ^ 3 := by ring
  rw [hpow, ← mul_pow, inv_mul_cancel₀ goldenRatio_ne_zero, one_pow]

/-- If the quadratic coefficient is the golden pair weight times `rho`, the `φ`-contrast returns `rho t²`.
The degree-four coefficient cancels for every `c`. -/
theorem golden_specialization (t b rho c : ℝ) :
    goldenContrast t b ((φ⁻¹) ^ 3 * rho) c = rho * t ^ 2 := by
  rw [goldenContrast_scale]
  calc
    (φ⁻¹) ^ 3 * rho * (φ ^ 4 - φ ^ 2) * t ^ 2
        = rho * ((φ⁻¹) ^ 3 * (φ ^ 4 - φ ^ 2)) * t ^ 2 := by ring
    _ = rho * 1 * t ^ 2 := by rw [golden_pair_weight_calibration]
    _ = rho * t ^ 2 := by ring

theorem golden_specialization_div {t b rho c : ℝ} (ht : t ≠ 0) :
    goldenContrast t b ((φ⁻¹) ^ 3 * rho) c / t ^ 2 = rho := by
  rw [golden_specialization]
  field_simp [ht]

theorem golden_filter_matches_contrast {t b a c : ℝ} :
    threePointFilter φ t b a c = goldenContrast t b a c / (φ ^ 2 * (φ ^ 2 - 1)) := by
  obtain ⟨h0, h1⟩ := golden_lambda_admissible
  have hden : φ ^ 2 * (φ ^ 2 - 1) ≠ 0 :=
    mul_ne_zero (pow_ne_zero 2 h0) (sub_ne_zero.mpr h1)
  rw [threePointFilter_eq_quadratic h0 h1, goldenContrast_scale]
  have hfac : φ ^ 4 - φ ^ 2 = φ ^ 2 * (φ ^ 2 - 1) := by ring
  rw [hfac]
  set D : ℝ := φ ^ 2 * (φ ^ 2 - 1)
  have hD : D ≠ 0 := by simpa [D] using hden
  field_simp [hD]

/-- Adding one common constant at every scale, including the blank, does not change the contrast. -/
theorem joint_spectator_blank_preserves_goldenContrast (t b a c r : ℝ) :
    goldenContrast t (b + r) a c = goldenContrast t b a c := by
  unfold goldenContrast degreeFour
  ring

/-! ### Counterexamples -/

def massWithoutRR : ℝ :=
  cylWeight (word .FF) + cylWeight (word .FR) + cylWeight (word .RF)

theorem dropRR_mass_ne_one : massWithoutRR ≠ 1 := by
  intro h
  have hsplit : massWithoutRR + cylWeight (word .RR) = 1 := by
    simpa [massWithoutRR] using fourCylinderMass
  have hzero : cylWeight (word .RR) = 0 := by linear_combination hsplit - h
  rw [cylWeight_RR] at hzero
  exact pow_ne_zero 4 (inv_ne_zero goldenRatio_ne_zero) hzero

theorem dropRR_unnormalized_second_moment :
    cylWeight (word .FR) + cylWeight (word .RF) = cylinderMoment 2 := by
  have hFF : (epsilon .FF : ℝ) ^ 2 = 0 := by norm_num [epsilon]
  have hFR : (epsilon .FR : ℝ) ^ 2 = 1 := by norm_num [epsilon]
  have hRF : (epsilon .RF : ℝ) ^ 2 = 1 := by norm_num [epsilon]
  have hRR : (epsilon .RR : ℝ) ^ 2 = 0 := by norm_num [epsilon]
  simp only [cylinderMoment, cylinderExpect, hFF, hFR, hRF, hRR, mul_zero, mul_one, zero_add,
    add_zero]

/-- Deleting `RR` and dividing by the remaining mass does not preserve `cylinderMoment 2`. -/
theorem dropRR_renormalized_second_moment_ne :
    (cylWeight (word .FR) + cylWeight (word .RF)) / massWithoutRR ≠ cylinderMoment 2 := by
  have hmom := dropRR_unnormalized_second_moment
  rw [hmom]
  have hs0 : cylinderMoment 2 ≠ 0 := by
    rw [cylinderMoment_two]
    exact mul_ne_zero (by norm_num) (pow_ne_zero 3 (inv_ne_zero goldenRatio_ne_zero))
  set s := cylinderMoment 2
  have hs : s ≠ 0 := by simpa [s] using hs0
  have hm1 : massWithoutRR ≠ 1 := dropRR_mass_ne_one
  have hm0 : massWithoutRR ≠ 0 := by
    have hsplit : massWithoutRR + cylWeight (word .RR) = 1 := by
      simpa [massWithoutRR] using fourCylinderMass
    intro hz
    have hRR : cylWeight (word .RR) = 1 := by linear_combination hsplit - hz
    rw [cylWeight_RR] at hRR
    have hlt : (φ⁻¹) ^ 4 < 1 := by
      have hp : φ⁻¹ < 1 := inv_lt_one_of_one_lt₀ one_lt_goldenRatio
      have hpos : 0 < φ⁻¹ := inv_pos.mpr goldenRatio_pos
      have h4 : (φ⁻¹) ^ 4 < (1 : ℝ) ^ 4 :=
        pow_lt_pow_left₀ hp (le_of_lt hpos) (by decide : (4 : ℕ) ≠ 0)
      simpa using h4
    exact ne_of_lt hlt hRR
  intro h
  have hsm : s = s * massWithoutRR := (div_eq_iff hm0).mp h
  have hcancel : 1 = massWithoutRR :=
    mul_left_cancel₀ hs (by simpa [mul_one] using hsm)
  exact hm1 hcancel.symm

/-- Blank shifted only at scale zero. The probe scales stay on the original polynomial. -/
def frozenBlankContrast (t b a c r : ℝ) : ℝ :=
  φ ^ 4 * (degreeFour b a c t - (degreeFour b a c 0 + r))
    - (degreeFour b a c (φ * t) - (degreeFour b a c 0 + r))

theorem frozen_blank_shift (t b a c r : ℝ) :
    frozenBlankContrast t b a c r = goldenContrast t b a c - (φ ^ 4 - 1) * r := by
  unfold frozenBlankContrast goldenContrast degreeFour
  ring

theorem phi_fourth_ne_one : φ ^ 4 ≠ 1 := by
  intro h
  have hsq : φ ^ 2 = φ + 1 := goldenRatio_sq
  have hstep : φ ^ 2 - 1 = φ := by linear_combination hsq
  have hfac : φ ^ 4 - 1 = φ * (φ ^ 2 + 1) := by
    calc
      φ ^ 4 - 1 = (φ ^ 2 - 1) * (φ ^ 2 + 1) := by ring
      _ = φ * (φ ^ 2 + 1) := by rw [hstep]
  have hz : φ * (φ ^ 2 + 1) = 0 := by
    rw [← hfac]
    exact sub_eq_zero.mpr h
  exact mul_ne_zero goldenRatio_ne_zero (ne_of_gt (by positivity)) hz

/-- A blank frozen off the common value changes the contrast of the zero polynomial. -/
theorem frozen_blank_fails :
    frozenBlankContrast 1 0 0 0 1 ≠ goldenContrast 1 0 0 0 := by
  have hL : frozenBlankContrast 1 0 0 0 1 = -(φ ^ 4 - 1) := by
    rw [frozen_blank_shift, goldenContrast_scale]
    ring
  have hR : goldenContrast 1 0 0 0 = 0 := by
    rw [goldenContrast_scale]
    ring
  rw [hL, hR]
  exact neg_ne_zero.mpr (sub_ne_zero.mpr phi_fourth_ne_one)

/-- Outer weight with the factor `lam²` omitted from the denominator. -/
def wrongCoeffC2 (lam : ℝ) : ℝ := -1 / (lam ^ 2 - 1)

/-- At `lam = 2`, on `F(t) = t⁴`, the wrong outer weight does not return the quadratic coefficient `0`.
The calibrated filter does. -/
theorem wrong_lambda_coefficient_fails :
    (let lam : ℝ := 2
      let c0 := -(coeffC1 lam + wrongCoeffC2 lam)
      c0 * degreeFour 0 0 1 0
        + coeffC1 lam * degreeFour 0 0 1 1
        + wrongCoeffC2 lam * degreeFour 0 0 1 (lam * 1))
      ≠ 0
    ∧ threePointFilter (2 : ℝ) 1 0 0 1 = 0 := by
  refine ⟨?_, ?_⟩
  · norm_num [degreeFour, coeffC1, wrongCoeffC2]
  · have h0 : (2 : ℝ) ≠ 0 := by norm_num
    have h1 : (2 : ℝ) ^ 2 ≠ 1 := by norm_num
    simpa using threePointFilter_eq_quadratic (lam := (2 : ℝ)) (t := 1) (b := 0) (a := 0) (c := 1) h0 h1

/-- Replacing the golden numerator's `φ⁴` by `φ²` does not kill a pure degree-four term. -/
theorem wrong_golden_scale_power_fails :
    φ ^ 2 * (degreeFour 0 0 1 1 - degreeFour 0 0 1 0)
        - (degreeFour 0 0 1 (φ * 1) - degreeFour 0 0 1 0)
      ≠ goldenContrast 1 0 0 1 := by
  have hsq : φ ^ 2 = φ + 1 := goldenRatio_sq
  have hstep : φ ^ 2 - 1 = φ := by linear_combination hsq
  have hpow : φ ^ 4 - φ ^ 2 = φ ^ 3 := by
    calc
      φ ^ 4 - φ ^ 2 = φ ^ 2 * (φ ^ 2 - 1) := by ring
      _ = φ ^ 2 * φ := by rw [hstep]
      _ = φ ^ 3 := by ring
  have hL :
      φ ^ 2 * (degreeFour 0 0 1 1 - degreeFour 0 0 1 0)
        - (degreeFour 0 0 1 (φ * 1) - degreeFour 0 0 1 0)
        = -(φ ^ 3) := by
    unfold degreeFour
    rw [← hpow]
    ring
  have hR : goldenContrast 1 0 0 1 = 0 := by
    rw [goldenContrast_scale]
    ring
  rw [hL, hR]
  exact neg_ne_zero.mpr (pow_ne_zero 3 goldenRatio_ne_zero)

end

#print axioms fourCylinderMass
#print axioms cylinderMoment_one
#print axioms cylinderMoment_two
#print axioms cylinderMoment_three
#print axioms cylinderMoment_four
#print axioms threePointFilter_eq_quadratic
#print axioms coeff_unique
#print axioms golden_pair_weight_calibration
#print axioms golden_specialization
#print axioms golden_specialization_div
#print axioms joint_spectator_blank_preserves_goldenContrast
#print axioms dropRR_mass_ne_one
#print axioms dropRR_renormalized_second_moment_ne
#print axioms frozen_blank_fails
#print axioms wrong_lambda_coefficient_fails
#print axioms wrong_golden_scale_power_fails

end D0.Research.GoldenCurvatureKernel
