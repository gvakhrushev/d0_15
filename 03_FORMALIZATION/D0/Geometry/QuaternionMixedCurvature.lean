import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import D0.Representation.CouplingAxisReadout

/-!
# D0-QUATERNION-MIXED-CURVATURE-001 & D0-QUATERNION-CROSS-ROLE-COMMUTATOR-ALGEBRA-001

## True Non-Abelian Cross-Role Curvature from the Quaternion Carrier

This module replaces the trivial self-commutator $[A, A] = 0$ with the genuine cross-role
directional curvature:
$$F_{rs} := [A_r, A_s], \quad r \ne s.$$

Using the quaternion axis representation from `CouplingAxisReadout.axis`:
$$G(x, y, z) = \begin{pmatrix} 0 & -x & -y & -z \\ x & 0 & -z & y \\ y & z & 0 & -x \\ z & -y & x & 0 \end{pmatrix},$$
we prove two fundamental vector identities:
1. **Anticommutator / Dot Product**:
   $$G(u) G(v) + G(v) G(u) = -2 (u \cdot v) I_4.$$
2. **Commutator / Cross Product**:
   $$[G(u), G(v)] = 2 G(u \times v).$$

### Consequences for Reference Generators:
For the three standard spatial axes $G_1 = G(1,0,0)$, $G_2 = G(0,1,0)$, $G_3 = G(0,0,1)$:
- Self-commutators vanish: $[G_i, G_i] = 0$.
- Cross-role commutators form the $\mathfrak{su}(2) \cong \mathfrak{so}(3)$ Lie algebra:
  $$[G_1, G_2] = 2 G_3 \ne 0, \quad [G_2, G_3] = 2 G_1 \ne 0, \quad [G_3, G_1] = 2 G_2 \ne 0.$$
- The Frobenius curvature readout is strictly positive and $S_3$-invariant:
  $$\|F_{ij}\|_F^2 = \operatorname{Tr}(F_{ij}^\top F_{ij}) = 16 \quad (i \ne j).$$
-/

namespace D0.Geometry.QuaternionMixedCurvature

open Matrix
open D0.Representation.CouplingAxisReadout

abbrev M4 := Matrix (Fin 4) (Fin 4) ℝ

/-- Cross product in $\mathbb{R}^3$. -/
def crossProduct (u v : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![u 1 * v 2 - u 2 * v 1,
    u 2 * v 0 - u 0 * v 2,
    u 0 * v 1 - u 1 * v 0]

/-- Dot product in $\mathbb{R}^3$. -/
def dotProduct (u v : Fin 3 → ℝ) : ℝ :=
  u 0 * v 0 + u 1 * v 1 + u 2 * v 2

/-- Generator matrix for a 3-vector $u \in \mathbb{R}^3$. -/
def G (u : Fin 3 → ℝ) : M4 :=
  axis (u 0) (u 1) (u 2)

/-- **D0-QUATERNION-MIXED-CURVATURE-001 (Anticommutator / Dot Identity)**:
$$G(u) G(v) + G(v) G(u) = -2 (u \cdot v) I_4.$$ -/
theorem quaternion_anticommutator_dot (u v : Fin 3 → ℝ) :
    G u * G v + G v * G u = (-2 * dotProduct u v) • (1 : M4) := by
  unfold G axis dotProduct
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.add_apply, Matrix.smul_apply] <;>
    ring

/-- **D0-QUATERNION-MIXED-CURVATURE-001 (Commutator / Cross Identity)**:
$$[G(u), G(v)] = 2 G(u \times v).$$ -/
theorem quaternion_commutator_cross (u v : Fin 3 → ℝ) :
    G u * G v - G v * G u = (2 : ℝ) • G (crossProduct u v) := by
  unfold G axis crossProduct
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.sub_apply, Matrix.smul_apply] <;>
    ring

/-- Spatial reference basis axes: $e_0 = (1,0,0), e_1 = (0,1,0), e_2 = (0,0,1)$. -/
def e (i : Fin 3) : Fin 3 → ℝ :=
  match i with
  | 0 => ![1, 0, 0]
  | 1 => ![0, 1, 0]
  | 2 => ![0, 0, 1]

def G_ref (i : Fin 3) : M4 := G (e i)

/-- Directional curvature between two spatial role axes:
$$F_{ij} := [G_i, G_j] = G_i G_j - G_j G_i.$$ -/
def directionalCurvature (i j : Fin 3) : M4 :=
  G_ref i * G_ref j - G_ref j * G_ref i

/-- Self-commutator vanishes identically: $F_{ii} = 0$. -/
theorem directional_curvature_self_zero (i : Fin 3) :
    directionalCurvature i i = 0 := by
  unfold directionalCurvature
  simp

