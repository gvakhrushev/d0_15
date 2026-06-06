import Mathlib.Data.Real.Basic
import D0.Geometry.ArchivePhaseDistance

namespace D0

def archiveAdjacent (n : Nat) (i j : archivePhaseIndex n) : Prop :=
  cyclicDistance (archiveFibers n) i j = 1

instance (n : Nat) (i j : archivePhaseIndex n) : Decidable (archiveAdjacent n i j) := by
  unfold archiveAdjacent
  infer_instance

theorem archiveAdjacent_symmetric (n : Nat) :
  Symmetric (archiveAdjacent n) := by
  intro a b h
  unfold archiveAdjacent at *
  rw [cyclicDistance_symmetric] at h
  exact h

theorem archiveAdjacent_irreflexive (n : Nat) :
  Irreflexive (archiveAdjacent n) := by
  intro a h
  unfold archiveAdjacent at h
  have h0 : cyclicDistance (archiveFibers n) a a = 0 := by
    have hF : 0 < archiveFibers n := by
      unfold archiveFibers
      omega
    exact (cyclicDistance_zero_iff (archiveFibers n) hF a a).mpr rfl
  omega

structure ArchiveWeightedGraph (n : Nat) where
  V : Type
  fintypeV : Fintype V
  weight : V → V → ℝ
  symmetric : ∀ u v, weight u v = weight v u
  nonnegative : ∀ u v, 0 ≤ weight u v
  irreflexive : ∀ u, weight u u = 0

noncomputable def archiveWeightedGraph (n : Nat) : ArchiveWeightedGraph n where
  V := archivePhaseIndex n
  fintypeV := inferInstance
  weight i j := if archiveAdjacent n i j then 1 else 0
  symmetric u v := by
    by_cases h : archiveAdjacent n u v
    · have h2 := archiveAdjacent_symmetric n h
      simp [h, h2]
    · have h2 : ¬ archiveAdjacent n v u := by
        intro hc
        exact h (archiveAdjacent_symmetric n hc)
      simp [h, h2]
  nonnegative u v := by
    split_ifs <;> linarith
  irreflexive u := by
    have h : ¬ archiveAdjacent n u u := archiveAdjacent_irreflexive n u
    simp [h]

noncomputable def archiveWeightedGraph_canonical (n : Nat) : ArchiveWeightedGraph n :=
  archiveWeightedGraph n

end D0
