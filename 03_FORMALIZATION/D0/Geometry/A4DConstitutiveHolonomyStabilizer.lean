import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Geometry.A4DPathCovariantHodge

/-!
# Constitutive consequences of a supplied holonomy stabilizer

`pathDressing_eq_iff_relativeHolonomy_stabilizes` is already owned. This file
does not restate it. An independently supplied seed that is compatible with
every edge transport is stabilized by every loop product. The same seed can
admit two distinct compatible connections, one with nontrivial holonomy.

Both owned directions stay in force: orientation-preserving rotations can fix
`I`, and rational shears can move it. The criterion is stabilizer membership.
Nonzero curvature is not claimed to force a Hodge ambiguity, and metric
compatibility is not a Levi-Civita uniqueness theorem.
-/

namespace D0.Geometry

open D0

section Loop

variable {n R : Type*} [Fintype n] [DecidableEq n] [CommRing R]

theorem edgeMetricCompatibility_implies_allLoopStabilizer
    (W : Matrix n n R) (U : List (Matrix n n R))
    (hedge : ∀ M ∈ U, M.transpose * W * M = W) :
    (List.prod U).transpose * W * List.prod U = W := by
  induction U with
  | nil => simp
  | cons M tail ih =>
      have hM : M.transpose * W * M = W := hedge M (by simp)
      have htail : (List.prod tail).transpose * W * List.prod tail = W :=
        ih (fun N hN => hedge N (by simp [hN]))
      simp only [List.prod_cons, Matrix.transpose_mul]
      calc
        (List.prod tail).transpose * M.transpose * W * (M * List.prod tail) =
            (List.prod tail).transpose * (M.transpose * W * M) * List.prod tail := by
              simp only [Matrix.mul_assoc]
        _ = (List.prod tail).transpose * W * List.prod tail := by rw [hM]
        _ = W := htail

end Loop

/-- Two edgewise transports preserve the seed `I`. They are not equal, and the
nontrivial one has holonomy `rot90² ≠ I` on a two-edge loop. -/
def seedRot90 : Matrix (Fin 3) (Fin 3) ℚ := !![0, -1, 0; 1, 0, 0; 0, 0, 1]

theorem metricCompatibility_does_not_select_connection :
    let I3 : Matrix (Fin 3) (Fin 3) ℚ := 1
    let trivial : Fin 2 → Matrix (Fin 3) (Fin 3) ℚ := fun _ => 1
    let rotated : Fin 2 → Matrix (Fin 3) (Fin 3) ℚ := fun _ => seedRot90
    trivial ≠ rotated ∧
      (∀ i, (trivial i).transpose * I3 * trivial i = I3) ∧
      (∀ i, (rotated i).transpose * I3 * rotated i = I3) ∧
      seedRot90 * seedRot90 ≠ 1 ∧
      (seedRot90 * seedRot90).transpose * I3 * (seedRot90 * seedRot90) = I3 := by
  native_decide

end D0.Geometry
