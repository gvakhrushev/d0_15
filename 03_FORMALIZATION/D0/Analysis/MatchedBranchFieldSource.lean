import D0.Analysis.MatchedBranchNormalizedPrice
import D0.Analysis.MatchedWeightedMeanFDeriv

/-!
# Matched branch field-source composition

The input `hfield` is exactly the owner branch-amplitude variation, not a
consequence of this finite matrix calculus. Its identification with an actual
admitted execution and the complete heat/clock/work source remain separate.
The gain may vanish; no division by the gain occurs in the base result.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Filter Matrix D0.Analysis.PositiveMatrixLogDet
open scoped BigOperators Topology Matrix.Norms.Frobenius ComplexOrder MatrixOrder

variable {ι θ : Type*} [Fintype ι] [DecidableEq ι]

/-- Algebraic coefficient identity for a positive matched corner and at least
one copy. No positivity of eta, nu, g or the gain is required. -/
theorem matched_owner_coefficient (M : ℕ) (c g eta nu w : ℝ)
    (hM : 0 < M) (hc : 0 < c) :
    (2 * nu * eta * c^M * w) * (2 * g * c^(M-1)) =
      (4 * g * (M : ℝ) * (nu * eta * (c^M)^2 * w) / c) / (M : ℝ) := by
  have hm : (M : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hM)
  have hcne : c ≠ 0 := ne_of_gt hc
  obtain ⟨m, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hM)
  simp only [Nat.succ_sub_one, pow_succ]
  field_simp; ring

/-- The scalar gain in the owner coefficient is the real trace of the
actual scaled resolvent history, with no commutation hypothesis needed. -/
theorem matched_owner_gain_trace (A R : Matrix ι ι ℂ) (eta t nu : ℝ) :
    nu * (((eta * t^2) • A * R).trace).re =
      nu * eta * t^2 * (R * A).trace.re := by
  rw [smul_mul_assoc, Matrix.trace_smul, Matrix.trace_mul_comm A R]
  simp only [Complex.smul_re, smul_eq_mul]
  ring

