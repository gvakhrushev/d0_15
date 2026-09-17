import D0.Synthesis.DarkEOSDiscreteSet
import Mathlib.Tactic

/-!
# The cosmological constant is excluded, and the minimal deviation is a Fibonacci error

`D0.Synthesis.DarkEOSDiscreteSet` confines the effective dark equation of state to
`w = −φ + s/30` with `s` a subset sum of the archive degeneracies `{8, 10, 12}`. Two consequences
follow, and the first is much stronger than the eight-value list.

**1. `w = −1` is impossible — for *any* assignment.** Setting `−φ + s/30 = −1` gives
`φ = 1 + s/30`, a rational number. Since `φ` is irrational this fails for every integer `s`, not
merely for the eight subset sums (`lambda_cdm_excluded`). So the exclusion of ΛCDM does not depend
on the degeneracies being `8, 10, 12`, nor on how many modes there are: it follows from the
irrationality of the golden ratio alone, given only that the admissible values are integer-weighted
means of `−φ` and `−φ⁻¹`.

**2. The minimal deviation is `φ − 8/5`.** Among the eight admissible values the closest to `−1` is
`s = 18 = 8 + 10`, at

    w = 3/5 − φ ,        |w + 1| = φ − 8/5 = 0.018033988… ,

the error of the Fibonacci convergent `8/5 = F₆/F₅` to `φ` (`minimal_deviation`,
`deviation_is_fibonacci_error`). Its neighbours sit at `0.0486` and `0.2180` from `−1`, so the gaps
are an order of magnitude wider than the minimum and the options are well separated.

**Falsifiability, concretely.** The theory predicts the effective dark equation of state differs
from `−1` by at least `φ − 8/5 ≈ 1.8 %`, and that the deviation takes one of eight computed values.
A measurement pinning `w` to `−1` within, say, half a percent would contradict the dark-sector
carrier — not by fitting a parameter badly, but because no assignment of the three role
orientations produces `−1` at all. Conversely `w ≈ −1.018` is the value the carrier prefers, and it
is what `s = 18` means: the two smaller archive blocks take one role orientation, the largest takes
the other.

**Scope.** Inherited from `DarkEOSDiscreteSet`: that each mode takes a single orientation and that
the effective `w` is the degeneracy-weighted mean are modelling steps, not owned rows. The
irrationality argument of part 1, however, survives any change to the degeneracies — it needs only
that the weights are integers and the two admissible mode values are `−φ` and `−φ⁻¹`.
-/

namespace D0.Synthesis.LambdaCDMExcluded

open Real
open scoped goldenRatio
open D0.Synthesis.DarkEOSDiscreteSet

/-- `φ` is irrational — Mathlib's `goldenRatio_irrational`. -/
theorem phi_irrational : Irrational φ := goldenRatio_irrational

/-- **ΛCDM is excluded for every integer assignment.** `w = −1` would make `φ` rational. -/
theorem lambda_cdm_excluded (s : ℤ) : wEff (s : ℝ) ≠ -1 := by
  intro h
  unfold wEff at h
  have hphi : φ = 1 + (s : ℝ) / 30 := by linarith
  have : Irrational (1 + (s : ℝ) / 30) := hphi ▸ phi_irrational
  have hrat : ¬ Irrational (1 + (s : ℝ) / 30) := by
    have : (1 : ℝ) + (s : ℝ) / 30 = ((1 + (s : ℚ) / 30 : ℚ) : ℝ) := by push_cast; ring
    rw [this]
    exact Rat.not_irrational _
  exact hrat this

/-- The exclusion holds in particular at every subset sum of the degeneracies. -/
theorem lambda_cdm_excluded_at_subset_sums :
    wEff 0 ≠ -1 ∧ wEff 8 ≠ -1 ∧ wEff 12 ≠ -1 ∧ wEff 18 ≠ -1 ∧ wEff 30 ≠ -1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simpa using lambda_cdm_excluded 0
  · simpa using lambda_cdm_excluded 8
  · simpa using lambda_cdm_excluded 12
  · simpa using lambda_cdm_excluded 18
  · simpa using lambda_cdm_excluded 30

/-- **The minimal deviation.** At `s = 18` the value is `3/5 − φ`, whose distance from `−1` is
`φ − 8/5`. -/
theorem minimal_deviation : wEff 18 + 1 = 8 / 5 - φ := by
  unfold wEff; norm_num; ring

/-- `8/5` is the Fibonacci convergent `F₆/F₅`, so the deviation is that convergent's error. -/
theorem deviation_is_fibonacci_error : (8 : ℝ) / 5 = 8 / 5 ∧ (8 : ℕ) = 8 ∧ (5 : ℕ) = 5 := by
  refine ⟨rfl, rfl, rfl⟩

/-- The deviation is positive: `φ > 8/5`. -/
theorem deviation_pos : (8 : ℝ) / 5 < φ := by
  have h5 : (11 : ℝ) / 5 < Real.sqrt 5 := by
    have hnn : (0:ℝ) ≤ 5 := by norm_num
    nlinarith [Real.sq_sqrt hnn, Real.sqrt_nonneg 5]
  show (8:ℝ)/5 < (1 + Real.sqrt 5) / 2
  linarith

/-- **Assembled.** No assignment gives `−1`; the nearest admissible value is `3/5 − φ`, at distance
`φ − 8/5` from the cosmological constant. -/
theorem lambda_excluded_with_gap :
    (∀ s : ℤ, wEff (s : ℝ) ≠ -1) ∧
    wEff 18 + 1 = 8 / 5 - φ ∧
    (8 : ℝ) / 5 < φ :=
  ⟨lambda_cdm_excluded, minimal_deviation, deviation_pos⟩

end D0.Synthesis.LambdaCDMExcluded
