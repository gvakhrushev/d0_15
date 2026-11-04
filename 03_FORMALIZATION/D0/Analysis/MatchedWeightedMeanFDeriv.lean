import D0.Analysis.MatchedWeightedMeanDerivative
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Add

/-!
# Fréchet derivative of a matched finite weighted mean

The finite mean map is differentiated on an arbitrary real normed input
space. Normalization is local, and all branches meet at the base point.
This is a conditional mathematical component of #334 `b42db3deb`, matched-source
synthesis §2, memo blob `886cac666344703940ebb699a304be2f86fb75bb`.
It does not establish a physical source map, native admission, or GR closure.
-/

noncomputable section
namespace D0.Analysis

open Filter
open scoped BigOperators Topology

/-- The full Fréchet derivative of a finite normalized mean at a common
branch value retains all independent branch derivatives. -/
theorem matched_weighted_mean_hasFDerivAt
    {ι X E : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset ι) (w : ι → X → ℝ) (x : ι → X → E)
    (dw : ι → X →L[ℝ] ℝ) (dx : ι → X →L[ℝ] E) (p : X) (x₀ : E)
    (hw : ∀ i ∈ s, HasFDerivAt (w i) (dw i) p)
    (hx : ∀ i ∈ s, HasFDerivAt (x i) (dx i) p)
    (hmatch : ∀ i ∈ s, x i p = x₀)
    (hnorm : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, w i y = 1) :
    HasFDerivAt (fun y => ∑ i ∈ s, w i y • x i y)
      (∑ i ∈ s, w i p • dx i) p := by
  have hweights : HasFDerivAt (fun y => ∑ i ∈ s, w i y) (∑ i ∈ s, dw i) p :=
    HasFDerivAt.fun_sum hw
  have hzero : (∑ i ∈ s, dw i) = 0 := by
    have hnorm' : (fun y => ∑ i ∈ s, w i y) =ᶠ[𝓝 p] (fun _ => (1 : ℝ)) := hnorm
    have hc := hweights.congr_of_eventuallyEq hnorm'.symm
    exact hc.unique (hasFDerivAt_const (1 : ℝ) p)
  have hmean : HasFDerivAt (fun y => ∑ i ∈ s, w i y • x i y)
      (∑ i ∈ s, (w i p • dx i + (dw i).smulRight (x i p))) p :=
    HasFDerivAt.fun_sum fun i hi => (hw i hi).smul (hx i hi)
  have heq : (∑ i ∈ s, (w i p • dx i + (dw i).smulRight (x i p))) =
      ∑ i ∈ s, w i p • dx i := by
    rw [Finset.sum_add_distrib]
    have hcancel : (∑ i ∈ s, (dw i).smulRight (x i p)) = 0 := by
      ext v
      simp only [ContinuousLinearMap.sum_apply, ContinuousLinearMap.smulRight_apply,
        ContinuousLinearMap.zero_apply]
      calc
        _ = ∑ i ∈ s, (dw i v) • x₀ := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [hmatch i hi]
        _ = (∑ i ∈ s, dw i v) • x₀ := by rw [Finset.sum_smul]
        _ = 0 := by
          have hv := congrArg (fun f : X →L[ℝ] ℝ => f v) hzero
          simp only [ContinuousLinearMap.sum_apply, ContinuousLinearMap.zero_apply] at hv
          rw [hv, zero_smul]
    rw [hcancel, add_zero]
  rwa [heq] at hmean

/-- One-dimensional consequence, matching the earlier curve theorem. -/
theorem matched_weighted_mean_one_dimensional_via_fderiv
    {ι E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset ι) (w : ι → ℝ → ℝ) (x : ι → ℝ → E)
    (dw : ι → ℝ) (dx : ι → E) (t₀ : ℝ) (x₀ : E)
    (hw : ∀ i ∈ s, HasDerivAt (w i) (dw i) t₀)
    (hx : ∀ i ∈ s, HasDerivAt (x i) (dx i) t₀)
    (hmatch : ∀ i ∈ s, x i t₀ = x₀)
    (hnorm : ∀ᶠ t in 𝓝 t₀, ∑ i ∈ s, w i t = 1) :
    HasDerivAt (fun t => ∑ i ∈ s, w i t • x i t)
      (∑ i ∈ s, w i t₀ • dx i) t₀ := by
  have h := matched_weighted_mean_hasFDerivAt s w x
    (fun i => (1 : ℝ →L[ℝ] ℝ).smulRight (dw i))
    (fun i => (1 : ℝ →L[ℝ] ℝ).smulRight (dx i)) t₀ x₀
    (fun i hi => (hw i hi).hasFDerivAt) (fun i hi => (hx i hi).hasFDerivAt)
    hmatch hnorm
  simpa using h.hasDerivAt

end D0.Analysis
end
