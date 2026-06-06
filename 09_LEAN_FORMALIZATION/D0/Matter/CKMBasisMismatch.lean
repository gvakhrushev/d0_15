import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0.Matter

/--
A finite operator basis is represented by a list of basis vectors together with a
coordinate readout into that basis.  The definition is intentionally finite and
algebraic: no PDG numbers, smooth fields, or phenomenological angles are used.
-/
structure FiniteOperatorBasis (n : ℕ) (Op : Type) where
  vector : Fin n → Op
  coord : Op → Fin n → ℚ

/--
The operator-basis mismatch matrix: coordinates of the `up` basis vectors as
read by the `down` basis.  In the matter sector this is the structural CKM
object before any numerical/passport calibration.
-/
def basisMismatchMatrix {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op) : Matrix (Fin n) (Fin n) ℚ :=
  fun i j => down.coord (up.vector i) j

/--
A candidate mismatch matrix is admissible only when it reports the down-sector
coordinates of every up-sector basis vector.
-/
structure BasisMismatchCandidate {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op) where
  matrix : Matrix (Fin n) (Fin n) ℚ
  agrees : ∀ i j, matrix i j = down.coord (up.vector i) j

/--
Uniqueness of the finite operator-basis mismatch matrix.
Once the two finite operator bases and the coordinate readout are fixed, there is
no additional phenomenological freedom in the transition matrix.  Numerical CKM
passports may only calibrate/evaluate this object; they cannot choose another
matrix without changing one of the two bases or the coordinate readout.
-/
theorem basis_mismatch_matrix_unique {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op)
    (C : BasisMismatchCandidate up down) :
    C.matrix = basisMismatchMatrix up down := by
  ext i j
  exact C.agrees i j

/-- Any two admissible candidates for the same pair of bases have the same matrix. -/
theorem basis_mismatch_candidates_have_same_matrix {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op)
    (C D : BasisMismatchCandidate up down) :
    C.matrix = D.matrix := by
  rw [basis_mismatch_matrix_unique up down C]
  rw [basis_mismatch_matrix_unique up down D]

/--
No alternative matrix is admissible once the two bases and the readout are fixed.
A different matrix must therefore come from changing a basis, changing the
coordinate readout, or leaving the finite-core layer for a calibrated/passport
layer.
-/
theorem no_alternative_basis_mismatch_matrix {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op)
    (M : Matrix (Fin n) (Fin n) ℚ)
    (hM : M ≠ basisMismatchMatrix up down) :
    ¬ ∃ C : BasisMismatchCandidate up down, C.matrix = M := by
  rintro ⟨C, hC⟩
  apply hM
  rw [← hC]
  exact basis_mismatch_matrix_unique up down C

/-- CKM structural closure: the finite CKM carrier is the unique basis mismatch. -/
theorem ckm_class_unique_as_operator_basis_mismatch {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op)
    (C : BasisMismatchCandidate up down) :
    C.matrix = basisMismatchMatrix up down :=
  basis_mismatch_matrix_unique up down C

/-- CKM no-free-parameter closure at fixed finite bases/readout. -/
theorem ckm_no_free_matrix_at_fixed_bases {n : ℕ} {Op : Type}
    (up down : FiniteOperatorBasis n Op)
    (M : Matrix (Fin n) (Fin n) ℚ)
    (hM : M ≠ basisMismatchMatrix up down) :
    ¬ ∃ C : BasisMismatchCandidate up down, C.matrix = M :=
  no_alternative_basis_mismatch_matrix up down M hM

end D0.Matter
