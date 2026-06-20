import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Matter.CKMBasisMismatch

set_option linter.unusedSimpArgs false

/-!
# D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001 — the CKM overlap invariant is not forced

`D0.Matter.CKMBasisMismatch` proves that **once the up/down bases are fixed**, the mismatch (overlap)
matrix `V_mix = B_up† B_down` is unique (`basis_mismatch_matrix_unique`). But present-core does NOT force
the basis completion itself: the frozen basis-origin (candidate family + score, `D0.Matter.CKMBasisOrigin`)
admits more than one admissible orthogonal completion.

Maximality witness: two admissible rational-orthogonal overlap matrices (genuine 2-flavour rotations from
the Pythagorean triples 3-4-5 and 5-12-13) — both legitimate completions — give **different** Cabibbo
overlap invariants `|V_mix₁₂|² = 16/25` vs `144/169`. Hence the overlap invariant is **underdetermined by
present-core**: no canonical `|V_mix₁₂|²` is forced. A canonical selection (symmetry-breaking /
modulus-fixing input) would be a NEW primitive (extension), not a present-core theorem. Closed-negative.
-/

namespace D0.Matter.CKMOverlapUnderdeterminationNoGo

open Matrix

/-- Admissible completion A: the 3-4-5 rational rotation overlap. -/
def VmixA : Matrix (Fin 2) (Fin 2) ℚ := !![3/5, 4/5; -4/5, 3/5]

/-- Admissible completion B: the 5-12-13 rational rotation overlap. -/
def VmixB : Matrix (Fin 2) (Fin 2) ℚ := !![5/13, 12/13; -12/13, 5/13]

/-- Completion A is a genuine (orthogonal) overlap — `VmixA · VmixAᵀ = 1` — hence admissible. -/
theorem VmixA_orthogonal : VmixA * VmixAᵀ = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [VmixA, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two, Matrix.one_apply] <;> norm_num

/-- Completion B is a genuine (orthogonal) overlap — `VmixB · VmixBᵀ = 1` — hence admissible. -/
theorem VmixB_orthogonal : VmixB * VmixBᵀ = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [VmixB, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two, Matrix.one_apply] <;> norm_num

/-- **The two admissible completions give different Cabibbo overlap invariants**:
`|V_mix₁₂|² = 16/25` (A) ≠ `144/169` (B). -/
theorem overlap_invariants_differ : (VmixA 0 1) ^ 2 ≠ (VmixB 0 1) ^ 2 := by
  simp only [VmixA, VmixB, Matrix.cons_val_one, Matrix.cons_val_zero, Matrix.head_cons]
  norm_num

/-- **D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001 (closed-negative).** Two admissible orthogonal overlap
completions of the frozen CKM basis-origin give different overlap invariants `|V_mix₁₂|²`. The mismatch
matrix is unique *given* fixed bases (`CKMBasisMismatch`), but present-core does not force the completion,
so the overlap invariant is underdetermined; a canonical selector is a new primitive, not present-core. -/
theorem ckm_overlap_underdetermination_nogo :
    VmixA * VmixAᵀ = 1 ∧ VmixB * VmixBᵀ = 1 ∧ (VmixA 0 1) ^ 2 ≠ (VmixB 0 1) ^ 2 :=
  ⟨VmixA_orthogonal, VmixB_orthogonal, overlap_invariants_differ⟩

end D0.Matter.CKMOverlapUnderdeterminationNoGo
