import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchiveProductLaplacian
import D0.Geometry.ArchivePhaseEdgeMetricScale

open scoped BigOperators

namespace D0.Geometry.ArchiveRoleProductLaplacian

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier
open D0.Geometry.ArchiveProductLaplacian
open D0.Geometry.ArchivePhaseEdgeMetricScale

local notation:70 A " *ᵥ " B => Matrix.mulVec A B

/-- **Canonical 4D Metric Role-Product Laplacian**:
The continuum-scaled 4D Laplacian operator on `ArchiveRolePhasePoint n`:
$$\Delta_L^{(4)} = L^2 \cdot L_{\mathrm{prod}} = (n + 2)^2 \sum_{r \in \mathrm{ABCD}} L_r.$$ -/
noncomputable def archiveMetricProductLaplacian (n : ℕ) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y => (archiveMetricLaplacianScale n) * archiveProductLaplacian n x y

/-- The metric 4D role-product Laplacian is symmetric: $L_{\mathrm{metric}}(x, y) = L_{\mathrm{metric}}(y, x)$. -/
theorem archiveMetricProductLaplacian_symmetric (n : ℕ) :
    MatrixSymmetric (archiveMetricProductLaplacian n) := by
  intro x y
  unfold archiveMetricProductLaplacian
  have h_symm := archiveProductLaplacian_symmetric n x y
  unfold MatrixSymmetric at h_symm
  rw [h_symm]

/-- The metric 4D role-product Laplacian strictly annihilates the constant zero mode:
$$\Delta_L^{(4)} \cdot \mathbf{1} = 0.$$ -/
theorem archiveMetricProductLaplacian_constant_zero (n : ℕ) (c : ℝ) :
    (archiveMetricProductLaplacian n *ᵥ (fun _ => c)) = 0 := by
  funext x
  unfold Matrix.mulVec dotProduct archiveMetricProductLaplacian
  dsimp
  have h_pull : (∑ y : ArchiveRolePhasePoint n, (archiveMetricLaplacianScale n * archiveProductLaplacian n x y) * c) =
      archiveMetricLaplacianScale n * (∑ y : ArchiveRolePhasePoint n, archiveProductLaplacian n x y * c) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro y _
    ring
  rw [h_pull]
  have h_zero : (∑ y : ArchiveRolePhasePoint n, archiveProductLaplacian n x y * c) = 0 := by
    have h_vec := archiveProductLaplacian_constant_zero n c
    have h_eval : (archiveProductLaplacian n *ᵥ (fun _ => c)) x = 0 := by rw [h_vec]; rfl
    exact h_eval
  rw [h_zero, mul_zero]

/-- The diagonal entry of the unscaled role-product Laplacian is the sum of cyclic degrees
across the four terminal roles:
$$L_{\mathrm{prod}}(x, x) = \sum_{r \in \mathrm{ABCD}} \mathrm{deg}_{\mathrm{cycle}}(x(r)).$$ -/
theorem archiveProductLaplacian_diag (n : ℕ) (x : ArchiveRolePhasePoint n) :
    archiveProductLaplacian n x x = ∑ r : Role, archiveDegree n (x r) := by
  unfold archiveProductLaplacian roleLaplacian
  apply Finset.sum_congr rfl
  intro r _
  split_ifs with h_cond
  · unfold archiveCanonicalLaplacian
    simp
  · exfalso
    exact h_cond (fun _ _ => rfl)

/-- **Small-Cycle Guard (Level $n = 0$, $L = 2$)**:
For $L = 2$, each vertex in the 2-cycle has degree 1, so the 4D diagonal degree is $1 \times 4 = 4$. -/
theorem small_cycle_diagonal_at_zero (x : ArchiveRolePhasePoint 0) :
    archiveProductLaplacian 0 x x = 4 := by
  rw [archiveProductLaplacian_diag]
  have h_deg : ∀ i : archivePhaseIndex 0, archiveDegree 0 i = 1 := by
    intro i
    unfold archiveDegree archiveAdjacent cyclicDistance archiveFibers
    change (∑ j : Fin 2, (if min ((i.val + 2 - j.val) % 2) ((j.val + 2 - i.val) % 2) = 1 then (1 : ℝ) else 0)) = 1
    rw [Fin.sum_univ_two]
    fin_cases i <;> norm_num
  have h_each : (∑ r : Role, archiveDegree 0 (x r)) = ∑ r : Role, (1 : ℝ) := by
    apply Finset.sum_congr rfl
    intro r _
    exact h_deg (x r)
  rw [h_each, Finset.sum_const, Finset.card_univ, card_role]
  norm_num

/-- **Small-Cycle Guard (Level $n = 1$, $L = 3$)**:
For $L = 3 \ge 3$, each vertex in the 3-cycle has degree 2, so the 4D diagonal degree
equals the canonical 4D lattice coordination number $2 \times |ABCD| = 2 \times 4 = 8$. -/
theorem small_cycle_diagonal_at_one (x : ArchiveRolePhasePoint 1) :
    archiveProductLaplacian 1 x x = 8 := by
  rw [archiveProductLaplacian_diag]
  have h_deg : ∀ i : archivePhaseIndex 1, archiveDegree 1 i = 2 := by
    intro i
    unfold archiveDegree archiveAdjacent cyclicDistance archiveFibers
    change (∑ j : Fin 3, (if min ((i.val + 3 - j.val) % 3) ((j.val + 3 - i.val) % 3) = 1 then (1 : ℝ) else 0)) = 2
    rw [Fin.sum_univ_three]
    fin_cases i <;> norm_num
  have h_each : (∑ r : Role, archiveDegree 1 (x r)) = ∑ r : Role, (2 : ℝ) := by
    apply Finset.sum_congr rfl
    intro r _
    exact h_deg (x r)
  rw [h_each, Finset.sum_const, Finset.card_univ, card_role]
  norm_num

/-- **D0-ARCHIVE-4D-METRIC-LAPLACIAN-001 (Owner)**:
Master theorem establishing the canonical 4D metric role-product Laplacian:
1. Symmetric matrix operator on `ArchiveRolePhasePoint n`;
2. Annihilates the constant zero mode ($\Delta_L^{(4)} \cdot \mathbf{1} = 0$);
3. Diagonal entries equal the sum of coordinate degrees;
4. Explicit small-cycle guard distinguishing $L = 2$ (degree 4) from canonical $L \ge 3$ (degree 8);
5. Scaled by the internal metric factor $L^2 = (n + 2)^2$. -/
theorem archive_4d_metric_laplacian_owner (n : ℕ) :
    MatrixSymmetric (archiveMetricProductLaplacian n) ∧
    (∀ c : ℝ, (archiveMetricProductLaplacian n *ᵥ (fun _ => c)) = 0) ∧
    (∀ x : ArchiveRolePhasePoint n, archiveProductLaplacian n x x = ∑ r : Role, archiveDegree n (x r)) ∧
    (∀ x : ArchiveRolePhasePoint 0, archiveProductLaplacian 0 x x = 4) ∧
    (∀ x : ArchiveRolePhasePoint 1, archiveProductLaplacian 1 x x = 8) :=
  ⟨archiveMetricProductLaplacian_symmetric n,
   archiveMetricProductLaplacian_constant_zero n,
   archiveProductLaplacian_diag n,
   small_cycle_diagonal_at_zero,
   small_cycle_diagonal_at_one⟩

end D0.Geometry.ArchiveRoleProductLaplacian
