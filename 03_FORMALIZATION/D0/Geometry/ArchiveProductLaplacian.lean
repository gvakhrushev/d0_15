import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveRolePhaseProductCarrier

open scoped BigOperators

namespace D0.Geometry.ArchiveProductLaplacian

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier

local notation:70 A " *ᵥ " B => Matrix.mulVec A B

/-- Coordinate-wise directional Laplacian component along a specific role $r \in \mathrm{Role}$.
It applies the 1D cyclic Laplacian `archiveCanonicalLaplacian n` to coordinate $r$,
while requiring all other coordinates $r' \ne r$ to match identically. -/
def roleLaplacian (n : ℕ) (r : Role) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y =>
    if ∀ r' : Role, r' ≠ r → x r' = y r' then
      archiveCanonicalLaplacian n (x r) (y r)
    else
      0

/-- **Canonical 4D Role-Product Laplacian**:
Defined coordinate-free as the sum of directional cycle Laplacians over all four terminal roles
`Role = Dyad × Dyad` (ABCD):
$$L_{\mathrm{prod}}(x, y) = \sum_{r \in \mathrm{Role}} L_r(x, y).$$ -/
def archiveProductLaplacian (n : ℕ) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y => ∑ r : Role, roleLaplacian n r x y

/-- Each directional role component $L_r$ is symmetric. -/
theorem roleLaplacian_symmetric (n : ℕ) (r : Role) :
    ∀ x y : ArchiveRolePhasePoint n, roleLaplacian n r x y = roleLaplacian n r y x := by
  intro x y
  unfold roleLaplacian
  have h_cond : (∀ r' : Role, r' ≠ r → x r' = y r') ↔ (∀ r' : Role, r' ≠ r → y r' = x r') := by
    constructor
    · intro h r' hr; exact (h r' hr).symm
    · intro h r' hr; exact (h r' hr).symm
  by_cases h : ∀ r' : Role, r' ≠ r → x r' = y r'
  · have h_rev := h_cond.mp h
    simp only [if_pos h, if_pos h_rev]
    have h_symm := archiveCanonicalLaplacian_symmetric n (x r) (y r)
    unfold MatrixSymmetric at h_symm
    exact h_symm
  · have h_rev : ¬ (∀ r' : Role, r' ≠ r → y r' = x r') := fun hc => h (h_cond.mpr hc)
    simp only [if_neg h, if_neg h_rev]

/-- **D0-ARCHIVE-PRODUCT-LAPLACIAN-OWNER-001 (Symmetry)**:
The 4D role-product Laplacian is symmetric: $L_{\mathrm{prod}}(x, y) = L_{\mathrm{prod}}(y, x)$. -/
theorem archiveProductLaplacian_symmetric (n : ℕ) :
    MatrixSymmetric (archiveProductLaplacian n) := by
  intro x y
  unfold archiveProductLaplacian
  apply Finset.sum_congr rfl
  intro r _
  exact roleLaplacian_symmetric n r x y

