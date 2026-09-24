import Mathlib.Tactic
import D0.Geometry.A4DSecondOrderCartanWitness

namespace D0.Geometry

open scoped BigOperators

set_option maxRecDepth 4096

/-!
# Output-site-local scalar advective groupoid two-jets

All transport conclusions in this file are scoped to the explicit output-site
parameter-local class `g_ξ(e) = M_ξ D_e`, with flat value `D_0 = D`. The
cell-support contradiction concerns direct elementary-edge energies on the
original scalar carrier only.
-/

abbrev AdvectiveFiveMatrix := Matrix (Fin 5) (Fin 5) ℚ
abbrev AdvectiveFiveVector := Fin 5 → ℚ

def advectiveFiveMul (f : AdvectiveFiveVector) : AdvectiveFiveMatrix :=
  Matrix.diagonal f

def advectiveFiveForwardDifference (ξ : AdvectiveFiveVector) : AdvectiveFiveVector :=
  fun x => (5 : ℚ) * (ξ (fiveCycleSucc x) - ξ x)

def advectiveFiveH0 (h : AdvectiveFiveVector) : AdvectiveFiveMatrix :=
  (1 / 2 : ℚ) •
    (advectiveFiveMul h * fiveCycleShift +
      fiveCycleShift.transpose * advectiveFiveMul h)

def advectiveFiveGenerator (ξ : AdvectiveFiveVector) : AdvectiveFiveMatrix :=
  advectiveFiveMul ξ * fiveCycleD

def advectiveFiveBackgroundDerivative (ξ : AdvectiveFiveVector)
    (h : AdvectiveFiveVector) : AdvectiveFiveMatrix :=
  -(advectiveFiveMul ξ * advectiveFiveH0 h * fiveCycleD)

def advectiveFiveSecondJet (ξ : AdvectiveFiveVector) : AdvectiveFiveMatrix :=
  advectiveFiveMul (fun x => ξ x ^ 2) * fiveCycleD * fiveCycleD

def fiveCycleD2 : AdvectiveFiveMatrix := fun i j =>
  if i = j then -(25 / 2 : ℚ)
  else if j = ⟨(i.val + 2) % 5, by omega⟩ ∨
      j = ⟨(i.val + 3) % 5, by omega⟩ then 25 / 4
  else 0

/-- Literal output-site parameter locality for a family of scalar generators. -/
def OutputSiteParameterLocal
    (g : AdvectiveFiveVector → AdvectiveFiveMatrix → AdvectiveFiveMatrix) : Prop :=
  ∀ e, ∃ Dₑ, ∀ ξ, g ξ e = advectiveFiveMul ξ * Dₑ

theorem fiveCycleD_skew : fiveCycleD.transpose = -fiveCycleD := by
  ext x y
  fin_cases x <;> fin_cases y <;>
    norm_num [fiveCycleD, fiveCycleShift, fiveCycleSucc, Fin.ext_iff]

private theorem advectiveFin5Sum (f : Fin 5 → ℚ) :
    (∑ i : Fin 5, f i) = f 0 + f 1 + f 2 + f 3 + f 4 := by
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  norm_num [Fin.succ]
  abel

private theorem advectiveFin5MatrixMulApply
    (A B : AdvectiveFiveMatrix) (i j : Fin 5) :
    (A * B) i j =
      A i 0 * B 0 j + A i 1 * B 1 j + A i 2 * B 2 j +
        A i 3 * B 3 j + A i 4 * B 4 j := by
  rw [Matrix.mul_apply, advectiveFin5Sum]

theorem fiveCycleD_squared : fiveCycleD * fiveCycleD = fiveCycleD2 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    rw [advectiveFin5MatrixMulApply] <;>
    norm_num [fiveCycleD, fiveCycleD2, fiveCycleShift, fiveCycleSucc,
      Fin.ext_iff, Fin.val_succ]

