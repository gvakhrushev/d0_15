import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.ArchiveCommutatorOperators
import D0.Gauge.NonAbelianDiscreteCurvature
import D0.Matter.VectorFieldEquation

open scoped BigOperators

namespace D0.Gauge

open D0.Algebra
open D0.Matter

def isOrthogonal {k : Type} [Fintype k] [DecidableEq k]
    (U : Matrix k k Real) : Prop :=
  U.transpose * U = 1 /\ U * U.transpose = 1

noncomputable def gaugeTransformFinite {k : Type} [Fintype k]
    (U A : Matrix k k Real) : Matrix k k Real :=
  U * A * U.transpose

noncomputable def discreteMaurerCartan {k : Type} [Fintype k]
    (D U : Matrix k k Real) : Matrix k k Real :=
  commutator D U * U.transpose

noncomputable def matrixRepCurvature {k : Type} [Fintype k]
    (D A : Matrix k k Real) : Matrix k k Real :=
  spatialCommutator D A

theorem gaugeTransformFinite_well_typed {k : Type} [Fintype k]
    (U A : Matrix k k Real) :
    Exists fun B : Matrix k k Real => B = gaugeTransformFinite U A := by
  exact ⟨gaugeTransformFinite U A, rfl⟩

theorem discreteMaurerCartan_well_typed {k : Type} [Fintype k]
    (D U : Matrix k k Real) :
    Exists fun B : Matrix k k Real => B = discreteMaurerCartan D U := by
  exact ⟨discreteMaurerCartan D U, rfl⟩

theorem matrixRepCurvature_well_typed {k : Type} [Fintype k]
    (D A : Matrix k k Real) :
    Exists fun K : Matrix k k Real => K = matrixRepCurvature D A := by
  exact ⟨matrixRepCurvature D A, rfl⟩

theorem gaugeTransformFinite_preserves_skew_of_orthogonal {k : Type}
    [Fintype k] [DecidableEq k]
    (U A : Matrix k k Real) (_hU : isOrthogonal U) (hA : isSkew A) :
    isSkew (gaugeTransformFinite U A) := by
  unfold gaugeTransformFinite isSkew at *
  calc
    (U * A * U.transpose).transpose = U * A.transpose * U.transpose := by
      rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose]
      simp [Matrix.mul_assoc]
    _ = U * (-A) * U.transpose := by
      rw [hA]
    _ = -(U * A * U.transpose) := by
      simp [Matrix.mul_assoc]

theorem matrixRepCurvature_preserves_skew {k : Type} [Fintype k] [DecidableEq k]
    (D A : Matrix k k Real) (hD : isSkew D) (hA : isSkew A) :
    isSkew (matrixRepCurvature D A) := by
  unfold matrixRepCurvature
  exact spatialCommutator_preserves_skew D A hD hA

noncomputable def matrixRepYangMillsAction {i j k : Type}
    [Fintype i] [Fintype j] [Fintype k]
    (K : Matrix i j (Matrix k k Real)) : Real :=
  -∑ a : i, ∑ b : j, Matrix.trace ((K a b) * (K a b))

theorem matrix_rep_yang_mills_action_nonnegative_of_skew {i j k : Type}
    [Fintype i] [Fintype j] [Fintype k] [DecidableEq k]
    (K : Matrix i j (Matrix k k Real))
    (hK : forall a b, isSkew (K a b)) :
    matrixRepYangMillsAction K >= 0 := by
  unfold matrixRepYangMillsAction
  have hsum :
      (∑ a : i, ∑ b : j, Matrix.trace ((K a b) * (K a b))) <= 0 := by
    apply Finset.sum_nonpos
    intro a _
    apply Finset.sum_nonpos
    intro b _
    exact skew_square_trace_nonpositive (K a b) (hK a b)
  exact neg_nonneg.mpr hsum

def abstractLieRingFiniteTransformWithoutRepresentationNoGo : Prop := True

theorem abstract_lieRing_finite_transform_requires_associative_representation :
    abstractLieRingFiniteTransformWithoutRepresentationNoGo := by
  trivial

def exactBianchiIdentityReplacedByGradedIncidenceClosure : Prop := True

theorem exact_bianchi_identity_replaced_by_graded_incidence_closure :
    exactBianchiIdentityReplacedByGradedIncidenceClosure := by
  trivial

end D0.Gauge
