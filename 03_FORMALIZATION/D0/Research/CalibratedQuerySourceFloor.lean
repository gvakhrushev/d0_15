import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Sharp calibrated QUERY-source floor

This module formalizes the exact real inequality isolated by the scoped
current-head checker in Draft #334, commit
`1dce9b709109c3fc2921c97ff75a31b3bcb09d6c`. For
`0 < α ≤ 4`, `0 < γ ≤ 1`, `0 < P < 1/2` and positive volume `Ω`, the
squared calibrated QUERY-source ratio is at least
`4 Ω² P (1-P)`. The bound is attained at `α=4`, `γ=1`.
With uniform positive lower bounds on `P` and `Ω`, a finite positive-weight
average of these block ratios has the corresponding `η*` lower bound.
The module also proves the scalar readiness-gain cancellation reported in
§7dk of the current #334 source: a `γ`-scaled source and its true adjusted
gain retain the original normalized coefficient.

These are scalar calibration theorems. They do not prove that the parameters
are selected by D0, identify a physical variation norm, admit a native
programme, prove the operator-to-QUERY source map, or establish GR closure.
-/

namespace D0.Research

/-- Squared calibrated QUERY-source to field-calibration ratio from #334. -/
noncomputable def calibratedQuerySourceRatioSq (α γ P Ω : ℝ) : ℝ :=
  let x := γ * P
  16 * Ω ^ 2 * (1 - α * x * (1 - x)) * P * (1 - x) /
    (α * γ * (1 - 2 * x) ^ 2)

/-- The squared uniform source floor for fixed probability and volume. -/
noncomputable def calibratedQuerySourceFloorSq (P Ω : ℝ) : ℝ :=
  4 * Ω ^ 2 * P * (1 - P)

/-- The nonnegative calibrated QUERY-source to field-calibration ratio. -/
noncomputable def calibratedQuerySourceRatio (α γ P Ω : ℝ) : ℝ :=
  Real.sqrt (calibratedQuerySourceRatioSq α γ P Ω)

