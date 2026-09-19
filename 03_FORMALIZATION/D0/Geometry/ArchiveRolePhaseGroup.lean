import Mathlib.Data.ZMod.Basic
import Mathlib.Logic.Equiv.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveRolePhaseProductCarrier

namespace D0.Geometry

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier

/-- Fiber cardinality is strictly non-zero: $n + 2 \ge 2 > 0$. -/
instance instNeZeroArchiveFibers (n : ℕ) : NeZero (archiveFibers n) :=
  ⟨by unfold archiveFibers; omega⟩

/-- The group shadow of the role-phase carrier:
Each role is assigned an element of the cyclic additive group $\mathbb{Z} / (n+2)\mathbb{Z}$.
$$\operatorname{ArchiveRolePhaseGroup}(n) = \mathrm{Role} \to \mathbb{Z} / (n+2)\mathbb{Z}.$$ -/
abbrev ArchiveRolePhaseGroup (n : ℕ) : Type :=
  Role → ZMod (archiveFibers n)

/-- Canonical bijection between `Fin L` and `ZMod L` for $L = n + 2$. -/
def finZModEquiv (n : ℕ) : archivePhaseIndex n ≃ ZMod (archiveFibers n) :=
  ZMod.finEquiv (archiveFibers n)

/-- **D0-ARCHIVE-ROLE-PHASE-GROUP-001 (Owner)**:
Canonical structural equivalence between the geometric point space `ArchiveRolePhasePoint n`
and the finite Abelian group `ArchiveRolePhaseGroup n`:
$$\operatorname{ArchiveRolePhasePoint}_L \simeq (\mathbb{Z} / L\mathbb{Z})^{\mathrm{Role}}.$$
This endows the coordinate-free role carrier with intrinsic group translations without
arbitrary linear coordinate orderings. -/
def archiveRolePhasePointGroupEquiv (n : ℕ) :
    ArchiveRolePhasePoint n ≃ ArchiveRolePhaseGroup n where
  toFun x r := finZModEquiv n (x r)
  invFun y r := (finZModEquiv n).symm (y r)
  left_inv x := by
    funext r
    exact (finZModEquiv n).left_inv (x r)
  right_inv y := by
    funext r
    exact (finZModEquiv n).right_inv (y r)

/-- Both types have the exact same mode cardinality $(n+2)^4 = \mathrm{archiveModes}(n)$. -/
theorem card_archive_role_phase_group (n : ℕ) :
    Fintype.card (ArchiveRolePhaseGroup n) = archiveModes n := by
  have h := Fintype.card_congr (archiveRolePhasePointGroupEquiv n)
  rw [← h]
  exact card_archive_role_phase_point n

/-- **D0-ARCHIVE-ROLE-PHASE-GROUP-001 (Owner theorem)**:
Confirms the equivalence and cardinality equality. -/
theorem archive_role_phase_group_owner (n : ℕ) :
    (Fintype.card (ArchiveRolePhaseGroup n) = archiveModes n) ∧
    (Fintype.card Role = 4) :=
  ⟨card_archive_role_phase_group n, card_role⟩

end D0.Geometry
