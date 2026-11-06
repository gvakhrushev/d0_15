import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Relative finite spectral log-price bounds

This module formalizes the scalar spectral-sum step of (11) and the
gain/contrast step of (12) in the existing #334 task-faithful source,
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

For nonnegative spectral values, the offset `a > 0` keeps every logarithm
argument positive, including at zero eigenvalues. The proof uses the
logarithm-ratio inequality, retains the actual spectral gain, and never
divides by an eigenvalue. No dimension or least-positive-eigenvalue factor
is introduced. The positive gain needed for a normalized contrast is an
explicit hypothesis and follows from any one positive spectral value.

These are finite scalar spectral lemmas. A matrix determinant/spectral
identity and the order comparison for the actual perturbed Gram operator
must still be supplied by their consumers. No physical task, preparation,
clock, heat contribution, derivative bound, or GR closure is selected here.
-/

noncomputable section

namespace D0.Analysis.RelativeLogDetScaleBound

open scoped BigOperators

variable {ι : Type*} [Fintype ι]

/-- Negative log-determinant written as a finite scalar spectral sum. -/
def finiteSpectralPrice (a : ℝ) (eigenvalue : ι → ℝ) (q : ℝ) : ℝ :=
  -∑ i, Real.log (a + q * eigenvalue i)

/-- The actual gain at the same positive scale as the spectral price. -/
def finiteSpectralGain (a : ℝ) (eigenvalue : ι → ℝ) (q : ℝ) : ℝ :=
  ∑ i, q * eigenvalue i / (a + q * eigenvalue i)

private theorem gainTerm_mono {a x y : ℝ} (ha : 0 < a) (hx : 0 ≤ x)
    (hxy : x ≤ y) : x / (a + x) ≤ y / (a + y) := by
  have hy : 0 ≤ y := hx.trans hxy
  apply (div_le_div_iff₀ (by positivity) (by positivity)).2
  nlinarith [mul_nonneg ha.le (sub_nonneg.mpr hxy)]

private theorem gainTerm_scale_le {a x q L : ℝ} (ha : 0 < a) (hx : 0 ≤ x)
    (hq : 0 < q) (hL : 1 ≤ L) (hqL : q ≤ L) :
    q * x / (a + q * x) ≤ L * (x / (a + x)) := by
  have hqx : 0 ≤ q * x := mul_nonneg hq.le hx
  have hbase : 0 < a + x := by positivity
  have hscaled : 0 < a + q * x := by positivity
  have hw : 0 ≤ x / (a + x) := div_nonneg hx hbase.le
  by_cases hqone : 1 ≤ q
  · have hden : a + x ≤ a + q * x := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hqone) hx]
    have hratio : q * x / (a + q * x) ≤ q * x / (a + x) :=
      (div_le_div_iff₀ hscaled hbase).2 (mul_le_mul_of_nonneg_left hden hqx)
    calc
      q * x / (a + q * x) ≤ q * (x / (a + x)) := by
        simpa only [mul_div_assoc] using hratio
      _ ≤ L * (x / (a + x)) := mul_le_mul_of_nonneg_right hqL hw
  · have hqle : q ≤ 1 := le_of_not_ge hqone
    have hqxle : q * x ≤ x := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hqle) hx]
    calc
      q * x / (a + q * x) ≤ x / (a + x) := gainTerm_mono ha hqx hqxle
      _ ≤ L * (x / (a + x)) := by
        nlinarith [mul_nonneg (sub_nonneg.mpr hL) hw]

private theorem logTerm_sub_le {a x q : ℝ} (ha : 0 < a) (hx : 0 ≤ x)
    (hq : 0 < q) :
    Real.log (a + q * x) - Real.log (a + x) ≤ (q - 1) * (x / (a + x)) := by
  have hbase : 0 < a + x := by positivity
  have hscaled : 0 < a + q * x := by positivity
  have hlog := Real.log_le_sub_one_of_pos (div_pos hscaled hbase)
  rw [Real.log_div (ne_of_gt hscaled) (ne_of_gt hbase)] at hlog
  have hratio : (a + q * x) / (a + x) - 1 = (q - 1) * (x / (a + x)) := by
    field_simp
    ring
  rwa [hratio] at hlog

