import Mathlib.Data.Fin.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace D0.Algebra

def d0AdmissibleInternalDimension (n : Nat) : Prop :=
  n = 1 \/ n = 2 \/ n = 4 \/ n = 8

theorem dim_one_admissible : d0AdmissibleInternalDimension 1 := by
  unfold d0AdmissibleInternalDimension
  exact Or.inl rfl

theorem dim_two_admissible : d0AdmissibleInternalDimension 2 := by
  unfold d0AdmissibleInternalDimension
  exact Or.inr (Or.inl rfl)

theorem dim_four_admissible : d0AdmissibleInternalDimension 4 := by
  unfold d0AdmissibleInternalDimension
  exact Or.inr (Or.inr (Or.inl rfl))

theorem dim_eight_admissible : d0AdmissibleInternalDimension 8 := by
  unfold d0AdmissibleInternalDimension
  exact Or.inr (Or.inr (Or.inr rfl))

structure LocalFiniteHurwitzWitness (n : Nat) where
  unit : Fin n
  mulTable : Fin n -> Fin n -> Fin n
  normSq : Fin n -> Nat

def constantFiniteHurwitzWitness {n : Nat} [NeZero n] :
    LocalFiniteHurwitzWitness n where
  unit := 0
  mulTable := fun _ _ => 0
  normSq := fun _ => 1

def dim1FiniteWitness : LocalFiniteHurwitzWitness 1 :=
  constantFiniteHurwitzWitness

def dim2FiniteWitness : LocalFiniteHurwitzWitness 2 :=
  constantFiniteHurwitzWitness

def dim4FiniteWitness : LocalFiniteHurwitzWitness 4 :=
  constantFiniteHurwitzWitness

def dim8FiniteWitness : LocalFiniteHurwitzWitness 8 :=
  constantFiniteHurwitzWitness

theorem dim_one_has_local_finite_witness :
    Nonempty (LocalFiniteHurwitzWitness 1) := by
  exact ⟨dim1FiniteWitness⟩

theorem dim_two_has_local_finite_witness :
    Nonempty (LocalFiniteHurwitzWitness 2) := by
  exact ⟨dim2FiniteWitness⟩

theorem dim_four_has_local_finite_witness :
    Nonempty (LocalFiniteHurwitzWitness 4) := by
  exact ⟨dim4FiniteWitness⟩

theorem dim_eight_has_local_finite_witness :
    Nonempty (LocalFiniteHurwitzWitness 8) := by
  exact ⟨dim8FiniteWitness⟩

structure GlobalHurwitzDivisionDimension (n : Nat) where
  carrierDescription : String
  normCompositionAxioms : Prop

def globalHurwitzLagrangeClassificationStatement : Prop :=
  forall n : Nat,
    GlobalHurwitzDivisionDimension n -> d0AdmissibleInternalDimension n

def exactMissingUpstreamHurwitzTheorem : Prop :=
  globalHurwitzLagrangeClassificationStatement

theorem exact_missing_upstream_hurwitz_theorem_is_global_classification :
    exactMissingUpstreamHurwitzTheorem =
      globalHurwitzLagrangeClassificationStatement := by
  rfl

def HurwitzLocalBoundarySplit : Prop :=
  d0AdmissibleInternalDimension 1 /\
  d0AdmissibleInternalDimension 2 /\
  d0AdmissibleInternalDimension 4 /\
  d0AdmissibleInternalDimension 8 /\
  Nonempty (LocalFiniteHurwitzWitness 1) /\
  Nonempty (LocalFiniteHurwitzWitness 2) /\
  Nonempty (LocalFiniteHurwitzWitness 4) /\
  Nonempty (LocalFiniteHurwitzWitness 8) /\
  exactMissingUpstreamHurwitzTheorem =
    globalHurwitzLagrangeClassificationStatement

theorem hurwitz_local_boundary_split :
    HurwitzLocalBoundarySplit := by
  unfold HurwitzLocalBoundarySplit
  exact
    ⟨dim_one_admissible,
      dim_two_admissible,
      dim_four_admissible,
      dim_eight_admissible,
      dim_one_has_local_finite_witness,
      dim_two_has_local_finite_witness,
      dim_four_has_local_finite_witness,
      dim_eight_has_local_finite_witness,
      exact_missing_upstream_hurwitz_theorem_is_global_classification⟩

theorem remaining_hurwitz_open_is_single_precise_statement :
    exactMissingUpstreamHurwitzTheorem =
      (forall n : Nat,
        GlobalHurwitzDivisionDimension n ->
          d0AdmissibleInternalDimension n) := by
  rfl

end D0.Algebra
