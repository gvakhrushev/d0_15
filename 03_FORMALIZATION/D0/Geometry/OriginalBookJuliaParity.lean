import D0.Geometry.OriginalBookCreatorParity
import D0.Geometry.OriginalBookJuliaWords
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute
import Mathlib.Tactic

/-!
# Source parity through the exact Julia operands

Pinned sources are uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 75-87, and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 95-159. The parity operator and four odd creators use the source/Fock
bridge. The analytic boost, real parameter, four mode phases, and operands are
exactly the previously proved source definitions. This file carries parity
through the original positive CFC roots; it does not assume effect ranks or
physical admission.
-/
open D0
open Matrix
open NormedSpace
open scoped MatrixOrder ComplexOrder Matrix.Norms.Operator
open D0.Geometry.OriginalBookCreatorParity
open D0.Geometry.OriginalBookCreatorBridge
open D0.Geometry.OriginalBookBoost
open D0.Geometry.CubicExponential
open D0.Geometry.OriginalBookStaticRoots
open D0.Geometry.OriginalBookJuliaWords

namespace D0.Geometry.OriginalBookJuliaParity

/-- Even matrices commute with the actual typed Fock parity. -/
def IsEven (X : Operator) : Prop := Commute sourceParity X
/-- Odd matrices anticommute with the actual typed Fock parity. -/
def IsOdd (X : Operator) : Prop := sourceParity * X = -(X * sourceParity)

lemma odd_star {X : Operator} (h : IsOdd X) : IsOdd Xᴴ := by
  have hs := congrArg Matrix.conjTranspose h
  simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_neg, sourceParity_hermitian] at hs
  unfold IsOdd
  rw [hs]
  simp

lemma odd_mul_odd {X Y : Operator} (hx : IsOdd X) (hy : IsOdd Y) : IsEven (X * Y) := by
  unfold IsEven IsOdd at *
  change sourceParity * (X * Y) = (X * Y) * sourceParity
  calc
    _ = (sourceParity * X) * Y := by simp [Matrix.mul_assoc]
    _ = (-(X * sourceParity)) * Y := by rw [hx]
    _ = -(X * (sourceParity * Y)) := by simp [Matrix.mul_assoc]
    _ = -(X * (-(Y * sourceParity))) := by rw [hy]
    _ = (X * Y) * sourceParity := by simp [Matrix.mul_assoc]

lemma odd_mul_even {X Y : Operator} (hx : IsOdd X) (hy : IsEven Y) : IsOdd (X * Y) := by
  unfold IsOdd at *
  change sourceParity * (X * Y) = -((X * Y) * sourceParity)
  calc
    _ = (sourceParity * X) * Y := by simp [Matrix.mul_assoc]
    _ = (-(X * sourceParity)) * Y := by rw [hx]
    _ = -(X * (sourceParity * Y)) := by simp [Matrix.mul_assoc]
    _ = -(X * (Y * sourceParity)) := by rw [hy.eq]
    _ = -((X * Y) * sourceParity) := by simp [Matrix.mul_assoc]

lemma even_mul_odd {X Y : Operator} (hx : IsEven X) (hy : IsOdd Y) : IsOdd (X * Y) := by
  unfold IsOdd at *
  change sourceParity * (X * Y) = -((X * Y) * sourceParity)
  calc
    _ = (sourceParity * X) * Y := by simp [Matrix.mul_assoc]
    _ = (X * sourceParity) * Y := by rw [hx.eq]
    _ = X * (sourceParity * Y) := by simp [Matrix.mul_assoc]
    _ = X * (-(Y * sourceParity)) := by rw [hy]
    _ = -((X * Y) * sourceParity) := by simp [Matrix.mul_assoc]

lemma odd_neg {X : Operator} (hx : IsOdd X) : IsOdd (-X) := by
  unfold IsOdd at *
  simpa using congrArg Neg.neg hx

lemma odd_smul_complex (c : ℂ) {X : Operator} (hx : IsOdd X) : IsOdd (c • X) := by
  unfold IsOdd at *
  simpa [Matrix.mul_smul, Matrix.smul_mul] using congrArg (fun M : Operator => c • M) hx

lemma odd_smul_real (c : ℝ) {X : Operator} (hx : IsOdd X) : IsOdd (c • X) := by
  unfold IsOdd at *
  simpa [Matrix.mul_smul, Matrix.smul_mul] using congrArg (fun M : Operator => c • M) hx

lemma even_star {X : Operator} (hx : IsEven X) : IsEven Xᴴ := by
  have hs := congrArg Matrix.conjTranspose hx.eq
  simp only [Matrix.conjTranspose_mul, sourceParity_hermitian] at hs
  exact hs.symm

/-- The exact source boost generator contains two creators and is even. -/
theorem sourceGenerator_even : IsEven sourceComplexGenerator := by
  rw [sourceComplexGenerator_eq_creators]
  exact (odd_mul_odd (creator_odd A) (odd_star (creator_odd D))).add_right
    (odd_mul_odd (creator_odd D) (odd_star (creator_odd A)))

/-- Evenness holds for the actual source exponential, without a spectral assumption. -/
theorem sourceBoost_even : IsEven (exp (sourceTheta • sourceComplexGenerator)) := by
  exact (sourceGenerator_even.smul_right sourceTheta).exp_right

/-- The unphased baseline source operand is odd. -/
theorem sourceBase_odd (r : Role) : IsOdd (sourceBase r) := by
  exact odd_smul_real _ (creator_odd r)

/-- The actual phased and boosted source operand is odd for every role. -/
theorem sourceAnalyticOperand_odd (r : Role) : IsOdd (sourceAnalyticOperand r) := by
  unfold sourceAnalyticOperand
  apply odd_smul_complex
  apply odd_mul_even (odd_smul_complex _ (creator_odd r))
  split_ifs
  · exact sourceBoost_even
  · exact Commute.one_right _

/-- A true positive defect root remains even by the continuous functional calculus. -/
theorem sqrt_even {X : Operator} (hx : IsEven X) : IsEven (CFC.sqrt X) := by
  exact (hx.symm.cfcₙ_nnreal NNReal.sqrt).symm

/-- Every actual Julia left root is parity even. -/
theorem liveLeft_even (r : Role) : IsEven (liveLeft r) := by
  rw [liveLeft_is_source_root]
  apply sqrt_even
  exact (Commute.one_right _).sub_right
    (odd_mul_odd (sourceAnalyticOperand_odd r) (odd_star (sourceAnalyticOperand_odd r)))

/-- Every actual Julia right root is parity even. -/
theorem liveRight_even (r : Role) : IsEven (liveRight r) := by
  rw [liveRight_is_source_root]
  apply sqrt_even
  exact (Commute.one_right _).sub_right
    (odd_mul_odd (odd_star (sourceAnalyticOperand_odd r)) (sourceAnalyticOperand_odd r))

/-- Both unphased baseline Julia roots are even as well. -/
theorem baseLeft_even (r : Role) : IsEven (baseLeft r) := by
  rw [baseLeft_is_source_root]
  apply sqrt_even
  exact (Commute.one_right _).sub_right
    (odd_mul_odd (sourceBase_odd r) (odd_star (sourceBase_odd r)))

theorem baseRight_even (r : Role) : IsEven (baseRight r) := by
  rw [baseRight_is_source_root]
  apply sqrt_even
  exact (Commute.one_right _).sub_right
    (odd_mul_odd (odd_star (sourceBase_odd r)) (sourceBase_odd r))

end D0.Geometry.OriginalBookJuliaParity
