import D0.Research.TaskFaithfulReturnBound
import D0.Research.TaskFaithfulReturnPrice
import D0.Research.TaskFaithfulRadialPriceDerivative

/-!
# Affine reporter compression and the ordered return price derivative

Source: #334 fd35893d77e4aa5f819bafa0c6428c8e7a8f1812, PROOF_RU.md
blob c99e90a8c8e96bae70e700fa88d1c2d824a1831b, §4 equations (5)-(8).
The protected full-input direction must compress to a supplied scalar alpha.
No physical admission, general nonradial variation, preparation derivative,
heat, clock, work, or normalized-gain existence is inferred.

The final theorem connects this reporter path to the exact ordered product.
For a family indexed by block label, the selected label must not recur in the
unchanged prefix or suffix; otherwise the same effect changes more than once.
-/
noncomputable section
namespace D0.Research

open Filter
open scoped ComplexOrder Topology

section Compression
variable {I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [CompleteSpace I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [CompleteSpace X]

/-- Fixed preparation, full-input affine reporter direction, scalar on the
protected input. The scalar slope is derived from the existing compression. -/
theorem taskReturnCompressionL_affine_scalar
    (prepare : X →L[ℂ] I) (reference direction : I →L[ℂ] I)
    (c0 alpha t : ℝ)
    (hcorner : taskReturnCompressionL prepare reference = (c0 : ℂ) • 1)
    (hscalar : prepare.adjoint ∘L (direction ∘L prepare) = (alpha : ℂ) • 1) :
    taskReturnCompressionL prepare (reference + (t : ℂ) • direction) =
      ((c0 - 2 * t * alpha : ℝ) : ℂ) • 1 := by
  have hcomp :
      prepare.adjoint ∘L (((t : ℂ) • direction) ∘L prepare) =
        (t : ℂ) • (prepare.adjoint ∘L (direction ∘L prepare)) := by
    ext v
    simp
  have hdiff :
      taskReturnCompressionL prepare (reference + (t : ℂ) • direction) -
        (c0 : ℂ) • 1 = (((-2 : ℂ) * (t : ℂ)) * (alpha : ℂ)) • 1 := by
    rw [← hcorner, taskReturnCompressionL_sub]
    simp only [add_sub_cancel_left]
    rw [hcomp, hscalar, smul_smul, smul_smul]
  calc
    taskReturnCompressionL prepare (reference + (t : ℂ) • direction) =
        (taskReturnCompressionL prepare (reference + (t : ℂ) • direction) -
          (c0 : ℂ) • 1) + (c0 : ℂ) • 1 := by abel
    _ = (((-2 : ℂ) * (t : ℂ)) * (alpha : ℂ)) • 1 + (c0 : ℂ) • 1 := by rw [hdiff]
    _ = ((c0 - 2 * t * alpha : ℝ) : ℂ) • 1 := by
      rw [← add_smul]
      congr 1 <;> push_cast <;> ring
end Compression

/-- The already-owned radial price derivative with the other factor made the
actual prefix/suffix scalar product. The full reporter compression identity is
a separate preceding theorem; tying the actual ordered operator product to
this scalar reference requires the listed scalar corner and occurrence maps. -/
theorem taskReturnGramPrice_affine_scalar_slope
    {J V X : Type*}
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z c0 alpha : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) (hc0 : 0 < c0)
    (left right : List J) (corners : J → ℝ) :
    let other := (left.map corners).prod * (right.map corners).prod
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) •
      D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => D0.Analysis.regularizedReturnPrice (1-z)
        ((((c0 - 2*t*alpha) ^ 2 : ℝ) : ℂ) • S))
      ((4 * alpha / c0) * D0.Analysis.regularizedReturnGain (1-z)
        (((c0 ^ 2 : ℝ) : ℂ) • S)) 0 := by
  let other := (left.map corners).prod * (right.map corners).prod
  let c : ℝ → ℝ := fun t => c0 - 2*t*alpha
  have hc : 0 < c 0 := by simpa [c] using hc0
  have hc' : HasDerivAt c (-(2*alpha)) 0 := by
    have h := (hasDerivAt_const 0 c0).sub
      (((hasDerivAt_id 0).const_mul 2).mul_const alpha)
    convert h using 1 <;> simp
  have h := taskReturnGramPrice_hasDerivAt_scalarCorner K basis z other 0
    hz hzOne c (-(2*alpha)) hc hc'
  dsimp only [c, other] at h ⊢
  convert h using 1 <;> (simp; ring)


