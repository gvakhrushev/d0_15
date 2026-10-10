import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveSeamCurvature
import D0.Geometry.ArchiveRefinementHodgeWeights
import D0.Geometry.ArchiveMetricMeasureHodgeLift
import Mathlib.Algebra.BigOperators.Fin

/-! Research construction of the documented one-dimensional cochain maps.
The all-role tensor proof is in the companion note. No physical readout,
stationarity, or continuum recovery is assumed or concluded here. -/
open scoped BigOperators
namespace D0.Research.NativeCochainRefinement
noncomputable section

/-- Add a duplicate of vertex zero. Coarse size m+1, fine size m+2. -/
def B0 (m : ℕ) (f : Fin (m+1) → ℝ) : Fin (m+2) → ℝ :=
  Fin.lastCases (f 0) f

/-- Copy each old oriented edge, set the collapsed last edge to zero. -/
def B1 (m : ℕ) (f : Fin (m+1) → ℝ) : Fin (m+2) → ℝ :=
  Fin.lastCases 0 f

/-- Oriented cyclic incidence, including the wrap edge. -/
def incidence (m : ℕ) (f : Fin (m+1) → ℝ) : Fin (m+1) → ℝ :=
  Fin.lastCases (f 0 - f (Fin.last m))
    (fun j => f j.succ - f j.castSucc)

theorem b0_gram (m : ℕ) (f g : Fin (m+1) → ℝ) :
    (∑ i, B0 m f i * B0 m g i) = (∑ i, f i * g i) + f 0 * g 0 := by
  rw [Fin.sum_univ_castSucc]
  simp [B0]

theorem b1_isometry (m : ℕ) (f g : Fin (m+1) → ℝ) :
    (∑ i, B1 m f i * B1 m g i) = ∑ i, f i * g i := by
  rw [Fin.sum_univ_castSucc]
  simp [B1]

theorem incidence_chain (m : ℕ) (f : Fin (m+1) → ℝ) :
    incidence (m+1) (B0 m f) = B1 m (incidence m f) := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · have hz : Fin.lastCases (f 0) f (0 : Fin (m+2)) = f 0 := by
      change Fin.lastCases (f 0) f (0 : Fin (m+1)).castSucc = f 0
      simp only [Fin.lastCases_castSucc]
    simp only [incidence, B0, B1, Fin.lastCases_last]
    rw [hz]
    ring
  · refine Fin.lastCases ?_ (fun k => ?_) j
    · simp [incidence, B0, B1]
    · simp [incidence, B0, B1, Fin.succ_castSucc, -Fin.castSucc_succ]

theorem incidence_smul (m : ℕ) (c : ℝ) (f : Fin (m+1) → ℝ) :
    incidence m (fun i => c * f i) = fun i => c * incidence m f i := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i <;> simp [incidence, mul_sub]

/-- Literal owner scale after identifying L with N+2. -/
theorem owner_scale (N : ℕ) :
    D0.Geometry.forwardDifferenceScale N = (N+2 : ℝ) := by
  simp [D0.Geometry.forwardDifferenceScale, D0.archiveFibers]

/-- Bind the constructed vertex map to the actual frozen archive projection. -/
theorem b0_literal_projection (N : ℕ) (f : D0.archivePhaseIndex N → ℝ) :
    B0 (N+1) f = fun i => f (D0.archiveRGPhaseProjection N i) := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · have hp : D0.archiveRGPhaseProjection N (Fin.last (N+2)) = 0 := by
      apply Fin.ext
      simp [D0.archiveRGPhaseProjection, D0.archiveFibers]
    simp only [B0, Fin.lastCases_last, hp]
    rfl
  · have hp : D0.archiveRGPhaseProjection N j.castSucc = j := by
      apply Fin.ext
      exact Nat.mod_eq_of_lt j.isLt
    simp [B0, hp]

