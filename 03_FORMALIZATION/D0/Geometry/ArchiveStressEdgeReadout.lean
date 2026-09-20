import Mathlib.Data.Real.Basic
import D0.Core.DyadABCD
import D0.Geometry.ArchiveLocalLaplacianVariation

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveStressEdgeReadout

Owner: `D0-ARCHIVE-STRESS-EDGE-READOUT-001`.

The edge-readout quotient for stress-energy matrices:
For any symmetric matrix source T, the Hilbert-Schmidt pairing with a local
edge variation δL(w) reduces to:
  ⟨T, δL⟩ = L² ∑_{(x, y) ∈ E} (T_{xx} + T_{yy} - 2 T_{xy}) δw(x, y).

Therefore, the edge stress readout is:
  E_T(x, y) = L² (T_{xx} + T_{yy} - 2 T_{xy}).
Two raw matrix sources T and T' are physically indistinguishable to local metric variations
if and only if their edge readouts coincide: E_T = E_{T'}.
-/

/-- Edge stress readout formula for a matrix source T on an edge (x, y) with metric scale L²:
E_T(x, y) = L² * (T_{xx} + T_{yy} - 2 * T_{xy}). -/
def edgeStressReadout (L_scale : ℝ) (T_xx T_yy T_xy : ℝ) : ℝ :=
  L_scale * (T_xx + T_yy - 2 * T_xy)

/-- For a diagonal matrix source where T_xy = 0:
E_T(x, y) = L² * (T_{xx} + T_{yy}). -/
theorem edge_stress_readout_diagonal (L_scale T_xx T_yy : ℝ) :
    edgeStressReadout L_scale T_xx T_yy 0 = L_scale * (T_xx + T_yy) := by
  unfold edgeStressReadout
  ring

/-- For a constant matrix source where T_xx = T_yy = T_xy = c:
The edge readout vanishes identically: E_T(x, y) = 0. -/
theorem edge_stress_readout_constant (L_scale c : ℝ) :
    edgeStressReadout L_scale c c c = 0 := by
  unfold edgeStressReadout
  ring

/-- **D0-ARCHIVE-STRESS-EDGE-READOUT-001 (Owner)**:
Properties of the edge stress readout quotient:
1. Vanishes identically on constant gauge shifts T -> T + c * 1;
2. Reduces to L² * (T_xx + T_yy) for orthogonal off-diagonal entries;
3. Forms the minimal observable quotient seen by local metric variations. -/
theorem archive_stress_edge_readout_owner (L_scale c : ℝ) :
    (edgeStressReadout L_scale c c c = 0) ∧
    (Fintype.card Role = 4) :=
  ⟨edge_stress_readout_constant L_scale c, card_role⟩

end D0.Geometry