/-- A single spectral term, uniformly on a multiplicative interval. -/
theorem abs_logTerm_sub_le {a x q L : ℝ} (ha : 0 < a) (hx : 0 ≤ x)
    (hq : 0 < q) (hL : 1 ≤ L) (hqL : q ≤ L) (hinv : q⁻¹ ≤ L) :
    |Real.log (a + q * x) - Real.log (a + x)| ≤ (L - 1) * (x / (a + x)) := by
  have hbase : 0 < a + x := by positivity
  have hw : 0 ≤ x / (a + x) := div_nonneg hx hbase.le
  have hbound : 0 ≤ (L - 1) * (x / (a + x)) :=
    mul_nonneg (sub_nonneg.mpr hL) hw
  apply abs_le.mpr
  constructor
  · by_cases hqone : 1 ≤ q
    · have hden : a + x ≤ a + q * x := by
        nlinarith [mul_nonneg (sub_nonneg.mpr hqone) hx]
      have hlog := Real.log_le_log hbase hden
      linarith
    · have hqle : q ≤ 1 := le_of_not_ge hqone
      have hqx : 0 ≤ q * x := mul_nonneg hq.le hx
      have hqxle : q * x ≤ x := by
        nlinarith [mul_nonneg (sub_nonneg.mpr hqle) hx]
      have hreverse := logTerm_sub_le ha hqx (inv_pos.mpr hq)
      have hcancel : q⁻¹ * (q * x) = x := by
        rw [← mul_assoc, inv_mul_cancel₀ (ne_of_gt hq), one_mul]
      rw [hcancel] at hreverse
      have hweight := gainTerm_mono ha hqx hqxle
      have hinvone : 0 ≤ q⁻¹ - 1 :=
        sub_nonneg.mpr ((one_le_inv₀ hq).2 hqle)
      have hreverse_bound :
          Real.log (a + x) - Real.log (a + q * x) ≤
            (L - 1) * (x / (a + x)) :=
        hreverse.trans ((mul_le_mul_of_nonneg_left hweight hinvone).trans
          (mul_le_mul_of_nonneg_right (sub_le_sub_right hinv 1) hw))
      linarith
  · exact (logTerm_sub_le ha hx hq).trans
      (mul_le_mul_of_nonneg_right (sub_le_sub_right hqL 1) hw)

theorem finiteSpectralGain_nonneg (a : ℝ) (eigenvalue : ι → ℝ) (q : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hq : 0 ≤ q) :
    0 ≤ finiteSpectralGain a eigenvalue q := by
  apply Finset.sum_nonneg
  intro i _
  have hi := hvalue i
  apply div_nonneg (mul_nonneg hq hi)
  positivity

/-- One positive value suffices for nonzero gain; the other values may be zero. -/
theorem finiteSpectralGain_pos (a : ℝ) (eigenvalue : ι → ℝ) (q : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hq : 0 < q)
    (hpositive : ∃ i, 0 < eigenvalue i) :
    0 < finiteSpectralGain a eigenvalue q := by
  apply Finset.sum_pos'
  · intro i _
    have hi := hvalue i
    exact div_nonneg (mul_nonneg hq.le hi) (by positivity)
  · obtain ⟨i, hi⟩ := hpositive
    exact ⟨i, Finset.mem_univ i, div_pos (mul_pos hq hi) (by positivity)⟩

/-- Upper gain comparison at two scales, including singular spectra. -/
theorem finiteSpectralGain_scale_le (a : ℝ) (eigenvalue : ι → ℝ) (q L : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hq : 0 < q)
    (hL : 1 ≤ L) (hqL : q ≤ L) :
    finiteSpectralGain a eigenvalue q ≤ L * finiteSpectralGain a eigenvalue 1 := by
  simp only [finiteSpectralGain, one_mul, Finset.mul_sum]
  exact Finset.sum_le_sum fun i _ => gainTerm_scale_le ha (hvalue i) hq hL hqL

