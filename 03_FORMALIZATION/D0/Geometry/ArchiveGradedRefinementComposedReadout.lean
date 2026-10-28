import D0.Geometry.ArchiveGradedCochainRefinement

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-!
The literal adjacent graded pullbacks are iterated here without replacing
them by a direct modulo map. The constant singleton component is a fixed
coordinate readout probe; no physical refinement is asserted.
-/

/-- Compose exactly `t` consecutive owned adjacent graded pullbacks. -/
def archiveRepeatedGradedPullback (N : ℕ) (ψ : ArchiveCochain N) :
    (t : ℕ) → ArchiveCochain (N + t)
  | 0 => ψ
  | t + 1 => archiveGradedCochainPullback (N + t)
      (archiveRepeatedGradedPullback N ψ t)

/-- A constant unit component in the literal singleton Fock sector. -/
def archiveUnitSingletonCochain (N : ℕ) (r : Role) : ArchiveCochain N :=
  fun p => if p.2 = singletonFockState r then 1 else 0

theorem archive_singleton_degree_one (r : Role) :
    fockDegree (singletonFockState r) = 1 := by
  classical
  unfold fockDegree singletonFockState fockSingletonState
  have h : Finset.univ.filter (fun s : Role => (if s = r then true else false) = true) = {r} := by
    ext s
    simp
  rw [h]
  simp

theorem archive_singleton_occupancy_mask (r : Role) (allowed : Role → Bool) :
    archiveOccupancyMask (singletonFockState r) allowed =
      (if allowed r = true then 1 else 0) := by
  classical
  by_cases h : allowed r = true
  · have hh : ∀ s : Role, singletonFockState r s = true → allowed s = true := by
      intro s hs
      have hs' : s = r := by simpa [singletonFockState, fockSingletonState] using hs
      simpa [hs'] using h
    simp only [archiveOccupancyMask, if_pos hh, if_pos h]
  · have hh : ¬ (∀ s : Role, singletonFockState r s = true → allowed s = true) := by
      intro ha
      apply h
      exact ha r (by simp [singletonFockState, fockSingletonState])
    simp only [archiveOccupancyMask, if_neg hh, if_neg h]

/-- One adjacent pullback acts on a singleton through its actual edge mask. -/
theorem archive_singleton_pullback_component (N : ℕ) (ψ : ArchiveCochain N)
    (r : Role) (y : ArchiveRolePhaseGroup (N + 1)) :
    archiveGradedCochainPullback N ψ (y, singletonFockState r) =
      (if (archiveFineRoleIndex N r y).val < N + 2 then
        archiveCochainScaleRatio (N + 1) *
          ψ (archiveRoleGroupProjection N y, singletonFockState r)
       else 0) := by
  classical
  simp [archiveGradedCochainPullback, archive_singleton_degree_one,
    archive_singleton_occupancy_mask, archiveRefinementAllowed]

/-- Repeated neighboring maps preserve the original edge prefix and set all
new edges to zero, with telescoping scale `(L+t)/L`, where `L=N+2`. -/
theorem archive_repeated_singleton_component (N t : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + t)) :
    archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) t
        (y, singletonFockState r) =
      (if ((finZModEquiv (N + t)).symm (y r)).val < N + 2 then
        ((N + t + 2 : ℝ) / (N + 2 : ℝ)) else 0) := by
  classical
  induction t with
  | zero =>
      have hi := ((finZModEquiv N).symm (y r)).isLt
      simp only [archivePhaseIndex, archiveFibers] at hi
      simp only [archiveRepeatedGradedPullback, archiveUnitSingletonCochain, Nat.add_zero]
      simp only [if_true, Nat.cast_zero, add_zero]
      split_ifs with hz
      · have hn : (N + 2 : ℝ) ≠ 0 := by positivity
        exact (div_self hn).symm
      · exact (hz hi).elim
  | succ t ih =>
      rw [archiveRepeatedGradedPullback, archive_singleton_pullback_component]
      let i := archiveFineRoleIndex (N + t) r y
      have hidx : ((finZModEquiv (N + t)).symm
          (archiveRoleGroupProjection (N + t) y r)).val = i.val % (N + t + 2) := by
        rw [archive_group_projection_role_index]
        rfl
      change (if i.val < N + t + 2 then
        archiveCochainScaleRatio (N + t + 1) *
          archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) t
            (archiveRoleGroupProjection (N + t) y, singletonFockState r) else 0) =
        (if i.val < N + 2 then (((N : ℝ) + ((t + 1 : ℕ) : ℝ) + 2) / (N + 2 : ℝ)) else 0)
      have hbound : i.val < N + t + 3 := by
        have h := i.isLt
        simpa [i, archivePhaseIndex, archiveFibers, Nat.add_assoc] using h
      by_cases h : i.val < N + t + 2
      · have hmod : i.val % (N + t + 2) = i.val := Nat.mod_eq_of_lt h
        have hp : ((finZModEquiv (N + t)).symm
            (archiveRoleGroupProjection (N + t) y r)).val = i.val := by
          rw [hidx, hmod]
        rw [if_pos h, ih, hp]
        by_cases hbase : i.val < N + 2
        · rw [if_pos hbase, if_pos hbase]
          unfold archiveCochainScaleRatio
          have hn : (N + 2 : ℝ) ≠ 0 := by positivity
          have hm : (N + t + 2 : ℝ) ≠ 0 := by positivity
          push_cast
          field_simp
          ring
        · simp [hbase]
      · have hbase : ¬ i.val < N + 2 := by omega
        simp [h, hbase]