/-- An exact scalar-corner word has exactly the price of its scalar reference.
This uses the owned full-product price theorem with zero error; no Gram
factorization or invertibility assumption is introduced. -/
theorem taskReturnProduct_exact_scalar_price
    {J I V X : Type*}
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (effect : J → I →ₗ[ℂ] I)
    (corners : J → ℝ) (w : List J)
    (hc : ∀ j ∈ w, 0 < corners j)
    (hcorner : ∀ j ∈ w, taskReturnCompression (prepare j).toLinearMap (effect j) =
      (corners j : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) :
    D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
      D0.Analysis.gramMatrix (taskReturnProduct prepare effect w ∘L K).toLinearMap basis) =
    D0.Analysis.regularizedReturnPrice (1-z)
      (((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) • D0.Analysis.gramMatrix K.toLinearMap basis) := by
  have h := taskReturnProduct_price_bound prepare effect effect corners (fun _ => 0) w
    hc hcorner (by intro j hj; simp) (by intro j hj; simp) K basis z hz hzOne
  apply sub_eq_zero.mp
  simpa [D0.Analysis.perturbationEta] using h


/-- Conditional local adapter to the real ordered product. The eventual
corner identities and product factor are explicit; a caller must derive them
from the affine reporter and the nonrepeated chosen occurrence. -/
theorem taskReturnProduct_price_affine_scalar_derivative
    {J I V X : Type*}
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (effect : ℝ → J → I →ₗ[ℂ] I)
    (c : ℝ → J → ℝ) (w : List J)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z c0 alpha : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) (hc0 : 0 < c0)
    (left right : List J) (corners : J → ℝ)
    (hnear : ∀ᶠ t in 𝓝 (0 : ℝ),
      (∀ j ∈ w, 0 < c t j) ∧
      (∀ j ∈ w, taskReturnCompression (prepare j).toLinearMap (effect t j) =
        (c t j : ℂ) • 1))
    (hproduct : ∀ᶠ t in 𝓝 (0 : ℝ), (w.map (c t)).prod =
      (c0 - 2*t*alpha) * ((left.map corners).prod * (right.map corners).prod)) :
    let other := (left.map corners).prod * (right.map corners).prod
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) •
      D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
        D0.Analysis.gramMatrix (taskReturnProduct prepare (effect t) w ∘L K).toLinearMap basis))
      ((4 * alpha / c0) * D0.Analysis.regularizedReturnGain (1-z)
        (((c0 ^ 2 : ℝ) : ℂ) • S)) 0 := by
  have h := taskReturnGramPrice_affine_scalar_slope K basis z c0 alpha hz hzOne hc0
    left right corners
  apply h.congr_of_eventuallyEq
  filter_upwards [hnear, hproduct] with t hn hp
  rw [taskReturnProduct_exact_scalar_price prepare (effect t) (c t) w hn.1 hn.2 K basis z hz hzOne, hp]
  simp only [smul_smul, ← Complex.ofReal_mul]
  congr 2 <;> ring


/-- Finite actual compression in the interface used by taskReturnProduct. -/
theorem taskReturnCompression_affine_scalar_finite
    {I X : Type*} [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    (prepare : X →ₗᵢ[ℂ] I) (reference direction : I →ₗ[ℂ] I)
    (c0 alpha t : ℝ)
    (hcorner : taskReturnCompression prepare.toLinearMap reference = (c0 : ℂ) • 1)
    (hscalar : prepare.toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L prepare.toContinuousLinearMap) = (alpha : ℂ) • 1) :
    taskReturnCompression prepare.toLinearMap (reference + (t : ℂ) • direction) =
      ((c0 - 2*t*alpha : ℝ) : ℂ) • 1 := by
  have hc : taskReturnCompressionL prepare.toContinuousLinearMap reference.toContinuousLinearMap =
      (c0 : ℂ) • 1 := by
    change taskReturnCompressionL prepare.toLinearMap.toContinuousLinearMap reference.toContinuousLinearMap = _
    rw [← taskReturnCompression_toContinuousLinearMap, hcorner]
    ext x
    simp
  have hv := taskReturnCompressionL_affine_scalar prepare.toContinuousLinearMap
    reference.toContinuousLinearMap direction.toContinuousLinearMap c0 alpha t hc hscalar
  ext x
  have hvx := congrArg (fun f : X →L[ℂ] X => f x) hv
  simpa [← taskReturnCompression_toContinuousLinearMap] using hvx