theorem fiveCycleD_apply (i j : Fin 5) :
    fiveCycleD i j = (5 / 2 : ℚ) * (if j = fiveCycleSucc i then 1 else 0) -
      (5 / 2 : ℚ) * (if i = fiveCycleSucc j then 1 else 0) := by
  simp [fiveCycleD, fiveCycleShift, fiveCycleSucc, Matrix.sub_apply,
    Matrix.transpose_apply] <;> split_ifs <;> ring

theorem advectiveFiveH0_apply (h : AdvectiveFiveVector) (i j : Fin 5) :
    advectiveFiveH0 h i j =
      (h i / 2) * (if j = fiveCycleSucc i then 1 else 0) +
      (h j / 2) * (if i = fiveCycleSucc j then 1 else 0) := by
  simp [advectiveFiveH0, advectiveFiveMul, Matrix.diagonal_mul,
    Matrix.mul_diagonal, fiveCycleShift, fiveCycleSucc,
    Matrix.transpose_apply, Matrix.add_apply, Matrix.smul_apply] <;> split_ifs <;> ring

/-- The finite-cycle commutator identity `[M_ξ,D] = -H₀(Δξ)`. -/
theorem advectiveFive_commutator (ξ : AdvectiveFiveVector) :
    advectiveFiveMul ξ * fiveCycleD - fiveCycleD * advectiveFiveMul ξ =
      -advectiveFiveH0 (advectiveFiveForwardDifference ξ) := by
  ext i j
  change ((Matrix.diagonal ξ * fiveCycleD -
      fiveCycleD * Matrix.diagonal ξ) i j) =
    -advectiveFiveH0 (advectiveFiveForwardDifference ξ) i j
  rw [Matrix.sub_apply, Matrix.diagonal_mul, Matrix.mul_diagonal]
  change ξ i * fiveCycleD i j - fiveCycleD i j * ξ j =
    -advectiveFiveH0 (advectiveFiveForwardDifference ξ) i j
  rw [fiveCycleD_apply, advectiveFiveH0_apply]
  simp only [advectiveFiveForwardDifference]
  fin_cases i <;> fin_cases j <;> norm_num [fiveCycleSucc] <;> ring_nf

theorem advectiveFiveH0_eq_neg_generator_sym (ξ : AdvectiveFiveVector) :
    advectiveFiveH0 (advectiveFiveForwardDifference ξ) =
      -(advectiveFiveGenerator ξ + (advectiveFiveGenerator ξ).transpose) := by
  have hc := advectiveFive_commutator ξ
  have hd : (advectiveFiveGenerator ξ).transpose =
      -(fiveCycleD * advectiveFiveMul ξ) := by
    change (advectiveFiveMul ξ * fiveCycleD).transpose =
      -(fiveCycleD * advectiveFiveMul ξ)
    rw [Matrix.transpose_mul, fiveCycleD_skew]
    have hM : (advectiveFiveMul ξ).transpose = advectiveFiveMul ξ := by
      change (Matrix.diagonal ξ).transpose = Matrix.diagonal ξ
      exact Matrix.diagonal_transpose _
    rw [hM, neg_mul]
  have hrel : advectiveFiveGenerator ξ +
      (advectiveFiveGenerator ξ).transpose =
      -advectiveFiveH0 (advectiveFiveForwardDifference ξ) := by
    rw [hd]
    simpa [advectiveFiveGenerator, sub_eq_add_neg] using hc
  simpa using congrArg (fun A : AdvectiveFiveMatrix => -A) hrel |>.symm

