import D0.Analysis.MatchedBranchAmplitudeDerivative
import D0.Analysis.MatchedBranchFieldSource

/-!
# Product-to-field matched branch composition

On the owner's ideal finite product, a local equality to the actual amplitude
and independently differentiable copy actions derive the matched amplitude
and branch field-variation inputs of the existing price/mean consumer. The
local product binding, every copy-action derivative, resolvent weight binding,
field/copy maps and all physical admission/source assumptions remain inputs.
No full heat/clock/work or physical GR claim follows.
Source: #334 `b42db3deb79a55d4ede542ac4aef54a2c2f1106c`, memo blob
`886cac666344703940ebb699a304be2f86fb75bb`, H4/H5/H18 and §2 R1–R2.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Filter Matrix D0.Analysis.PositiveMatrixLogDet
open D0.Analysis.MatchedBranchAmplitude
open scoped BigOperators Topology Matrix.Norms.Frobenius ComplexOrder MatrixOrder

variable {ι θ : Type*} [Fintype ι] [DecidableEq ι]

/-- The concrete matched product supplies both amplitude hypotheses of the
existing owner price/mean theorem. Each copy-action derivative is bound to the
same supplied covector and direction; the product and weight bindings remain
explicit and do not establish a physically admitted field path. -/
theorem branchReturn_price_owner_product_mean_composition
    {X E : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : Finset θ) (M : ℕ) (hM : 0 < M)
    (pt c d eta nu g Q₀ : ℝ) (hc : 0 < c) (A : Matrix ι ι ℂ)
    (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) pt)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) pt)
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
    (I : θ → Fin M → ℝ → ℝ)
    (hlocal : ∀ i ∈ s, amp i =ᶠ[𝓝 pt] amplitude M Q₀ g (I i))
    (hI : ∀ i ∈ s, ∀ j, HasDerivAt (I i j) (L (dz (i,j) v)) pt)
    (hcorner : ∀ i ∈ s, ∀ j, 1 - 2 * (Q₀ + g * I i j pt) = c) :
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
  have hmatchAmp : ∀ i ∈ s, amp i pt = c^M := by
    intro i hi
    rw [(hlocal i hi).self_of_nhds]
    unfold amplitude
    calc
      _ = ∏ _j : Fin M, c := by
        apply Finset.prod_congr rfl
        intro j hj
        exact hcorner i hi j
      _ = c^M := by simp
  have hfield : ∀ i ∈ s, damp i = -2*g*c^(M-1) *
      ∑ j : Fin M, L (dz (i,j) v) :=
    branch_derivatives_forced s M Q₀ g pt c amp damp I
      (fun i j => L (dz (i,j) v)) hamp hlocal hI hcorner
  exact branchReturn_price_owner_mean_composition s M hM pt c d eta nu g hc A
    amp proj damp dproj hamp hproj hmatchAmp hcomplete hself hid hA hAne hd heta
    px z₀ v L pi dpi z dz hpi hz hmatchZ hnorm hbind hfield

end D0.Analysis.MatchedBranchReturn
end
