import D0.Research.TaskFaithfulAffineReporterDerivative

/-!
# Repeated tied reporter labels in the ordered return price

Conditional extension of `TaskFaithfulAffineReporterDerivative`: every
occurrence of one typed label uses the same fixed preparation, effect and
affine direction. Its number of occurrences gives the exact multiplicity in
the derivative of the actual ordered price. A repeated gate name does not
itself establish that physical inputs share this label. Effect bounds,
admission, changing preparation, nonradial directions, heat, clock and work
are not derived. Source: #334 `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`,
`PROOF_RU.md` blob `c99e90a8c8e96bae70e700fa88d1c2d824a1831b`, §4–5.
-/

noncomputable section
namespace D0.Research

open scoped BigOperators

/-- Updating a shared label changes all its occurrences. The complementary
product retains the original word order and every unchanged occurrence. -/
theorem updated_word_product_count {J : Type*} [DecidableEq J]
    (w : List J) (j : J) (c : J → ℝ) (s : ℝ) :
    (w.map (Function.update c j s)).prod =
      s ^ w.count j * (w.map (fun k => if k = j then 1 else c k)).prod := by
  classical
  induction w with
  | nil => simp
  | cons k w ih =>
    by_cases h : k = j
    · subst k
      simp only [List.map_cons, List.prod_cons, List.count_cons_self,
        Function.update_self, if_true, one_mul, ih, pow_succ]
      ring
    · simp only [List.map_cons, List.prod_cons, List.count_cons_of_ne h,
        Function.update_of_ne h, if_neg h, ih]
      ring

/-- The exact scalar product of an affine update has its elementary
multiplicity derivative, including the empty and absent-label cases. -/
theorem updated_word_product_hasDerivAt {J : Type*} [DecidableEq J]
    (w : List J) (j : J) (c : J → ℝ) (alpha : ℝ) :
    HasDerivAt
      (fun t : ℝ => (w.map (Function.update c j (c j - 2*t*alpha))).prod)
      ((w.count j : ℝ) * (c j) ^ (w.count j - 1) * (-(2*alpha)) *
        (w.map (fun k => if k = j then 1 else c k)).prod) 0 := by
  have ha : HasDerivAt (fun t : ℝ => c j - 2*t*alpha) (-(2*alpha)) 0 := by
    have h := (hasDerivAt_const 0 (c j)).sub
      (((hasDerivAt_id 0).const_mul 2).mul_const alpha)
    convert h using 1 <;> simp
  have h := (ha.fun_pow (w.count j)).mul_const
    ((w.map (fun k => if k = j then 1 else c k)).prod)
  simp only [mul_zero, zero_mul, sub_zero] at h
  exact h.congr_of_eventuallyEq (Filter.Eventually.of_forall fun t =>
    (updated_word_product_count w j c (c j - 2*t*alpha)))

/-- Logarithmic square-product derivative for one tied reporter label,
including any number of its occurrences. Positivity is an explicit premise. -/
theorem updated_word_log_square_hasDerivAt {J : Type*} [DecidableEq J]
    (w : List J) (j : J) (c : J → ℝ) (alpha : ℝ)
    (hcj : 0 < c j) (hpos : ∀ k ∈ w, 0 < c k) :
    HasDerivAt
      (fun t : ℝ => Real.log (((w.map (Function.update c j (c j - 2*t*alpha))).prod)^2))
      (-4 * (w.count j : ℝ) * alpha / c j) 0 := by
  let other : ℝ := (w.map (fun k => if k = j then 1 else c k)).prod
  have hother : 0 < other := by
    dsimp only [other]
    apply List.prod_pos
    intro x hx
    obtain ⟨k, hk, rfl⟩ := List.mem_map.mp hx
    split_ifs with heq
    · norm_num
    · exact hpos k hk
  have hPzero : ((w.map (Function.update c j (c j - 2*(0:ℝ)*alpha))).prod) =
      (c j) ^ w.count j * other := by
    simpa [other] using updated_word_product_count w j c (c j)
  have hPpos : 0 < ((w.map (Function.update c j (c j - 2*(0:ℝ)*alpha))).prod) := by
    rw [hPzero]
    exact mul_pos (pow_pos hcj _) hother
  have hp := updated_word_product_hasDerivAt w j c alpha
  have hlog := (hp.fun_pow 2).log (pow_ne_zero 2 (ne_of_gt hPpos))
  have hcne : c j ≠ 0 := ne_of_gt hcj
  have hone : other ≠ 0 := ne_of_gt hother
  have halgebra :
      (2 * ((w.map (Function.update c j (c j - 2*(0:ℝ)*alpha))).prod) ^ (2-1) *
       ((w.count j : ℝ) * (c j) ^ (w.count j - 1) * (-(2*alpha)) * other)) /
       (((w.map (Function.update c j (c j - 2*(0:ℝ)*alpha))).prod)^2) =
       -4 * (w.count j : ℝ) * alpha / c j := by
    rw [hPzero]
    cases hcount : w.count j with
    | zero => simp [hcount]
    | succ n =>
      have hpow : (c j)^n ≠ 0 := pow_ne_zero n hcne
      simp only [hcount, Nat.cast_succ, Nat.succ_sub_one, pow_succ, pow_one]
      field_simp
      <;> ring
  convert hlog using 1
  simpa only [other] using halgebra.symm


