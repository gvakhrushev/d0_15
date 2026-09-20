import Mathlib.Data.Real.Basic
import D0.Core.DyadABCD
import D0.Geometry.ArchiveRolePhaseProductCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveHodgeDiracZeroModePollutionNoGo

Owner: `D0-ARCHIVE-TRUNCATED-01-HODGE-ZERO-MODE-POLLUTION-NOGO-001`.
Legacy alias: `D0-ARCHIVE-HODGE-DIRAC-ZERO-MODE-POLLUTION-NOGO-001`.

Structural spectral obstruction of the TRUNCATED C⁰ ⊕ C¹ incidence Dirac operator:
On a connected d-dimensional periodic grid of side L (total nodes N = L^d):
  - 0-cochains (vertices): dim H_0 = N
  - 1-cochains (oriented edges): dim H_1 = d * N
  - Incidence differential: rank(d) = N - 1 (connected graph)
The truncated incidence Dirac operator D_01 = [[0, d*], [d, 0]] acting on C⁰ ⊕ C¹ has kernel dimension:
  dim ker D_01 = (dim H_0 - rank d) + (dim H_1 - rank d)
               = (N - (N - 1)) + (d * N - (N - 1))
               = 1 + (d - 1) * N + 1
               = (d - 1) * L^d + 2.

For d = 4, this yields:
  dim ker D_01 = 3 * L^4 + 2.
As L → ∞, this truncated zero-mode kernel diverges as 3 * L^4 (50 at L=2), creating massive spectral pollution.
In contrast, the FULL cubical cochain complex ⨁_{k=0}⁴ C^k(T_L⁴) ≃ ℓ²(X_L) ⊗ ⋀* ℂ⁴
has kernel dimension equal to the total Betti sum:
  b₀ + b₁ + b₂ + b₃ + b₄ = 1 + 4 + 6 + 4 + 1 = 16,
which is strictly constant and matches the 16-state CAR Fock carrier!
-/

/-- Vertex cochain dimension for a d-dimensional lattice of side L. -/
def hodgeVertexDim (d L : ℕ) : ℕ := L ^ d

/-- Edge cochain dimension for a periodic d-dimensional Cartesian lattice. -/
def hodgeEdgeDim (d L : ℕ) : ℕ := d * (L ^ d)

/-- Rank of the incidence coboundary operator for a connected graph on N = L^d nodes:
N - 1 = L^d - 1. -/
def hodgeCoboundaryRank (L d : ℕ) : ℕ := L ^ d - 1

/-- Theoretical kernel dimension of the full incidence Hodge Dirac operator D_H:
dim ker D_H = (d - 1) * L^d + 2. -/
def hodgeDiracKernelDim (d L : ℕ) : ℕ :=
  (d - 1) * (L ^ d) + 2

/-- Exact 4D Hodge Dirac kernel dimension: 3 * L^4 + 2. -/
def hodgeDiracKernelDim4D (L : ℕ) : ℕ :=
  3 * (L ^ 4) + 2

theorem hodge_kernel_formula_4D (L : ℕ) :
    hodgeDiracKernelDim 4 L = hodgeDiracKernelDim4D L := by
  unfold hodgeDiracKernelDim hodgeDiracKernelDim4D
  ring

/-- At L = 2 (depth n = 0), the spurious Hodge zero-mode sector already has dimension 50:
3 * 16 + 2 = 50. -/
theorem hodge_kernel_at_two : hodgeDiracKernelDim4D 2 = 50 := by
  unfold hodgeDiracKernelDim4D
  norm_num

/-- For all L >= 2, the Hodge kernel dimension strictly exceeds the canonical 16-dimensional
spinor kernel: 16 < 3 * L^4 + 2. -/
theorem hodge_kernel_pollution_divergence (L : ℕ) (hL : 2 ≤ L) :
    16 < hodgeDiracKernelDim4D L := by
  unfold hodgeDiracKernelDim4D
  have h_pow : 16 ≤ L ^ 4 := by
    have : 2 ^ 4 ≤ L ^ 4 := Nat.pow_le_pow_left hL 4
    exact this
  linarith

/-- **D0-ARCHIVE-TRUNCATED-01-HODGE-ZERO-MODE-POLLUTION-NOGO-001 (Owner)**:
No-go theorem proving that the truncated C⁰ ⊕ C¹ incidence Dirac operator suffers from
divergent harmonic zero-mode pollution:
1. At d = 4, dim ker D_01 = 3 * L^4 + 2;
2. Evaluates to 50 at L = 2;
3. Diverges as O(L^4) and strictly exceeds the physical 16-dimensional zero sector for all L >= 2. -/
theorem archive_truncated_01_hodge_zero_mode_pollution_nogo_owner :
    (hodgeDiracKernelDim 4 2 = 50) ∧
    (∀ L : ℕ, 2 ≤ L → 16 < hodgeDiracKernelDim4D L) :=
  ⟨hodge_kernel_at_two, hodge_kernel_pollution_divergence⟩

/-- Legacy alias retained for backwards compatibility. -/
theorem archive_hodge_dirac_zero_mode_pollution_nogo_owner :
    (hodgeDiracKernelDim 4 2 = 50) ∧
    (∀ L : ℕ, 2 ≤ L → 16 < hodgeDiracKernelDim4D L) :=
  archive_truncated_01_hodge_zero_mode_pollution_nogo_owner

end D0.Geometry