/-- Updating one label changes precisely its unique listed occurrence. -/
theorem updated_corner_product_split {J : Type*} [DecidableEq J]
    (left right : List J) (j : J) (corners : J → ℝ) (v : ℝ)
    (hleft : j ∉ left) (hright : j ∉ right) :
    ((left ++ j :: right).map (Function.update corners j v)).prod =
      v * ((left.map corners).prod * (right.map corners).prod) := by
  have hl : left.map (Function.update corners j v) = left.map corners := by
    apply List.map_congr_left
    intro x hx
    apply Function.update_of_ne
    intro heq
    subst x
    exact hleft hx
  have hr : right.map (Function.update corners j v) = right.map corners := by
    apply List.map_congr_left
    intro x hx
    apply Function.update_of_ne
    intro heq
    subst x
    exact hright hx
  simp only [List.map_append, List.map_cons, List.prod_append, List.prod_cons,
    Function.update_self, hl, hr]
  ring


/-- Actual one-reporter affine direction, with an explicitly nonrepeating
selected occurrence. This theorem does not assert physical admissibility. -/
theorem taskReturnProduct_price_one_affine_reporter
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ)
    (left right : List J) (j : J) (hleft : j ∉ left) (hright : j ∉ right)
    (hpos : ∀ k ∈ left ++ j :: right, 0 < corners k)
    (hcorner : ∀ k ∈ left ++ j :: right,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) :
    let other := (left.map corners).prod * (right.map corners).prod
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) • D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t : ℝ => D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
        D0.Analysis.gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction))
          (left ++ j :: right) ∘L K).toLinearMap basis))
      ((4 * alpha / corners j) * D0.Analysis.regularizedReturnGain (1-z)
        (((corners j ^ 2 : ℝ) : ℂ) • S)) 0 := by
  let effects : ℝ → J → I →ₗ[ℂ] I := fun t =>
    Function.update reference j (reference j + (t : ℂ) • direction)
  let c : ℝ → J → ℝ := fun t => Function.update corners j (corners j - 2*t*alpha)
  have hjmem : j ∈ left ++ j :: right := by simp
  have hc0 : 0 < corners j := hpos j hjmem
  have hp : ∀ᶠ t in 𝓝 (0 : ℝ), 0 < corners j - 2*t*alpha := by
    have hcont : Continuous (fun t : ℝ => corners j - 2*t*alpha) := by fun_prop
    exact hcont.continuousAt.eventually (eventually_gt_nhds (by simpa using hc0))
  have hnear : ∀ᶠ t in 𝓝 (0 : ℝ),
      (∀ k ∈ left ++ j :: right, 0 < c t k) ∧
      (∀ k ∈ left ++ j :: right, taskReturnCompression (prepare k).toLinearMap (effects t k) =
        (c t k : ℂ) • 1) := by
    filter_upwards [hp] with t ht
    constructor
    · intro k hk
      by_cases heq : k = j
      · subst k; simpa [c] using ht
      · simpa [c, Function.update, heq, Ne.symm heq] using hpos k hk
    · intro k hk
      by_cases heq : k = j
      · subst k
        simpa [c, effects] using taskReturnCompression_affine_scalar_finite
          (prepare j) (reference j) direction (corners j) alpha t (hcorner j hjmem) hscalar
      · simpa [c, effects, Function.update, heq, Ne.symm heq] using hcorner k hk
  have hproduct : ∀ᶠ t in 𝓝 (0 : ℝ), ((left ++ j :: right).map (c t)).prod =
      (corners j - 2*t*alpha) * ((left.map corners).prod * (right.map corners).prod) := by
    filter_upwards [] with t
    simpa [c] using updated_corner_product_split left right j corners
      (corners j - 2*t*alpha) hleft hright
  exact taskReturnProduct_price_affine_scalar_derivative prepare effects c (left ++ j :: right)
    K basis z (corners j) alpha hz hzOne hc0 left right corners hnear hproduct


/-- Zero scalar reporter direction implies zero price derivative even when
other protected directions and the retained history are nontrivial. -/
theorem taskReturnProduct_price_zero_compressed_direction {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ)
    (left right : List J) (j : J) (hleft : j ∉ left) (hright : j ∉ right)
    (hpos : ∀ k ∈ left ++ j :: right, 0 < corners k)
    (hcorner : ∀ k ∈ left ++ j :: right,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = 0)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) :
    HasDerivAt
      (fun t : ℝ => D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
        D0.Analysis.gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction))
          (left ++ j :: right) ∘L K).toLinearMap basis)) 0 0 := by
  have hs : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (0 : ℂ) • 1 := by
    simpa using hscalar
  have h := taskReturnProduct_price_one_affine_reporter prepare reference direction corners
    left right j hleft hright hpos hcorner 0 hs K basis z hz hzOne
  simpa using h

end D0.Research
end