theorem b0_literal_matrix (N : ℕ) (f : D0.archivePhaseIndex N → ℝ) :
    B0 (N+1) f = (D0.archiveLiftOperator N).mulVec f := by
  rw [b0_literal_projection]
  funext i
  simp [D0.archiveLiftOperator, Matrix.mulVec, dotProduct]

theorem b1_smul (m : ℕ) (c : ℝ) (f : Fin (m+1) → ℝ) :
    B1 m (fun i => c * f i) = fun i => c * B1 m f i := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i <;> simp [B1]

/-- Degree-k normalization needed for the owner's L-scaled differential. -/
def scaleRatio (m : ℕ) : ℝ := (m+2 : ℝ) / (m+1 : ℝ)

theorem scaled_incidence_chain (m k : ℕ) (f : Fin (m+1) → ℝ) (i : Fin (m+2)) :
    (m+2 : ℝ) * incidence (m+1) (fun j => scaleRatio m ^ k * B0 m f j) i =
      scaleRatio m ^ (k+1) * B1 m (fun j => (m+1 : ℝ) * incidence m f j) i := by
  rw [incidence_smul, incidence_chain, b1_smul, pow_succ]
  have h : (m+1 : ℝ) ≠ 0 := by positivity
  simp only [scaleRatio]
  field_simp

/-- Equality of the oriented incidence energies, not Laplacian intertwinement. -/
theorem incidence_energy_pullback (m : ℕ) (f g : Fin (m+1) → ℝ) :
    (∑ i, incidence (m+1) (B0 m f) i * incidence (m+1) (B0 m g) i) =
      ∑ i, incidence m f i * incidence m g i := by
  rw [incidence_chain, incidence_chain, b1_isometry]

/-- All degrees in the literal metric-measure formula; no uniqueness claim. -/
theorem metric_measure_all_degrees {α : Type*} [DecidableEq α]
    (s : Finset α) (mu : ℝ) (mass : α → ℝ) (hmu : mu ≠ 0) :
    D0.Geometry.hodgeMetricMeasureWeight s.card mu (∏ r ∈ s, mu / mass r) =
      mu / (∏ r ∈ s, mass r) := by
  rw [Finset.prod_div_distrib, Finset.prod_const]
  unfold D0.Geometry.hodgeMetricMeasureWeight D0.Geometry.muExponent
  have hh : mu ^ (1 - (s.card : ℤ)) * mu ^ s.card = mu := by
    rw [← zpow_natCast, ← zpow_add₀ hmu]
    simp
  rw [← mul_div_assoc, hh]

theorem metric_measure_refinement_weight {α : Type*} [Fintype α] [DecidableEq α]
    (s : Finset α) (mass : α → ℝ) (hmass : ∀ r, mass r ≠ 0) :
    D0.Geometry.hodgeMetricMeasureWeight s.card (∏ r, mass r)
        (∏ r ∈ s, (∏ t, mass t) / mass r) =
      ∏ r ∈ Finset.univ \ s, mass r := by
  have hall : (∏ r, mass r) ≠ 0 := Finset.prod_ne_zero_iff.mpr (by
    intro r _
    exact hmass r)
  have hs : (∏ r ∈ s, mass r) ≠ 0 := Finset.prod_ne_zero_iff.mpr (by
    intro r _
    exact hmass r)
  rw [metric_measure_all_degrees s _ _ hall]
  apply (div_eq_iff hs).mpr
  exact (Finset.prod_sdiff (Finset.subset_univ s)).symm

#print axioms b0_gram
#print axioms b1_isometry
#print axioms incidence_chain
#print axioms incidence_smul
#print axioms owner_scale
#print axioms b0_literal_projection
#print axioms b0_literal_matrix
#print axioms b1_smul
#print axioms scaled_incidence_chain
#print axioms incidence_energy_pullback
#print axioms metric_measure_all_degrees
#print axioms metric_measure_refinement_weight
end
end D0.Research.NativeCochainRefinement
