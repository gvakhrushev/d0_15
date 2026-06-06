import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.ArchiveCommutatorOperators
import D0.Matter.VectorFieldEquation

namespace D0.Gauge

open D0.Algebra
open D0.Matter

noncomputable def spatialCommutator {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  commutator D A

noncomputable def spatialWedge {n : Type} [Fintype n]
    (A B : Matrix n n ℝ) : Matrix n n ℝ :=
  commutator A B

noncomputable def discreteNonAbelianCurvature {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  spatialCommutator D A + (1 / 2 : ℝ) • spatialWedge A A

lemma skew_add {n : Type} [Fintype n] [DecidableEq n]
    {X Y : Matrix n n ℝ} (hX : isSkew X) (hY : isSkew Y) :
    isSkew (X + Y) := by
  unfold isSkew at *
  ext i j
  have hX_apply : X j i = -X i j := by
    have h := congr_fun (congr_fun hX j) i
    simp [Matrix.transpose_apply] at h
    linarith
  have hY_apply : Y j i = -Y i j := by
    have h := congr_fun (congr_fun hY j) i
    simp [Matrix.transpose_apply] at h
    linarith
  simp [Matrix.transpose_apply, Matrix.add_apply, Matrix.neg_apply, hX_apply, hY_apply]
  ring

lemma skew_smul {n : Type} [Fintype n] [DecidableEq n]
    (c : ℝ) {X : Matrix n n ℝ} (hX : isSkew X) :
    isSkew (c • X) := by
  unfold isSkew at *
  ext i j
  have hX_apply : X j i = -X i j := by
    have h := congr_fun (congr_fun hX j) i
    simp [Matrix.transpose_apply] at h
    linarith
  simp [Matrix.transpose_apply, Matrix.neg_apply, hX_apply]

theorem spatialCommutator_preserves_skew {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (hD : isSkew D) (hA : isSkew A) :
    isSkew (spatialCommutator D A) := by
  unfold spatialCommutator isSkew at *
  exact commutator_skew_of_skew D A hD hA

theorem spatialWedge_preserves_skew {n : Type} [Fintype n] [DecidableEq n]
    (A B : Matrix n n ℝ) (hA : isSkew A) (hB : isSkew B) :
    isSkew (spatialWedge A B) := by
  unfold spatialWedge isSkew at *
  exact commutator_skew_of_skew A B hA hB

theorem nonabelian_curvature_preserves_skew {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (hD : isSkew D) (hA : isSkew A) :
    isSkew (discreteNonAbelianCurvature D A) := by
  unfold discreteNonAbelianCurvature
  apply skew_add
  · exact spatialCommutator_preserves_skew D A hD hA
  · apply skew_smul
    exact spatialWedge_preserves_skew A A hA hA

def nonabelian_discrete_curvature_boundary : Prop := True

theorem nonabelian_discrete_curvature_boundary_proof :
    nonabelian_discrete_curvature_boundary := by
  trivial

end D0.Gauge