open Filter D0.Analysis D0.Analysis.ReturnPriceLogScaleDerivative
open scoped ComplexOrder Topology

/-- General adapter from an exact scalar-corner family and its log-product
slope to the actual ordered product's price. No history inverse or positive
gain is assumed. -/
theorem taskReturnProduct_price_of_scalar_log_product
    {J I V X : Type*}
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (effect : ℝ → J → I →ₗ[ℂ] I)
    (c : ℝ → J → ℝ) (w : List J)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z slope : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (hnear : ∀ᶠ t in 𝓝 (0 : ℝ),
      (∀ j ∈ w, 0 < c t j) ∧
      (∀ j ∈ w, taskReturnCompression (prepare j).toLinearMap (effect t j) =
        (c t j : ℂ) • 1))
    (hqlog : HasDerivAt (fun t => Real.log ((w.map (c t)).prod ^ 2)) slope 0) :
    let S : Matrix n n ℂ := ((z : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare (effect t) w ∘L K).toLinearMap basis))
      (-slope * regularizedReturnGain (1-z)
        ((((w.map (c 0)).prod ^ 2 : ℝ) : ℂ) • S)) 0 := by
  let S : Matrix n n ℂ := ((z : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
  let q : ℝ → ℝ := fun t => (w.map (c t)).prod
  have hS : S.PosSemidef :=
    (gramMatrix_posSemidef K.toLinearMap basis).smul (Complex.zero_le_real.mpr hz)
  have hqnear : ∀ᶠ t in 𝓝 (0 : ℝ), 0 < q t := by
    filter_upwards [hnear] with t ht
    apply List.prod_pos
    intro x hx
    obtain ⟨j,hj,rfl⟩ := List.mem_map.mp hx
    exact ht.1 j hj
  have hq0 : 0 < q 0 := (mem_of_mem_nhds (s := {t : ℝ | 0 < q t}) hqnear)
  have houter := regularizedReturnPrice_hasDerivAt_logScale S hS (1-z)
    (Real.log (q 0 ^ 2)) (sub_pos.mpr hzOne)
  have h := houter.comp 0 hqlog
  rw [Real.exp_log (sq_pos_of_pos hq0)] at h
  have heq : (fun t => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare (effect t) w ∘L K).toLinearMap basis)) =ᶠ[𝓝 (0 : ℝ)]
      (fun t => regularizedReturnPrice (1-z) ((Real.exp (Real.log (q t ^ 2)) : ℂ) • S)) := by
    filter_upwards [hnear, hqnear] with t ht hpos
    rw [taskReturnProduct_exact_scalar_price prepare (effect t) (c t) w ht.1 ht.2 K basis z hz hzOne,
      Real.exp_log (sq_pos_of_pos hpos)]
    dsimp [S,q]
    simp only [smul_smul, ← Complex.ofReal_mul]
    congr 2 <;> ring
  have h' := h.congr_of_eventuallyEq heq
  convert h' using 1 <;> ring