/-- The calibrated QUERY-source ratio obeys the sharp probability floor. -/
theorem calibratedQuerySourceRatioSq_ge_floor
    (α γ P Ω : ℝ)
    (hα0 : 0 < α) (hα4 : α ≤ 4)
    (hγ0 : 0 < γ) (hγ1 : γ ≤ 1)
    (hP0 : 0 < P) (hPhalf : P < 1 / 2)
    (hΩ0 : 0 < Ω) :
    calibratedQuerySourceFloorSq P Ω ≤
      calibratedQuerySourceRatioSq α γ P Ω := by
  let x := γ * P
  let y := 1 - 2 * x
  let c := 1 - α * x * (1 - x)
  let q₁ := c / y ^ 2
  let q₂ := 4 / (α * γ)
  let q₃ := (1 - x) / (1 - P)
  have hx0 : 0 < x := by
    dsimp [x]
    positivity
  have hxP : x ≤ P := by
    dsimp [x]
    calc
      γ * P ≤ 1 * P := mul_le_mul_of_nonneg_right hγ1 hP0.le
      _ = P := by ring
  have hxhalf : x < 1 / 2 := by linarith
  have hy0 : 0 < y := by
    dsimp [y]
    linarith
  have hOneMinusX : 0 < 1 - x := by linarith
  have hOneMinusP : 0 < 1 - P := by linarith [hPhalf]
  have hαγ0 : 0 < α * γ := mul_pos hα0 hγ0
  have hαγ4 : α * γ ≤ 4 := by
    calc
      α * γ ≤ 4 * γ := mul_le_mul_of_nonneg_right hα4 hγ0.le
      _ ≤ 4 := by nlinarith [hγ1]
  have hCornerIdentity :
      c - y ^ 2 = (4 - α) * x * (1 - x) := by
    dsimp [c, y]
    ring
  have hCorner : y ^ 2 ≤ c := by
    have hRemainder : 0 ≤ (4 - α) * x * (1 - x) :=
      mul_nonneg (mul_nonneg (by linarith [hα4]) hx0.le) hOneMinusX.le
    linarith [hCornerIdentity]
  have hq₁ : 1 ≤ q₁ := by
    dsimp [q₁]
    rw [le_div_iff₀ (sq_pos_of_pos hy0)]
    nlinarith [hCorner]
  have hq₂ : 1 ≤ q₂ := by
    dsimp [q₂]
    rw [le_div_iff₀ hαγ0]
    linarith [hαγ4]
  have hq₃ : 1 ≤ q₃ := by
    dsimp [q₃]
    rw [le_div_iff₀ hOneMinusP]
    linarith [hxP]
  have hq₁₂ : 1 ≤ q₁ * q₂ := by
    have hq₁nonneg : 0 ≤ q₁ - 1 := by linarith [hq₁]
    have hq₂nonneg : 0 ≤ q₂ - 1 := by linarith [hq₂]
    nlinarith [mul_nonneg hq₁nonneg hq₂nonneg]
  have hq : 1 ≤ (q₁ * q₂) * q₃ := by
    have hq₁₂nonneg : 0 ≤ q₁ * q₂ - 1 := by linarith [hq₁₂]
    have hq₃nonneg : 0 ≤ q₃ - 1 := by linarith [hq₃]
    nlinarith [mul_nonneg hq₁₂nonneg hq₃nonneg]
  have hFloor0 : 0 < calibratedQuerySourceFloorSq P Ω := by
    dsimp [calibratedQuerySourceFloorSq]
    positivity
  have hFactor :
      calibratedQuerySourceFloorSq P Ω * ((q₁ * q₂) * q₃) =
        calibratedQuerySourceRatioSq α γ P Ω := by
    dsimp [calibratedQuerySourceFloorSq, calibratedQuerySourceRatioSq,
      q₁, q₂, q₃, x, y, c]
    field_simp [ne_of_gt hαγ0, ne_of_gt (sq_pos_of_pos hy0),
      ne_of_gt hOneMinusP]
    ring_nf
  calc
    calibratedQuerySourceFloorSq P Ω =
        calibratedQuerySourceFloorSq P Ω * 1 := by ring
    _ ≤ calibratedQuerySourceFloorSq P Ω * ((q₁ * q₂) * q₃) :=
      mul_le_mul_of_nonneg_left hq hFloor0.le
    _ = calibratedQuerySourceRatioSq α γ P Ω := hFactor

/-- Equality in the floor is attained at the sharp corner `α=4`, `γ=1`. -/
theorem calibratedQuerySourceRatioSq_eq_floor_at_sharp_corner
    (P Ω : ℝ) (hPhalf : P < 1 / 2) :
    calibratedQuerySourceRatioSq 4 1 P Ω = calibratedQuerySourceFloorSq P Ω := by
  have hypos : 0 < 1 - 2 * P := by linarith
  have hden : 4 * (1 - 2 * P) ^ 2 ≠ 0 := by positivity
  dsimp [calibratedQuerySourceRatioSq, calibratedQuerySourceFloorSq]
  simp only [one_mul]
  rw [show 1 - 4 * P * (1 - P) = (1 - 2 * P) ^ 2 by ring]
  field_simp [hden]
  ring