/-- The constant vector is in the nullspace of each directional role component:
$$\sum_y L_r(x, y) = 0.$$ -/
theorem roleLaplacian_row_sum_zero (n : ℕ) (r : Role) (x : ArchiveRolePhasePoint n) :
    (∑ y : ArchiveRolePhasePoint n, roleLaplacian n r x y) = 0 := by
  classical
  let F : archivePhaseIndex n → ArchiveRolePhasePoint n := fun yr => Function.update x r yr
  have hF_inj : Function.Injective F := by
    intro a b hab
    have h_eval : F a r = F b r := by rw [hab]
    dsimp [F] at h_eval
    rw [Function.update_self, Function.update_self] at h_eval
    exact h_eval
  have h_val : ∀ yr : archivePhaseIndex n,
      roleLaplacian n r x (F yr) = archiveCanonicalLaplacian n (x r) yr := by
    intro yr
    unfold roleLaplacian F
    have h_match : ∀ r' : Role, r' ≠ r → x r' = Function.update x r yr r' := by
      intro r' hr'
      rw [Function.update_of_ne hr']
    simp only [if_pos h_match, Function.update_self]
  have h_zero_outside : ∀ y : ArchiveRolePhasePoint n, y ∉ Finset.image F Finset.univ → roleLaplacian n r x y = 0 := by
    intro y hy
    unfold roleLaplacian
    split_ifs with h_eq
    · exfalso
      apply hy
      rw [Finset.mem_image]
      refine ⟨y r, Finset.mem_univ (y r), ?_⟩
      dsimp [F]
      funext r'
      by_cases hr' : r' = r
      · subst hr'
        rw [Function.update_self]
      · rw [Function.update_of_ne hr', ← h_eq r' hr']
    · rfl
  have h_sum_total : (∑ y : ArchiveRolePhasePoint n, roleLaplacian n r x y) =
      ∑ y ∈ Finset.image F Finset.univ, roleLaplacian n r x y := by
    rw [← Finset.sum_subset (Finset.subset_univ (Finset.image F Finset.univ))]
    intro y _ hy_not
    exact h_zero_outside y hy_not
  rw [h_sum_total]
  rw [Finset.sum_image (by simpa using hF_inj)]
  have h_sum_cycle : (∑ yr : archivePhaseIndex n, roleLaplacian n r x (F yr)) =
      ∑ yr : archivePhaseIndex n, archiveCanonicalLaplacian n (x r) yr := by
    apply Finset.sum_congr rfl
    intro yr _
    exact h_val yr
  rw [h_sum_cycle]
  have h_const := archiveCanonicalLaplacian_constant_zero n 1
  have h_row : (archiveCanonicalLaplacian n *ᵥ (fun _ => (1 : ℝ))) (x r) = 0 := by
    rw [h_const]
    rfl
  dsimp [Matrix.mulVec, dotProduct] at h_row
  simp only [mul_one] at h_row
  exact h_row

/-- **D0-ARCHIVE-PRODUCT-LAPLACIAN-OWNER-001 (Constant Zero Mode)**:
The 4D role-product Laplacian annihilates the constant function:
$$L_{\mathrm{prod}} \cdot \mathbf{1} = 0.$$ -/
theorem archiveProductLaplacian_constant_zero (n : ℕ) (c : ℝ) :
    (archiveProductLaplacian n *ᵥ (fun _ => c)) = 0 := by
  funext x
  unfold Matrix.mulVec dotProduct archiveProductLaplacian
  dsimp
  rw [← Finset.sum_mul]
  have h_comm : (∑ y : ArchiveRolePhasePoint n, ∑ r : Role, roleLaplacian n r x y) =
      ∑ r : Role, ∑ y : ArchiveRolePhasePoint n, roleLaplacian n r x y :=
    Finset.sum_comm
  rw [h_comm]
  have h_zero : (∑ r : Role, ∑ y : ArchiveRolePhasePoint n, roleLaplacian n r x y) = 0 := by
    have h_each : ∀ r ∈ (Finset.univ : Finset Role), (∑ y : ArchiveRolePhasePoint n, roleLaplacian n r x y) = 0 :=
      fun r _ => roleLaplacian_row_sum_zero n r x
    rw [Finset.sum_congr rfl h_each, Finset.sum_const_zero]
  rw [h_zero, zero_mul]

/-- **D0-ARCHIVE-PRODUCT-LAPLACIAN-OWNER-001 (Owner)**:
Master theorem establishing the canonical 4D role-product Laplacian:
1. Symmetric matrix operator on `ArchiveRolePhasePoint n`.
2. Directional decomposition into 4 role components matching the terminal ABCD roles.
3. Rigorous vanishing on constant zero-mode states. -/
theorem archive_product_laplacian_owner (n : ℕ) :
    MatrixSymmetric (archiveProductLaplacian n) ∧
    (∀ c : ℝ, (archiveProductLaplacian n *ᵥ (fun _ => c)) = 0) ∧
    (∀ r : Role, MatrixSymmetric (roleLaplacian n r)) :=
  ⟨archiveProductLaplacian_symmetric n,
   archiveProductLaplacian_constant_zero n,
   fun r => by intro x y; exact roleLaplacian_symmetric n r x y⟩

end D0.Geometry.ArchiveProductLaplacian
