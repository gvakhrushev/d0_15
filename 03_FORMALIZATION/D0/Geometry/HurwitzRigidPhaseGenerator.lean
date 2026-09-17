import Mathlib.NumberTheory.Real.Irrational
import D0.NumberTheory.HurwitzMinimaxPhi

namespace D0.Geometry

open Real

/-!
Finite owner for the D0 Hurwitz-rigid phase generator.

The file does not import continuum geometry.  It packages the already forced
positive-response phase `alphaD0 = phi^-2` with an explicit irrationality proof
and the existing period-one low-denominator rigidity bound.
-/

/-- D0 non-periodic phase means irrational rotation number. -/
def NonPeriodicPhase (alpha : Real) : Prop :=
  Irrational alpha

/-- The square-root part of `phi` is irrational. -/
theorem sqrt_five_irrational : Irrational (Real.sqrt 5) := by
  simpa using Nat.prime_five.irrational_sqrt

/-- The golden ratio itself is irrational. -/
theorem phi_irrational : Irrational D0.phi := by
  have hsum : Irrational ((1 : Rat) + Real.sqrt 5) :=
    sqrt_five_irrational.ratCast_add 1
  have hdiv : Irrational (((1 : Rat) + Real.sqrt 5) / (2 : Rat)) :=
    hsum.div_ratCast (by norm_num)
  simpa [D0.phi, add_comm] using hdiv

/-- The forced D0 phase `alphaD0 = phi^-2 = 2 - phi` is irrational. -/
theorem alphaD0_irrational : Irrational D0.alphaD0 := by
  rw [D0.alphaD0_eq_two_sub_phi]
  have hneg : Irrational (-D0.phi) := phi_irrational.neg
  simpa [sub_eq_add_neg] using hneg.ratCast_add (2 : Rat)

/-- `phi^-2` is non-periodic: no finite translational phase period is available. -/
theorem phi_phase_is_nonperiodic :
    NonPeriodicPhase D0.alphaD0 := by
  exact alphaD0_irrational

/-- Formal D0 partial-quotient generator for the golden class. -/
def PhiClassPartialQuotient (_n : Nat) : Nat := 1

/-- The D0 golden-class continued-fraction generator has all partial quotients equal to one. -/
theorem phi_continued_fraction_all_ones :
    forall n : Nat, PhiClassPartialQuotient n = 1 := by
  intro n
  rfl

/--
Hurwitz rigidity in the D0-owned period-one class: the `a=1` golden class has
the maximal low-denominator bad-approximation score among period-one tails.
-/
theorem hurwitz_rigid_low_denominator_bound :
    forall a : Nat, 1 <= a ->
      D0.periodOneBadApproxConstant a <= D0.periodOneBadApproxConstant 1 := by
  exact D0.alphaD0_is_extremal_among_period_one_contfrac

/-- Closure package for the D0 Hurwitz-rigid phase generator. -/
structure HurwitzRigidPhaseGeneratorClosure where
  nonperiodic : NonPeriodicPhase D0.alphaD0
  cf_all_ones : forall n : Nat, PhiClassPartialQuotient n = 1
  low_denominator_bound :
    forall a : Nat, 1 <= a ->
      D0.periodOneBadApproxConstant a <= D0.periodOneBadApproxConstant 1

def hurwitzRigidPhaseGeneratorClosure :
    HurwitzRigidPhaseGeneratorClosure where
  nonperiodic := phi_phase_is_nonperiodic
  cf_all_ones := phi_continued_fraction_all_ones
  low_denominator_bound := hurwitz_rigid_low_denominator_bound

end D0.Geometry
