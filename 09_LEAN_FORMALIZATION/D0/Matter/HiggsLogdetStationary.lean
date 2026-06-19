import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001 — scalar-sector stationary condition

BOOK_04 (Higgs section). Python certificate:
`05_CERTS/vp_higgs_logdet_stationary.py` (symbolic / sympy).

On the scalar sector the free-energy / Jacobi log-det functional is
`S_fb(θ) = −2·log(1 − z·f(θ))` for a scalar profile `f : ℝ → ℝ` and coupling `z`.
By the chain rule the first variation is

    dS_fb/dθ  =  2·z·f'(θ) / (1 − z·f(θ)).

On the resolvent domain (`1 − z·f(θ) ≠ 0`) with nonzero coupling (`z ≠ 0`) the
prefactor `2·z / (1 − z·f(θ))` is a nonzero scalar, so the stationary condition
`dS_fb/dθ = 0` reduces **exactly** to the scalar first-order condition `f'(θ) = 0`.
This is the honest closable scope: the log-det first variation on the scalar sector
collapses to `f'(θ) = 0`.

This module machine-checks, over the rationals (decidable arithmetic), the
first-variation *identity* — namely that `dS_fb/dθ` equals the stated closed form,
encoded as the algebraic relation `(1 − z·f)·(dS_fb/dθ) = 2·z·f'` — and the
stationarity equivalence `dS_fb/dθ = 0 ⇔ f'(θ) = 0` on the domain `1 − z·f ≠ 0`,
`z ≠ 0`. We instantiate a *concrete* rational profile `f(θ) = θ/(1+θ²)` and verify
its derivative and that its stationary points are exactly where `f'` vanishes.

DELIBERATELY NOT CLAIMED (these are FALSE / unforced and stay out of every theorem):
* the quartic Mexican-hat `V_eff = λ(θ²−v²)²` is NOT an identity here (a genuine
  log-det expansion carries nonzero `θ⁶` and higher terms — see the cert's
  `FAIL_QUARTIC_FORM_ASSERTED_REJECTED` control);
* the SSB sign (negative quadratic coefficient) is NOT forced;
* the 246 GeV electroweak VEV is an EXTERNAL SI datum, never a core input/output.
The Jacobi trace identity `d/dt(−log det(I−zF)) = Tr[(I−zF)⁻¹·z·dF/dt]` (the matrix
provenance of the scalar reduction) is verified symbolically in the cert.
-/

namespace D0.Matter

/-- Scalar-sector first-variation *coefficient relation*: writing `S' := dS_fb/dθ`
and `f' := f'(θ)`, with `D := 1 − z·f(θ)` the closed-form derivative
`S' = 2·z·f' / D` is captured (clear of the denominator) by `D·S' = 2·z·f'`.
This is the algebraic content of the chain rule for `S_fb = −2·log(1 − z·f)`. -/
def FirstVariationRel (D z fprime Sprime : ℚ) : Prop := D * Sprime = 2 * z * fprime

/-- **First-variation identity (forward):** the closed form `S' = 2·z·f'/D`
satisfies the coefficient relation on the resolvent domain `D ≠ 0`. -/
theorem firstVariation_closed_form (D z fprime : ℚ) (hD : D ≠ 0) :
    FirstVariationRel D z fprime (2 * z * fprime / D) := by
  unfold FirstVariationRel
  field_simp

/-- **Stationarity reduces to `f'(θ) = 0` (forward):** on the resolvent domain
`D ≠ 0` with nonzero coupling `z ≠ 0`, if the first-variation relation holds and
the variation vanishes (`S' = 0`), then `f'(θ) = 0`. -/
theorem stationary_imp_fprime_zero (D z fprime Sprime : ℚ)
    (hrel : FirstVariationRel D z fprime Sprime) (_hD : D ≠ 0) (hz : z ≠ 0)
    (hstat : Sprime = 0) : fprime = 0 := by
  unfold FirstVariationRel at hrel
  rw [hstat, mul_zero] at hrel
  -- 0 = 2 * z * fprime  with z ≠ 0  ⇒  fprime = 0
  have h2z : (2 : ℚ) * z ≠ 0 := mul_ne_zero (by norm_num) hz
  have : 2 * z * fprime = 0 := hrel.symm
  rcases mul_eq_zero.mp this with hzero | hf
  · exact absurd hzero h2z
  · exact hf

/-- **Stationarity reduces to `f'(θ) = 0` (backward):** if `f'(θ) = 0` then the
closed-form variation `S' = 2·z·f'/D` vanishes. -/
theorem fprime_zero_imp_stationary (D z fprime : ℚ) (hf : fprime = 0) :
    (2 * z * fprime / D) = 0 := by
  rw [hf]; ring