/-- A positive lower bound on block probability and volume gives the common
unsquared source floor `2 Ω₀ sqrt(b (1-b))`. -/
theorem calibratedQuerySourceRatio_ge_uniform_floor
    (α γ P Ω Ω₀ b : ℝ)
    (hα0 : 0 < α) (hα4 : α ≤ 4)
    (hγ0 : 0 < γ) (hγ1 : γ ≤ 1)
    (hP0 : 0 < P) (hPhalf : P < 1 / 2)
    (hΩ0 : 0 < Ω) (hΩlower0 : 0 < Ω₀) (hΩlower : Ω₀ ≤ Ω)
    (hb0 : 0 < b) (hbP : b ≤ P) :
    2 * Ω₀ * Real.sqrt (b * (1 - b)) ≤
      calibratedQuerySourceRatio α γ P Ω := by
  have hbh : b < 1 / 2 := lt_of_le_of_lt hbP hPhalf
  have hbOne : 0 < 1 - b := by linarith
  have hPOne : 0 < 1 - P := by linarith
  have hprod : b * (1 - b) ≤ P * (1 - P) := by
    have hleft : 0 ≤ P - b := sub_nonneg.mpr hbP
    have hright : 0 ≤ 1 - P - b := by linarith [hPhalf, hbP]
    nlinarith [mul_nonneg hleft hright]
  have hbase :
      4 * Ω₀ ^ 2 * (b * (1 - b)) ≤ 4 * Ω ^ 2 * (P * (1 - P)) := by
    have hvol : Ω₀ ^ 2 ≤ Ω ^ 2 := by nlinarith [hΩlower, hΩlower0]
    have hbprod : 0 ≤ b * (1 - b) := mul_nonneg hb0.le hbOne.le
    have hPprod : 0 ≤ P * (1 - P) := mul_nonneg hP0.le hPOne.le
    calc
      4 * Ω₀ ^ 2 * (b * (1 - b)) ≤
          4 * Ω ^ 2 * (b * (1 - b)) := by nlinarith
      _ ≤ 4 * Ω ^ 2 * (P * (1 - P)) := by nlinarith
  have hratio := calibratedQuerySourceRatioSq_ge_floor
    α γ P Ω hα0 hα4 hγ0 hγ1 hP0 hPhalf hΩ0
  have hsq :
      4 * Ω₀ ^ 2 * (b * (1 - b)) ≤
        calibratedQuerySourceRatioSq α γ P Ω := by
    dsimp [calibratedQuerySourceFloorSq] at hratio
    linarith [hbase, hratio]
  have hsqrt := Real.sqrt_le_sqrt hsq
  have hleft :
      Real.sqrt (4 * Ω₀ ^ 2 * (b * (1 - b))) =
        2 * Ω₀ * Real.sqrt (b * (1 - b)) := by
    calc
      Real.sqrt (4 * Ω₀ ^ 2 * (b * (1 - b))) =
          Real.sqrt ((2 * Ω₀) ^ 2 * (b * (1 - b))) := by congr 1; ring
      _ = Real.sqrt ((2 * Ω₀) ^ 2) * Real.sqrt (b * (1 - b)) := by
          rw [Real.sqrt_mul (sq_nonneg (2 * Ω₀))]
      _ = 2 * Ω₀ * Real.sqrt (b * (1 - b)) := by
          rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity)]
  rw [calibratedQuerySourceRatio, ← hleft]
  exact hsqrt

/-- A finite positive-weight average preserves a common lower bound. -/
theorem weightedAverage_ge_of_pointwise_ge
    {ι : Type*} [Fintype ι]
    (weight value : ι → ℝ) (floor : ℝ)
    (hweightSum : 0 < ∑ i, weight i)
    (hpoint : ∀ i, weight i * floor ≤ weight i * value i) :
    floor ≤ (∑ i, weight i * value i) / (∑ i, weight i) := by
  rw [le_div_iff₀ hweightSum]
  calc
    floor * (∑ i, weight i) = ∑ i, weight i * floor := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ ≤ ∑ i, weight i * value i :=
      Finset.sum_le_sum (fun i hi => hpoint i)

/-- The finite parent-domain QUERY norm has the `η*` floor whenever every
block has `P ≥ b > 0` and `Ω ≥ Ω₀ > 0`. This is a weighted-average theorem on
the declared QUERY chart; it does not assert that the chart is physically
admitted or transfer its norm through an execution map. -/
theorem calibratedQuerySourceWeightedAverage_ge_uniform_floor
    {ι : Type*} [Fintype ι]
    (α γ P Ω weight : ι → ℝ) (Ω₀ b : ℝ)
    (hα0 : ∀ i, 0 < α i) (hα4 : ∀ i, α i ≤ 4)
    (hγ0 : ∀ i, 0 < γ i) (hγ1 : ∀ i, γ i ≤ 1)
    (hP0 : ∀ i, 0 < P i) (hPhalf : ∀ i, P i < 1 / 2)
    (hΩ0 : ∀ i, 0 < Ω i) (hΩlower0 : 0 < Ω₀)
    (hΩlower : ∀ i, Ω₀ ≤ Ω i)
    (hb0 : 0 < b) (hbP : ∀ i, b ≤ P i)
    (hweight0 : ∀ i, 0 < weight i)
    (hweightSum : 0 < ∑ i, weight i) :
    2 * Ω₀ * Real.sqrt (b * (1 - b)) ≤
      (∑ i, weight i * calibratedQuerySourceRatio
        (α i) (γ i) (P i) (Ω i)) / (∑ i, weight i) := by
  apply weightedAverage_ge_of_pointwise_ge weight
    (fun i => calibratedQuerySourceRatio (α i) (γ i) (P i) (Ω i))
    (2 * Ω₀ * Real.sqrt (b * (1 - b))) hweightSum
  intro i
  exact mul_le_mul_of_nonneg_left
    (calibratedQuerySourceRatio_ge_uniform_floor
      (α i) (γ i) (P i) (Ω i) Ω₀ b
      (hα0 i) (hα4 i) (hγ0 i) (hγ1 i) (hP0 i) (hPhalf i)
      (hΩ0 i) (hΩlower0) (hΩlower i) hb0 (hbP i))
    (le_of_lt (hweight0 i))