/-- The finite spectral form of (11), using the actual unscaled gain. -/
theorem finiteSpectralPrice_scale_bound (a : ℝ) (eigenvalue : ι → ℝ) (q L : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hq : 0 < q)
    (hL : 1 ≤ L) (hqL : q ≤ L) (hinv : q⁻¹ ≤ L) :
    |finiteSpectralPrice a eigenvalue q - finiteSpectralPrice a eigenvalue 1| ≤
      (L - 1) * finiteSpectralGain a eigenvalue 1 := by
  have hdifference :
      finiteSpectralPrice a eigenvalue q - finiteSpectralPrice a eigenvalue 1 =
        -(∑ i, (Real.log (a + q * eigenvalue i) - Real.log (a + eigenvalue i))) := by
    simp only [finiteSpectralPrice, one_mul, Finset.sum_sub_distrib]
    ring
  rw [hdifference, abs_neg]
  calc
    |∑ i, (Real.log (a + q * eigenvalue i) - Real.log (a + eigenvalue i))| ≤
        ∑ i, |Real.log (a + q * eigenvalue i) - Real.log (a + eigenvalue i)| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, (L - 1) * (eigenvalue i / (a + eigenvalue i)) :=
      Finset.sum_le_sum fun i _ => abs_logTerm_sub_le ha (hvalue i) hq hL hqL hinv
    _ = (L - 1) * finiteSpectralGain a eigenvalue 1 := by
      simp only [finiteSpectralGain, one_mul, Finset.mul_sum]

/-- Logarithmic scale displacement at most `2 η` gives precisely (11)'s factor. -/
theorem finiteSpectralPrice_exp_bound (a : ℝ) (eigenvalue : ι → ℝ) (t η : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hη : 0 ≤ η)
    (ht : |t| ≤ 2 * η) :
    |finiteSpectralPrice a eigenvalue (Real.exp t) - finiteSpectralPrice a eigenvalue 1| ≤
      (Real.exp (2 * η) - 1) * finiteSpectralGain a eigenvalue 1 := by
  apply finiteSpectralPrice_scale_bound a eigenvalue (Real.exp t) (Real.exp (2 * η))
    ha hvalue (Real.exp_pos t)
  · exact Real.one_le_exp_iff.mpr (by positivity)
  · exact Real.exp_le_exp.mpr (abs_le.mp ht).2
  · rw [← Real.exp_neg]
    apply Real.exp_le_exp.mpr
    linarith [(abs_le.mp ht).1]

/-- Gain at a logarithmically displaced endpoint is at most `exp θ` times
the original gain. Only an upper bound on the displacement is needed. -/
theorem finiteSpectralGain_exp_le (a : ℝ) (eigenvalue : ι → ℝ) (t θ : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) (hθ : 0 ≤ θ)
    (ht : t ≤ θ) :
    finiteSpectralGain a eigenvalue (Real.exp t) ≤
      Real.exp θ * finiteSpectralGain a eigenvalue 1 :=
  finiteSpectralGain_scale_le a eigenvalue (Real.exp t) (Real.exp θ)
    ha hvalue (Real.exp_pos t) (Real.one_le_exp_iff.mpr hθ) (Real.exp_le_exp.mpr ht)

