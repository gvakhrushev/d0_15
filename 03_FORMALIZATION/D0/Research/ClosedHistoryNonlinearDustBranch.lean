import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Exact algebraic branch of the nonlinear direct-click source

This module formalizes the finite algebraic part of the #334 nonlinear
Einstein-dust intake: the original click polynomial is quadratic in the
curvature variable, and the displayed radical selects its negative root
when the trace coefficients have the stated signs. The exact coefficient
signs and the rational κ enclosure are now proved on the owner's fixed
Golden sector z=y₀=2⁻²⁰. It does not formalize the source-to-field variation,
the LTB solution, or physical admission. Source: PR #334 commit
`c296829fc2e74d673a2a679baa1e10a49524b290`, file
`A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md`, Git blob
`154b341f17adce88594b0b5e9df0d38c0283d288`, Eqs. (15), (25)--(27).
-/

noncomputable section

namespace D0.Research.ClosedHistoryNonlinearDustBranch

/-- The Golden rotation parameter used by the #334 original click. -/
def goldenRotation : ℝ := (Real.sqrt 5 - 1) / 2

/-- The pinned Golden parameter satisfies the quadratic relation used in
the coefficient reduction. -/
theorem goldenRotation_relation : goldenRotation ^ 2 + goldenRotation = 1 := by
  have hsqrt : (Real.sqrt 5) ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  dsimp [goldenRotation]
  nlinarith [hsqrt]

/-- One recurrence step for the integer coefficients of successive Golden
powers. The polynomial relation `p^2 + p = 1` gives `p^(n+2) = p^n -
p^(n+1)`, so every power reduces to a rational-linear expression in `p`. -/
def goldenCoeffStep (a b : ℤ × ℤ) : ℤ × ℤ :=
  (a.1 - b.1, a.2 - b.2)

/-- The first component is the coefficient pair for `p^n`; the second is the
coefficient pair for `p^(n+1)`. -/
def goldenCoeffStates : ℕ → (ℤ × ℤ) × (ℤ × ℤ)
  | 0 => ((0, 1), (1, 0))
  | n + 1 => ((goldenCoeffStates n).2,
      goldenCoeffStep (goldenCoeffStates n).1 (goldenCoeffStates n).2)

/-- Rational-linear form for the `n`th power on the Golden quadratic. -/
def goldenPowerLinear (n : ℕ) (p : ℝ) : ℝ :=
  ((goldenCoeffStates n).1.1 : ℝ) * p + (goldenCoeffStates n).1.2

theorem golden_pow_recurrence {p : ℝ} (hp : p ^ 2 + p = 1) (n : ℕ) :
    p ^ (n + 2) = p ^ n - p ^ (n + 1) := by
  have hp2 : p ^ 2 = 1 - p := by linarith
  calc
    p ^ (n + 2) = p ^ n * p ^ 2 := by rw [pow_add]
    _ = p ^ n * (1 - p) := by rw [hp2]
    _ = p ^ n - p ^ (n + 1) := by rw [pow_succ]; ring

/-- Every Golden power reduces by an exact integer recurrence. This keeps
high-degree coefficient calculations in Lean within the quadratic number
field instead of treating powers of the parameter as independent inputs. -/
theorem golden_power_linear {p : ℝ} (hp : p ^ 2 + p = 1) (n : ℕ) :
    p ^ n = goldenPowerLinear n p := by
  refine Nat.twoStepInduction ?_ ?_ ?_ n
  · norm_num [goldenPowerLinear, goldenCoeffStates]
  · norm_num [goldenPowerLinear, goldenCoeffStates]
  · intro k hk hk1
    rw [golden_pow_recurrence hp k, hk, hk1]
    simp [goldenPowerLinear, goldenCoeffStates, goldenCoeffStep]
    ring

/-- The original curvature rotation coordinate `E=p²(1+x)`. -/
def curvatureRotation (p x : ℝ) : ℝ := p ^ 2 * (1 + x)

/-- The original matter rotation coordinate `b=p-p² y`. -/
def matterRotation (p y : ℝ) : ℝ := p - p ^ 2 * y

/-- The curvature click `ell=4E(1-E)`. -/
def curvatureClick (p x : ℝ) : ℝ :=
  4 * curvatureRotation p x * (1 - curvatureRotation p x)

/-- The matter click `B=4b²(1-b²)`. -/
def matterClick (p y : ℝ) : ℝ :=
  4 * (matterRotation p y) ^ 2 * (1 - (matterRotation p y) ^ 2)

/-- The unchanged original sigma-minus direct click polynomial. -/
def originalClick (p z x y : ℝ) : ℝ :=
  let ell := curvatureClick p x
  let B := matterClick p y
  let A := ell + (1 - ell) * B
  z * (A + B) - z ^ 2 * A * B

