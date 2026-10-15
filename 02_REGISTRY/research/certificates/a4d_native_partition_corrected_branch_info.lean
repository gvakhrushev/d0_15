import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Tactic

/-!
The branch-information cocycle is the complete action information only when
the native path weights are already normalized.  For the Book III partition
weight, the exact correction is log_phi Z, with its genuine field derivative.
This capsule proves the algebraic boundary; it does not assert that Z=1 for
the physical D0 histories.
-/

open Real
open Filter
open scoped goldenRatio
open scoped Topology

namespace D0.Research.NativePartitionCorrectedBranchInfo

noncomputable def codeCost (mu : ℝ) : ℝ := -Real.log mu / Real.log φ

noncomputable def pathAction (w : ℝ) : ℝ := -Real.log w / Real.log φ

noncomputable def bookInfo (mu w : ℝ) : ℝ := codeCost mu - pathAction w

noncomputable def normalizedLikelihoodInfo (mu q Z : ℝ) : ℝ :=
  (Real.log (q / mu) + Real.log Z) / Real.log φ

noncomputable def unnormalizedLikelihoodInfo (mu q : ℝ) : ℝ :=
  Real.log (q / mu) / Real.log φ

noncomputable def partition (ι : Type*) [Fintype ι] (w : ι → ℝ) : ℝ :=
  ∑ i, w i

noncomputable def normalizedWeight {ι : Type*} [Fintype ι]
    (w : ι → ℝ) (i : ι) : ℝ := w i / partition ι w

noncomputable def normalizedEntropy {ι : Type*} [Fintype ι]
    (q : ι → ℝ) : ℝ :=
  -(∑ i, q i * Real.log (q i)) / Real.log φ

noncomputable def expectedPathAction {ι : Type*} [Fintype ι]
    (q w : ι → ℝ) : ℝ :=
  ∑ i, q i * pathAction (w i)

theorem log_phi_pos : 0 < Real.log φ := Real.log_pos Real.one_lt_goldenRatio

/-- Normalization is by the full finite partition, with no omitted outcomes. -/
theorem partition_pos {ι : Type*} [Fintype ι] [Nonempty ι]
    (w : ι → ℝ) (hw : ∀ i, 0 < w i) : 0 < partition ι w := by
  unfold partition
  exact Finset.sum_pos (fun i _ => hw i) Finset.univ_nonempty

theorem normalizedWeight_sum_one {ι : Type*} [Fintype ι] [Nonempty ι]
    (w : ι → ℝ) (hw : ∀ i, 0 < w i) :
    ∑ i, normalizedWeight w i = 1 := by
  have hZ := partition_pos w hw
  unfold normalizedWeight
  rw [← Finset.sum_div]
  exact div_self (ne_of_gt hZ)

/-- The exact partition correction to the pathwise code-minus-information
identity. If q=w/Z, then I = log_phi(q/mu) + log_phi(Z). -/
theorem bookInfo_partition_identity
    (mu q Z : ℝ) (hmu : 0 < mu) (hq : 0 < q) (hZ : 0 < Z) :
    bookInfo mu (q * Z) = normalizedLikelihoodInfo mu q Z := by
  unfold bookInfo codeCost pathAction normalizedLikelihoodInfo
  rw [Real.log_mul (ne_of_gt hq) (ne_of_gt hZ)]
  rw [Real.log_div (ne_of_gt hq) (ne_of_gt hmu)]
  ring

/-- Binding the abstract correction formula to the actual finite partition:
the normalized Born weight and the raw path weight obey w=q*Z exactly. -/
theorem bookInfo_normalizedWeight_identity
    {ι : Type*} [Fintype ι] [Nonempty ι]
    (w : ι → ℝ) (hw : ∀ j, 0 < w j) (mu : ℝ) (hmu : 0 < mu) (i : ι) :
    bookInfo mu (w i) =
      normalizedLikelihoodInfo mu (normalizedWeight w i) (partition ι w) := by
  have hZ := partition_pos w hw
  have hq : 0 < normalizedWeight w i := div_pos (hw i) hZ
  have hfactor : normalizedWeight w i * partition ι w = w i := by
    unfold normalizedWeight
    exact div_mul_cancel₀ (w i) (ne_of_gt hZ)
  rw [← hfactor]
  exact bookInfo_partition_identity mu (normalizedWeight w i)
    (partition ι w) hmu hq hZ