/-- Exact owner field substitution on the original one-curve finite price.
The per-branch amplitude law is an explicit assumption, with every copy
retained independently. The defined Gamma may vanish. -/
theorem branchReturn_price_owner_field_substitution
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p c d eta nu g : ℝ)
    (M : ℕ) (field : θ → Fin M → ℝ) (A : Matrix ι ι ℂ)
    (hM : 0 < M) (hc : 0 < c)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = c^M)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1)
    (hself : ∀ i ∈ s, star (proj i p) = proj i p)
    (hid : ∀ i ∈ s, proj i p * proj i p = proj i p)
    (hA : A.PosSemidef) (hAne : A ≠ 0) (hd : 0 < d) (heta : 0 ≤ eta)
    (hfield : ∀ i ∈ s, damp i = -2*g*c^(M-1) * ∑ j : Fin M, field i j) :
    let R := (affinePencil A d (eta * (c^M)^2))⁻¹
    let w := (R * A).trace.re
    let pi := fun i => (proj i p * R * A).trace.re / w
    let gain := nu * eta * (c^M)^2 * w
    let gamma := 4 * g * (M : ℝ) * gain / c
    0 < w ∧ (∀ i ∈ s, 0 ≤ pi i) ∧ (∑ i ∈ s, pi i) = 1 ∧
      HasDerivAt (fun y => -nu * Real.log
        ((d • (1 : Matrix ι ι ℂ) + eta •
          (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
        ((gamma / (M : ℝ)) * ∑ i ∈ s, pi i * ∑ j : Fin M, field i j) p := by
  let R := (affinePencil A d (eta * (c^M)^2))⁻¹
  let w := (R * A).trace.re
  let pi := fun i => (proj i p * R * A).trace.re / w
  have h := branchReturn_price_normalized_derivative s amp proj damp dproj p (c^M) d eta nu A
    hamp hproj hmatch hcomplete hself hid hA hAne hd heta
  refine ⟨h.1, h.2.1, h.2.2.1, ?_⟩
  have hcoef := matched_owner_coefficient M c g eta nu w hM hc
  apply h.2.2.2.congr_deriv
  calc
    _ = (2 * nu * eta * c^M * w) * (2 * g * c^(M-1)) *
        ∑ i ∈ s, pi i * ∑ j : Fin M, field i j := by
          rw [Finset.mul_sum]
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro i hi
          rw [hfield i hi]
          ring
    _ = _ := by rw [hcoef]


/-- A finite, normalized branch/copy mean has the full Fréchet derivative;
every weight derivative cancels at a common branch field value. -/
theorem matched_owner_mean_hasFDerivAt
    {X E : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset θ) (M : ℕ) (hM : 0 < M) (p : X) (z₀ : E)
    (pi : θ → X → ℝ) (dpi : θ → X →L[ℝ] ℝ)
    (z : θ × Fin M → X → E) (dz : θ × Fin M → X →L[ℝ] E)
    (hpi : ∀ i ∈ s, HasFDerivAt (pi i) (dpi i) p)
    (hz : ∀ a ∈ s.product Finset.univ, HasFDerivAt (z a) (dz a) p)
    (hmatch : ∀ a ∈ s.product Finset.univ, z a p = z₀)
    (hnorm : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, pi i y = 1) :
    let u := s.product (Finset.univ : Finset (Fin M))
    let weights := fun (a : θ × Fin M) y => ((M : ℝ)⁻¹) * pi a.1 y
    HasFDerivAt (fun y => ∑ a ∈ u, weights a y • z a y)
      (∑ a ∈ u, weights a p • dz a) p := by
  let u := s.product (Finset.univ : Finset (Fin M))
  let weights := fun (a : θ × Fin M) y => ((M : ℝ)⁻¹) * pi a.1 y
  have hm : (M : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hM)
  have hw : ∀ a ∈ u, HasFDerivAt (weights a) (((M : ℝ)⁻¹) • dpi a.1) p := by
    intro a ha
    have hi : a.1 ∈ s := (Finset.mem_product.mp ha).1
    exact (hpi a.1 hi).const_mul ((M : ℝ)⁻¹)
  have hwsum : ∀ᶠ y in 𝓝 p, ∑ a ∈ u, weights a y = 1 := by
    filter_upwards [hnorm] with y hy
    dsimp [u, weights]
    simp only [Finset.sum_product, Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    rw [← Finset.mul_sum, ← Finset.mul_sum, hy]
    field_simp
  exact D0.Analysis.matched_weighted_mean_hasFDerivAt u weights z
    (fun a => ((M : ℝ)⁻¹) • dpi a.1) dz p z₀ hw hz hmatch hwsum


/-- Evaluation of the copied-field mean derivative by a common field
covector. This keeps all branch and copy directions. -/
theorem matched_owner_mean_source_evaluation
    {X E : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset θ) (M : ℕ) (pi : θ → ℝ)
    (dz : θ × Fin M → X →L[ℝ] E) (L : E →L[ℝ] ℝ) (v : X) :
    L ((∑ a ∈ s.product (Finset.univ : Finset (Fin M)),
      (((M : ℝ)⁻¹) * pi a.1) • dz a) v) =
      (M : ℝ)⁻¹ * ∑ i ∈ s, pi i * ∑ j : Fin M, L (dz (i,j) v) := by
  simp only [ContinuousLinearMap.sum_apply, ContinuousLinearMap.smul_apply,
    map_sum, map_smul, smul_eq_mul, Finset.mul_sum]
  rw [Finset.product_eq_sprod]
  rw [Finset.sum_product s (Finset.univ : Finset (Fin M))
    (fun a => ((M : ℝ)⁻¹) * pi a.1 * L (dz a v))]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring


/-- Conditional same-direction composition with the full Fréchet mean map.
The owner amplitude law and the actual resolvent-to-mean weight binding are
explicit inputs, not consequences of the abstract charts. -/
theorem branchReturn_price_owner_mean_composition
    {X E : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset θ) (M : ℕ) (hM : 0 < M)
    (pt c d eta nu g : ℝ) (hc : 0 < c) (A : Matrix ι ι ℂ)
    (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) pt)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) pt)
    (hmatchAmp : ∀ i ∈ s, amp i pt = c^M)
    (hcomplete : ∀ᶠ y in 𝓝 pt, ∑ i ∈ s, proj i y = 1)
    (hself : ∀ i ∈ s, star (proj i pt) = proj i pt)
    (hid : ∀ i ∈ s, proj i pt * proj i pt = proj i pt)
    (hA : A.PosSemidef) (hAne : A ≠ 0) (hd : 0 < d) (heta : 0 ≤ eta)
    (px : X) (z₀ : E) (v : X) (L : E →L[ℝ] ℝ)
    (pi : θ → X → ℝ) (dpi : θ → X →L[ℝ] ℝ)
    (z : θ × Fin M → X → E) (dz : θ × Fin M → X →L[ℝ] E)
    (hpi : ∀ i ∈ s, HasFDerivAt (pi i) (dpi i) px)
    (hz : ∀ a ∈ s.product Finset.univ, HasFDerivAt (z a) (dz a) px)
    (hmatchZ : ∀ a ∈ s.product Finset.univ, z a px = z₀)
    (hnorm : ∀ᶠ y in 𝓝 px, ∑ i ∈ s, pi i y = 1)
    (hbind : ∀ i ∈ s, pi i px =
      (proj i pt * (affinePencil A d (eta * (c^M)^2))⁻¹ * A).trace.re /
        (((affinePencil A d (eta * (c^M)^2))⁻¹ * A).trace.re))
    (hfield : ∀ i ∈ s, damp i = -2*g*c^(M-1) *
      ∑ j : Fin M, L (dz (i,j) v)) :
    let R := (affinePencil A d (eta * (c^M)^2))⁻¹
    let gain := nu * eta * (c^M)^2 * (R * A).trace.re
    let gamma := 4 * g * (M : ℝ) * gain / c
    let u := s.product (Finset.univ : Finset (Fin M))
    let weights := fun (a : θ × Fin M) y => ((M : ℝ)⁻¹) * pi a.1 y
    let Dmean := ∑ a ∈ u, weights a px • dz a
    HasFDerivAt (fun y => ∑ a ∈ u, weights a y • z a y) Dmean px ∧
      HasDerivAt (fun y => -nu * Real.log
        ((d • (1 : Matrix ι ι ℂ) + eta •
          (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
        (gamma * L (Dmean v)) pt := by
  let R := (affinePencil A d (eta * (c^M)^2))⁻¹
  let piR := fun i => (proj i pt * R * A).trace.re / (R * A).trace.re
  let u := s.product (Finset.univ : Finset (Fin M))
  let weights := fun (a : θ × Fin M) y => ((M : ℝ)⁻¹) * pi a.1 y
  let Dmean := ∑ a ∈ u, weights a px • dz a
  have hmean := matched_owner_mean_hasFDerivAt s M hM px z₀ pi dpi z dz hpi hz hmatchZ hnorm
  have hprice := branchReturn_price_owner_field_substitution s amp proj damp dproj pt c d eta nu g
    M (fun i j => L (dz (i,j) v)) A hM hc hamp hproj hmatchAmp hcomplete hself hid hA hAne hd heta hfield
  have heval := matched_owner_mean_source_evaluation s M (fun i => pi i px) dz L v
  have hsum : (∑ i ∈ s, piR i * ∑ j : Fin M, L (dz (i,j) v)) =
      ∑ i ∈ s, pi i px * ∑ j : Fin M, L (dz (i,j) v) := by
    apply Finset.sum_congr rfl
    intro i hi
    rw [hbind i hi]
  constructor
  · exact hmean
  · apply hprice.2.2.2.congr_deriv
    rw [hsum]
    change _ = _ * L (Dmean v)
    rw [show L (Dmean v) = _ from heval]
    simp only [div_eq_mul_inv]
    ring

end D0.Analysis.MatchedBranchReturn
end
