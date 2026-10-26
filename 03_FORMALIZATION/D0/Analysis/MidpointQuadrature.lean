import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Tactic

namespace D0.Analysis

noncomputable section

private theorem taylorWithinEval_two_eq_of_uniqueDiff
    (f : ℝ → ℝ) (s : Set ℝ) (m y : ℝ)
    (hs : UniqueDiffOn ℝ s) (hm : m ∈ s) (hf : ContDiff ℝ 3 f) :
    taylorWithinEval f 2 s m y =
      f m + (y - m) * deriv f m + ((y - m) ^ 2 / 2) * iteratedDeriv 2 f m := by
  have h1 : iteratedDerivWithin 1 f s m = deriv f m := by
    rw [iteratedDerivWithin_eq_iteratedDeriv hs
      ((hf.contDiffAt (x := m)).of_le (by norm_num)) hm,
      iteratedDeriv_one]
  have h2 : iteratedDerivWithin 2 f s m = iteratedDeriv 2 f m := by
    rw [iteratedDerivWithin_eq_iteratedDeriv hs
      ((hf.contDiffAt (x := m)).of_le (by norm_num)) hm]
  have hFirst : taylorWithinEval f 1 s m y =
      f m + (y - m) * deriv f m := by
    rw [taylorWithinEval_succ]
    simp [taylor_within_zero_eval, h1, Nat.factorial]
  have hcoeff : (((((1 : ℕ) : ℝ) + 1) * ((Nat.factorial 1 : ℕ) : ℝ))⁻¹) =
      (1 : ℝ) / 2 := by norm_num
  rw [taylorWithinEval_succ, hFirst, h2]
  simp only [smul_eq_mul]
  rw [hcoeff]
  ring

private theorem lagrange_remainder_abs_le_midpoint
    (third h M d : ℝ) (h_nonneg : 0 ≤ h)
    (hthird : |third| ≤ M) (hdist : |d| = h / 2) :
    |third * d ^ 3 / 6| ≤ M * h ^ 3 / 48 := by
  rw [abs_div, abs_mul, abs_of_nonneg (by norm_num : 0 ≤ (6 : ℝ)), abs_pow, hdist]
  calc
    |third| * (h / 2) ^ 3 / 6 ≤ M * (h / 2) ^ 3 / 6 := by
      apply div_le_div_of_nonneg_right _ (by norm_num)
      exact mul_le_mul_of_nonneg_right hthird (by positivity)
    _ = M * h ^ 3 / 48 := by ring

