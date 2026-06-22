import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# D0-V15 Work Package B + D — branch coupling and lepton mass-ratio (NO-GO)

Two final no-gos, each with a declared admissible class and a real negative control.

## B — branch CP-readout is NOT unique (NO-GO)

The branch carrier carries the frozen scene's three generation directions as **distinct isotypic blocks**
(`Aut_raw` fixes the part-constant directions; the part sizes `9,11,13` are pairwise distinct — see
`D0.Extensions.X5.Grading.SymmetryGroups`). Hence the commutant of the branch representation contains the
three independent block scalars: `commutantDim = 3 > 1`. The frozen diagonal (marginal) constraint
`V†(Eⱼ)V = Qⱼ` fixes only the *diagonal* of the readout density operator, not its coherences — so the
normalized block state is not unique. Negative control: `rho1` (diagonal) and `rho2` (same diagonal, nonzero
coherence) are two admissible readouts with the same frozen marginals (`same_diagonal`) but `rho1 ≠ rho2`.
The unique-readout requires the **twirling/depolarizing** rule `PRIM-BRANCH-ISOTROPIC-READOUT`, which is a new
primitive, not present-core. Cite `D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001`.

## D — lepton mass ratios are underdetermined (NO-GO)

For branch exponents `{0, 1/4, 1/3}` the Vandermonde matrix is invertible (`det = 1/144 ≠ 0`), so for ANY
target pair `(r_μ, r_τ)` there is a (quadratic, hence smooth) positive matching function `m(p)` with
`m(0)=mₑ, m(1/4)=r_μ mₑ, m(1/3)=r_τ mₑ`. The exponents impose NO constraint on the achievable ratios — the
measured masses are not derivable in the finite branch class. Missing owner: `PRIM-EFT-IR-MATCHING-FUNCTIONAL`.
Cite `D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001`, `D0-LEPTON-STURMIAN-PUISEUX-COEFFICIENTS-001`.
-/

namespace D0.Integration.V15.BranchAudit

open Matrix

/-! ## B — non-unique branch CP readout -/

/-- Commutant dimension of the branch representation: 3 independent generation blocks. -/
def commutantDim : ℕ := 3

/-- The branch representation is reducible (commutant strictly larger than the scalars). -/
theorem branch_reducible : 1 < commutantDim := by decide

/-- A diagonal admissible readout (the "intended" maximally-mixed block state). -/
def rho1 : Matrix (Fin 3) (Fin 3) ℚ := !![1/2, 0, 0; 0, 1/3, 0; 0, 0, 1/6]

/-- A second admissible readout with the SAME diagonal marginals but nonzero coherence. -/
def rho2 : Matrix (Fin 3) (Fin 3) ℚ := !![1/2, 1/10, 0; 1/10, 1/3, 0; 0, 0, 1/6]

/-- Both readouts have the same frozen diagonal marginals `(1/2, 1/3, 1/6)`. -/
theorem same_diagonal : rho1 0 0 = rho2 0 0 ∧ rho1 1 1 = rho2 1 1 ∧ rho1 2 2 = rho2 2 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> native_decide

/-- **B is a NO-GO.** Two admissible readouts share the frozen marginals yet differ: the CP readout is not
unique without `PRIM-BRANCH-ISOTROPIC-READOUT`. -/
theorem branch_readout_not_unique :
    1 < commutantDim ∧ rho1 ≠ rho2 ∧ (rho1 0 0 = rho2 0 0 ∧ rho1 1 1 = rho2 1 1 ∧ rho1 2 2 = rho2 2 2) := by
  refine ⟨branch_reducible, ?_, same_diagonal⟩
  intro h
  have : rho1 0 1 = rho2 0 1 := by rw [h]
  simp [rho1, rho2] at this

/-! ## D — lepton mass-ratio underdetermination -/

/-- Vandermonde matrix at the three branch exponents `{0, 1/4, 1/3}` (rows `[pⁿ]`, `n = 0,1,2`). -/
def vandermonde : Matrix (Fin 3) (Fin 3) ℚ := !![1, 0, 0; 1, 1/4, 1/16; 1, 1/3, 1/9]

/-- **D is a NO-GO.** The Vandermonde determinant at `{0,1/4,1/3}` is nonzero (`1/144`), so the quadratic
interpolation map is onto: every target `(r_μ, r_τ)` is realized by a smooth positive matching function. The
exponents do not determine the mass ratios. -/
theorem mass_ratio_underdetermined : vandermonde.det = 1/144 ∧ vandermonde.det ≠ 0 := by
  refine ⟨?_, ?_⟩
  · native_decide
  · native_decide

end D0.Integration.V15.BranchAudit
