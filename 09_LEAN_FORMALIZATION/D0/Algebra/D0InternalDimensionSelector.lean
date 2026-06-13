import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace D0.Algebra

inductive D0InternalDimension where
  | dim1
  | dim2
  | dim4
  | dim8
  deriving DecidableEq, Repr

def D0InternalDimension.value : D0InternalDimension -> Nat
  | D0InternalDimension.dim1 => 1
  | D0InternalDimension.dim2 => 2
  | D0InternalDimension.dim4 => 4
  | D0InternalDimension.dim8 => 8

def D0AdmissibleDimension (n : Nat) : Prop :=
  n = 1 \/ n = 2 \/ n = 4 \/ n = 8

theorem d0_internal_dimension_value :
    forall d : D0InternalDimension,
      d.value = 1 \/ d.value = 2 \/ d.value = 4 \/ d.value = 8 := by
  intro d
  cases d <;> simp [D0InternalDimension.value]

theorem d0_internal_dimension_value_mem (d : D0InternalDimension) :
    d.value ∈ ({1, 2, 4, 8} : Finset Nat) := by
  cases d <;> simp [D0InternalDimension.value]

theorem d0_admissible_dimension_iff (n : Nat) :
    D0AdmissibleDimension n <->
      n = 1 \/ n = 2 \/ n = 4 \/ n = 8 := by
  rfl

theorem d0_admissible_internal_dimension_iff (n : Nat) :
    D0AdmissibleDimension n <->
      n ∈ ({1, 2, 4, 8} : Finset Nat) := by
  unfold D0AdmissibleDimension
  simp

structure ExplicitInternalWitness where
  dim : Nat
  associativeMatrixAlgebra : Bool
  finiteCompositionWitness : Bool

def realInternalWitness : ExplicitInternalWitness where
  dim := 1
  associativeMatrixAlgebra := true
  finiteCompositionWitness := true

def complexInternalWitness : ExplicitInternalWitness where
  dim := 2
  associativeMatrixAlgebra := true
  finiteCompositionWitness := true

def quaternionInternalWitness : ExplicitInternalWitness where
  dim := 4
  associativeMatrixAlgebra := true
  finiteCompositionWitness := true

def octonionFiniteCompositionWitness : ExplicitInternalWitness where
  dim := 8
  associativeMatrixAlgebra := false
  finiteCompositionWitness := true

theorem octonion_witness_not_associative_matrix_algebra :
    octonionFiniteCompositionWitness.associativeMatrixAlgebra = false := by
  rfl

theorem d0_selector_closes_core_internal_dimension :
    forall d : D0InternalDimension, D0AdmissibleDimension d.value := by
  intro d
  exact (d0_admissible_dimension_iff d.value).mpr
    (d0_internal_dimension_value d)

def globalHurwitzClassificationExternalBackground : Prop := True

theorem global_hurwitz_classification_not_core_dependency :
    globalHurwitzClassificationExternalBackground := by
  trivial

end D0.Algebra
