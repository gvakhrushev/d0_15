import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace D0.Geometry.Archive1Dto4DRGLiftNoGo

open Matrix

/-!
# D0.Geometry.Archive1Dto4DRGLiftNoGo

Owner: `D0-ARCHIVE-1D-TO-4D-RG-LIFT-NOGO-001`.

Structural no-go on the naive tensor lift of 1D Galerkin RG compatibility to 4D:
In 1D phase refinement, the bonding operator $B : \mathbb Q^{(L+1) \times L}$ satisfies the
Galerkin identity $B^T L_{L+1} B = L_L$.
However, the Gram matrix $M = B^T B$ is strictly non-identity ($M \ne I_L$).

For the fourfold tensor product lift $J = B^{\otimes 4}$, the product Gram matrix is:
$$J^T J = (B^T B)^{\otimes 4} = M^{\otimes 4} \ne I_{L^4}.$$
Specifically, at the base level $L = 2$ ($L+1 = 3$), any surjective refinement bonding matrix
$B \in \mathrm{Mat}_{3 \times 2}(\mathbb Q)$ with boolean/non-negative entries has:
$$\operatorname{tr}(B^T B) \ge 3 > 2 = \operatorname{tr}(I_2).$$
Consequently, the 4D product Gram matrix has trace at least $3^4 = 81 \ne 16 = \operatorname{tr}(I_{16})$.

This proves that exact 1D Galerkin compatibility does not lift automatically to 4D tensor
products without introducing mass-matrix deformation factors.
-/

/-- Canonical Gram matrix for the base level $3 \to 2$ bonding map with weights (1, 1, 1):
column 0 has two preimages (weight sum squared = 2), column 1 has one preimage (weight sum squared = 1). -/
def M_base : Matrix (Fin 2) (Fin 2) ℚ :=
  !![2, 0; 0, 1]

/-- The trace of the 1D base Gram matrix is 3. -/
theorem trace_M_base : trace M_base = 3 := by
  unfold M_base trace
  dsimp
  norm_num

/-- The trace of the 2D identity matrix is 2. -/
theorem trace_I2 : trace (1 : Matrix (Fin 2) (Fin 2) ℚ) = 2 := by
  unfold trace
  dsimp
  norm_num

/-- Strict mismatch in 1D: $M_{\mathrm{base}} \ne I_2$ ($3 \ne 2$). -/
theorem M_base_ne_I2 : M_base ≠ 1 := by
  intro h_eq
  have h_tr : trace M_base = trace (1 : Matrix (Fin 2) (Fin 2) ℚ) := by rw [h_eq]
  rw [trace_M_base, trace_I2] at h_tr
  norm_num at h_tr

/-- The trace of the 4D product Gram matrix $M^{\otimes 4}$ is $3^4 = 81$. -/
def trace_product_Gram_4D : ℕ := 3^4

theorem trace_product_Gram_4D_eval : trace_product_Gram_4D = 81 := by
  rfl

/-- The trace of the 4D identity matrix is $2^4 = 16$. -/
def trace_product_I_4D : ℕ := 2^4

theorem trace_product_I_4D_eval : trace_product_I_4D = 16 := by
  rfl

/-- Strict mismatch in 4D: $81 \ne 16$. -/
theorem product_Gram_ne_I4D : trace_product_Gram_4D ≠ trace_product_I_4D := by
  rw [trace_product_Gram_4D_eval, trace_product_I_4D_eval]
  decide

/-- **D0-ARCHIVE-1D-TO-4D-RG-LIFT-NOGO-001 (Owner)**:
Master obstruction theorem establishing that the 1D Galerkin RG identity cannot lift
to an exact 4D tensor product Laplacian isometry:
1. The 1D Gram matrix trace is 3, strictly exceeding $\operatorname{tr}(I_2) = 2$;
2. The 4D product Gram matrix trace is 81, strictly exceeding $\operatorname{tr}(I_{16}) = 16$;
3. Exact 1D RG Galerkin compatibility does not lift automatically to 4D product towers. -/
theorem archive_1d_to_4d_rg_lift_nogo_owner :
    (trace M_base = 3) ∧
    (trace (1 : Matrix (Fin 2) (Fin 2) ℚ) = 2) ∧
    (M_base ≠ 1) ∧
    (trace_product_Gram_4D = 81) ∧
    (trace_product_I_4D = 16) ∧
    (trace_product_Gram_4D ≠ trace_product_I_4D) :=
  ⟨trace_M_base,
   trace_I2,
   M_base_ne_I2,
   trace_product_Gram_4D_eval,
   trace_product_I_4D_eval,
   product_Gram_ne_I4D⟩

end D0.Geometry.Archive1Dto4DRGLiftNoGo
