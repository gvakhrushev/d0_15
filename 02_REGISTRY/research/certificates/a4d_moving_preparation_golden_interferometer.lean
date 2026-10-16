import D0.Representation.GoldenOrderInterferometer
import D0.Core.FiniteTypes
import Mathlib.Tactic

open Matrix

namespace D0.Research.MovingPreparationGoldenBridge

noncomputable section

/-- Operator-valued lift of the existing two-port golden gate. -/
def blockGate {n : ℕ} (a p : ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix (Fin n) (Fin n) ℝ) :=
  !![a • (1 : Matrix (Fin n) (Fin n) ℝ), -p • (1 : Matrix (Fin n) (Fin n) ℝ);
    p • (1 : Matrix (Fin n) (Fin n) ℝ), a • (1 : Matrix (Fin n) (Fin n) ℝ)]

/-- Controlled comparison of the identity return with a return operator U. -/
def controlledReturn {n : ℕ} (U : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix (Fin n) (Fin n) ℝ) :=
  !![(1 : Matrix (Fin n) (Fin n) ℝ), 0; 0, U]

/-- Full golden comparison Gᵀ diag(I,U) G, before reading the two record ports. -/
def comparisonOutput {n : ℕ} (a p : ℝ) (U : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix (Fin n) (Fin n) ℝ) :=
  (blockGate a p).transpose * controlledReturn U * blockGate a p

theorem blockGate_lifted_from_owner {n : ℕ} (a p : ℝ) (i j : Fin 2) :
    blockGate a p i j =
      D0.Representation.GoldenOrderInterferometer.gate a p i j •
        (1 : Matrix (Fin n) (Fin n) ℝ) := by
  fin_cases i <;> fin_cases j <;>
    simp [blockGate, D0.Representation.GoldenOrderInterferometer.gate]

theorem comparisonOutput_zero_zero {n : ℕ} (a p : ℝ)
    (U : Matrix (Fin n) (Fin n) ℝ) :
    comparisonOutput a p U 0 0 =
      a^2 • (1 : Matrix (Fin n) (Fin n) ℝ) + p^2 • U := by
  ext x y
  simp [comparisonOutput, blockGate, controlledReturn, Matrix.mul_apply,
    Fin.sum_univ_succ]
  ring

theorem comparisonOutput_one_zero {n : ℕ} (a p : ℝ)
    (U : Matrix (Fin n) (Fin n) ℝ) :
    comparisonOutput a p U 1 0 = (a*p) • (U - 1) := by
  ext x y
  simp [comparisonOutput, blockGate, controlledReturn, Matrix.mul_apply,
    Fin.sum_univ_succ]
  ring

/-- Scalar controlled-sign specialization is exactly the existing owner output. -/
theorem scalar_specialization_zero {n : ℕ} (a p s : ℝ) :
    comparisonOutput a p (s • (1 : Matrix (Fin n) (Fin n) ℝ)) 0 0 =
      (D0.Representation.GoldenOrderInterferometer.output a p s) 0 •
        (1 : Matrix (Fin n) (Fin n) ℝ) := by
  rw [comparisonOutput_zero_zero,
    D0.Representation.GoldenOrderInterferometer.output_formula]
  simp only [Matrix.cons_val_zero]
  module

theorem scalar_specialization_one {n : ℕ} (a p s : ℝ) :
    comparisonOutput a p (s • (1 : Matrix (Fin n) (Fin n) ℝ)) 1 0 =
      (D0.Representation.GoldenOrderInterferometer.output a p s) 1 •
        (1 : Matrix (Fin n) (Fin n) ℝ) := by
  rw [comparisonOutput_one_zero,
    D0.Representation.GoldenOrderInterferometer.output_formula]
  simp only [Matrix.cons_val_one, Matrix.cons_val_zero]
  module

def branchZero {n : ℕ} (a p : ℝ) (U : Matrix (Fin n) (Fin n) ℝ) :=
  comparisonOutput a p U 0 0

def branchOne {n : ℕ} (a p : ℝ) (U : Matrix (Fin n) (Fin n) ℝ) :=
  comparisonOutput a p U 1 0