/-- The normalized expectation of the raw path action is entropy minus the
logarithm of the scalar partition. The partition term cannot be dropped from
the source merely because the probabilities sum to one. -/
theorem expectedPathAction_partition_identity
    {ι : Type*} [Fintype ι] (q : ι → ℝ) (Z : ℝ)
    (hq : ∀ i, 0 < q i) (hZ : 0 < Z)
    (hsum : ∑ i, q i = 1) :
    expectedPathAction q (fun i => q i * Z) =
      normalizedEntropy q - Real.log Z / Real.log φ := by
  unfold expectedPathAction pathAction normalizedEntropy
  have hlog (i) : Real.log (q i * Z) = Real.log (q i) + Real.log Z :=
    Real.log_mul (ne_of_gt (hq i)) (ne_of_gt hZ)
  simp_rw [hlog]
  have hsplit (i) :
      q i * (-(Real.log (q i) + Real.log Z) / Real.log φ) =
        -(q i * Real.log (q i)) / Real.log φ -
          (q i * Real.log Z) / Real.log φ := by ring
  simp_rw [hsplit]
  rw [Finset.sum_sub_distrib]
  have hfirst :
      (∑ i, -(q i * Real.log (q i)) / Real.log φ) =
        -(∑ i, q i * Real.log (q i)) / Real.log φ := by
    rw [← Finset.sum_div, Finset.sum_neg_distrib]
  have hsecond :
      (∑ i, (q i * Real.log Z) / Real.log φ) = Real.log Z / Real.log φ := by
    rw [← Finset.sum_div]
    calc
      (∑ i, q i * Real.log Z) / Real.log φ =
          ((∑ i, q i) * Real.log Z) / Real.log φ := by rw [Finset.sum_mul]
      _ = Real.log Z / Real.log φ := by rw [hsum]; ring
  rw [hfirst, hsecond]

/-- At a normalized base point Z=1, the value agrees with the uncorrected
likelihood cocycle. This does not imply that its derivative is unchanged. -/
theorem normalized_base_value
    (mu q : ℝ) :
    normalizedLikelihoodInfo mu q 1 = Real.log (q / mu) / Real.log φ := by
  simp [normalizedLikelihoodInfo]

/-- The partition correction is a common additive shift across outcomes. -/
theorem normalizedLikelihoodInfo_common_shift
    (mu q Z : ℝ) :
    normalizedLikelihoodInfo mu q Z =
      unnormalizedLikelihoodInfo mu q + Real.log Z / Real.log φ := by
  unfold normalizedLikelihoodInfo unnormalizedLikelihoodInfo
  ring

/-- Every zero-sum linear contrast of branch information annihilates the
common partition correction. This does not identify the physical source with
such a contrast. -/
theorem balanced_contrast_kills_partition_correction
    {ι : Type*} [Fintype ι] (c q : ι → ℝ) (mu Z : ℝ)
    (hbalanced : ∑ i, c i = 0) :
    ∑ i, c i *
      (normalizedLikelihoodInfo mu (q i) Z -
        unnormalizedLikelihoodInfo mu (q i)) = 0 := by
  have hshift : ∀ i,
      normalizedLikelihoodInfo mu (q i) Z -
        unnormalizedLikelihoodInfo mu (q i) = Real.log Z / Real.log φ := by
    intro i
    rw [normalizedLikelihoodInfo_common_shift]
    ring
  simp_rw [hshift]
  rw [← Finset.sum_mul, hbalanced]
  simp

