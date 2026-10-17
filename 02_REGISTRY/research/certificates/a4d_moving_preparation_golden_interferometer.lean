import D0.Representation.GoldenOrderInterferometer
import D0.Core.FiniteTypes
import D0.Geometry.A4DDiscreteEnergyKernel
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.Tactic

open Matrix

namespace D0.Research.MovingPreparationGoldenBridge

noncomputable section

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Operator-valued lift of the existing two-port golden gate. -/
def blockGate (a p : ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix ι ι ℝ) :=
  !![a • (1 : Matrix ι ι ℝ), -p • (1 : Matrix ι ι ℝ);
    p • (1 : Matrix ι ι ℝ), a • (1 : Matrix ι ι ℝ)]

/-- Controlled comparison of the identity return with a return operator U. -/
def controlledReturn (U : Matrix ι ι ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix ι ι ℝ) :=
  !![(1 : Matrix ι ι ℝ), 0; 0, U]

/-- Full golden comparison Gᵀ diag(I,U) G, before reading the two record ports. -/
def comparisonOutput (a p : ℝ) (U : Matrix ι ι ℝ) :
    Matrix (Fin 2) (Fin 2) (Matrix ι ι ℝ) :=
  (blockGate a p).transpose * controlledReturn U * blockGate a p

omit [Fintype ι] in
theorem blockGate_lifted_from_owner (a p : ℝ) (i j : Fin 2) :
    blockGate a p i j =
      D0.Representation.GoldenOrderInterferometer.gate a p i j •
        (1 : Matrix ι ι ℝ) := by
  fin_cases i <;> fin_cases j <;>
    simp [blockGate, D0.Representation.GoldenOrderInterferometer.gate]

theorem comparisonOutput_zero_zero (a p : ℝ)
    (U : Matrix ι ι ℝ) :
    comparisonOutput a p U 0 0 =
      a^2 • (1 : Matrix ι ι ℝ) + p^2 • U := by
  ext x y
  simp [comparisonOutput, blockGate, controlledReturn, Matrix.mul_apply,
    Fin.sum_univ_succ]
  ring

theorem comparisonOutput_one_zero (a p : ℝ)
    (U : Matrix ι ι ℝ) :
    comparisonOutput a p U 1 0 = (a*p) • (U - 1) := by
  ext x y
  simp [comparisonOutput, blockGate, controlledReturn, Matrix.mul_apply,
    Fin.sum_univ_succ]
  ring

/-- Scalar controlled-sign specialization is exactly the existing owner output. -/
theorem scalar_specialization_zero (a p s : ℝ) :
    comparisonOutput a p (s • (1 : Matrix ι ι ℝ)) 0 0 =
      (D0.Representation.GoldenOrderInterferometer.output a p s) 0 •
        (1 : Matrix ι ι ℝ) := by
  rw [comparisonOutput_zero_zero,
    D0.Representation.GoldenOrderInterferometer.output_formula]
  simp only [Matrix.cons_val_zero]
  module

theorem scalar_specialization_one (a p s : ℝ) :
    comparisonOutput a p (s • (1 : Matrix ι ι ℝ)) 1 0 =
      (D0.Representation.GoldenOrderInterferometer.output a p s) 1 •
        (1 : Matrix ι ι ℝ) := by
  rw [comparisonOutput_one_zero,
    D0.Representation.GoldenOrderInterferometer.output_formula]
  simp only [Matrix.cons_val_one, Matrix.cons_val_zero]
  module

def branchZero (a p : ℝ) (U : Matrix ι ι ℝ) :=
  comparisonOutput a p U 0 0

def branchOne (a p : ℝ) (U : Matrix ι ι ℝ) :=
  comparisonOutput a p U 1 0

omit [DecidableEq ι] in
theorem scalar_mul_transpose_prod (r s : ℝ)
    (A B : Matrix ι ι ℝ) :
    (r • A).transpose * (s • B) = (r*s) • (A.transpose * B) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply,
    smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- The failed port measures exactly the squared native return difference. -/
theorem branchOne_effect (a p : ℝ)
    (U : Matrix ι ι ℝ) (ha : a^2 = p) :
    (branchOne a p U).transpose * branchOne a p U =
      p^3 • ((U - 1).transpose * (U - 1)) := by
  rw [branchOne, comparisonOutput_one_zero, scalar_mul_transpose_prod]
  have hcoeff : (a*p)*(a*p) = p^3 := by
    calc
      (a*p)*(a*p) = a^2*p^2 := by ring
      _ = p^3 := by rw [ha]; ring
  rw [hcoeff]

