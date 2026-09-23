import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Analysis.SpecialFunctions.Complex.CircleAddChar
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.NumberTheory.LegendreSymbol.AddCharacter
import Mathlib.Tactic

/-!
# Finite-cycle Fourier lemmas

Generic facts about the standard additive character of `ZMod n` and the
second-difference symbol `(2 n sin(π k / n))²`.  These are the Fourier
ingredients of the spatial Hodge shell.  They do not mention Fock space,
`hodgeCarDirac`, or a constitutive metric.
-/

namespace D0.Geometry.FiniteCycleFourier

open Complex Real AddChar
open scoped ComplexConjugate

variable {n : ℕ} [NeZero n]

/-- Standard character `j ↦ exp(2 π i k j / n)`. -/
noncomputable def cycleChar (k j : ZMod n) : ℂ :=
  ZMod.stdAddChar (k * j)

theorem cycleChar_zero_right (k : ZMod n) : cycleChar k 0 = 1 := by
  simp [cycleChar, map_zero_eq_one]

theorem cycleChar_add_right (k j₁ j₂ : ZMod n) :
    cycleChar k (j₁ + j₂) = cycleChar k j₁ * cycleChar k j₂ := by
  simp [cycleChar, mul_add, map_add_eq_mul]

theorem cycleChar_neg_right (k j : ZMod n) :
    cycleChar k (-j) = (cycleChar k j)⁻¹ := by
  have h := cycleChar_add_right k j (-j)
  simp only [add_neg_cancel, cycleChar_zero_right] at h
  exact (inv_eq_of_mul_eq_one_right h.symm).symm

theorem cycleChar_one (k : ZMod n) :
    cycleChar k 1 = exp (2 * ↑Real.pi * I * (k.val : ℂ) / n) := by
  have hval : ((k * 1).val : ℂ) = k.val := by simp
  simp [cycleChar, ZMod.stdAddChar_apply, ZMod.toCircle_apply, hval]

theorem sum_cycleChar (k : ZMod n) :
    ∑ j : ZMod n, cycleChar k j = if k = 0 then (Fintype.card (ZMod n) : ℂ) else 0 := by
  simpa [cycleChar, mul_comm] using
    sum_mulShift (ψ := ZMod.stdAddChar (N := n)) k (ZMod.isPrimitive_stdAddChar n)

theorem sum_cycleChar_eq (k : ZMod n) :
    ∑ j : ZMod n, cycleChar k j = if k = 0 then (n : ℂ) else 0 := by
  rw [sum_cycleChar]
  simp [ZMod.card]

/-- `2 - ω - ω⁻¹ = 4 sin²(π k / n)` for the first step of the character. -/
theorem two_sub_char_eq_sin_sq (k : ZMod n) :
    2 - cycleChar k 1 - (cycleChar k 1)⁻¹ =
      Complex.ofReal (4 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2) := by
  set θ : ℝ := 2 * Real.pi * (k.val : ℝ) / n
  have hθ : (2 * ↑Real.pi * (k.val : ℂ) / n) = (θ : ℂ) := by
    simp only [θ]
    push_cast
    ring_nf
  have hexp : exp (2 * ↑Real.pi * I * (k.val : ℂ) / n) = exp ((θ : ℂ) * I) := by
    congr 1
    rw [← hθ]
    ring_nf
  rw [cycleChar_one, hexp]
  have hz : exp ((θ : ℂ) * I) = ↑(Real.cos θ) + ↑(Real.sin θ) * I := by
    simpa [mul_comm] using Complex.exp_ofReal_mul_I θ
  have hzinv : (exp ((θ : ℂ) * I))⁻¹ = ↑(Real.cos θ) - ↑(Real.sin θ) * I := by
    rw [← Complex.exp_neg]
    have hneg : -((θ : ℂ) * I) = ((-θ : ℝ) : ℂ) * I := by simp [mul_comm]
    rw [hneg]
    simpa [Real.cos_neg, Real.sin_neg, mul_comm] using Complex.exp_ofReal_mul_I (-θ)
  rw [hzinv, hz]
  have hre : Real.cos θ = 1 - 2 * Real.sin (θ / 2) ^ 2 := by
    simpa [two_mul] using Real.cos_two_mul_eq_one_sub (θ / 2)
  have hhalf : θ / 2 = Real.pi * (k.val : ℝ) / n := by
    simp [θ]
    ring
  have hre4 : 2 - Real.cos θ - Real.cos θ =
      4 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2 := by
    rw [hre, hhalf]
    ring
  have hlhs :
      2 - (↑(Real.cos θ) + ↑(Real.sin θ) * I) - (↑(Real.cos θ) - ↑(Real.sin θ) * I) =
        ↑(2 - Real.cos θ - Real.cos θ) := by
    apply Complex.ext <;>
      simp only [Complex.sub_re, Complex.sub_im, Complex.add_re, Complex.add_im,
        Complex.mul_re, Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im,
        Complex.I_re, Complex.I_im, Complex.re_ofNat, Complex.im_ofNat] <;>
      ring_nf
  rw [hlhs]
  exact congrArg Complex.ofReal hre4