/-- The full joint first variation contains both the measured likelihood jet
and the partition jet. -/
theorem normalizedLikelihoodInfo_hasDerivAt
    (mu : ℝ) (q Z : ℝ → ℝ) (dq dZ t : ℝ)
    (hmu : 0 < mu) (hq : 0 < q t) (hZ : 0 < Z t)
    (hqd : HasDerivAt q dq t) (hZd : HasDerivAt Z dZ t) :
    HasDerivAt (fun s => normalizedLikelihoodInfo mu (q s) (Z s))
      ((dq / q t + dZ / Z t) / Real.log φ) t := by
  have hlogq : HasDerivAt (fun s => Real.log (q s / mu))
      ((dq / mu) / (q t / mu)) t := by
    exact (hqd.div_const mu).log (ne_of_gt (div_pos hq hmu))
  have hlogZ : HasDerivAt (fun s => Real.log (Z s)) (dZ / Z t) t :=
    hZd.log (ne_of_gt hZ)
  have hsum := hlogq.add hlogZ
  have hscale := hsum.div_const (Real.log φ)
  have hderiv : (dq / mu) / (q t / mu) = dq / q t := by
    field_simp [ne_of_gt hmu, ne_of_gt hq]
  simpa [normalizedLikelihoodInfo, hderiv] using hscale

/-- Differentiate the expected path action along a normalized outcome family.
The complete source is the entropy derivative minus the genuine partition
jet, including when the base partition equals one. -/
theorem expectedPathAction_hasDerivAt
    {ι : Type*} [Fintype ι]
    (q : ι → ℝ → ℝ) (Z : ℝ → ℝ) (dH dZ t : ℝ)
    (hZ : 0 < Z t)
    (hqEventually : ∀ᶠ s in 𝓝 t, ∀ i, 0 < q i s)
    (hZEventually : ∀ᶠ s in 𝓝 t, 0 < Z s)
    (hsumEventually : ∀ᶠ s in 𝓝 t, ∑ i, q i s = 1)
    (hH : HasDerivAt (fun s => normalizedEntropy (fun i => q i s)) dH t)
    (hZd : HasDerivAt Z dZ t) :
    HasDerivAt
      (fun s => expectedPathAction (fun i => q i s) (fun i => q i s * Z s))
      (dH - (dZ / Z t) / Real.log φ) t := by
  have hlog : HasDerivAt (fun s => Real.log (Z s) / Real.log φ)
      ((dZ / Z t) / Real.log φ) t := by
    exact (hZd.log (ne_of_gt hZ)).div_const (Real.log φ)
  have hderiv := hH.sub hlog
  have hEq :
      (fun s => expectedPathAction (fun i => q i s) (fun i => q i s * Z s)) =ᶠ[𝓝 t]
      (fun s => normalizedEntropy (fun i => q i s) - Real.log (Z s) / Real.log φ) := by
    filter_upwards [hqEventually, hZEventually, hsumEventually] with s hq hZs hsum
    exact expectedPathAction_partition_identity (fun i => q i s) (Z s) hq hZs hsum
  simpa only [sub_eq_add_neg] using hderiv.congr_of_eventuallyEq hEq

#check partition_pos
#check normalizedWeight_sum_one
#check bookInfo_normalizedWeight_identity
#check bookInfo_partition_identity
#check expectedPathAction_partition_identity
#check normalized_base_value
#check normalizedLikelihoodInfo_common_shift
#check balanced_contrast_kills_partition_correction
#check normalizedLikelihoodInfo_hasDerivAt
#check expectedPathAction_hasDerivAt
#print axioms partition_pos
#print axioms normalizedWeight_sum_one
#print axioms bookInfo_normalizedWeight_identity
#print axioms bookInfo_partition_identity
#print axioms expectedPathAction_partition_identity
#print axioms normalized_base_value
#print axioms normalizedLikelihoodInfo_common_shift
#print axioms balanced_contrast_kills_partition_correction
#print axioms normalizedLikelihoodInfo_hasDerivAt
#print axioms expectedPathAction_hasDerivAt

end D0.Research.NativePartitionCorrectedBranchInfo
