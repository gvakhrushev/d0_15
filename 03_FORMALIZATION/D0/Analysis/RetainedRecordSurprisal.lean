import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# Joint surprisal on a fixed set of retained records

For each positive record mass, the Born factor cancels the exponential of its
joint log-mass contribution to the price. Only the tariffs can contribute to
the scalar moment's first variation while the support is fixed. This compares
one specified evaluation of the recorded outcomes on the validated Parry task.
-/

namespace D0.Analysis.RetainedRecordSurprisal

open Filter
open scoped Topology

variable {ι : Type*}

/-- Scalar moment with the joint classical surprisal of each recorded outcome. -/
noncomputable def moment (records : Finset ι) (ell : ℝ) (mass tariff : ι → ℝ) : ℝ :=
  ∑ i ∈ records, mass i * Real.exp (-ell * (tariff i + Real.log (mass i) / ell))

/-- Each positive outcome contributes its tariff weight, independently of its mass. -/
theorem moment_eq_tariff_sum (records : Finset ι) {ell : ℝ} (hell : ell ≠ 0)
    (mass tariff : ι → ℝ) (hpos : ∀ i ∈ records, 0 < mass i) :
    moment records ell mass tariff = ∑ i ∈ records, Real.exp (-ell * tariff i) := by
  apply Finset.sum_congr rfl
  intro i hi
  have hexp : -ell * (tariff i + Real.log (mass i) / ell) =
      -ell * tariff i - Real.log (mass i) := by
    field_simp
    ring
  rw [hexp, Real.exp_sub, Real.exp_log (hpos i hi)]
  rw [← mul_div_assoc, mul_div_cancel_left₀ _ (hpos i hi).ne']

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- On a neighbourhood with the same positive support, all moving tariffs retain
their derivatives; no differentiability hypothesis is needed for the masses. -/
theorem hasFDerivAt_moment (records : Finset ι) {ell : ℝ} (hell : ell ≠ 0) {x : E}
    (mass tariff : E → ι → ℝ) (dTariff : ι → E →L[ℝ] ℝ)
    (hpos : ∀ᶠ y in 𝓝 x, ∀ i ∈ records, 0 < mass y i)
    (hd : ∀ i ∈ records, HasFDerivAt (fun y => tariff y i) (dTariff i) x) :
    HasFDerivAt (fun y => moment records ell (mass y) (tariff y))
      (∑ i ∈ records, Real.exp (-ell * tariff x i) • ((-ell) • dTariff i)) x := by
  apply (HasFDerivAt.fun_sum (u := records)
    (fun i hi => ((hd i hi).const_mul (-ell)).exp)).congr_of_eventuallyEq
  exact hpos.mono fun y hy => moment_eq_tariff_sum records hell (mass y) (tariff y) hy

/-- Fixed parse lengths give zero full derivative on every fixed positive support. -/
theorem hasFDerivAt_moment_fixed (records : Finset ι) {ell : ℝ} (hell : ell ≠ 0) {x : E}
    (mass : E → ι → ℝ) (tariff : ι → ℝ)
    (hpos : ∀ᶠ y in 𝓝 x, ∀ i ∈ records, 0 < mass y i) :
    HasFDerivAt (fun y => moment records ell (mass y) tariff) (0 : E →L[ℝ] ℝ) x := by
  simpa using hasFDerivAt_moment records hell mass (fun _ => tariff) (fun _ => 0)
    hpos (fun i _ => hasFDerivAt_const (tariff i) x)

end D0.Analysis.RetainedRecordSurprisal
