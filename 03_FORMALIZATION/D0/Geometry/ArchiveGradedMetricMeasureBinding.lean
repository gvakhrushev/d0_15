import D0.Geometry.ArchiveGradedCochainGramTrace
import D0.Geometry.ArchiveMetricMeasureHodgeLift

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-! This is an algebraic interpretation of the proven counting Gram weights.
It does not select a physical metric or constitutive law. -/

/-- The repeated-zero mass on each actual coarse group coordinate. -/
def archiveRoleMass (N : ℕ) (x : ArchiveRolePhaseGroup N) (r : Role) : ℝ :=
  if x r = 0 then 2 else 1

/-- Product measure of the four role masses. -/
def archiveRoleMeasure (N : ℕ) (x : ArchiveRolePhaseGroup N) : ℝ :=
  ∏ r : Role, archiveRoleMass N x r

/-- Occupied directions of the actual Fock state. -/
def archiveOccupiedRoles (S : ArchiveFockState) : Finset Role :=
  Finset.univ.filter (fun r => S r = true)

/-- The conductance selected for this algebraic identity includes the
degree-correction factor of the literal cochain pullback. -/
def archiveRoleConductance (N : ℕ) (x : ArchiveRolePhaseGroup N) (r : Role) : ℝ :=
  archiveCochainScaleRatio (N + 1) ^ 2 * (archiveRoleMeasure N x / archiveRoleMass N x r)

theorem archive_role_mass_pos (N : ℕ) (x : ArchiveRolePhaseGroup N) (r : Role) :
    0 < archiveRoleMass N x r := by
  unfold archiveRoleMass
  split <;> norm_num

theorem archive_role_measure_pos (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    0 < archiveRoleMeasure N x := by
  unfold archiveRoleMeasure
  exact Finset.prod_pos (fun r _ => archive_role_mass_pos N x r)

theorem archive_role_mass_ne_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) (r : Role) :
    archiveRoleMass N x r ≠ 0 := ne_of_gt (archive_role_mass_pos N x r)

theorem archive_role_measure_ne_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    archiveRoleMeasure N x ≠ 0 := ne_of_gt (archive_role_measure_pos N x)

/-- All-degree algebraic identity from the preserved refinement capsule. -/
theorem archive_metric_measure_all_degrees {α : Type*} [DecidableEq α]
    (s : Finset α) (mu : ℝ) (mass : α → ℝ) (hmu : mu ≠ 0) :
    hodgeMetricMeasureWeight s.card mu (∏ r ∈ s, mu / mass r) =
      mu / (∏ r ∈ s, mass r) := by
  rw [Finset.prod_div_distrib, Finset.prod_const]
  unfold hodgeMetricMeasureWeight muExponent
  have hh : mu ^ (1 - (s.card : ℤ)) * mu ^ s.card = mu := by
    rw [← zpow_natCast, ← zpow_add₀ hmu]
    simp
  rw [← mul_div_assoc, hh]

/-- Product-measure specialization, retaining every unoccupied role. -/
theorem archive_metric_measure_refinement_weight {α : Type*} [Fintype α] [DecidableEq α]
    (s : Finset α) (mass : α → ℝ) (hmass : ∀ r, mass r ≠ 0) :
    hodgeMetricMeasureWeight s.card (∏ r, mass r)
        (∏ r ∈ s, (∏ t, mass t) / mass r) =
      ∏ r ∈ Finset.univ \ s, mass r := by
  have hall : (∏ r, mass r) ≠ 0 := Finset.prod_ne_zero_iff.mpr (by
    intro r _
    exact hmass r)
  have hs : (∏ r ∈ s, mass r) ≠ 0 := Finset.prod_ne_zero_iff.mpr (by
    intro r _
    exact hmass r)
  rw [archive_metric_measure_all_degrees s _ _ hall]
  apply (div_eq_iff hs).mpr
  exact (Finset.prod_sdiff (Finset.subset_univ s)).symm

/-- Without nonzero masses, the generic identity fails even on one role:
Lean's real division has `0 / 0 = 0`, while the empty product is one. -/
theorem archive_metric_measure_zero_mass_counterexample :
    hodgeMetricMeasureWeight (Finset.univ : Finset Unit).card
        (∏ _ : Unit, (0 : ℝ))
        (∏ _ ∈ (Finset.univ : Finset Unit), (∏ _ : Unit, (0 : ℝ)) / (0 : ℝ)) ≠
      ∏ _ ∈ (Finset.univ : Finset Unit) \ Finset.univ, (0 : ℝ) := by
  norm_num [hodgeMetricMeasureWeight, muExponent]

/-- The specified metric-measure expression is exactly the counting Gram
weight, including its degree-dependent refinement scale. -/
theorem archive_graded_metric_measure_weight (N : ℕ) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) :
    hodgeMetricMeasureWeight (fockDegree S) (archiveRoleMeasure N x)
      (∏ r ∈ archiveOccupiedRoles S, archiveRoleConductance N x r) =
        archiveGradedGramWeight N x S := by
  classical
  have hcard : (archiveOccupiedRoles S).card = fockDegree S := rfl
  have hbase := archive_metric_measure_refinement_weight (archiveOccupiedRoles S)
    (archiveRoleMass N x) (archive_role_mass_ne_zero N x)
  change hodgeMetricMeasureWeight (archiveOccupiedRoles S).card (archiveRoleMeasure N x)
    (∏ r ∈ archiveOccupiedRoles S, archiveRoleMeasure N x / archiveRoleMass N x r) = _ at hbase
  unfold archiveRoleConductance
  rw [Finset.prod_mul_distrib, Finset.prod_const, hcard]
  unfold hodgeMetricMeasureWeight at hbase ⊢
  rw [hcard] at hbase
  rw [archiveGradedGramWeight]
  have hfilter : Finset.univ \ archiveOccupiedRoles S =
      Finset.univ.filter (fun r : Role => S r = false) := by
    ext r
    simp only [Finset.mem_sdiff, Finset.mem_univ, true_and, Finset.mem_filter,
      archiveOccupiedRoles]
    cases S r <;> simp
  have hp : (∏ r : Role, archiveGramCoordinateWeight (S r) (x r)) =
      ∏ r ∈ Finset.univ \ archiveOccupiedRoles S, archiveRoleMass N x r := by
    rw [hfilter]
    simp [archiveGramCoordinateWeight, archiveRoleMass, Finset.prod_ite]
  rw [hp]
  rw [pow_mul]
  calc
    _ = (archiveCochainScaleRatio (N + 1) ^ 2) ^ fockDegree S *
        (archiveRoleMeasure N x ^ muExponent (fockDegree S) *
          ∏ r ∈ archiveOccupiedRoles S, archiveRoleMeasure N x / archiveRoleMass N x r) := by ring
    _ = _ := by rw [hbase]

/-- Literal diagonal of the actual refinement Gram matrix, not an abstract
or independently stipulated weight. -/
theorem archive_graded_metric_measure_gram_diagonal (N : ℕ)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    ((archiveGradedPullbackMatrix N).transpose * archiveGradedPullbackMatrix N) (x, S) (x, S) =
      hodgeMetricMeasureWeight (fockDegree S) (archiveRoleMeasure N x)
        (∏ r ∈ archiveOccupiedRoles S, archiveRoleConductance N x r) := by
  rw [archive_graded_matrix_gram]
  simp only [Matrix.diagonal_apply_eq]
  exact (archive_graded_metric_measure_weight N x S).symm

end
end D0.Geometry