theorem cycleChar_ne_zero (k j : ZMod n) : cycleChar k j ≠ 0 := by
  simp [cycleChar, ZMod.stdAddChar_apply, ZMod.toCircle_apply, Complex.exp_ne_zero]

theorem cycleChar_second_difference (k j : ZMod n) :
    (n : ℂ) ^ 2 * (2 * cycleChar k j - cycleChar k (j + 1) - cycleChar k (j - 1)) =
      Complex.ofReal (4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2) *
        cycleChar k j := by
  have hplus : cycleChar k (j + 1) = cycleChar k j * cycleChar k 1 := by
    simpa using cycleChar_add_right k j 1
  have hstep : cycleChar k (j - 1) * cycleChar k 1 = cycleChar k j := by
    simpa [sub_add_cancel] using (cycleChar_add_right k (j - 1) 1).symm
  have hminus : cycleChar k (j - 1) = cycleChar k j * (cycleChar k 1)⁻¹ := by
    have hne : cycleChar k 1 ≠ 0 := cycleChar_ne_zero k 1
    exact (eq_mul_inv_iff_mul_eq₀ hne).2 hstep
  rw [hplus, hminus]
  have hfactor :
      2 * cycleChar k j - cycleChar k j * cycleChar k 1 -
          cycleChar k j * (cycleChar k 1)⁻¹ =
        cycleChar k j * (2 - cycleChar k 1 - (cycleChar k 1)⁻¹) := by
    ring
  rw [hfactor, two_sub_char_eq_sin_sq]
  push_cast
  ring_nf

theorem sin_sq_of_one (hn : 0 < n) :
    Real.sin (Real.pi * (1 : ℕ) / n) ^ 2 = Real.sin (Real.pi / n) ^ 2 := by
  have : Real.pi * (1 : ℕ) / n = Real.pi / n := by
    simp [Nat.cast_one]
  rw [this]

theorem sin_sq_of_neg_one (hn : 1 ≤ n) (hn0 : n ≠ 0) :
    Real.sin (Real.pi * (n - 1 : ℕ) / n) ^ 2 = Real.sin (Real.pi / n) ^ 2 := by
  have hcast : ((n - 1 : ℕ) : ℝ) = (n : ℝ) - 1 := by
    rw [Nat.cast_sub hn, Nat.cast_one]
  have harg : Real.pi * (n - 1 : ℕ) / n = Real.pi - Real.pi / n := by
    rw [hcast]
    field_simp [hn0]
  rw [harg, Real.sin_pi_sub]

/-- Cosine of the standard character, read on the unit circle. -/
noncomputable def cycleCos (k j : ZMod n) : ℝ :=
  (cycleChar k j).re

/-- Sine of the standard character. -/
noncomputable def cycleSin (k j : ZMod n) : ℝ :=
  (cycleChar k j).im

theorem cycleChar_zero_left (j : ZMod n) : cycleChar 0 j = 1 := by
  simp [cycleChar, zero_mul, map_zero_eq_one]

theorem cycleChar_add_left (k₁ k₂ j : ZMod n) :
    cycleChar (k₁ + k₂) j = cycleChar k₁ j * cycleChar k₂ j := by
  simp [cycleChar, add_mul, map_add_eq_mul]

theorem cycleChar_eq_exp (k j : ZMod n) :
    cycleChar k j = exp (↑(2 * Real.pi * ((k * j).val : ℝ) / n) * I) := by
  simp only [cycleChar, ZMod.stdAddChar_apply, ZMod.toCircle_apply]
  congr 1
  push_cast
  ring_nf

theorem cycleCos_eq (k j : ZMod n) :
    cycleCos k j = Real.cos (2 * Real.pi * ((k * j).val : ℝ) / n) := by
  rw [cycleCos, cycleChar_eq_exp]
  exact Complex.exp_ofReal_mul_I_re _

theorem cycleSin_eq (k j : ZMod n) :
    cycleSin k j = Real.sin (2 * Real.pi * ((k * j).val : ℝ) / n) := by
  rw [cycleSin, cycleChar_eq_exp]
  exact Complex.exp_ofReal_mul_I_im _

