import D0.Analysis.MatchedWeightedMeanDerivative
import Mathlib.Analysis.Calculus.Deriv.Comp
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
  -- The finite product rule gives differentiability; identify its derivative
  -- on each direction by applying the curve theorem to the corresponding line.
  have hmean := HasFDerivAt.fun_sum (u := s) fun i hi => (hw i hi).smul (hx i hi)
  apply hmean.congr_fderiv
  ext v
  let line : ℝ → X := fun t => p + t • v
  have hbase : p = line 0 := by simp [line]
  have hline : HasDerivAt line v 0 := by
    simpa [line] using ((hasDerivAt_id' (0 : ℝ)).smul_const v).const_add p
  have ht : Tendsto line (𝓝 0) (𝓝 p) := hbase ▸ hline.continuousAt
  have hcurve := matched_weighted_mean_hasDerivAt s (fun i => w i ∘ line)
    (fun i => x i ∘ line) (fun i => dw i v) (fun i => dx i v) 0 x₀
    (fun i hi => (hw i hi).comp_hasDerivAt_of_eq 0 hline hbase)
    (fun i hi => (hx i hi).comp_hasDerivAt_of_eq 0 hline hbase)
    (fun i hi => by simpa only [Function.comp_apply, ← hbase] using hmatch i hi)
    (ht.eventually hnorm)
  have h := (hmean.comp_hasDerivAt_of_eq 0 hline hbase).unique hcurve
  simpa only [ContinuousLinearMap.sum_apply, ContinuousLinearMap.smul_apply,
    Function.comp_apply, ← hbase] using h

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