/-- The curvature-independent term in the exact quadratic expansion. -/
def clickCoefficient0 (p z y : ℝ) : ℝ :=
  z * matterClick p y * (2 - z * matterClick p y) +
    z * (1 - z * matterClick p y) * (1 - matterClick p y) *
      (4 * p ^ 2 * (1 - p ^ 2))

/-- The linear coefficient in the exact quadratic expansion. -/
def clickCoefficient1 (p z y : ℝ) : ℝ :=
  z * (1 - z * matterClick p y) * (1 - matterClick p y) *
    (4 * p ^ 2 * (1 - 2 * p ^ 2))

/-- The quadratic coefficient in the exact quadratic expansion. -/
def clickCoefficient2 (p z y : ℝ) : ℝ :=
  -(z * (1 - z * matterClick p y) * (1 - matterClick p y) *
    (4 * p ^ 4))

/-- The shared Golden branch factor `d=z(1-zB)(1-B)` from the source proof. -/
def clickBranchFactor (p z y : ℝ) : ℝ :=
  z * (1 - z * matterClick p y) * (1 - matterClick p y)

/-- Under the Golden relation `p²+p=1`, the exact quadratic coefficients
reduce to the source proof's Eqs. (25):
`A₀=zB(2-zB)+4p³d`, `A₁=4p⁵d`, and `A₂=−4p⁴d`. -/
theorem golden_click_coefficients {p z y : ℝ} (hp : p ^ 2 + p = 1) :
    clickCoefficient0 p z y =
        z * matterClick p y * (2 - z * matterClick p y) +
          4 * p ^ 3 * clickBranchFactor p z y ∧
      clickCoefficient1 p z y = 4 * p ^ 5 * clickBranchFactor p z y ∧
      clickCoefficient2 p z y = -4 * p ^ 4 * clickBranchFactor p z y := by
  have hp2 : p ^ 2 = 1 - p := by linarith
  have h1mp2 : 1 - p ^ 2 = p := by linarith
  have hp3 : p ^ 3 = 2 * p - 1 := by
    calc
      p ^ 3 = p * p ^ 2 := by ring
      _ = p * (1 - p) := by rw [hp2]
      _ = 2 * p - 1 := by linarith [hp2]
  have hfactor : 1 - 2 * p ^ 2 = p ^ 3 := by
    rw [hp2, hp3]
    ring
  refine ⟨?_, ?_, ?_⟩
  · simp only [clickCoefficient0, clickBranchFactor]
    rw [h1mp2]
    ring
  · simp only [clickCoefficient1, clickBranchFactor]
    rw [hfactor]
    ring
  · simp only [clickCoefficient2, clickBranchFactor]
    ring

/-- The source's concrete Golden parameter instantiates the generic exact
coefficient reduction. -/
theorem golden_rotation_click_coefficients (z y : ℝ) :
    clickCoefficient0 goldenRotation z y =
        z * matterClick goldenRotation y *
          (2 - z * matterClick goldenRotation y) +
          4 * goldenRotation ^ 3 * clickBranchFactor goldenRotation z y ∧
      clickCoefficient1 goldenRotation z y =
        4 * goldenRotation ^ 5 * clickBranchFactor goldenRotation z y ∧
      clickCoefficient2 goldenRotation z y =
        -4 * goldenRotation ^ 4 * clickBranchFactor goldenRotation z y := by
  exact golden_click_coefficients goldenRotation_relation

/-- The original direct-click probability is exactly quadratic in `x`. -/
theorem originalClick_eq_quadratic (p z x y : ℝ) :
    originalClick p z x y = clickCoefficient0 p z y +
      clickCoefficient1 p z y * x + clickCoefficient2 p z y * x ^ 2 := by
  simp [originalClick, curvatureClick, curvatureRotation, matterClick,
    matterRotation, clickCoefficient0, clickCoefficient1, clickCoefficient2]
  ring

