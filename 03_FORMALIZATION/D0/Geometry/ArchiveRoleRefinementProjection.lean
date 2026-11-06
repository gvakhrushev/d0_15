import D0.Geometry.ArchiveRolePhaseCarrier
import D0.Geometry.Archive1DCochainRefinementBinding

namespace D0.Geometry

open D0
noncomputable section

/-- The literal role-product projection, transported to the cyclic group carrier. -/
def archiveRoleGroupProjection (N : ℕ) (y : ArchiveRolePhaseGroup (N + 1)) :
    ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N
    (archiveRolePhaseProjection N ((archiveRolePhasePointGroupEquiv (N + 1)).symm y))

/-- The fine phase index at the selected role. -/
def archiveFineRoleIndex (N : ℕ) (r : Role) (y : ArchiveRolePhaseGroup (N + 1)) :
    archivePhaseIndex (N + 1) := (finZModEquiv (N + 1)).symm (y r)

/-- A scalar field restricted to a role line through a coarse group point. -/
def archiveRoleSlice (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N)
    (f : ArchiveRolePhaseGroup N → ℝ) : archivePhaseIndex N → ℝ :=
  fun j => f (Function.update x r (finZModEquiv N j))

theorem archive_group_projection_update (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (i : archivePhaseIndex (N + 1)) :
    archiveRoleGroupProjection N (Function.update y r (finZModEquiv (N + 1) i)) =
      Function.update (archiveRoleGroupProjection N y) r
        (finZModEquiv N (archiveRGPhaseProjection N i)) := by
  classical
  funext s
  by_cases h : s = r
  · subst s
    simp [archiveRoleGroupProjection, archiveRolePhasePointGroupEquiv,
      archiveRolePhaseProjection]
  · simp [archiveRoleGroupProjection, archiveRolePhasePointGroupEquiv,
      archiveRolePhaseProjection, h]

theorem archive_role_slice_projection (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ) :
    archiveRoleSlice (N + 1) r y (fun z => f (archiveRoleGroupProjection N z)) =
      archiveCochainB0 (N + 1) (archiveRoleSlice N r (archiveRoleGroupProjection N y) f) := by
  rw [archive_b0_literal_projection]
  funext i
  simp [archiveRoleSlice, archive_group_projection_update]

theorem archive_incidence_add_one (m : ℕ) (f : Fin (m + 1) → ℝ)
    (i : Fin (m + 1)) :
    archiveCycleIncidence m f i = f (i + 1) - f i := by
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [archiveCycleIncidence, Fin.last_add_one]
  · simp [archiveCycleIncidence]

theorem archive_role_slice_incidence (N : ℕ) (r : Role)
    (x : ArchiveRolePhaseGroup N) (f : ArchiveRolePhaseGroup N → ℝ) :
    archiveCycleIncidence (N + 1) (archiveRoleSlice N r x f)
        ((finZModEquiv N).symm (x r)) =
      f (roleTranslatePlus N r x) - f x := by
  classical
  rw [archive_incidence_add_one]
  have h : Function.update x r
      (finZModEquiv N ((finZModEquiv N).symm (x r) + 1)) =
      roleTranslatePlus N r x := by
    funext s
    by_cases hs : s = r
    · subst s
      simp [roleTranslatePlus_apply, roleStep, finZModEquiv, ZMod.finEquiv]
    · simp [roleTranslatePlus_apply, roleStep, hs]
  simp only [archiveRoleSlice, Equiv.apply_symm_apply, Function.update_eq_self]
  exact congrArg (fun z => f z - f x) h

/-- Scalar-to-singleton application of the 1D degree-corrected chain block.
The `B1` edge map keeps every original edge (including wrap) and sends the
new final edge to zero. This is not a full four-dimensional chain map. -/
theorem archive_scalar_singleton_refinement (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ) :
    oneFormComponent (N + 1)
        (dForward (N + 1) (scalarCochain (N + 1)
          (fun z => f (archiveRoleGroupProjection N z)))) r y =
      archiveCochainScaleRatio (N + 1) *
        archiveCochainB1 (N + 1)
          (fun j => forwardDifferenceScale N *
            archiveCycleIncidence (N + 1)
              (archiveRoleSlice N r (archiveRoleGroupProjection N y) f) j)
          (archiveFineRoleIndex N r y) := by
  rw [dForward_scalar_oneForm_component, forwardDifference_apply]
  have h := archive_scaled_block_with_owner_scale N 0
    (archiveRoleSlice N r (archiveRoleGroupProjection N y) f)
    (archiveFineRoleIndex N r y)
  simp only [pow_zero, one_mul, zero_add, pow_one] at h
  rw [← archive_role_slice_projection] at h
  change forwardDifferenceScale (N + 1) *
    archiveCycleIncidence (N + 2)
      (archiveRoleSlice (N + 1) r y (fun z => f (archiveRoleGroupProjection N z)))
      ((finZModEquiv (N + 1)).symm (y r)) = _ at h
  rw [archive_role_slice_incidence] at h
  exact h

/-- The final fine edge is collapsed by the actual group projection. -/
theorem archive_scalar_singleton_collapsed (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ)
    (h : archiveFineRoleIndex N r y = Fin.last (N + 2)) :
    oneFormComponent (N + 1)
      (dForward (N + 1) (scalarCochain (N + 1)
        (fun z => f (archiveRoleGroupProjection N z)))) r y = 0 := by
  rw [archive_scalar_singleton_refinement, h]
  simp [archiveCochainB1]

/-- Every old edge survives, including the old wrap edge. -/
theorem archive_scalar_singleton_old_edge (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ)
    (j : archivePhaseIndex N) (h : archiveFineRoleIndex N r y = j.castSucc) :
    oneFormComponent (N + 1)
      (dForward (N + 1) (scalarCochain (N + 1)
        (fun z => f (archiveRoleGroupProjection N z)))) r y =
      archiveCochainScaleRatio (N + 1) * (forwardDifferenceScale N *
        archiveCycleIncidence (N + 1)
          (archiveRoleSlice N r (archiveRoleGroupProjection N y) f) j) := by
  rw [archive_scalar_singleton_refinement, h]
  apply congrArg (fun z : ℝ => archiveCochainScaleRatio (N + 1) * z)
  change Fin.lastCases (motive := fun _ : Fin ((N + 1) + 2) => ℝ) 0
    (fun i : Fin ((N + 1) + 1) => forwardDifferenceScale N *
      archiveCycleIncidence (N + 1)
        (archiveRoleSlice N r (archiveRoleGroupProjection N y) f) i)
    ((show Fin ((N + 1) + 1) from j).castSucc) = _
  rw [Fin.lastCases_castSucc]

/-- The old wrap edge is copied, rather than mistaken for the collapsed edge. -/
theorem archive_scalar_singleton_wrap (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ)
    (h : archiveFineRoleIndex N r y = (Fin.last (N + 1)).castSucc) :
    oneFormComponent (N + 1)
      (dForward (N + 1) (scalarCochain (N + 1)
        (fun z => f (archiveRoleGroupProjection N z)))) r y =
      archiveCochainScaleRatio (N + 1) * (forwardDifferenceScale N *
        (archiveRoleSlice N r (archiveRoleGroupProjection N y) f 0 -
         archiveRoleSlice N r (archiveRoleGroupProjection N y) f (Fin.last (N + 1)))) := by
  rw [archive_scalar_singleton_old_edge N r y f (Fin.last (N + 1)) h]
  rw [archiveCycleIncidence, Fin.lastCases_last]
  rfl

/-- Explicit adjacent-level normalization. -/
theorem archive_role_refinement_scale (N : ℕ) :
    archiveCochainScaleRatio (N + 1) = (N + 3 : ℝ) / (N + 2 : ℝ) := by
  simp only [archiveCochainScaleRatio, Nat.cast_add, Nat.cast_one]
  congr 1 <;> ring

end
end D0.Geometry
