import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalLaplacian

namespace D0

/-!
# Archive phase-local Laplacian uniqueness

The previous version of this module registered a `NO_GO_ARCHIVE_PHASE_LOCAL_UNIQUENESS`
whose proof field was merely `True`.  That status was too weak: the contract below already fixes
the matrix uniquely.

Indeed, nearest-neighbour support plus normalized edge weight fixes every off-diagonal entry, while
`zero_on_constants` fixes the diagonal as minus the off-diagonal row sum.  Nonnegativity and cycle
translation invariance remain useful structural properties, but they are not needed for uniqueness.

This theorem is about the *simple-cycle* phase Laplacian.  It does not identify that operator with the
oriented finite-difference/multigraph Laplacian used by the archive Weyl certificate at the degenerate
two-site stage; that operator provenance is handled separately.
-/

structure PhaseLocalQuadraticForm (n : Nat) where
  Q : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  symmetric : ∀ i j, Q i j = Q j i
  nonnegative : ∀ f, 0 ≤ matrixQuadraticForm Q f
  zero_on_constants : ∀ c, Matrix.mulVec Q (fun _ => c) = 0
  support_only_nearest_phase_neighbors :
    ∀ i j, ¬ archiveAdjacent n i j → i ≠ j → Q i j = 0
  translation_invariant_on_cycle :
    ∀ (i j : archivePhaseIndex n) (k : archivePhaseIndex n), Q (i + k) (j + k) = Q i j
  normalized_edge_weight : ∀ i j, archiveAdjacent n i j → Q i j = -1

/--
The phase-local contract uniquely determines the canonical simple-cycle Laplacian.

Off diagonal, the support and normalized-edge clauses determine the entry pointwise.  On the
diagonal, both `Q` and `archiveCanonicalLaplacian` kill the constant-one vector, so equality of all
off-diagonal entries forces equality of the remaining diagonal entry.
-/
theorem phase_local_quadratic_form_unique (n : Nat) (q : PhaseLocalQuadraticForm n) :
    q.Q = archiveCanonicalLaplacian n := by
  classical
  ext i j
  by_cases hij : i = j
  · subst j
    have hqzero : (∑ k : archivePhaseIndex n, q.Q i k) = 0 := by
      have h := congr_fun (q.zero_on_constants (1 : ℝ)) i
      simpa [Matrix.mulVec, dotProduct] using h
    have hlzero : (∑ k : archivePhaseIndex n, archiveCanonicalLaplacian n i k) = 0 := by
      have h := congr_fun (archiveCanonicalLaplacian_constant_zero n (1 : ℝ)) i
      simpa [Matrix.mulVec, dotProduct] using h
    have hoff :
        ∀ k ∈ (Finset.univ : Finset (archivePhaseIndex n)).erase i,
          q.Q i k = archiveCanonicalLaplacian n i k := by
      intro k hk
      have hki : k ≠ i := Finset.ne_of_mem_erase hk
      have hik : i ≠ k := Ne.symm hki
      unfold archiveCanonicalLaplacian
      rw [if_neg hik]
      by_cases hadj : archiveAdjacent n i k
      · rw [if_pos hadj, q.normalized_edge_weight i k hadj]
      · rw [if_neg hadj, q.support_only_nearest_phase_neighbors i k hadj hik]
    have hsumoff :
        (∑ k ∈ (Finset.univ : Finset (archivePhaseIndex n)).erase i, q.Q i k) =
          ∑ k ∈ (Finset.univ : Finset (archivePhaseIndex n)).erase i,
            archiveCanonicalLaplacian n i k := by
      apply Finset.sum_congr rfl
      intro k hk
      exact hoff k hk
    have hqsplit :=
      Finset.sum_erase_add Finset.univ (fun k : archivePhaseIndex n => q.Q i k)
        (Finset.mem_univ i)
    have hlsplit :=
      Finset.sum_erase_add Finset.univ
        (fun k : archivePhaseIndex n => archiveCanonicalLaplacian n i k)
        (Finset.mem_univ i)
    rw [← hqsplit] at hqzero
    rw [← hlsplit] at hlzero
    rw [hsumoff] at hqzero
    linarith
  · unfold archiveCanonicalLaplacian
    rw [if_neg hij]
    by_cases hadj : archiveAdjacent n i j
    · rw [if_pos hadj, q.normalized_edge_weight i j hadj]
    · rw [if_neg hadj, q.support_only_nearest_phase_neighbors i j hadj hij]

/-- Packaging theorem for the registered owner. -/
theorem archive_phase_local_laplacian_uniqueness_owner :
    ∀ n (q : PhaseLocalQuadraticForm n), q.Q = archiveCanonicalLaplacian n := by
  intro n q
  exact phase_local_quadratic_form_unique n q

end D0