/-- Cold weight after adding a genuine READY branch of probability `γ`.

This is the scalar centre used by the §7dk readiness construction in #334.
The definition does not encode admission of the flag or its actuators. -/
def readinessColdWeight (γ c : ℝ) : ℝ := 1 - γ + γ * c

/-- Calibrated field gain after the READY branch is included in the cold
normalizer. -/
noncomputable def readinessAdjustedGain (γ c gain : ℝ) : ℝ :=
  (γ * c / readinessColdWeight γ c) * gain

/-- On the positive readiness chart the enlarged cold weight stays positive. -/
theorem readinessColdWeight_pos
    (γ c : ℝ) (hγ0 : 0 < γ) (hγ1 : γ ≤ 1) (hc0 : 0 < c) :
    0 < readinessColdWeight γ c := by
  unfold readinessColdWeight
  nlinarith [mul_pos hγ0 hc0]

/-- The READY cold weight and calibrated gain multiply to the original source
scale `γ c λ`, before the source itself is normalized. -/
theorem readinessColdWeight_mul_adjustedGain
    (γ c gain : ℝ) (hγ0 : 0 < γ) (hγ1 : γ ≤ 1) (hc0 : 0 < c) :
    readinessColdWeight γ c * readinessAdjustedGain γ c gain =
      γ * (c * gain) := by
  have hready_pos := readinessColdWeight_pos γ c hγ0 hγ1 hc0
  have hready : 1 - γ + γ * c ≠ 0 := by
    rw [readinessColdWeight] at hready_pos
    exact ne_of_gt hready_pos
  change (1 - γ + γ * c) *
      ((γ * c / (1 - γ + γ * c)) * gain) = γ * (c * gain)
  field_simp [hready]

/-- Exact scalar cancellation in #334 §7dk(977): when the READY map scales a
source by `γ` and uses `λ_ready=(γ c/c_ready)λ`, its normalized source is the
same as the original `source/(c λ)`. This formalizes only the scalar gain
identity; the operator source map and physical READY admission remain separate
premises. -/
theorem readinessNormalizedSource_eq
    (γ c gain source : ℝ) (hγ0 : 0 < γ) (hγ1 : γ ≤ 1)
    (hc0 : 0 < c) (hgain0 : 0 < gain) :
    (γ * source) /
        (readinessColdWeight γ c * readinessAdjustedGain γ c gain) =
      source / (c * gain) := by
  rw [readinessColdWeight_mul_adjustedGain γ c gain hγ0 hγ1 hc0]
  have hγ : γ ≠ 0 := ne_of_gt hγ0
  have hcl : c * gain ≠ 0 := ne_of_gt (mul_pos hc0 hgain0)
  field_simp [hγ, hcl]

/-- The exact k=4 checker parameters specialize the cold weight to
`1-p^8+p^11`; this is arithmetic bookkeeping, not a device-admission claim. -/
theorem readinessColdWeight_p8_p3 (p : ℝ) :
    readinessColdWeight (p ^ 8) (p ^ 3) = 1 - p ^ 8 + p ^ 11 := by
  unfold readinessColdWeight
  ring

end D0.Research