/-- The mixed-constant groupoid condition forces the derivative of `D_e`
inside the output-site-local class to `[M_ξ D,D] = -H₀(Δξ)D`. -/
theorem outputSiteLocal_forced_differential_derivative
    (g : AdvectiveFiveVector → AdvectiveFiveMatrix → AdvectiveFiveMatrix)
    (hout : OutputSiteParameterLocal g)
    (ξ : AdvectiveFiveVector)
    (Ddot : AdvectiveFiveMatrix)
    (hmixedConstant : Ddot =
      advectiveFiveGenerator ξ * fiveCycleD - fiveCycleD * advectiveFiveGenerator ξ) :
    Ddot = -advectiveFiveH0 (advectiveFiveForwardDifference ξ) * fiveCycleD := by
  rw [hmixedConstant]
  unfold advectiveFiveGenerator
  have hcomm := advectiveFive_commutator ξ
  calc
    advectiveFiveMul ξ * fiveCycleD * fiveCycleD -
        fiveCycleD * (advectiveFiveMul ξ * fiveCycleD) =
        (advectiveFiveMul ξ * fiveCycleD -
          fiveCycleD * advectiveFiveMul ξ) * fiveCycleD := by
            calc
              _ = (advectiveFiveMul ξ * fiveCycleD) * fiveCycleD -
                  (fiveCycleD * advectiveFiveMul ξ) * fiveCycleD := by
                    congr 1 <;> simp only [← Matrix.mul_assoc]
              _ = (advectiveFiveMul ξ * fiveCycleD -
                  fiveCycleD * advectiveFiveMul ξ) * fiveCycleD := by
                    rw [Matrix.sub_mul]
    _ = -advectiveFiveH0 (advectiveFiveForwardDifference ξ) * fiveCycleD :=
      congrArg (fun A : AdvectiveFiveMatrix => A * fiveCycleD) hcomm

/-- The forced particular mixed derivative. -/
theorem outputSiteLocal_forced_background_derivative
    (ξ : AdvectiveFiveVector) (h : AdvectiveFiveVector)
    (B : AdvectiveFiveMatrix)
    (hforced : B = -(advectiveFiveMul ξ *
      advectiveFiveH0 h * fiveCycleD)) :
    B = advectiveFiveBackgroundDerivative ξ h := by
  change B = -(advectiveFiveMul ξ * advectiveFiveH0 h * fiveCycleD)
  exact hforced

/-- The output-site-local particular derivative obeys the complete mixed
two-parameter cocycle equation. -/
theorem advectiveFive_mixed_cocycle (ξ ζ : AdvectiveFiveVector) :
    advectiveFiveBackgroundDerivative ζ (advectiveFiveForwardDifference ξ) -
      advectiveFiveBackgroundDerivative ξ (advectiveFiveForwardDifference ζ) +
      (advectiveFiveGenerator ζ * advectiveFiveGenerator ξ -
        advectiveFiveGenerator ξ * advectiveFiveGenerator ζ) = 0 := by
  unfold advectiveFiveBackgroundDerivative
  rw [advectiveFiveH0_eq_neg_generator_sym ξ,
    advectiveFiveH0_eq_neg_generator_sym ζ]
  have hdξ : (advectiveFiveGenerator ξ).transpose =
      -(fiveCycleD * advectiveFiveMul ξ) := by
    unfold advectiveFiveGenerator
    rw [Matrix.transpose_mul, fiveCycleD_skew]
    have hM : (advectiveFiveMul ξ).transpose = advectiveFiveMul ξ := by
      unfold advectiveFiveMul
      exact Matrix.diagonal_transpose _
    rw [hM, neg_mul]
  have hdζ : (advectiveFiveGenerator ζ).transpose =
      -(fiveCycleD * advectiveFiveMul ζ) := by
    unfold advectiveFiveGenerator
    rw [Matrix.transpose_mul, fiveCycleD_skew]
    have hM : (advectiveFiveMul ζ).transpose = advectiveFiveMul ζ := by
      unfold advectiveFiveMul
      exact Matrix.diagonal_transpose _
    rw [hM, neg_mul]
  rw [hdξ, hdζ]
  unfold advectiveFiveGenerator
  have hdiagcomm : advectiveFiveMul ζ * advectiveFiveMul ξ =
      advectiveFiveMul ξ * advectiveFiveMul ζ := by
    simp [advectiveFiveMul, Matrix.diagonal_mul_diagonal, mul_comm]
  simp only [neg_mul, mul_neg, neg_neg, mul_add, add_mul]
  calc
    _ = ((advectiveFiveMul ζ * advectiveFiveMul ξ -
        advectiveFiveMul ξ * advectiveFiveMul ζ) * fiveCycleD) * fiveCycleD := by
          noncomm_ring
    _ = 0 := by rw [hdiagcomm]; simp