theorem cycleChar_conj (k j : ZMod n) :
    conj (cycleChar k j) = cycleChar (-k) j := by
  have hmul : (-k) * j = -(k * j) := by ring
  simp only [cycleChar, hmul, ZMod.stdAddChar_apply]
  rw [AddChar.map_neg_eq_inv (ZMod.toCircle (N := n)) (k * j)]
  exact (Circle.coe_inv_eq_conj (ZMod.toCircle (k * j))).symm

private theorem ofReal_mul_re (a : ℝ) (z : ℂ) : ((a : ℂ) * z).re = a * z.re := by
  simp [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im]

private theorem ofReal_mul_im (a : ℝ) (z : ℂ) : ((a : ℂ) * z).im = a * z.im := by
  simp [Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im]

theorem cycleCos_second_difference (k j : ZMod n) :
    (n : ℝ) ^ 2 * (2 * cycleCos k j - cycleCos k (j + 1) - cycleCos k (j - 1)) =
      4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2 * cycleCos k j := by
  set diff : ℂ := 2 * cycleChar k j - cycleChar k (j + 1) - cycleChar k (j - 1)
  have h := congrArg Complex.re (cycleChar_second_difference k j)
  have hdiff : diff.re =
      2 * cycleCos k j - cycleCos k (j + 1) - cycleCos k (j - 1) := by
    simp only [diff, cycleCos, Complex.sub_re, Complex.add_re, Complex.mul_re, Complex.ofReal_im,
      Complex.re_ofNat, Complex.im_ofNat]
    ring_nf
  have hscale : (((n : ℂ) ^ 2) * diff).re = (n : ℝ) ^ 2 * diff.re := by
    have hn : ((n : ℂ) ^ 2) = ↑((n : ℝ) ^ 2) := by
      push_cast
      ring
    rw [hn]
    exact ofReal_mul_re _ _
  set s : ℝ := 4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2
  have hR : ((s : ℂ) * cycleChar k j).re = s * cycleCos k j := by
    rw [ofReal_mul_re]
    rfl
  calc
    (n : ℝ) ^ 2 * (2 * cycleCos k j - cycleCos k (j + 1) - cycleCos k (j - 1))
        = (n : ℝ) ^ 2 * diff.re := by rw [hdiff]
    _ = (((n : ℂ) ^ 2) * diff).re := hscale.symm
    _ = ((s : ℂ) * cycleChar k j).re := by simpa [diff, s] using h
    _ = s * cycleCos k j := hR

theorem cycleSin_second_difference (k j : ZMod n) :
    (n : ℝ) ^ 2 * (2 * cycleSin k j - cycleSin k (j + 1) - cycleSin k (j - 1)) =
      4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2 * cycleSin k j := by
  set diff : ℂ := 2 * cycleChar k j - cycleChar k (j + 1) - cycleChar k (j - 1)
  have h := congrArg Complex.im (cycleChar_second_difference k j)
  have hdiff : diff.im =
      2 * cycleSin k j - cycleSin k (j + 1) - cycleSin k (j - 1) := by
    simp only [diff, cycleSin, Complex.sub_im, Complex.add_im, Complex.mul_im, Complex.ofReal_re,
      Complex.re_ofNat, Complex.im_ofNat]
    ring_nf
  have hscale : (((n : ℂ) ^ 2) * diff).im = (n : ℝ) ^ 2 * diff.im := by
    have hn : ((n : ℂ) ^ 2) = ↑((n : ℝ) ^ 2) := by
      push_cast
      ring
    rw [hn]
    exact ofReal_mul_im _ _
  set s : ℝ := 4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * (k.val : ℝ) / n) ^ 2
  have hR : ((s : ℂ) * cycleChar k j).im = s * cycleSin k j := by
    rw [ofReal_mul_im]
    rfl
  calc
    (n : ℝ) ^ 2 * (2 * cycleSin k j - cycleSin k (j + 1) - cycleSin k (j - 1))
        = (n : ℝ) ^ 2 * diff.im := by rw [hdiff]
    _ = (((n : ℂ) ^ 2) * diff).im := hscale.symm
    _ = ((s : ℂ) * cycleChar k j).im := by simpa [diff, s] using h
    _ = s * cycleSin k j := hR

