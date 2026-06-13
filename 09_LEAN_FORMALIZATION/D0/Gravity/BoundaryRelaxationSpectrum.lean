import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Multiset.Basic

namespace D0

structure BoundaryRelaxationOperator where
  dim : Nat
  dim_positive : 0 < dim
  T : Matrix (Fin dim) (Fin dim) Complex
  dissipative : Prop
  dissipativeProof : dissipative

def BoundaryModeMultiset (op : BoundaryRelaxationOperator) : Multiset Complex :=
  Multiset.ofList ((List.finRange op.dim).map (fun i => op.T i i))

def BoundarySpectrum (op : BoundaryRelaxationOperator) : Multiset Complex :=
  BoundaryModeMultiset op

def DampedMode (omega : Complex) : Prop :=
  omega.im <= 0

theorem finite_boundary_has_finite_mode_multiset
    (op : BoundaryRelaxationOperator) :
    exists modes : Multiset Complex, BoundarySpectrum op = modes := by
  exact ⟨BoundarySpectrum op, rfl⟩

structure QNMDelta0PassportInput where
  preregisteredD0Ladder : Prop
  extractedQNMTable : Prop
  baselineComparison : Prop

def QNMDelta0PassportReady (p : QNMDelta0PassportInput) : Prop :=
  p.preregisteredD0Ladder /\ p.extractedQNMTable /\ p.baselineComparison

theorem qnm_passport_requires_preregistered_inputs
    (p : QNMDelta0PassportInput) :
    QNMDelta0PassportReady p ->
      p.preregisteredD0Ladder /\ p.extractedQNMTable := by
  intro h
  exact ⟨h.1, h.2.1⟩

end D0
