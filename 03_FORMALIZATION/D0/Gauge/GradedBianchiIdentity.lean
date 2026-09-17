import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.ArchiveCommutatorOperators
import D0.Topology.GradedIncidenceComplex

namespace D0.Gauge

open D0.Algebra
open D0.Topology

theorem abelian_bianchi_exact
    (C : GradedCellComplex) (A : C.V -> Real) (f : C.F) :
    d1 C (d0 C A) f = 0 := by
  exact discrete_exact_bianchi C A f

theorem graded_bianchi_exact
    (C : GradedCellComplex3) (c : C.C3) (e : C.E) :
    (Finset.univ.sum fun f => C.boundary3 c f * C.boundary2 f e) = 0 := by
  exact D0.Topology.graded_bianchi_exact C c e

def fin2SkewD : Matrix (Fin 2) (Fin 2) Real := fun i j =>
  if i.val = 0 /\ j.val = 1 then 1
  else if i.val = 1 /\ j.val = 0 then -1
  else 0

def fin2A : Matrix (Fin 2) (Fin 2) Real := fun i j =>
  if i.val = 0 /\ j.val = 0 then 1 else 0

theorem fin2SkewD_is_skew :
    fin2SkewD.transpose = -fin2SkewD := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [fin2SkewD, Matrix.transpose_apply]

theorem ungraded_bianchi_residual_counterexample_fin2 :
    exists D A : Matrix (Fin 2) (Fin 2) Real,
      D.transpose = -D /\
      Not (D0.Algebra.commutator D (D0.Algebra.commutator D A) = 0) := by
  refine ⟨fin2SkewD, fin2A, fin2SkewD_is_skew, ?_⟩
  intro h
  have h_entry := congr_fun (congr_fun h (0 : Fin 2)) (0 : Fin 2)
  norm_num [D0.Algebra.commutator, fin2SkewD, fin2A, Matrix.mul_apply,
    Fin.sum_univ_two] at h_entry

end D0.Gauge