theorem sin_fold (hn : 0 < n) {m : ℕ} (hm : m < n) :
    Real.sin (Real.pi * (m : ℝ) / n) =
      Real.sin (Real.pi * (↑(min m (n - m)) : ℝ) / n) := by
  by_cases hle : m ≤ n - m
  · simp [Nat.min_eq_left hle]
  · have hmle : m ≤ n := Nat.le_of_lt hm
    have hgt : n - m < m := Nat.lt_of_not_ge hle
    have hmin : min m (n - m) = n - m := Nat.min_eq_right (Nat.le_of_lt hgt)
    have hcast : ((n - m : ℕ) : ℝ) = (n : ℝ) - (m : ℝ) := Nat.cast_sub hmle
    have harg : Real.pi * (m : ℝ) / n = Real.pi - Real.pi * ((n - m : ℕ) : ℝ) / n := by
      rw [hcast]
      field_simp [hn.ne']
      ring
    rw [harg, Real.sin_pi_sub, hmin]

theorem sin_mem_upper (hn : 0 < n) {m : ℕ} (hm : m ≤ n) :
    Real.pi * (m : ℝ) / n ∈ Set.Icc 0 Real.pi := by
  constructor
  · positivity
  · rw [div_le_iff₀ (by exact_mod_cast hn : (0 : ℝ) < n)]
    have hmle : (m : ℝ) ≤ n := by exact_mod_cast hm
    nlinarith [Real.pi_pos]

theorem sin_first_pos (hn : 2 ≤ n) : 0 < Real.sin (Real.pi / n) := by
  have hn0 : 0 < n := by omega
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn0
  refine Real.sin_pos_of_pos_of_lt_pi (div_pos Real.pi_pos hnpos) ?_
  rw [div_lt_iff₀ hnpos]
  have h1 : (1 : ℝ) < n := by exact_mod_cast (by omega : 1 < n)
  nlinarith [Real.pi_pos]

/-- On a cycle of length at least 3, `sin²(π m / n) = sin²(π / n)` exactly at the first harmonics. -/
theorem sin_sq_eq_first_harmonic_iff (hn : 3 ≤ n) {m : ℕ} (hm : m < n) :
    Real.sin (Real.pi * (m : ℝ) / n) ^ 2 = Real.sin (Real.pi / n) ^ 2 ↔
      m = 1 ∨ m = n - 1 := by
  have hn0 : 0 < n := by omega
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn0
  constructor
  · intro hsq
    by_cases hm0 : m = 0
    · exfalso
      have hzero : Real.sin (Real.pi * (m : ℝ) / n) = 0 := by simp [hm0]
      have hpos := sin_first_pos (by omega : 2 ≤ n)
      have : Real.sin (Real.pi / n) ^ 2 = 0 := by simpa [hzero] using hsq.symm
      exact (sq_pos_of_pos hpos).ne' this
    · have hsin_nonneg : 0 ≤ Real.sin (Real.pi * (m : ℝ) / n) :=
        Real.sin_nonneg_of_nonneg_of_le_pi (by positivity)
          (sin_mem_upper hn0 (Nat.le_of_lt hm)).2
      have hsin1_nonneg : 0 ≤ Real.sin (Real.pi / n) :=
        (sin_first_pos (by omega)).le
      have hsin_eq : Real.sin (Real.pi * (m : ℝ) / n) = Real.sin (Real.pi / n) :=
        (sq_eq_sq₀ hsin_nonneg hsin1_nonneg).mp hsq
      let m' : ℕ := min m (n - m)
      have hfold := sin_fold hn0 hm
      have hm'eq : Real.sin (Real.pi * (m' : ℝ) / n) = Real.sin (Real.pi / n) := by
        simpa [m'] using hfold.symm.trans hsin_eq
      have h2le : 2 * m' ≤ n := by
        have hleft : m' ≤ m := Nat.min_le_left _ _
        have hright : m' ≤ n - m := Nat.min_le_right _ _
        have hsum : m + (n - m) = n := Nat.add_sub_of_le (Nat.le_of_lt hm)
        omega
      have hangle_le : Real.pi * (m' : ℝ) / n ≤ Real.pi / 2 := by
        rw [div_le_div_iff₀ hnpos two_pos]
        have hcast : 2 * (m' : ℝ) ≤ n := by exact_mod_cast h2le
        nlinarith [Real.pi_pos]
      have hmem1 : Real.pi / n ∈ Set.Icc (-(Real.pi / 2)) (Real.pi / 2) := by
        constructor
        · linarith [Real.pi_nonneg, div_nonneg Real.pi_nonneg hnpos.le]
        · rw [div_le_div_iff₀ hnpos two_pos]
          have : (2 : ℝ) ≤ n := by exact_mod_cast (by omega : 2 ≤ n)
          nlinarith [Real.pi_pos]
      have hmem' : Real.pi * (m' : ℝ) / n ∈ Set.Icc (-(Real.pi / 2)) (Real.pi / 2) := by
        constructor
        · have hnonneg : 0 ≤ Real.pi * (m' : ℝ) / n := by positivity
          linarith [hnonneg, Real.pi_nonneg]
        · exact hangle_le
      have heqθ := Real.strictMonoOn_sin.injOn hmem' hmem1 hm'eq
      have hm're : (m' : ℝ) = 1 := by
        have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
        field_simp at heqθ
        linarith
      have hm'1 : m' = 1 := by exact_mod_cast hm're
      by_cases hle : m ≤ n - m
      · left
        simpa [m', Nat.min_eq_left hle] using hm'1
      · right
        have hgt : n - m ≤ m := Nat.le_of_lt (Nat.lt_of_not_ge hle)
        have : n - m = 1 := by simpa [m', Nat.min_eq_right hgt] using hm'1
        omega
  · rintro (rfl | hm1)
    · simpa using sin_sq_of_one hn0
    · simpa [hm1] using sin_sq_of_neg_one (by omega) (by omega)

theorem sin_sq_gt_of_not_endpoint (hn : 3 ≤ n) {m : ℕ} (hm : m < n)
    (h0 : m ≠ 0) (h1 : m ≠ 1) (hn1 : m ≠ n - 1) :
    Real.sin (Real.pi / n) ^ 2 < Real.sin (Real.pi * (m : ℝ) / n) ^ 2 := by
  have hn0 : 0 < n := by omega
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn0
  let m' : ℕ := min m (n - m)
  have hm'2 : 2 ≤ m' := by
    have hmpos : 1 ≤ m := Nat.one_le_iff_ne_zero.mpr h0
    have hnmpos : 1 ≤ n - m := Nat.le_sub_of_add_le (by omega)
    by_cases hle : m ≤ n - m
    · have : m' = m := Nat.min_eq_left hle
      have hm2 : 2 ≤ m := by omega
      simpa [m', this] using hm2
    · have hgt : n - m ≤ m := Nat.le_of_lt (Nat.lt_of_not_ge hle)
      have : m' = n - m := Nat.min_eq_right hgt
      have hnm2 : 2 ≤ n - m := by omega
      simpa [m', this] using hnm2
  have hfold := sin_fold hn0 hm
  have h2le : 2 * m' ≤ n := by
    have hleft : m' ≤ m := Nat.min_le_left _ _
    have hright : m' ≤ n - m := Nat.min_le_right _ _
    have hsum : m + (n - m) = n := Nat.add_sub_of_le (Nat.le_of_lt hm)
    omega
  have hlt_angle : Real.pi / n < Real.pi * (m' : ℝ) / n := by
    rw [div_lt_div_iff_of_pos_right hnpos]
    have hm' : (1 : ℝ) < m' := by exact_mod_cast (by omega : 1 < m')
    nlinarith [Real.pi_pos]
  have hangle_le : Real.pi * (m' : ℝ) / n ≤ Real.pi / 2 := by
    rw [div_le_div_iff₀ hnpos two_pos]
    have hcast : 2 * (m' : ℝ) ≤ n := by exact_mod_cast h2le
    nlinarith [Real.pi_pos]
  have hmem1 : Real.pi / n ∈ Set.Icc (-(Real.pi / 2)) (Real.pi / 2) := by
    constructor
    · linarith [Real.pi_nonneg, div_nonneg Real.pi_nonneg hnpos.le]
    · rw [div_le_div_iff₀ hnpos two_pos]
      have : (2 : ℝ) ≤ n := by exact_mod_cast (by omega : 2 ≤ n)
      nlinarith [Real.pi_pos]
  have hmem' : Real.pi * (m' : ℝ) / n ∈ Set.Icc (-(Real.pi / 2)) (Real.pi / 2) := by
    constructor
    · have hnonneg : 0 ≤ Real.pi * (m' : ℝ) / n := by positivity
      linarith [hnonneg, Real.pi_nonneg]
    · exact hangle_le
  have hsin_lt := Real.strictMonoOn_sin hmem1 hmem' hlt_angle
  have hsin_lt' : Real.sin (Real.pi / n) < Real.sin (Real.pi * (m : ℝ) / n) := by
    simpa [m', hfold] using hsin_lt
  exact (sq_lt_sq₀ (sin_first_pos (by omega)).le
    (Real.sin_nonneg_of_nonneg_of_le_pi (by positivity) (sin_mem_upper hn0 (Nat.le_of_lt hm)).2)).mpr
    hsin_lt'

/-- Every residue is the zero mode, a first harmonic, or strictly above the first sine square. -/
theorem sin_sq_trichotomy (hn : 2 ≤ n) {m : ℕ} (hm : m < n) :
    Real.sin (Real.pi * (m : ℝ) / n) ^ 2 = 0 ∧ m = 0 ∨
      Real.sin (Real.pi * (m : ℝ) / n) ^ 2 = Real.sin (Real.pi / n) ^ 2 ∧
        (m = 1 ∨ m = n - 1) ∨
      Real.sin (Real.pi / n) ^ 2 < Real.sin (Real.pi * (m : ℝ) / n) ^ 2 := by
  by_cases hm0 : m = 0
  · left
    exact ⟨by simp [hm0], hm0⟩
  · by_cases hend : m = 1 ∨ m = n - 1
    · right; left
      rcases hend with rfl | hm1
      · exact ⟨sin_sq_of_one (by omega), Or.inl rfl⟩
      · exact ⟨by simpa [hm1] using sin_sq_of_neg_one (by omega) (by omega), Or.inr hm1⟩
    · right; right
      have hn3 : 3 ≤ n := by
        have hm1 : m ≠ 1 := by
          intro h
          exact hend (Or.inl h)
        have hnm : m ≠ n - 1 := by
          intro h
          exact hend (Or.inr h)
        have hmge : 2 ≤ m := by omega
        omega
      push_neg at hend
      exact sin_sq_gt_of_not_endpoint hn3 hm hm0 hend.1 hend.2

/-! ## Product characters on a finite torus -/

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Product character `x ↦ exp(2 π i ∑_i k_i x_i / n)`. -/
noncomputable def piCycleChar (k x : ι → ZMod n) : ℂ :=
  ∏ i, cycleChar (k i) (x i)

theorem piCycleChar_zero (x : ι → ZMod n) : piCycleChar 0 x = 1 := by
  unfold piCycleChar
  simp [cycleChar_zero_left]

theorem piCycleChar_add_right (k x y : ι → ZMod n) :
    piCycleChar k (x + y) = piCycleChar k x * piCycleChar k y := by
  unfold piCycleChar
  rw [← Finset.prod_mul_distrib]
  refine Finset.prod_congr rfl fun i _ => ?_
  simp [cycleChar_add_right]

theorem piCycleChar_add_left (k₁ k₂ x : ι → ZMod n) :
    piCycleChar (k₁ + k₂) x = piCycleChar k₁ x * piCycleChar k₂ x := by
  unfold piCycleChar
  rw [← Finset.prod_mul_distrib]
  refine Finset.prod_congr rfl fun i _ => ?_
  simp [Pi.add_apply, cycleChar_add_left]

theorem piCycleChar_comm (k x : ι → ZMod n) : piCycleChar k x = piCycleChar x k := by
  unfold piCycleChar
  refine Finset.prod_congr rfl fun i _ => ?_
  simp [cycleChar, mul_comm]

theorem piCycleChar_conj (k x : ι → ZMod n) :
    conj (piCycleChar k x) = piCycleChar (-k) x := by
  unfold piCycleChar
  rw [map_prod]
  refine Finset.prod_congr rfl fun i _ => ?_
  simpa [Pi.neg_apply] using cycleChar_conj (k i) (x i)

theorem sum_piCycleChar (k : ι → ZMod n) :
    ∑ x : ι → ZMod n, piCycleChar k x =
      if k = 0 then (n : ℂ) ^ Fintype.card ι else 0 := by
  classical
  have hsum := Finset.sum_prod_piFinset (s := (Finset.univ : Finset (ZMod n)))
    (g := fun i j => cycleChar (k i) j)
  simp only [Fintype.piFinset_univ] at hsum
  have hrewrite : ∑ x : ι → ZMod n, piCycleChar k x =
      ∏ i, ∑ j : ZMod n, cycleChar (k i) j := by
    simpa [piCycleChar] using hsum
  rw [hrewrite]
  simp_rw [sum_cycleChar_eq]
  by_cases hk : k = 0
  · simp [hk, Finset.prod_const, Finset.card_univ]
  · have hex : ∃ i, k i ≠ 0 := by
      contrapose! hk
      funext i
      exact hk i
    obtain ⟨i, hi⟩ := hex
    have hprod : ∏ t, (if k t = 0 then (n : ℂ) else 0) = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (by simp [hi])
    simpa [hk] using hprod

theorem sum_piCycleChar_of_site (z : ι → ZMod n) :
    ∑ k : ι → ZMod n, piCycleChar k z =
      if z = 0 then (n : ℂ) ^ Fintype.card ι else 0 := by
  simpa [piCycleChar_comm] using sum_piCycleChar z

/-- Fourier coefficient `∑_y f(y) conj(χ_k(y))`. -/
noncomputable def fourierCoeff (f : (ι → ZMod n) → ℂ) (k : ι → ZMod n) : ℂ :=
  ∑ y, f y * conj (piCycleChar k y)

theorem piCycleChar_neg_right (k x : ι → ZMod n) :
    piCycleChar k (-x) = piCycleChar (-k) x := by
  unfold piCycleChar
  refine Finset.prod_congr rfl fun i _ => ?_
  have hmul : (k i) * (-x i) = (-k i) * x i := by ring
  simp [cycleChar, Pi.neg_apply, hmul]

theorem sum_conj_shift (x y : ι → ZMod n) :
    ∑ k : ι → ZMod n, conj (piCycleChar k y) * piCycleChar k x =
      if y = x then (n : ℂ) ^ Fintype.card ι else 0 := by
  have hstep : ∀ k, conj (piCycleChar k y) * piCycleChar k x = piCycleChar k (x - y) := by
    intro k
    calc
      conj (piCycleChar k y) * piCycleChar k x
          = piCycleChar (-k) y * piCycleChar k x := by rw [piCycleChar_conj]
      _ = piCycleChar k (-y) * piCycleChar k x := by rw [piCycleChar_neg_right]
      _ = piCycleChar k x * piCycleChar k (-y) := by ring
      _ = piCycleChar k (x + -y) := by rw [← piCycleChar_add_right]
      _ = piCycleChar k (x - y) := by rw [sub_eq_add_neg]
  calc
    ∑ k, conj (piCycleChar k y) * piCycleChar k x
        = ∑ k, piCycleChar k (x - y) := by
          refine Finset.sum_congr rfl fun k _ => hstep k
    _ = ∑ k, piCycleChar (x - y) k := by
          refine Finset.sum_congr rfl fun k _ => piCycleChar_comm k (x - y)
    _ = if x - y = 0 then (n : ℂ) ^ Fintype.card ι else 0 := sum_piCycleChar (x - y)
    _ = if y = x then (n : ℂ) ^ Fintype.card ι else 0 := by
          by_cases hxy : y = x
          · simp [hxy]
          · have hsub : x - y ≠ 0 := by
              intro hzero
              exact hxy (eq_comm.mp (sub_eq_zero.mp hzero))
            simp [hxy, hsub]

theorem fourier_inversion (f : (ι → ZMod n) → ℂ) (x : ι → ZMod n) :
    (n : ℂ) ^ Fintype.card ι * f x =
      ∑ k, fourierCoeff f k * piCycleChar k x := by
  classical
  symm
  calc
    ∑ k, fourierCoeff f k * piCycleChar k x
        = ∑ k, ∑ y, f y * conj (piCycleChar k y) * piCycleChar k x := by
          simp only [fourierCoeff, Finset.sum_mul]
    _ = ∑ y, ∑ k, f y * conj (piCycleChar k y) * piCycleChar k x := Finset.sum_comm
    _ = ∑ y, f y * ∑ k, conj (piCycleChar k y) * piCycleChar k x := by
          refine Finset.sum_congr rfl fun y _ => ?_
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun k _ => ?_
          ring
    _ = f x * (n : ℂ) ^ Fintype.card ι := by
          simp_rw [sum_conj_shift]
          rw [Finset.sum_eq_single x]
          · simp
          · intro y _ hy
            simp [hy]
          · simp
    _ = (n : ℂ) ^ Fintype.card ι * f x := by ring

/-- A product character is an eigenvector of one coordinate's second difference. -/
theorem piCycleChar_coordinate_difference (k : ι → ZMod n) (i : ι) (x : ι → ZMod n) :
    (n : ℂ) ^ 2 * (2 * piCycleChar k x -
        piCycleChar k (Function.update x i (x i + 1)) -
        piCycleChar k (Function.update x i (x i - 1))) =
      Complex.ofReal (4 * (n : ℝ) ^ 2 *
          Real.sin (Real.pi * ((k i).val : ℝ) / n) ^ 2) * piCycleChar k x := by
  classical
  have hP : piCycleChar k x =
      cycleChar (k i) (x i) *
        ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j) := by
    simpa [piCycleChar] using (Finset.mul_prod_erase Finset.univ
      (fun j => cycleChar (k j) (x j)) (Finset.mem_univ i)).symm
  have hplus : piCycleChar k (Function.update x i (x i + 1)) =
      cycleChar (k i) (x i + 1) *
        ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j) := by
    have hprod : ∏ j, cycleChar (k j) (Function.update x i (x i + 1) j) =
        cycleChar (k i) (x i + 1) *
          ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (Function.update x i (x i + 1) j) := by
      simpa using (Finset.mul_prod_erase Finset.univ
        (fun j => cycleChar (k j) (Function.update x i (x i + 1) j)) (Finset.mem_univ i)).symm
    have herase : ∏ j ∈ Finset.univ.erase i,
        cycleChar (k j) (Function.update x i (x i + 1) j) =
        ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j) := by
      refine Finset.prod_congr rfl fun j hj => ?_
      have hne : j ≠ i := by
        simpa using (Finset.mem_erase.mp hj).1
      simp [Function.update_of_ne hne]
    simpa [piCycleChar, herase] using hprod
  have hminus : piCycleChar k (Function.update x i (x i - 1)) =
      cycleChar (k i) (x i - 1) *
        ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j) := by
    have hprod : ∏ j, cycleChar (k j) (Function.update x i (x i - 1) j) =
        cycleChar (k i) (x i - 1) *
          ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (Function.update x i (x i - 1) j) := by
      simpa using (Finset.mul_prod_erase Finset.univ
        (fun j => cycleChar (k j) (Function.update x i (x i - 1) j)) (Finset.mem_univ i)).symm
    have herase : ∏ j ∈ Finset.univ.erase i,
        cycleChar (k j) (Function.update x i (x i - 1) j) =
        ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j) := by
      refine Finset.prod_congr rfl fun j hj => ?_
      have hne : j ≠ i := by
        simpa using (Finset.mem_erase.mp hj).1
      simp [Function.update_of_ne hne]
    simpa [piCycleChar, herase] using hprod
  set P := ∏ j ∈ Finset.univ.erase i, cycleChar (k j) (x j)
  have hplus' : cycleChar (k i) (x i + 1) = cycleChar (k i) (x i) * cycleChar (k i) 1 := by
    simpa using cycleChar_add_right (k i) (x i) 1
  have hminus' : cycleChar (k i) (x i - 1) = cycleChar (k i) (x i) * (cycleChar (k i) 1)⁻¹ := by
    have hstep : cycleChar (k i) (x i - 1) * cycleChar (k i) 1 = cycleChar (k i) (x i) := by
      simpa [sub_add_cancel] using (cycleChar_add_right (k i) (x i - 1) 1).symm
    exact (eq_mul_inv_iff_mul_eq₀ (cycleChar_ne_zero (k i) 1)).2 hstep
  have hfactor :
      2 * piCycleChar k x - piCycleChar k (Function.update x i (x i + 1)) -
          piCycleChar k (Function.update x i (x i - 1)) =
        piCycleChar k x * (2 - cycleChar (k i) 1 - (cycleChar (k i) 1)⁻¹) := by
    rw [hP, hplus, hminus, hplus', hminus']
    ring
  rw [hfactor, two_sub_char_eq_sin_sq]
  set s : ℝ := 4 * Real.sin (Real.pi * ((k i).val : ℝ) / n) ^ 2
  have hn : ((n : ℂ) ^ 2) = ↑((n : ℝ) ^ 2) := by
    push_cast
    ring
  have hs : (n : ℝ) ^ 2 * s =
      4 * (n : ℝ) ^ 2 * Real.sin (Real.pi * ((k i).val : ℝ) / n) ^ 2 := by
    simp [s]
    ring
  calc
    (n : ℂ) ^ 2 * (piCycleChar k x * (s : ℂ))
        = ↑((n : ℝ) ^ 2) * (piCycleChar k x * (s : ℂ)) := by rw [hn]
    _ = (↑((n : ℝ) ^ 2) * (s : ℂ)) * piCycleChar k x := by ring
    _ = ↑((n : ℝ) ^ 2 * s) * piCycleChar k x := by rw [← Complex.ofReal_mul]
    _ = Complex.ofReal (4 * (n : ℝ) ^ 2 *
          Real.sin (Real.pi * ((k i).val : ℝ) / n) ^ 2) * piCycleChar k x := by
          rw [hs]

/-- Real and imaginary parts of one conjugate pair are the cosine and sine modes. -/
theorem conjugate_pair_as_cos_sin (c : ℂ) (j : ZMod n) :
    c * cycleChar 1 j + conj c * cycleChar (-1) j =
      ↑(2 * c.re * cycleCos 1 j - 2 * c.im * cycleSin 1 j) := by
  have hneg : cycleChar (-1) j = conj (cycleChar 1 j) := by
    simpa using (cycleChar_conj (1 : ZMod n) j).symm
  rw [hneg, ← Complex.re_add_im c]
  have hz : cycleChar 1 j = ↑(cycleCos 1 j) + ↑(cycleSin 1 j) * I := by
    rw [cycleChar_eq_exp, cycleCos_eq, cycleSin_eq]
    have hθ : (2 * Real.pi * (((1 : ZMod n) * j).val : ℝ) / n) =
        2 * Real.pi * ((1 * j).val : ℝ) / n := rfl
    simpa [hθ, mul_comm] using Complex.exp_ofReal_mul_I
      (2 * Real.pi * (((1 : ZMod n) * j).val : ℝ) / n)
  rw [hz]
  apply Complex.ext <;>
    simp only [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im, Complex.conj_re,
      Complex.conj_im, Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im] <;>
    ring_nf

end D0.Geometry.FiniteCycleFourier
