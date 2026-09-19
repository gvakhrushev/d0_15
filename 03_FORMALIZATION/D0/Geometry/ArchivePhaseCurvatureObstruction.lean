import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveLaplacianRG

namespace D0

/-!
# Strict phase-refinement obstruction with explicit witnesses

The earlier version of this module packaged two no-go claims with fields of type `True`.  This file
now proves the actual negative statements.

The canonical phase projection collapses the newly inserted last fine vertex onto the coarse zero
vertex.  For `n > 1`, coarse vertices `0` and `1` are adjacent while fine vertices `n+2` and
`1` are not.  Hence the nearest-neighbour cycle Laplacian cannot be a strict entrywise pullback.
The same explicit entry witnesses a nonzero refinement obstruction.

This is an RG/extrinsic refinement defect.  No intrinsic Riemann-curvature interpretation is asserted.
-/

def archivePhaseProjection (n : Nat) : archivePhaseIndex (n+1) → archivePhaseIndex n :=
  archiveRGPhaseProjection n

def pullbackLaplacian {n : Nat} (L : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  fun i j => L (archivePhaseProjection n i) (archivePhaseProjection n j)

def phaseCurvatureObstruction (n : Nat) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  pullbackLaplacian (archiveCanonicalLaplacian n) - archiveCanonicalLaplacian (n+1)

def PhaseProjectionFlat (n : Nat) : Prop :=
  ∀ i j : archivePhaseIndex (n+1),
    (archiveCanonicalLaplacian n) (archivePhaseProjection n i) (archivePhaseProjection n j) =
      (archiveCanonicalLaplacian (n+1)) i j

theorem phase_flat_iff_zero_curvature_obstruction (n : Nat) :
  phaseCurvatureObstruction n = 0 ↔ PhaseProjectionFlat n := by
  unfold phaseCurvatureObstruction PhaseProjectionFlat
  constructor
  · intro h i j
    have h_eq :
        (pullbackLaplacian (archiveCanonicalLaplacian n) -
            archiveCanonicalLaplacian (n+1)) i j = 0 := by
      rw [h]
      rfl
    change archiveCanonicalLaplacian n (archivePhaseProjection n i)
      (archivePhaseProjection n j) - archiveCanonicalLaplacian (n+1) i j = 0 at h_eq
    linarith
  · intro h
    ext i j
    unfold pullbackLaplacian
    change archiveCanonicalLaplacian n (archivePhaseProjection n i)
      (archivePhaseProjection n j) - archiveCanonicalLaplacian (n+1) i j = 0
    rw [h i j]
    simp

def PhaseProjectivelyCompatible
  (L : ∀ n, Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (proj : ∀ n, archivePhaseIndex (n+1) → archivePhaseIndex n) : Prop :=
  ∀ n (i j : archivePhaseIndex (n+1)),
    L (n+1) i j = L n (proj n i) (proj n j)

/-- In the fine cycle of size `n+3`, the newly inserted last vertex is not adjacent to vertex one. -/
lemma phase_cycle_last_not_adj_one (n : Nat) (hn : 1 < n) :
    ¬ archiveAdjacent (n+1)
        ⟨n+2, by unfold archiveFibers; omega⟩
        ⟨1, by unfold archiveFibers; omega⟩ := by
  unfold archiveAdjacent cyclicDistance archiveFibers
  intro hc
  have h_t1 : (n+2 + (n+3) - 1) % (n+3) = n+1 := by
    rw [show n+2 + (n+3) - 1 = (n+1) + (n+3) from by omega, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt (by omega)
  have h_t2 : (1 + (n+3) - (n+2)) % (n+3) = 2 := by
    rw [show 1 + (n+3) - (n+2) = 2 from by omega]
    exact Nat.mod_eq_of_lt (by omega)
  simp only [h_t1, h_t2, min_eq_right (show 2 ≤ n+1 from by omega)] at hc
  omega

/-- In the coarse cycle of size `n+2`, vertices zero and one are adjacent. -/
lemma phase_cycle_zero_adj_one (n : Nat) (hn : 1 < n) :
    archiveAdjacent n
        ⟨0, by unfold archiveFibers; omega⟩
        ⟨1, by unfold archiveFibers; omega⟩ := by
  unfold archiveAdjacent cyclicDistance archiveFibers
  have h_t1 : (0 + (n+2) - 1) % (n+2) = n+1 := by
    rw [show 0 + (n+2) - 1 = n+1 from by omega]
    exact Nat.mod_eq_of_lt (by omega)
  have h_t2 : (1 + (n+2) - 0) % (n+2) = 1 := by
    rw [show 1 + (n+2) - 0 = 1 + (n+2) from by omega, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt (by omega)
  simp only [h_t1, h_t2, min_eq_right (show 1 ≤ n+1 from by omega)]

/--
Strict entrywise pullback flatness fails at every level `n > 1`.

Witness: the fine vertex `n+2` projects to coarse vertex `0`; vertex `1` projects to itself.
The coarse pair is adjacent, the fine pair is not.
-/
theorem phase_projection_not_flat (n : Nat) (hn : 1 < n) :
    ¬ PhaseProjectionFlat n := by
  intro hflat
  let iFine : archivePhaseIndex (n+1) :=
    ⟨n+2, by unfold archiveFibers; omega⟩
  let jFine : archivePhaseIndex (n+1) :=
    ⟨1, by unfold archiveFibers; omega⟩
  let iCoarse : archivePhaseIndex n :=
    ⟨0, by unfold archiveFibers; omega⟩
  let jCoarse : archivePhaseIndex n :=
    ⟨1, by unfold archiveFibers; omega⟩
  have hpi : archivePhaseProjection n iFine = iCoarse := by
    apply Fin.ext
    simp [archivePhaseProjection, archiveRGPhaseProjection, iFine, iCoarse,
      archiveFibers, Nat.mod_self]
  have hpj : archivePhaseProjection n jFine = jCoarse := by
    apply Fin.ext
    simp [archivePhaseProjection, archiveRGPhaseProjection, jFine, jCoarse,
      archiveFibers, Nat.mod_eq_of_lt (show 1 < n + 2 by omega)]
  have hentry := hflat iFine jFine
  rw [hpi, hpj] at hentry
  have hcoarse_ne : iCoarse ≠ jCoarse := by
    intro h
    have hv := congrArg Fin.val h
    simp [iCoarse, jCoarse] at hv
  have hfine_ne : iFine ≠ jFine := by
    intro h
    have hv := congrArg Fin.val h
    simp [iFine, jFine] at hv
  have hcoarse_adj : archiveAdjacent n iCoarse jCoarse := by
    simpa [iCoarse, jCoarse] using phase_cycle_zero_adj_one n hn
  have hfine_not_adj : ¬ archiveAdjacent (n+1) iFine jFine := by
    simpa [iFine, jFine] using phase_cycle_last_not_adj_one n hn
  unfold archiveCanonicalLaplacian at hentry
  rw [if_neg hcoarse_ne, if_pos hcoarse_adj, if_neg hfine_ne, if_neg hfine_not_adj] at hentry
  norm_num at hentry

/-- The refinement-curvature matrix is genuinely nonzero for every nondegenerate level `n > 1`. -/
theorem phase_curvature_obstruction_nonzero (n : Nat) (hn : 1 < n) :
    phaseCurvatureObstruction n ≠ 0 := by
  intro hzero
  exact phase_projection_not_flat n hn ((phase_flat_iff_zero_curvature_obstruction n).mp hzero)

/-- The whole nearest-neighbour phase-Laplacian tower is not strictly entrywise projective. -/
theorem archive_phase_laplacian_not_projectively_compatible :
    ¬ PhaseProjectivelyCompatible archiveCanonicalLaplacian archivePhaseProjection := by
  intro hcompat
  have hflat : PhaseProjectionFlat 2 := by
    intro i j
    exact (hcompat 2 i j).symm
  exact phase_projection_not_flat 2 (by omega) hflat

/-- Registered owner: strict projective compatibility fails and the explicit obstruction is nonzero. -/
theorem archive_phase_curvature_obstruction_owner :
    (¬ PhaseProjectivelyCompatible archiveCanonicalLaplacian archivePhaseProjection) ∧
      (∀ n, 1 < n → phaseCurvatureObstruction n ≠ 0) := by
  refine ⟨archive_phase_laplacian_not_projectively_compatible, ?_⟩
  intro n hn
  exact phase_curvature_obstruction_nonzero n hn

end D0