/--
For a scalar `C^3` function, the midpoint increment defect on one cell is
bounded by `M * h^3 / 24` when the third derivative is bounded by `M` there.
Taylor expansion at the midpoint cancels the shared quadratic term; the two
endpoint Lagrange remainders each contribute at most `M * h^3 / 48`.
-/
theorem midpointQuadrature_error_abs_le_of_thirdDerivative_bound
    (f : ℝ → ℝ) (x h M : ℝ) (h_nonneg : 0 ≤ h)
    (hf : ContDiff ℝ 3 f)
    (hthird : ∀ y ∈ Set.Icc x (x + h), |iteratedDeriv 3 f y| ≤ M) :
    |h * deriv f (x + h / 2) - (f (x + h) - f x)| ≤ M * h ^ 3 / 24 := by
  by_cases hh : h = 0
  · subst h
    simp
  · have hpos : 0 < h := lt_of_le_of_ne h_nonneg (Ne.symm hh)
    let m : ℝ := x + h / 2
    let sRight : Set ℝ := Set.uIcc m (x + h)
    let sLeft : Set ℝ := Set.uIcc m x
    have hmLeft : x < m := by dsimp [m]; linarith
    have hmRight : m < x + h := by dsimp [m]; linarith
    have hmidRight : x + h - m = h / 2 := by dsimp [m]; ring
    have hmidLeft : x - m = -(h / 2) := by dsimp [m]; ring
    have hsRight : UniqueDiffOn ℝ sRight := by
      dsimp [sRight]
      rw [Set.uIcc_of_lt hmRight]
      exact uniqueDiffOn_Icc hmRight
    have hsLeft : UniqueDiffOn ℝ sLeft := by
      dsimp [sLeft]
      rw [Set.uIcc_of_gt hmLeft]
      exact uniqueDiffOn_Icc hmLeft
    obtain ⟨yRight, hyRight, hTaylorRight⟩ :=
      taylor_mean_remainder_lagrange_iteratedDeriv
        (f := f) (x := x + h) (x₀ := m) (n := 2)
        (by dsimp [m]; linarith) (hf.contDiffOn)
    obtain ⟨yLeft, hyLeft, hTaylorLeft⟩ :=
      taylor_mean_remainder_lagrange_iteratedDeriv
        (f := f) (x := x) (x₀ := m) (n := 2)
        (by dsimp [m]; linarith) (hf.contDiffOn)
    have hTaylorPolyRight :=
      taylorWithinEval_two_eq_of_uniqueDiff f sRight m (x + h)
        hsRight (by simp [sRight]) hf
    have hTaylorPolyLeft :=
      taylorWithinEval_two_eq_of_uniqueDiff f sLeft m x
        hsLeft (by simp [sLeft]) hf
    let pRight : ℝ :=
      f m + (x + h - m) * deriv f m +
        ((x + h - m) ^ 2 / 2) * iteratedDeriv 2 f m
    let pLeft : ℝ :=
      f m + (x - m) * deriv f m +
        ((x - m) ^ 2 / 2) * iteratedDeriv 2 f m
    have hTaylorRight' : f (x + h) - pRight =
        iteratedDeriv 3 f yRight * (h / 2) ^ 3 / 6 := by
      rw [hTaylorPolyRight, hmidRight] at hTaylorRight
      norm_num at hTaylorRight
      simpa [pRight, hmidRight] using hTaylorRight
    have hTaylorLeft' : f x - pLeft =
        iteratedDeriv 3 f yLeft * (-(h / 2)) ^ 3 / 6 := by
      rw [hTaylorPolyLeft, hmidLeft] at hTaylorLeft
      norm_num at hTaylorLeft
      simpa [pLeft, hmidLeft] using hTaylorLeft
    have hyRightCell : yRight ∈ Set.Icc x (x + h) := by
      rw [Set.uIoo_of_lt hmRight] at hyRight
      rcases Set.mem_Ioo.mp hyRight with ⟨hylo, hyhi⟩
      exact ⟨le_trans (le_of_lt hmLeft) (le_of_lt hylo), le_of_lt hyhi⟩
    have hyLeftCell : yLeft ∈ Set.Icc x (x + h) := by
      rw [Set.uIoo_of_gt hmLeft] at hyLeft
      rcases Set.mem_Ioo.mp hyLeft with ⟨hylo, hyhi⟩
      exact ⟨le_of_lt hylo, le_trans (le_of_lt hyhi) (le_of_lt hmRight)⟩
    have hRightBound : |f (x + h) - pRight| ≤ M * h ^ 3 / 48 := by
      rw [hTaylorRight']
      exact lagrange_remainder_abs_le_midpoint _ h M (h / 2) h_nonneg
        (hthird yRight hyRightCell) (by rw [abs_of_nonneg (by positivity)])
    have hLeftBound : |f x - pLeft| ≤ M * h ^ 3 / 48 := by
      rw [hTaylorLeft']
      exact lagrange_remainder_abs_le_midpoint _ h M (-(h / 2)) h_nonneg
        (hthird yLeft hyLeftCell) (by rw [abs_neg, abs_of_nonneg (by positivity)])
    have hpolyDiff : pRight - pLeft = h * deriv f m := by
      dsimp [pRight, pLeft]
      rw [hmidRight, hmidLeft]
      ring
    have hDefect : h * deriv f m - (f (x + h) - f x) =
        (f x - pLeft) - (f (x + h) - pRight) := by
      rw [← hpolyDiff]
      ring
    calc
      |h * deriv f (x + h / 2) - (f (x + h) - f x)| =
          |(f x - pLeft) - (f (x + h) - pRight)| := by
            simpa [m] using congrArg abs hDefect
      _ ≤ |f x - pLeft| + |f (x + h) - pRight| := abs_sub _ _
      _ ≤ M * h ^ 3 / 48 + M * h ^ 3 / 48 := add_le_add hLeftBound hRightBound
      _ = M * h ^ 3 / 24 := by ring

end

end D0.Analysis