/-- Repeated tied label, conditional only on the scalar log-product calculus.
The same selected effect and preparation are used at each occurrence. -/
theorem taskReturnProduct_price_repeated_affine_of_log_product
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ) (w : List J) (j : J)
    (hpos : ∀ k ∈ w, 0 < corners k) (hcj : 0 < corners j)
    (hcorner : ∀ k ∈ w,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (hqlog : HasDerivAt
      (fun t => Real.log ((w.map (Function.update corners j (corners j - 2*t*alpha))).prod ^ 2))
      (-4 * (w.count j : ℝ) * alpha / corners j) 0) :
    let S : Matrix n n ℂ := ((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis))
      ((4 * (w.count j : ℝ) * alpha / corners j) * regularizedReturnGain (1-z) S) 0 := by
  let effects : ℝ → J → I →ₗ[ℂ] I := fun t =>
    Function.update reference j (reference j + (t : ℂ) • direction)
  let c : ℝ → J → ℝ := fun t => Function.update corners j (corners j - 2*t*alpha)
  have hp : ∀ᶠ t in 𝓝 (0 : ℝ), 0 < corners j - 2*t*alpha := by
    have hcont : Continuous (fun t : ℝ => corners j - 2*t*alpha) := by fun_prop
    exact hcont.continuousAt.eventually (eventually_gt_nhds (by simpa using hcj))
  have hnear : ∀ᶠ t in 𝓝 (0 : ℝ),
      (∀ k ∈ w, 0 < c t k) ∧
      (∀ k ∈ w, taskReturnCompression (prepare k).toLinearMap (effects t k) =
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
          (prepare j) (reference j) direction (corners j) alpha t (hcorner j hk) hscalar
      · simpa [c, effects, Function.update, heq, Ne.symm heq] using hcorner k hk
  have hcbase : c 0 = corners := by
    funext k
    by_cases h : k = j
    · subst k; simp [c]
    · simp [c, Function.update, h, Ne.symm h]
  have hex := taskReturnProduct_price_of_scalar_log_product prepare effects c w K basis z
    (-4 * (w.count j : ℝ) * alpha / corners j) hz hzOne hnear hqlog
  rw [hcbase] at hex
  dsimp only [effects] at hex
  have hsign : -(-4 * (w.count j : ℝ) * alpha / corners j) =
      4 * (w.count j : ℝ) * alpha / corners j := by ring
  rw [hsign] at hex
  simpa only [smul_smul, ← Complex.ofReal_mul, mul_comm] using hex

/-- No occurrences: price is constant without any positivity, scalarity,
or nonzero-gain premises. -/
theorem taskReturnProduct_price_absent_label
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (w : List J) (j : J) (hj : j ∉ w)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V) (z : ℝ) :
    HasDerivAt
      (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis))
      0 0 := by
  have heq : ∀ t : ℝ, taskReturnProduct prepare
      (Function.update reference j (reference j + (t : ℂ) • direction)) w =
        taskReturnProduct prepare reference w := by
    intro t
    unfold taskReturnProduct
    congr 1
    apply List.map_congr_left
    intro k hk
    have h : k ≠ j := by
      intro e
      subst k
      exact hj hk
    rw [Function.update_of_ne h]
  have hfun : (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis)) =
      (fun _ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare reference w ∘L K).toLinearMap basis)) := by
    funext t
    rw [heq]
  rw [hfun]
  exact hasDerivAt_const 0 _


theorem taskReturnProduct_price_repeated_affine
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ) (w : List J) (j : J)
    (hpos : ∀ k ∈ w, 0 < corners k) (hcj : 0 < corners j)
    (hcorner : ∀ k ∈ w,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
 :
    let S : Matrix n n ℂ := ((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis))
      ((4 * (w.count j : ℝ) * alpha / corners j) * regularizedReturnGain (1-z) S) 0 := by
  exact taskReturnProduct_price_repeated_affine_of_log_product prepare reference direction corners w j
    hpos hcj hcorner alpha hscalar K basis z hz hzOne
    (updated_word_log_square_hasDerivAt w j corners alpha hcj hpos)



theorem taskReturnProduct_price_repeated_count_1
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ) (w : List J) (j : J)
    (hpos : ∀ k ∈ w, 0 < corners k) (hcj : 0 < corners j)
    (hcorner : ∀ k ∈ w,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (hcount : w.count j = 1)
    (alpha : ℝ)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
 :
    let S : Matrix n n ℂ := ((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis))
      ((4 * alpha / corners j) * regularizedReturnGain (1-z) S) 0 := by
  have h := taskReturnProduct_price_repeated_affine prepare reference direction corners w j
    hpos hcj hcorner alpha hscalar K basis z hz hzOne
  norm_num [hcount] at h ⊢
  exact h


theorem taskReturnProduct_price_repeated_count_2
    {J I V X : Type*} [DecidableEq J]
    [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference : J → I →ₗ[ℂ] I)
    (direction : I →ₗ[ℂ] I) (corners : J → ℝ) (w : List J) (j : J)
    (hpos : ∀ k ∈ w, 0 < corners k) (hcj : 0 < corners j)
    (hcorner : ∀ k ∈ w,
      taskReturnCompression (prepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (hcount : w.count j = 2)
    (alpha : ℝ)
    (hscalar : (prepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (prepare j).toContinuousLinearMap) = (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
 :
    let S : Matrix n n ℂ := ((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t : ℝ => regularizedReturnPrice (1-z) ((z : ℂ) •
        gramMatrix (taskReturnProduct prepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w ∘L K).toLinearMap basis))
      ((8 * alpha / corners j) * regularizedReturnGain (1-z) S) 0 := by
  have h := taskReturnProduct_price_repeated_affine prepare reference direction corners w j
    hpos hcj hcorner alpha hscalar K basis z hz hzOne
  norm_num [hcount] at h ⊢
  exact h

end D0.Research
end
