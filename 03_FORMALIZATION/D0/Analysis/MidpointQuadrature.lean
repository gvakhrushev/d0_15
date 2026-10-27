import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Tactic

namespace D0.Analysis

open MeasureTheory

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

private theorem taylorWithinEval_two_eq_of_uniqueDiff_vector
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (f : ℝ → F) (s : Set ℝ) (m y : ℝ)
    (hs : UniqueDiffOn ℝ s) (hm : m ∈ s)
    (hfAt : ContDiffAt ℝ 3 f m) :
    taylorWithinEval f 2 s m y =
      f m + (y - m) • deriv f m + ((y - m) ^ 2 / 2) • iteratedDeriv 2 f m := by
  have h1 : iteratedDerivWithin 1 f s m = deriv f m := by
    rw [iteratedDerivWithin_eq_iteratedDeriv hs
      (hfAt.of_le (by norm_num)) hm,
      iteratedDeriv_one]
  have h2 : iteratedDerivWithin 2 f s m = iteratedDeriv 2 f m := by
    rw [iteratedDerivWithin_eq_iteratedDeriv hs
      (hfAt.of_le (by norm_num)) hm]
  have hFirst : taylorWithinEval f 1 s m y = f m + (y - m) • deriv f m := by
    rw [taylorWithinEval_succ]
    simp [taylor_within_zero_eval, h1, Nat.factorial]
  have hcoeff : (((((1 : ℕ) : ℝ) + 1) * ((Nat.factorial 1 : ℕ) : ℝ))⁻¹) =
      (1 : ℝ) / 2 := by norm_num
  rw [taylorWithinEval_succ, hFirst, h2]
  rw [hcoeff]
  module

private theorem intervalIntegral_sq_sub_right (a b : ℝ) :
    (∫ t in a..b, (b - t) ^ 2) = (b - a) ^ 3 / 3 := by
  calc
    (∫ t in a..b, (b - t) ^ 2) = ∫ t in a..b, (t - b) ^ 2 := by
      congr 1
      funext t
      ring
    _ = ∫ t in a - b..b - b, t ^ 2 := by
      exact intervalIntegral.integral_comp_sub_right
        (a := a) (b := b) (f := fun t : ℝ => t ^ 2) b
    _ = (b - a) ^ 3 / 3 := by
      rw [integral_pow]
      ring

private theorem taylor_remainder_norm_le_of_thirdDerivativeWithin_bound
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : ℝ → F) (a b M : ℝ)
    (hf : ContDiffOn ℝ 3 f (Set.uIcc a b))
    (hM : 0 ≤ M)
    (hthird : ∀ t ∈ Set.uIcc a b,
      ‖iteratedDerivWithin 3 f (Set.uIcc a b) t‖ ≤ M) :
    ‖f b - taylorWithinEval f 2 (Set.uIcc a b) a b‖ ≤ M * |b - a| ^ 3 / 6 := by
  have hTaylor := taylor_integral_remainder (f := f) (x := b) (x₀ := a) (n := 2) hf
  have hTaylor' : f b - taylorWithinEval f 2 (Set.uIcc a b) a b =
      ∫ t in a..b, ((b - t) ^ 2 / 2) •
        iteratedDerivWithin 3 f (Set.uIcc a b) t := by
    simpa [Nat.factorial] using hTaylor
  rw [hTaylor']
  let g : ℝ → ℝ := fun t => (M / 2) * (b - t) ^ 2
  have hbound : ∀ t ∈ Set.uIoc a b,
      ‖((b - t) ^ 2 / 2) • iteratedDerivWithin 3 f (Set.uIcc a b) t‖ ≤ g t := by
    intro t ht
    have htIcc : t ∈ Set.uIcc a b := Set.uIoc_subset_uIcc ht
    have hc : 0 ≤ (b - t) ^ 2 / 2 := by positivity
    calc
      ‖((b - t) ^ 2 / 2) • iteratedDerivWithin 3 f (Set.uIcc a b) t‖ =
          ((b - t) ^ 2 / 2) *
            ‖iteratedDerivWithin 3 f (Set.uIcc a b) t‖ := by
              rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg hc]
      _ ≤ ((b - t) ^ 2 / 2) * M := mul_le_mul_of_nonneg_left (hthird t htIcc) hc
      _ = g t := by dsimp [g]; ring
  have hg : IntervalIntegrable g volume a b := by
    dsimp [g]
    apply Continuous.intervalIntegrable
    fun_prop
  have hAE : ∀ᵐ t ∂volume.restrict (Set.uIoc a b),
      ‖((b - t) ^ 2 / 2) • iteratedDerivWithin 3 f (Set.uIcc a b) t‖ ≤ g t := by
    filter_upwards [ae_restrict_mem measurableSet_uIoc] with t ht
    exact hbound t ht
  have hIntegral := intervalIntegral.norm_integral_le_abs_of_norm_le
    (μ := volume) hAE hg
  · have hIntegralValue : (∫ t in a..b, g t) = (M / 2) * ((b - a) ^ 3 / 3) := by
      dsimp [g]
      rw [intervalIntegral.integral_const_mul, intervalIntegral_sq_sub_right]
    calc
      ‖∫ t in a..b,
          ((b - t) ^ 2 / 2) • iteratedDerivWithin 3 f (Set.uIcc a b) t‖ ≤
          |∫ t in a..b, g t| := hIntegral
      _ = |(M / 2) * ((b - a) ^ 3 / 3)| := by rw [hIntegralValue]
      _ = M * |b - a| ^ 3 / 6 := by
        rw [abs_mul, abs_of_nonneg (by positivity : 0 ≤ M / 2), abs_div,
          abs_pow, abs_of_nonneg (by norm_num : 0 ≤ (3 : ℝ))]
        ring

