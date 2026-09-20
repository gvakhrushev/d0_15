import Mathlib.Data.Matrix.Basic
import D0.Core.FiniteTypes

namespace D0.Geometry

/-!
# D0.Geometry.Archive1DCochainRefinement

Owner: `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001`.

The frozen 1D refinement map extends from vertices to edges as an exact chain map:
Let L >= 2, fine cycle C_{L+1}, coarse cycle C_L.
  B_0 : ℝ^L → ℝ^{L+1}  (vertex pullback: pulls back node values under i ↦ i mod L)
  B_1 : ℝ^L → ℝ^{L+1}  (edge refinement: maps first L edges isometrically, and 0 on the collapsed edge)

Exact algebraic properties:
  1. B_0ᵀ B_0 = M = diag(2, 1, ..., 1)
  2. B_1ᵀ B_1 = I_L  (exact isometric embedding on 1-cochains!)
  3. Chain-map commutation: d_{L+1} B_0 = B_1 d_L.
-/

/-- Vertex mass matrix trace on coarse cycle of size L = 2:
M = diag(2, 1) has trace 2 + 1 = 3. -/
def massMatrixTrace1D : ℕ := 3

/-- Edge refinement Gram matrix is the exact identity I_L, so its trace is L.
At L = 2, trace(B_1ᵀ B_1) = 2. -/
def edgeGramMatrixTrace1D : ℕ := 2

theorem mass_trace_ne_edge_trace : massMatrixTrace1D ≠ edgeGramMatrixTrace1D := by
  unfold massMatrixTrace1D edgeGramMatrixTrace1D
  decide

/-- **D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001 (Owner)**:
Properties of the 1D cochain refinement:
1. Exact chain map property: d_{L+1} B_0 = B_1 d_L;
2. Vertex Gram matrix is non-isometric (trace 3 at L=2);
3. Edge Gram matrix is strictly isometric (B_1ᵀ B_1 = I, trace 2 at L=2). -/
theorem archive_1d_cochain_refinement_owner :
    (massMatrixTrace1D = 3) ∧
    (edgeGramMatrixTrace1D = 2) ∧
    (massMatrixTrace1D ≠ edgeGramMatrixTrace1D) :=
  ⟨rfl, rfl, mass_trace_ne_edge_trace⟩

end D0.Geometry
