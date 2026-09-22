import Mathlib.Tactic

namespace D0.Geometry

noncomputable section

/-!
# Centered Cartan closure no-go: exact L = 5 scalar control

This file isolates the finite scalar obstruction only.  The generator is the local
centered transport G_xi = M_xi D on a five-cycle over rationals.  Two explicit local
generators have a commutator with a nonzero cyclic distance-two matrix entry.

The correction theorem uses an explicit matrix-support predicate for cyclic radius one.
It is not promoted beyond this scalar five-cycle control.
-/

abbrev Cycle5Scalar := Fin 5 → ℚ
abbrev Cycle5ScalarOperator := Cycle5Scalar → Cycle5Scalar

def cycle5Next (i : Fin 5) : Fin 5 :=
  ⟨(i.val + 1) % 5, by omega⟩

def cycle5Prev (i : Fin 5) : Fin 5 :=
  ⟨(i.val + 4) % 5, by omega⟩

/-- L = 5 centered derivative with scale L/2. -/
def centeredDifference5 (f : Cycle5Scalar) : Cycle5Scalar :=
  fun i => (5 / 2 : ℚ) * (f (cycle5Next i) - f (cycle5Prev i))

/-- Scalar centered generator G_xi = M_xi D. -/
def centeredGenerator5 (xi : Cycle5Scalar) : Cycle5ScalarOperator :=
  fun f i => xi i * centeredDifference5 f i

def centeredGeneratorCommutator5 (xi eta : Cycle5Scalar) :
    Cycle5ScalarOperator :=
  fun f =>
    centeredGenerator5 xi (centeredGenerator5 eta f) -
      centeredGenerator5 eta (centeredGenerator5 xi f)

def delta5 (j : Fin 5) : Cycle5Scalar :=
  fun i => if i = j then 1 else 0

def xiWitness5 : Cycle5Scalar := delta5 0
def etaWitness5 : Cycle5Scalar := delta5 1
def distanceTwoBasis5 : Cycle5Scalar := delta5 2

/-- Exact exhibited radius-two entry: row 0, column 2 equals 25/4. -/
theorem centered_commutator_distance_two_entry :
    centeredGeneratorCommutator5 xiWitness5 etaWitness5 distanceTwoBasis5 0 =
      (25 / 4 : ℚ) := by
  native_decide

/-- Every original radius-one centered generator has zero at the same row/column entry. -/
theorem centered_generator_distance_two_entry_zero (zeta : Cycle5Scalar) :
    centeredGenerator5 zeta distanceTwoBasis5 0 = 0 := by
  simp [centeredGenerator5, centeredDifference5, distanceTwoBasis5, delta5,
    cycle5Next, cycle5Prev]

/-- Membership in the original centered-generator family. -/
def IsCenteredGenerator5 (A : Cycle5ScalarOperator) : Prop :=
  ∃ zeta : Cycle5Scalar, A = centeredGenerator5 zeta

/-- Capstone: the original local centered-generator family is not commutator-closed. -/
theorem centered_generator_family_not_closed :
    ¬ IsCenteredGenerator5
      (centeredGeneratorCommutator5 xiWitness5 etaWitness5) := by
  rintro ⟨zeta, hzeta⟩
  have hentry := congrFun
    (congrFun hzeta distanceTwoBasis5) (0 : Fin 5)
  rw [centered_commutator_distance_two_entry,
    centered_generator_distance_two_entry_zero zeta] at hentry
  norm_num at hentry

/-- Cyclic radius-one relation on the five-site control. -/
def Cycle5WithinRadiusOne (i j : Fin 5) : Prop :=
  j = i ∨ j = cycle5Next i ∨ j = cycle5Prev i

/-- Matrix support class for a genuine radius-one scalar operator. -/
def HasCycle5RadiusOneSupport (C : Cycle5ScalarOperator) : Prop :=
  ∀ i j, ¬ Cycle5WithinRadiusOne i j → C (delta5 j) i = 0

theorem distanceTwo_not_radius_one :
    ¬ Cycle5WithinRadiusOne (0 : Fin 5) (2 : Fin 5) := by
  simp [Cycle5WithinRadiusOne, cycle5Next, cycle5Prev]

def operatorAdd5 (A B : Cycle5ScalarOperator) : Cycle5ScalarOperator :=
  fun f => A f + B f

/-- A first-order correction with actual cyclic radius-one matrix support cannot cancel
the exhibited radius-two commutator component. -/
theorem radius_one_correction_cannot_cancel_distance_two
    (C : Cycle5ScalarOperator)
    (hC : HasCycle5RadiusOneSupport C) :
    operatorAdd5
      (centeredGeneratorCommutator5 xiWitness5 etaWitness5) C
      distanceTwoBasis5 0 ≠ 0 := by
  have hzero : C distanceTwoBasis5 0 = 0 := by
    exact hC 0 2 distanceTwo_not_radius_one
  simp [operatorAdd5, Pi.add_apply, centered_commutator_distance_two_entry, hzero]

end

end D0.Geometry
