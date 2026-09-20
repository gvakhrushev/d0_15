import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.BigOperators
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveModeExponent

namespace D0.Geometry.ArchiveRolePhaseProductCarrier

open D0

/-- **Canonical 4D Role-Phase Carrier**:
The point space at refinement depth `n` is the coordinate-free function space from the
four terminal roles `Role = Dyad × Dyad` (ABCD) to the cycle phase index `archivePhaseIndex n = Fin (n + 2)`.
No artificial linear ordering of the four coordinates is chosen. -/
abbrev ArchiveRolePhasePoint (n : ℕ) : Type :=
  Role → archivePhaseIndex n

/-- The fiber cardinality at depth `n` is `archiveFibers n = n + 2`. -/
theorem card_archive_phase_index (n : ℕ) :
    Fintype.card (archivePhaseIndex n) = archiveFibers n := by
  unfold archivePhaseIndex archiveFibers
  exact Fintype.card_fin (n + 2)

/-- The role capacity is strictly 4: `|Role| = 4`. -/
theorem card_role_is_four : Fintype.card Role = 4 := card_role

/-- **D0-ARCHIVE-ROLE-PHASE-PRODUCT-CARRIER-001 (Cardinality Identity)**:
The cardinality of the role-phase product space `ArchiveRolePhasePoint n` matches
the exact number of archive modes `archiveModes n = (n + 2)^4`:
$$|\mathrm{ArchiveRolePhasePoint}(n)| = (\mathrm{archiveFibers}(n))^{|\mathrm{Role}|} = (n + 2)^4 = \mathrm{archiveModes}(n).$$ -/
theorem card_archive_role_phase_point (n : ℕ) :
    Fintype.card (ArchiveRolePhasePoint n) = archiveModes n := by
  classical
  have h_card_fun : Fintype.card (ArchiveRolePhasePoint n) =
      Fintype.card (archivePhaseIndex n) ^ Fintype.card Role :=
    Fintype.card_fun
  have h1 : Fintype.card (archivePhaseIndex n) ^ Fintype.card Role = (archiveFibers n)^4 := by
    rw [card_archive_phase_index, card_role_is_four]
  have h2 : (archiveFibers n)^4 = archiveModes n := rfl
  exact h_card_fun.trans (h1.trans h2)

/-- The role-phase product space is nonempty for every refinement level `n`. -/
instance (n : ℕ) : Nonempty (ArchiveRolePhasePoint n) := by
  have h_card : 0 < Fintype.card (ArchiveRolePhasePoint n) := by
    rw [card_archive_role_phase_point]
    unfold archiveModes archiveFibers
    positivity
  exact Fintype.card_pos_iff.mp h_card

/-- Equivariance under role permutations: any permutation $\sigma \in \mathrm{Equiv.Perm}(\mathrm{Role})$
induces an automorphism of `ArchiveRolePhasePoint n` by precomposition. -/
def permuteRole (n : ℕ) (σ : Equiv.Perm Role) :
    ArchiveRolePhasePoint n ≃ ArchiveRolePhasePoint n where
  toFun x := x ∘ σ
  invFun y := y ∘ σ.symm
  left_inv x := by
    funext r
    simp
  right_inv y := by
    funext r
    simp

/-- **D0-ARCHIVE-ROLE-PHASE-PRODUCT-CARRIER-001 (Owner)**:
Rigorous definition of the coordinate-free 4D archive carrier, proving exact mode cardinality
matching $(n+2)^4$, nonemptiness, and natural role-permutation equivariance. -/
theorem archive_role_phase_product_carrier_owner (n : ℕ) :
    (Fintype.card (ArchiveRolePhasePoint n) = archiveModes n) ∧
    (Fintype.card Role = 4) ∧
    (Fintype.card (archivePhaseIndex n) = archiveFibers n) ∧
    Nonempty (ArchiveRolePhasePoint n) :=
  ⟨card_archive_role_phase_point n, card_role_is_four, card_archive_phase_index n, inferInstance⟩

end D0.Geometry.ArchiveRolePhaseProductCarrier