/-- The contrast step (12) from two endpoint price errors and their actual
spectral gains. Matrix comparison, heat error, and measurement error are not
premises silently supplied by this scalar statement. -/
theorem finiteSpectralPrice_contrast_bound
    (a : ℝ) (eigenvalue : ι → ℝ) (qPlus qMinus actualPlus actualMinus η θ t Λ : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i)
    (hqPlus : 0 < qPlus) (hqMinus : 0 < qMinus)
    (hη : 0 ≤ η) (hθ : 0 ≤ θ)
    (hqPlusUpper : qPlus ≤ Real.exp θ) (hqMinusUpper : qMinus ≤ Real.exp θ)
    (hgain : 0 < finiteSpectralGain a eigenvalue 1) (ht : t ≠ 0) (hΛ : 0 < Λ)
    (hplus : |actualPlus - finiteSpectralPrice a eigenvalue qPlus| ≤
      (Real.exp (2 * η) - 1) * finiteSpectralGain a eigenvalue qPlus)
    (hminus : |actualMinus - finiteSpectralPrice a eigenvalue qMinus| ≤
      (Real.exp (2 * η) - 1) * finiteSpectralGain a eigenvalue qMinus) :
    |(actualPlus - actualMinus - finiteSpectralPrice a eigenvalue qPlus +
        finiteSpectralPrice a eigenvalue qMinus) /
        (2 * t * (finiteSpectralGain a eigenvalue 1 * Λ))| ≤
      Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * Λ) := by
  let w := finiteSpectralGain a eigenvalue 1
  let E := Real.exp (2 * η) - 1
  let C := Real.exp θ * E
  have hw : 0 < w := hgain
  have hE : 0 ≤ E := sub_nonneg.mpr (Real.one_le_exp_iff.mpr (by positivity))
  have hL : 1 ≤ Real.exp θ := Real.one_le_exp_iff.mpr hθ
  have hpGain := finiteSpectralGain_scale_le a eigenvalue qPlus (Real.exp θ)
    ha hvalue hqPlus hL hqPlusUpper
  have hmGain := finiteSpectralGain_scale_le a eigenvalue qMinus (Real.exp θ)
    ha hvalue hqMinus hL hqMinusUpper
  have hp : |actualPlus - finiteSpectralPrice a eigenvalue qPlus| ≤ C * w := by
    calc
      _ ≤ E * finiteSpectralGain a eigenvalue qPlus := hplus
      _ ≤ E * (Real.exp θ * w) := mul_le_mul_of_nonneg_left hpGain hE
      _ = C * w := by dsimp [C]; ring
  have hm : |actualMinus - finiteSpectralPrice a eigenvalue qMinus| ≤ C * w := by
    calc
      _ ≤ E * finiteSpectralGain a eigenvalue qMinus := hminus
      _ ≤ E * (Real.exp θ * w) := mul_le_mul_of_nonneg_left hmGain hE
      _ = C * w := by dsimp [C]; ring
  have hnum : |actualPlus - actualMinus - finiteSpectralPrice a eigenvalue qPlus +
      finiteSpectralPrice a eigenvalue qMinus| ≤ 2 * C * w := by
    calc
      _ = |(actualPlus - finiteSpectralPrice a eigenvalue qPlus) +
          -(actualMinus - finiteSpectralPrice a eigenvalue qMinus)| := by
        congr 1
        ring
      _ ≤ |actualPlus - finiteSpectralPrice a eigenvalue qPlus| +
          |actualMinus - finiteSpectralPrice a eigenvalue qMinus| := by
        simpa only [abs_neg] using abs_add_le
          (actualPlus - finiteSpectralPrice a eigenvalue qPlus)
          (-(actualMinus - finiteSpectralPrice a eigenvalue qMinus))
      _ ≤ 2 * C * w := by linarith
  have htpos : 0 < |t| := abs_pos.mpr ht
  have hden : 0 < 2 * |t| * (w * Λ) := by positivity
  calc
    _ = |actualPlus - actualMinus - finiteSpectralPrice a eigenvalue qPlus +
          finiteSpectralPrice a eigenvalue qMinus| / (2 * |t| * (w * Λ)) := by
      rw [abs_div]
      simp only [abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2),
        abs_of_pos hw, abs_of_pos hΛ, w]
    _ ≤ (2 * C * w) / (2 * |t| * (w * Λ)) :=
      div_le_div_of_nonneg_right hnum hden.le
    _ = Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * Λ) := by
      dsimp [C, E]
      field_simp

end D0.Analysis.RelativeLogDetScaleBound

end