/-- Generic trace-minus-radial source of a quadratic `a₀(y)+a₁(y)x+a₂(y)x²`.
This is the reusable calculus step behind Eq. (26) of the nonlinear source. -/
theorem quadratic_trace_source_identity
    (a₀ a₁ a₂ : ℝ → ℝ) (a₀' a₁' a₂' x y : ℝ)
    (h₀ : HasDerivAt a₀ a₀' y)
    (h₁ : HasDerivAt a₁ a₁' y)
    (h₂ : HasDerivAt a₂ a₂' y) :
    x * deriv (fun u : ℝ => a₀ y + a₁ y * u + a₂ y * u ^ 2) x -
      y * deriv (fun v : ℝ => a₀ v + a₁ v * x + a₂ v * x ^ 2) y =
        (2 * a₂ y - y * a₂') * x ^ 2 +
          (a₁ y - y * a₁') * x - y * a₀' := by
  have hIdX : HasDerivAt (fun u : ℝ => u) 1 x := hasDerivAt_id x
  have hSqX : HasDerivAt (fun u : ℝ => u ^ 2) (2 * x) x := by
    simpa using hIdX.pow 2
  have hX₀ : HasDerivAt (fun u : ℝ => a₀ y) 0 x := hasDerivAt_const x (a₀ y)
  have hX₁ : HasDerivAt (fun u : ℝ => a₁ y * u) (a₁ y) x := by
    simpa [mul_comm] using hIdX.const_mul (a₁ y)
  have hX₂ : HasDerivAt (fun u : ℝ => a₂ y * u ^ 2) (a₂ y * (2 * x)) x := by
    simpa [mul_comm, mul_left_comm, mul_assoc] using hSqX.const_mul (a₂ y)
  have hX : HasDerivAt
      (fun u : ℝ => a₀ y + a₁ y * u + a₂ y * u ^ 2)
      (a₁ y + a₂ y * (2 * x)) x := by
    convert hX₀.add (hX₁.add hX₂) using 1
    · ext u
      simp only [Pi.add_apply]
      ring
    · ring
  have hY₀ : HasDerivAt (fun v : ℝ => a₀ v) a₀' y := h₀
  have hY₁ : HasDerivAt (fun v : ℝ => a₁ v * x) (a₁' * x) y := by
    simpa using h₁.mul_const x
  have hY₂ : HasDerivAt (fun v : ℝ => a₂ v * x ^ 2) (a₂' * x ^ 2) y := by
    simpa using h₂.mul_const (x ^ 2)
  have hY : HasDerivAt
      (fun v : ℝ => a₀ v + a₁ v * x + a₂ v * x ^ 2)
      (a₀' + a₁' * x + a₂' * x ^ 2) y := by
    convert hY₀.add (hY₁.add hY₂) using 1
    · ext v
      simp only [Pi.add_apply]
      ring
    · ring
  rw [hX.deriv, hY.deriv]
  ring

/-- For the actual nonlinear click, the independent-coframe trace source is
the quadratic from Eq. (26). The three differentiability witnesses are kept
explicit so the theorem states exactly which source family is varied. -/
theorem originalClick_trace_source_identity
    (p z x y d₀ d₁ d₂ : ℝ)
    (h₀ : HasDerivAt (fun v : ℝ => clickCoefficient0 p z v) d₀ y)
    (h₁ : HasDerivAt (fun v : ℝ => clickCoefficient1 p z v) d₁ y)
    (h₂ : HasDerivAt (fun v : ℝ => clickCoefficient2 p z v) d₂ y) :
    x * deriv (fun u : ℝ => originalClick p z u y) x -
      y * deriv (fun v : ℝ => originalClick p z x v) y =
        (2 * clickCoefficient2 p z y - y * d₂) * x ^ 2 +
          (clickCoefficient1 p z y - y * d₁) * x - y * d₀ := by
  have hx : (fun u : ℝ => originalClick p z u y) =
      (fun u : ℝ => clickCoefficient0 p z y +
        clickCoefficient1 p z y * u + clickCoefficient2 p z y * u ^ 2) := by
    funext u
    exact originalClick_eq_quadratic p z u y
  have hy : (fun v : ℝ => originalClick p z x v) =
      (fun v : ℝ => clickCoefficient0 p z v +
        clickCoefficient1 p z v * x + clickCoefficient2 p z v * x ^ 2) := by
    funext v
    exact originalClick_eq_quadratic p z x v
  rw [hx, hy]
  exact quadratic_trace_source_identity
    (fun v => clickCoefficient0 p z v)
    (fun v => clickCoefficient1 p z v)
    (fun v => clickCoefficient2 p z v) d₀ d₁ d₂ x y h₀ h₁ h₂

/-- For a real quadratic with negative leading coefficient and positive
linear and constant coefficients, the stable radical expression is a
negative root. -/
def negativeQuadraticRoot (a b c : ℝ) : ℝ :=
  -2 * c / (b + Real.sqrt (b ^ 2 - a * c * 4))

theorem negativeQuadraticRoot_spec {a b c : ℝ}
    (ha : a < 0) (hb : 0 < b) (hc : 0 < c) :
    a * negativeQuadraticRoot a b c ^ 2 +
        b * negativeQuadraticRoot a b c + c = 0 ∧
      negativeQuadraticRoot a b c < 0 := by
  have hdisc : 0 < b ^ 2 - 4 * a * c := by
    nlinarith
  have hdisc' : 0 < b ^ 2 - a * c * 4 := by
    nlinarith
  let d : ℝ := Real.sqrt (b ^ 2 - a * c * 4)
  have hsqrt : d ^ 2 = b ^ 2 - a * c * 4 := by
    dsimp [d]
    exact Real.sq_sqrt (le_of_lt hdisc')
  have hsqrt_pos : 0 < d := by
    dsimp [d]
    exact Real.sqrt_pos.2 hdisc'
  have hden : 0 < b + d := by
    linarith
  have hden'_ne : b + d ≠ 0 := ne_of_gt hden
  have hroot :
      a * (-2 * c / (b + d)) ^ 2 + b * (-2 * c / (b + d)) + c = 0 := by
    field_simp [hden'_ne]
    nlinarith [hsqrt]
  constructor
  · dsimp [negativeQuadraticRoot]
    simpa [d] using hroot
  · dsimp [negativeQuadraticRoot]
    have hnum : -2 * c < 0 := by nlinarith
    exact div_neg_of_neg_of_pos hnum (show 0 < b + Real.sqrt (b ^ 2 - a * c * 4) by
      simpa [d] using hden)

/-- The negative radical root is the only negative root when `a < 0`,
`b > 0` and `c > 0`: the two roots of this quadratic have opposite signs. -/
theorem negativeQuadraticRoot_unique_negative {a b c q : ℝ}
    (ha : a < 0) (hb : 0 < b) (hc : 0 < c)
    (hq : a * q ^ 2 + b * q + c = 0) (hqneg : q < 0) :
    q = negativeQuadraticRoot a b c := by
  obtain ⟨hr, hrneg⟩ := negativeQuadraticRoot_spec ha hb hc
  have hfactor : (q - negativeQuadraticRoot a b c) *
      (a * (q + negativeQuadraticRoot a b c) + b) = 0 := by
    nlinarith [hq, hr]
  rcases mul_eq_zero.mp hfactor with hsame | hother
  · linarith
  · have hsum : q + negativeQuadraticRoot a b c < 0 := by linarith
    have hprod : 0 < a * (q + negativeQuadraticRoot a b c) :=
      mul_pos_of_neg_of_neg ha hsum
    linarith

/-- Each actual nonlinear-click coefficient is polynomial in its matter
coordinate, hence the generic trace-source identity applies without extra
smoothness assumptions. -/
theorem originalClick_trace_source_identity_actual
    (p z x y : ℝ) :
    x * deriv (fun u : ℝ => originalClick p z u y) x -
      y * deriv (fun v : ℝ => originalClick p z x v) y =
        (2 * clickCoefficient2 p z y -
            y * deriv (fun v : ℝ => clickCoefficient2 p z v) y) * x ^ 2 +
          (clickCoefficient1 p z y -
            y * deriv (fun v : ℝ => clickCoefficient1 p z v) y) * x -
          y * deriv (fun v : ℝ => clickCoefficient0 p z v) y := by
  apply originalClick_trace_source_identity p z x y
    (deriv (fun v : ℝ => clickCoefficient0 p z v) y)
    (deriv (fun v : ℝ => clickCoefficient1 p z v) y)
    (deriv (fun v : ℝ => clickCoefficient2 p z v) y)
  · apply DifferentiableAt.hasDerivAt
    dsimp [clickCoefficient0, matterClick, matterRotation]
    fun_prop
  · apply DifferentiableAt.hasDerivAt
    dsimp [clickCoefficient1, matterClick, matterRotation]
    fun_prop
  · apply DifferentiableAt.hasDerivAt
    dsimp [clickCoefficient2, matterClick, matterRotation]
    fun_prop

/-- The three coefficients of the original click's independent-coframe
trace equation, matching Eq. (26) of the source proof. -/
def traceCoefficientA (p z y : ℝ) : ℝ :=
  2 * clickCoefficient2 p z y -
    y * deriv (fun v : ℝ => clickCoefficient2 p z v) y

def traceCoefficientB (p z y : ℝ) : ℝ :=
  clickCoefficient1 p z y -
    y * deriv (fun v : ℝ => clickCoefficient1 p z v) y

def traceCoefficientC (p z y : ℝ) : ℝ :=
  -y * deriv (fun v : ℝ => clickCoefficient0 p z v) y

/-- The exact original-number aperture z=y0=2^-20 used by the #334
nonlinear dust branch check. -/
def nonlinearDustSectorScale : ℝ := 1 / (2 : ℝ) ^ 20

/-- Common exact denominator in the Golden-field reduction of the three
trace coefficients at the fixed nonlinear dust sector. -/
def nonlinearDustTraceDenominator : ℝ :=
  12554203470773361527671578846415332832204710888928069025792

def nonlinearDustTraceDoubleDenominator : ℝ :=
  25108406941546723055343157692830665664409421777856138051584

def nonlinearDustTraceANumeratorP : ℝ :=
  5268058650513054623262402433763395984907432211655930041

def nonlinearDustTraceANumerator0 : ℝ :=
  3256618061576135697087915186179800036979780546381991681

def nonlinearDustTraceBNumeratorP : ℝ :=
  4262322096210792984780744979814770254080253549199977049

def nonlinearDustTraceBNumerator0 : ℝ :=
  5268038554089187623229439150431301957946247093117994757

def nonlinearDustTraceCNumeratorP : ℝ :=
  13884776909660477911855969143871666536523671553327

def nonlinearDustTraceCNumerator0 : ℝ :=
  4293319083168921166295556200737408068151796045153

/-- Rational endpoints enclosing the exact Golden rotation parameter. The
proof checks both square inequalities, rather than rounding sqrt 5. -/
def goldenRotationLower : ℝ :=
  61803398874989484820458683436563811772 / 10 ^ 38

def goldenRotationUpper : ℝ :=
  61803398874989484820458683436563811773 / 10 ^ 38

theorem goldenRotation_rational_bounds :
    goldenRotationLower < goldenRotation ∧ goldenRotation < goldenRotationUpper := by
  have hlo_nonneg : 0 ≤ 2 * goldenRotationLower + 1 := by
    norm_num [goldenRotationLower]
  have hlo_sq : (2 * goldenRotationLower + 1) ^ 2 < 5 := by
    norm_num [goldenRotationLower]
  have hlo_sqrt : 2 * goldenRotationLower + 1 < Real.sqrt 5 :=
    (Real.lt_sqrt hlo_nonneg).2 hlo_sq
  have hhi_nonneg : 0 ≤ 2 * goldenRotationUpper + 1 := by
    norm_num [goldenRotationUpper]
  have hhi_sq : 5 < (2 * goldenRotationUpper + 1) ^ 2 := by
    norm_num [goldenRotationUpper]
  have hhi_sqrt : Real.sqrt 5 < 2 * goldenRotationUpper + 1 :=
    (Real.sqrt_lt (by norm_num) hhi_nonneg).2 hhi_sq
  dsimp [goldenRotation]
  constructor <;> linarith

/-- Exact rational-field reductions of the original trace-source coefficients
on p=(sqrt 5-1)/2, z=y0=2^-20. The large rationals are independently reduced
in Lean using the Golden quadratic recurrence above. -/
theorem golden_sector_trace_coefficient_values :
    traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale =
        (nonlinearDustTraceANumeratorP / nonlinearDustTraceDenominator) * goldenRotation -
          nonlinearDustTraceANumerator0 / nonlinearDustTraceDenominator ∧
      traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale =
        (nonlinearDustTraceBNumeratorP / nonlinearDustTraceDenominator) * goldenRotation -
          nonlinearDustTraceBNumerator0 / nonlinearDustTraceDoubleDenominator ∧
      traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale =
        (2 * nonlinearDustTraceCNumerator0) / nonlinearDustTraceDenominator -
          (nonlinearDustTraceCNumeratorP / nonlinearDustTraceDenominator) * goldenRotation := by
  refine ⟨?_, ?_, ?_⟩
  · have hp := goldenRotation_relation
    simp (disch := fun_prop) [traceCoefficientA, clickCoefficient2,
      matterClick, matterRotation, nonlinearDustSectorScale]
    ring_nf
    simp_rw [golden_power_linear hp]
    simp [goldenPowerLinear, goldenCoeffStates, goldenCoeffStep]
    norm_num [nonlinearDustTraceANumeratorP, nonlinearDustTraceANumerator0,
      nonlinearDustTraceDenominator]
    ring
  · have hp := goldenRotation_relation
    simp (disch := fun_prop) [traceCoefficientB, clickCoefficient1,
      matterClick, matterRotation, nonlinearDustSectorScale]
    ring_nf
    simp_rw [golden_power_linear hp]
    simp [goldenPowerLinear, goldenCoeffStates, goldenCoeffStep]
    norm_num [nonlinearDustTraceBNumeratorP, nonlinearDustTraceBNumerator0,
      nonlinearDustTraceDenominator, nonlinearDustTraceDoubleDenominator]
    ring
  · have hp := goldenRotation_relation
    simp (disch := fun_prop) [traceCoefficientC, clickCoefficient0,
      matterClick, matterRotation, nonlinearDustSectorScale]
    ring_nf
    simp_rw [golden_power_linear hp]
    simp [goldenPowerLinear, goldenCoeffStates, goldenCoeffStep]
    norm_num [nonlinearDustTraceCNumeratorP, nonlinearDustTraceCNumerator0,
      nonlinearDustTraceDenominator]
    ring

/-- The exact trace-source coefficient signs used by the #334 negative branch
hold in its declared fixed sector; they are derived rather than supplied as
premises. -/
theorem golden_sector_trace_coefficient_signs :
    traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale < 0 ∧
      0 < traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale ∧
      0 < traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale := by
  rcases golden_sector_trace_coefficient_values with ⟨hAvalue, hBvalue, hCvalue⟩
  rw [hAvalue, hBvalue, hCvalue]
  have hp := goldenRotation_rational_bounds
  have hA :
      (nonlinearDustTraceANumeratorP / nonlinearDustTraceDenominator) * goldenRotationUpper -
        nonlinearDustTraceANumerator0 / nonlinearDustTraceDenominator < 0 := by
    norm_num [nonlinearDustTraceANumeratorP, nonlinearDustTraceANumerator0,
      nonlinearDustTraceDenominator, goldenRotationUpper]
  have hB : 0 <
      (nonlinearDustTraceBNumeratorP / nonlinearDustTraceDenominator) * goldenRotationLower -
        nonlinearDustTraceBNumerator0 / nonlinearDustTraceDoubleDenominator := by
    norm_num [nonlinearDustTraceBNumeratorP, nonlinearDustTraceBNumerator0,
      nonlinearDustTraceDenominator, nonlinearDustTraceDoubleDenominator,
      goldenRotationLower]
  have hC : 0 <
      (2 * nonlinearDustTraceCNumerator0) / nonlinearDustTraceDenominator -
        (nonlinearDustTraceCNumeratorP / nonlinearDustTraceDenominator) * goldenRotationUpper := by
    norm_num [nonlinearDustTraceCNumeratorP, nonlinearDustTraceCNumerator0,
      nonlinearDustTraceDenominator, goldenRotationUpper]
  have hAcoef : 0 < nonlinearDustTraceANumeratorP / nonlinearDustTraceDenominator := by
    norm_num [nonlinearDustTraceANumeratorP, nonlinearDustTraceDenominator]
  have hBcoef : 0 < nonlinearDustTraceBNumeratorP / nonlinearDustTraceDenominator := by
    norm_num [nonlinearDustTraceBNumeratorP, nonlinearDustTraceDenominator]
  have hCcoef : 0 < nonlinearDustTraceCNumeratorP / nonlinearDustTraceDenominator := by
    norm_num [nonlinearDustTraceCNumeratorP, nonlinearDustTraceDenominator]
  have hAmon := mul_lt_mul_of_pos_left hp.2 hAcoef
  have hBmon := mul_lt_mul_of_pos_left hp.1 hBcoef
  have hCmon := mul_lt_mul_of_pos_left hp.2 hCcoef
  constructor
  · nlinarith [hAmon, hA]
  constructor
  · nlinarith [hBmon, hB]
  · nlinarith [hCmon, hC]

/-- Exact 30-decimal rational enclosure requested by the #334 branch check. -/
def nonlinearDustKappaLower : ℝ :=
  23414790278587526834413240421129 / 10 ^ 30

def nonlinearDustKappaUpper : ℝ :=
  23414790278587526834413240421130 / 10 ^ 30

/-- The exact trace-source polynomial in the curvature coordinate for this
fixed Golden-sector specialization. -/
def nonlinearDustTracePolynomial (x : ℝ) : ℝ :=
  traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale * x ^ 2 +
    traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale * x +
    traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale

/-- The original trace polynomial has opposite signs at the two rational
curvature endpoints corresponding to the owner's kappa interval. -/
theorem golden_sector_trace_polynomial_endpoint_signs :
    0 < nonlinearDustTracePolynomial
        (-nonlinearDustKappaLower * nonlinearDustSectorScale) ∧
      nonlinearDustTracePolynomial
        (-nonlinearDustKappaUpper * nonlinearDustSectorScale) < 0 := by
  change 0 <
      traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale *
          (-nonlinearDustKappaLower * nonlinearDustSectorScale) ^ 2 +
        traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale *
          (-nonlinearDustKappaLower * nonlinearDustSectorScale) +
        traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale ∧
      traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale *
          (-nonlinearDustKappaUpper * nonlinearDustSectorScale) ^ 2 +
        traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale *
          (-nonlinearDustKappaUpper * nonlinearDustSectorScale) +
        traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale < 0
  rcases golden_sector_trace_coefficient_values with ⟨hA, hB, hC⟩
  rw [hA, hB, hC]
  rcases goldenRotation_rational_bounds with ⟨hpLo, hpHi⟩
  norm_num [goldenRotationLower, goldenRotationUpper] at hpLo hpHi
  constructor
  · norm_num [nonlinearDustKappaLower, nonlinearDustSectorScale,
      nonlinearDustTraceANumeratorP, nonlinearDustTraceANumerator0,
      nonlinearDustTraceBNumeratorP, nonlinearDustTraceBNumerator0,
      nonlinearDustTraceCNumeratorP, nonlinearDustTraceCNumerator0,
      nonlinearDustTraceDenominator, nonlinearDustTraceDoubleDenominator]
    nlinarith [hpHi]
  · norm_num [nonlinearDustKappaUpper, nonlinearDustSectorScale,
      nonlinearDustTraceANumeratorP, nonlinearDustTraceANumerator0,
      nonlinearDustTraceBNumeratorP, nonlinearDustTraceBNumerator0,
      nonlinearDustTraceCNumeratorP, nonlinearDustTraceCNumerator0,
      nonlinearDustTraceDenominator, nonlinearDustTraceDoubleDenominator]
    nlinarith [hpLo]


/-- The original click's trace-minus-radial equation is exactly the stated
quadratic in curvature, not a separately imposed branch equation. -/
theorem originalClick_trace_eq_quadratic (p z x y : ℝ) :
    x * deriv (fun u : ℝ => originalClick p z u y) x -
      y * deriv (fun v : ℝ => originalClick p z x v) y =
        traceCoefficientA p z y * x ^ 2 +
          traceCoefficientB p z y * x + traceCoefficientC p z y := by
  rw [originalClick_trace_source_identity_actual]
  simp [traceCoefficientA, traceCoefficientB, traceCoefficientC]
  ring

/-- If the actual trace coefficients have the source's signs, the original
click trace equation has the stable negative radical branch. The sign bounds
are explicit premises; the concrete rational enclosure and its physical
application are not part of this theorem. -/
theorem originalClick_trace_negative_branch {p z y : ℝ}
    (ha : traceCoefficientA p z y < 0)
    (hb : 0 < traceCoefficientB p z y)
    (hc : 0 < traceCoefficientC p z y) :
    ∃ x : ℝ, x < 0 ∧
      x * deriv (fun u : ℝ => originalClick p z u y) x -
        y * deriv (fun v : ℝ => originalClick p z x v) y = 0 := by
  let x := negativeQuadraticRoot (traceCoefficientA p z y)
    (traceCoefficientB p z y) (traceCoefficientC p z y)
  have hroot := negativeQuadraticRoot_spec ha hb hc
  refine ⟨x, ?_, ?_⟩
  · simpa [x] using hroot.2
  · rw [originalClick_trace_eq_quadratic]
    simpa [x] using hroot.1

/-- Every negative solution of the actual original-click trace equation is
the displayed radical branch, under the same coefficient-sign hypotheses. -/
theorem originalClick_trace_unique_negative_branch {p z y q : ℝ}
    (ha : traceCoefficientA p z y < 0)
    (hb : 0 < traceCoefficientB p z y)
    (hc : 0 < traceCoefficientC p z y)
    (hq : q * deriv (fun u : ℝ => originalClick p z u y) q -
      y * deriv (fun v : ℝ => originalClick p z q v) y = 0)
    (hqneg : q < 0) :
    q = negativeQuadraticRoot (traceCoefficientA p z y)
      (traceCoefficientB p z y) (traceCoefficientC p z y) := by
  have hpoly := hq
  rw [originalClick_trace_eq_quadratic] at hpoly
  exact negativeQuadraticRoot_unique_negative ha hb hc hpoly hqneg

/-- A quadratic with negative leading coefficient and positive linear
coefficient is strictly increasing on the negative axis. -/
theorem quadratic_polynomial_strictMono_negative {a b c x y : ℝ}
    (ha : a < 0) (hb : 0 < b) (hy : y < 0) (hxy : x < y) :
    a * x ^ 2 + b * x + c < a * y ^ 2 + b * y + c := by
  have hsum : x + y < 0 := by linarith
  have hprod : 0 < a * (x + y) := mul_pos_of_neg_of_neg ha hsum
  have hcoef : 0 < a * (x + y) + b := by linarith
  have hfactor : (a * y ^ 2 + b * y + c) - (a * x ^ 2 + b * x + c) =
      (y - x) * (a * (x + y) + b) := by ring
  have hdiff : 0 < (a * y ^ 2 + b * y + c) - (a * x ^ 2 + b * x + c) := by
    rw [hfactor]
    exact mul_pos (by linarith) hcoef
  linarith

/-- The exact negative radical branch has the source's rational kappa
enclosure, proved from the exact endpoint signs and monotonicity of the
original trace polynomial on negative curvature. -/
theorem golden_sector_kappa_enclosure :
    nonlinearDustKappaLower <
        -negativeQuadraticRoot
          (traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
          (traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
          (traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale) /
          nonlinearDustSectorScale ∧
      -negativeQuadraticRoot
          (traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
          (traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
          (traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale) /
          nonlinearDustSectorScale < nonlinearDustKappaUpper := by
  let a := traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale
  let b := traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale
  let c := traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale
  let q := negativeQuadraticRoot a b c
  let xFar := -nonlinearDustKappaUpper * nonlinearDustSectorScale
  let xNear := -nonlinearDustKappaLower * nonlinearDustSectorScale
  change nonlinearDustKappaLower < -q / nonlinearDustSectorScale ∧
    -q / nonlinearDustSectorScale < nonlinearDustKappaUpper
  rcases golden_sector_trace_coefficient_signs with ⟨ha, hb, hc⟩
  have hspec := negativeQuadraticRoot_spec ha hb hc
  have hqneg : q < 0 := by simpa [q] using hspec.2
  have hqpoly :
      a * q ^ 2 + b * q + c = 0 := by
    simpa [q, a, b, c] using hspec.1
  have hxFarNeg : xFar < 0 := by
    norm_num [xFar, nonlinearDustKappaUpper, nonlinearDustSectorScale]
  have hxNearNeg : xNear < 0 := by
    norm_num [xNear, nonlinearDustKappaLower, nonlinearDustSectorScale]
  have hEnds := golden_sector_trace_polynomial_endpoint_signs
  have hFarSign : a * xFar ^ 2 + b * xFar + c < 0 := by
    simpa [xFar, a, b, c, nonlinearDustTracePolynomial] using hEnds.2
  have hNearSign : 0 < a * xNear ^ 2 + b * xNear + c := by
    simpa [xNear, a, b, c, nonlinearDustTracePolynomial] using hEnds.1
  have hFarLt : xFar < q := by
    by_contra hnot
    have hle : q ≤ xFar := le_of_not_gt hnot
    rcases lt_or_eq_of_le hle with hlt | heq
    · have hmono := quadratic_polynomial_strictMono_negative
        (a := a) (b := b) (c := c) ha hb hxFarNeg hlt
      nlinarith [hmono, hqpoly, hFarSign]
    · rw [heq] at hqpoly
      nlinarith [hqpoly, hFarSign]
  have hLtNear : q < xNear := by
    by_contra hnot
    have hle : xNear ≤ q := le_of_not_gt hnot
    rcases lt_or_eq_of_le hle with hlt | heq
    · have hmono := quadratic_polynomial_strictMono_negative
        (a := a) (b := b) (c := c) ha hb hqneg hlt
      nlinarith [hmono, hqpoly, hNearSign]
    · rw [← heq] at hqpoly
      nlinarith [hqpoly, hNearSign]
  have hs : 0 < nonlinearDustSectorScale := by
    norm_num [nonlinearDustSectorScale]
  constructor
  · apply (lt_div_iff₀ hs).2
    dsimp [xNear] at hLtNear
    nlinarith [hLtNear]
  · apply (div_lt_iff₀ hs).2
    dsimp [xFar] at hFarLt
    nlinarith [hFarLt]


/-- The concrete #334 sector has an actual negative solution of the original
trace-source equation; its three coefficient signs are proved from the exact
rational Golden enclosure rather than passed into the general branch lemma. -/
theorem golden_sector_negative_branch_exists :
    ∃ x : ℝ, x < 0 ∧
      x * deriv (fun u : ℝ => originalClick goldenRotation
        nonlinearDustSectorScale u nonlinearDustSectorScale) x -
        nonlinearDustSectorScale * deriv (fun v : ℝ => originalClick goldenRotation
          nonlinearDustSectorScale x v) nonlinearDustSectorScale = 0 := by
  rcases golden_sector_trace_coefficient_signs with ⟨ha, hb, hc⟩
  exact originalClick_trace_negative_branch ha hb hc

/-- Any negative solution in the same concrete #334 sector is its displayed
stable radical branch. -/
theorem golden_sector_negative_branch_unique {q : ℝ}
    (hq : q * deriv (fun u : ℝ => originalClick goldenRotation
      nonlinearDustSectorScale u nonlinearDustSectorScale) q -
      nonlinearDustSectorScale * deriv (fun v : ℝ => originalClick goldenRotation
        nonlinearDustSectorScale q v) nonlinearDustSectorScale = 0)
    (hqneg : q < 0) :
    q = negativeQuadraticRoot
      (traceCoefficientA goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
      (traceCoefficientB goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale)
      (traceCoefficientC goldenRotation nonlinearDustSectorScale nonlinearDustSectorScale) := by
  rcases golden_sector_trace_coefficient_signs with ⟨ha, hb, hc⟩
  exact originalClick_trace_unique_negative_branch ha hb hc hq hqneg

end D0.Research.ClosedHistoryNonlinearDustBranch

end