theorem cross_e0_e1 : crossProduct (e 0) (e 1) = e 2 := by
  unfold crossProduct e
  ext k
  fin_cases k <;> simp

theorem cross_e1_e2 : crossProduct (e 1) (e 2) = e 0 := by
  unfold crossProduct e
  ext k
  fin_cases k <;> simp

theorem cross_e2_e0 : crossProduct (e 2) (e 0) = e 1 := by
  unfold crossProduct e
  ext k
  fin_cases k <;> simp

/-- **D0-QUATERNION-CROSS-ROLE-COMMUTATOR-ALGEBRA-001**:
Cross-role commutators do NOT vanish:
$$F_{01} = 2 G_2 \ne 0, \quad F_{12} = 2 G_0 \ne 0, \quad F_{20} = 2 G_1 \ne 0.$$ -/
theorem cross_role_curvature_01 : directionalCurvature 0 1 = (2 : ℝ) • G_ref 2 := by
  unfold directionalCurvature G_ref
  rw [quaternion_commutator_cross, cross_e0_e1]

theorem cross_role_curvature_12 : directionalCurvature 1 2 = (2 : ℝ) • G_ref 0 := by
  unfold directionalCurvature G_ref
  rw [quaternion_commutator_cross, cross_e1_e2]

theorem cross_role_curvature_20 : directionalCurvature 2 0 = (2 : ℝ) • G_ref 1 := by
  unfold directionalCurvature G_ref
  rw [quaternion_commutator_cross, cross_e2_e0]

/-- Frobenius norm squared of a matrix: $\operatorname{Tr}(M^\top M)$. -/
def frobeniusNormSq (M : M4) : ℝ :=
  Matrix.trace (M.transpose * M)

/-- Frobenius norm squared of zero matrix is 0. -/
theorem frobenius_zero : frobeniusNormSq (0 : M4) = 0 := by
  unfold frobeniusNormSq Matrix.trace
  simp

/-- Frobenius norm squared of each reference generator is 4. -/
theorem frobenius_G_ref_0 : frobeniusNormSq (G_ref 0) = 4 := by
  unfold frobeniusNormSq G_ref G axis e Matrix.trace
  simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
  ring

theorem frobenius_G_ref_1 : frobeniusNormSq (G_ref 1) = 4 := by
  unfold frobeniusNormSq G_ref G axis e Matrix.trace
  simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
  ring

theorem frobenius_G_ref_2 : frobeniusNormSq (G_ref 2) = 4 := by
  unfold frobeniusNormSq G_ref G axis e Matrix.trace
  simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
  ring

theorem frobenius_ref_generator (i : Fin 3) :
    frobeniusNormSq (G_ref i) = 4 := by
  match i with
  | 0 => exact frobenius_G_ref_0
  | 1 => exact frobenius_G_ref_1
  | 2 => exact frobenius_G_ref_2

/-- **D0-QUATERNION-CROSS-ROLE-COMMUTATOR-ALGEBRA-001 (Frobenius Readout)**:
The magnitude of the cross-role curvature is strictly equal to 16 for all distinct pairs:
$$\|F_{01}\|_F^2 = \|F_{12}\|_F^2 = \|F_{20}\|_F^2 = 16.$$ -/
theorem cross_role_frobenius_magnitude :
    frobeniusNormSq (directionalCurvature 0 1) = 16 ∧
    frobeniusNormSq (directionalCurvature 1 2) = 16 ∧
    frobeniusNormSq (directionalCurvature 2 0) = 16 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [cross_role_curvature_01]
    unfold frobeniusNormSq G_ref G axis e Matrix.trace
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
    ring
  · rw [cross_role_curvature_12]
    unfold frobeniusNormSq G_ref G axis e Matrix.trace
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
    ring
  · rw [cross_role_curvature_20]
    unfold frobeniusNormSq G_ref G axis e Matrix.trace
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
    ring

theorem cross_role_curvature_01_nonzero : directionalCurvature 0 1 ≠ 0 := by
  intro h
  have h_norm := cross_role_frobenius_magnitude.1
  rw [h, frobenius_zero] at h_norm
  norm_num at h_norm

theorem cross_role_curvature_12_nonzero : directionalCurvature 1 2 ≠ 0 := by
  intro h
  have h_norm := cross_role_frobenius_magnitude.2.1
  rw [h, frobenius_zero] at h_norm
  norm_num at h_norm

theorem cross_role_curvature_20_nonzero : directionalCurvature 2 0 ≠ 0 := by
  intro h
  have h_norm := cross_role_frobenius_magnitude.2.2
  rw [h, frobenius_zero] at h_norm
  norm_num at h_norm

end D0.Geometry.QuaternionMixedCurvature
