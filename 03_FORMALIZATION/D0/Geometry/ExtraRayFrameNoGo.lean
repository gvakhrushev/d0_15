import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# Finite frame-dependence witnesses

Exact rational witnesses that a Euclidean orthogonal change moves the
background projector `P = I - uuᵀ/4`, and that a rational Lorentz boost
moves the spatial projector `I - TT♭`.  No manifold, continuum naturality,
or Einstein uniqueness is claimed.
-/

namespace D0.Geometry.ExtraRayFrameNoGo

open Matrix

def hadamardFrame : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1 / 2, 1 / 2, 1 / 2, 1 / 2;
     1 / 2, -1 / 2, 1 / 2, -1 / 2;
     1 / 2, 1 / 2, -1 / 2, -1 / 2;
     1 / 2, -1 / 2, -1 / 2, 1 / 2]

def equalVector : Fin 4 → ℚ := fun _ => 1

def backgroundProjector : Matrix (Fin 4) (Fin 4) ℚ :=
  1 - (1 / 4 : ℚ) • vecMulVec equalVector equalVector

theorem hadamardFrame_orthogonal :
    hadamardFrame.transpose * hadamardFrame = 1 := by
  native_decide

theorem hadamardFrame_sends_half_equal_to_basis :
    hadamardFrame.mulVec (fun i => equalVector i / 2) = Pi.single 0 1 := by
  native_decide

theorem hadamardFrame_moves_background_projector :
    hadamardFrame * backgroundProjector * hadamardFrame.transpose ≠ backgroundProjector := by
  native_decide

def rationalBoost : Matrix (Fin 4) (Fin 4) ℚ :=
  !![5 / 3, 4 / 3, 0, 0;
     4 / 3, 5 / 3, 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

def minkowski : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1, 0, 0, 0;
     0, -1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, -1]

def timeVector : Fin 4 → ℚ := Pi.single 0 1

def boostedTime : Fin 4 → ℚ := rationalBoost.mulVec timeVector

def spatialProjector (T : Fin 4 → ℚ) : Matrix (Fin 4) (Fin 4) ℚ :=
  1 - vecMulVec T (minkowski.mulVec T)

theorem rationalBoost_preserves_minkowski :
    rationalBoost.transpose * minkowski * rationalBoost = minkowski := by
  native_decide

theorem boostedTime_coords :
    boostedTime = ![5 / 3, 4 / 3, 0, 0] := by
  native_decide

theorem boostedTime_unit :
    dotProduct boostedTime (minkowski.mulVec boostedTime) = 1 := by
  native_decide

theorem spatialProjector_moves :
    spatialProjector boostedTime ≠ spatialProjector timeVector := by
  native_decide

theorem time_form_killed_by_rest_projector :
    (spatialProjector timeVector).mulVec timeVector = 0 := by
  native_decide

theorem time_form_survives_boosted_projector :
    (spatialProjector boostedTime).mulVec timeVector ≠ 0 := by
  native_decide

end D0.Geometry.ExtraRayFrameNoGo
