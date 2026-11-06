import D0.Geometry.ArchiveRoleRefinementProjection
import D0.Geometry.ArchiveCochainOccupancyMask

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-- Fine edges except the final collapsed edge are allowed in a role. -/
def archiveRefinementAllowed (N : ℕ) (y : ArchiveRolePhaseGroup (N + 1))
    (r : Role) : Bool :=
  decide ((archiveFineRoleIndex N r y).val < N + 2)

/-- Degree-scaled pullback with an edge mask in each occupied direction. -/
def archiveGradedCochainPullback (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain (N + 1) :=
  fun p => archiveCochainScaleRatio (N + 1) ^ fockDegree p.2 *
    archiveOccupancyMask p.2 (archiveRefinementAllowed N p.1) *
      ψ (archiveRoleGroupProjection N p.1, p.2)

theorem archive_group_projection_role_index (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) :
    (finZModEquiv N).symm (archiveRoleGroupProjection N y r) =
      archiveRGPhaseProjection N (archiveFineRoleIndex N r y) := by
  simp [archiveRoleGroupProjection, archiveRolePhasePointGroupEquiv,
    archiveRolePhaseProjection, archiveFineRoleIndex]

/-- The scalar result expressed directly as fine and coarse forward differences. -/
theorem archive_forward_pullback (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (f : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference (N + 1) r (fun z => f (archiveRoleGroupProjection N z)) y =
      (if archiveRefinementAllowed N y r = true then
        archiveCochainScaleRatio (N + 1) *
          forwardDifference N r f (archiveRoleGroupProjection N y)
       else 0) := by
  classical
  have hcomponent := congrFun (dForward_scalar_oneForm_component (N + 1)
    (fun z => f (archiveRoleGroupProjection N z)) r) y
  by_cases h : (archiveFineRoleIndex N r y).val < N + 2
  · let j : archivePhaseIndex N := ⟨(archiveFineRoleIndex N r y).val, h⟩
    have hi : archiveFineRoleIndex N r y = j.castSucc := by
      apply Fin.ext
      rfl
    have hp : archiveRGPhaseProjection N (archiveFineRoleIndex N r y) = j := by
      rw [hi]
      apply Fin.ext
      exact Nat.mod_eq_of_lt j.isLt
    have hj : (finZModEquiv N).symm (archiveRoleGroupProjection N y r) = j := by
      rw [archive_group_projection_role_index, hp]
    have he := archive_scalar_singleton_old_edge N r y f j hi
    rw [← hj, archive_role_slice_incidence] at he
    rw [← hcomponent, he]
    simp [archiveRefinementAllowed, h, forwardDifference_apply]
  · have hi : archiveFineRoleIndex N r y = Fin.last (N + 2) := by
      apply Fin.ext
      have hb := (archiveFineRoleIndex N r y).isLt
      simp only [Fin.val_last]
      unfold archivePhaseIndex archiveFibers at hb
      omega
    have he := archive_scalar_singleton_collapsed N r y f hi
    rw [← hcomponent, he]
    simp [archiveRefinementAllowed, h]

/-- Moving in an unoccupied role does not change the ket's edge mask. -/
theorem archive_mask_translate_unoccupied (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (ket : ArchiveFockState)
    (hr : ket r = false) :
    archiveOccupancyMask ket (archiveRefinementAllowed N (roleTranslatePlus (N + 1) r y)) =
      archiveOccupancyMask ket (archiveRefinementAllowed N y) := by
  apply archiveOccupancyMask_congr
  intro s hs
  have hsr : s ≠ r := by
    intro heq
    subst s
    rw [hr] at hs
    cases hs
  simp [archiveRefinementAllowed, archiveFineRoleIndex, roleTranslatePlus_apply,
    roleStep, hsr]

/-- A creation-supported ket has a constant prefactor on its forward edge. -/
theorem archive_graded_direction_factor (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + 1)) (ψ : ArchiveCochain N)
    (ket : ArchiveFockState) (hr : ket r = false) :
    forwardDifference (N + 1) r
      (fun z => archiveGradedCochainPullback N ψ (z, ket)) y =
        (archiveCochainScaleRatio (N + 1) ^ fockDegree ket *
          archiveOccupancyMask ket (archiveRefinementAllowed N y)) *
          forwardDifference (N + 1) r
            (fun z => ψ (archiveRoleGroupProjection N z, ket)) y := by
  have hm := archive_mask_translate_unoccupied N r y ket hr
  simp only [forwardDifference_apply, archiveGradedCochainPullback] at *
  rw [hm]
  ring

/-- The degree-scaled, mask-supported pullback intertwines the actual
finite Fock cochain differential in every occupation sector. -/
theorem archive_graded_cochain_chain (N : ℕ) (ψ : ArchiveCochain N) :
    dForward (N + 1) (archiveGradedCochainPullback N ψ) =
      archiveGradedCochainPullback N (dForward N ψ) := by
  classical
  funext p
  rcases p with ⟨y, bra⟩
  change (∑ r : Role, ∑ ket : ArchiveFockState,
    carCreate r bra ket * forwardDifference (N + 1) r
      (fun z => archiveGradedCochainPullback N ψ (z, ket)) y) =
    (archiveCochainScaleRatio (N + 1) ^ fockDegree bra *
      archiveOccupancyMask bra (archiveRefinementAllowed N y)) *
      (∑ r : Role, ∑ ket : ArchiveFockState,
        carCreate r bra ket * forwardDifference N r (fun x => ψ (x, ket))
          (archiveRoleGroupProjection N y))
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro r hr
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro ket hk
  by_cases hc : carCreate r bra ket = 0
  · rw [hc]
    simp only [zero_mul, mul_zero]
  · have hs := carCreate_support r bra ket hc
    have hd := carCreate_degree_raise r bra ket hc
    have hm := archiveOccupancyMask_carCreate r bra ket (archiveRefinementAllowed N y) hc
    have hf := archive_graded_direction_factor N r y ψ ket hs.2.1
    have ha := archive_forward_pullback N r y (fun x => ψ (x, ket))
    rw [hf, ha, hd, hm, pow_succ]
    by_cases h : archiveRefinementAllowed N y r = true <;> simp [h] <;> ring

end
end D0.Geometry
