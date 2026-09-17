import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Topology

structure GradedCellComplex where
  V : Type
  E : Type
  F : Type
  fintypeV : Fintype V
  fintypeE : Fintype E
  fintypeF : Fintype F
  boundary1 : Matrix E V Real
  boundary2 : Matrix F E Real
  boundary_nilpotency :
    forall f : F, forall v : V,
      (Finset.univ.sum fun e => boundary2 f e * boundary1 e v) = 0

attribute [instance] GradedCellComplex.fintypeV
attribute [instance] GradedCellComplex.fintypeE
attribute [instance] GradedCellComplex.fintypeF

noncomputable def d0 (C : GradedCellComplex) (A : C.V -> Real) :
    C.E -> Real :=
  fun e => Finset.univ.sum fun v => C.boundary1 e v * A v

noncomputable def d1 (C : GradedCellComplex) (B : C.E -> Real) :
    C.F -> Real :=
  fun f => Finset.univ.sum fun e => C.boundary2 f e * B e

theorem graded_nilpotency (C : GradedCellComplex) (f : C.F) (v : C.V) :
    (Finset.univ.sum fun e => C.boundary2 f e * C.boundary1 e v) = 0 := by
  exact C.boundary_nilpotency f v

theorem discrete_exact_bianchi
    (C : GradedCellComplex) (A : C.V -> Real) (f : C.F) :
    d1 C (d0 C A) f = 0 := by
  unfold d1 d0
  calc
    (Finset.univ.sum fun e =>
      C.boundary2 f e * (Finset.univ.sum fun v => C.boundary1 e v * A v))
        = Finset.univ.sum fun e =>
            Finset.univ.sum fun v =>
              C.boundary2 f e * (C.boundary1 e v * A v) := by
          simp [Finset.mul_sum]
    _ = Finset.univ.sum fun v =>
          Finset.univ.sum fun e =>
            C.boundary2 f e * (C.boundary1 e v * A v) := by
          rw [Finset.sum_comm]
    _ = Finset.univ.sum fun v =>
          Finset.univ.sum fun e =>
            (C.boundary2 f e * C.boundary1 e v) * A v := by
          apply Finset.sum_congr rfl
          intro v _
          apply Finset.sum_congr rfl
          intro e _
          ring
    _ = Finset.univ.sum fun v =>
          (Finset.univ.sum fun e => C.boundary2 f e * C.boundary1 e v) * A v := by
          simp [Finset.sum_mul]
    _ = Finset.univ.sum fun v => 0 * A v := by
          apply Finset.sum_congr rfl
          intro v _
          rw [C.boundary_nilpotency f v]
    _ = 0 := by
          simp

structure GradedCellComplex3 extends GradedCellComplex where
  C3 : Type
  fintypeC3 : Fintype C3
  boundary3 : Matrix C3 F Real
  boundary_nilpotency2 :
    forall c : C3, forall e : E,
      (Finset.univ.sum fun f => boundary3 c f * boundary2 f e) = 0

attribute [instance] GradedCellComplex3.fintypeC3

theorem graded_bianchi_exact (C : GradedCellComplex3) (c : C.C3) (e : C.E) :
    (Finset.univ.sum fun f => C.boundary3 c f * C.boundary2 f e) = 0 := by
  exact C.boundary_nilpotency2 c e

end D0.Topology