theorem scalar_mul_transpose_prod {n : ℕ} (r s : ℝ)
    (A B : Matrix (Fin n) (Fin n) ℝ) :
    (r • A).transpose * (s • B) = (r*s) • (A.transpose * B) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply,
    smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- The failed port measures exactly the squared native return difference. -/
theorem branchOne_effect {n : ℕ} (a p : ℝ)
    (U : Matrix (Fin n) (Fin n) ℝ) (ha : a^2 = p) :
    (branchOne a p U).transpose * branchOne a p U =
      p^3 • ((U - 1).transpose * (U - 1)) := by
  rw [branchOne, comparisonOutput_one_zero, scalar_mul_transpose_prod]
  have hcoeff : (a*p)*(a*p) = p^3 := by
    calc
      (a*p)*(a*p) = a^2*p^2 := by ring
      _ = p^3 := by rw [ha]; ring
  rw [hcoeff]

def roleKrausOne {n : ℕ} (a p : ℝ)
    (U : D0.Role → Matrix (Fin n) (Fin n) ℝ) (r : D0.Role) :
    Matrix (Fin n) (Fin n) ℝ :=
  (1/2 : ℝ) • branchOne a p (U r)

def roleFailureEffect {n : ℕ} (a p : ℝ)
    (U : D0.Role → Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  ∑ r : D0.Role, (roleKrausOne a p U r).transpose * roleKrausOne a p U r

/-- Four Role branches and their q⁻¹ᐟ²=1/2 amplitudes give the v3 effect. -/
theorem roleFailureEffect_formula {n : ℕ} (a p : ℝ)
    (U : D0.Role → Matrix (Fin n) (Fin n) ℝ) (ha : a^2 = p) :
    roleFailureEffect a p U = (p^3/4) •
      ∑ r : D0.Role, ((U r - 1).transpose * (U r - 1)) := by
  unfold roleFailureEffect roleKrausOne
  calc
    (∑ r : D0.Role,
        ((1/2 : ℝ) • branchOne a p (U r)).transpose *
          ((1/2 : ℝ) • branchOne a p (U r))) =
      ∑ r : D0.Role, (p^3/4) • ((U r - 1).transpose * (U r - 1)) := by
        apply Finset.sum_congr rfl
        intro r hr
        rw [scalar_mul_transpose_prod]
        rw [branchOne_effect a p (U r) ha]
        simp only [smul_smul]
        congr 1
        ring
    _ = (p^3/4) •
        ∑ r : D0.Role, ((U r - 1).transpose * (U r - 1)) := by
          simp only [Finset.smul_sum]

theorem native_role_cardinality : Fintype.card D0.Role = 4 := D0.card_role

end

#print D0.Research.MovingPreparationGoldenBridge.blockGate_lifted_from_owner
#print axioms D0.Research.MovingPreparationGoldenBridge.blockGate_lifted_from_owner
#print D0.Research.MovingPreparationGoldenBridge.comparisonOutput_zero_zero
#print axioms D0.Research.MovingPreparationGoldenBridge.comparisonOutput_zero_zero
#print D0.Research.MovingPreparationGoldenBridge.comparisonOutput_one_zero
#print axioms D0.Research.MovingPreparationGoldenBridge.comparisonOutput_one_zero
#print D0.Research.MovingPreparationGoldenBridge.scalar_specialization_zero
#print axioms D0.Research.MovingPreparationGoldenBridge.scalar_specialization_zero
#print D0.Research.MovingPreparationGoldenBridge.scalar_specialization_one
#print axioms D0.Research.MovingPreparationGoldenBridge.scalar_specialization_one
#print D0.Research.MovingPreparationGoldenBridge.branchOne_effect
#print axioms D0.Research.MovingPreparationGoldenBridge.branchOne_effect
#print D0.Research.MovingPreparationGoldenBridge.roleFailureEffect_formula
#print axioms D0.Research.MovingPreparationGoldenBridge.roleFailureEffect_formula
#print D0.Research.MovingPreparationGoldenBridge.native_role_cardinality
#print axioms D0.Research.MovingPreparationGoldenBridge.native_role_cardinality