/--
For a complete real normed vector space, the midpoint increment defect is
bounded in the vector norm by the same `M * h^3 / 24` constant as the scalar
estimate, when the norm of the third derivative is bounded by `M`. The proof
uses the vector-valued integral Taylor remainder, so it does not introduce a
dimension-dependent factor by estimating components separately.
-/
theorem midpointQuadrature_error_norm_le_of_thirdDerivative_bound_on_interval
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : ℝ → F) (x h M : ℝ) (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (hC3At : ∀ y ∈ Set.Icc x (x + h), ContDiffAt ℝ 3 f y)
    (hthird : ∀ y ∈ Set.Icc x (x + h), ‖iteratedDeriv 3 f y‖ ≤ M) :
    ‖h • deriv f (x + h / 2) - (f (x + h) - f x)‖ ≤ M * h ^ 3 / 24 := by
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
    have hCellRight : ∀ t ∈ sRight, t ∈ Set.Icc x (x + h) := by
      intro t ht
      dsimp [sRight] at ht
      rw [Set.uIcc_of_lt hmRight] at ht
      exact ⟨le_trans (le_of_lt hmLeft) ht.1, ht.2⟩
    have hCellLeft : ∀ t ∈ sLeft, t ∈ Set.Icc x (x + h) := by
      intro t ht
      dsimp [sLeft] at ht
      rw [Set.uIcc_of_gt hmLeft] at ht
      exact ⟨ht.1, le_trans ht.2 (le_of_lt hmRight)⟩
    have hThirdRight : ∀ t ∈ sRight,
        ‖iteratedDerivWithin 3 f sRight t‖ ≤ M := by
      intro t ht
      rw [iteratedDerivWithin_eq_iteratedDeriv hsRight
        ((hC3At t (hCellRight t ht)).of_le (by norm_num)) ht]
      exact hthird t (hCellRight t ht)
    have hThirdLeft : ∀ t ∈ sLeft,
        ‖iteratedDerivWithin 3 f sLeft t‖ ≤ M := by
      intro t ht
      rw [iteratedDerivWithin_eq_iteratedDeriv hsLeft
        ((hC3At t (hCellLeft t ht)).of_le (by norm_num)) ht]
      exact hthird t (hCellLeft t ht)
    have hC3Right : ContDiffOn ℝ 3 f sRight := by
      intro t ht
      exact (hC3At t (hCellRight t ht)).contDiffWithinAt
    have hC3Left : ContDiffOn ℝ 3 f sLeft := by
      intro t ht
      exact (hC3At t (hCellLeft t ht)).contDiffWithinAt
    let pRight : F := f m + (x + h - m) • deriv f m +
      ((x + h - m) ^ 2 / 2) • iteratedDeriv 2 f m
    let pLeft : F := f m + (x - m) • deriv f m +
      ((x - m) ^ 2 / 2) • iteratedDeriv 2 f m
    have hTaylorPolyRight :=
      taylorWithinEval_two_eq_of_uniqueDiff_vector f sRight m (x + h)
        hsRight (by simp [sRight])
        (hC3At m (by constructor <;> dsimp [m] <;> linarith))
    have hTaylorPolyLeft :=
      taylorWithinEval_two_eq_of_uniqueDiff_vector f sLeft m x
        hsLeft (by simp [sLeft])
        (hC3At m (by constructor <;> dsimp [m] <;> linarith))
    have hRight := taylor_remainder_norm_le_of_thirdDerivativeWithin_bound
      f m (x + h) M hC3Right
      M_nonneg hThirdRight
    have hLeft := taylor_remainder_norm_le_of_thirdDerivativeWithin_bound
      f m x M hC3Left
      M_nonneg hThirdLeft
    have hRight' : ‖f (x + h) -
        taylorWithinEval f 2 sRight m (x + h)‖ ≤ M * |x + h - m| ^ 3 / 6 := hRight
    rw [hTaylorPolyRight] at hRight'
    have hRightBound : ‖f (x + h) - pRight‖ ≤ M * h ^ 3 / 48 := by
      have hRight'' : ‖f (x + h) - pRight‖ ≤ M * |h / 2| ^ 3 / 6 := by
        simpa [pRight, hmidRight] using hRight'
      calc
        ‖f (x + h) - pRight‖ ≤ M * |h / 2| ^ 3 / 6 := hRight''
        _ = M * h ^ 3 / 48 := by
          rw [show |h / 2| = h / 2 by exact abs_of_nonneg (by positivity)]
          ring
    have hLeft' : ‖f x - taylorWithinEval f 2 sLeft m x‖ ≤ M * |x - m| ^ 3 / 6 := hLeft
    rw [hTaylorPolyLeft] at hLeft'
    have hLeftBound : ‖f x - pLeft‖ ≤ M * h ^ 3 / 48 := by
      have habs : |x - m| = h / 2 := by
        rw [hmidLeft, abs_neg]
        exact abs_of_nonneg (by positivity)
      have hLeft'' : ‖f x - pLeft‖ ≤ M * |h / 2| ^ 3 / 6 := by
        simpa [pLeft, hmidLeft, habs] using hLeft'
      calc
        ‖f x - pLeft‖ ≤ M * |h / 2| ^ 3 / 6 := hLeft''
        _ = M * h ^ 3 / 48 := by
          rw [show |h / 2| = h / 2 by exact abs_of_nonneg (by positivity)]
          ring
    have hpolyDiff : pRight - pLeft = h • deriv f m := by
      dsimp [pRight, pLeft]
      rw [hmidRight, hmidLeft]
      module
    have hDefect : h • deriv f m - (f (x + h) - f x) =
        (f x - pLeft) - (f (x + h) - pRight) := by
      rw [← hpolyDiff]
      abel
    calc
      ‖h • deriv f (x + h / 2) - (f (x + h) - f x)‖ =
          ‖(f x - pLeft) - (f (x + h) - pRight)‖ := by
            simpa [m] using congrArg norm hDefect
      _ ≤ ‖f x - pLeft‖ + ‖f (x + h) - pRight‖ := norm_sub_le _ _
      _ ≤ M * h ^ 3 / 48 + M * h ^ 3 / 48 := add_le_add hLeftBound hRightBound
      _ = M * h ^ 3 / 24 := by ring

/-- The global-smoothness API is a compatibility wrapper for the interval-local proof. -/
theorem midpointQuadrature_error_norm_le_of_thirdDerivative_bound
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : ℝ → F) (x h M : ℝ) (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (hf : ContDiff ℝ 3 f)
    (hthird : ∀ y ∈ Set.Icc x (x + h), ‖iteratedDeriv 3 f y‖ ≤ M) :
    ‖h • deriv f (x + h / 2) - (f (x + h) - f x)‖ ≤ M * h ^ 3 / 24 := by
  exact midpointQuadrature_error_norm_le_of_thirdDerivative_bound_on_interval
    f x h M h_nonneg M_nonneg (fun y _ => hf.contDiffAt (x := y)) hthird

/-- A chronological midpoint record in a real normed vector space. -/
def finiteVectorMidpointHistory {F : Type*} [AddCommGroup F] [Module ℝ F]
    (h : ℝ) (rate : ℕ → F) (base : F) : ℕ → F
  | 0 => base
  | n + 1 => finiteVectorMidpointHistory h rate base n + h • rate n

/-- Exact values of a vector field at the mesh points. -/
def sampledVectorExactValues {F : Type*} (f : ℝ → F) (x₀ h : ℝ) : ℕ → F :=
  fun n => f (x₀ + (n : ℝ) * h)

/-- Midpoint derivative rates of a vector field on the mesh. -/
def sampledVectorMidpointRate {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (f : ℝ → F) (x₀ h : ℝ) : ℕ → F :=
  fun n => deriv f (x₀ + (n : ℝ) * h + h / 2)

/-- The vector increment defect at one midpoint step. -/
def finiteVectorMidpointLocalDefect {F : Type*} [AddCommGroup F] [Module ℝ F]
    (h : ℝ) (rate exact : ℕ → F) (n : ℕ) : F :=
  h • rate n - (exact (n + 1) - exact n)

/-- The chronological history error is the sum of its local vector defects. -/
theorem finiteVectorMidpointHistory_error_eq_localDefectSum
    {F : Type*} [AddCommGroup F] [Module ℝ F]
    (h : ℝ) (rate exact : ℕ → F) (n : ℕ) :
    finiteVectorMidpointHistory h rate (exact 0) n - exact n =
      ∑ k ∈ Finset.range n, finiteVectorMidpointLocalDefect h rate exact k := by
  induction n with
  | zero => simp [finiteVectorMidpointHistory, finiteVectorMidpointLocalDefect]
  | succ n ih =>
      calc
        finiteVectorMidpointHistory h rate (exact 0) (n + 1) - exact (n + 1) =
            (finiteVectorMidpointHistory h rate (exact 0) n - exact n) +
              finiteVectorMidpointLocalDefect h rate exact n := by
                simp [finiteVectorMidpointHistory, finiteVectorMidpointLocalDefect]
                abel
        _ = (∑ k ∈ Finset.range n, finiteVectorMidpointLocalDefect h rate exact k) +
              finiteVectorMidpointLocalDefect h rate exact n := by rw [ih]
        _ = ∑ k ∈ Finset.range (n + 1),
              finiteVectorMidpointLocalDefect h rate exact k := by
                rw [Finset.sum_range_succ]

/-- The accumulated vector error is bounded by the count times a uniform local bound. -/
theorem finiteVectorMidpointHistory_error_norm_le_localDefectBound
    {F : Type*} [NormedAddCommGroup F] [Module ℝ F]
    (h C : ℝ) (rate exact : ℕ → F) (N : ℕ)
    (hLocal : ∀ k < N,
      ‖finiteVectorMidpointLocalDefect h rate exact k‖ ≤ C) :
    ∀ n ≤ N,
      ‖finiteVectorMidpointHistory h rate (exact 0) n - exact n‖ ≤ (n : ℝ) * C := by
  intro n
  induction n with
  | zero => intro _; simp [finiteVectorMidpointHistory]
  | succ n ih =>
      intro hn
      have hPrev : n ≤ N := Nat.le_of_succ_le hn
      have hStep : ‖finiteVectorMidpointLocalDefect h rate exact n‖ ≤ C :=
        hLocal n (Nat.lt_of_succ_le hn)
      calc
        ‖finiteVectorMidpointHistory h rate (exact 0) (n + 1) - exact (n + 1)‖ =
            ‖(finiteVectorMidpointHistory h rate (exact 0) n - exact n) +
              finiteVectorMidpointLocalDefect h rate exact n‖ := by
                congr 1
                simp [finiteVectorMidpointHistory, finiteVectorMidpointLocalDefect]
                abel
        _ ≤ ‖finiteVectorMidpointHistory h rate (exact 0) n - exact n‖ +
              ‖finiteVectorMidpointLocalDefect h rate exact n‖ := norm_add_le _ _
        _ ≤ (n : ℝ) * C + C := add_le_add (ih hPrev) hStep
        _ = ((n + 1 : ℕ) : ℝ) * C := by push_cast; ring

/--
The vector-valued midpoint record converges uniformly at its mesh points with
the classical `duration * M * h^2 / 24` bound under a vector third-derivative
bound. The estimate composes local vector defects without a component-count
loss.
-/
theorem sampledVectorMidpointHistory_error_le_refinementBound_on_interval
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : ℝ → F) (x₀ h M duration : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (h_duration : (N : ℝ) * h = duration)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 f t)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 f t‖ ≤ M) :
    ∀ n ≤ N,
      ‖finiteVectorMidpointHistory h (sampledVectorMidpointRate f x₀ h)
          (sampledVectorExactValues f x₀ h 0) n -
        sampledVectorExactValues f x₀ h n‖ ≤ duration * M * h ^ 2 / 24 := by
  have hCellBound : ∀ k < N,
      ‖finiteVectorMidpointLocalDefect h (sampledVectorMidpointRate f x₀ h)
          (sampledVectorExactValues f x₀ h) k‖ ≤ M * h ^ 3 / 24 := by
    intro k hk
    let xₖ : ℝ := x₀ + (k : ℝ) * h
    have hkN : (k : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast Nat.succ_le_of_lt hk
    have hStart : x₀ ≤ xₖ := by
      dsimp [xₖ]
      exact le_add_of_nonneg_right (mul_nonneg (Nat.cast_nonneg k) h_nonneg)
    have hEnd : xₖ + h ≤ x₀ + duration := by
      dsimp [xₖ]
      rw [← h_duration]
      nlinarith [mul_le_mul_of_nonneg_right hkN h_nonneg]
    have hCell : ∀ y ∈ Set.Icc xₖ (xₖ + h), y ∈ Set.Icc x₀ (x₀ + duration) := by
      intro y hy
      exact ⟨le_trans hStart hy.1, le_trans hy.2 hEnd⟩
    have hNextSite : x₀ + ((k : ℝ) + 1) * h = xₖ + h := by
      dsimp [xₖ]
      ring
    have hLocal := midpointQuadrature_error_norm_le_of_thirdDerivative_bound_on_interval
      f xₖ h M h_nonneg M_nonneg (fun y hy => hC3At y (hCell y hy))
      (fun y hy => hThird y (hCell y hy))
    simpa [finiteVectorMidpointLocalDefect, sampledVectorMidpointRate,
      sampledVectorExactValues, xₖ, hNextSite] using hLocal
  have hC : 0 ≤ M * h ^ 3 / 24 := by positivity
  have hCount := finiteVectorMidpointHistory_error_norm_le_localDefectBound
    h (M * h ^ 3 / 24) (sampledVectorMidpointRate f x₀ h)
    (sampledVectorExactValues f x₀ h) N hCellBound
  intro n hn
  have hnN : (n : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hn
  calc
    ‖finiteVectorMidpointHistory h (sampledVectorMidpointRate f x₀ h)
        (sampledVectorExactValues f x₀ h 0) n -
      sampledVectorExactValues f x₀ h n‖ ≤ (n : ℝ) * (M * h ^ 3 / 24) :=
        hCount n hn
    _ ≤ (N : ℝ) * (M * h ^ 3 / 24) :=
      mul_le_mul_of_nonneg_right hnN hC
    _ = duration * M * h ^ 2 / 24 := by rw [← h_duration]; ring

/-- The global-smoothness history API remains as a wrapper over the local theorem. -/
theorem sampledVectorMidpointHistory_error_le_refinementBound
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : ℝ → F) (x₀ h M duration : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (h_duration : (N : ℝ) * h = duration)
    (hf : ContDiff ℝ 3 f)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 f t‖ ≤ M) :
    ∀ n ≤ N,
      ‖finiteVectorMidpointHistory h (sampledVectorMidpointRate f x₀ h)
          (sampledVectorExactValues f x₀ h 0) n -
        sampledVectorExactValues f x₀ h n‖ ≤ duration * M * h ^ 2 / 24 := by
  exact sampledVectorMidpointHistory_error_le_refinementBound_on_interval
    f x₀ h M duration N h_nonneg M_nonneg h_duration
    (fun t _ => hf.contDiffAt (x := t)) hThird

end

end D0.Analysis