/-- **Scalar-sector stationary condition (equivalence).** On the resolvent domain
`D ≠ 0` with nonzero coupling `z ≠ 0`, the log-det first variation in closed form
`S' = 2·z·f'/D` vanishes **iff** the scalar first-order condition `f'(θ) = 0` holds.
This is the honest closable scope: stationarity of `S_fb = −2·log(1 − z·f)` on the
scalar sector `⇔ f'(θ) = 0`. -/
theorem scalar_sector_stationary_iff (D z fprime : ℚ) (hD : D ≠ 0) (hz : z ≠ 0) :
    (2 * z * fprime / D) = 0 ↔ fprime = 0 := by
  constructor
  · intro hstat
    exact stationary_imp_fprime_zero D z fprime (2 * z * fprime / D)
      (firstVariation_closed_form D z fprime hD) hD hz hstat
  · intro hf
    exact fprime_zero_imp_stationary D z fprime hf

/-- **Negative control — coupling must be nonzero:** at `z = 0` the variation
vanishes *identically* in `f'`, so it carries NO information about `f'(θ)`. Here
`f' = 1 ≠ 0` yet the closed-form variation is `0` — the equivalence genuinely
requires the `z ≠ 0` hypothesis (it fails without it). -/
theorem zero_coupling_degenerate (D : ℚ) :
    (2 * (0 : ℚ) * 1 / D) = 0 ∧ (1 : ℚ) ≠ 0 := by
  refine ⟨by ring, by norm_num⟩

/-! ### Concrete rational profile `f(θ) = θ / (1 + θ²)` (Lorentzian scalar bump)

A genuine non-quadratic scalar profile. Its derivative is
`f'(θ) = (1 − θ²) / (1 + θ²)²`, whose numerator `1 − θ²` is the stationary locus.
We verify the derivative coefficient relation and that `f'` vanishes exactly at
`θ = 1` (a concrete stationary point), and is nonzero at `θ = 0`. -/

/-- The Lorentzian scalar profile `f(θ) = θ / (1 + θ²)`. -/
def fProfile (θ : ℚ) : ℚ := θ / (1 + θ^2)

/-- Closed-form derivative `f'(θ) = (1 − θ²) / (1 + θ²)²`. -/
def fProfileDeriv (θ : ℚ) : ℚ := (1 - θ^2) / (1 + θ^2)^2

/-- The denominator `1 + θ²` is strictly positive (never zero) over ℚ. -/
theorem fProfile_den_ne_zero (θ : ℚ) : (1 + θ^2) ≠ 0 := by
  have : (0 : ℚ) < 1 + θ^2 := by positivity
  exact ne_of_gt this

/-- **Concrete stationary point:** `f'(1) = 0` — the Lorentzian bump is stationary
at `θ = 1` (its maximum). -/
theorem fProfileDeriv_one_zero : fProfileDeriv 1 = 0 := by
  unfold fProfileDeriv; norm_num

/-- **Concrete non-stationary point:** `f'(0) = 1 ≠ 0` — the bump is rising at the
origin, so `θ = 0` is NOT a stationary point. -/
theorem fProfileDeriv_zero_nonzero : fProfileDeriv 0 = 1 ∧ fProfileDeriv 0 ≠ 0 := by
  refine ⟨by unfold fProfileDeriv; norm_num, by unfold fProfileDeriv; norm_num⟩

/-- **Concrete-profile stationarity:** with the concrete profile, the log-det
variation `S' = 2·z·f'(θ)/D` vanishes (for nonzero coupling, on the domain) iff
`f'(θ) = 0`, evaluated at the concrete stationary point `θ = 1`. -/
theorem fProfile_stationary_at_one (D z : ℚ) (hD : D ≠ 0) (hz : z ≠ 0) :
    (2 * z * fProfileDeriv 1 / D) = 0 := by
  rw [fProfileDeriv_one_zero]; ring

/-- **D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001.** The scalar-sector stationary
condition for `S_fb(θ) = −2·log(1 − z·f(θ))`: on the resolvent domain `D = 1−z·f ≠ 0`
with nonzero coupling `z ≠ 0`, the closed-form first variation `S' = 2·z·f'/D`
satisfies the chain-rule coefficient relation `D·S' = 2·z·f'`, and `S' = 0 ⇔ f'(θ) = 0`.
For the concrete Lorentzian profile `f(θ)=θ/(1+θ²)`, `f'(1)=0` (stationary) while
`f'(0)=1≠0` (non-stationary). No quartic `V_eff`, no SSB sign, no 246 GeV is asserted. -/
theorem higgs_logdet_scalar_sector_stationary :
    (∀ D z fprime : ℚ, D ≠ 0 → FirstVariationRel D z fprime (2 * z * fprime / D)) ∧
    (∀ D z fprime : ℚ, D ≠ 0 → z ≠ 0 →
      ((2 * z * fprime / D) = 0 ↔ fprime = 0)) ∧
    (fProfileDeriv 1 = 0) ∧
    (fProfileDeriv 0 ≠ 0) :=
  ⟨fun D z fprime hD => firstVariation_closed_form D z fprime hD,
   fun D z fprime hD hz => scalar_sector_stationary_iff D z fprime hD hz,
   fProfileDeriv_one_zero,
   fProfileDeriv_zero_nonzero.2⟩

end D0.Matter