/-- The probe is exactly the owned one-form embedding of a constant unit
coefficient in role `r`, rather than an unrelated label-level witness. -/
theorem archive_unit_singleton_eq_oneFormCochain (N : ℕ) (r : Role) :
    archiveUnitSingletonCochain N r =
      oneFormCochain N (fun _ s => if s = r then 1 else 0) := by
  classical
  funext p
  unfold archiveUnitSingletonCochain oneFormCochain
  rw [Finset.sum_eq_single r]
  · simp
  · intro s hs hsr
    simp [hsr]
  · simp

/-- The chain identity composes along the literal adjacent pullbacks. -/
theorem archive_repeated_graded_chain (N t : ℕ) (ψ : ArchiveCochain N) :
    dForward (N + t) (archiveRepeatedGradedPullback N ψ t) =
      archiveRepeatedGradedPullback N (dForward N ψ) t := by
  induction t with
  | zero => rfl
  | succ t ih =>
      change dForward ((N + t) + 1)
          (archiveGradedCochainPullback (N + t) (archiveRepeatedGradedPullback N ψ t)) =
        archiveGradedCochainPullback (N + t)
          (archiveRepeatedGradedPullback N (dForward N ψ) t)
      rw [archive_graded_cochain_chain, ih]

/-- At size doubling the literal singleton component is two on the original
prefix and zero on the newly appended tail. -/
theorem archive_doubling_singleton_component (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + (N + 2))) :
    oneFormComponent (N + (N + 2))
      (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r y =
      (if ((finZModEquiv (N + (N + 2))).symm (y r)).val < N + 2 then 2 else 0) := by
  rw [oneFormComponent, archive_repeated_singleton_component]
  have h : (((N : ℝ) + ((N + 2 : ℕ) : ℝ) + 2) / (N + 2 : ℝ)) = 2 := by
    have hn : (N + 2 : ℝ) ≠ 0 := by positivity
    push_cast
    field_simp
    ring
  rw [h]

/-- The error is measured against the constant component 1 at every fine site.
This specifies a fixed-component readout probe, without physical selection. -/
def archiveSingletonComponentError (N : ℕ) (ψ : ArchiveCochain N)
    (r : Role) (y : ArchiveRolePhaseGroup N) : ℝ :=
  oneFormComponent N ψ r y - 1

/-- The absolute readout error is exactly one at every doubled fine site. -/
theorem archive_doubling_singleton_abs_error (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + (N + 2))) :
    |archiveSingletonComponentError (N + (N + 2))
      (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r y| = 1 := by
  unfold archiveSingletonComponentError
  rw [archive_doubling_singleton_component]
  split_ifs <;> norm_num

/-- The squared readout error is exactly one at every doubled fine site. -/
theorem archive_doubling_singleton_sq_error (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + (N + 2))) :
    (archiveSingletonComponentError (N + (N + 2))
      (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r y) ^ 2 = 1 := by
  unfold archiveSingletonComponentError
  rw [archive_doubling_singleton_component]
  split_ifs <;> norm_num

/-- Mean absolute error under normalized counting measure on the actual
four-role site carrier. -/
def archiveNormalizedSingletonL1 (N : ℕ) (ψ : ArchiveCochain N) (r : Role) : ℝ :=
  (∑ y : ArchiveRolePhaseGroup N, |archiveSingletonComponentError N ψ r y|) /
    (Fintype.card (ArchiveRolePhaseGroup N) : ℝ)

/-- Mean squared error under the same normalized counting measure. -/
def archiveNormalizedSingletonL2Squared (N : ℕ) (ψ : ArchiveCochain N) (r : Role) : ℝ :=
  (∑ y : ArchiveRolePhaseGroup N, (archiveSingletonComponentError N ψ r y) ^ 2) /
    (Fintype.card (ArchiveRolePhaseGroup N) : ℝ)

/-- Both fixed-component normalized errors remain exactly one at every
size-doubling, although every adjacent map is a cochain chain map. -/
theorem archive_doubling_fixed_component_errors (N : ℕ) (r : Role) :
    archiveNormalizedSingletonL1 (N + (N + 2))
        (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r = 1 ∧
    archiveNormalizedSingletonL2Squared (N + (N + 2))
        (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r = 1 := by
  have hn : (Fintype.card (ArchiveRolePhaseGroup (N + (N + 2))) : ℝ) ≠ 0 := by
    have hp : 0 < Fintype.card (ArchiveRolePhaseGroup (N + (N + 2))) :=
      Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast (ne_of_gt hp)
  constructor
  · unfold archiveNormalizedSingletonL1
    simp_rw [archive_doubling_singleton_abs_error]
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    exact div_self hn
  · unfold archiveNormalizedSingletonL2Squared
    simp_rw [archive_doubling_singleton_sq_error]
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    exact div_self hn

end
end D0.Geometry
