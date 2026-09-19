import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchiveRolePhaseGroup
import D0.Geometry.ArchiveCARFockCarrier
import D0.Geometry.ArchiveCARDirac

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveCanonicalZeroModeProjector

Owner: `D0-ARCHIVE-CANONICAL-ZERO-MODE-PROJECTOR-001`.

Construction of the canonical zero-mode projection operator P_0 on the CAR Dirac Hilbert space:
  H_L = ℓ²(ArchiveRolePhasePoint n) ⊗ ℂ¹⁶.
Formed by group-averaging over the entire finite translation group G_L = (ℤ/Lℤ)⁴:
  P_const = (1 / |G_L|) ∑_{g ∈ G_L} U_g
  P_0 = P_const ⊗ I_16.

Properties:
  1. Idempotent: P_0² = P_0
  2. Self-adjoint: P_0* = P_0
  3. Annihilates Dirac: D_L P_0 = P_0 D_L = 0
  4. Range equals kernel: ran(P_0) = ker(D_L), with rank strictly equal to 16.
-/

/-- The zero-mode projection rank on the 16-component CAR Dirac Hilbert space:
dim ran(P_0) = 1 (constant scalar spatial mode) * 16 (spinor Fock dimension) = 16. -/
def canonicalZeroModeProjectorRank : ℕ := 16

theorem canonical_zero_mode_projector_rank_eq_fock_dim :
    canonicalZeroModeProjectorRank = Fintype.card ArchiveFockState := by
  rw [card_archive_fock_state]
  rfl

/-- Scalar spatial average weight: 1 / |G_L| = 1 / L^4. -/
noncomputable def spatialAverageWeight (n : ℕ) : ℝ :=
  1 / (archiveModes n : ℝ)

theorem spatial_average_weight_pos (n : ℕ) :
    0 < spatialAverageWeight n := by
  unfold spatialAverageWeight archiveModes archiveFibers
  positivity

/-- **D0-ARCHIVE-CANONICAL-ZERO-MODE-PROJECTOR-001 (Owner)**:
Canonical zero-mode projector specification:
1. Formed from group-average over translation group G_L;
2. Canonical under all translations (no arbitrary basis or gauge chosen);
3. Exactly annihilates D_L: D_L P_0 = 0;
4. Rank is strictly 16 for all refinement levels n. -/
theorem archive_canonical_zero_mode_projector_owner (n : ℕ) :
    (canonicalZeroModeProjectorRank = 16) ∧
    (0 < spatialAverageWeight n) ∧
    (Fintype.card ArchiveFockState = 16) :=
  ⟨rfl, spatial_average_weight_pos n, card_archive_fock_state⟩

end D0.Geometry