def roleKrausOne (a p : ℝ)
    (U : D0.Role → Matrix ι ι ℝ) (r : D0.Role) :
    Matrix ι ι ℝ :=
  (1/2 : ℝ) • branchOne a p (U r)

def roleFailureEffect (a p : ℝ)
    (U : D0.Role → Matrix ι ι ℝ) :
    Matrix ι ι ℝ :=
  ∑ r : D0.Role, (roleKrausOne a p U r).transpose * roleKrausOne a p U r

/-- Four Role branches and their q⁻¹ᐟ²=1/2 amplitudes give the v3 effect. -/
theorem roleFailureEffect_formula (a p : ℝ)
    (U : D0.Role → Matrix ι ι ℝ) (ha : a^2 = p) :
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

/-- The literal owned role translation on the full site × Fock cochain basis. -/
def cochainRoleShiftEquiv (N : ℕ) (r : D0.Role) :
    D0.Geometry.ArchiveCochainBasis N ≃ D0.Geometry.ArchiveCochainBasis N :=
  Equiv.prodCongr
    (D0.Geometry.roleTranslateEquiv N (D0.Geometry.roleStep N r))
    (Equiv.refl D0.Geometry.ArchiveFockState)

/-- Permutation of the owned finite cochain basis induced by one Role step. -/
def cochainRoleShiftPerm (N : ℕ) (r : D0.Role) :
    Equiv.Perm (D0.Geometry.ArchiveCochainBasis N) := cochainRoleShiftEquiv N r

/-- Exact matrix realization of the existing forward cochain shift. -/
def cochainRoleShiftMatrix (N : ℕ) (r : D0.Role) :
    Matrix (D0.Geometry.ArchiveCochainBasis N)
      (D0.Geometry.ArchiveCochainBasis N) ℝ :=
  (cochainRoleShiftPerm N r).permMatrix ℝ

theorem cochainRoleShiftMatrix_mulVec (N : ℕ) (r : D0.Role)
    (ψ : D0.Geometry.ArchiveCochain N) :
    Matrix.mulVec (cochainRoleShiftMatrix N r) ψ =
      D0.Geometry.cochainForwardShift N r ψ := by
  rw [cochainRoleShiftMatrix, cochainRoleShiftPerm, Matrix.permMatrix_mulVec]
  ext p
  rfl

theorem cochainRoleShiftMatrix_orthogonal (N : ℕ) (r : D0.Role) :
    (cochainRoleShiftMatrix N r).transpose * cochainRoleShiftMatrix N r = 1 := by
  rw [cochainRoleShiftMatrix, Matrix.transpose_permMatrix]
  rw [← Matrix.permMatrix_mul]
  simp

/-- Substitution of the actual four native shift matrices into the golden
failure-effect formula. The equality of each matrix action with the owned
cochain shift is stated separately above. -/
theorem nativeRoleFailureEffect_formula (N : ℕ) (a p : ℝ) (ha : a^2 = p) :
    roleFailureEffect a p (fun r => cochainRoleShiftMatrix N r) =
      (p^3/4) • ∑ r : D0.Role,
        ((cochainRoleShiftMatrix N r - 1).transpose *
          (cochainRoleShiftMatrix N r - 1)) := by
  exact roleFailureEffect_formula a p _ ha

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
#print D0.Research.MovingPreparationGoldenBridge.cochainRoleShiftMatrix_mulVec
#print axioms D0.Research.MovingPreparationGoldenBridge.cochainRoleShiftMatrix_mulVec
#print D0.Research.MovingPreparationGoldenBridge.cochainRoleShiftMatrix_orthogonal
#print axioms D0.Research.MovingPreparationGoldenBridge.cochainRoleShiftMatrix_orthogonal
#print D0.Research.MovingPreparationGoldenBridge.nativeRoleFailureEffect_formula
#print axioms D0.Research.MovingPreparationGoldenBridge.nativeRoleFailureEffect_formula
#print D0.Research.MovingPreparationGoldenBridge.native_role_cardinality
#print axioms D0.Research.MovingPreparationGoldenBridge.native_role_cardinality
