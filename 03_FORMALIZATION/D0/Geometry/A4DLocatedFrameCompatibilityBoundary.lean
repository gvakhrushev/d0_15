import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DLocatedPrimalDualCell
import D0.Geometry.A4DLocatedTopologicalStar
import D0.Geometry.A4DPrimalDualCellPairing

/-!
# Located frame compatibility boundary

Common-fiber cofactor identity and the shifted-anchor obstruction to naive
sitewise Lorentz action on both colors. Does **not** modify located placement `J`.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

def algebraicComplementMatrix (T S : ArchiveFockState) : ℚ :=
  if occupationComplement S = T then (complementOrientationInt S : ℚ) else 0

theorem common_fiber_cofactor_rationalABBoost :
    ∀ T S : ArchiveFockState,
      fockMatMulR algebraicComplementMatrix (exteriorLiftQ rationalABBoostQ) T S =
        (Matrix.det rationalABBoostQ : ℚ) *
          fockMatMulR
            (fun a b => exteriorLiftQ rationalABBoostInvQ b a)
            algebraicComplementMatrix T S := by
  native_decide

theorem located_J_unchanged (N : ℕ) (c : PrimalCell N) :
    locatedPrimalToDual c =
      { site := c.site - occupationIndicator N (occupationComplement c.label)
        label := occupationComplement c.label } := rfl

theorem located_dual_anchors_AB_differ_L2 :
    (locatedPrimalToDual (N := 0) ⟨0, fockSingletonState A⟩).site ≠
      (locatedPrimalToDual (N := 0) ⟨0, fockSingletonState B⟩).site := by
  native_decide

theorem boost_mixes_A_into_B :
    exteriorLiftQ rationalABBoostQ (fockSingletonState B) (fockSingletonState A) = (3 : ℚ) / 4 := by
  native_decide

theorem sitewise_lorentz_dual_obstruction_L2 :
    exteriorLiftQ rationalABBoostQ (fockSingletonState B) (fockSingletonState A) = (3 : ℚ) / 4 ∧
    (locatedPrimalToDual (N := 0) ⟨0, fockSingletonState A⟩).site ≠
      (locatedPrimalToDual (N := 0) ⟨0, fockSingletonState B⟩).site :=
  ⟨boost_mixes_A_into_B, located_dual_anchors_AB_differ_L2⟩

theorem a4d_located_frame_compatibility_boundary_owner :
    (∀ T S,
        fockMatMulR algebraicComplementMatrix (exteriorLiftQ rationalABBoostQ) T S =
          Matrix.det rationalABBoostQ *
            fockMatMulR (fun a b => exteriorLiftQ rationalABBoostInvQ b a)
              algebraicComplementMatrix T S) ∧
    (exteriorLiftQ rationalABBoostQ (fockSingletonState B) (fockSingletonState A) =
      (3 : ℚ) / 4) ∧
    (∀ N c, locatedPrimalToDual (N := N) c =
        { site := c.site - occupationIndicator N (occupationComplement c.label)
          label := occupationComplement c.label }) :=
  ⟨common_fiber_cofactor_rationalABBoost, boost_mixes_A_into_B, located_J_unchanged⟩

end

end D0.Geometry