/-- In the output-site-local class, the forced generator derivative and the
mixed law give `K_ξ = G_ξ² + B_adv(ξ,Δξ) = M_(ξ²)D²`. -/
theorem outputSiteLocal_forced_second_jet
    (g : AdvectiveFiveVector → AdvectiveFiveMatrix → AdvectiveFiveMatrix)
    (hout : OutputSiteParameterLocal g) (ξ : AdvectiveFiveVector) :
    advectiveFiveGenerator ξ * advectiveFiveGenerator ξ +
        advectiveFiveBackgroundDerivative ξ (advectiveFiveForwardDifference ξ) =
      advectiveFiveSecondJet ξ := by
  let _outputLocalityAtFlat := hout 0
  unfold advectiveFiveBackgroundDerivative
  rw [advectiveFiveH0_eq_neg_generator_sym ξ]
  have hd : (advectiveFiveGenerator ξ).transpose =
      -(fiveCycleD * advectiveFiveMul ξ) := by
    unfold advectiveFiveGenerator
    rw [Matrix.transpose_mul, fiveCycleD_skew]
    have hM : (advectiveFiveMul ξ).transpose = advectiveFiveMul ξ := by
      unfold advectiveFiveMul
      exact Matrix.diagonal_transpose _
    rw [hM, neg_mul]
  rw [hd]
  unfold advectiveFiveGenerator
  calc
    _ = (advectiveFiveMul ξ * advectiveFiveMul ξ * fiveCycleD) * fiveCycleD := by
      noncomm_ring
    _ = advectiveFiveSecondJet ξ := by
      unfold advectiveFiveSecondJet advectiveFiveMul
      calc
        (Matrix.diagonal ξ * Matrix.diagonal ξ * fiveCycleD) * fiveCycleD =
            (Matrix.diagonal (fun x => ξ x * ξ x) * fiveCycleD) * fiveCycleD := by
              rw [Matrix.diagonal_mul_diagonal]
        _ = (Matrix.diagonal (fun x => ξ x ^ 2) * fiveCycleD) * fiveCycleD := by
              congr 2
              funext x
              ring

/-- Complete forced `K` matrix at `L=5` for `ξ=δ₀`, in cyclic site order. -/
def fiveCycleAdvectiveDeltaK : AdvectiveFiveMatrix := fun i j =>
  if i.val = 0 ∧ j.val = 0 then -(25 / 2 : ℚ)
  else if i.val = 0 ∧ (j.val = 2 ∨ j.val = 3) then 25 / 4
  else 0

theorem fiveCycleAdvectiveDeltaK_exact :
    advectiveFiveSecondJet fiveCycleDelta = fiveCycleAdvectiveDeltaK := by
  calc
    advectiveFiveSecondJet fiveCycleDelta =
        advectiveFiveMul (fun x => fiveCycleDelta x ^ 2) * fiveCycleD2 := by
      unfold advectiveFiveSecondJet
      rw [Matrix.mul_assoc, fiveCycleD_squared]
    _ = fiveCycleAdvectiveDeltaK := by
      ext i j
      change ((Matrix.diagonal (fun x => fiveCycleDelta x ^ 2) *
        fiveCycleD2) i j) = _
      rw [Matrix.diagonal_mul]
      fin_cases i <;> fin_cases j <;>
        norm_num [fiveCycleDelta, fiveCycleD2,
          fiveCycleAdvectiveDeltaK, Fin.ext_iff]

