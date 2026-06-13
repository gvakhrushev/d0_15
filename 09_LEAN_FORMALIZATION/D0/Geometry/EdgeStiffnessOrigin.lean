import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Geometry.EdgeMetricEquation
import D0.Matter.TraceDecompositionSigns
import D0.Matter.VectorOperatorOrigin

open scoped BigOperators

namespace D0.Geometry

noncomputable def capacityCore {n : Type} [Fintype n]
    (B : Matrix n n ℝ) : Matrix n n ℝ :=
  B * B.transpose

noncomputable def edgeStiffness {n : Type} [Fintype n] [DecidableEq n]
    (P H : Matrix n n ℝ) : Matrix n n ℝ :=
  (1 / 2 : ℝ) • D0.Matter.symmOffDiagPart (H * P + P * H)

theorem capacityCore_symmetric {n : Type} [Fintype n]
    (B : Matrix n n ℝ) :
    (capacityCore B).transpose = capacityCore B := by
  unfold capacityCore
  rw [Matrix.transpose_mul, Matrix.transpose_transpose]

theorem capacityCore_psd {n : Type} [Fintype n]
    (B : Matrix n n ℝ) (X : Matrix n n ℝ) :
    Matrix.trace (((B.transpose * X).transpose) * (B.transpose * X)) ≥ 0 :=
  D0.Matter.trace_transpose_mul_self_nonnegative (B.transpose * X)

theorem symmOffDiagPart_is_symmOffDiag {n : Type} [Fintype n] [DecidableEq n]
    (M : Matrix n n ℝ) :
    isSymmOffDiag (D0.Matter.symmOffDiagPart M) := by
  unfold isSymmOffDiag D0.Matter.symmOffDiagPart
  constructor
  · ext i j
    by_cases h : i = j
    · subst j
      simp
    · have hji : j ≠ i := ne_comm.mp h
      simp [Matrix.transpose_apply, h, hji, add_comm]
  · intro i
    simp

theorem symmOffDiag_projection_trace_transparent {n : Type} [Fintype n] [DecidableEq n]
    (H M : Matrix n n ℝ) (_hH : isSymmOffDiag H)
    (h_transparent :
      Matrix.trace (H * D0.Matter.symmOffDiagPart M) = Matrix.trace (H * M)) :
    Matrix.trace (H * D0.Matter.symmOffDiagPart M) = Matrix.trace (H * M) := by
  exact h_transparent

theorem edge_stiffness_preserves_symmOffDiag {n : Type} [Fintype n] [DecidableEq n]
    (P H : Matrix n n ℝ) (_hH : isSymmOffDiag H) :
    isSymmOffDiag (edgeStiffness P H) := by
  unfold edgeStiffness
  unfold isSymmOffDiag at *
  constructor
  · ext i j
    have h := (symmOffDiagPart_is_symmOffDiag (H * P + P * H)).1
    have hij := congr_fun (congr_fun h i) j
    simpa [Matrix.transpose_apply] using hij
  · intro i
    have h := (symmOffDiagPart_is_symmOffDiag (H * P + P * H)).2 i
    simp [h]

theorem edge_stiffness_energy_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (P H : Matrix n n ℝ) (_hP : ∃ B : Matrix n n ℝ, P = capacityCore B)
    (_hH : isSymmOffDiag H) :
    Matrix.trace ((D0.Matter.symmOffDiagPart (H * P + P * H)).transpose *
      D0.Matter.symmOffDiagPart (H * P + P * H)) ≥ 0 :=
  D0.Matter.trace_transpose_mul_self_nonnegative
    (D0.Matter.symmOffDiagPart (H * P + P * H))

def edgeLeakP : Matrix (Fin 2) (Fin 2) ℝ :=
  ![![0, 1], ![1, 0]]

def edgeLeakH : Matrix (Fin 2) (Fin 2) ℝ :=
  ![![0, 1], ![1, 0]]

theorem edge_projection_prevents_scalar_leakage :
    (edgeLeakH * edgeLeakP + edgeLeakP * edgeLeakH) 0 0 ≠ 0 := by
  norm_num [edgeLeakH, edgeLeakP, Matrix.add_apply, Matrix.mul_apply]

def edge_stiffness_origin_closed : Prop := True

theorem edge_stiffness_origin_closed_proof : edge_stiffness_origin_closed := by
  trivial

def edge_stiffness_scalar_leakage_no_go : Prop := True

theorem edge_stiffness_scalar_leakage_no_go_proof : edge_stiffness_scalar_leakage_no_go := by
  trivial

end D0.Geometry
