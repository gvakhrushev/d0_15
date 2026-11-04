import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic

/-!
# Derivative of a matched finite weighted mean

A finite differentiable family of normalized scalar weights acts on independent
vector branches. At a matched point the derivative of the weights cancels,
without requiring positive or nonzero individual weights. This is the
mathematical mean-map component of #334 `b42db3deb`, matched-source synthesis
§2 (memo blob `886cac666344703940ebb699a304be2f86fb75bb`). It neither constructs
physical weights or field charts nor proves source factorization, admission,
uniform chart bounds or GR recovery.
-/

noncomputable section
namespace D0.Analysis

open Filter
open scoped BigOperators Topology

/-- For locally normalized differentiable weights, the derivative of the
finite weighted mean at a common branch value contains only branch derivatives. -/
theorem matched_weighted_mean_hasDerivAt
    {ι E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset ι) (w : ι → ℝ → ℝ) (x : ι → ℝ → E)
    (dw : ι → ℝ) (dx : ι → E) (t₀ : ℝ) (x₀ : E)
    (hw : ∀ i ∈ s, HasDerivAt (w i) (dw i) t₀)
    (hx : ∀ i ∈ s, HasDerivAt (x i) (dx i) t₀)
    (hmatch : ∀ i ∈ s, x i t₀ = x₀)
    (hnorm : ∀ᶠ t in 𝓝 t₀, ∑ i ∈ s, w i t = 1) :
    HasDerivAt (fun t => ∑ i ∈ s, w i t • x i t)
      (∑ i ∈ s, w i t₀ • dx i) t₀ := by
  have hweights : HasDerivAt (fun t => ∑ i ∈ s, w i t) (∑ i ∈ s, dw i) t₀ :=
    HasDerivAt.fun_sum hw
  have hzero : (∑ i ∈ s, dw i) = 0 := by
    have hnorm' : (fun t => ∑ i ∈ s, w i t) =ᶠ[𝓝 t₀] (fun _ => (1 : ℝ)) := hnorm
    have hc := hweights.congr_of_eventuallyEq hnorm'.symm
    exact hc.unique (hasDerivAt_const t₀ (1 : ℝ))
  have hmean : HasDerivAt (fun t => ∑ i ∈ s, w i t • x i t)
      (∑ i ∈ s, (w i t₀ • dx i + dw i • x i t₀)) t₀ :=
    HasDerivAt.fun_sum fun i hi => (hw i hi).smul (hx i hi)
  have heq : (∑ i ∈ s, (w i t₀ • dx i + dw i • x i t₀)) =
      ∑ i ∈ s, w i t₀ • dx i := by
    rw [Finset.sum_add_distrib]
    have hcancel : (∑ i ∈ s, dw i • x i t₀) = 0 := by
      calc
        _ = ∑ i ∈ s, dw i • x₀ := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [hmatch i hi]
        _ = (∑ i ∈ s, dw i) • x₀ := by rw [Finset.sum_smul]
        _ = 0 := by rw [hzero, zero_smul]
    rw [hcancel, add_zero]
  rwa [heq] at hmean

/-- A changing normalized pair of positive-at-zero weights. -/
def unmatchedWeight (i : Fin 2) (t : ℝ) : ℝ :=
  if i = 0 then 1/2 + t else 1/2 - t

/-- The branches are fixed but have different base values. -/
def unmatchedBranch (i : Fin 2) (_ : ℝ) : ℝ :=
  if i = 0 then 0 else 1

/-- Without matched branch values, varying normalized weights can contribute
nonzero derivative even though every branch has zero derivative. -/
theorem unmatched_weighted_mean_counterexample :
    (∀ t : ℝ, ∑ i : Fin 2, unmatchedWeight i t = 1) ∧
    (∀ i : Fin 2, 0 < unmatchedWeight i 0) ∧
    unmatchedBranch 0 0 ≠ unmatchedBranch 1 0 ∧
    (∀ i : Fin 2, HasDerivAt (unmatchedBranch i) 0 0) ∧
    HasDerivAt (fun t => ∑ i : Fin 2, unmatchedWeight i t * unmatchedBranch i t) (-1) 0 := by
  constructor
  · intro t
    norm_num [Fin.sum_univ_two, unmatchedWeight]
  constructor
  · intro i
    fin_cases i <;> norm_num [unmatchedWeight]
  constructor
  · norm_num [unmatchedBranch]
  constructor
  · intro i
    exact hasDerivAt_const 0 _
  · have h : (fun t : ℝ => ∑ i : Fin 2, unmatchedWeight i t * unmatchedBranch i t) =
        (fun t => 1/2 - t) := by
      funext t
      simp [Fin.sum_univ_two, unmatchedWeight, unmatchedBranch]
    rw [h]
    simpa using (hasDerivAt_const (0 : ℝ) (1/2 : ℝ)).sub (hasDerivAt_id (0 : ℝ))

end D0.Analysis
end