/-- Complete induced energy Hessian for the delta witness, computed from the
generic inverse-transpose congruence formula. -/
def fiveCycleAdvectiveDeltaHessian : AdvectiveFiveMatrix := fun i j =>
  if i.val = 0 ∧ j.val = 0 then 25
  else if i.val = 0 ∧ (j.val = 2 ∨ j.val = 3) then -(25 / 4 : ℚ)
  else if j.val = 0 ∧ (i.val = 2 ∨ i.val = 3) then -(25 / 4 : ℚ)
  else if i.val = 1 ∧ j.val = 1 then 25 / 2
  else if i.val = 1 ∧ j.val = 4 then -(25 / 2 : ℚ)
  else if i.val = 4 ∧ j.val = 1 then -(25 / 2 : ℚ)
  else if i.val = 4 ∧ j.val = 4 then 25 / 2
  else 0

theorem fiveCycleAdvectiveDeltaHessian_exact :
    secondOrderCongruenceCoefficient fiveCycleCartanTangent
      (advectiveFiveSecondJet fiveCycleDelta) = fiveCycleAdvectiveDeltaHessian := by
  rw [secondOrderCongruenceCoefficient_eq, fiveCycleAdvectiveDeltaK_exact]
  ext i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply,
    Matrix.transpose_apply, two_smul]
  simp only [advectiveFin5MatrixMulApply]
  fin_cases i <;> fin_cases j <;>
    norm_num [fiveCycleCartanTangent, fiveCycleAdvectiveDeltaK,
      fiveCycleAdvectiveDeltaHessian, Fin.ext_iff] <;> ring_nf

theorem fiveCycleAdvective_sameAxis_distanceTwo_nonzero :
    secondOrderCongruenceCoefficient fiveCycleCartanTangent
      (advectiveFiveSecondJet fiveCycleDelta) 1 4 = -(25 / 2 : ℚ) := by
  rw [fiveCycleAdvectiveDeltaHessian_exact]
  norm_num [fiveCycleAdvectiveDeltaHessian]

/-- A non-delta L=5 input does not inherit the delta nilpotence special case. -/
def fiveCycleNonDeltaGauge : FiveCycleVector := fun x =>
  if x.val = 0 then 1 else if x.val = 1 then 2 else 0

theorem fiveCycleNonDelta_generator_square_ne_zero :
    (advectiveFiveGenerator fiveCycleNonDeltaGauge *
      advectiveFiveGenerator fiveCycleNonDeltaGauge) 0 0 ≠ 0 := by
  norm_num [advectiveFiveGenerator, advectiveFiveMul, fiveCycleNonDeltaGauge,
    fiveCycleD, fiveCycleShift, fiveCycleSucc, Matrix.diagonal,
    Matrix.mul_apply, Fin.sum_univ_succ]

/-- Direct elementary-edge support on the original five-site scalar carrier:
an energy Hessian can only connect equal or adjacent cycle sites. -/
def DirectElementaryCellHessianSupport (H : AdvectiveFiveMatrix) : Prop :=
  ∀ i j, j ≠ i → j ≠ fiveCycleSucc i → i ≠ fiveCycleSucc j → H i j = 0

theorem directElementaryCell_hessian_distanceTwo_zero
    (H : AdvectiveFiveMatrix) (hcell : DirectElementaryCellHessianSupport H) :
    H 1 4 = 0 := by
  apply hcell
  · decide
  · decide
  · decide

/-- Scoped obstruction: no output-site-parameter-local scalar groupoid with
the forced advective Hessian can also have a direct elementary-cell energy
on the original carrier. This is not a universal matter-locality no-go. -/
theorem outputSiteLocal_noDirectElementaryCellInvariantEnergy
    (g : AdvectiveFiveVector → AdvectiveFiveMatrix → AdvectiveFiveMatrix)
    (H : AdvectiveFiveMatrix)
    (hout : OutputSiteParameterLocal g)
    (hforced : H = secondOrderCongruenceCoefficient fiveCycleCartanTangent
      (advectiveFiveSecondJet fiveCycleDelta))
    (hcell : DirectElementaryCellHessianSupport H) : False := by
  let _outputLocalityAtFlat := hout 0
  have hzero := directElementaryCell_hessian_distanceTwo_zero H hcell
  rw [hforced, fiveCycleAdvective_sameAxis_distanceTwo_nonzero] at hzero
  norm_num at hzero

end D0.Geometry
